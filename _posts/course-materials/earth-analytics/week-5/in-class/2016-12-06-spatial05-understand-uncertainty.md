---
layout: single
title: "Lidar Remote sensing data - Understand uncertainty / error associated with height metrics extracted from lidar raster data in Python"
excerpt: "In this lesson, we cover the topic of uncertainty. We focus on the types of uncertainty that you can expect when working with tree height data both derived from lidar remote sensing and human measurements. Further we cover sources of error including systematic vs. random error."
authors: ['Chris Holdgraf', 'Carson Farmer', 'Leah Wasser']
modified: 2017-05-24
category: [course-materials]
class-lesson: ['class-intro-spatial-python']
permalink: /course-materials/earth-analytics-python/week-5/understand-uncertainty-lidar/
nav-title: 'Remote sensing uncertainty'
module-type: 'class'
course: "Earth Analytics Python"
week: 5
sidebar:
  nav:
author_profile: false
comments: true
order: 5
---

# Lesson Notes
##  Is there a way to set the working directory when this builds - that way we can comment this out and in the nbconvert script it forces the working directory - this works best....
## Rasterstats needs to be loaded also geocoder and contextily - what do those do?
# i think we need to be consistent in how we import things. sometimes we are importing parts of a library separately - why?
## All of the plots on this page are visual representations thus the code should be hidden throughout. need to find out how to hide code!

{% include toc title="In This Lesson" icon="file-text" %}

<div class='notice--success' markdown="1">

## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives

After completing this tutorial, you will be able to:

* Be able to list atleast 3 sources of uncertainty / error associated with remote sensing data.
* Be able to interpret a scatter plot that compares remote sensing values with field measured values to determine how "well" the two metrics compare.
* Be able to describe 1-3 ways to better understand sources of error associated with a comparison between remote sensing values with field measured values.

## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need

You will need a computer with internet access to complete this lesson and the data for week 5 of the course.

</div>

## Understanding uncertainty and error.

It is important to consider error and uncertainty when presenting scientific
results. Most measurements that we make - be they from instruments or humans -
have uncertainty associated with them. We will discuss what
that means, below.

## Uncertainty

**Uncertainty:** Uncertainty quantifies the range of values within which the
value of the measure falls within - within a specified level of confidence. The
uncertainty quantitatively indicates the "quality" of your measurement. It
answers the question: "how well does the result represent the value of the
quantity being measured?"

### Tree height measurement example

So for example let's pretend that we measured the height of a tree 10 times. Each
time our tree height measurement may be slightly different? Why? Because maybe
each time we visually determined the top of the tree to be in a slightly different
place. Or maybe there was wind that day during measurements that
caused the tree to shift as we measured it yielding a slightly different height each time. or... what other reasons can you think of that might impact tree height
measurements?

<figure>
   <a href="{{ site.url }}/images/course-materials/earth-analytics/week-5/measuring-tree-height.jpg">
   <img src="{{ site.url }}/images/course-materials/earth-analytics/week-5/measuring-tree-height.jpg" alt="national geographic scaling trees graphic"></a>
   <figcaption>When we measure tree height by hand, many different variables may impact the accuracy and precision of our results. Source:  http://www.haddenham.net/newsroom/guess-tree-height.html
   </figcaption>
</figure>

## What is the true value?

So you may be wondering, what is the true height of our tree?
In the cause of a tree in a forest, it's very difficult to determine the
true height. So we accept that there will be some variation in our measurements
and we measure the tree over and over again until we understand the range of
heights that we are likely to get when we measure the tree.




```python
import os
# be sure to set your working directory
os.chdir("/Users/lewa8222/Documents/earth-analytics")

```


```python
import pandas as pd
import matplotlib.pyplot as plt
# why not just import glob?
from glob import glob

import numpy as np
import geopandas as gpd
# why import parts of raster io sepearately?
import rasterio as rio
from rasterio import plot as riop
import rasterstats as rs

import geocoder
import contextily as ctx
from shapely.geometry import Point
plt.ion()

# to install rasterstats & geocoder contextily use pip

```

## Why do we create a df here  (which i thnjk is better) vs previously we used a numpy array to create a list of xy locations.
## seems beter to just use pandas if we plan to use geopandas.
# below why is _ used -- this is different from how we set the axis title etc previously


```python
tree_heights = pd.DataFrame([10, 10.1, 9.9, 9.5, 9.7, 9.8, 9.6, 10.5, 10.7, 10.3, 10.6], columns=['heights'])

# What is the average tree height
print(tree_heights.mean(0))

# What is the standard deviation of measurements?
print(tree_heights.std())

# Make a boxplot to visualize
ax = tree_heights.plot.box()
_ = ax.set(title="Distribution of tree height measurements (m)", ylabel="Height (m)",
          xlabel="Distribution of tree heights")


```

    heights    10.063636
    dtype: float64
    heights    0.412971
    dtype: float64



