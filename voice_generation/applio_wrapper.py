"""Python integration for RVC voice conversion with optional Edge-TTS input."""

import asyncio
import importlib.util
import os
import sys
from pathlib import Path
from threading import RLock
from typing import Any, Dict, List, Optional, Tuple

import yaml

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"


class ApplioWrapper:
    """Compatibility wrapper backed by the lightweight ``rvc-python`` package."""

    def __init__(self, config_path: Optional[str] = None):
        cfg_file = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
        if not cfg_file.exists():
            raise FileNotFoundError(f"Configuration file not found at: {cfg_file}")

        with cfg_file.open("r", encoding="utf-8") as handle:
            self.config = yaml.safe_load(handle) or {}

        self.gen_cfg = self.config.get("generation", {})
        self.models_cfg = self.config.get("models", {})
        self.defaults = self.config.get("inference_defaults", {})
        project_root = Path(__file__).resolve().parent.parent
        self.models_dir = Path(os.environ.get("RVC_MODELS_DIR", project_root / "models" / "rvc_voices"))
        self.device = os.environ.get("RVC_DEVICE", "")

        self.intermediate_tts_dir = Path(self.gen_cfg.get("intermediate_tts_dir", "data/intermediate_tts"))
        self.output_dir = Path(self.gen_cfg.get("output_dir", "data/synthetic_rvc"))
        self.intermediate_tts_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self._engine = None
        self._loaded_model: Optional[str] = None
        self._engine_lock = RLock()
        self._auto_discover_models()

    def _auto_discover_models(self) -> None:
        """Map each local speaker folder to its best checkpoint and optional index."""
        if not self.models_dir.is_dir():
            return

        for folder in self.models_dir.iterdir():
            if not folder.is_dir():
                continue
            model_name = folder.name.removesuffix("_rvc")
            checkpoints = [
                path for path in folder.glob("*.pth")
                if not path.name.startswith(("G_", "D_"))
            ]
            checkpoints.sort(
                key=lambda path: ("100e" in path.name.lower(), path.stat().st_mtime),
                reverse=True,
            )
            if not checkpoints:
                continue

            indices = sorted(folder.glob("*.index"))
            metadata = self.models_cfg.get(model_name, {})
            metadata["pth_file"] = str(checkpoints[0].relative_to(self.models_dir))
            metadata["index_file"] = str(indices[0].relative_to(self.models_dir)) if indices else ""
            self.models_cfg[model_name] = metadata

        for checkpoint in self.models_dir.glob("*.pth"):
            if checkpoint.name.startswith(("G_", "D_")):
                continue
            model_name = checkpoint.stem.removesuffix("_rvc")
            metadata = self.models_cfg.setdefault(model_name, {})
            metadata["pth_file"] = checkpoint.name
            indices = sorted(self.models_dir.glob(f"*{model_name}*.index"))
            metadata["index_file"] = indices[0].name if indices else ""

    def get_available_models(self) -> List[str]:
        self._auto_discover_models()
        return sorted(self.models_cfg)

    def get_status(self) -> Dict[str, Any]:
        """Report installed runtime pieces and local model files without loading PyTorch."""
        self._auto_discover_models()
        try:
            package_installed = importlib.util.find_spec("rvc_python") is not None
        except (ImportError, ValueError):
            package_installed = False
        try:
            torch_installed = importlib.util.find_spec("torch") is not None
        except (ImportError, ValueError):
            torch_installed = False

        models: Dict[str, Dict[str, bool]] = {}
        for model_name in sorted(self.models_cfg):
            metadata = self.models_cfg[model_name]
            pth = self.models_dir / metadata.get("pth_file", "")
            index_value = metadata.get("index_file", "")
            index = self.models_dir / index_value if index_value else None
            models[model_name] = {
                "weights": pth.is_file(),
                "index": bool(index and index.is_file()),
            }

        requested_models = [f"teammate{number:02d}" for number in range(1, 6)]
        all_weights_present = all(models.get(name, {}).get("weights", False) for name in requested_models)
        all_indexes_present = all(models.get(name, {}).get("index", False) for name in requested_models)
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        missing = []
        if sys.version_info >= (3, 13):
            missing.append("use Python 3.10–3.12 for this project (3.10 is recommended for RVC)")
        if not package_installed:
            missing.append("rvc-python is not installed")
        if not torch_installed:
            missing.append("PyTorch is not installed")
        if not all_weights_present:
            missing.append("one or more teammate .pth files are missing")
        if not all_indexes_present:
            missing.append("one or more teammate .index files are missing")
        ready = not missing
        return {
            "ready": ready,
            "python_version": python_version,
            "package_installed": package_installed,
            "pytorch_installed": torch_installed,
            "models_dir": str(self.models_dir),
            "device_preference": self.device or "auto",
            "models": models,
            "message": "RVC is ready" if ready else "; ".join(missing),
        }

    def validate_model(self, model_name: str) -> Tuple[Path, Optional[Path]]:
        self._auto_discover_models()
        if model_name not in self.models_cfg:
            raise KeyError(f"Model '{model_name}' not found under {self.models_dir}")

        metadata = self.models_cfg[model_name]
        pth_path = (self.models_dir / metadata["pth_file"]).resolve()
        if not pth_path.is_file():
            raise FileNotFoundError(f"RVC model weights (.pth) not found: {pth_path}")

        index_value = metadata.get("index_file", "")
        index_path = (self.models_dir / index_value).resolve() if index_value else None
        if index_path and not index_path.is_file():
            print(f"[WARNING] FAISS index not found at: {index_path}. Proceeding without index.")
            index_path = None
        return pth_path, index_path

    def _get_engine(self):
        if self._engine is None:
            try:
                import torch
                from rvc_python.infer import RVCInference
            except ImportError as exc:
                raise RuntimeError("RVC conversion requires the 'rvc-python' package and PyTorch") from exc

            device = self.device or ("cuda:0" if torch.cuda.is_available() else "cpu:0")
            self._engine = RVCInference(models_dir=str(self.models_dir), device=device)
        return self._engine

    def convert_audio(
        self,
        input_wav: str,
        model_name: str,
        out_path: str,
        **overrides: Any,
    ) -> str:
        """Convert source speech to the selected speaker using the local RVC v2 model."""
        in_file = Path(input_wav).resolve()
        if not in_file.is_file():
            raise FileNotFoundError(f"Source input audio not found: {in_file}")

        pth_path, index_path = self.validate_model(model_name)
        out_file = Path(out_path).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)

        with self._engine_lock:
            engine = self._get_engine()
            # Loading by explicit paths ensures the paired local index is used.
            if self._loaded_model != model_name:
                engine.load_model(
                    str(pth_path),
                    version=overrides.get("version", "v2"),
                    index_path=str(index_path) if index_path else "",
                )
                self._loaded_model = model_name
            engine.set_params(
                f0method=overrides.get("f0_method", self.defaults.get("f0_method", "rmvpe")),
                f0up_key=int(overrides.get("pitch", self.defaults.get("pitch", 0))),
                index_rate=float(overrides.get("index_rate", self.defaults.get("index_rate", 0.80))) if index_path else 0.0,
                protect=float(overrides.get("protect", self.defaults.get("protect", 0.33))),
            )
            engine.infer_file(str(in_file), str(out_file))

        if not out_file.is_file() or out_file.stat().st_size == 0:
            raise RuntimeError(f"RVC output was not generated at: {out_file}")
        return str(out_file)

    def text_to_rvc(
        self,
        text: str,
        model_name: str,
        out_path: str,
        tts_voice: Optional[str] = None,
        intermediate_tts_path: Optional[str] = None,
        **overrides: Any,
    ) -> Dict[str, str]:
        """Generate Edge-TTS source speech, then convert that file with local RVC."""
        import edge_tts
        import librosa
        import soundfile as sf

        out_file = Path(out_path).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)
        tts_file = (
            Path(intermediate_tts_path).resolve()
            if intermediate_tts_path
            else (self.intermediate_tts_dir / f"tts_{out_file.stem}.wav").resolve()
        )
        tts_file.parent.mkdir(parents=True, exist_ok=True)
        voice = tts_voice or self.models_cfg.get(model_name, {}).get("default_tts_voice", "en-IN-PrabhatNeural")
        tts_rate = int(overrides.get("tts_rate", self.defaults.get("tts_rate", 0)))
        rate_text = f"{tts_rate:+d}%"
        temp_mp3 = tts_file.with_suffix(".mp3")

        async def synthesize() -> None:
            await edge_tts.Communicate(text=text, voice=voice, rate=rate_text).save(str(temp_mp3))

        asyncio.run(synthesize())
        audio, sample_rate = librosa.load(str(temp_mp3), sr=16000, mono=True)
        sf.write(str(tts_file), audio, sample_rate, subtype="PCM_16")
        try:
            temp_mp3.unlink()
        except OSError:
            pass

        self.convert_audio(str(tts_file), model_name, str(out_file), **overrides)
        return {"output_rvc_path": str(out_file), "intermediate_tts_path": str(tts_file)}
