---
layout: single
title: "Customize ggplot plots in R - earth analytics - data science for scientists"
excerpt: 'This lesson covers how to customize ggplot plot colors and label axes in R. It uses the ggplot2 package.'
authors: ['Leah Wasser', 'Data Carpentry']
modified: 2017-05-25
category: [course-materials]
class-lesson: ['hw-ggplot2-r']
nav-title: 'GGPLOT R'
permalink: /course-materials/earth-analytics/week-2/hw-ggplot2-r/
module-description: 'This module covers handling with data fields in R so you can efficiently plot time series data using ggplot(). We will use the as.DATE() function to convert dates stored in a data.frame to a date class. We will then plot the time series data using ggplot() and learn how to customize colors and axis labels. '
module-nav-title: 'Time Series Data in R'
module-title: 'Work with Sensor Network Derived Time Series Data in R'
module-type: 'homework'
course: "earth-analytics"
week: 2
sidebar:
  nav:
author_profile: false
comments: true
order: 1
topics:
  reproducible-science-and-programming: ['RStudio']
  data-exploration-and-analysis: ['data-visualization']
---



{% include toc title="In This Lesson" icon="file-text" %}



In this tutorial, we will explore more advanced plotting techniques using `ggplot2`.



<div class='notice--success' markdown="1">



## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives

At the end of this activity, you will be able to:



* Use the `ggplot()` plot function to create custom plots.

* Add labels to x and y axes and a title to your ggplot plot.

* Customize the colors and look of a ggplot plot.



## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need



You need `R` and `RStudio` to complete this tutorial. Also you should have

an `earth-analytics` directory setup on your computer with a `/data`

directory with it.



* [How to Setup R / RStudio](/course-materials/earth-analytics/week-1/setup-r-rstudio/)

* [Setup your working directory](/course-materials/earth-analytics/week-1/setup-working-directory/)

* [Intro to the R & RStudio Interface](/course-materials/earth-analytics/week-1/intro-to-r-and-rstudio)



</div>





In our week 1 homework, we used the quick plot function of ggplot2 to plot our data.

In this tutorial, we'll explore ggplot - which offers many more advanced plotting

features.



Let's explore the code below to create a quick plot.





```python
import earthlab as et
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
plt.ion()
plt.style.use('ggplot')
```


```python
os.chdir('/Users/choldgraf/earth-analytics/')
```


```python
et.download("https://ndownloader.figshare.com/files/7010681", 'boulder-precip.csv', './data/')
```

    Downloading data from https://s3-eu-west-1.amazonaws.com/pfigshare-u-files/7010681/precipboulderaugoct2013.csv (391 bytes)
    
    [........................................] 100.00000 | (391 bytes / 391 bytes)   
    File saved as ./data/boulder-precip.csv.
    
    Successfully moved file to ./data/boulder-precip.csv





    './data/boulder-precip.csv'




```python
boulder_precip = pd.read_csv('./data/boulder-precip.csv', index_col=0, parse_dates=['DATE'])
```


```python
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
boulder_precip.plot('DATE', 'PRECIP')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1194d9b00>




![png](../../../../../images/course-materials/earth-analytics-python//week-2/hw-plot-precip-data/2017-01-25-flood01-intro-to-ggplot-R_7_1.png)



```python
# ```{r plot-data, fig.cap="quick plot of precip data"}



# # load the ggplot2 library for plotting

# library(ggplot2)



# # download data from figshare

# # note that we already downloaded the data to our laptops previously

# # but in case you don't have it - re-download it by uncommenting the code below.

# # download.file(url = "https://ndownloader.figshare.com/files/7010681",

# #              destfile = "data/boulder-precip.csv")



# # import data

# boulder_precip <- read.csv(file="data/boulder-precip.csv")



# # view first few rows of the data

# head(boulder_precip)



# # when we download the data we create a dataframe

# # view each column of the data frame using its name (or header)

# boulder_precip$DATE



# # view the precip column

# boulder_precip$PRECIP



# # q plot stands for quick plot. Let's use it to plot our data

# qplot(x=boulder_precip$DATE,

#       y=boulder_precip$PRECIP)



# ```

