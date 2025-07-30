import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import os

summary_path = "output_wbgt/wbgt_daily_summary.csv"
if not os.path.exists(summary_path):
    raise FileNotFoundError("Run wbgt_pipeline_master.py first to generate daily summary.")

df = pd.read_csv(summary_path, parse_dates=["date"], infer_datetime_format=True)
df = df.dropna()

# Convert date string to datetime if needed
if df["date"].dtype == object:
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")

# Monthly average WBGT
monthly = df.groupby(df["date"].dt.to_period("M")).mean()
monthly.index = monthly.index.to_timestamp()

# Save CSV
monthly.to_csv("output_wbgt/wbgt_monthly_avg.csv")

# Plot
monthly.plot(figsize=(10, 5), legend=False)
plt.title("Monthly Average WBGT")
plt.ylabel("WBGT (°C)")
plt.grid(True)
plt.tight_layout()
plt.savefig("output_wbgt/wbgt_monthly_avg.png")
plt.show()
