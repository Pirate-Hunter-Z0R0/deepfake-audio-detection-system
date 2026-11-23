# AI Agent Seed Prompt & Architectural Blueprint

> **How to use this file:**  
> When starting a conversation with your new AI coding agent (Cursor, Claude Code, Windsurf, Aider, etc.), **copy and paste the prompt below as your first message**. It primes the agent with 100% of the project's context in ~600 tokens, preventing it from wasting tens of thousands of tokens exploring files or hallucinating code.

---

### 📋 Copy & Paste This into Your Other AI Agent:

```markdown
You are assisting me on the **Audio Deepfake Detection System (DFADS)** project located in this workspace.

### Core Architecture & Key Details:
1. **Goal**: Detect synthetic/cloned speech (deepfakes) vs genuine human speech in real-time.
2. **Feature Domain (78-dimensional vector)**:
   - 26 Mel-Frequency Cepstral Coefficients (MFCC: 13 mean + 13 std)
   - 26 Linear-Frequency Cepstral Coefficients (LFCC: 13 mean + 13 std)
   - 26 Constant-Q Cepstral Coefficients (CQCC: 13 mean + 13 std)
   - Reshaped into a (6, 13, 1) spectral feature matrix for grouped convolutions.
3. **Detection Engines**:
   - Primary: Deep ResNeXt CNN (Grouped Convolutions with Cardinality C=4, Bottleneck transformations).
   - Resilient Fallback: Pre-trained RBF Kernel Support Vector Machine (`models/adapted_baseline_model.pkl`).
4. **Interactive Web Application (`app/app.py` & `app/templates/index.html`)**:
   - Port: 5000 (`http://localhost:5000`)
   - Interactive STFT Log-Frequency Spectrogram with Magma colormap (+0 dB to -80 dB, octave ticks 512, 1024, 2048, 4096, 8192 Hz, real-time mouse crosshair hover inspection).
   - In-browser 16 kHz PCM WAV microphone capture (zero external ffmpeg dependency).
   - Edge-TTS multi-speaker adversarial voice cloning simulator (`teammate01` to `teammate05`).
5. **Key Folders**:
   - `app/`: Flask web application and UI templates.
   - `src/`: Training, evaluation, feature extraction, and diagnostic scripts.
   - `models/`: Trained model binaries (`adapted_baseline_model.pkl`, `adapted_resnext_scaler.pkl`).
   - `reports/`: Complete formal academic project reports (`.docx`).
   - `results/`: Benchmark evaluations, confusion matrices, ROC curves, calibration charts.

Please inspect only the files relevant to the specific tasks I assign. Do not re-architect or rewrite working components from scratch.
```

---

### 📂 Quick Workspace Map:
* **Launch App**: `python app/app.py` (models are pre-loaded; runs immediately)
* **Streamlit Pro Dashboard**: `streamlit run streamlit_app.py`
* **Retrain Adapted Model**: `python src/train_adapted_model.py`
* **Evaluate Benchmark**: `python src/compute_step2_metrics.py`