```



## Plot with ggplot2



`ggplot2` is a plotting package that makes it simple to create complex plots

from data in a data.frame. It uses default settings, which help to create

publication quality plots with a minimal amount of settings and tweaking.



ggplot graphics are built step by step by adding new elements.



To build a ggplot() we need to:



- bind the plot to a specific data frame using the `data` argument





```python
fig, ax = plt.subplots()
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/hw-plot-precip-data/2017-01-25-flood01-intro-to-ggplot-R_10_0.png)



```python
# ```{r, eval=FALSE, purl=FALSE, fig.cap="ggplot binding"}

# ggplot(data = boulder_precip)



# ```

```





- define aesthetics (`aes`), by selecting the variables to be plotted and the variables to define the presentation

     such as plotting size, shape color, etc.,





```python
fig, ax = plt.subplots()
ax.plot('DATE', 'PRECIP', data=boulder_precip)
ax.set(title="matplotlib example plot precip")
plt.setp(ax.get_xticklabels(), rotation=45);
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/hw-plot-precip-data/2017-01-25-flood01-intro-to-ggplot-R_13_0.png)



```python
# ```{r, eval=FALSE, purl=FALSE, fig.cap="ggplot example plot precip"}

# ggplot(data = boulder_precip, aes(x = DATE, y = PRECIP))

# ```

```



- add `geoms` -- graphical representation of the data in the plot (points,

     lines, bars). To add a geom to the plot use `+` operator:





```python
fig, ax = plt.subplots()
ax.plot('DATE', 'PRECIP', '-o', data=boulder_precip)
ax.set(title="matplotlib example plot precip")
plt.setp(ax.get_xticklabels(), rotation=45);
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/hw-plot-precip-data/2017-01-25-flood01-intro-to-ggplot-R_16_0.png)



```python
# ```{r first-ggplot, purl=FALSE, fig.cap="ggplot boulder precip"}

# ggplot(data = boulder_precip,  aes(x = DATE, y = PRECIP)) +

#   geom_point()



# ```

```



The `+` in the `ggplot2` package is particularly useful because it allows you

to modify existing `ggplot` objects. This means you can easily set up plot

"templates" and conveniently explore different types of plots, so the above

plot can also be generated with code like this:





```python
# This would just be a combination of calls to `ax.scatter` `ax.plot` etc
# Could show here that you can also give the values directly to the plotting functions, e.g.:
```


```python
dates = pd.date_range(pd.datetime(2016, 1, 1), pd.datetime(2016, 1, 2), freq='H')
dates = pd.DataFrame(dates, columns=['date'])
```


```python
boulder_precip['DATE'].index
```




    Int64Index([756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768,
                769, 770, 771, 772, 773],
               dtype='int64')




```python
fig, ax = plt.subplots()
ax.scatter(boulder_precip['DATE'].values, boulder_precip['PRECIP'].values)
plt.setp(ax.get_xticklabels(), rotation=45);
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/hw-plot-precip-data/2017-01-25-flood01-intro-to-ggplot-R_22_0.png)



```python
# ```{r, first-ggplot-with-plus, eval=FALSE, purl=FALSE, fig.cap="first ggplot"}

# # Create the plot object (nothing will render on your screen)

# precip_plot <-  ggplot(data = boulder_precip,  aes(x = DATE, y = PRECIP))



# # Draw the plot

# precip_plot + geom_point()



# ```

```





```python
# ```{r, eval=FALSE, purl=TRUE, echo=FALSE, purl=FALSE, fig.cap="2nd ggplot"}

# # Create

# precip_plot <-  ggplot(data = boulder_precip,  aes(x = DATE, y = PRECIP))



# # Draw the plot

# precip_plot + geom_point()

# ```

```





We can also apply a color to our points





```python
fig, ax = plt.subplots()
ax.scatter(boulder_precip['DATE'].values, boulder_precip['PRECIP'].values,
           c='blue')
plt.setp(ax.get_xticklabels(), rotation=45);
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/hw-plot-precip-data/2017-01-25-flood01-intro-to-ggplot-R_27_0.png)



```python
# ```{r adding-colors, purl=FALSE, fig.cap="ggplot with blue points"}

# ggplot(data = boulder_precip,  aes(x = DATE, y = PRECIP)) +

#     geom_point(color = "blue")



# ```

