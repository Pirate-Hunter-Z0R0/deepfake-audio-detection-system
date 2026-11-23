# AI Based Audio Deepfake Detection

An end-to-end forensic verification pipeline designed to detect AI-generated voice clones and neural speech deepfakes in milliseconds. The system extracts a standardized 78-dimensional multi-domain acoustic feature representation — combining Mel-Frequency Cepstral Coefficients (MFCC), Linear-Frequency Cepstral Coefficients (LFCC), and Constant-Q Cepstral Coefficients (CQCC) — to evaluate audio across a deep ResNeXt neural architecture featuring grouped convolutions ($C=32$) and an RBF Support Vector Machine (SVM) baseline for dual-model consensus verification. 

The project incorporates post-hoc probability calibration (Platt scaling & Youden's $J$ optimization), an explainability studio with interactive STFT log-frequency spectrograms and FFT vocoder cutoff analyzers, an Applio RVC v2 voice conversion testbed, and an intuitive Streamlit web application.

---

## 👥 Project Team & Academic Affiliation

**The National Institute of Engineering (NIE), Mysuru**  
*Department of Information Science & Engineering*  
*Minor Project (BIS586) — Academic Year 2026–2027*

* **Team Members:**
  * Sameer Kumar (`4NI24IS168`)
  * Tharun T L (`4NI24IS239`)
  * Dhanush K P (`4NI24IS242`)
  * Abhinand P (`4NI24IS244`)
---

## 📁 Repository Structure

```text
audio-deepfake-agent2/
├── data/
│   ├── features/               # Standardized feature databases (78 columns)
│   │   ├── features.csv        # 35,740 extracted feature vectors
│   │   ├── features.npy        # NumPy binary representation
│   │   └── test_split.csv      # Standardized 20% test split (7,148 samples)
│   ├── real_recordings/        # Authentic multi-speaker human control recordings
│   └── synthetic_rvc/          # Synthesized RVC v2 / XTTS test clips
├── models/
│   ├── adapted_deep_model.weights.h5 # Trained ResNeXt model weights (281K params)
│   ├── baseline_model.pkl      # Calibrated RBF Support Vector Machine (SVM)
│   ├── scaler.pkl              # Fitted StandardScaler (78-D feature normalization)
│   └── rvc_voices/             # Local RVC v2 voice models and FAISS retrieval index profiles
├── src/
│   ├── preprocessing.py        # Audio decoding, mono 16 kHz resample, trim & peak normalization
│   ├── feature_extraction.py   # Multi-domain 78-D feature extraction (MFCC, LFCC, CQCC)
│   ├── train_baseline.py       # Baseline ML model training (RBF SVM, Random Forest, Logistic Reg)
│   ├── train_deep_model.py     # Grouped-convolution ResNeXt CNN training (TensorFlow/Keras)
│   ├── compute_step2_metrics.py# 199-sample multi-vocoder benchmark evaluation script
│   ├── diagnose_misclassifications.py # Platt calibration, Brier score, ECE & error diagnostics
│   ├── evaluate.py             # Accuracy, Precision, Recall, F1, ROC AUC, and EER computation
│   └── robustness_test.py      # Noise (SNR), MP3 compression, and time perturbation stress tests
├── app/
│   ├── app.py                  # Flask REST API service and voice conversion route (Port 5000)
│   ├── templates/index.html    # Web ingestion interface
│   └── static/                 # Upload buffers and temporary WAV playback files
├── streamlit_app.py            # Primary Interactive Forensic Dashboard (Port 8501)
├── results/
│   ├── evaluation_metrics.json # Full benchmark empirical metric outputs
│   ├── roc_curve.png           # Receiver Operating Characteristic curve (AUC = 0.9221)
│   ├── confusion_matrix.png    # 199-sample forensic confusion matrix
│   ├── calibration_curve.png   # Reliability diagram (ECE = 4.10%, Brier = 0.0571)
│   ├── latency_breakdown.png   # Latency profile (93.35 ms average end-to-end)
│   └── robustness_chart.png    # Perturbation degradation bar charts
├── requirements.txt            # Python dependencies (TensorFlow 2.12, Librosa, Scikit-Learn)
└── README.md                   # This project guide
```

> **Note on Raw Audio:** To optimize disk storage, the 5+ GB of downloaded raw audio files in `data/raw/` and `data/processed/` were safely removed after feature extraction. The pipeline operates directly on the pre-computed 78-D feature stores (`data/features/`) and active benchmark audio (`data/real_recordings/` & `data/synthetic_rvc/`).

---

## 🔬 System Architecture & Methodology

1. **Acoustic Conditioning (16 kHz):**
   * Decodes incoming audio (`.wav`, `.mp3`, `.flac`), downmixes multi-channel input to mono, standardizes sampling rate to exactly **16,000 Hz**, removes leading/trailing silence, and applies peak-amplitude normalization.

2. **78-Dimensional Multi-Domain Feature Extraction:**
   * **MFCC (26 features):** 13 mean + 13 standard deviation coefficients capturing the vocal-tract spectral envelope.
   * **LFCC (26 features):** 13 mean + 13 standard deviation coefficients using linear filterbanks to capture high-frequency vocoder cues.
   * **CQCC-like (26 features):** 13 mean + 13 standard deviation coefficients using geometrically spaced octave filterbanks to detect pitch/harmonic synthetic artifacts.
   * All 78 dimensions are normalized using a pre-fitted `StandardScaler`.

3. **Grouped Convolutional ResNeXt Architecture:**
   * Formulates feature vectors into structured 2D representations processed across parallel bottleneck pathways with **cardinality $C=32$** and residual skip connections.
   * Total parameter count: **281,409 weights (~1.1 MB checkpoint)**, making it suited for CPU-based real-time deployment without GPU dependencies.

4. **Probabilistic Calibration:**
   * Raw deep neural network logits are post-processed via **Platt scaling** (logistic sigmoid calibration) to eliminate over-confident predictions.
   * Optimal operational classification threshold is established at **0.1900** via **Youden's $J$ statistic**.

---

## 📊 Empirical Results & Benchmarks

### 1. Large-Scale Standardized Split (7,148 Samples)
Evaluated on the held-out 20% test split:

| Model Architecture | Accuracy | Equal Error Rate (EER) | ROC AUC | Parameters |
| :--- | :---: | :---: | :---: | :---: |
| **ResNeXt Deep CNN** | **99.79%** | **0.14%** | **1.0000** | **281,409** |
| Baseline RBF SVM | 99.05% | 0.91% | 0.9996 | — |
| Random Forest | 98.42% | 1.84% | 0.9982 | — |
| Logistic Regression | 93.18% | 6.82% | 0.9812 | — |

### 2. Multi-Vocoder Real-World Benchmark (199 Samples)
Independent test set consisting of 154 pristine human recordings, 30 RVC v2 clones, and 15 cross-vocoder XTTS samples:

* **Overall Accuracy:** **92.46%**
* **ROC AUC:** **0.9221** | **Equal Error Rate (EER):** **13.81%**
* **True Negative Rate (Pristine Human):** **97.40%** (150 / 154 correctly classified; 4 false alarms)
* **True Positive Rate (Voice Clones):** **75.56%** (34 / 45 correctly classified)
  * **RVC v2 In-Distribution Clones:** **100.0% Detection Rate** (30 / 30 detected)
  * **XTTS Out-of-Distribution Clones:** **6.67% Detection Rate** (1 / 15 detected — demonstrates cross-vocoder domain shift)
* **Calibration Metrics:** **Brier Score = 0.0571** | **Expected Calibration Error (ECE) = 4.10%**
* **End-to-End Latency (CPU):** **93.35 ms average per sample** (71.06 ms feature extraction + 22.29 ms neural inference)

---

## 🛠️ Installation & Execution

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/Pirate-Hunter-Z0R0/audio-deepfake-detection.git
cd audio-deepfake-agent2

# Create and activate virtual environment (Python 3.10 recommended)
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Running the Interactive Applications

#### Primary Forensic Dashboard (Streamlit):
```bash
streamlit run streamlit_app.py
```
* Opens at **http://localhost:8501**.
* Features drag-and-drop file upload, live microphone recording, instant Real vs. Deepfake verdict with calibrated risk confidence, and interactive STFT spectrogram / FFT power spectrum displays.

#### Web Service & Voice Cloning Testbed (Flask):
```bash
python app/app.py
```
* Opens at **http://localhost:5000**.
* Provides the REST API and live microphone target voice conversion routes powered by Applio RVC v2.

### 3. Reproducing Experimental Benchmarks

```bash
# Evaluate the 199-sample benchmark & verify the 92.46% accuracy:
python src/compute_step2_metrics.py

# Regenerate calibration curves, reliability diagrams, and error breakdowns:
python src/diagnose_misclassifications.py

# Evaluate test split baseline vs deep model:
python src/evaluate.py --model-path models/adapted_deep_model.weights.h5 --model-type deep

# Run noise and compression perturbation tests:
python src/robustness_test.py
```

---

## 📚 Key Literature References

1. **Tahaoglu, M., Acar, S. K., & Cetin, O. (2025).** *"Audio Deepfake Detection Using Multi-Domain Spectral Features and Grouped Convolutional Networks,"* IEEE Transactions on Information Forensics and Security, vol. 20, pp. 112–126.
2. **Rabhi, M., Bakiras, E., & Di Pietro, R. (2024).** *"Adversarial Attacks and Defenses on Deepfake Audio Detection: A Robustness and Generalization Survey,"* ACM Computing Surveys, vol. 56, no. 8, pp. 1–38.
3. **Xie, S., Girshick, R., Dollár, P., Tu, Z., & He, K. (2017).** *"Aggregated Residual Transformations for Deep Neural Networks,"* in IEEE CVPR, pp. 1492–1500.

---

## 📄 License

This project is developed for academic evaluation purposes under the Bachelor of Engineering curriculum at **The National Institute of Engineering, Mysuru**.
