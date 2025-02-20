#!/usr/bin/env python
# Script to generate matplotlib frames of micasa data

import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import xarray as xr
import pandas as pd
import cartopy
from cartopy import crs as ccrs, feature as cfeature
import datetime
import glob
import os
import sys


# Functions
def get_single_match(pattern):
    matches = glob.glob(pattern)
    if len(matches) == 1:
        return matches[0]
    elif len(matches) == 0:
        raise ValueError(f"No matches found")
    else:
        raise ValueError(f"Multiple matches found: {matches}")


def normalize_rgb(colors):
    """Normalize a list of RGB colors from 0-255 to 0-1 range."""
    return [(r/255, g/255, b/255) for r, g, b in colors]


def create_color_dict(colors, positions, alpha=None):
    """
    Creates a dictionary for red, green, and blue channels, optionally adding alpha.

    Parameters:
        colors (list of tuples): List of RGB values in 0-255 range.
        positions (list): List of positions corresponding to the colors.
        alpha (list of tuples, optional): List of alpha channel values.

    Returns:
        dict: A dictionary with red, green, blue, and optionally alpha mappings.
    """
    normalized_colors = normalize_rgb(colors)
    cdict = {'red': [], 'green': [], 'blue': []}

    # Create red, green, and blue mappings
    for pos, (r, g, b) in zip(positions, normalized_colors):
        cdict['red'].append((pos, r, r))
        cdict['green'].append((pos, g, g))
        cdict['blue'].append((pos, b, b))

    # Add alpha channel if provided (only if alpha is not None)
    if alpha is not None:
        cdict['alpha'] = alpha

    return cdict


# ## Import NEE data
filepath = 'micasa-data/daily-0.1deg-final/holding/3hrly/2024/09/MiCASA_v1_flux_x3600_y1800_3hrly_202409*.nc4'
ds = xr.open_mfdataset(filepath, combine="by_coords", chunks={})['NEE']

# ## Preprocess data for plotting
# Plot only North America, drop unused lat/lon
min_lon, max_lon = -170, -30
min_lat, max_lat = 10, 70
proj=ccrs.PlateCarree()

# Plot only two days for testing
time_start, time_stop = '2024-09-26', '2024-09-27'

ds_subset = ds.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon,max_lon),time=slice(time_start,time_stop))

# mask zeroes
ds_subset_mask = ds_subset.where(ds_subset != 0)

# Define output directory
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)
filename = 'micasa'


# Define the colormap colors/transparency
colors = [
    (109, 10, 245),
    (255, 255, 255),
    (245, 138, 0)
]
# Define the position of these colors
positions = [0, 0.5, 1]

# Define alpha
alpha = [(0.0, 1.0, 1.0), # Opaque at 0 
          (0.4, 0.8, 0.8), 
          (0.5, 0, 0), 
          (0.6,  0.8, 0.8), 
          (1.0, 1.0, 1.0)]  # Opaque at 1

# Make a custom colormap
cdict = create_color_dict(colors,positions,alpha)
custom_cmap = mcolors.LinearSegmentedColormap('custom_cmap', cdict)

# Background Map Image
# Import background image saved locally
cartopy_files = os.path.join(cartopy.config['data_dir'],'mapimgs/')
map_path = os.path.join(cartopy_files, 'world.200409.3x5400x2700.jpg')
# Read in image  using maplotlib
img = plt.imread(map_path)
# Define the image (covers the entire Earth)
img_extent = (-180, 180, -90, 90)

loop_start = time.time() # Overall timer 

for i, t in enumerate(ds_subset_mask.time):

    iter_start = time.time() # Time each frame generation 

    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=300, subplot_kw= {'projection': proj},layout='constrained')
    ax.set_extent([min_lon,max_lon,min_lat,max_lat], crs=proj)
    
    # Add the background image to plot
    ax.imshow(img, origin='upper', extent=img_extent, transform=ccrs.PlateCarree(),alpha=0.9)
    
    # Subset data for the current time step
    data_at_time = ds_subset_mask.isel(time=i)
 
    # Extract time value
    time_value = data_at_time.time.dt

    # Create plot
    im = ax.pcolormesh(data_at_time.lon, data_at_time.lat, data_at_time.variable,
                       cmap=custom_cmap, vmin=-2e-7, vmax=2e-7)

    title = time_value.strftime('%b %d %Y %H:%MZ').item()
    ax.set_title(title)

    # Colorbar
    ## Create an inset axes for the colorbar
    cax = inset_axes(ax, 
                 width="40%", height="5%",
                 loc='lower left',
                borderpad=3.5,
                )
    
    
    ## Create colorbar and modify appearance
    cbar = plt.colorbar(im, 
                        cax=cax, 
                        orientation='horizontal',
                        extend='both',
                       )
    cbar.set_label("NEE (kg m$^{-2}$ s$^{-1}$)",,c='w',weight='bold')
    cbar.ax.tick_params(which='both',color='white',labelcolor='white')
    
    # Save frame
    filedt = time_value.strftime('%Y%m%d%HZ').item()
    frame = f"{output_dir}/{filename}_{filedt}.png"
    plt.savefig(frame,dpi=300)
    plt.close(fig)  # Free memory
   
    
    iter_end = time.time()
    iter_elapsed = iter_end - iter_start
    iter_minutes = int(iter_elapsed // 60)
    iter_seconds = int(iter_elapsed % 60)
    print(f"{title} took {iter_minutes} min {iter_seconds} sec")
   
loop_end = time.time()
loop_elapsed = loop_end - loop_start
loop_minutes = int(loop_elapsed // 60)
loop_seconds = int(loop_elapsed % 60)
print(f"Frame generation complete. Total time in loop: {loop_minutes} min {loop_seconds} sec")

