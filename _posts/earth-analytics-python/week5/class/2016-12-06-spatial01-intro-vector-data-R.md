---
layout: single
title: "GIS in Python: Introduction to vector format spatial data - points, lines and polygons"
excerpt: "This lesson introduces what vector data are and how to open vector data stored in
shapefile format in Python. "
authors: ['Chris Holdgraf', 'Leah Wasser']
modified: '2017-01-01'
category: [course-materials]
class-lesson: ['class-intro-spatial-python']
permalink: /course-materials/earth-analytics-python/week-5/intro-vector-data-python/
nav-title: 'Vector data in Python'
module-title: 'Spatial data in Python and remote sensing uncertainty'
module-description: 'This tutorial covers the basic principles of LiDAR remote sensing and
the three commonly used data products: the digital elevation model, digital surface model and the canopy height model. Finally it walks through opening lidar derived raster data in Python'
module-nav-title: 'Spatial Data in Python'
module-type: 'class'
week: 5
sidebar:
  nav:
author_profile: false
comments: true
order: 1
---



{% include toc title="In This Lesson" icon="file-text" %}



<div class='notice--success' markdown="1">



## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives



After completing this tutorial, you will be able to:



* Be able to describe the characteristics of 3 key vector data structures: points, lines and polygons.

* Be able to open a shapefile in R using `readOGR()`.

* Be able to view the metadata of a vector spatial layer in R including CRS

* Be able to access the tabular (`data.frame`) attributes of a vector spatial layer in `R`.



## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need



You will need a computer with internet access to complete this lesson and the data for week 5 of the course.



