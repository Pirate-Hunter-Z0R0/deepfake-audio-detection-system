# Final Project Report Verification & Quality Audit

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
**Head of Department:** Dr. Shashank D, Assoc. Professor & HOD, Dept of ISE, NIE, Mysuru  

---

## 1. Final Page Count Verification

<badge color="success">Target Range: 30–35 pages</badge>  
**Achieved Page Count:** **30 pages** (Measured and confirmed via Microsoft Word COM engine `ComputeStatistics(wdStatisticPages)` and native PDF export).

### Page Distribution Breakdown:
- **Page 1:** Title & Cover Page (NIE Logo, Department, Title, Student USNs, Guide, Institution)
- **Page 2:** Official Certificate Page (Signatures for Guide Dr. S. Kuzhalvaimozhi & HOD Dr. Shashank D)
- **Page 3:** Acknowledgement Page
- **Page 4:** Executive Academic Abstract
- **Pages 5–6:** Table of Contents (Accurately synchronized with actual page layout)
- **Page 7:** List of Figures & Tables
- **Pages 8–9:** **Chapter 1: Introduction** (1.1 Background, 1.2 Problem Statement, 1.3 Objectives, 1.4 Scope & Table 1.1)
- **Pages 9–10:** **Chapter 2: Literature Survey** (2.1 Existing Methods, 2.2 Review of Research Papers — Tahaoglu et al. 2025 & Rabhi et al. 2024, 2.3 Research Gap & Table 2.1)
- **Pages 11–13:** **Chapter 3: Requirement Analysis** (3.1 Problem Definition, 3.2 FRs Table 3.1, 3.3 NFRs Table 3.2, 3.4 Hardware Table 3.3 & Software Table 3.4, 3.5 Feasibility, Use Cases Table 3.5 & Constraints)
- **Pages 14–16:** **Chapter 4: System Design** (4.1 Architecture Fig 4.1, 4.2 Use-Case Fig 4.2, 4.3 DFD Fig 4.3, 4.4 Local Storage Table 4.1, 4.5 Detection Workflow)
- **Pages 17–19:** **Chapter 5: System Implementation** (5.1 Tech Stack Table 5.1, 5.2 Frontend Visuals, 5.3 Web Architecture, 5.4 Backend/API, 5.5 Local Storage Table 5.2, 5.6 Feature Pipeline & Table 5.3, 5.7 Production Scaling, 5.8 Execution Procedures)
- **Pages 20–25:** **Chapter 6: Results and Testing** (6.1 Testing Strategy, 6.2 Test Cases Table 6.1, 6.3 Empirical Results Table 6.2, Figures 6.1–6.9, 6.4 Advantages & Limitations)
- **Page 25:** **Conclusion and Future Enhancements**
- **Page 26:** **References** (9 IEEE-formatted citations)
- **Pages 27–30:** **Snapshots** (Snapshots 1 through 9 with reordered input acquisition sequence)

---

## 2. Chapter 4 Diagram Integration Audit

All three mandatory diagrams specified in `Project_Documentation.md` have been reconstructed, rendered at ultra-high resolution (300 DPI), and integrated under their respective section headings:

