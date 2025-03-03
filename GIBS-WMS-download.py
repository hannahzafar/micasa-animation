#!/usr/bin/env python
from owslib.wms import WebMapService

layerName = 'BlueMarble_ShadedRelief_Bathymetry'

# Connect to GIBS WMS Service
wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')

# Configure request for MODIS_Terra_CorrectedReflectance_TrueColor
img = wms.getmap(layers=[layerName],  # Layers
                 srs='epsg:4326',  # Map projection
                 bbox=(-180,-90,180,90),  # Bounds
                 # size=(1200, 600),  # Image size
                 # time='2021-09-21',  # Time of data
                 format='image/png',  # Image format
                 transparent=True)  # Nodata transparency

# Save output PNG to a file
out = open(f'image-downloads/{layerName}.png', 'wb')
out.write(img.read())
out.close()