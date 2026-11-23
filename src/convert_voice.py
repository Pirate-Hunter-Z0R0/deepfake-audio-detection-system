"""Run an RVC source-to-target conversion outside the Flask application."""

import argparse
import os
import sys
import time
from pathlib import Path

import soundfile as sf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from voice_generation.applio_wrapper import ApplioWrapper


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert one speech recording to an RVC teammate voice.")
    parser.add_argument("--input", required=True, help="Source speech WAV/audio file")
    parser.add_argument("--output-dir", default="results/rvc_conversions", help="Directory for converted WAVs")
    parser.add_argument(
        "--model",
        default="all",
        choices=["all", "teammate01", "teammate02", "teammate03", "teammate04", "teammate05"],
        help="Target voice to convert to, or all five for a quick comparison",
    )
    parser.add_argument("--device", choices=["auto", "cpu:0", "cuda:0"], default="auto")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.is_file():
        parser.error(f"Input audio file not found: {input_path}")

    if args.device != "auto":
        os.environ["RVC_DEVICE"] = args.device

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    wrapper = ApplioWrapper()
    status = wrapper.get_status()
    if not status["ready"]:
        print(f"RVC is not ready: {status['message']}")
        print(f"Python: {status['python_version']}")
        print(f"Installed package: {status['package_installed']}; PyTorch: {status['pytorch_installed']}")
        print(f"Models folder: {status['models_dir']}")
        return 2

    model_names = wrapper.get_available_models() if args.model == "all" else [args.model]
    errors = 0
    for model_name in model_names:
        output_path = output_dir / f"{input_path.stem}_{model_name}.wav"
        started = time.perf_counter()
        try:
            wrapper.convert_audio(str(input_path), model_name, str(output_path))
            info = sf.info(str(output_path))
            elapsed = time.perf_counter() - started
            print(
                f"OK {model_name}: {output_path} | {info.samplerate} Hz, "
                f"{info.duration:.2f} sec, {elapsed:.1f} sec processing"
            )
        except Exception as exc:
            errors += 1
            print(f"FAILED {model_name}: {exc}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