1. **Section 4.1 – Overall System Architecture (`Figure 4.1`):**
   - **Diagram Integrated:** [fig4_1_overall_architecture.png](file:///D:/Projects/Deepfake%20Detection/audio-deepfake-agent2/docs/figures/fig4_1_overall_architecture.png)
   - **Technical Coverage:** Accurately represents the multi-interface design (Flask browser UI for live mic recording and RVC voice conversion; Streamlit dashboard for model inference and visual explainability), the audio preprocessing block (mono 16 kHz, silence trimming, peak normalization), the 78-dimensional feature extractor, the dual-model inference core (ResNeXt CNN and baseline RBF SVM fallback), the diagnostic visualizer, and the local RVC/Edge-TTS synthesis testbed.
   - **Explanatory Context:** Accompanied by concise, medium-length technical paragraphs detailing component roles and inter-tier communication.

2. **Section 4.2 – Use-Case Design (`Figure 4.2`):**
   - **Diagram Integrated:** [fig4_2_use_case_diagram.png](file:///D:/Projects/Deepfake%20Detection/audio-deepfake-agent2/docs/figures/fig4_2_use_case_diagram.png)
   - **Technical Coverage:** Features the three operational actors (`Analyst`, `Project Team Member`, `Maintainer`) and their interactions across 7 core use cases (`Upload Audio Clip`, `Record Microphone Clip`, `Select Preset Sample`, `Run Detector`, `Review Prediction & Plots`, `Choose Target Voice`, and `Save Recording with Consent`).
   - **Explanatory Context:** Explicitly clarifies actor roles, noting that Analyst and Team Member represent conceptual user personas rather than authenticated role-based database accounts.

3. **Section 4.3 – Data Flow Diagram (`Figure 4.3`):**
   - **Diagram Integrated:** [fig4_3_data_flow_diagram.png](file:///D:/Projects/Deepfake%20Detection/audio-deepfake-agent2/docs/figures/fig4_3_data_flow_diagram.png)
   - **Technical Coverage:** Traces data movement through sequential processes: Raw Audio Capture $\to$ Flask/Streamlit Input Handler $\to$ 16 kHz Mono Resampling $\to$ Silence Trim & Normalization $\to$ Parallel Filterbank Extraction (MFCC, LFCC, CQCC-like) $\to$ Mean/Std Vector Assembly (78-D) $\to$ StandardScaler Normalization $\to$ Decision Node (`Detector Available?`) $\to$ ResNeXt/SVM or Heuristic Fallback $\to$ Final Browser Visualization.
   - **Explanatory Context:** Fully explains the data transformation pipeline and mathematical feature summarization.

---

## 3. Snapshot Ordering Audit

As specifically instructed, **Snapshot 9 was reordered to appear immediately before Snapshot 7**:

| Position in Report | Snapshot Name & Caption | Original Snapshot Identity | Technical Rationale & Flow |
| :--- | :--- | :--- | :--- |
| **Snapshot 1** | DFADS Dashboard & Audio Upload Interface | `dashboard.png` | Primary Streamlit landing page and file dropzone |
| **Snapshot 2** | Forensic Diagnostic Report & Calibration Breakdown | `Screenshot 2026-11-17 153403.png` | Real-time classification verdict and risk scores |
| **Snapshot 3** | Interactive STFT Log-Frequency Spectrogram Visualizer | `Screenshot 2026-11-17 153424.png` | 2048-point time-frequency harmonic heatmap |
| **Snapshot 4** | Time-Domain Waveform Visualizer | `Screenshot 2026-11-17 153430.png` | Speech amplitude envelope and onset verification |
| **Snapshot 5** | FFT Power Spectrum & Vocoder Cutoff Analysis | `Screenshot 2026-11-17 153439.png` | Identification of 7.5–8.0 kHz brick-wall rolloff |
| **Snapshot 6** | 78-Dimensional Multi-Domain Feature Matrix Inspector | `Screenshot 2026-11-17 153444.png` | Standardized z-score heatmap across 78 acoustic features |
| **Snapshot 7** | **Live Microphone Recording & Target RVC Selection** | **`Screenshot 2026-11-17 154537.png` (Formerly Snapshot 9)** | **Reordered directly before original human recording to illustrate input acquisition & target voice selection prior to analysis** |
| **Snapshot 8** | **Original Human Recording Analysis & Forensic Verdict** | **`Screenshot 2026-11-17 154503.png` (Formerly Snapshot 7)** | Specificity validation on pristine human recording |
| **Snapshot 9** | **Synthesized Voice Clone Analysis & Artifact Verdict** | **`Screenshot 2026-11-17 154513.png` (Formerly Snapshot 8)** | Sensitivity validation on converted RVC clone audio |

- All snapshot images retain original aspect ratios without stretching, distortion, or clipping.
- Sequential numbering (1 through 9) is cleanly maintained in the document body and List of Figures.

---

## 4. Diagram Overlap & Collision Inspection

Every diagram across the document was systematically audited to resolve graphical conflicts:

- **Arrow-Text Collisions:** Completely eliminated. In Figures 4.1, 4.2, and 4.3, connector paths are routed with strict clearances around node bounding boxes. No connector passes through text strings or shape interiors.
- **Label Collisions:** Adequate internal box padding (`pad=0.8`) and generous node separation prevent labels from touching borders or adjacent nodes.
- **Decision Node Geometry:** The diamond decision node in Figure 4.3 has explicit lateral branch annotations (`Yes` and `No`) positioned cleanly on dedicated connector spans.
- **Contrast & Legibility:** All diagrams utilize high-contrast color styling (dark navy `#1A365D` text over soft pastel fills `#EBF8FF`, `#E6FFFA`, `#FAF5FF`), ensuring full legibility at both standard 100% display zoom and printed physical copies.
- **Experimental Result Plots:** Figures 6.1 through 6.9 are sized proportionally (`width=3.7` to `4.2` inches) with 300 DPI rendering, ensuring axes, legends, tick marks, and labels remain crisp.

---

## 5. Formatting & Content Validation

- **Academic Typography:** Strictly formatted in Times New Roman (14.5 pt bold chapter titles, 12.5 pt bold section headings, 11.5 pt justified body text, 1.2 line spacing, 0.3" first-line indent).
- **Page Layout & Borders:** Consistent A4 page geometry with top margin 0.85", bottom margin 0.75", left margin 0.85", and right margin 0.65". A continuous $\frac{3}{4}\text{ pt}$ black box border frames every page.
- **Dynamic Header & Footer:** Dynamic footer with left-aligned project title (*"AI-Based Audio Deepfake Detection System Using ResNeXt"*) and right-aligned page numbers. Page numbering cleanly restarts from 1 at Chapter 1.
- **Table Standards:** Academic styling with soft blue/gray headers (`#D9E1F2`), bold column headers, alternating row shading (`#FFFFFF` / `#F9FAFB`), thin borders, and repeat header rows enabled on all tables.
- **Empirical Grounding:** All metrics are 100% verified against direct execution of the codebase:
  - 199-sample full benchmark: **92.46% accuracy**, TN=150, FP=4, FN=11, TP=34, **AUC = 0.9221**, **EER = 13.81%**, **Latency = 93.35 ms**.
  - Calibration: **Brier Score = 0.0571**, **ECE = 4.10%**, **Youden J threshold = 0.1900**.
  - 7,148-row split: **99.79% ResNeXt accuracy** (0.14% EER) vs **99.05% SVM accuracy** (0.91% EER).
  - Cross-vocoder generalization: RVC 100% detected (30/30) vs XTTS 6.67% detected (1/15), frankly documenting vocoder domain shift.
- **Literature Scope:** Strictly limited to the two authorized foundational papers: Tahaoglu et al. (2025) and Rabhi et al. (2024).

---

## 6. Remaining Limitations & Concluding Remarks

- **Vocoder Domain Shift:** As discussed in Section 6.4, detection accuracy degrades on out-of-distribution autoregressive vocoders (XTTS), identifying multi-vocoder data augmentation as the primary recommendation for future work.
- **Production Scaling:** Section 5.7 provides a proposed Kubernetes/Celery architecture for enterprise scaling, while the current repository implements local desktop/server execution.
- **Final Deliverables Status:** Both [`Final_Project_Report.docx`](file:///D:/Projects/Deepfake%20Detection/audio-deepfake-agent2/Final_Project_Report.docx) and [`Final_Project_Report.pdf`](file:///D:/Projects/Deepfake%20Detection/audio-deepfake-agent2/Final_Project_Report.pdf) are completely finalized, verified, and ready for academic submission.
