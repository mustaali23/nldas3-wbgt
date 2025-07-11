import xarray as xr

# Open NLDAS-3 data (NetCDF or converted from GRIB)
ds = xr.open_dataset("sample_nldas3.nc")  # Replace with actual file

# Coarsen spatial resolution to ~5 km
ds_5km = ds.coarsen(lat=5, lon=5, boundary='trim').mean()

# Save output
ds_5km.to_netcdf("nldas3_5km.nc")
