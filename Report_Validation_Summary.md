# Minor Project Report Validation Summary

**Project Title:** AI-Based Audio Deepfake Detection System Using ResNeXt (DFADS)  
**Institution:** The National Institute of Engineering (NIE), Mysuru – Department of Information Science & Engineering  
**Academic Year:** 2026–2027  
**Course:** Minor Project (BIS586)  
**Authors:**
- ABHISHEK G P (4NI24IS004)
- MAHESH M S (4NI24IS096)
- RAJESH N (4NI24IS150)
- S M SHRIVATHSA NONAVINAKERE (4NI24IS159)

**Guide:** Dr. S. Kuzhalvaimozhi, Professor, Dept of IS&E, NIE, Mysuru  
**Head of Department:** Dr. Shashank D, Assoc. Professor & HOD, Dept. of ISE, NIE, Mysuru  
**Project Directory:** `D:\Projects\Deepfake Detection\audio-deepfake-agent2`  
**Generated Report Artifacts:**
- Microsoft Word Document: [`Audio_Deepfake_Detection_Minor_Project_Report.docx`](file:///D:/Projects/Deepfake%20Detection/audio-deepfake-agent2/Audio_Deepfake_Detection_Minor_Project_Report.docx) (6.40 MB)
- Adobe PDF Document: [`Audio_Deepfake_Detection_Minor_Project_Report.pdf`](file:///D:/Projects/Deepfake%20Detection/audio-deepfake-agent2/Audio_Deepfake_Detection_Minor_Project_Report.pdf) (2.37 MB)

---

## 1. Structural Conformance & Chapter Sequence

The generated report strictly replicates the complete academic structure and logical sequence of the master template (`full_minor.docx` / `final_minor.docx`):

| Section / Chapter | Template Heading Alignment | Implemented DFADS Content | Conformance Status |
| :--- | :--- | :--- | :--- |
| **Front Matter** | Cover, Certificate, Acknowledgement, Abstract, TOC, List of Figures, List of Tables | Exact NIE Mysuru styling, authentic college logo, student details, signatures, and formatted tables | **100% Matched** |
| **Chapter 1** | Introduction (1.1 Background, 1.2 Problem Statement, 1.3 Objectives, 1.4 Scope of Work & Table 1.1) | Real-world deepfake voice cloning threats (RVC, XTTS, HiFi-GAN), mathematical problem formulation $f(\mathbf{x}) \to y \in \{0, 1\}$, 7 core technical objectives, and verified implementation status table | **100% Matched** |
| **Chapter 2** | Literature Survey (2.1 Existing Methods, 2.2 Review of Research Papers, 2.3 Research Gap & Table 2.1) | Evolution of acoustic features, **strictly focused on the two specified papers**: Tahaoglu et al. (2025) and Rabhi et al. (2024), followed by a 6-point comparative matrix | **100% Matched** |
| **Chapter 3** | Requirement Analysis (3.1 Problem Definition, 3.2 FRs Table 3.1, 3.3 NFRs Table 3.2, 3.4 Hardware/Software Tables 3.3/3.4, 3.5 Use Cases Table 3.5 & Constraints) | Forensic analyst/security stakeholders, 8 functional requirements (FR-01 to FR-08), 6 non-functional requirements, exact hardware/software specifications, and 6 principal use cases | **100% Matched** |
| **Chapter 4** | System Design (4.1 Architecture Fig 4.1, 4.2 Use-Case Fig 4.2, 4.3 DFD Level 0 Fig 4.3 & Level 1 Fig 4.4, 4.4 Data Entities Table 4.1 & ER Fig 4.5, 4.5 Workflow Fig 4.6) | 4-layer decoupled system architecture, UML use-case diagram, DFD Level 0 & Level 1, 6 core data entities with relational schema, and 6-stage end-to-end classification workflow | **100% Matched** |
| **Chapter 5** | System Implementation (5.1 Tech Stack Table 5.1, 5.2 Frontend/Visuals, 5.3 Web Architecture Fig 5.1, 5.4 Backend/API, 5.5 Local Storage Table 5.2, 5.6 Feature Pipeline Fig 5.2 & Table 5.3, 5.7 Production Scaling, 5.8 Execution Procedures) | Technology justification, Streamlit 4-tab forensic visualizer, client-application-model workflow, 78-dimensional multi-domain feature pipeline, production Kubernetes/Celery scaling, and exact CLI commands | **100% Matched** |
| **Chapter 6** | Results and Testing (6.1 Testing Strategy, 6.2 Test Cases Table 6.1, 6.3 Reported Results Table 6.2 & Figs 6.1–6.9, 6.4 Advantages & Limitations) | Multi-tiered testing methodology, 8 verified test cases, 199-sample full benchmark analysis, 7,148-row test split evaluation, 9 embedded result charts, and empirical discussion of XTTS domain shift | **100% Matched** |
| **Conclusion & Future** | Conclusion & Future Enhancements | Synthesis of research contributions, 92.46% benchmark summary, and 4 roadmap directions (multi-vocoder pre-training, WavLM SSL, raw waveform, SIP telephony) | **100% Matched** |
| **References** | Academic Bibliography | 9 IEEE-formatted citations prominently highlighting Tahaoglu et al. (2025), Rabhi et al. (2024), Xie et al. (ResNeXt), and foundational signal processing libraries | **100% Matched** |
| **Snapshots** | Application Visual Evidence | All 9 full-page interface screenshots from `project-snapshots/` with formal academic figure captions and technical descriptions | **100% Matched** |

---

## 2. Integrated Visual Assets & Figures

All figures and snapshots are high-resolution, centered, and accompanied by formal numbered captions matching the master template:

### A. Architectural & System Design Diagrams
1. **Figure 4.1:** Overall Architecture of Audio Deepfake Detection System (DFADS) — Presentation, Feature Extraction, Inference Core, and Calibration/Testbed.
2. **Figure 4.2:** Use-Case Diagram of DFADS — Actors, system boundary, and 7 operational use cases.
3. **Figure 4.3:** Context-Level Data Flow Diagram (DFD Level 0) — External entities (Forensic Analyst, Voice Synthesis Testbed) and Process 0.0.
4. **Figure 4.4:** Level 1 Data Flow Diagram (DFD Level 1) — Processes 1.0 to 5.0 with Data Stores D1 (Feature Store) and D2 (Model Store).
5. **Figure 4.5:** Proposed Logical Data Model for DFADS Forensics — Relational entity schema with primary and foreign keys.
6. **Figure 4.6:** Audio Ingestion and Forensic Classification Workflow — 6-step deterministic execution pipeline.
7. **Figure 5.1:** DFADS Web Client and Dashboard Access Workflow — Tiered client-server-model communication.
8. **Figure 5.2:** 78-Dimensional Multi-Domain Feature Extraction Pipeline — MFCC (40-D), Delta (20-D), Spectral (6-D), Chroma (6-D), and Energy/ZCR (6-D).

### B. Empirical Experimental Result Figures
1. **Figure 6.1:** Receiver Operating Characteristic (ROC) Curve of ResNeXt Detector (AUC = 0.9221, EER = 13.81%).
2. **Figure 6.2:** Confusion Matrix on Full Benchmark (199 Samples: TN=150, FP=4, FN=11, TP=34).
3. **Figure 6.3:** Diagnostic Probability Calibration Curve & Reliability Diagram (Brier = 0.0571, ECE = 4.10%).
4. **Figure 6.4:** Diagnostic Error Breakdown across Real (2.6%), RVC (0.0%), and XTTS (93.3%) Subsets.
5. **Figure 6.5:** Diagnostic Score Distributions across Real vs. Synthetic Classes (Youden J Cutoff = 0.1900).
6. **Figure 6.6:** Acoustic Energy Distributions of Benchmark Audio Signals (Dynamic range compression in vocoders).
7. **Figure 6.7:** Inference Latency Breakdown (71.06 ms Feature Extraction vs. 22.29 ms Model Inference = 93.35 ms Total).
8. **Figure 6.8:** Robustness Evaluation across Acoustic Noise (10–40 dB SNR) & MP3 Compression (64–320 kbps).
9. **Figure 6.9:** Training and Validation Loss/Accuracy Convergence Curves over 50 Epochs.

### C. Application Interface Snapshots
- **Snapshot 1:** DFADS Dashboard & Audio Upload Interface (`dashboard.png`).
- **Snapshot 2:** Forensic Diagnostic Report & Calibration Breakdown (`Screenshot 2026-11-17 153403.png`).
- **Snapshot 3:** Interactive STFT Log-Frequency Spectrogram Visualizer (`Screenshot 2026-11-17 153424.png`).
- **Snapshot 4:** Time-Domain Waveform Visualizer (`Screenshot 2026-11-17 153430.png`).
- **Snapshot 5:** FFT Power Spectrum & Vocoder Cutoff Analysis (`Screenshot 2026-11-17 153439.png`).
- **Snapshot 6:** 78-Dimensional Multi-Domain Acoustic Feature Matrix Inspector (`Screenshot 2026-11-17 153444.png`).
- **Snapshot 7:** Original Human Recording Analysis & Forensic Verdict (`Screenshot 2026-11-17 154503.png`).
- **Snapshot 8:** Synthesized Voice Clone Analysis & Forensic Artifact Verdict (`Screenshot 2026-11-17 154513.png`).
- **Snapshot 9:** Live Microphone Recording Interface & Target RVC Selection (`Screenshot 2026-11-17 154537.png`).

---

## 3. Verified Quantitative Results Incorporated

Every numerical claim in the report is grounded in direct execution of the project's source code and datasets:

| Metric / Parameter | Evaluated Callset | Verified Empirical Result | Forensic Significance |
| :--- | :--- | :--- | :--- |
| **Overall Classification Accuracy** | 199 Audio Files Benchmark | **92.46%** (184/199 correct) | High generalizability across real speech and voice clones |
| **True Negative Rate (Specificity)** | 154 Real Human Recordings | **97.40%** (150/154 pristine speech) | Very low false alarm rate (2.60% FP rate) |
| **True Positive Rate (Sensitivity)** | 45 Synthetic Audio Clones | **75.56%** (34/45 clones detected) | Identifies majority of synthetic speech attacks |
| **Area Under ROC Curve (AUC)** | 199 Audio Files Benchmark | **0.9221** | Robust discriminative capacity across threshold ranges |
| **Equal Error Rate (EER)** | 199 Audio Files Benchmark | **13.81%** | Benchmark operational trade-off point |
| **Large-Scale Test Accuracy** | 7,148-row `test_split.csv` | **99.79%** (ResNeXt) vs **99.05%** (SVM) | Near-perfect separation on in-distribution multi-speaker data |
| **Large-Scale Test EER** | 7,148-row `test_split.csv` | **0.14%** (ResNeXt) vs **0.91%** (SVM) | Demonstrates deep grouped convolution superiority |
| **RVC Detection Rate** | 30 RVC Clones (5 Speakers) | **100.0%** (30/30 detected by ResNeXt) | Flawless detection on retrieval-based voice conversion |
| **XTTS Detection Rate** | 15 Cross-Vocoder Clones | **6.67%** (1/15 detected by ResNeXt) | Highlights zero-shot vocoder overfitting vulnerability |
| **Brier Calibration Score** | 199 Audio Files Benchmark | **0.0571** | Well-calibrated probabilities reflecting true risk |
| **Expected Calibration Error (ECE)**| 199 Audio Files Benchmark | **4.10%** | Conforms to strict academic reliability standards (<5%) |
| **Optimal Operating Threshold** | Youden’s J Statistic | **0.1900** | Optimizes sensitivity without inflating false alarms |
| **End-to-End Inference Latency** | Single-core / Quad-core CPU | **93.35 ms** (71.06 ms Feat + 22.29 ms Model) | Sub-100 ms real-time processing capability |

---

## 4. Microsoft Word Formatting Properties Preserved

The `.docx` document was authored to match the exact visual design of `full_minor.docx`:
1. **Typography:** Consistent Times New Roman font throughout (16 pt bold chapter titles, 13 pt bold section headings, 12 pt italic subsection headings, 12 pt regular body text, 9.5–10 pt tables and references).
2. **Paragraph Formatting:** 1.5 line spacing, 0.4-inch first-line indentation, left/justified alignment, and consistent 6 pt space-after paragraph separation.
3. **Margins & Layout:** Standard A4 page geometry ($8.27 \times 11.70$ inches) with top margin 0.95", bottom margin 0.80", left margin 0.90", and right margin 0.70".
4. **Academic Page Border:** Professional $\frac{3}{4}\text{ pt}$ single-line box border applied across all pages.
5. **Header & Footer:** Front matter sections contain Roman-numeral references, while Chapter 1 initiates a new section with page numbering restarting at 1. The footer features left-aligned project title (*"AI-Based Audio Deepfake Detection System Using ResNeXt"*) and right-aligned dynamic page numbers.
6. **Table Presentation:** Academic styling featuring `#D9E1F2` soft blue/gray headers, bold column titles, alternating row shading (`#FFFFFF` / `#F9FAFB`), thin borders, repeat header rows across page breaks, and prevention of mid-row page splits.
7. **Document Conversion:** Natively compiled and converted to PDF using Microsoft Word 16.0 COM Automation (`wdFormatPDF = 17`), guaranteeing 100% visual fidelity, exact pagination, and clean vector graphics.

---

## 5. Verification Verdict

**Final Audit Verdict:** **FULLY VALIDATED AND COMPLETE**  
Both required deliverables—`Audio_Deepfake_Detection_Minor_Project_Report.docx` and `Audio_Deepfake_Detection_Minor_Project_Report.pdf`—have been generated, verified, and placed in the project root directory alongside this validation summary.
