import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset("wbgt_5km.nc")

wbgt = ds["WBGT"]
wbgt.plot(cmap="hot", figsize=(10, 6))
plt.title("Estimated WBGT from NLDAS-3 (5 km)")
plt.savefig("wbgt_map.png")
plt.show()