```



And adjust the transparency.





```python
fig, ax = plt.subplots()
ax.scatter(boulder_precip['DATE'].values, boulder_precip['PRECIP'].values,
           c='blue', alpha=.5)
plt.setp(ax.get_xticklabels(), rotation=45);
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/hw-plot-precip-data/2017-01-25-flood01-intro-to-ggplot-R_30_0.png)



```python
# ```{r add-alpha, fig.cap="ggplot with blue points and alpha"}

# ggplot(data = boulder_precip,  aes(x = DATE, y = PRECIP)) +

#     geom_point(alpha=.5, color = "blue")



# ```

```





Or to color each value in the plot differently:





```python
fig, ax = plt.subplots()
ax.scatter(boulder_precip['DATE'].values, boulder_precip['PRECIP'].values,
           c=boulder_precip['PRECIP'].values, alpha=.5, cmap='rainbow')
plt.setp(ax.get_xticklabels(), rotation=45);
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/hw-plot-precip-data/2017-01-25-flood01-intro-to-ggplot-R_33_0.png)



```python
# ```{r color-by-species, purl=FALSE, fig.cap="ggplot with colored points"}

# ggplot(data = boulder_precip,  aes(x = DATE, y = PRECIP)) +

#     geom_point(alpha = 0.9, aes(color=PRECIP))



# ```

```





We can turn our plot into a bar plot.





```python
fig, ax = plt.subplots()
ax.bar(boulder_precip['DATE'].values, boulder_precip['PRECIP'].values)
plt.setp(ax.get_xticklabels(), rotation=45);
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/hw-plot-precip-data/2017-01-25-flood01-intro-to-ggplot-R_36_0.png)



```python
# ```{r barplot, purl=FALSE, fig.cap="ggplot with bars"}

# ggplot(data = boulder_precip,  aes(x = DATE, y = PRECIP)) +

#     geom_bar(stat="identity")



# ```

```



Turn the bar outlines blue





```python
fig, ax = plt.subplots()
ax.bar(boulder_precip['DATE'].values, boulder_precip['PRECIP'].values,
       edgecolor='blue')
plt.setp(ax.get_xticklabels(), rotation=45);
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/hw-plot-precip-data/2017-01-25-flood01-intro-to-ggplot-R_39_0.png)



```python
# ```{r bar-color, purl=FALSE, fig.cap="ggplot with blue bars"}

# ggplot(data = boulder_precip,  aes(x = DATE, y = PRECIP)) +

#     geom_bar(stat="identity", color="blue")



# ```

```



Change the fill to bright green.





```python
fig, ax = plt.subplots()
ax.bar(boulder_precip['DATE'].values, boulder_precip['PRECIP'].values,
       edgecolor='blue', color='green')
plt.setp(ax.get_xticklabels(), rotation=45);
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/hw-plot-precip-data/2017-01-25-flood01-intro-to-ggplot-R_42_0.png)



```python
# ```{r barcolor2, purl=FALSE, fig.cap="ggplot with green bars"}

# ggplot(data = boulder_precip,  aes(x = DATE, y = PRECIP)) +

#     geom_bar(stat="identity", color="blue", fill="green")



# ```

```





## Add plot labels



You can add labels to your plots as well. Let's add a title, and x and y labels using the glab() argument.





```python
fig, ax = plt.subplots()
ax.bar(boulder_precip['DATE'].values, boulder_precip['PRECIP'].values,
       edgecolor='blue')
plt.setp(ax.get_xticklabels(), rotation=45);
ax.set(xlabel="Date", ylabel="Precipitation (Inches)", title="Daily Precipitation (inches)\nBoulder, Colorado 2013");
```


![png](../../../../../images/course-materials/earth-analytics-python//week-2/hw-plot-precip-data/2017-01-25-flood01-intro-to-ggplot-R_45_0.png)



```python
# ```{r add-title, fig.cap="ggplot with labels" }

# ggplot(data = boulder_precip,  aes(x = DATE, y = PRECIP)) +

#     geom_point(alpha = 0.9, aes(color=PRECIP)) +

#     glabs(x="Date",

#       y="Precipitation (Inches)",

#       title="Daily Precipitation (inches)"

#       subtitle="Boulder, Colorado 2013")

# ```

```


```python

```
