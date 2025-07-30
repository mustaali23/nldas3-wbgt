import xarray as xr

# Replace with an actual NLDAS-3 file
ds = xr.open_dataset("sample_nldas3.nc")

print("Variables in file:")
for var in ds.data_vars:
    print(f"- {var}: {ds[var].attrs.get('long_name', '')}, units = {ds[var].attrs.get('units', 'unknown')}")

print("\nDimensions:", ds.dims)
print("Coordinates:", list(ds.coords))
print("Time range:", ds['time'].values[:3], "...")
