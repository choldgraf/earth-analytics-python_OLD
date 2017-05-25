---
layout: single
title: "Extract raster values using vector boundaries in Python"
excerpt: "This lesson reviews how to extract data from a raster dataset using a
vector dataset. "
authors: ['Chris Holdgraf', 'Carson Farmer', 'Leah Wasser']
modified: 2017-05-25
category: [course-materials]
class-lesson: ['class-intro-spatial-python']
permalink: /course-materials/earth-analytics-python/week-5/extract-data-from-raster/
nav-title: 'Extract data from raster'
course: "Earth Analytics Python"
week: 5
sidebar:
  nav:
author_profile: false
comments: true
order: 6
---

{% include toc title="In This Lesson" icon="file-text" %}

<div class='notice--success' markdown="1">

## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives

After completing this tutorial, you will be able to:

* Use the `extract()` function to extract raster values using a vector extent or set of extents.
* Create a scatter plot with a one to one line in `R`.
* Understand the concept of uncertainty as it's associated with remote sensing data.

## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need

You will need a computer with internet access to complete this lesson and the data for week 5 of the course.

[<i class="fa fa-download" aria-hidden="true"></i> Download Week 5 Data (~500 MB)](https://ndownloader.figshare.com/files/7525363){:data-proofer-ignore='' .btn }


</div>

First let's import the needed libraries and make sure our working directory is set


```python
# import all libraries
import os
import numpy as np
import rasterio as rio
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterstats as rs
import pandas as pd
#from rasterio import plot as riop
plt.ion()

# be sure to set your working directory
os.chdir("/Users/lewa8222/Documents/earth-analytics")
```

## Import Canopy Height Model

First, we will import a canopy height model created by the NEON project. In the
previous lessons / weeks we learned how to make a canopy height model by
subtracting the Digital elevation model (DEM) from the Digital surface model (DSM).

* first open and view histogram
then fix data...

## is there an easy way to view summary stats?
## any reason to not use context manager throughout? (code is commented)



```python
# So do i need to use a context manager each time - here we don't use it.
# carson suggests we probably should
#SJER_chm = rio.open('data/week5/california/SJER/2013/lidar/SJER_lidarCHM.tif')

with rio.open('data/week5/california/SJER/2013/lidar/SJER_lidarCHM.tif') as lidar_chm_src:
    # read the data into a numpy array
    # note that the (1) ensures you get a 2 dimensional object rather than 3
    SJER_chm_data = lidar_chm_src.read(1, masked=True) 

# read in data -- not sure if masked = True works
# can we create summary stats on the array?

#SJER_chm_data = SJER_chm.read(masked=True)

# plot histogram
# Need to add x and y labels to plot and title 
fig, ax = plt.subplots()
ax.hist(SJER_chm_data.compressed())
plt.title('Distribution of lidar canopy height values ')


```




    <matplotlib.text.Text at 0x141e5dc88>




![png](../../../../../images/course-materials/earth-analytics-python//week-5/in-class/2016-12-06-spatial06-extract-raster-values_4_1.png)



```python
print('Mean:', SJER_chm_data.mean())
print('Max:', SJER_chm_data.max())
print('Min:', SJER_chm_data.min())
```

    Mean: 1.9355862432
    Max: 45.88
    Min: 0.0


## Data values
Looking at the distribution of data, it appears as if there is a skew around 0. IN this case, there are a lot of pixels with a value of 0 - where there are no trees. We may want to set these values to NA as the will impact our plot summary statistics.

## Clean CHM data

Notice that when we import the raster below, we use a context manager `with`. This creates a 
connection to our geotiff dataset. When the with segment of code ends, the connection to 
the dataset is then closed for us. 

The code below performs the following tasks:

1. we create a connection to the `SJER_lidarCHM.tif` geotiff file. 
2. We then read in the actual data as a numpy array. This allows us to manipulate the data. Notice that the code below uses `read(1)` - this tells python to only import the FIRST BAND of our raster. In this case we only have one band but we need to specify that we are only importing that one band. 

`SJER_chm_data = lidar_chm_src.read(1)`

3. Finally we set all pixels that have the value of 0 to `nan` (no data values)
`SJER_chm_data[SJER_chm_data==0] = np.nan`
4. Finally we grab the spatial attributes of our original raster and save them to a variable called `profile`.

`profile = lidar_chm_src.profile`


```python
# load lidar canopy height model raster  using rasterio
# note that we are using a context manager - with to do this 
with rio.open('data/week5/california/SJER/2013/lidar/SJER_lidarCHM.tif') as lidar_chm_src:
    # read the data into a numpy array
    # note that the (1) ensures you get a 2 dimensional object rather than 3
    SJER_chm_data = lidar_chm_src.read(1) 
    # set CHM values of 0 to NAN
    SJER_chm_data[SJER_chm_data==0] = np.nan
    profile = lidar_chm_src.profile

# https://mapbox.github.io/rasterio/quickstart.html

```

## Spatial attributes stored in a dictionary

Before we go any further, let's have a look at the `profile` object. This object is a dictionary that contains all of the spatial attributes of our original geotiff. 

When we read the data into a numpy array, it becomes a generic object with no spatial attributes. A numpy array only contains the pixel values for each cell stored in an `array` or matrix format. 


```python
type(profile)
```




    dict



If we look at the profile object we will see all of the attributes. We are going to use that object to 
set all of the spatial attributes when we write out our modified numpy array to a new geotiff.



```python
profile
```




    {'affine': Affine(1.0, 0.0, 254571.0,
           0.0, -1.0, 4112362.0),
     'compress': 'lzw',
     'count': 1,
     'crs': CRS({'init': 'epsg:32611'}),
     'driver': 'GTiff',
     'dtype': 'float32',
     'height': 5059,
     'interleave': 'band',
     'nodata': -9999.0,
     'tiled': False,
     'transform': (254571.0, 1.0, 0.0, 4112362.0, 0.0, -1.0),
     'width': 4296}







There are a lot of values in our CHM that == 0. Let's set those to `NA` and plot

again.





```python
# load lidar canopy height model raster  using rasterio
# note that we are using a context manager - with to do this 
with rio.open('data/week5/california/SJER/2013/lidar/SJER_lidarCHM.tif') as lidar_chm_src:
    # read the data into a numpy array
    # note that the (1) ensures you get a 2 dimensional object rather than 3
    SJER_chm_data = lidar_chm_src.read(1) 
    # set CHM values of 0 to NAN
    # currently this seems to be assigning all values to nan
    # instead i set it tot he no data value which is -9999.0
    SJER_chm_data[SJER_chm_data == 0] = -9999
    profile = lidar_chm_src.profile

```


```python
# what is .ravel -- a flattened array? i don't think we want that 
#SJER_chm_data_ravel = SJER_chm_data.ravel()
#SJER_chm_data_ravel = SJER_chm_data_ravel[SJER_chm_data_ravel > 0]

# create histogram 
#fig, ax = plt.subplots()
#ax.hist(SJER_chm_data_ravel)

print('MEAN:',SJER_chm_data.mean())
print('MIN:',SJER_chm_data.min())
print('MAX:',SJER_chm_data.max())
# create histogram 
#fig, ax = plt.subplots()
#ax.hist(SJER_chm_data)
```

    MEAN: -7640.71
    MIN: -9999.0
    MAX: 45.88



```python
# ok so this is a masked array -- need to better understand ravel
# then need to understand how you'd export this to a geotiff if need be. 
type(SJER_chm_data)
```




    numpy.ndarray



Finally, export the cleaned data to a geotiff. Notice that we have a nodatavalue specified in our profile object.


```python
# assign cleaned lidar path
lidar_path = 'sjer_chm_zero_removed.tif'
# write a new geotiff using the spatial attributes of the original data 
with rio.open(lidar_path, 'w', **profile) as dst:
     # astype ensures the output format is correct 
    dst.write(SJER_chm_data.astype(rio.float32), 1) 

```

    /Users/lewa8222/anaconda/lib/python3.6/site-packages/rasterio/__init__.py:160: FutureWarning: GDAL-style transforms are deprecated and will not be supported in Rasterio 1.0.
      transform = guard_transform(transform)


Finally let's have a look at a historgram of the cleaned, exported CHM data. Note that when we import the 
data, we set masked=True to make sure that python maskes out our NA or no data values. 


```python
# open the masked CHM geotiff
with rio.open(lidar_path) as lidar_chm2_src:
    SJER_chm2_data = lidar_chm2_src.read(1, masked=True)
   
# view mean, min max
print('MEAN:',SJER_chm2_data.mean())
print('MIN:',SJER_chm2_data.min())
print('MAX:',SJER_chm2_data.max())

```

    MEAN: 8.21350469357
    MIN: 2.0
    MAX: 45.88


##  View distribution of pixel values

Finally we can plot a historgram which represents the distribution of pixels values in our raster.
By using the `.compressed()` attribute, we force python to ignore no data values (-9999 values in this case). 

# can we add outlines to each bar?


```python
# create histogram 
fig, ax = plt.subplots()
# .compressed() forces numpy to not plot the NA values
ax.hist(SJER_chm2_data.compressed())
plt.title('Distribution of lidar canopy height values ')

```




    <matplotlib.text.Text at 0x142515e10>




![png](../../../../../images/course-materials/earth-analytics-python//week-5/in-class/2016-12-06-spatial06-extract-raster-values_21_1.png)


## Part 2. Does our CHM data compare to field measured tree heights?

We now have a canopy height model for our study area in California. However, how
do the height values extracted from the CHM compare to our laboriously collected,
field measured canopy height data? To figure this out, we will use *in situ* collected
tree height data, measured within circular plots across our study area. We will compare
the maximum measured tree height value to the maximum LiDAR derived height value
for each circular plot using regression.

For this activity, we will use the a `csv` (comma separate value) file,
located in `SJER/2013/insitu/veg_structure/D17_2013_SJER_vegStr.csv`.

First we import the shapefile that contains the plot centroid locations using geopandas.


```python
SJER_plots = gpd.read_file('data/week5/california/SJER/vector_data/SJER_plot_centroids.shp')
type(SJER_plots)
```




    geopandas.geodataframe.GeoDataFrame




```python
# view spatial extent of shapefile 
SJER_plots.total_bounds
```




    (254738.61799999999, 4107527.074, 258497.10200000001, 4112167.7779999999)



## Data structure
We can use `SJER_plots.geom_type.head()` to determine the vector type of the shapefile that we imported. Below, we see that the data are stored as points. These points represent the centroid (or hte center) of the plot where trees were measured. We want to extract tree height values derived from the lidar data for the entire plot. To do this, we will need to create a BUFFER around the points.


```python
SJER_plots.geom_type.head()
```




    0    Point
    1    Point
    2    Point
    3    Point
    4    Point
    dtype: object



In this case our plot size is 40m. If we create a circular buffer wiht a 20m diameter it will closely approximate where trees were measured on the ground. 

We can use the .buffer() function to create the buffer. Here the buffer size is specified in the () of the function. We will send the new object to a new shapefile using .to_file() as follows:

`SJER_plots.buffer(20).to_file('path-to-shapefile-here.shp')`



```python
# sneaky assign the buffer geometry to the points layer to maintain attributes
SJER_plots["geometry"] = SJER_plots.geometry.buffer(20)
SJER_plots["geometry"]

# export the layer as a shapefile to use in zonal stats
plot_buffer_path = 'plot_buffer.shp'
SJER_plots.to_file(plot_buffer_path)
```


```python
# Why do you need to specify the extent here? 
# why is the point all black - ie the color isn't takig and it seems to be dominated by the fill?
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(SJER_chm.read(masked=True)[0], 
          extent=[bounds.left, bounds.right, bounds.bottom, bounds.top], 
          cmap='Greys')
SJER_plots.plot(ax=ax, # overlay points on the ax plot
                marker='o', 
                markersize=5, # set point symbol size
                color='purple') # set point color
ax.set_title("San Joachin - Tree Plot Locations", 
             fontsize=25)
```




    <matplotlib.text.Text at 0x142f4ab38>




![png](../../../../../images/course-materials/earth-analytics-python//week-5/in-class/2016-12-06-spatial06-extract-raster-values_30_1.png)



```python

```

## Extract pixel values for each plot 

Once we have the boundary for each plot location (a 20m diameter circle) we can extract all of the pixels that fall within each circle using the function `zonal_stats` in the `rasterstats` library. 



### Extract CMH data within 20 m radius of each plot centroid.

Next, we will create a boundary region (called a buffer) representing the spatial
extent of each plot (where trees were measured). We will then extract all CHM pixels
that fall within the plot boundary to use to estimate tree height for that plot.

There are a few ways to go about this task. If our plots are circular, then we can
use the `extract()` function.

<figure>
    <img src="{{ site.url }}/images/course-materials/earth-analytics/week-5/buffer-circular.png" alt="buffer circular">
    <figcaption>The extract function in R allows you to specify a circular buffer
    radius around an x,y point location. Values for all pixels in the specified
    raster that fall within the circular buffer are extracted. In this case, we
    will tell R to extract the maximum value of all pixels using the fun=max
    command. Source: Colin Williams, NEON
    </figcaption>
</figure>

### Extract Plot Data Using Circle: 20m Radius Plots


```python
# import new geotiff with 0's removed
# Extract zonal stats
sjer_tree_heights = rs.zonal_stats(plot_buffer_path, 
            lidar_path, 
            geojson_out=True,
            copy_properties=True,
            stats="count min mean max median")
# view first item in dictionary
sjer_tree_heights[1]

```

    /Users/lewa8222/anaconda/lib/python3.6/site-packages/rasterstats/main.py:142: FutureWarning: The value of this property will change in version 1.0. Please see https://github.com/mapbox/rasterio/issues/86 for details.
      with Raster(raster, affine, nodata, band) as rast:
    /Users/lewa8222/anaconda/lib/python3.6/site-packages/rasterstats/io.py:242: FutureWarning: GDAL-style transforms are deprecated and will not be supported in Rasterio 1.0.
      self.affine = guard_transform(self.src.transform)





    {'geometry': {'coordinates': [[(257426.967, 4111298.971),
        (257426.87069453346, 4111297.010657193),
        (257426.58270560807, 4111295.0691935597),
        (257426.10580671465, 4111293.165306455),
        (257425.44459065024, 4111291.3173313527),
        (257424.60542528698, 4111289.5430652634),
        (257423.59639224605, 4111287.8595953393),
        (257422.42720906725, 4111286.2831343166),
        (257421.10913562373, 4111284.828864376),
        (257419.6548656833, 4111283.5107909325),
        (257418.0784046604, 4111282.3416077537),
        (257416.3949347365, 4111281.332574713),
        (257414.62066864732, 4111280.4934093496),
        (257412.7726935451, 4111279.832193285),
        (257410.86880644032, 4111279.355294392),
        (257408.9273428066, 4111279.0673054666),
        (257406.967, 4111278.971),
        (257405.00665719341, 4111279.0673054666),
        (257403.06519355968, 4111279.355294392),
        (257401.16130645492, 4111279.832193285),
        (257399.3133313527, 4111280.4934093496),
        (257397.5390652635, 4111281.332574713),
        (257395.8555953396, 4111282.3416077537),
        (257394.27913431672, 4111283.5107909325),
        (257392.82486437628, 4111284.828864376),
        (257391.50679093276, 4111286.2831343166),
        (257390.33760775396, 4111287.8595953393),
        (257389.32857471303, 4111289.5430652634),
        (257388.48940934977, 4111291.3173313527),
        (257387.82819328536, 4111293.165306455),
        (257387.35129439193, 4111295.0691935597),
        (257387.06330546655, 4111297.010657193),
        (257386.967, 4111298.971),
        (257387.06330546655, 4111300.9313428067),
        (257387.35129439193, 4111302.87280644),
        (257387.82819328536, 4111304.776693545),
        (257388.48940934977, 4111306.624668647),
        (257389.32857471303, 4111308.3989347364),
        (257390.33760775396, 4111310.0824046605),
        (257391.50679093276, 4111311.6588656832),
        (257392.82486437628, 4111313.1131356237),
        (257394.27913431672, 4111314.4312090673),
        (257395.8555953396, 4111315.600392246),
        (257397.5390652635, 4111316.6094252868),
        (257399.3133313527, 4111317.44859065),
        (257401.16130645492, 4111318.1098067146),
        (257403.06519355968, 4111318.586705608),
        (257405.00665719341, 4111318.874694533),
        (257406.967, 4111318.971),
        (257408.9273428066, 4111318.874694533),
        (257410.86880644032, 4111318.586705608),
        (257412.7726935451, 4111318.1098067146),
        (257414.62066864732, 4111317.44859065),
        (257416.3949347365, 4111316.6094252868),
        (257418.0784046604, 4111315.600392246),
        (257419.6548656833, 4111314.4312090673),
        (257421.10913562373, 4111313.1131356237),
        (257422.42720906725, 4111311.6588656832),
        (257423.59639224605, 4111310.0824046605),
        (257424.60542528698, 4111308.3989347364),
        (257425.44459065024, 4111306.624668647),
        (257426.10580671465, 4111304.776693545),
        (257426.58270560807, 4111302.87280644),
        (257426.87069453346, 4111300.9313428067),
        (257426.967, 4111298.971)]],
      'type': 'Polygon'},
     'id': '1',
     'properties': OrderedDict([('Plot_ID', 'SJER112'),
                  ('Point', 'center'),
                  ('easting', 257406.967),
                  ('northing', 4111298.971),
                  ('plot_type', 'trees'),
                  ('min', 2.0999999046325684),
                  ('max', 24.01999855041504),
                  ('mean', 10.3692772996614),
                  ('count', 443),
                  ('median', 7.869999885559082)]),
     'type': 'Feature'}




```python
# turn extracted data into a pandas geo data frame 
SJER_lidar_height_df = gpd.GeoDataFrame.from_features(sjer_tree_heights)
SJER_lidar_height_df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Plot_ID</th>
      <th>Point</th>
      <th>count</th>
      <th>easting</th>
      <th>geometry</th>
      <th>max</th>
      <th>mean</th>
      <th>median</th>
      <th>min</th>
      <th>northing</th>
      <th>plot_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SJER1068</td>
      <td>center</td>
      <td>161</td>
      <td>255852.376</td>
      <td>POLYGON ((255872.376 4111567.818, 255872.27969...</td>
      <td>19.049999</td>
      <td>11.544347</td>
      <td>12.62</td>
      <td>2.04</td>
      <td>4111567.818</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SJER112</td>
      <td>center</td>
      <td>443</td>
      <td>257406.967</td>
      <td>POLYGON ((257426.967 4111298.971, 257426.87069...</td>
      <td>24.019999</td>
      <td>10.369277</td>
      <td>7.87</td>
      <td>2.10</td>
      <td>4111298.971</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SJER116</td>
      <td>center</td>
      <td>643</td>
      <td>256838.760</td>
      <td>POLYGON ((256858.76 4110819.876, 256858.663694...</td>
      <td>16.070000</td>
      <td>7.518398</td>
      <td>6.80</td>
      <td>2.82</td>
      <td>4110819.876</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SJER117</td>
      <td>center</td>
      <td>245</td>
      <td>256176.947</td>
      <td>POLYGON ((256196.947 4108752.026, 256196.85069...</td>
      <td>11.059999</td>
      <td>7.675346</td>
      <td>7.93</td>
      <td>3.24</td>
      <td>4108752.026</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SJER120</td>
      <td>center</td>
      <td>17</td>
      <td>255968.372</td>
      <td>POLYGON ((255988.372 4110476.079, 255988.27569...</td>
      <td>5.740000</td>
      <td>4.591177</td>
      <td>4.45</td>
      <td>3.38</td>
      <td>4110476.079</td>
      <td>grass</td>
    </tr>
  </tbody>
</table>
</div>



#### Explore The Data Distribution

If you want to explore the data distribution of pixel height values in each plot,
you could remove the `fun` call to max and generate a list.
`cent_ovrList <- extract(chm,centroid_sp,buffer = 20)`. It's good to look at the
distribution of values we've extracted for each plot. Then you could generate a
histogram for each plot `hist(cent_ovrList[[2]])`. If we wanted, we could loop
through several plots and create histograms using a `for loop`.



```python

# this should show how to create a histogram of tree heights for each plot 
# we can skip this if it's not possible with  zonal stats...


```

## Extract descriptive stats from *In situ* Data
In our final step, we will extract summary height values from our field data.
We will use the `dplyr` library to do this efficiently.

First let's see how many plots are in our tree height data. Note that our tree
height data is stored in csv format.


```python
# import in situ data
path_insitu = 'data/week5/california/SJER/2013/insitu/veg_structure/D17_2013_SJER_vegStr.csv'
SJER_insitu = pd.read_csv(path_insitu)
# what is the structure of the data
type(SJER_insitu)
# view the first 5 rows of data
SJER_insitu.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>siteid</th>
      <th>sitename</th>
      <th>plotid</th>
      <th>easting</th>
      <th>northing</th>
      <th>taxonid</th>
      <th>scientificname</th>
      <th>indvidual_id</th>
      <th>pointid</th>
      <th>individualdistance</th>
      <th>...</th>
      <th>canopyform</th>
      <th>livingcanopy</th>
      <th>inplotcanopy</th>
      <th>materialsampleid</th>
      <th>dbhqf</th>
      <th>stemmapqf</th>
      <th>plant_group</th>
      <th>common_name</th>
      <th>aop_plot</th>
      <th>unique_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SJER</td>
      <td>San Joaquin</td>
      <td>SJER128</td>
      <td>257085.7</td>
      <td>4111381.5</td>
      <td>PISA2</td>
      <td>Pinus sabiniana</td>
      <td>1485</td>
      <td>center</td>
      <td>9.7</td>
      <td>...</td>
      <td>NaN</td>
      <td>100</td>
      <td>100</td>
      <td>NaN</td>
      <td>0</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SJER</td>
      <td>San Joaquin</td>
      <td>SJER2796</td>
      <td>256047.7</td>
      <td>4111548.5</td>
      <td>ARVI4</td>
      <td>Arctostaphylos viscida</td>
      <td>1622</td>
      <td>NE</td>
      <td>5.8</td>
      <td>...</td>
      <td>Hemisphere</td>
      <td>70</td>
      <td>100</td>
      <td>f095</td>
      <td>0</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SJER</td>
      <td>San Joaquin</td>
      <td>SJER272</td>
      <td>256722.9</td>
      <td>4112170.2</td>
      <td>ARVI4</td>
      <td>Arctostaphylos viscida</td>
      <td>1427</td>
      <td>center</td>
      <td>6.0</td>
      <td>...</td>
      <td>Hemisphere</td>
      <td>35</td>
      <td>100</td>
      <td>NaN</td>
      <td>0</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SJER</td>
      <td>San Joaquin</td>
      <td>SJER112</td>
      <td>257421.4</td>
      <td>4111308.2</td>
      <td>ARVI4</td>
      <td>Arctostaphylos viscida</td>
      <td>1511</td>
      <td>center</td>
      <td>17.2</td>
      <td>...</td>
      <td>Sphere</td>
      <td>70</td>
      <td>100</td>
      <td>f035</td>
      <td>0</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SJER</td>
      <td>San Joaquin</td>
      <td>SJER272</td>
      <td>256720.5</td>
      <td>4112177.2</td>
      <td>ARVI4</td>
      <td>Arctostaphylos viscida</td>
      <td>1431</td>
      <td>center</td>
      <td>9.9</td>
      <td>...</td>
      <td>Sphere</td>
      <td>80</td>
      <td>100</td>
      <td>f087</td>
      <td>0</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 30 columns</p>
</div>



We want to calculate a summary value of max tree height (the tallest tree measured) in each plot. 
We have a unique id for each plot - **plotid** that we can use to group the data. The tree height values themselves are located in the **stemheight** column.

We can calculate this by using the .groupy() method in pandas. Note that the statement below 

## what is reset_index??

## Extract Max Tree Height

Next, we can use dplyr to extract a summary tree height value for each plot. In
this case, we will calculate the mean MEASURED tree height value for each
plot. This value represents the average tree in each plot. We will also calculate
the max height representing the max height for each plot.

FInally, we will compare the mean measured tree height per plot to the mean
tree height extracted from the lidar CHM.


```python
## extract max tree height for each plot
insitu_stem_height = SJER_insitu.groupby('plotid').max()['stemheight'].reset_index()
# view the top 
insitu_stem_height
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>plotid</th>
      <th>stemheight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SJER1068</td>
      <td>19.3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SJER112</td>
      <td>23.9</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SJER116</td>
      <td>16.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SJER117</td>
      <td>11.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SJER120</td>
      <td>8.8</td>
    </tr>
    <tr>
      <th>5</th>
      <td>SJER128</td>
      <td>18.2</td>
    </tr>
    <tr>
      <th>6</th>
      <td>SJER192</td>
      <td>13.7</td>
    </tr>
    <tr>
      <th>7</th>
      <td>SJER272</td>
      <td>12.4</td>
    </tr>
    <tr>
      <th>8</th>
      <td>SJER2796</td>
      <td>9.4</td>
    </tr>
    <tr>
      <th>9</th>
      <td>SJER3239</td>
      <td>17.9</td>
    </tr>
    <tr>
      <th>10</th>
      <td>SJER36</td>
      <td>9.2</td>
    </tr>
    <tr>
      <th>11</th>
      <td>SJER361</td>
      <td>11.8</td>
    </tr>
    <tr>
      <th>12</th>
      <td>SJER37</td>
      <td>11.5</td>
    </tr>
    <tr>
      <th>13</th>
      <td>SJER4</td>
      <td>10.8</td>
    </tr>
    <tr>
      <th>14</th>
      <td>SJER8</td>
      <td>5.2</td>
    </tr>
    <tr>
      <th>15</th>
      <td>SJER824</td>
      <td>26.5</td>
    </tr>
    <tr>
      <th>16</th>
      <td>SJER916</td>
      <td>18.4</td>
    </tr>
    <tr>
      <th>17</th>
      <td>SJER952</td>
      <td>7.7</td>
    </tr>
  </tbody>
</table>
</div>




```python

```

### Merge InSitu Data With Spatial data.frame

Once we have our summarized insitu data, we can `merge` it into the centroids
`data.frame`. Merge requires two data.frames and the names of the columns
containing the unique ID that we will merge the data on. In this case, we will
merge the data on the plot_id column. Notice that it's spelled slightly differently
in both data.frames so we'll need to tell R what it's called in each data.frame.



```python
# join data
# note the code below doesn't work because the attributes didn't transfer when i created the buffer object
SJER_final_height = pd.merge(insitu_stem_height, 
                       SJER_lidar_height_df, 
                       left_on='plotid', 
                       right_on='Plot_ID')
SJER_final_height
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>plotid</th>
      <th>stemheight</th>
      <th>Plot_ID</th>
      <th>Point</th>
      <th>count</th>
      <th>easting</th>
      <th>geometry</th>
      <th>max</th>
      <th>mean</th>
      <th>median</th>
      <th>min</th>
      <th>northing</th>
      <th>plot_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SJER1068</td>
      <td>19.3</td>
      <td>SJER1068</td>
      <td>center</td>
      <td>161</td>
      <td>255852.376</td>
      <td>POLYGON ((255872.376 4111567.818, 255872.27969...</td>
      <td>19.049999</td>
      <td>11.544347</td>
      <td>12.620000</td>
      <td>2.04</td>
      <td>4111567.818</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SJER112</td>
      <td>23.9</td>
      <td>SJER112</td>
      <td>center</td>
      <td>443</td>
      <td>257406.967</td>
      <td>POLYGON ((257426.967 4111298.971, 257426.87069...</td>
      <td>24.019999</td>
      <td>10.369277</td>
      <td>7.870000</td>
      <td>2.10</td>
      <td>4111298.971</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SJER116</td>
      <td>16.0</td>
      <td>SJER116</td>
      <td>center</td>
      <td>643</td>
      <td>256838.760</td>
      <td>POLYGON ((256858.76 4110819.876, 256858.663694...</td>
      <td>16.070000</td>
      <td>7.518398</td>
      <td>6.800000</td>
      <td>2.82</td>
      <td>4110819.876</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SJER117</td>
      <td>11.0</td>
      <td>SJER117</td>
      <td>center</td>
      <td>245</td>
      <td>256176.947</td>
      <td>POLYGON ((256196.947 4108752.026, 256196.85069...</td>
      <td>11.059999</td>
      <td>7.675346</td>
      <td>7.930000</td>
      <td>3.24</td>
      <td>4108752.026</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SJER120</td>
      <td>8.8</td>
      <td>SJER120</td>
      <td>center</td>
      <td>17</td>
      <td>255968.372</td>
      <td>POLYGON ((255988.372 4110476.079, 255988.27569...</td>
      <td>5.740000</td>
      <td>4.591177</td>
      <td>4.450000</td>
      <td>3.38</td>
      <td>4110476.079</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>5</th>
      <td>SJER128</td>
      <td>18.2</td>
      <td>SJER128</td>
      <td>center</td>
      <td>381</td>
      <td>257078.867</td>
      <td>POLYGON ((257098.867 4111388.57, 257098.770694...</td>
      <td>19.139999</td>
      <td>8.987087</td>
      <td>8.020000</td>
      <td>2.16</td>
      <td>4111388.570</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>6</th>
      <td>SJER192</td>
      <td>13.7</td>
      <td>SJER192</td>
      <td>center</td>
      <td>929</td>
      <td>256683.434</td>
      <td>POLYGON ((256703.434 4111071.087, 256703.33769...</td>
      <td>16.549999</td>
      <td>7.229096</td>
      <td>6.630000</td>
      <td>2.20</td>
      <td>4111071.087</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>7</th>
      <td>SJER272</td>
      <td>12.4</td>
      <td>SJER272</td>
      <td>center</td>
      <td>711</td>
      <td>256717.467</td>
      <td>POLYGON ((256737.467 4112167.778, 256737.37069...</td>
      <td>11.840000</td>
      <td>7.107061</td>
      <td>6.980000</td>
      <td>2.37</td>
      <td>4112167.778</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>8</th>
      <td>SJER2796</td>
      <td>9.4</td>
      <td>SJER2796</td>
      <td>center</td>
      <td>270</td>
      <td>256034.390</td>
      <td>POLYGON ((256054.39 4111533.879, 256054.293694...</td>
      <td>20.279999</td>
      <td>6.409630</td>
      <td>6.230000</td>
      <td>2.03</td>
      <td>4111533.879</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>9</th>
      <td>SJER3239</td>
      <td>17.9</td>
      <td>SJER3239</td>
      <td>center</td>
      <td>195</td>
      <td>258497.102</td>
      <td>POLYGON ((258517.102 4109856.983, 258517.00569...</td>
      <td>12.910000</td>
      <td>6.009128</td>
      <td>5.950000</td>
      <td>2.02</td>
      <td>4109856.983</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>10</th>
      <td>SJER36</td>
      <td>9.2</td>
      <td>SJER36</td>
      <td>center</td>
      <td>97</td>
      <td>258277.829</td>
      <td>POLYGON ((258297.829 4110161.674, 258297.73269...</td>
      <td>8.990000</td>
      <td>6.516288</td>
      <td>6.680000</td>
      <td>2.03</td>
      <td>4110161.674</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>11</th>
      <td>SJER361</td>
      <td>11.8</td>
      <td>SJER361</td>
      <td>center</td>
      <td>72</td>
      <td>256961.794</td>
      <td>POLYGON ((256981.794 4107527.074, 256981.69769...</td>
      <td>18.730000</td>
      <td>13.899028</td>
      <td>13.684999</td>
      <td>2.12</td>
      <td>4107527.074</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>12</th>
      <td>SJER37</td>
      <td>11.5</td>
      <td>SJER37</td>
      <td>center</td>
      <td>201</td>
      <td>256148.197</td>
      <td>POLYGON ((256168.197 4107578.841, 256168.10069...</td>
      <td>11.490000</td>
      <td>7.109850</td>
      <td>7.100000</td>
      <td>2.19</td>
      <td>4107578.841</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>13</th>
      <td>SJER4</td>
      <td>10.8</td>
      <td>SJER4</td>
      <td>center</td>
      <td>395</td>
      <td>257228.336</td>
      <td>POLYGON ((257248.336 4109767.289, 257248.23969...</td>
      <td>9.530000</td>
      <td>5.034937</td>
      <td>5.220000</td>
      <td>2.15</td>
      <td>4109767.289</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>14</th>
      <td>SJER8</td>
      <td>5.2</td>
      <td>SJER8</td>
      <td>center</td>
      <td>7</td>
      <td>254738.618</td>
      <td>POLYGON ((254758.618 4110249.265, 254758.52169...</td>
      <td>4.150000</td>
      <td>3.024286</td>
      <td>3.000000</td>
      <td>2.27</td>
      <td>4110249.265</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>15</th>
      <td>SJER824</td>
      <td>26.5</td>
      <td>SJER824</td>
      <td>center</td>
      <td>382</td>
      <td>256185.584</td>
      <td>POLYGON ((256205.584 4110047.586, 256205.48769...</td>
      <td>25.660000</td>
      <td>7.720838</td>
      <td>6.265000</td>
      <td>2.09</td>
      <td>4110047.586</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>16</th>
      <td>SJER916</td>
      <td>18.4</td>
      <td>SJER916</td>
      <td>center</td>
      <td>264</td>
      <td>257460.486</td>
      <td>POLYGON ((257480.486 4109616.679, 257480.38969...</td>
      <td>18.730000</td>
      <td>11.170795</td>
      <td>10.980000</td>
      <td>2.15</td>
      <td>4109616.679</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>17</th>
      <td>SJER952</td>
      <td>7.7</td>
      <td>SJER952</td>
      <td>center</td>
      <td>42</td>
      <td>255871.194</td>
      <td>POLYGON ((255891.194 4110759.039, 255891.09769...</td>
      <td>6.380000</td>
      <td>4.149285</td>
      <td>4.080000</td>
      <td>2.84</td>
      <td>4110759.039</td>
      <td>grass</td>
    </tr>
  </tbody>
</table>
</div>





## Plot by height





```python
# this is a spatial plot where the points are sized according to tree height
# points overlaid on top of the chm ...

# this is just a plot of field plot locations overlayed on top of the chm
img = SJER_chm.read().squeeze()
img[img == 0] = np.nan

fig, ax = plt.subplots(figsize=(10, 10))
# riop.show(SJER_chm, cmap='Greys', ax=ax)
ax.imshow(img, cmap='Greys', extent=[SJER_chm.bounds[ii] for ii in [0, 2, 1, 3]])
# why are the markers so tiny tiny?!
SJER_plots.plot(ax=ax, markersize=500, color='r')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x143e68a20>




![png](../../../../../images/course-materials/earth-analytics-python//week-5/in-class/2016-12-06-spatial06-extract-raster-values_47_1.png)






### Plot Data (CHM vs Measured)

Let's create a plot that illustrates the relationship between in situ measured

max canopy height values and lidar derived max canopy height values.







```python
# this plot should be a scatter plot with labels and such
# how to add x and y labels
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.plot.html
# Prettier plots: https://datasciencelab.wordpress.com/2013/12/21/beautiful-plots-with-pandas-and-matplotlib/
fig, ax = plt.subplots(figsize=(10, 10))

csfont = {'fontname':'Myriad Pro'}
SJER_final_height.plot('max', 'stemheight', 
                       kind='scatter',
                       title="Lidar vs measured tree height - SJER", 
                       fontsize=14, ax=ax)

ax.set(xlabel="Lidar derived max tree height", 
       ylabel="Measured tree height (m)")
# Customize title, set position, allow space on top of plot for title
# this doesn't work - i'm not sure why
ax.set_title(ax.get_title(), 
             fontsize=30, 
             **csfont)
# ax.set_xlabel(xlabel, fontsize=20, ha='left')


```




    <matplotlib.text.Text at 0x14952b550>




![png](../../../../../images/course-materials/earth-analytics-python//week-5/in-class/2016-12-06-spatial06-extract-raster-values_49_1.png)




Next, let's fix the plot adding a 1:1 line and making the x and y axis the same .

## need to add a 1:1 line to the plot below



```python
# this plot should be a scatter plot with labels and such
# how to add x and y labels
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.plot.html
# Prettier plots: https://datasciencelab.wordpress.com/2013/12/21/beautiful-plots-with-pandas-and-matplotlib/
fig, ax = plt.subplots(figsize=(10, 10))

csfont = {'fontname':'Myriad Pro'}
SJER_final_height.plot('max', 'stemheight', 
                       kind='scatter',
                       title="Lidar vs measured tree height - SJER", 
                       fontsize=14, ax=ax)

ax.set(xlabel="Lidar derived max tree height", 
       ylabel="Measured tree height (m)")
# Customize title, set position, allow space on top of plot for title
# this doesn't work - i'm not sure why
ax.set_title(ax.get_title(), 
             fontsize=30, 
             **csfont)
# ax.set_xlabel(xlabel, fontsize=20, ha='left')

```




    <matplotlib.text.Text at 0x14a063eb8>




![png](../../../../../images/course-materials/earth-analytics-python//week-5/in-class/2016-12-06-spatial06-extract-raster-values_51_1.png)


We can also add a regression fit to our plot. Explore the GGPLOT options and
customize your plot.

# need to add a regression fit to the plot below





```python
# this plot should be a scatter plot with labels and such
# how to add x and y labels
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.plot.html
# Prettier plots: https://datasciencelab.wordpress.com/2013/12/21/beautiful-plots-with-pandas-and-matplotlib/
fig, ax = plt.subplots(figsize=(10, 10))

csfont = {'fontname':'Myriad Pro'}
SJER_final_height.plot('max', 'stemheight', 
                       kind='scatter',
                       title="Lidar vs measured tree height - SJER", 
                       fontsize=14, ax=ax)

ax.set(xlabel="Lidar derived max tree height", 
       ylabel="Measured tree height (m)")
# Customize title, set position, allow space on top of plot for title
# this doesn't work - i'm not sure why
ax.set_title(ax.get_title(), 
             fontsize=30, 
             **csfont)
# ax.set_xlabel(xlabel, fontsize=20, ha='left')

```




    <matplotlib.text.Text at 0x14a832f60>




![png](../../../../../images/course-materials/earth-analytics-python//week-5/in-class/2016-12-06-spatial06-extract-raster-values_53_1.png)



## View Difference: lidar vs measured

# this doesn't look right... 



```python

# Calculate difference
# also need to add the plot id to each xaxis label
SJER_final_height["lidar_measured"] = SJER_final_height["max"] - SJER_final_height["stemheight"]
SJER_final_height["lidar_measured"].plot(kind="bar")
```




    <matplotlib.axes._subplots.AxesSubplot at 0x14ac90a58>




![png](../../../../../images/course-materials/earth-analytics-python//week-5/in-class/2016-12-06-spatial06-extract-raster-values_55_1.png)

