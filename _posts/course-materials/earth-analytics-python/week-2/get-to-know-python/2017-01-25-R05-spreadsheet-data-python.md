---
layout: single
title: "Working with spreadsheet (tabular) data in R"
excerpt: "."
authors: ['Data Carpentry', 'Leah Wasser']
category: [course-materials]
class-lesson: ['get-to-know-r']
permalink: /course-materials/earth-analytics-python/week-2/spreadsheet-data-in-R/
nav-title: 'Spreadsheet Data in R'
dateCreated: 2016-12-13
modified: 2017-05-25
week: 2
sidebar:
  nav:
author_profile: false
comments: true
order: 5
---



{% include toc title="In This Lesson" icon="file-text" %}



This lesson introduces the data.frame which is very similar to working with

a spreadsheet in `R`.



<div class='notice--success' markdown="1">



## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives

At the end of this activity, you will be able to:



* Open .csv or text file containing tabular (spreadsheet) formatted data in R.

* Quickly plot the data using the GGPLOT2 function qplot()



## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need



You need R and RStudio to complete this tutorial. Also we recommend have you

have an `earth-analytics` directory setup on your computer with a `/data`

directory with it.



* [How to Setup R / R Studio](/course-materials/earth-analytics-python/week-1/setup-r-rstudio/)

* [Setup your working directory](/course-materials/earth-analytics-python/week-1/setup-working-directory/)





</div>



In the homework from week 1, we used the code below to create a report with `knitr`

in `RStudio`.





```python
import earthlab as et
import numpy as np
import pandas as pd
```


```python
paths = et.data.get_data('week_02')
print(paths)
```

    Replace is False and data exists, so doing nothing. Use replace==True to re-download the data.
    Replace is False and data exists, so doing nothing. Use replace==True to re-download the data.
    ['/Users/choldgraf/data_earthlab/week_02/boulder-precip.csv', '/Users/choldgraf/data_earthlab/week_02/temperature_example.csv']



```python
# ```{r open-file }



# # load the ggplot2 library for plotting

# library(ggplot2)



# # turn off factors

# options(stringsAsFactors = FALSE)



# # download data from figshare

# # note that we are downloaded the data into your

# download.file(url = "https://ndownloader.figshare.com/files/7010681",

#               destfile = "data/boulder-precip.csv")

# ```

```



Let's break the code above down. First, we use the `download.file` function to

download a datafile. In this case, the data are housed on

<a href="http://www.figshare.com" target="_blank">Figshare</a> - a

popular data repository that is free to use if your data are cumulatively

smaller than 20gb.



Notice that download.file() function has two **ARGUMENTS**:



1. **url**: this is the path to the data file that you wish to download

2. **destfile**: this is the location on your computer (in this case: `/data`) and name of the

file when saved (in this case: boulder-precip.csv). So we downloaded a file from

a url on figshare do our data directory. We named that file `boulder-precip.csv`.



Next, we read in the data using the function: `read.csv()`.





```python
boulder_precip = pd.read_csv(paths[0], index_col=0)
boulder_precip.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DATE</th>
      <th>PRECIP</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>756</th>
      <td>2013-08-21</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>757</th>
      <td>2013-08-26</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>758</th>
      <td>2013-08-27</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>759</th>
      <td>2013-09-01</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>760</th>
      <td>2013-09-09</td>
      <td>0.1</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Not sure what `str` should be mapped to in python
```


```python
# ```{r import-data }

# # import data

# boulder_precip <- read.csv(file="data/boulder-precip.csv")



# # view first few rows of the data

# head(boulder_precip)



# # view the format of the boulder_precip object in R

# str(boulder_precip)

# ```

```

<div class="notice--warning" markdown="1">



## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Challenge

What is the format associated with each column for the `boulder_precip`

data.frame? Describe the attributes of each format. Can you perform math

on each column? Why or why not?



<!--

integer - numbers without decimal points,

character: text strings

number: numeric values (can contain decimals places)

 -->



</div>



## Introduction to the Data.Frame



When we read data into R using read.csv() it imports it into a data frame format.

Data frames are the _de facto_ data structure for most tabular data, and what we

use for statistics and plotting.



A data frame is a collection of vectors of identical lengths. Each vector

represents a column, and each vector can be of a different data type (e.g.,

characters, integers, factors). The `str()` function is useful to inspect the

data types of the columns.



A data frame can be created by hand, but most commonly they are generated when

you important a text file or spreadsheet into R using the

functions `read.csv()` or `read.table()`.



## Extracting / Specifying "columns" By Name



You can extract just one single column from your data.frame using the `$` symbol

followed by the name of the column (or the column header):





```python
# when we download the data we create a dataframe
# view each column of the data frame using its name (or header)
boulder_precip['DATE']
```




    756    2013-08-21
    757    2013-08-26
    758    2013-08-27
    759    2013-09-01
    760    2013-09-09
    761    2013-09-10
    762    2013-09-11
    763    2013-09-12
    764    2013-09-13
    765    2013-09-15
    766    2013-09-16
    767    2013-09-22
    768    2013-09-23
    769    2013-09-27
    770    2013-09-28
    771    2013-10-01
    772    2013-10-04
    773    2013-10-11
    Name: DATE, dtype: object




```python
# view the precip column

boulder_precip['PRECIP']
```


```python
# ```{r view-column }

# # when we download the data we create a dataframe

# # view each column of the data frame using its name (or header)

# boulder_precip$DATE



# # view the precip column

# boulder_precip$PRECIP

# ```

```





## View Structure of a Data Frame



We can explore the format of our data frame in a similar way to how we explored

vectors in the third lesson of this module. Let's take a look.







```python
boulder_precip.shape
```




    (18, 2)




```python
# ```{r view-structure }

# # when we download the data we create a dataframe

# # view each column of the data frame using its name (or header)

# # how many rows does the data frame have

# nrow(boulder_precip)



# # view the precip column

# boulder_precip$PRECIP

# ```

```



## Plotting our Data



We can quickly plot our data too. Note that we are using the `ggplot2` function

qplot() rather than the R base plot functionality. We are doing this because

`ggplot2` is generally more powerful and efficient to use for plotting.





```python
%matplotlib inline
```


```python
ax = boulder_precip.plot('DATE', 'PRECIP')
plt.setp(ax.get_xticklabels(), rotation=45);
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/get-to-know-python/2017-01-25-R05-spreadsheet-data-python_18_0.png)



```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
boulder_precip['DATE'] = pd.to_datetime(boulder_precip['DATE'])
ax.plot('DATE', 'PRECIP', data=boulder_precip)
plt.setp(ax.get_xticklabels(), rotation=45);
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/get-to-know-python/2017-01-25-R05-spreadsheet-data-python_19_0.png)



```python
# ```{r quick-plot, fig.cap="plot precipitation data" }

# # q plot stands for quick plot. Let's use it to plot our data

# qplot(x=boulder_precip$DATE,

#       y=boulder_precip$PRECIP)



# ```

```
