---
layout: single
title: "Missing data in Python"
excerpt: "This tutorial introduces the concept of missing of no data values in Python."
authors: ['Data Carpentry', 'Leah Wasser']
category: [course-materials]
class-lesson: ['get-to-know-python']
permalink: /course-materials/earth-analytics-python/week-2/missing-data-in-python-na/
nav-title: 'Missing data'
dateCreated: 2017-05-23
modified: 2017-06-05
week: 2
sidebar:
  nav:
author_profile: false
comments: true
order: 4
course: "earth-analytics-python"
topics:
  reproducible-science-and-programming: ['jupyter-notebooks']
---

{% include toc title="In This Lesson" icon="file-text" %}

This lesson covers how to work with no data values in `Python`.

<div class='notice--success' markdown="1">

## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives
At the end of this activity, you will be able to:

* Understand why it is important to make note of missing data values.
* Be able to define what a `NA` value is in `R` and how it is used in a vector.

## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need

You need R and RStudio to complete this tutorial. Also we recommend have you
have an `earth-analytics` directory setup on your computer with a `/data`
directory with it.

* [How to Setup R / R Studio](/course-materials/earth-analytics/week-1/setup-r-rstudio/)
* [Setup your working directory](/course-materials/earth-analytics/week-1/setup-working-directory/)


</div>

## Missing data - No Data Values

Sometimes, our data are missing values. Imagine a spreadsheet in Microsoft excel
with cells that are blank. If the cells are blank, we don't know for sure whether
those data weren't collected, or something someone forgot to fill in. To account
for data that are missing (not by mistake) we can put a value in those cells
that represents `no data`.

The `Python` programming language uses the value `np.nan` to represent missing data values.


```python
# work with numeric data
import numpy as np
# work with tabular data - dataframes
import pandas as pd
# download data from a url
import urllib
import os
# note that the dir names are week02 rather than week2. week 02 is better but i want to wait to fix all of the R lessons before fixing them here.

```


```python
# be sure to set your working directory\n",
os.chdir("/Users/lewa8222/Documents/earth-analytics/")
```


```python
planets = np.array(["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus",
                    "Neptune", np.nan])
planets
```




    array(['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
           'Neptune', 'nan'], 
          dtype='<U7')



When the numpy library is loaded, the default setting for most base functions that read data into `python` is to
interpret `np.nan` as a missing value.

## Customizing no data values

Sometimes, you'll find a dataset that uses another value for missing data. In some
disciplines, for example -999 is sometimes used. If there are multiple types of
missing values in your dataset, you can extend what `R` considers a missing value when it reads
the file in using  "`na_values`" argument. For instance, if you wanted to read
in a `.CSV` file named `temperature_example.csv` that had missing values represented as an empty
cell, a single blank space, and the value -999, you would use:


```python
# download file from Earth Lab figshare repository
urllib.request.urlretrieve(url='https://ndownloader.figshare.com/files/7275959', 
                           filename= 'data/week2/temperature_example.csv')
```




    ('data/week2/temperature_example.csv',
     <http.client.HTTPMessage at 0x10f3014e0>)




```python
# import data frame without specifying missing data values
temp_df = pd.read_csv('data/week2/temperature_example.csv')
temp_df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>avg_temp</th>
      <th>day</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>55.0</td>
      <td>thursday</td>
    </tr>
    <tr>
      <th>1</th>
      <td>25.0</td>
      <td>tuesday</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NaN</td>
      <td>wednesday</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-999.0</td>
      <td>saturday</td>
    </tr>
    <tr>
      <th>4</th>
      <td>15.0</td>
      <td>thursday</td>
    </tr>
    <tr>
      <th>5</th>
      <td>25.0</td>
      <td>tuesday</td>
    </tr>
    <tr>
      <th>6</th>
      <td>65.0</td>
      <td>thursday</td>
    </tr>
    <tr>
      <th>7</th>
      <td>NaN</td>
      <td>tuesday</td>
    </tr>
    <tr>
      <th>8</th>
      <td>95.0</td>
      <td>thursday</td>
    </tr>
    <tr>
      <th>9</th>
      <td>-999.0</td>
      <td>monday</td>
    </tr>
    <tr>
      <th>10</th>
      <td>85.0</td>
      <td>monday</td>
    </tr>
    <tr>
      <th>11</th>
      <td>-999.0</td>
      <td>monday</td>
    </tr>
    <tr>
      <th>12</th>
      <td>85.0</td>
      <td>monday</td>
    </tr>
  </tbody>
</table>
</div>



In the example above, we imported the data and the -999.0 values imported as numeric values. This will in turn impact any statistics or calculations run on that data column.


```python
temp_df.mean()
```




    avg_temp   -231.545455
    dtype: float64



However, if we specify what the missing data values is when we import that data, then it will be assigned a np.nan value. Python will thus know to ignore those cells when it performs calculations on the data.


```python
temp_df2 = pd.read_csv('data/week2/temperature_example.csv', 
                       na_values=['NA', ' ', '-999'])
