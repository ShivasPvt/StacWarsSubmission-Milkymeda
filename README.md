# StacWarsSubmission-Milkymeda

**Team MilkyMeda** · STAC WARS (Astronomy Club Freshers Hackathon) submission

*May the Code Be With You.*

---

## Repository structure

```
.
├── ps1/                         PS1
│   ├── MilkyMeda_ Report.pdf      report
│   ├── MilkyMeda_flightdata.csv   flight data
│   └── rocket.ork                 OpenRocket design file
├── ps2/                         PS2 – Solar Radiation Analysis and Prediction
│   ├── PS2_Solar_Radiation_AnalysisReal.py   code (Parts A, B, C + ML bonus)
│   ├── PS2_Report.pdf                        report: plots, inferences, scores
│   ├── figures/                              all plots (PNG)
│   ├── daily_report.csv                      day-wise solar report (Part C)
│   ├── SolarPrediction.csv                   dataset
│   └── requirements.txt
└── ps3/                         PS3 – Exoplanet Hunters
    ├── code/                      stac_ps3.py, check_answers.py, plot_graphs.py, run_all.bat
    ├── report/STAC_PS3_Report.pdf report
    ├── presentation/              Operation-Dim-Starbyb.pptx
    ├── time/light_curves.png      light-curve plot
    └── requirements.txt
```

---

## PS1

- 📄 Report: [`ps1/MilkyMeda_ Report.pdf`](ps1/MilkyMeda_%20Report.pdf)
- 📈 Flight data: [`ps1/MilkyMeda_flightdata.csv`](ps1/MilkyMeda_flightdata.csv)
- 🚀 Rocket design (open in OpenRocket): [`ps1/rocket.ork`](ps1/rocket.ork)

---

## PS2 – Solar Radiation Analysis and Prediction

- 💻 Code: [`ps2/PS2_Solar_Radiation_AnalysisReal.py`](ps2/PS2_Solar_Radiation_AnalysisReal.py)
- 📄 Report: [`ps2/PS2_Report.pdf`](ps2/PS2_Report.pdf)
- 📊 Plots: [`ps2/figures/`](ps2/figures)
- 🗓️ Day-wise report: [`ps2/daily_report.csv`](ps2/daily_report.csv)

### How to run
```bash
cd ps2
pip install -r requirements.txt
python PS2_Solar_Radiation_AnalysisReal.py
```
The script prints every result and saves all plots to `ps2/figures/` and the day-wise report to `ps2/daily_report.csv`.

### Key results
| | |
|---|---|
| Peak radiation time | 11:00–13:00 (best hour 12:00, mean 727 W/m²; median daily peak 12:15) |
| Strongest related parameter | Temperature, r = +0.73 (humidity −0.23 overall, −0.39 in daylight) |
| Record day | 4 Sep 2016 – 1,601.26 W/m² at 12:15:04 (61 °F, 93 % humidity, 9.0 mph wind), 6 h 07 min after sunrise |
| Top 5 days by average radiation | 19 Sep, 2 Sep, 22 Sep, 25 Sep, 28 Sep |
| ML model (bonus) | Gradient Boosting, tested on 24 unseen days: **RMSE 108.7 W/m², R² 0.873** |
| Most useful features | Sun position (SunPos), time of day, humidity |

The model is evaluated on **whole held-out days** (94 days train / 24 days test), so neighbouring 5-minute readings cannot leak from training into testing.

---

## PS3 – Exoplanet Hunters

- 💻 Code: [`ps3/code/`](ps3/code) – `stac_ps3.py`, `check_answers.py`, `plot_graphs.py`
- 📄 Report: [`ps3/report/STAC_PS3_Report.pdf`](ps3/report/STAC_PS3_Report.pdf)
- 🖥️ Presentation: [`ps3/presentation/Operation-Dim-Starbyb.pptx`](ps3/presentation/Operation-Dim-Starbyb.pptx)
- 📈 Light curves: [`ps3/time/light_curves.png`](ps3/time/light_curves.png)

### How to run
```bash
cd ps3/code
pip install -r ../requirements.txt
python stac_ps3.py
python check_answers.py
python plot_graphs.py
```
On Windows you can also double-click `run_all.bat`.