![png](../../../../../images/course-materials/earth-analytics//week-5/in-class/2016-12-06-spatial05-understand-uncertainty_6_1.png)


In the example above, our mean tree height value is towards the center of
our distribution of measured heights. We might expect that the sample mean of
our observations provides a reasonable estimate of the true value. The
variation among our measured values may also provide some information about the
precision (or lack thereof) of the measurement process.

<a href="http://www.physics.csbsju.edu/stats/box2.html" target="_blank">Read more about  the basics of a box plot</a>

# Need to customize colors, make title larger, set up figure size so it's larger
# create axes without decimal points?


```python
ax = tree_heights.plot.hist(bins=[8, 8.5, 9.6, 10.2, 10.8, 11, 11.5], legend=False)
ax.set(title="Distribution of measured tree height values",
       xlabel="Height (m)")
ax.set_title(ax.get_title(),
             fontsize=20)

```




    <matplotlib.text.Text at 0x14af77518>




![png](../../../../../images/course-materials/earth-analytics//week-5/in-class/2016-12-06-spatial05-understand-uncertainty_9_1.png)


## Measurement accuracy

Measurement **accuracy** is a concept that relates to whether there is bias in
measurements, i.e. whether the expected value of our observations is close to
the true value. For low accuracy measurements, we may collect many observations,
and the mean of those observations may not provide a good measure of the truth
(e.g., the height of the tree). For high accuracy measurements, the mean of
many observations would provide a good measure of the true value. This is
different from **precision**, which typically refers to the variation among
observations. Accuracy and precision are not always tightly coupled. It is
possible to have measurements that are very precise but inaccurate, very
imprecise but accurate, etc.

## Systematic vs Random error

**Systematic error:** a systematic error is one that tends to shift all measurements
in a systematic way. This means that the mean value of a set of measurements is
consistently displaced or varied in a predictable way, leading to inaccurate observations.
Causes of systematic errors may be known or unknown but should always be corrected for when present.
For instance, no instrument can ever be calibrated perfectly, so when a group of measurements systematically differ from the value of a standard reference specimen, an adjustment in the values should be made.
Systematic error can be corrected for only when the "true value" (such as the value assigned to a calibration or reference specimen) is known.

*Example:* Remote sensing instruments need to be calibrated. For example a laser in
a lidar system may be tested in a lab to ensure that the distribution of output light energy
is consistent every time the laser "fires".

**Random error:** is a component of the total error which, in the course of a number of measurements, varies in an unpredictable way. It is not possible to correct for random error.  Random errors can occur for a variety of reasons such as:

* Lack of equipment sensitivity. An instrument may not be able to respond to or indicate a change in some quantity that is too small or the observer may not be able to discern the change.
* Noise in the measurement.  Noise is extraneous disturbances that are unpredictable or random and cannot be completely accounted for.
* Imprecise definition. It is difficult to exactly define the dimensions of a object.  For example, it is difficult to determine the ends of a crack with measuring its length.  Two people may likely pick two different starting and ending points.

*Example:* random error may be introduced when we measure tree heights as discussed above.

- <a href="https://www.nde-ed.org/GeneralResources/ErrorAnalysis/UncertaintyTerms.htm">Source: nde-ed.org</a>


<figure>
   <a href="{{ site.url }}/images/course-materials/earth-analytics/week-5/accuracy_precision.png">
   <img src="{{ site.url }}/images/course-materials/earth-analytics/week-5/accuracy_precision.png" alt="national geographic scaling trees graphic"></a>
   <figcaption>Accuracy vs precision. Accuracy quantifies how close a measured value is to the true value. Precision quantifies how close two or more measurements agree with each other (how quantitatively repeatable are the results) Source: http://www.ece.rochester.edu/courses/ECE111/error_uncertainty.pdf
   </figcaption>
</figure>

## Using lidar to estimate tree height

We use lidar data to estimate tree height because it is an efficient way to measure
large areas of trees (forests) quantitatively. However, we can process the lidar
data in many different ways to estimate height. Which method most closely represents
the actual heights of the trees on the ground?

<figure>
   <a href="{{ site.url }}/images/course-materials/earth-analytics/week-3/scaling-trees-nat-geo.jpg">
   <img src="{{ site.url }}/images/course-materials/earth-analytics/week-3/scaling-trees-nat-geo.jpg" alt="national geographic scaling trees graphic"></a>
   <figcaption>It can be difficult to measure the true height of trees! Often times "seeing" the very top of the tree where it is tallest is not possible from the ground - especially in dense, tall forests. One can imagine the amount of uncertainty that is thus introduced when we try to estimate the true height of trees! Image Source:
   National Geographic
   </figcaption>
</figure>

<figure>
   <a href="{{ site.url }}/images/course-materials/earth-analytics/week-3/waveform.png" target="_blank">
   <img src="{{ site.url }}/images/course-materials/earth-analytics/week-3/waveform.png" alt="Example of a lidar waveform"></a>
   <figcaption>An example LiDAR waveform. Source: NEON, Boulder, CO.
   </figcaption>
</figure>


<figure>
   <a href="{{ site.url }}/images/course-materials/earth-analytics/week-3/Treeline_ScannedPoints.png">
   <img src="{{ site.url }}/images/course-materials/earth-analytics/week-3/Treeline_ScannedPoints.png" alt="example of a tree profile after a lidar scan."></a>
   <figcaption>Cross section showing LiDAR point cloud data (above) and the
   corresponding landscape profile (below). Graphic: Leah A. Wasser
   </figcaption>
</figure>


```python
# not sure what this is doing -- it looks like it's trying to find all the shapefiles or something but i'm not sure why that is necessary
#folders = glob('/data/week5/california/*')
#files = glob(folders[0] + '/*.shp') + glob(folders[1] + '/*/*.shp') + glob(folders[1] + '/*/*/*')
#files
```




```python
# first buffer the plot points
# load sjer plot locations - shapefile format using geopandas
SJER_plots = gpd.read_file('data/week5/california/SJER/vector_data/SJER_plot_centroids.shp')
type(SJER_plots)
```




    geopandas.geodataframe.GeoDataFrame



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

# Below the attributes are not transfered - not sure how to force them to transfer


```python
# Create a 20m diameter 20m diameter circular buffer arond each point
# then export the buffered layer as a polygon shapefile using to_file

#SJER_plots.buffer(20).to_file(plot_buffer_path)

```


```python
# sneaky assign the buffer geometry to the points layer to maintain attributes
SJER_plots["geometry"] = SJER_plots.geometry.buffer(20)
SJER_plots["geometry"]
# export the layer as a shapefile to use in zonal stats
plot_buffer_path = 'plot_buffer.shp'
SJER_plots.to_file(plot_buffer_path)
```

## Extract pixel values for each plot

Once we have the boundary for each plot location (a 20m diameter circle) we can extract all of the pixels that fall within each circle using the function `zonal_stats` in the `rasterstats` library.




```python
# load lidar canopy height model raster  using rasterio
# note that we are using a context manager - with to do this
with rio.open('data/week5/california/SJER/2013/lidar/SJER_lidarCHM.tif') as lidar_chm_src:
    # read the data into a numpy array
    # note that the (1) ensures you get a 2 dimensional object rather than 3
    SJER_chm_data = lidar_chm_src.read(1)
    # set CHM values of 0 to NAN
    SJER_chm_data[SJER_chm_data == 0] = np.nan
    profile = lidar_chm_src.profile


# SJER_chm = rio.open('data/week5/california/SJER/2013/lidar/SJER_lidarCHM.tif')

# https://mapbox.github.io/rasterio/quickstart.html
#SJER_chm_data = SJER_chm.read()

# access the mask for the data
# note it seems that if we just added another no data value this could work?
#SJER_chm.read_masks()


#SJER_chm.nodata
#SJER_chm[SJER_chm==0] = np.nan
#SJER_chm.get_nodatavals()
```


```python
# this is a dictionary containing all of the spatial attributes of the geotiff
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




```python
SJER_chm_data.shape

```




    (5059, 4296)




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


Let's have a look at the structure ot type of the `SJER_chm_data` object. Notice that is it now a numpy array. This object is a generic object that does not contain associated spatial data attributes.

We can use the `.zonal_stats()` function within the `rasterio` package to extract values for a set of shapefile boundaries.

# NOTE the plot id doesn't export here - i must have broken something but am not sure what.
# Also copy_properties should transfer attributes but it's not.


```python
# import the buffer spatial object (shapefile)
gpd.read_file(plot_buffer_path)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Plot_ID</th>
      <th>Point</th>
      <th>easting</th>
      <th>geometry</th>
      <th>northing</th>
      <th>plot_type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SJER1068</td>
      <td>center</td>
      <td>255852.376</td>
      <td>POLYGON ((255872.376 4111567.818, 255872.27969...</td>
      <td>4111567.818</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SJER112</td>
      <td>center</td>
      <td>257406.967</td>
      <td>POLYGON ((257426.967 4111298.971, 257426.87069...</td>
      <td>4111298.971</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SJER116</td>
      <td>center</td>
      <td>256838.760</td>
      <td>POLYGON ((256858.76 4110819.876, 256858.663694...</td>
      <td>4110819.876</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SJER117</td>
      <td>center</td>
      <td>256176.947</td>
      <td>POLYGON ((256196.947 4108752.026, 256196.85069...</td>
      <td>4108752.026</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SJER120</td>
      <td>center</td>
      <td>255968.372</td>
      <td>POLYGON ((255988.372 4110476.079, 255988.27569...</td>
      <td>4110476.079</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>5</th>
      <td>SJER128</td>
      <td>center</td>
      <td>257078.867</td>
      <td>POLYGON ((257098.867 4111388.57, 257098.770694...</td>
      <td>4111388.570</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>6</th>
      <td>SJER192</td>
      <td>center</td>
      <td>256683.434</td>
      <td>POLYGON ((256703.434 4111071.087, 256703.33769...</td>
      <td>4111071.087</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>7</th>
      <td>SJER272</td>
      <td>center</td>
      <td>256717.467</td>
      <td>POLYGON ((256737.467 4112167.778, 256737.37069...</td>
      <td>4112167.778</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>8</th>
      <td>SJER2796</td>
      <td>center</td>
      <td>256034.390</td>
      <td>POLYGON ((256054.39 4111533.879, 256054.293694...</td>
      <td>4111533.879</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>9</th>
      <td>SJER3239</td>
      <td>center</td>
      <td>258497.102</td>
      <td>POLYGON ((258517.102 4109856.983, 258517.00569...</td>
      <td>4109856.983</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>10</th>
      <td>SJER36</td>
      <td>center</td>
      <td>258277.829</td>
      <td>POLYGON ((258297.829 4110161.674, 258297.73269...</td>
      <td>4110161.674</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>11</th>
      <td>SJER361</td>
      <td>center</td>
      <td>256961.794</td>
      <td>POLYGON ((256981.794 4107527.074, 256981.69769...</td>
      <td>4107527.074</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>12</th>
      <td>SJER37</td>
      <td>center</td>
      <td>256148.197</td>
      <td>POLYGON ((256168.197 4107578.841, 256168.10069...</td>
      <td>4107578.841</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>13</th>
      <td>SJER4</td>
      <td>center</td>
      <td>257228.336</td>
      <td>POLYGON ((257248.336 4109767.289, 257248.23969...</td>
      <td>4109767.289</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>14</th>
      <td>SJER8</td>
      <td>center</td>
      <td>254738.618</td>
      <td>POLYGON ((254758.618 4110249.265, 254758.52169...</td>
      <td>4110249.265</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>15</th>
      <td>SJER824</td>
      <td>center</td>
      <td>256185.584</td>
      <td>POLYGON ((256205.584 4110047.586, 256205.48769...</td>
      <td>4110047.586</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>16</th>
      <td>SJER916</td>
      <td>center</td>
      <td>257460.486</td>
      <td>POLYGON ((257480.486 4109616.679, 257480.38969...</td>
      <td>4109616.679</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>17</th>
      <td>SJER952</td>
      <td>center</td>
      <td>255871.194</td>
      <td>POLYGON ((255891.194 4110759.039, 255891.09769...</td>
      <td>4110759.039</td>
      <td>grass</td>
    </tr>
  </tbody>
</table>
</div>




```python
# import new geotiff with 0's removed
# Extract zonal stats
sjer_tree_heights = rs.zonal_stats(plot_buffer_path,
            lidar_path,
            geojson_out=True,
            copy_properties=True,
            stats="count min mean max median")
sjer_tree_heights
```

    /Users/lewa8222/anaconda/lib/python3.6/site-packages/rasterstats/main.py:142: FutureWarning: The value of this property will change in version 1.0. Please see https://github.com/mapbox/rasterio/issues/86 for details.
      with Raster(raster, affine, nodata, band) as rast:
    /Users/lewa8222/anaconda/lib/python3.6/site-packages/rasterstats/io.py:242: FutureWarning: GDAL-style transforms are deprecated and will not be supported in Rasterio 1.0.
      self.affine = guard_transform(self.src.transform)





    [{'geometry': {'coordinates': [[(255872.376, 4111567.818),
         (255872.27969453344, 4111565.857657193),
         (255871.99170560806, 4111563.9161935598),
         (255871.51480671464, 4111562.012306455),
         (255870.85359065022, 4111560.164331353),
         (255870.01442528696, 4111558.3900652635),
         (255869.00539224604, 4111556.7065953393),
         (255867.83620906723, 4111555.1301343166),
         (255866.51813562372, 4111553.675864376),
         (255865.06386568327, 4111552.3577909325),
         (255863.48740466038, 4111551.1886077537),
         (255861.8039347365, 4111550.179574713),
         (255860.0296686473, 4111549.3404093497),
         (255858.18169354508, 4111548.6791932853),
         (255856.2778064403, 4111548.202294392),
         (255854.33634280658, 4111547.9143054667),
         (255852.376, 4111547.818),
         (255850.4156571934, 4111547.9143054667),
         (255848.47419355967, 4111548.202294392),
         (255846.5703064549, 4111548.6791932853),
         (255844.72233135268, 4111549.3404093497),
         (255842.94806526348, 4111550.179574713),
         (255841.2645953396, 4111551.1886077537),
         (255839.6881343167, 4111552.3577909325),
         (255838.23386437626, 4111553.675864376),
         (255836.91579093275, 4111555.1301343166),
         (255835.74660775394, 4111556.7065953393),
         (255834.737574713, 4111558.3900652635),
         (255833.89840934976, 4111560.164331353),
         (255833.23719328534, 4111562.012306455),
         (255832.76029439192, 4111563.9161935598),
         (255832.47230546654, 4111565.857657193),
         (255832.376, 4111567.818),
         (255832.47230546654, 4111569.7783428067),
         (255832.76029439192, 4111571.71980644),
         (255833.23719328534, 4111573.623693545),
         (255833.89840934976, 4111575.471668647),
         (255834.737574713, 4111577.2459347364),
         (255835.74660775394, 4111578.9294046606),
         (255836.91579093275, 4111580.5058656833),
         (255838.23386437626, 4111581.960135624),
         (255839.6881343167, 4111583.2782090674),
         (255841.2645953396, 4111584.447392246),
         (255842.94806526348, 4111585.456425287),
         (255844.72233135268, 4111586.2955906503),
         (255846.5703064549, 4111586.9568067146),
         (255848.47419355967, 4111587.433705608),
         (255850.4156571934, 4111587.7216945332),
         (255852.376, 4111587.818),
         (255854.33634280658, 4111587.7216945332),
         (255856.2778064403, 4111587.433705608),
         (255858.18169354508, 4111586.9568067146),
         (255860.0296686473, 4111586.2955906503),
         (255861.8039347365, 4111585.456425287),
         (255863.48740466038, 4111584.447392246),
         (255865.06386568327, 4111583.2782090674),
         (255866.51813562372, 4111581.960135624),
         (255867.83620906723, 4111580.5058656833),
         (255869.00539224604, 4111578.9294046606),
         (255870.01442528696, 4111577.2459347364),
         (255870.85359065022, 4111575.471668647),
         (255871.51480671464, 4111573.623693545),
         (255871.99170560806, 4111571.71980644),
         (255872.27969453344, 4111569.7783428067),
         (255872.376, 4111567.818)]],
       'type': 'Polygon'},
      'id': '0',
      'properties': OrderedDict([('Plot_ID', 'SJER1068'),
                   ('Point', 'center'),
                   ('easting', 255852.376),
                   ('northing', 4111567.818),
                   ('plot_type', 'trees'),
                   ('min', 2.0399999618530273),
                   ('max', 19.049999237060547),
                   ('mean', 11.544347158870341),
                   ('count', 161),
                   ('median', 12.619999885559082)]),
      'type': 'Feature'},
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
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(256858.76, 4110819.876),
         (256858.66369453346, 4110817.9156571934),
         (256858.37570560808, 4110815.97419356),
         (256857.89880671466, 4110814.0703064553),
         (256857.23759065024, 4110812.222331353),
         (256856.39842528699, 4110810.4480652637),
         (256855.38939224606, 4110808.7645953395),
         (256854.22020906725, 4110807.188134317),
         (256852.90213562374, 4110805.7338643763),
         (256851.4478656833, 4110804.4157909327),
         (256849.8714046604, 4110803.246607754),
         (256848.18793473652, 4110802.2375747133),
         (256846.41366864732, 4110801.39840935),
         (256844.5656935451, 4110800.7371932855),
         (256842.66180644033, 4110800.2602943922),
         (256840.7203428066, 4110799.972305467),
         (256838.76, 4110799.876),
         (256836.79965719342, 4110799.972305467),
         (256834.8581935597, 4110800.2602943922),
         (256832.95430645492, 4110800.7371932855),
         (256831.1063313527, 4110801.39840935),
         (256829.3320652635, 4110802.2375747133),
         (256827.64859533962, 4110803.246607754),
         (256826.07213431672, 4110804.4157909327),
         (256824.61786437628, 4110805.7338643763),
         (256823.29979093277, 4110807.188134317),
         (256822.13060775396, 4110808.7645953395),
         (256821.12157471303, 4110810.4480652637),
         (256820.28240934978, 4110812.222331353),
         (256819.62119328536, 4110814.0703064553),
         (256819.14429439194, 4110815.97419356),
         (256818.85630546656, 4110817.9156571934),
         (256818.76, 4110819.876),
         (256818.85630546656, 4110821.836342807),
         (256819.14429439194, 4110823.7778064404),
         (256819.62119328536, 4110825.681693545),
         (256820.28240934978, 4110827.5296686473),
         (256821.12157471303, 4110829.3039347366),
         (256822.13060775396, 4110830.987404661),
         (256823.29979093277, 4110832.5638656835),
         (256824.61786437628, 4110834.018135624),
         (256826.07213431672, 4110835.3362090676),
         (256827.64859533962, 4110836.5053922464),
         (256829.3320652635, 4110837.514425287),
         (256831.1063313527, 4110838.3535906505),
         (256832.95430645492, 4110839.014806715),
         (256834.8581935597, 4110839.491705608),
         (256836.79965719342, 4110839.7796945334),
         (256838.76, 4110839.876),
         (256840.7203428066, 4110839.7796945334),
         (256842.66180644033, 4110839.491705608),
         (256844.5656935451, 4110839.014806715),
         (256846.41366864732, 4110838.3535906505),
         (256848.18793473652, 4110837.514425287),
         (256849.8714046604, 4110836.5053922464),
         (256851.4478656833, 4110835.3362090676),
         (256852.90213562374, 4110834.018135624),
         (256854.22020906725, 4110832.5638656835),
         (256855.38939224606, 4110830.987404661),
         (256856.39842528699, 4110829.3039347366),
         (256857.23759065024, 4110827.5296686473),
         (256857.89880671466, 4110825.681693545),
         (256858.37570560808, 4110823.7778064404),
         (256858.66369453346, 4110821.836342807),
         (256858.76, 4110819.876)]],
       'type': 'Polygon'},
      'id': '2',
      'properties': OrderedDict([('Plot_ID', 'SJER116'),
                   ('Point', 'center'),
                   ('easting', 256838.76),
                   ('northing', 4110819.876),
                   ('plot_type', 'grass'),
                   ('min', 2.819999933242798),
                   ('max', 16.06999969482422),
                   ('mean', 7.518398255248834),
                   ('count', 643),
                   ('median', 6.799999713897705)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(256196.947, 4108752.026),
         (256196.85069453344, 4108750.0656571933),
         (256196.56270560806, 4108748.12419356),
         (256196.08580671463, 4108746.220306455),
         (256195.42459065022, 4108744.372331353),
         (256194.58542528696, 4108742.5980652636),
         (256193.57639224603, 4108740.9145953394),
         (256192.40720906723, 4108739.3381343167),
         (256191.0891356237, 4108737.883864376),
         (256189.63486568327, 4108736.5657909326),
         (256188.05840466038, 4108735.396607754),
         (256186.3749347365, 4108734.387574713),
         (256184.6006686473, 4108733.5484093498),
         (256182.75269354507, 4108732.8871932854),
         (256180.8488064403, 4108732.410294392),
         (256178.90734280657, 4108732.122305467),
         (256176.947, 4108732.026),
         (256174.9866571934, 4108732.122305467),
         (256173.04519355966, 4108732.410294392),
         (256171.1413064549, 4108732.8871932854),
         (256169.29333135267, 4108733.5484093498),
         (256167.51906526348, 4108734.387574713),
         (256165.8355953396, 4108735.396607754),
         (256164.2591343167, 4108736.5657909326),
         (256162.80486437626, 4108737.883864376),
         (256161.48679093274, 4108739.3381343167),
         (256160.31760775394, 4108740.9145953394),
         (256159.308574713, 4108742.5980652636),
         (256158.46940934975, 4108744.372331353),
         (256157.80819328534, 4108746.220306455),
         (256157.33129439192, 4108748.12419356),
         (256157.04330546653, 4108750.0656571933),
         (256156.947, 4108752.026),
         (256157.04330546653, 4108753.986342807),
         (256157.33129439192, 4108755.9278064403),
         (256157.80819328534, 4108757.831693545),
         (256158.46940934975, 4108759.6796686472),
         (256159.308574713, 4108761.4539347365),
         (256160.31760775394, 4108763.1374046607),
         (256161.48679093274, 4108764.7138656834),
         (256162.80486437626, 4108766.168135624),
         (256164.2591343167, 4108767.4862090675),
         (256165.8355953396, 4108768.6553922463),
         (256167.51906526348, 4108769.664425287),
         (256169.29333135267, 4108770.5035906504),
         (256171.1413064549, 4108771.1648067147),
         (256173.04519355966, 4108771.641705608),
         (256174.9866571934, 4108771.9296945333),
         (256176.947, 4108772.026),
         (256178.90734280657, 4108771.9296945333),
         (256180.8488064403, 4108771.641705608),
         (256182.75269354507, 4108771.1648067147),
         (256184.6006686473, 4108770.5035906504),
         (256186.3749347365, 4108769.664425287),
         (256188.05840466038, 4108768.6553922463),
         (256189.63486568327, 4108767.4862090675),
         (256191.0891356237, 4108766.168135624),
         (256192.40720906723, 4108764.7138656834),
         (256193.57639224603, 4108763.1374046607),
         (256194.58542528696, 4108761.4539347365),
         (256195.42459065022, 4108759.6796686472),
         (256196.08580671463, 4108757.831693545),
         (256196.56270560806, 4108755.9278064403),
         (256196.85069453344, 4108753.986342807),
         (256196.947, 4108752.026)]],
       'type': 'Polygon'},
      'id': '3',
      'properties': OrderedDict([('Plot_ID', 'SJER117'),
                   ('Point', 'center'),
                   ('easting', 256176.947),
                   ('northing', 4108752.026),
                   ('plot_type', 'trees'),
                   ('min', 3.240000009536743),
                   ('max', 11.059999465942383),
                   ('mean', 7.675346281090561),
                   ('count', 245),
                   ('median', 7.929999828338623)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(255988.372, 4110476.079),
         (255988.27569453345, 4110474.118657193),
         (255987.98770560807, 4110472.1771935597),
         (255987.51080671465, 4110470.273306455),
         (255986.84959065024, 4110468.4253313527),
         (255986.01042528698, 4110466.6510652634),
         (255985.00139224605, 4110464.9675953393),
         (255983.83220906724, 4110463.3911343166),
         (255982.51413562373, 4110461.936864376),
         (255981.0598656833, 4110460.6187909325),
         (255979.4834046604, 4110459.4496077537),
         (255977.7999347365, 4110458.440574713),
         (255976.02566864731, 4110457.6014093496),
         (255974.1776935451, 4110456.9401932852),
         (255972.27380644032, 4110456.463294392),
         (255970.3323428066, 4110456.1753054666),
         (255968.372, 4110456.079),
         (255966.4116571934, 4110456.1753054666),
         (255964.47019355968, 4110456.463294392),
         (255962.56630645492, 4110456.9401932852),
         (255960.7183313527, 4110457.6014093496),
         (255958.9440652635, 4110458.440574713),
         (255957.2605953396, 4110459.4496077537),
         (255955.68413431672, 4110460.6187909325),
         (255954.22986437628, 4110461.936864376),
         (255952.91179093276, 4110463.3911343166),
         (255951.74260775396, 4110464.9675953393),
         (255950.73357471303, 4110466.6510652634),
         (255949.89440934977, 4110468.4253313527),
         (255949.23319328536, 4110470.273306455),
         (255948.75629439193, 4110472.1771935597),
         (255948.46830546655, 4110474.118657193),
         (255948.372, 4110476.079),
         (255948.46830546655, 4110478.0393428067),
         (255948.75629439193, 4110479.98080644),
         (255949.23319328536, 4110481.884693545),
         (255949.89440934977, 4110483.732668647),
         (255950.73357471303, 4110485.5069347364),
         (255951.74260775396, 4110487.1904046605),
         (255952.91179093276, 4110488.7668656833),
         (255954.22986437628, 4110490.2211356238),
         (255955.68413431672, 4110491.5392090674),
         (255957.2605953396, 4110492.708392246),
         (255958.9440652635, 4110493.717425287),
         (255960.7183313527, 4110494.55659065),
         (255962.56630645492, 4110495.2178067146),
         (255964.47019355968, 4110495.694705608),
         (255966.4116571934, 4110495.982694533),
         (255968.372, 4110496.079),
         (255970.3323428066, 4110495.982694533),
         (255972.27380644032, 4110495.694705608),
         (255974.1776935451, 4110495.2178067146),
         (255976.02566864731, 4110494.55659065),
         (255977.7999347365, 4110493.717425287),
         (255979.4834046604, 4110492.708392246),
         (255981.0598656833, 4110491.5392090674),
         (255982.51413562373, 4110490.2211356238),
         (255983.83220906724, 4110488.7668656833),
         (255985.00139224605, 4110487.1904046605),
         (255986.01042528698, 4110485.5069347364),
         (255986.84959065024, 4110483.732668647),
         (255987.51080671465, 4110481.884693545),
         (255987.98770560807, 4110479.98080644),
         (255988.27569453345, 4110478.0393428067),
         (255988.372, 4110476.079)]],
       'type': 'Polygon'},
      'id': '4',
      'properties': OrderedDict([('Plot_ID', 'SJER120'),
                   ('Point', 'center'),
                   ('easting', 255968.372),
                   ('northing', 4110476.079),
                   ('plot_type', 'grass'),
                   ('min', 3.379999876022339),
                   ('max', 5.739999771118164),
                   ('mean', 4.5911766501034),
                   ('count', 17),
                   ('median', 4.449999809265137)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(257098.867, 4111388.57),
         (257098.77069453345, 4111386.609657193),
         (257098.48270560807, 4111384.6681935596),
         (257098.00580671465, 4111382.764306455),
         (257097.34459065023, 4111380.9163313527),
         (257096.50542528697, 4111379.1420652634),
         (257095.49639224604, 4111377.458595339),
         (257094.32720906724, 4111375.8821343165),
         (257093.00913562372, 4111374.427864376),
         (257091.55486568328, 4111373.1097909324),
         (257089.9784046604, 4111371.9406077536),
         (257088.2949347365, 4111370.931574713),
         (257086.5206686473, 4111370.0924093495),
         (257084.6726935451, 4111369.431193285),
         (257082.76880644032, 4111368.954294392),
         (257080.8273428066, 4111368.6663054666),
         (257078.867, 4111368.57),
         (257076.9066571934, 4111368.6663054666),
         (257074.96519355968, 4111368.954294392),
         (257073.0613064549, 4111369.431193285),
         (257071.2133313527, 4111370.0924093495),
         (257069.4390652635, 4111370.931574713),
         (257067.7555953396, 4111371.9406077536),
         (257066.1791343167, 4111373.1097909324),
         (257064.72486437627, 4111374.427864376),
         (257063.40679093276, 4111375.8821343165),
         (257062.23760775395, 4111377.458595339),
         (257061.22857471302, 4111379.1420652634),
         (257060.38940934977, 4111380.9163313527),
         (257059.72819328535, 4111382.764306455),
         (257059.25129439193, 4111384.6681935596),
         (257058.96330546655, 4111386.609657193),
         (257058.867, 4111388.57),
         (257058.96330546655, 4111390.5303428066),
         (257059.25129439193, 4111392.47180644),
         (257059.72819328535, 4111394.3756935447),
         (257060.38940934977, 4111396.223668647),
         (257061.22857471302, 4111397.9979347363),
         (257062.23760775395, 4111399.6814046605),
         (257063.40679093276, 4111401.257865683),
         (257064.72486437627, 4111402.7121356237),
         (257066.1791343167, 4111404.0302090673),
         (257067.7555953396, 4111405.199392246),
         (257069.4390652635, 4111406.2084252867),
         (257071.2133313527, 4111407.04759065),
         (257073.0613064549, 4111407.7088067145),
         (257074.96519355968, 4111408.1857056078),
         (257076.9066571934, 4111408.473694533),
         (257078.867, 4111408.57),
         (257080.8273428066, 4111408.473694533),
         (257082.76880644032, 4111408.1857056078),
         (257084.6726935451, 4111407.7088067145),
         (257086.5206686473, 4111407.04759065),
         (257088.2949347365, 4111406.2084252867),
         (257089.9784046604, 4111405.199392246),
         (257091.55486568328, 4111404.0302090673),
         (257093.00913562372, 4111402.7121356237),
         (257094.32720906724, 4111401.257865683),
         (257095.49639224604, 4111399.6814046605),
         (257096.50542528697, 4111397.9979347363),
         (257097.34459065023, 4111396.223668647),
         (257098.00580671465, 4111394.3756935447),
         (257098.48270560807, 4111392.47180644),
         (257098.77069453345, 4111390.5303428066),
         (257098.867, 4111388.57)]],
       'type': 'Polygon'},
      'id': '5',
      'properties': OrderedDict([('Plot_ID', 'SJER128'),
                   ('Point', 'center'),
                   ('easting', 257078.867),
                   ('northing', 4111388.57),
                   ('plot_type', 'trees'),
                   ('min', 2.1599998474121094),
                   ('max', 19.139999389648438),
                   ('mean', 8.987086819225722),
                   ('count', 381),
                   ('median', 8.019999504089355)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(256703.434, 4111071.087),
         (256703.33769453346, 4111069.126657193),
         (256703.04970560808, 4111067.1851935596),
         (256702.57280671466, 4111065.281306455),
         (256701.91159065024, 4111063.4333313527),
         (256701.07242528698, 4111061.6590652633),
         (256700.06339224605, 4111059.975595339),
         (256698.89420906725, 4111058.3991343165),
         (256697.57613562373, 4111056.944864376),
         (256696.1218656833, 4111055.6267909324),
         (256694.5454046604, 4111054.4576077536),
         (256692.86193473652, 4111053.448574713),
         (256691.08766864732, 4111052.6094093495),
         (256689.2396935451, 4111051.948193285),
         (256687.33580644033, 4111051.471294392),
         (256685.3943428066, 4111051.1833054665),
         (256683.434, 4111051.087),
         (256681.47365719342, 4111051.1833054665),
         (256679.5321935597, 4111051.471294392),
         (256677.62830645492, 4111051.948193285),
         (256675.7803313527, 4111052.6094093495),
         (256674.0060652635, 4111053.448574713),
         (256672.32259533962, 4111054.4576077536),
         (256670.74613431672, 4111055.6267909324),
         (256669.29186437628, 4111056.944864376),
         (256667.97379093277, 4111058.3991343165),
         (256666.80460775396, 4111059.975595339),
         (256665.79557471303, 4111061.6590652633),
         (256664.95640934978, 4111063.4333313527),
         (256664.29519328536, 4111065.281306455),
         (256663.81829439194, 4111067.1851935596),
         (256663.53030546656, 4111069.126657193),
         (256663.434, 4111071.087),
         (256663.53030546656, 4111073.0473428066),
         (256663.81829439194, 4111074.98880644),
         (256664.29519328536, 4111076.8926935447),
         (256664.95640934978, 4111078.740668647),
         (256665.79557471303, 4111080.5149347363),
         (256666.80460775396, 4111082.1984046604),
         (256667.97379093277, 4111083.774865683),
         (256669.29186437628, 4111085.2291356237),
         (256670.74613431672, 4111086.5472090673),
         (256672.32259533962, 4111087.716392246),
         (256674.0060652635, 4111088.7254252867),
         (256675.7803313527, 4111089.56459065),
         (256677.62830645492, 4111090.2258067145),
         (256679.5321935597, 4111090.7027056077),
         (256681.47365719342, 4111090.990694533),
         (256683.434, 4111091.087),
         (256685.3943428066, 4111090.990694533),
         (256687.33580644033, 4111090.7027056077),
         (256689.2396935451, 4111090.2258067145),
         (256691.08766864732, 4111089.56459065),
         (256692.86193473652, 4111088.7254252867),
         (256694.5454046604, 4111087.716392246),
         (256696.1218656833, 4111086.5472090673),
         (256697.57613562373, 4111085.2291356237),
         (256698.89420906725, 4111083.774865683),
         (256700.06339224605, 4111082.1984046604),
         (256701.07242528698, 4111080.5149347363),
         (256701.91159065024, 4111078.740668647),
         (256702.57280671466, 4111076.8926935447),
         (256703.04970560808, 4111074.98880644),
         (256703.33769453346, 4111073.0473428066),
         (256703.434, 4111071.087)]],
       'type': 'Polygon'},
      'id': '6',
      'properties': OrderedDict([('Plot_ID', 'SJER192'),
                   ('Point', 'center'),
                   ('easting', 256683.434),
                   ('northing', 4111071.087),
                   ('plot_type', 'grass'),
                   ('min', 2.200000047683716),
                   ('max', 16.549999237060547),
                   ('mean', 7.229095886033369),
                   ('count', 929),
                   ('median', 6.62999963760376)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(256737.467, 4112167.778),
         (256737.37069453346, 4112165.817657193),
         (256737.08270560807, 4112163.8761935597),
         (256736.60580671465, 4112161.972306455),
         (256735.94459065024, 4112160.1243313528),
         (256735.10542528698, 4112158.3500652635),
         (256734.09639224605, 4112156.6665953393),
         (256732.92720906725, 4112155.0901343166),
         (256731.60913562373, 4112153.635864376),
         (256730.1548656833, 4112152.3177909325),
         (256728.5784046604, 4112151.1486077537),
         (256726.8949347365, 4112150.139574713),
         (256725.12066864732, 4112149.3004093496),
         (256723.2726935451, 4112148.6391932853),
         (256721.36880644032, 4112148.162294392),
         (256719.4273428066, 4112147.8743054667),
         (256717.467, 4112147.778),
         (256715.50665719341, 4112147.8743054667),
         (256713.56519355968, 4112148.162294392),
         (256711.66130645492, 4112148.6391932853),
         (256709.8133313527, 4112149.3004093496),
         (256708.0390652635, 4112150.139574713),
         (256706.3555953396, 4112151.1486077537),
         (256704.77913431672, 4112152.3177909325),
         (256703.32486437628, 4112153.635864376),
         (256702.00679093276, 4112155.0901343166),
         (256700.83760775396, 4112156.6665953393),
         (256699.82857471303, 4112158.3500652635),
         (256698.98940934977, 4112160.1243313528),
         (256698.32819328536, 4112161.972306455),
         (256697.85129439193, 4112163.8761935597),
         (256697.56330546655, 4112165.817657193),
         (256697.467, 4112167.778),
         (256697.56330546655, 4112169.7383428067),
         (256697.85129439193, 4112171.67980644),
         (256698.32819328536, 4112173.583693545),
         (256698.98940934977, 4112175.431668647),
         (256699.82857471303, 4112177.2059347364),
         (256700.83760775396, 4112178.8894046606),
         (256702.00679093276, 4112180.4658656833),
         (256703.32486437628, 4112181.920135624),
         (256704.77913431672, 4112183.2382090674),
         (256706.3555953396, 4112184.407392246),
         (256708.0390652635, 4112185.416425287),
         (256709.8133313527, 4112186.2555906503),
         (256711.66130645492, 4112186.9168067146),
         (256713.56519355968, 4112187.393705608),
         (256715.50665719341, 4112187.681694533),
         (256717.467, 4112187.778),
         (256719.4273428066, 4112187.681694533),
         (256721.36880644032, 4112187.393705608),
         (256723.2726935451, 4112186.9168067146),
         (256725.12066864732, 4112186.2555906503),
         (256726.8949347365, 4112185.416425287),
         (256728.5784046604, 4112184.407392246),
         (256730.1548656833, 4112183.2382090674),
         (256731.60913562373, 4112181.920135624),
         (256732.92720906725, 4112180.4658656833),
         (256734.09639224605, 4112178.8894046606),
         (256735.10542528698, 4112177.2059347364),
         (256735.94459065024, 4112175.431668647),
         (256736.60580671465, 4112173.583693545),
         (256737.08270560807, 4112171.67980644),
         (256737.37069453346, 4112169.7383428067),
         (256737.467, 4112167.778)]],
       'type': 'Polygon'},
      'id': '7',
      'properties': OrderedDict([('Plot_ID', 'SJER272'),
                   ('Point', 'center'),
                   ('easting', 256717.467),
                   ('northing', 4112167.778),
                   ('plot_type', 'trees'),
                   ('min', 2.369999885559082),
                   ('max', 11.84000015258789),
                   ('mean', 7.107060643020394),
                   ('count', 711),
                   ('median', 6.980000019073486)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(256054.39, 4111533.879),
         (256054.29369453347, 4111531.9186571934),
         (256054.00570560808, 4111529.97719356),
         (256053.52880671466, 4111528.0733064553),
         (256052.86759065025, 4111526.225331353),
         (256052.028425287, 4111524.4510652637),
         (256051.01939224606, 4111522.7675953396),
         (256049.85020906726, 4111521.191134317),
         (256048.53213562374, 4111519.7368643763),
         (256047.0778656833, 4111518.4187909327),
         (256045.5014046604, 4111517.249607754),
         (256043.81793473652, 4111516.2405747133),
         (256042.04366864733, 4111515.40140935),
         (256040.1956935451, 4111514.7401932855),
         (256038.29180644033, 4111514.2632943923),
         (256036.3503428066, 4111513.975305467),
         (256034.39, 4111513.879),
         (256032.42965719342, 4111513.975305467),
         (256030.4881935597, 4111514.2632943923),
         (256028.58430645493, 4111514.7401932855),
         (256026.7363313527, 4111515.40140935),
         (256024.9620652635, 4111516.2405747133),
         (256023.27859533962, 4111517.249607754),
         (256021.70213431673, 4111518.4187909327),
         (256020.2478643763, 4111519.7368643763),
         (256018.92979093277, 4111521.191134317),
         (256017.76060775397, 4111522.7675953396),
         (256016.75157471304, 4111524.4510652637),
         (256015.91240934978, 4111526.225331353),
         (256015.25119328537, 4111528.0733064553),
         (256014.77429439194, 4111529.97719356),
         (256014.48630546656, 4111531.9186571934),
         (256014.39, 4111533.879),
         (256014.48630546656, 4111535.839342807),
         (256014.77429439194, 4111537.7808064404),
         (256015.25119328537, 4111539.684693545),
         (256015.91240934978, 4111541.5326686474),
         (256016.75157471304, 4111543.3069347367),
         (256017.76060775397, 4111544.990404661),
         (256018.92979093277, 4111546.5668656835),
         (256020.2478643763, 4111548.021135624),
         (256021.70213431673, 4111549.3392090676),
         (256023.27859533962, 4111550.5083922464),
         (256024.9620652635, 4111551.517425287),
         (256026.7363313527, 4111552.3565906505),
         (256028.58430645493, 4111553.017806715),
         (256030.4881935597, 4111553.494705608),
         (256032.42965719342, 4111553.7826945335),
         (256034.39, 4111553.879),
         (256036.3503428066, 4111553.7826945335),
         (256038.29180644033, 4111553.494705608),
         (256040.1956935451, 4111553.017806715),
         (256042.04366864733, 4111552.3565906505),
         (256043.81793473652, 4111551.517425287),
         (256045.5014046604, 4111550.5083922464),
         (256047.0778656833, 4111549.3392090676),
         (256048.53213562374, 4111548.021135624),
         (256049.85020906726, 4111546.5668656835),
         (256051.01939224606, 4111544.990404661),
         (256052.028425287, 4111543.3069347367),
         (256052.86759065025, 4111541.5326686474),
         (256053.52880671466, 4111539.684693545),
         (256054.00570560808, 4111537.7808064404),
         (256054.29369453347, 4111535.839342807),
         (256054.39, 4111533.879)]],
       'type': 'Polygon'},
      'id': '8',
      'properties': OrderedDict([('Plot_ID', 'SJER2796'),
                   ('Point', 'center'),
                   ('easting', 256034.39),
                   ('northing', 4111533.879),
                   ('plot_type', 'soil'),
                   ('min', 2.0299999713897705),
                   ('max', 20.279998779296875),
                   ('mean', 6.409629539207176),
                   ('count', 270),
                   ('median', 6.229999542236328)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(258517.102, 4109856.983),
         (258517.00569453347, 4109855.0226571932),
         (258516.71770560808, 4109853.08119356),
         (258516.24080671466, 4109851.177306455),
         (258515.57959065025, 4109849.329331353),
         (258514.740425287, 4109847.5550652635),
         (258513.73139224606, 4109845.8715953394),
         (258512.56220906726, 4109844.2951343167),
         (258511.24413562374, 4109842.840864376),
         (258509.7898656833, 4109841.5227909326),
         (258508.2134046604, 4109840.3536077538),
         (258506.52993473652, 4109839.344574713),
         (258504.75566864733, 4109838.5054093497),
         (258502.9076935451, 4109837.8441932853),
         (258501.00380644033, 4109837.367294392),
         (258499.0623428066, 4109837.0793054667),
         (258497.102, 4109836.983),
         (258495.14165719342, 4109837.0793054667),
         (258493.2001935597, 4109837.367294392),
         (258491.29630645493, 4109837.8441932853),
         (258489.4483313527, 4109838.5054093497),
         (258487.6740652635, 4109839.344574713),
         (258485.99059533962, 4109840.3536077538),
         (258484.41413431673, 4109841.5227909326),
         (258482.9598643763, 4109842.840864376),
         (258481.64179093277, 4109844.2951343167),
         (258480.47260775397, 4109845.8715953394),
         (258479.46357471304, 4109847.5550652635),
         (258478.62440934978, 4109849.329331353),
         (258477.96319328537, 4109851.177306455),
         (258477.48629439194, 4109853.08119356),
         (258477.19830546656, 4109855.0226571932),
         (258477.102, 4109856.983),
         (258477.19830546656, 4109858.943342807),
         (258477.48629439194, 4109860.88480644),
         (258477.96319328537, 4109862.788693545),
         (258478.62440934978, 4109864.636668647),
         (258479.46357471304, 4109866.4109347365),
         (258480.47260775397, 4109868.0944046606),
         (258481.64179093277, 4109869.6708656834),
         (258482.9598643763, 4109871.125135624),
         (258484.41413431673, 4109872.4432090675),
         (258485.99059533962, 4109873.6123922463),
         (258487.6740652635, 4109874.621425287),
         (258489.4483313527, 4109875.4605906503),
         (258491.29630645493, 4109876.1218067147),
         (258493.2001935597, 4109876.598705608),
         (258495.14165719342, 4109876.8866945333),
         (258497.102, 4109876.983),
         (258499.0623428066, 4109876.8866945333),
         (258501.00380644033, 4109876.598705608),
         (258502.9076935451, 4109876.1218067147),
         (258504.75566864733, 4109875.4605906503),
         (258506.52993473652, 4109874.621425287),
         (258508.2134046604, 4109873.6123922463),
         (258509.7898656833, 4109872.4432090675),
         (258511.24413562374, 4109871.125135624),
         (258512.56220906726, 4109869.6708656834),
         (258513.73139224606, 4109868.0944046606),
         (258514.740425287, 4109866.4109347365),
         (258515.57959065025, 4109864.636668647),
         (258516.24080671466, 4109862.788693545),
         (258516.71770560808, 4109860.88480644),
         (258517.00569453347, 4109858.943342807),
         (258517.102, 4109856.983)]],
       'type': 'Polygon'},
      'id': '9',
      'properties': OrderedDict([('Plot_ID', 'SJER3239'),
                   ('Point', 'center'),
                   ('easting', 258497.102),
                   ('northing', 4109856.983),
                   ('plot_type', 'soil'),
                   ('min', 2.0199999809265137),
                   ('max', 12.90999984741211),
                   ('mean', 6.00912835536859),
                   ('count', 195),
                   ('median', 5.949999809265137)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(258297.829, 4110161.674),
         (258297.73269453345, 4110159.7136571934),
         (258297.44470560807, 4110157.77219356),
         (258296.96780671465, 4110155.868306455),
         (258296.30659065023, 4110154.020331353),
         (258295.46742528697, 4110152.2460652636),
         (258294.45839224604, 4110150.5625953395),
         (258293.28920906724, 4110148.986134317),
         (258291.97113562372, 4110147.5318643763),
         (258290.51686568328, 4110146.2137909327),
         (258288.9404046604, 4110145.044607754),
         (258287.2569347365, 4110144.0355747133),
         (258285.4826686473, 4110143.19640935),
         (258283.6346935451, 4110142.5351932854),
         (258281.73080644032, 4110142.058294392),
         (258279.7893428066, 4110141.770305467),
         (258277.829, 4110141.674),
         (258275.8686571934, 4110141.770305467),
         (258273.92719355968, 4110142.058294392),
         (258272.0233064549, 4110142.5351932854),
         (258270.1753313527, 4110143.19640935),
         (258268.4010652635, 4110144.0355747133),
         (258266.7175953396, 4110145.044607754),
         (258265.1411343167, 4110146.2137909327),
         (258263.68686437627, 4110147.5318643763),
         (258262.36879093276, 4110148.986134317),
         (258261.19960775395, 4110150.5625953395),
         (258260.19057471302, 4110152.2460652636),
         (258259.35140934977, 4110154.020331353),
         (258258.69019328535, 4110155.868306455),
         (258258.21329439193, 4110157.77219356),
         (258257.92530546655, 4110159.7136571934),
         (258257.829, 4110161.674),
         (258257.92530546655, 4110163.634342807),
         (258258.21329439193, 4110165.5758064403),
         (258258.69019328535, 4110167.479693545),
         (258259.35140934977, 4110169.3276686473),
         (258260.19057471302, 4110171.1019347366),
         (258261.19960775395, 4110172.7854046607),
         (258262.36879093276, 4110174.3618656835),
         (258263.68686437627, 4110175.816135624),
         (258265.1411343167, 4110177.1342090676),
         (258266.7175953396, 4110178.3033922464),
         (258268.4010652635, 4110179.312425287),
         (258270.1753313527, 4110180.1515906504),
         (258272.0233064549, 4110180.812806715),
         (258273.92719355968, 4110181.289705608),
         (258275.8686571934, 4110181.5776945334),
         (258277.829, 4110181.674),
         (258279.7893428066, 4110181.5776945334),
         (258281.73080644032, 4110181.289705608),
         (258283.6346935451, 4110180.812806715),
         (258285.4826686473, 4110180.1515906504),
         (258287.2569347365, 4110179.312425287),
         (258288.9404046604, 4110178.3033922464),
         (258290.51686568328, 4110177.1342090676),
         (258291.97113562372, 4110175.816135624),
         (258293.28920906724, 4110174.3618656835),
         (258294.45839224604, 4110172.7854046607),
         (258295.46742528697, 4110171.1019347366),
         (258296.30659065023, 4110169.3276686473),
         (258296.96780671465, 4110167.479693545),
         (258297.44470560807, 4110165.5758064403),
         (258297.73269453345, 4110163.634342807),
         (258297.829, 4110161.674)]],
       'type': 'Polygon'},
      'id': '10',
      'properties': OrderedDict([('Plot_ID', 'SJER36'),
                   ('Point', 'center'),
                   ('easting', 258277.829),
                   ('northing', 4110161.674),
                   ('plot_type', 'trees'),
                   ('min', 2.0299999713897705),
                   ('max', 8.989999771118164),
                   ('mean', 6.516288206749356),
                   ('count', 97),
                   ('median', 6.679999828338623)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(256981.794, 4107527.074),
         (256981.69769453345, 4107525.1136571933),
         (256981.40970560806, 4107523.17219356),
         (256980.93280671464, 4107521.268306455),
         (256980.27159065023, 4107519.420331353),
         (256979.43242528697, 4107517.6460652635),
         (256978.42339224604, 4107515.9625953394),
         (256977.25420906724, 4107514.3861343167),
         (256975.93613562372, 4107512.931864376),
         (256974.48186568328, 4107511.6137909326),
         (256972.90540466039, 4107510.444607754),
         (256971.2219347365, 4107509.435574713),
         (256969.4476686473, 4107508.5964093497),
         (256967.59969354508, 4107507.9351932853),
         (256965.69580644032, 4107507.458294392),
         (256963.75434280658, 4107507.1703054667),
         (256961.794, 4107507.074),
         (256959.8336571934, 4107507.1703054667),
         (256957.89219355967, 4107507.458294392),
         (256955.9883064549, 4107507.9351932853),
         (256954.14033135268, 4107508.5964093497),
         (256952.3660652635, 4107509.435574713),
         (256950.6825953396, 4107510.444607754),
         (256949.1061343167, 4107511.6137909326),
         (256947.65186437627, 4107512.931864376),
         (256946.33379093275, 4107514.3861343167),
         (256945.16460775395, 4107515.9625953394),
         (256944.15557471302, 4107517.6460652635),
         (256943.31640934976, 4107519.420331353),
         (256942.65519328535, 4107521.268306455),
         (256942.17829439192, 4107523.17219356),
         (256941.89030546654, 4107525.1136571933),
         (256941.794, 4107527.074),
         (256941.89030546654, 4107529.034342807),
         (256942.17829439192, 4107530.97580644),
         (256942.65519328535, 4107532.879693545),
         (256943.31640934976, 4107534.727668647),
         (256944.15557471302, 4107536.5019347365),
         (256945.16460775395, 4107538.1854046606),
         (256946.33379093275, 4107539.7618656834),
         (256947.65186437627, 4107541.216135624),
         (256949.1061343167, 4107542.5342090675),
         (256950.6825953396, 4107543.7033922463),
         (256952.3660652635, 4107544.712425287),
         (256954.14033135268, 4107545.5515906503),
         (256955.9883064549, 4107546.2128067147),
         (256957.89219355967, 4107546.689705608),
         (256959.8336571934, 4107546.9776945333),
         (256961.794, 4107547.074),
         (256963.75434280658, 4107546.9776945333),
         (256965.69580644032, 4107546.689705608),
         (256967.59969354508, 4107546.2128067147),
         (256969.4476686473, 4107545.5515906503),
         (256971.2219347365, 4107544.712425287),
         (256972.90540466039, 4107543.7033922463),
         (256974.48186568328, 4107542.5342090675),
         (256975.93613562372, 4107541.216135624),
         (256977.25420906724, 4107539.7618656834),
         (256978.42339224604, 4107538.1854046606),
         (256979.43242528697, 4107536.5019347365),
         (256980.27159065023, 4107534.727668647),
         (256980.93280671464, 4107532.879693545),
         (256981.40970560806, 4107530.97580644),
         (256981.69769453345, 4107529.034342807),
         (256981.794, 4107527.074)]],
       'type': 'Polygon'},
      'id': '11',
      'properties': OrderedDict([('Plot_ID', 'SJER361'),
                   ('Point', 'center'),
                   ('easting', 256961.794),
                   ('northing', 4107527.074),
                   ('plot_type', 'grass'),
                   ('min', 2.119999885559082),
                   ('max', 18.729999542236328),
                   ('mean', 13.899027506510416),
                   ('count', 72),
                   ('median', 13.684999465942383)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(256168.197, 4107578.841),
         (256168.10069453344, 4107576.8806571933),
         (256167.81270560806, 4107574.93919356),
         (256167.33580671463, 4107573.035306455),
         (256166.67459065022, 4107571.187331353),
         (256165.83542528696, 4107569.4130652635),
         (256164.82639224603, 4107567.7295953394),
         (256163.65720906723, 4107566.1531343167),
         (256162.3391356237, 4107564.698864376),
         (256160.88486568327, 4107563.3807909326),
         (256159.30840466038, 4107562.2116077538),
         (256157.6249347365, 4107561.202574713),
         (256155.8506686473, 4107560.3634093497),
         (256154.00269354507, 4107559.7021932853),
         (256152.0988064403, 4107559.225294392),
         (256150.15734280657, 4107558.9373054667),
         (256148.197, 4107558.841),
         (256146.2366571934, 4107558.9373054667),
         (256144.29519355966, 4107559.225294392),
         (256142.3913064549, 4107559.7021932853),
         (256140.54333135267, 4107560.3634093497),
         (256138.76906526348, 4107561.202574713),
         (256137.0855953396, 4107562.2116077538),
         (256135.5091343167, 4107563.3807909326),
         (256134.05486437626, 4107564.698864376),
         (256132.73679093274, 4107566.1531343167),
         (256131.56760775394, 4107567.7295953394),
         (256130.558574713, 4107569.4130652635),
         (256129.71940934975, 4107571.187331353),
         (256129.05819328534, 4107573.035306455),
         (256128.58129439192, 4107574.93919356),
         (256128.29330546653, 4107576.8806571933),
         (256128.197, 4107578.841),
         (256128.29330546653, 4107580.801342807),
         (256128.58129439192, 4107582.74280644),
         (256129.05819328534, 4107584.646693545),
         (256129.71940934975, 4107586.494668647),
         (256130.558574713, 4107588.2689347365),
         (256131.56760775394, 4107589.9524046606),
         (256132.73679093274, 4107591.5288656834),
         (256134.05486437626, 4107592.983135624),
         (256135.5091343167, 4107594.3012090675),
         (256137.0855953396, 4107595.4703922463),
         (256138.76906526348, 4107596.479425287),
         (256140.54333135267, 4107597.3185906503),
         (256142.3913064549, 4107597.9798067147),
         (256144.29519355966, 4107598.456705608),
         (256146.2366571934, 4107598.7446945333),
         (256148.197, 4107598.841),
         (256150.15734280657, 4107598.7446945333),
         (256152.0988064403, 4107598.456705608),
         (256154.00269354507, 4107597.9798067147),
         (256155.8506686473, 4107597.3185906503),
         (256157.6249347365, 4107596.479425287),
         (256159.30840466038, 4107595.4703922463),
         (256160.88486568327, 4107594.3012090675),
         (256162.3391356237, 4107592.983135624),
         (256163.65720906723, 4107591.5288656834),
         (256164.82639224603, 4107589.9524046606),
         (256165.83542528696, 4107588.2689347365),
         (256166.67459065022, 4107586.494668647),
         (256167.33580671463, 4107584.646693545),
         (256167.81270560806, 4107582.74280644),
         (256168.10069453344, 4107580.801342807),
         (256168.197, 4107578.841)]],
       'type': 'Polygon'},
      'id': '12',
      'properties': OrderedDict([('Plot_ID', 'SJER37'),
                   ('Point', 'center'),
                   ('easting', 256148.197),
                   ('northing', 4107578.841),
                   ('plot_type', 'trees'),
                   ('min', 2.190000057220459),
                   ('max', 11.489999771118164),
                   ('mean', 7.109849920320274),
                   ('count', 201),
                   ('median', 7.099999904632568)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(257248.336, 4109767.289),
         (257248.23969453346, 4109765.328657193),
         (257247.95170560808, 4109763.3871935597),
         (257247.47480671466, 4109761.483306455),
         (257246.81359065024, 4109759.6353313527),
         (257245.974425287, 4109757.8610652634),
         (257244.96539224606, 4109756.1775953392),
         (257243.79620906725, 4109754.6011343165),
         (257242.47813562374, 4109753.146864376),
         (257241.0238656833, 4109751.8287909324),
         (257239.4474046604, 4109750.6596077536),
         (257237.76393473652, 4109749.650574713),
         (257235.98966864732, 4109748.8114093496),
         (257234.1416935451, 4109748.150193285),
         (257232.23780644033, 4109747.673294392),
         (257230.2963428066, 4109747.3853054666),
         (257228.336, 4109747.289),
         (257226.37565719342, 4109747.3853054666),
         (257224.4341935597, 4109747.673294392),
         (257222.53030645492, 4109748.150193285),
         (257220.6823313527, 4109748.8114093496),
         (257218.9080652635, 4109749.650574713),
         (257217.22459533962, 4109750.6596077536),
         (257215.64813431673, 4109751.8287909324),
         (257214.19386437628, 4109753.146864376),
         (257212.87579093277, 4109754.6011343165),
         (257211.70660775396, 4109756.1775953392),
         (257210.69757471303, 4109757.8610652634),
         (257209.85840934978, 4109759.6353313527),
         (257209.19719328536, 4109761.483306455),
         (257208.72029439194, 4109763.3871935597),
         (257208.43230546656, 4109765.328657193),
         (257208.336, 4109767.289),
         (257208.43230546656, 4109769.2493428066),
         (257208.72029439194, 4109771.19080644),
         (257209.19719328536, 4109773.094693545),
         (257209.85840934978, 4109774.942668647),
         (257210.69757471303, 4109776.7169347364),
         (257211.70660775396, 4109778.4004046605),
         (257212.87579093277, 4109779.976865683),
         (257214.19386437628, 4109781.4311356237),
         (257215.64813431673, 4109782.7492090673),
         (257217.22459533962, 4109783.918392246),
         (257218.9080652635, 4109784.9274252867),
         (257220.6823313527, 4109785.76659065),
         (257222.53030645492, 4109786.4278067145),
         (257224.4341935597, 4109786.904705608),
         (257226.37565719342, 4109787.192694533),
         (257228.336, 4109787.289),
         (257230.2963428066, 4109787.192694533),
         (257232.23780644033, 4109786.904705608),
         (257234.1416935451, 4109786.4278067145),
         (257235.98966864732, 4109785.76659065),
         (257237.76393473652, 4109784.9274252867),
         (257239.4474046604, 4109783.918392246),
         (257241.0238656833, 4109782.7492090673),
         (257242.47813562374, 4109781.4311356237),
         (257243.79620906725, 4109779.976865683),
         (257244.96539224606, 4109778.4004046605),
         (257245.974425287, 4109776.7169347364),
         (257246.81359065024, 4109774.942668647),
         (257247.47480671466, 4109773.094693545),
         (257247.95170560808, 4109771.19080644),
         (257248.23969453346, 4109769.2493428066),
         (257248.336, 4109767.289)]],
       'type': 'Polygon'},
      'id': '13',
      'properties': OrderedDict([('Plot_ID', 'SJER4'),
                   ('Point', 'center'),
                   ('easting', 257228.336),
                   ('northing', 4109767.289),
                   ('plot_type', 'trees'),
                   ('min', 2.1499998569488525),
                   ('max', 9.529999732971191),
                   ('mean', 5.0349365234375),
                   ('count', 395),
                   ('median', 5.21999979019165)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(254758.618, 4110249.265),
         (254758.52169453344, 4110247.3046571934),
         (254758.23370560806, 4110245.36319356),
         (254757.75680671463, 4110243.459306455),
         (254757.09559065022, 4110241.611331353),
         (254756.25642528696, 4110239.8370652637),
         (254755.24739224603, 4110238.1535953395),
         (254754.07820906723, 4110236.577134317),
         (254752.7601356237, 4110235.1228643763),
         (254751.30586568327, 4110233.8047909327),
         (254749.72940466038, 4110232.635607754),
         (254748.0459347365, 4110231.6265747133),
         (254746.2716686473, 4110230.78740935),
         (254744.42369354508, 4110230.1261932855),
         (254742.5198064403, 4110229.649294392),
         (254740.57834280658, 4110229.361305467),
         (254738.618, 4110229.265),
         (254736.6576571934, 4110229.361305467),
         (254734.71619355967, 4110229.649294392),
         (254732.8123064549, 4110230.1261932855),
         (254730.96433135268, 4110230.78740935),
         (254729.19006526348, 4110231.6265747133),
         (254727.5065953396, 4110232.635607754),
         (254725.9301343167, 4110233.8047909327),
         (254724.47586437626, 4110235.1228643763),
         (254723.15779093275, 4110236.577134317),
         (254721.98860775394, 4110238.1535953395),
         (254720.979574713, 4110239.8370652637),
         (254720.14040934975, 4110241.611331353),
         (254719.47919328534, 4110243.459306455),
         (254719.00229439192, 4110245.36319356),
         (254718.71430546654, 4110247.3046571934),
         (254718.618, 4110249.265),
         (254718.71430546654, 4110251.225342807),
         (254719.00229439192, 4110253.1668064403),
         (254719.47919328534, 4110255.070693545),
         (254720.14040934975, 4110256.9186686473),
         (254720.979574713, 4110258.6929347366),
         (254721.98860775394, 4110260.3764046608),
         (254723.15779093275, 4110261.9528656835),
         (254724.47586437626, 4110263.407135624),
         (254725.9301343167, 4110264.7252090676),
         (254727.5065953396, 4110265.8943922464),
         (254729.19006526348, 4110266.903425287),
         (254730.96433135268, 4110267.7425906505),
         (254732.8123064549, 4110268.403806715),
         (254734.71619355967, 4110268.880705608),
         (254736.6576571934, 4110269.1686945334),
         (254738.618, 4110269.265),
         (254740.57834280658, 4110269.1686945334),
         (254742.5198064403, 4110268.880705608),
         (254744.42369354508, 4110268.403806715),
         (254746.2716686473, 4110267.7425906505),
         (254748.0459347365, 4110266.903425287),
         (254749.72940466038, 4110265.8943922464),
         (254751.30586568327, 4110264.7252090676),
         (254752.7601356237, 4110263.407135624),
         (254754.07820906723, 4110261.9528656835),
         (254755.24739224603, 4110260.3764046608),
         (254756.25642528696, 4110258.6929347366),
         (254757.09559065022, 4110256.9186686473),
         (254757.75680671463, 4110255.070693545),
         (254758.23370560806, 4110253.1668064403),
         (254758.52169453344, 4110251.225342807),
         (254758.618, 4110249.265)]],
       'type': 'Polygon'},
      'id': '14',
      'properties': OrderedDict([('Plot_ID', 'SJER8'),
                   ('Point', 'center'),
                   ('easting', 254738.618),
                   ('northing', 4110249.265),
                   ('plot_type', 'trees'),
                   ('min', 2.2699999809265137),
                   ('max', 4.150000095367432),
                   ('mean', 3.0242857251848494),
                   ('count', 7),
                   ('median', 3.0)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(256205.584, 4110047.586),
         (256205.48769453345, 4110045.6256571934),
         (256205.19970560807, 4110043.68419356),
         (256204.72280671465, 4110041.780306455),
         (256204.06159065024, 4110039.932331353),
         (256203.22242528698, 4110038.1580652636),
         (256202.21339224605, 4110036.4745953395),
         (256201.04420906724, 4110034.898134317),
         (256199.72613562373, 4110033.4438643763),
         (256198.2718656833, 4110032.1257909327),
         (256196.6954046604, 4110030.956607754),
         (256195.0119347365, 4110029.9475747133),
         (256193.2376686473, 4110029.10840935),
         (256191.3896935451, 4110028.4471932855),
         (256189.48580644032, 4110027.970294392),
         (256187.5443428066, 4110027.682305467),
         (256185.584, 4110027.586),
         (256183.6236571934, 4110027.682305467),
         (256181.68219355968, 4110027.970294392),
         (256179.77830645491, 4110028.4471932855),
         (256177.9303313527, 4110029.10840935),
         (256176.1560652635, 4110029.9475747133),
         (256174.4725953396, 4110030.956607754),
         (256172.89613431672, 4110032.1257909327),
         (256171.44186437628, 4110033.4438643763),
         (256170.12379093276, 4110034.898134317),
         (256168.95460775396, 4110036.4745953395),
         (256167.94557471303, 4110038.1580652636),
         (256167.10640934977, 4110039.932331353),
         (256166.44519328536, 4110041.780306455),
         (256165.96829439193, 4110043.68419356),
         (256165.68030546655, 4110045.6256571934),
         (256165.584, 4110047.586),
         (256165.68030546655, 4110049.546342807),
         (256165.96829439193, 4110051.4878064403),
         (256166.44519328536, 4110053.391693545),
         (256167.10640934977, 4110055.2396686473),
         (256167.94557471303, 4110057.0139347366),
         (256168.95460775396, 4110058.6974046608),
         (256170.12379093276, 4110060.2738656835),
         (256171.44186437628, 4110061.728135624),
         (256172.89613431672, 4110063.0462090676),
         (256174.4725953396, 4110064.2153922464),
         (256176.1560652635, 4110065.224425287),
         (256177.9303313527, 4110066.0635906504),
         (256179.77830645491, 4110066.724806715),
         (256181.68219355968, 4110067.201705608),
         (256183.6236571934, 4110067.4896945334),
         (256185.584, 4110067.586),
         (256187.5443428066, 4110067.4896945334),
         (256189.48580644032, 4110067.201705608),
         (256191.3896935451, 4110066.724806715),
         (256193.2376686473, 4110066.0635906504),
         (256195.0119347365, 4110065.224425287),
         (256196.6954046604, 4110064.2153922464),
         (256198.2718656833, 4110063.0462090676),
         (256199.72613562373, 4110061.728135624),
         (256201.04420906724, 4110060.2738656835),
         (256202.21339224605, 4110058.6974046608),
         (256203.22242528698, 4110057.0139347366),
         (256204.06159065024, 4110055.2396686473),
         (256204.72280671465, 4110053.391693545),
         (256205.19970560807, 4110051.4878064403),
         (256205.48769453345, 4110049.546342807),
         (256205.584, 4110047.586)]],
       'type': 'Polygon'},
      'id': '15',
      'properties': OrderedDict([('Plot_ID', 'SJER824'),
                   ('Point', 'center'),
                   ('easting', 256185.584),
                   ('northing', 4110047.586),
                   ('plot_type', 'soil'),
                   ('min', 2.0899999141693115),
                   ('max', 25.65999984741211),
                   ('mean', 7.720837977544176),
                   ('count', 382),
                   ('median', 6.264999866485596)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(257480.486, 4109616.679),
         (257480.38969453346, 4109614.7186571932),
         (257480.10170560807, 4109612.77719356),
         (257479.62480671465, 4109610.873306455),
         (257478.96359065024, 4109609.025331353),
         (257478.12442528698, 4109607.2510652635),
         (257477.11539224605, 4109605.5675953394),
         (257475.94620906725, 4109603.9911343167),
         (257474.62813562373, 4109602.536864376),
         (257473.1738656833, 4109601.2187909326),
         (257471.5974046604, 4109600.0496077538),
         (257469.9139347365, 4109599.040574713),
         (257468.13966864732, 4109598.2014093497),
         (257466.2916935451, 4109597.5401932853),
         (257464.38780644033, 4109597.063294392),
         (257462.4463428066, 4109596.7753054667),
         (257460.486, 4109596.679),
         (257458.52565719342, 4109596.7753054667),
         (257456.58419355968, 4109597.063294392),
         (257454.68030645492, 4109597.5401932853),
         (257452.8323313527, 4109598.2014093497),
         (257451.0580652635, 4109599.040574713),
         (257449.3745953396, 4109600.0496077538),
         (257447.79813431672, 4109601.2187909326),
         (257446.34386437628, 4109602.536864376),
         (257445.02579093276, 4109603.9911343167),
         (257443.85660775396, 4109605.5675953394),
         (257442.84757471303, 4109607.2510652635),
         (257442.00840934977, 4109609.025331353),
         (257441.34719328536, 4109610.873306455),
         (257440.87029439193, 4109612.77719356),
         (257440.58230546655, 4109614.7186571932),
         (257440.486, 4109616.679),
         (257440.58230546655, 4109618.639342807),
         (257440.87029439193, 4109620.58080644),
         (257441.34719328536, 4109622.484693545),
         (257442.00840934977, 4109624.332668647),
         (257442.84757471303, 4109626.1069347365),
         (257443.85660775396, 4109627.7904046606),
         (257445.02579093276, 4109629.3668656833),
         (257446.34386437628, 4109630.821135624),
         (257447.79813431672, 4109632.1392090674),
         (257449.3745953396, 4109633.3083922463),
         (257451.0580652635, 4109634.317425287),
         (257452.8323313527, 4109635.1565906503),
         (257454.68030645492, 4109635.8178067147),
         (257456.58419355968, 4109636.294705608),
         (257458.52565719342, 4109636.5826945333),
         (257460.486, 4109636.679),
         (257462.4463428066, 4109636.5826945333),
         (257464.38780644033, 4109636.294705608),
         (257466.2916935451, 4109635.8178067147),
         (257468.13966864732, 4109635.1565906503),
         (257469.9139347365, 4109634.317425287),
         (257471.5974046604, 4109633.3083922463),
         (257473.1738656833, 4109632.1392090674),
         (257474.62813562373, 4109630.821135624),
         (257475.94620906725, 4109629.3668656833),
         (257477.11539224605, 4109627.7904046606),
         (257478.12442528698, 4109626.1069347365),
         (257478.96359065024, 4109624.332668647),
         (257479.62480671465, 4109622.484693545),
         (257480.10170560807, 4109620.58080644),
         (257480.38969453346, 4109618.639342807),
         (257480.486, 4109616.679)]],
       'type': 'Polygon'},
      'id': '16',
      'properties': OrderedDict([('Plot_ID', 'SJER916'),
                   ('Point', 'center'),
                   ('easting', 257460.486),
                   ('northing', 4109616.679),
                   ('plot_type', 'soil'),
                   ('min', 2.1499998569488525),
                   ('max', 18.729999542236328),
                   ('mean', 11.170794862689394),
                   ('count', 264),
                   ('median', 10.979999542236328)]),
      'type': 'Feature'},
     {'geometry': {'coordinates': [[(255891.194, 4110759.039),
         (255891.09769453344, 4110757.078657193),
         (255890.80970560806, 4110755.1371935597),
         (255890.33280671464, 4110753.233306455),
         (255889.67159065022, 4110751.3853313527),
         (255888.83242528696, 4110749.6110652634),
         (255887.82339224603, 4110747.9275953392),
         (255886.65420906723, 4110746.3511343165),
         (255885.33613562371, 4110744.896864376),
         (255883.88186568327, 4110743.5787909324),
         (255882.30540466038, 4110742.4096077536),
         (255880.6219347365, 4110741.400574713),
         (255878.8476686473, 4110740.5614093496),
         (255876.99969354508, 4110739.900193285),
         (255875.0958064403, 4110739.423294392),
         (255873.15434280658, 4110739.1353054666),
         (255871.194, 4110739.039),
         (255869.2336571934, 4110739.1353054666),
         (255867.29219355967, 4110739.423294392),
         (255865.3883064549, 4110739.900193285),
         (255863.54033135268, 4110740.5614093496),
         (255861.76606526348, 4110741.400574713),
         (255860.0825953396, 4110742.4096077536),
         (255858.5061343167, 4110743.5787909324),
         (255857.05186437626, 4110744.896864376),
         (255855.73379093275, 4110746.3511343165),
         (255854.56460775394, 4110747.9275953392),
         (255853.555574713, 4110749.6110652634),
         (255852.71640934976, 4110751.3853313527),
         (255852.05519328534, 4110753.233306455),
         (255851.57829439192, 4110755.1371935597),
         (255851.29030546654, 4110757.078657193),
         (255851.194, 4110759.039),
         (255851.29030546654, 4110760.9993428066),
         (255851.57829439192, 4110762.94080644),
         (255852.05519328534, 4110764.844693545),
         (255852.71640934976, 4110766.692668647),
         (255853.555574713, 4110768.4669347364),
         (255854.56460775394, 4110770.1504046605),
         (255855.73379093275, 4110771.726865683),
         (255857.05186437626, 4110773.1811356237),
         (255858.5061343167, 4110774.4992090673),
         (255860.0825953396, 4110775.668392246),
         (255861.76606526348, 4110776.6774252867),
         (255863.54033135268, 4110777.51659065),
         (255865.3883064549, 4110778.1778067145),
         (255867.29219355967, 4110778.654705608),
         (255869.2336571934, 4110778.942694533),
         (255871.194, 4110779.039),
         (255873.15434280658, 4110778.942694533),
         (255875.0958064403, 4110778.654705608),
         (255876.99969354508, 4110778.1778067145),
         (255878.8476686473, 4110777.51659065),
         (255880.6219347365, 4110776.6774252867),
         (255882.30540466038, 4110775.668392246),
         (255883.88186568327, 4110774.4992090673),
         (255885.33613562371, 4110773.1811356237),
         (255886.65420906723, 4110771.726865683),
         (255887.82339224603, 4110770.1504046605),
         (255888.83242528696, 4110768.4669347364),
         (255889.67159065022, 4110766.692668647),
         (255890.33280671464, 4110764.844693545),
         (255890.80970560806, 4110762.94080644),
         (255891.09769453344, 4110760.9993428066),
         (255891.194, 4110759.039)]],
       'type': 'Polygon'},
      'id': '17',
      'properties': OrderedDict([('Plot_ID', 'SJER952'),
                   ('Point', 'center'),
                   ('easting', 255871.194),
                   ('northing', 4110759.039),
                   ('plot_type', 'grass'),
                   ('min', 2.8399999141693115),
                   ('max', 6.37999963760376),
                   ('mean', 4.149285452706473),
                   ('count', 42),
                   ('median', 4.079999923706055)]),
      'type': 'Feature'}]




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




```python
# view docstring for object
#data?
#SJER_chm.
```

# not sure what the .transform component does
#stats = rs.zonal_stats(SJER_plots,
#                       lidar_tif_path,
#                       geojson_out=True,
#                       tranform=SJER_chm.transform)
#http://pythonhosted.org/rasterstats/
# Warning : https://github.com/mapbox/rasterio/issues/86
FutureWarning: GDAL-style transforms are deprecated and will not be supported in Rasterio 1.0.
  self.affine = guard_transform(self.src.transform)

## here we are reading things in using the path vs typing in the path directlry. i'm open to either but we should be consistent throughout.


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



Note that now we have the maximum tree height value for each field plot where
we measured trees. Next we can join the
measured tree height data that we summarized above with the maximum tree
height data that we extracted from our lidar canopy height model raster.

## Is there a good way to enforce line widths -- it may be nice if we can work in py scripts and go back and forth to notebooks...

it would be good to be abel to rename columns so the lidar columns say lidar vs measured - consider doing that above



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





## Study site location



To answer the question above, let's look at some data from a study site location

in California - the San Joaquin Experimental range field site. You can see the field

site location on the map below.





```python
# this chunk of code should write an automatic google map using the study site location
# Pull the california lat / long pair, then fetch a box around it
cali = geocoder.google('california')
zoom = 6
# _ = ctx.howmany(cali.west, cali.south, cali.east, cali.north, zoom, ll=True)  # Tel tell how big the download is
_ = ctx.bounds2raster(cali.west, cali.south, cali.east, cali.north, 6, './cali.tif', ll=True, url=ctx.sources.ST_TERRAIN)
calir = rio.open('./cali.tif')

# Fetch the state boundaries
state_boundary_us = gpd.read_file(
    "data/week5/usa-boundary-layers/US-State-Boundaries-Census-2014.shp")

# Generate our LatLng for the station we care about
SJER_chm_point = Point(SJER_chm.bounds[0], SJER_chm.bounds[1])
SJER_chm_df = pd.DataFrame([SJER_chm_point], columns=['geometry'])
SJER_chm_gpd = gpd.GeoDataFrame(SJER_chm_df, crs=SJER_chm.crs)

# Project into the same CRS
state_boundary_us_chm = state_boundary_us.to_crs(calir.crs)
SJER_chm_gpd = SJER_chm_gpd.to_crs(calir.crs)


# Make the figure
fig, ax = plt.subplots(figsize=(10, 10))

# Load the tile raster (note the re-arrangement of the bounds)
bb = calir.bounds
riop.show(calir, ax=ax)
# ax.imshow(img, extent=(bb.left, bb.right, bb.bottom, bb.top))
state_boundary_us_chm.plot(ax=ax, alpha=.3, color='k')
SJER_chm_gpd.plot(ax=ax, markersize=50, color='r')


```




    <matplotlib.axes._subplots.AxesSubplot at 0x139ef90f0>




![png](../../../../../images/course-materials/earth-analytics//week-5/in-class/2016-12-06-spatial05-understand-uncertainty_39_1.png)




## Study area plots



At this study site, we have both lidar data - specifically a canopy height model

that was processed by NEON (National Ecological Observatory Network). We also

have some "ground truth" data. That is we have measured tree height values collected at a set

of field site plots by technicians at NEON. We will call these measured values

*in situ* measurements.



A map of our study plots is below overlaid on top of the canopy height mode.




## The chunk below uses .read() rather than rio.open -- we really need to be consistent in how we open and work with data...


```python
# this is just a plot of field plot locations overlayed on top of the chm
img = SJER_chm.read().squeeze()
img[img == 0] = np.nan

fig, ax = plt.subplots(figsize=(10, 10))
# riop.show(SJER_chm, cmap='Greys', ax=ax)
ax.imshow(img, cmap='Greys', extent=[SJER_chm.bounds[ii] for ii in [0, 2, 1, 3]])
# why are the markers so tiny tiny?!
SJER_plots.plot(ax=ax, markersize=500, color='r')




```




    <matplotlib.axes._subplots.AxesSubplot at 0x129109cc0>




![png](../../../../../images/course-materials/earth-analytics//week-5/in-class/2016-12-06-spatial05-understand-uncertainty_42_1.png)




### Compare lidar derived height to in situ measurements



We can compare maximum tree height values at each plot to the maximum pixel value

in our CHM for each plot. To do this, we define the geographic boundary of our plot

using a polygon - in the case below we use a circle as the boundary. We then extract

the raster cell values for each circle and calculate the max value for all of the

pixels that fall within the plot area.



Then, we calculate the max height of our measured plot tree height data.



Finally we compare the two using a scatter plot to see how closely the data relate.

Do they follow a 1:1 line? Do the data diverge from a 1:1 relationship?



<figure>

    <img src="{{ site.url }}/images/course-materials/earth-analytics/week-5/buffer-circular.png" alt="buffer circular">

    <figcaption>The extract function in R allows you to specify a circular buffer

    radius around an x,y point location. Values for all pixels in the specified

    raster that fall within the circular buffer are extracted. In this case, we

    will tell R to extract the maximum value of all pixels using the fun=max

    command. Source: Colin Williams, NEON

    </figcaption>

</figure>





```python
SJER_final_height.columns
```




    Index(['plotid', 'stemheight', 'Plot_ID', 'Point', 'count', 'easting',
           'geometry', 'max', 'mean', 'median', 'min', 'northing', 'plot_type'],
          dtype='object')




```python

```


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




    <matplotlib.text.Text at 0x14b140198>




![png](../../../../../images/course-materials/earth-analytics//week-5/in-class/2016-12-06-spatial05-understand-uncertainty_46_1.png)



```python
# ```{r plot-data, fig.cap="final plot", echo=F, warning=F, message=F}



# # create plot

# p <-ggplot(SJER_height@data, aes(x = insitu_max, y=SJER_lidarCHM)) +

#   geom_point() +

#   theme_bw() +

#   xlab("Mean measured height (m)") +

#   ylab("Mean LiDAR pixel (m)") +

#   ggtitle("Lidar Derived Max Tree Height \nvs. InSitu Measured Max Tree Height") +

#   geom_abline(intercept = 0, slope=1) +

#   geom_smooth(method=lm)



# p



# ```

## This plot should show the same with a regression line

```



### How different are the data?





```python

# Calculate difference
# also need to add the plot id to each xaxis label
SJER_final_height["lidar_measured"] = SJER_final_height["max"] - SJER_final_height["stemheight"]
SJER_final_height["lidar_measured"].plot(kind="bar")
```




    <matplotlib.axes._subplots.AxesSubplot at 0x128cea6a0>




![png](../../../../../images/course-materials/earth-analytics//week-5/in-class/2016-12-06-spatial05-understand-uncertainty_49_1.png)


## View interactive scatterplot

<a href="https://plot.ly/~leahawasser/170/" target="_blank">View scatterplot plotly</a>



## View interactive difference barplot

<a href="https://plot.ly/~leahawasser/158/chm-minus-insitu-differences/" target="_blank">View scatterplot differences</a>





```python
# python has a plotly api too!

#```{r ggplotly, echo=F, eval=F}

#library(plotly)

#Sys.setenv("plotly_username"="leahawasser")

#Sys.setenv("plotly_api_key"="#")
#plotly_POST(p)

```

```