temp_df2
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>avg_temp</th>
      <th>day</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>55.0</td>
      <td>thursday</td>
    </tr>
    <tr>
      <th>1</th>
      <td>25.0</td>
      <td>tuesday</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NaN</td>
      <td>wednesday</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NaN</td>
      <td>saturday</td>
    </tr>
    <tr>
      <th>4</th>
      <td>15.0</td>
      <td>thursday</td>
    </tr>
    <tr>
      <th>5</th>
      <td>25.0</td>
      <td>tuesday</td>
    </tr>
    <tr>
      <th>6</th>
      <td>65.0</td>
      <td>thursday</td>
    </tr>
    <tr>
      <th>7</th>
      <td>NaN</td>
      <td>tuesday</td>
    </tr>
    <tr>
      <th>8</th>
      <td>95.0</td>
      <td>thursday</td>
    </tr>
    <tr>
      <th>9</th>
      <td>NaN</td>
      <td>monday</td>
    </tr>
    <tr>
      <th>10</th>
      <td>85.0</td>
      <td>monday</td>
    </tr>
    <tr>
      <th>11</th>
      <td>NaN</td>
      <td>monday</td>
    </tr>
    <tr>
      <th>12</th>
      <td>85.0</td>
      <td>monday</td>
    </tr>
  </tbody>
</table>
</div>




```python
temp_df2.mean()
```




    avg_temp    56.25
    dtype: float64



In the example below, note how a mean value is calculated differently depending
upon on how NA values are treated when the data are imported.


# What's the difference between doing np.mean and dataframe.mean() ??
# why is dropna used below whereas it's not used in the previous 2 cells? it doesn't seem to ignore the na values unless they're explicetiy sent to dropna() ??



```python
np.mean(temp_df)
```




    avg_temp   -231.545455
    dtype: float64




```python
np.mean(temp_df2)
```




    avg_temp    56.25
    dtype: float64




```python
print(np.mean(temp_df['avg_temp']))
print(np.mean(temp_df2['avg_temp']))
```

    -231.54545454545453
    56.25



```python
print(np.mean(temp_df['avg_temp'].dropna()))
print(np.mean(temp_df2['avg_temp'].dropna()))
```

    -231.54545454545453
    56.25



```python
# confused about why this works below
np.nanmean(temp_df2['avg_temp'])
```




    56.25



Notice a difference between `temp_df` and `temp_df2` ?

<div class="notice--warning" markdown="1">

## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Optional challenge

* **Question**: Why, in the the example above did mean(temp_df) return
a negative value whereas mean(temp_df2) which is the same data returned a positive value?

<!-- * _Answer_: Because if there are NA values in a dataset that are numeric, python will calculate them as numeric values. In this case -999 was a NA value. By importing the data using na_strings= we can specify what values should be converted to NA by python. -->

</div>

# dooes python by default know to ignore NA when performing math?
# i generally don't understand how this works in python

When performing mathematical operations on numbers in `Python`, most functions will
return the value `NA` if the data you are working with include missing values.
This allows you to see that you have missing data in your dataset. You can add the
argument `na.rm=TRUE` to calculate the result while ignoring the missing values.

# below this seems to be a different way of handing missing data. what's the best approach? previously we did .dropna 


```python
heights = np.array([2, 4, 4, np.nan, 6])
print(np.mean(heights))
print(np.max(heights))
```

    nan
    nan



```python
print(np.mean(heights[~np.isnan(heights)]))
print(np.max(heights[~np.isnan(heights)]))
```

    4.0
    6.0



```python
print(np.nanmean(heights))
print(np.nanmax(heights))
```

    4.0
    6.0



```python
# ```{r math-no-data }

# heights <- c(2, 4, 4, NA, 6)

# mean(heights)

# max(heights)

# mean(heights, na.rm = TRUE)

# max(heights, na.rm = TRUE)

# ```

```

The function, `np.isnan()` can be used to figure out if your data has assigned (`nan`) no-data values. 
If we use `np.isnan()` we can see just the objects that are missing data values. In this case, we have one nan object.


```python
# view objects that equal nan
heights[np.isnan(heights)]

```




    array([ nan])




```python
# how many nan values are in our array?
len(heights[np.isnan(heights)])

```




    1



We can select all of the objects that are values (not equal to nan) by asking python to return the inverse of what we selected above. We use the `~` sign to request the inverse as follows:

`~np.isnan(object-name-here)`


```python
# select objects that are NON equal to NAN.
heights[~np.isnan(heights)]
```




    array([ 2.,  4.,  4.,  6.])




```python
# no "omit" function in python nor "complete cases"
```


<div class="notice--warning" markdown="1">
## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Challenge

* **Question**: Why does the following piece of code return a warning?

</div>

# remove or change this challenge as it's not an issue in python - it seems python by default knows to ignore NAN values. Is this correct? 


```python
# This doesn't return a warning in python
sample = np.array([2, 4, 4, np.nan, 6])
np.nanmean(sample)
```




    4.0




```python
# ```{r, purl=FALSE}

# sample <- c(2, 4, 4, "NA", 6)

# mean(sample, na.rm = TRUE)

# ```

```
