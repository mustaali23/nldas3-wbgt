from pywbgt import wbgt_outdoor
import xarray as xr

ds = xr.open_dataset("nldas3_5km.nc")  # Must contain necessary variables

# Replace variable names as needed to match your dataset
tair = ds['temperature'].isel(time=0)
rh = ds['humidity'].isel(time=0)
wind = ds['wind'].isel(time=0)
solar = ds['solar_radiation'].isel(time=0)
pressure = ds['pressure'].isel(time=0)

wbgt = wbgt_outdoor(tair, rh, wind, solar, pressure)
wbgt.name = "WBGT"

# Save output
wbgt.to_netcdf("wbgt_5km.nc")
