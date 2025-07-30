
# wbgt_pipeline_master.py

"""
Enhanced end-to-end WBGT calculation pipeline using NLDAS-3 data (via AWS S3).
Includes:
- Multi-year looping
- 5km spatial aggregation
- WBGT calculation using Liljegren model
- Daily NetCDF outputs + CSV summary
"""

import os
import xarray as xr
import pandas as pd
import s3fs
from pywbgt import wbgt_outdoor
from datetime import datetime, timedelta

# ---------------------------
# USER SETTINGS
# ---------------------------
START_DATE = "2020-07-01"
END_DATE = "2020-07-03"  # Extend this for longer runs
OUTPUT_DIR = "output_wbgt"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------
# AWS S3 Access
# ---------------------------
fs = s3fs.S3FileSystem(anon=True)

# ---------------------------
# Processing Loop
# ---------------------------
date_cursor = datetime.strptime(START_DATE, "%Y-%m-%d")
end_date = datetime.strptime(END_DATE, "%Y-%m-%d")
results = []

while date_cursor < end_date:
    date_str = date_cursor.strftime("%Y%m%d")
    year = date_cursor.year
    month = date_cursor.month

    s3_path = f"s3://nasa-nldas3/hourly_forcing/{year}/{year}-{month:02d}/nldas3_{date_str}.nc"
    print(f"Processing {s3_path} ...")

    try:
        with fs.open(s3_path) as f:
            ds = xr.open_dataset(f)

            # Spatial aggregation to ~5km (coarsen 5x5)
            ds_5km = ds.coarsen(lat=5, lon=5, boundary="trim").mean()

            # Extract variables & compute WBGT
            tair = ds_5km["Tair"].isel(time=0)
            rh = ds_5km["Qair"].isel(time=0) * 100  # Convert from kg/kg to %
            wind = (ds_5km["Wind_E"]**2 + ds_5km["Wind_N"]**2)**0.5
            solar = ds_5km["SWdown"].isel(time=0)
            pressure = ds_5km["PSurf"].isel(time=0)

            wbgt = wbgt_outdoor(tair, rh, wind, solar, pressure)
            wbgt.name = "WBGT"

            # Save to NetCDF
            out_path = os.path.join(OUTPUT_DIR, f"wbgt_{date_str}_5km.nc")
            wbgt.to_netcdf(out_path)

            # Record mean value
            results.append({"date": date_str, "wbgt_mean": float(wbgt.mean().values)})

    except Exception as e:
        print(f"Failed for {date_str}: {e}")
        results.append({"date": date_str, "wbgt_mean": None, "error": str(e)})

    date_cursor += timedelta(days=1)

# ---------------------------
# Save Summary CSV
# ---------------------------
df = pd.DataFrame(results)
df.to_csv(os.path.join(OUTPUT_DIR, "wbgt_daily_summary.csv"), index=False)
print("\nPipeline complete. Output stored in:", OUTPUT_DIR)
