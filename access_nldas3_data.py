import s3fs
import xarray as xr

# Access public NLDAS-3 data via AWS S3
fs = s3fs.S3FileSystem(anon=True)

# Sample file path – adjust if needed
nldas_path = 'nasa-nldas/data/forcing/2020/NLDAS_FORA0125_H.A20200701.0000.002.grb'

# Open and print metadata
with fs.open(nldas_path, 'rb') as f:
    ds = xr.open_dataset(f, engine='cfgrib')
    print(ds)
