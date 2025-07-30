# NLDAS-3 WBGT Pipeline

This repository contains a complete pipeline to calculate Wet Bulb Globe Temperature (WBGT) using NASA’s NLDAS-3 meteorological data. The WBGT is a comprehensive index for assessing heat stress by accounting for temperature, humidity, solar radiation, and wind.

## Features

- Access hourly NLDAS-3 forcing data from AWS
- Coarsen spatial resolution to 5 km
- Calculate WBGT using the Liljegren et al. (2008) model
- Save daily outputs and summary statistics
- Visualize WBGT spatial maps

## 📂 Project Structure

```
.
├── access_nldas3_data.py       # Example script to access NLDAS-3 data
├── process_to_5km.py           # Coarsen data to ~5km resolution
├── calculate_wbgt.py           # Apply Liljegren WBGT model
├── visualize_wbgt.py           # Plot WBGT output maps
├── wbgt_pipeline_master.py     # FULL end-to-end pipeline (recommended)
├── requirements.txt            # Install dependencies
└── README.md
```

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the full pipeline:
```bash
python wbgt_pipeline_master.py
```

3. Outputs are saved in `output_wbgt/`:
   - One `.nc` file per day
   - `wbgt_daily_summary.csv` for mean WBGT values

## References

- [NASA NLDAS-3](https://ldas.gsfc.nasa.gov/nldas/v3)
- [Liljegren et al. 2008](https://pubmed.ncbi.nlm.nih.gov/18668494/)
- [PyWBGT GitHub](https://github.com/QINQINKONG/PyWBGT)
