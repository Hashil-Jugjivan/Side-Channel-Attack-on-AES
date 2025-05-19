# 🔓 Side-Channel Attack on AES-128 (Correlation Power Analysis)

> **Educational project** demonstrating how unintended power‑consumption leakages in hardware can be exploited to recover a full 128‑bit AES key with **Correlation Power Analysis (CPA)**.

---

## Table of Contents
1. [Overview](#overview)
2. [Attack Workflow](#attack-workflow)
3. [Repository Layout](#repository-layout)
4. [Prerequisites](#prerequisites)
5. [Running the Attack](#running-the-attack)
6. [Results](#results)
7. [Mitigation & Defensive Notes](#mitigation--defensive-notes)
8. [License](#license)

---

## Overview

Modern ciphers such as **AES‑128** are mathematically robust, yet a careless *physical* implementation can leak secrets through side‑channels.  
In this project you will:

* Capture **110** power traces from an embedded device while it encrypts random plaintexts.
* Build a **Hamming‑weight leakage model** for every key‑byte hypothesis (`0x00–0xFF`).
* Sweep **2 500** sampling points per trace, computing the **Pearson correlation** between predicted and measured leakages.
* Identify the key byte whose model yields the **highest correlation spike** ➜ repeat 16 × ➜ recover the entire AES key.

A complete methodology, hardware description, and mathematical background are documented in the accompanying lab report.

---

## Attack Workflow

| # | Stage | Description |
|---|-------|-------------|
| 1 | **Trace Collection** | UART script sends random 16‑byte plaintext to target; oscilloscope (triggered on GPIO) records ~2 500 sample points of V<sub>dd</sub> per encryption. |
| 2 | **Leakage Modelling** | For a key‑byte guess `k`, compute `HW(SBox(PT_byte ⊕ k))` for all plaintexts as the expected power consumption. |
| 3 | **CPA Sweep** | For each time index *t*, correlate the predicted leakage vector with the measured power at *t*. |
| 4 | **Key‑Byte Decision** | The guess `k*` yielding the max \|ρ\| peak is deemed correct. |
| 5 | **Full‑Key Recovery** | Loop over 16 byte positions ➜ obtain the 128‑bit key. |

> **Compute load**: 256 guesses × 2 500 points × 110 traces ≈ **640 k** correlations per byte (≈ 10 M for full key).

---

## Repository Layout

```text
Side-Channel-Attack-on-AES/
│
├── cpa_implementation.py     # Core CPA script
├── waveform.csv              # 110 traces × 2 500 pts + PT/CT columns
├── CPS_Side-Channel_Analysis_Report.pdf
└── README.md                 # You are here
```

---

## Prerequisites

| Requirement | Tested Version |
|-------------|---------------|
| Python      | 3.8 – 3.12 |
| NumPy       | ≥ 1.23 |
| SciPy       | ≥ 1.9 |
| Matplotlib  | ≥ 3.6 |

```bash
python -m venv .venv
source .venv/bin/activate      # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
# or
pip install numpy scipy matplotlib
```

---

## Running the Attack

```bash
python cpa_implementation.py
```

Example output (truncated):

```
Traces: 110, Points: 2502
Byte 0: 0x48 at t= 513  (|ρ|=0.573)
Byte 1: 0x9D at t= 613  (|ρ|=0.626)
…
Byte15: 0xB7 at t=2014  (|ρ|=0.552)

Recovered AES‑128 Key:
48 9D B4 B3 F3 17 29 61 CC 2B CB 4E D2 E2 8E B7
```

Uncomment the plotting block in the script to generate correlation heat‑maps.

---

## Results

* **100 % byte‑level success** with only **110 traces**.  
* Correlation spikes align with the AddRoundKey ➜ S‑Box schedule.  
* Key verified against reference AES implementation.

---

## Mitigation & Defensive Notes

| Category | Countermeasure |
|----------|----------------|
| **Masking** | Random masks decorrelate intermediates from the real key. |
| **Hiding**  | Constant‑time S‑Boxes, current flatteners reduce amplitude. |
| **Randomisation** | Clock/voltage jitter misaligns traces and lowers SNR. |
| **Verification** | Integrate leakage tests (TVLA, CPA) into silicon validation. |

---

## License

Released under the **MIT License** – see `LICENSE` for details.  
Educational use only. **Do not** attack devices you don’t own or lack permission to test.

---
  