[<i class="fa fa-download" aria-hidden="true"></i> Download Week 5 Data (~500 MB)](https://ndownloader.figshare.com/files/7525363){:data-proofer-ignore='' .btn }



</div>



## About Vector Data

Vector data are composed of discrete geometric locations (x,y values) known as **vertices** that define the "shape" of the spatial object. The organization of the vertices, determines the type of vector that we are working
with: point, line or polygon.



<figure>
    <a href="{{ site.baseurl }}/images/course-materials/earth-analytics/week-5/pnt_line_poly.png">
    <img src="{{ site.baseurl }}/images/course-materials/earth-analytics/week-5/pnt_line_poly.png" alt="points lines and polygons graphic."></a>
    <figcaption> There are 3 types of vector objects: points, lines or polygons. Each object type has a different structure. Image Source: Colin Williams (NEON)
    </figcaption>
</figure>



* **Points:** Each individual point is defined by a single x, y coordinate. There can be many points in a vector point file. Examples of point data include: sampling locations, the location of individual trees or the location of plots.

* **Lines:** Lines are composed of many (at least 2) vertices, or points, that are connected. For instance, a road or a stream may be represented by a line. This line is composed of a series of segments, each "bend" in the road or stream represents a vertex that has defined `x, y` location.

* **Polygons:** A polygon consists of 3 or more vertices that are connected and "closed". Thus the outlines of plot boundaries, lakes, oceans, and states or countries are often represented by polygons. Occasionally, a polygon can have a hole in the middle of it (like a doughnut), this is something to be aware of but not an issue we will deal with in this tutorial.


<i class="fa fa-star"></i> **Data Tip:** Sometimes, boundary layers such as states and countries, are stored as lines rather than polygons. However, these boundaries, when represented as a line, will not create a closed object with a defined "area" that can be "filled".
{: .notice}



## Shapefiles: Points, Lines, and Polygons

Geospatial data in vector format are often stored in a `shapefile` format. Because the structure of points, lines, and polygons are different, each individual shapefile can only contain one vector type (all points, all lines
or all polygons). You will not find a mixture of point, line and polygon objects in a single shapefile.

Objects stored in a shapefile often have a set of associated `attributes` that describe the data. For example, a line shapefile that contains the locations of streams, might contain the associated stream name, stream "order" and other
information about each stream line object.



* More about shapefiles can found on <a href="https://en.wikipedia.org/wiki/Shapefile" target="_blank">Wikipedia</a>.



## Import Shapefiles


We will use the `geopandas` library to work with vector data in `R`. We will also use `matplotlib.pyplot` to plot our data and `folium`.




```python
## Note not sure what folium does...  leaflet interactive mapping
## had to install it via pip rather than conda...
## will need some discussion on using pip vs conda...
```


```python
import geopandas as gpd
import matplotlib.pyplot as plt
# import folium
import os.path as op
# is there any reason to not just import os
import os
# what does this do?
plt.ion()
```


```python
# os.getcwd()
# be sure to set your working directory
os.chdir("/Users/lewa8222/Documents/earth-analytics")

#print os.getcwd();
```


The shapefiles that we will import are:

* A polygon shapefile representing our field site boundary,
* A line shapefile representing roads, and
* A point shapefile representing the location of field sites at the <a href="http://www.neonscience.org/science-design/field-sites/harvard-forest" target="_blank"> San Joachin field site</a>.

The first shapefile that we will open contains the point locations of plots where trees have been measured. To import shapefiles we use the `geopandas` function `read_file()`. Notice that we call the `read_file()` function using `gpd.read_file()` to tell python to look for the function within the `geopandas` library.



```python
# path_data = '../../../../../../../data/week05/'

sjer_plot_locations = gpd.read_file(filename="data/week5/california/SJER/vector_data/SJER_plot_centroids.shp")
# view attribute table of data
sjer_plot_locations
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
      <td>POINT (255852.376 4111567.818)</td>
      <td>4111567.818</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SJER112</td>
      <td>center</td>
      <td>257406.967</td>
      <td>POINT (257406.967 4111298.971)</td>
      <td>4111298.971</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SJER116</td>
      <td>center</td>
      <td>256838.760</td>
      <td>POINT (256838.76 4110819.876)</td>
      <td>4110819.876</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SJER117</td>
      <td>center</td>
      <td>256176.947</td>
      <td>POINT (256176.947 4108752.026)</td>
      <td>4108752.026</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SJER120</td>
      <td>center</td>
      <td>255968.372</td>
      <td>POINT (255968.372 4110476.079)</td>
      <td>4110476.079</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>5</th>
      <td>SJER128</td>
      <td>center</td>
      <td>257078.867</td>
      <td>POINT (257078.867 4111388.57)</td>
      <td>4111388.570</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>6</th>
      <td>SJER192</td>
      <td>center</td>
      <td>256683.434</td>
      <td>POINT (256683.434 4111071.087)</td>
      <td>4111071.087</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>7</th>
      <td>SJER272</td>
      <td>center</td>
      <td>256717.467</td>
      <td>POINT (256717.467 4112167.778)</td>
      <td>4112167.778</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>8</th>
      <td>SJER2796</td>
      <td>center</td>
      <td>256034.390</td>
      <td>POINT (256034.39 4111533.879)</td>
      <td>4111533.879</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>9</th>
      <td>SJER3239</td>
      <td>center</td>
      <td>258497.102</td>
      <td>POINT (258497.102 4109856.983)</td>
      <td>4109856.983</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>10</th>
      <td>SJER36</td>
      <td>center</td>
      <td>258277.829</td>
      <td>POINT (258277.829 4110161.674)</td>
      <td>4110161.674</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>11</th>
      <td>SJER361</td>
      <td>center</td>
      <td>256961.794</td>
      <td>POINT (256961.794 4107527.074)</td>
      <td>4107527.074</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>12</th>
      <td>SJER37</td>
      <td>center</td>
      <td>256148.197</td>
      <td>POINT (256148.197 4107578.841)</td>
      <td>4107578.841</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>13</th>
      <td>SJER4</td>
      <td>center</td>
      <td>257228.336</td>
      <td>POINT (257228.336 4109767.289)</td>
      <td>4109767.289</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>14</th>
      <td>SJER8</td>
      <td>center</td>
      <td>254738.618</td>
      <td>POINT (254738.618 4110249.265)</td>
      <td>4110249.265</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>15</th>
      <td>SJER824</td>
      <td>center</td>
      <td>256185.584</td>
      <td>POINT (256185.584 4110047.586)</td>
      <td>4110047.586</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>16</th>
      <td>SJER916</td>
      <td>center</td>
      <td>257460.486</td>
      <td>POINT (257460.486 4109616.679)</td>
      <td>4109616.679</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>17</th>
      <td>SJER952</td>
      <td>center</td>
      <td>255871.194</td>
      <td>POINT (255871.194 4110759.039)</td>
      <td>4110759.039</td>
      <td>grass</td>
    </tr>
  </tbody>
</table>
</div>



We can view the type of object that we are working with using the `type()` function. Here we can see that our `sjer_plot_locations` object is a `geopandas geodataframe`.


```python
# what type of object did we import
type(sjer_plot_locations)
```




    geopandas.geodataframe.GeoDataFrame




<i class="fa fa-star"></i> **Data Tip:** The acronym, OGR, refers to the OpenGIS Simple Features Reference Implementation. <a href="https://trac.osgeo.org/gdal/wiki/FAQGeneral" target="_blank"> Learn more about OGR.</a>
{: .notice}


## Shapefile Metadata & Attributes

When we import the `SJER_plot_centroids` shapefile layer into `Python` the `gpd.read_file()` function automatically stores information about the data. We are particularly interested in the geospatial **metadata**, describing the format, `CRS`, `extent`, and other components of the vector data, and the **attributes** which describe properties associated with each individual vector object.


## Spatial Metadata

Key metadata for all shapefiles include:

1. **Object Type:** the class of the imported object.
2. **Coordinate Reference System (CRS):** the projection of the data.
3. **Extent:** the spatial extent (geographic area that the shapefile covers) of the shapefile. Note that the spatial extent for a shapefile represents the extent for ALL spatial objects in the shapefile.

We can view shapefile metadata using the `class`, `crs` and `extent` methods:



```python
# don't understand what this is doing
# getattr(sjer_plot_locations.head(), attr)

# view the spatial extent
sjer_plot_locations.total_bounds
```




    (254738.61799999999, 4107527.074, 258497.10200000001, 4112167.7779999999)




```python
# Get summary of several key spatial attributes
#for attr in ['crs', 'total_bounds', 'length']:
#    print(attr, '\n', getattr(sjer_plot_locations.head(), attr), '\n---\n')

# view the crs or coordinate reference system of the data
sjer_plot_locations.crs

```




    {'init': 'epsg:32611'}



The CRS for our data is epsg code: 32611. We will discuss CRS' in a later lesson but for now a quick google search reveals that this CRS is: UTM zone 11 North - WGS84

http://spatialreference.org/ref/epsg/wgs-84-utm-zone-11n/



```python
# view the type of geometry contained in the spatial object
sjer_plot_locations.geom_type

```




    0     Point
    1     Point
    2     Point
    3     Point
    4     Point
    5     Point
    6     Point
    7     Point
    8     Point
    9     Point
    10    Point
    11    Point
    12    Point
    13    Point
    14    Point
    15    Point
    16    Point
    17    Point
    dtype: object



## How do i count the number of objects in the geopandas dataframe?


```python
# view the type of geometry contained in the spatial object
length(sjer_plot_locations.geom_type)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-38-786b972b090d> in <module>()
          1 # view the type of geometry contained in the spatial object
    ----> 2 length(sjer_plot_locations.geom_type)


    NameError: name 'length' is not defined


The CRS **UTM zone 18N**. The CRS is critical to interpreting the object `extent` values as it specifies units.


<figure>
    <a href="{{ site.baseurl }}/images/course-materials/earth-analytics/week-5/spatial_extent.png">
    <img src="{{ site.baseurl }}/images/course-materials/earth-analytics/week-5/spatial_extent.png" alt="the spatial extent represents the spatial area that a particular dataset covers."></a>
    <figcaption>The spatial extent of a shapefile or R spatial object represents
    the geographic "edge" or location that is the furthest north, south east and
    west. Thus is represents the overall geographic coverage of the spatial object.
    Image Source: National Ecological Observatory Network (NEON)
    </figcaption>
</figure>



## Spatial Data Attributes

Each object in a shapefile has one or more attributes associated with it.
Shapefile attributes are similar to fields or columns in a spreadsheet. Each row
in the spreadsheet has a set of columns associated with it that describe the row
element. In the case of a shapefile, each row represents a spatial object - for
example, a road, represented as a line in a line shapefile, will have one "row"
of attributes associated with it. These attributes can include different types
of information that describe objects stored within a shapefile. Thus, our road,
may have a name, length, number of lanes, speed limit, type of road and other
attributes stored with it.



<figure>

    <a href="{{ site.baseurl }}/images/course-materials/earth-analytics/week-5/attribute_table.png">
    <img src="{{ site.baseurl }}/images/course-materials/earth-analytics/week-5/attribute_table.png" alt="A shapefile has an associated attribute table. Each spatial feature in an R spatial object has the same set of
    associated attributes that describe or characterize the feature.
    Attribute data are stored in a separate *.dbf file. "></a>
    <figcaption>Each spatial feature in an R spatial object has the same set of
    associated attributes that describe or characterize the feature.
    Attribute data are stored in a separate *.dbf file. Attribute data can be
    compared to a spreadsheet. Each row in a spreadsheet represents one feature
    in the spatial object.
    Image Source: National Ecological Observatory Network (NEON)
    </figcaption>
</figure>


We view the attribute table associated with our geopandas `GeoDataFrame` by simply typing the object name into the console
(e.g., `sjer_plot_locations`).



```python
# view attribute table associated with the data
sjer_plot_locations
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
      <td>POINT (255852.376 4111567.818)</td>
      <td>4111567.818</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>1</th>
      <td>SJER112</td>
      <td>center</td>
      <td>257406.967</td>
      <td>POINT (257406.967 4111298.971)</td>
      <td>4111298.971</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>2</th>
      <td>SJER116</td>
      <td>center</td>
      <td>256838.760</td>
      <td>POINT (256838.76 4110819.876)</td>
      <td>4110819.876</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>3</th>
      <td>SJER117</td>
      <td>center</td>
      <td>256176.947</td>
      <td>POINT (256176.947 4108752.026)</td>
      <td>4108752.026</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SJER120</td>
      <td>center</td>
      <td>255968.372</td>
      <td>POINT (255968.372 4110476.079)</td>
      <td>4110476.079</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>5</th>
      <td>SJER128</td>
      <td>center</td>
      <td>257078.867</td>
      <td>POINT (257078.867 4111388.57)</td>
      <td>4111388.570</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>6</th>
      <td>SJER192</td>
      <td>center</td>
      <td>256683.434</td>
      <td>POINT (256683.434 4111071.087)</td>
      <td>4111071.087</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>7</th>
      <td>SJER272</td>
      <td>center</td>
      <td>256717.467</td>
      <td>POINT (256717.467 4112167.778)</td>
      <td>4112167.778</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>8</th>
      <td>SJER2796</td>
      <td>center</td>
      <td>256034.390</td>
      <td>POINT (256034.39 4111533.879)</td>
      <td>4111533.879</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>9</th>
      <td>SJER3239</td>
      <td>center</td>
      <td>258497.102</td>
      <td>POINT (258497.102 4109856.983)</td>
      <td>4109856.983</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>10</th>
      <td>SJER36</td>
      <td>center</td>
      <td>258277.829</td>
      <td>POINT (258277.829 4110161.674)</td>
      <td>4110161.674</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>11</th>
      <td>SJER361</td>
      <td>center</td>
      <td>256961.794</td>
      <td>POINT (256961.794 4107527.074)</td>
      <td>4107527.074</td>
      <td>grass</td>
    </tr>
    <tr>
      <th>12</th>
      <td>SJER37</td>
      <td>center</td>
      <td>256148.197</td>
      <td>POINT (256148.197 4107578.841)</td>
      <td>4107578.841</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>13</th>
      <td>SJER4</td>
      <td>center</td>
      <td>257228.336</td>
      <td>POINT (257228.336 4109767.289)</td>
      <td>4109767.289</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>14</th>
      <td>SJER8</td>
      <td>center</td>
      <td>254738.618</td>
      <td>POINT (254738.618 4110249.265)</td>
      <td>4110249.265</td>
      <td>trees</td>
    </tr>
    <tr>
      <th>15</th>
      <td>SJER824</td>
      <td>center</td>
      <td>256185.584</td>
      <td>POINT (256185.584 4110047.586)</td>
      <td>4110047.586</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>16</th>
      <td>SJER916</td>
      <td>center</td>
      <td>257460.486</td>
      <td>POINT (257460.486 4109616.679)</td>
      <td>4109616.679</td>
      <td>soil</td>
    </tr>
    <tr>
      <th>17</th>
      <td>SJER952</td>
      <td>center</td>
      <td>255871.194</td>
      <td>POINT (255871.194 4110759.039)</td>
      <td>4110759.039</td>
      <td>grass</td>
    </tr>
  </tbody>
</table>
</div>



In this case, we have several attributes associated with our points including:

* Plot_ID, Point, easting, geometry, northing, plot_type


## Metadata & Attribute Summary

We can view a metadata & attribute summary of each shapefile using a for loop to access the attributes that we are interested in. Below we include the **coordinate reference system** (`crs`) and the spatial **extent**.




```python
for attr in ['crs', 'total_bounds']:
    print(attr, '\n', getattr(sjer_plot_locations.head(), attr))

```

    crs
     {'init': 'epsg:32611'}
    total_bounds
     (255852.37599999999, 4108752.0260000001, 257406.967, 4111567.818)


# Plot a Shapefile

Next, let's visualize the data in our `R` `spatialpointsdataframe` object using the `.plot()` method.


```python
# quickly plot the data
sjer_plot_locations.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x10ec75828>




![png](output_21_1.png)


We can adjust the symbol size of our plot using the `markersize` argument.
We can add a title using `ax.set_title()`.

We can create a larger map by adjusting the `figsize` argument. Below we set it to 10 x 10.


```python
# Plot the data adjusting marker size and colors
# # 'col' sets point symbol color

ax = sjer_plot_locations.plot(figsize=(10, 10), markersize=15)
# add a title to the plot
ax.set_title('SJER Plot Locations\nMadera County, CA')
```




    <matplotlib.text.Text at 0x11281e438>




![png](output_23_1.png)


### Change plot colors & symbols

We can use the cmap argument to adjust the colors of our plot. Below we used a colormap that is a part of the matplotlib colormap library.

http://matplotlib.org/users/colormaps.html

Finally we use the marker= argument to specify the marker style.


```python
ax = sjer_plot_locations.plot(figsize=(10, 10), marker='*', markersize=15, cmap='OrRd')
# add a title to the plot
ax.set_title('SJER Plot Locations\nMadera County, CA')
```




    <matplotlib.text.Text at 0x112b9f518>




![png](output_25_1.png)



<div class="notice--warning" markdown="1">


## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Test your knowledge: Import Line & Polygon Shapefiles

Using the steps above, import the `data/week5/california/madera-county-roads/tl_2013_06039_roads` and `data/week5/california/SJER/vector_data/SJER_crop.shp` shapefiles into your `Jupyter notebook`. Call the roads object `sjer_roads` and the crop layer `sjer_crop_extent`.

Answer the following questions:

1. What type of spatial object is created when you import each layer?
2. What is the geom_type of each layer (points, lines or polygons)?
2. What is the `CRS` and spatial `extent` for each layer?
4. How many spatial objects are in each file?
</div>



```python
## NOTE that this is the answer to the challenge and thus needs to be hidden.

# ```{r import-point-line, echo=FALSE, results="hide" }
# import line shapefile
# sjer_roads <- readOGR("data/week5/california/madera-county-roads",
#                       layer = "tl_2013_06039_roads")


# sjer_crop_extent <- readOGR("data/week5/california/SJER/vector_data/",
#                             "SJER_crop")

# 1
# class(sjer_roads)
# class(sjer_plot_locations)

# # 2
# crs(sjer_roads)
# extent(sjer_roads)
# crs(sjer_plot_locations)
# extent(sjer_plot_locations)

# 3
# #sjer_roads contains only lines and sjer_plot_locations contains only 1 point

# 4 -> numerous ways to find this; sjer_roads=13,
# length(sjer_roads)  #easiest, but not previously taught
# sjer_roads  #look at 'features'
# attributes(sjer_roads)  #found in the $data section as above


# sjer_roads = gpd.read_file(op.join(path_data, 'california', 'madera-county-roads', 'tl_2013_06039_roads.shp'))
sjer_roads = gpd.read_file("data/week5/california/madera-county-roads/tl_2013_06039_roads.shp")
#sjer_crop_extent = gpd.read_file(op.join(path_data, 'california', 'SJER', 'vector_data', 'SJER_crop.shp'))
sjer_crop_extent = gpd.read_file("data/week5/california/SJER/vector_data/SJER_crop.shp")


print("CRS:", sjer_roads.crs)
print("Spatial Extent roads layer:", sjer_roads.total_bounds)
sjer_roads.geom_type
print("CRS:",sjer_crop_extent.crs)
print("Spatial Extent crop boundary:", sjer_crop_extent.total_bounds)
sjer_crop_extent.geom_type
```

    CRS: {'init': 'epsg:4269'}
    Spatial Extent roads layer: (-120.530241, 36.771308999999995, -119.031075, 37.686847)
    CRS: {'init': 'epsg:32611'}
    Spatial Extent crop boundary: (254570.56699999966, 4107303.0768445507, 258867.40933092419, 4112361.9202610701)





    0    Polygon
    dtype: object





## Plot Multiple Shapefiles

The `.plot` method can be used to plot spatial objects. Use the following arguments to add a title to your plot and to layer several spatial objects

on top of each other in your plot.



* `add = TRUE`: overlay a shapefile or raster on top the existing plot. This argument mimics layers in a typical GIS application like QGIS.

* `main=""`: add a title to the plot. To add a line break to your title, use `\n` where the line break should occur.





```python
# ```{r plot-multiple-shapefiles, fig.cap="plot of sjer plots layered on top of the crop extent." }

# # Plot multiple shapefiles

# plot(sjer_crop_extent, col = "lightgreen",

#      main="NEON Harvard Forest\nField Site")

# plot(sjer_roads, add = TRUE)


# ```
# reproject the data
sjer_roads = sjer_roads.to_crs(sjer_plot_locations.crs)


# plot the data - overlayed
ax = sjer_crop_extent.plot(color='g', alpha=.5)
sjer_plot_locations.plot(ax=ax, markersize=10, color='r')
# add a title to the plot
ax.set_title('SJER Plot Locations\nMadera County, CA')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1133e10b8>




![png](output_29_1.png)



```python
ax = sjer_roads.plot(cmap='Greys', alpha=.5, figsize=(10, 10))
sjer_crop_extent.plot(color='g', ax=ax, alpha=.5)
sjer_plot_locations.plot(ax=ax, markersize=10, color='r')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x11ea2df60>




![png](output_30_1.png)


Why is plotting so slow?
I remember chris asking about this - it really is a lot slower than R.
* Can we zoom in to the extent of another object when we plot?
* Should i introduce crop here?


```python
# get spatial extent
bounds = sjer_crop_extent.geometry.bounds
bounds
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>minx</th>
      <th>miny</th>
      <th>maxx</th>
      <th>maxy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>254570.567</td>
      <td>4.107303e+06</td>
      <td>258867.409331</td>
      <td>4.112362e+06</td>
    </tr>
  </tbody>
</table>
</div>



We can zoom in on just our study area - defined by the sjer_crop_extent layer by defining the xlim and ylim coordinate boundaries.


```python
ax = sjer_crop_extent.plot(alpha=.5, figsize=(10, 10))
sjer_roads.plot(cmap='Greys', ax=ax, alpha=.5)
sjer_plot_locations.plot(ax=ax, markersize=10, color='r')

# set the bounds of the map using the extent object
plt.xlim([bounds.minx.min()-5, bounds.maxx.max()+5])
plt.ylim([bounds.miny.min()-5, bounds.maxy.max()+5]);
```


![png](output_34_0.png)



```python

```
