# a2_galfit_expdisk_devauc

# Creating bulge and disk from devauc, expdisk_res
The script `bulge_disk_data.py` creates bulge and disk files to be used by `jedisim` program.
- Bulg is the devauc component, when there is bad or no galfit components, bulge is empty fitsfile of shape 601 * 601.
- Disk is the expdisk+res fitting. If there is bad or no galfit components, original galaxy is the disk.fits.
- NO any original galaxies have -ve pixels and all have shape 601,601.
- All f814w original galaxies have mag0 26.78212 and pixscale 0.06.
- We make the very small bulge pixels zero. `bulge[bulge<1e-14] = 0`.
- If disk has -ve pixels, we make them zero and add the same quantity to the corrosponding disk.
```python
# Make sum of bulge and disk same before and after
dd = d.copy()
ddd = d.copy()
dd[dd<0] = 0
ddd[ddd>0] = 0

disk = dd
bulge = b + ddd
```


# This particular galfit fitting
Out of 201 f814w input galaxies, 15 do not have bulge-disk components from galfit, and 30 are badly fitted.
```python
# Date: Mar 2018
band        = f814w
Total       = 201
nmissing    =  15
nbad        =  30
nmiss_bad   =  45
missing     =  [37, 38, 40, 65, 79, 80, 99, 102, 117, 129, 142, 164, 165, 177, 192]
bad         =  [11, 12, 18, 25, 27, 43, 48, 54, 61, 66, 88, 93, 94, 107, 110, 120, 126, 137, 145, 146, 149, 152, 161, 163, 167, 168, 175, 183, 195, 196]
missing_bad =  [37, 38, 40, 65, 79, 80, 99, 102, 117, 129, 142, 164, 165, 177, 192, 11, 12, 18, 25, 27, 43, 48, 54, 61, 66, 88, 93, 94, 107, 110, 120, 126, 137, 145, 146, 149, 152, 161, 163, 167, 168, 175, 183, 195, 196]
```
