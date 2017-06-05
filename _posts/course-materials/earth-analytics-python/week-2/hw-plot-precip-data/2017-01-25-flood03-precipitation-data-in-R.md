---
layout: single
title: "Subset time series data in R - introduction to dplyr pipes and tidyverse coding approaches - Flooding & erosion data"
excerpt: "This lesson walks through extracting temporal subsets of time series data using dplyr pipes. In the previous lesson we learned how to convert data containing a data field into a data class. In this lesson we use pipes to extract temporal subsets so that we can refine our time series data analysis. Finally we plot the data using ggplot."
authors: ['Leah Wasser']
modified: 2017-06-05
category: [course-materials]
class-lesson: ['hw-ggplot2-r']
permalink: /course-materials/earth-analytics/week-2/precip-in-r/
nav-title: 'Subset time series data in R'
week: 2
sidebar:
  nav:
author_profile: false
comments: true
order: 3
course: "earth-analytics"
topics:
  reproducible-science-and-programming: ['RStudio']
  time-series:
  data-exploration-and-analysis: ['data-visualization']
---



{% include toc title="In This Lesson" icon="file-text" %}







```python
import earthlab as et
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
plt.ion()
```


```python
os.chdir('/Users/choldgraf/earth-analytics/')
```


```python
precip_boulder = pd.read_csv('data/week_02-hw/precipitation/805325-precip-daily-2003-2013.csv', parse_dates=['DATE'])
```


```python
precip_boulder_daily = precip_boulder.groupby('DATE').aggregate(
    {'HPCP': 'sum', 'STATION': 'first', 'ELEVATION': 'first',
     'STATION_NAME': 'first', 'LATITUDE': 'first', 'LONGITUDE': 'first'})
precip_boulder_daily = precip_boulder_daily.rename(columns={'HPCP': 'DAILY_PRECIP'})
precip_boulder_daily.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ELEVATION</th>
      <th>STATION</th>
      <th>STATION_NAME</th>
      <th>DAILY_PRECIP</th>
      <th>LONGITUDE</th>
      <th>LATITUDE</th>
    </tr>
    <tr>
      <th>DATE</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2003-01-01 01:00:00</th>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.0</td>
      <td>-105.28111</td>
      <td>40.03389</td>
    </tr>
    <tr>
      <th>2003-02-01 01:00:00</th>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.0</td>
      <td>-105.28111</td>
      <td>40.03389</td>
    </tr>
    <tr>
      <th>2003-02-02 19:00:00</th>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.2</td>
      <td>-105.28111</td>
      <td>40.03389</td>
    </tr>
    <tr>
      <th>2003-02-02 22:00:00</th>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.1</td>
      <td>-105.28111</td>
      <td>40.03389</td>
    </tr>
    <tr>
      <th>2003-02-03 02:00:00</th>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.1</td>
      <td>-105.28111</td>
      <td>40.03389</td>
    </tr>
  </tbody>
</table>
</div>




```python
# ``` {r daily-summ, eval=F, echo=F}



# # the data processing workflow

# library(dplyr)

# library(lubridate)



# # import precip data into R data.frame

# precip_boulder <- read.csv("data/week2/precipitation/805325-precip-daily-2003-2013.csv",

#                            header = TRUE,

#                            na.strings = c(999.99))



# # convert time

# precip_boulder$DATE <- as.Date(precip_boulder$DATE, # convert to Date class

#                                   format="%Y%m%d %H:%M")

#                                   #DATE in the format: YearMonthDay Hour:Minute



# precip_boulder_daily <- precip_boulder %>%

#     group_by(DATE) %>% # summarize on the date column

#     summarize(DAILY_PRECIP = sum(HPCP, na.rm=TRUE), # sum up rainfall for each day

#               STATION = first(STATION), STATION_NAME= first(STATION_NAME),

#               ELEVATION= first(ELEVATION), LATITUDE= first(LATITUDE),

#               LONGITUDE= first(LONGITUDE))
```


```python
precip_boulder_daily['YEAR'] = precip_boulder_daily.index.year
precip_boulder_daily['JULIAN'] = precip_boulder_daily.index.date
precip_boulder_daily.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ELEVATION</th>
      <th>STATION</th>
      <th>STATION_NAME</th>
      <th>DAILY_PRECIP</th>
      <th>LONGITUDE</th>
      <th>LATITUDE</th>
      <th>YEAR</th>
      <th>JULIAN</th>
    </tr>
    <tr>
      <th>DATE</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2003-01-01 01:00:00</th>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.0</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-01-01</td>
    </tr>
    <tr>
      <th>2003-02-01 01:00:00</th>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.0</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-01</td>
    </tr>
    <tr>
      <th>2003-02-02 19:00:00</th>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.2</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-02</td>
    </tr>
    <tr>
      <th>2003-02-02 22:00:00</th>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.1</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-02</td>
    </tr>
    <tr>
      <th>2003-02-03 02:00:00</th>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.1</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-03</td>
    </tr>
  </tbody>
</table>
</div>




```python
precip_boulder_daily.to_csv('./data/week_02-hw/precipitation/805325-precip-dailysum-2003-2013.csv')
```


```python
# # add a year

# precip_boulder_daily$YEAR <- format(precip_boulder_daily$DATE, "%Y")

# # add a jday

# precip_boulder_daily$JULIAN <- yday(precip_boulder_daily$DATE)



# # view the results

# # head(precip_boulder_daily)



# # export to daily csv

# write.csv(precip_boulder_daily, "data/week2/805325-precip-dailysum-2003-2013.csv")



# ```
```



In this lesson, we will learn how to import a larger dataset, and test our

skills cleaning and plotting the data.





<div class='notice--success' markdown="1">



## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives



After completing this tutorial, you will be able to:



* Import a text file into R.

* Plot quantitative time series data using ggplot

* Ensure that NoData values do not interfere with quantitative analysis by setting them to `NA` in `R`.

* Use the `na.rm` argument when performing math with large datasets.

* Subset data using the dplyr `filter()` function

* Use dplyr pipes to filter data in R.



## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need



You need `R` and `RStudio` to complete this tutorial. Also you should have

an `earth-analytics` directory setup on your computer with a `/data`

directory with it.



* [How to Setup R / RStudio](/course-materials/earth-analytics/week-1/setup-r-rstudio/)

* [Setup your working directory](/course-materials/earth-analytics/week-1/setup-working-directory/)

* [Intro to the R & RStudio Interface](/course-materials/earth-analytics/week-1/intro-to-r-and-rstudio)



### R Libraries to Install:



* **ggplot2:** `install.packages("ggplot2")`

* **dplyr:** `install.packages("dplyr")`





[<i class="fa fa-download" aria-hidden="true"></i> Download Week 2 Data](https://ndownloader.figshare.com/files/7426738){:data-proofer-ignore='' .btn }



</div>



## Important - Data Organization

Before you begin this lesson, be sure that you've downloaded the dataset above.

You will need to UNZIP the zip file. When you do this, be sure that your directory

looks like the image below: note that all of the data are within the week2

directory. They are not nested within another directory. You may have to copy and

paste your files to make this look right.



<figure>

<a href="{{ site.baseurl }}/images/course-materials/earth-analytics/week-2/week2-data.png">

<img src="{{ site.baseurl }}/images/course-materials/earth-analytics/week-2/week2-data.png" alt="week 2 file organization">

</a>

<figcaption>Your `week2` file directory should look like the one above. Note that

the data directly under the week-2 folder.</figcaption>

</figure>



## Get started with time series data

Let's get started by loading the `ggplot2` and `dplyr` libraries. Also, let's set

our working directory. Finally, set `stringsAsFactors` to `FALSE` globally as

shown below.





```python
precip_boulder = pd.read_csv('./data/week_02-hw/precipitation/805325-precip-dailysum-2003-2013.csv', parse_dates=['DATE'])
```


```python
# ```{r load-libraries}

# # set your working directory to the earth-analytics directory

# # setwd("working-dir-path-here")



# # load packages

# library(ggplot2) # efficient plotting

# library(dplyr) # efficient data manipulation



# # set strings as factors to false for everything

# options(stringsAsFactors = FALSE)



# ```

```





## Import precipitation time series



We will use a precipitation dataset derived from data accessed through the

National Centers for Environmental Information (formerly

National Climate Data Center) Cooperative Observer Network (COOP)

station 050843 in Boulder, CO. The data time span is: 1 January 2003 through 31

December 2013.



We can use `read.csv()` to import the `.csv` file.





```python
boulder_daily_precip = pd.read_csv('./data/week_02-hw/precipitation/805325-precip-dailysum-2003-2013.csv', parse_dates=['DATE'])
boulder_daily_precip.head(6)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DATE</th>
      <th>ELEVATION</th>
      <th>STATION</th>
      <th>STATION_NAME</th>
      <th>DAILY_PRECIP</th>
      <th>LONGITUDE</th>
      <th>LATITUDE</th>
      <th>YEAR</th>
      <th>JULIAN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2003-01-01 01:00:00</td>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.0</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-01-01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2003-02-01 01:00:00</td>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.0</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2003-02-02 19:00:00</td>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.2</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-02</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2003-02-02 22:00:00</td>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.1</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-02</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2003-02-03 02:00:00</td>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.1</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-03</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2003-02-05 02:00:00</td>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.1</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-05</td>
    </tr>
  </tbody>
</table>
</div>




```python
boulder_daily_precip.describe()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ELEVATION</th>
      <th>DAILY_PRECIP</th>
      <th>LONGITUDE</th>
      <th>LATITUDE</th>
      <th>YEAR</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>1840.0</td>
      <td>1840.000000</td>
      <td>1840.000000</td>
      <td>1840.000000</td>
      <td>1840.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>1650.5</td>
      <td>51.192587</td>
      <td>-105.281106</td>
      <td>40.033851</td>
      <td>2007.954348</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.0</td>
      <td>220.208147</td>
      <td>0.000005</td>
      <td>0.000045</td>
      <td>3.252319</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1650.5</td>
      <td>0.000000</td>
      <td>-105.281110</td>
      <td>40.033800</td>
      <td>2003.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>1650.5</td>
      <td>0.100000</td>
      <td>-105.281110</td>
      <td>40.033800</td>
      <td>2005.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>1650.5</td>
      <td>0.100000</td>
      <td>-105.281110</td>
      <td>40.033890</td>
      <td>2008.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>1650.5</td>
      <td>0.100000</td>
      <td>-105.281100</td>
      <td>40.033890</td>
      <td>2011.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>1650.5</td>
      <td>999.990000</td>
      <td>-105.281100</td>
      <td>40.033890</td>
      <td>2013.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
# ```{r import-precip}

# # download the data

# # download.file(url = "https://ndownloader.figshare.com/files/7283285",

# #              destfile = "data/week2/805325-precip-dailysum_2003-2013.csv")



# # import the data

# boulder_daily_precip <- read.csv("data/week2/precipitation/805325-precip-dailysum-2003-2013.csv",

#          header = TRUE)





# # view first 6 lines of the data

# head(boulder_daily_precip)



# # view structure of data

# str(boulder_daily_precip)



# # are there any unusual / No data values?

# summary(boulder_daily_precip$DAILY_PRECIP)

# max(boulder_daily_precip$DAILY_PRECIP)

# ```

```



### About the Data



Viewing the structure of these data, we can see that different types of data are included in

this file.



* **STATION** and **STATION_NAME**: Identification of the COOP station.

* **ELEVATION, LATITUDE** and **LONGITUDE**: The spatial location of the station.

* **DATE**: The date when the data were collected in the format: YYYYMMDD. Notice that DATE is

currently class `chr`, meaning the data is interpreted as a character class and

not as a date.

* **DAILY_PRECIP**: The total precipitation in inches. Important: the metadata

notes that the value 999.99 indicates missing data. Also important,

hours with no precipitation are not recorded.

* **YEAR**: the year the data were collected

* **JULIAN**: the JULIAN DAY the data were collected.





Additional information about the data, known as metadata, is available in the

<a href="https://ndownloader.figshare.com/files/7283453">PRECIP_HLY_documentation.pdf</a>.

The metadata tell us that the noData value for these data is 999.99. IMPORTANT:

we have modified these data a bit for ease of teaching and learning. Specifically,

we've aggregated the data to represent daily sum values and added some noData

values to ensure you learn how to clean them!



You can download the original complete data subset with additional documentation

<a href="https://figshare.com/articles/NEON_Remote_Sensing_Boulder_Flood_2013_Teaching_Data_Subset_Lee_Hill_Road/3146284">here. </a>



<div class="notice--warning" markdown="1">



## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Challenge



Using everything you've learned in the previous lessons:



* Import the dataset: `data/week2/precipitation/805325-precip-dailysum-2003-2013.csv`

* Clean the data by assigning noData values to `NA`

* Make sure the date column is a date class

* When you are done, plot it using `ggplot()`.

  * Be sure to include a TITLE, and label the X and Y axes.

  * Change the color of the plotted points



Some notes to help you along:



* Date: be sure to take of the date format when you import the data.

* NoData Values: We know that the no data value = 999.99. We can account for this

when we read in the data. Remember how?



Your final plot should look something like the plot below.

</div>









```python
boulder_daily_precip = pd.read_csv('./data/week_02-hw/precipitation/805325-precip-dailysum-2003-2013.csv', parse_dates=['DATE'],
                                   na_values=[999.99])
boulder_daily_precip.head(6)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DATE</th>
      <th>ELEVATION</th>
      <th>STATION</th>
      <th>STATION_NAME</th>
      <th>DAILY_PRECIP</th>
      <th>LONGITUDE</th>
      <th>LATITUDE</th>
      <th>YEAR</th>
      <th>JULIAN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2003-01-01 01:00:00</td>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.0</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-01-01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2003-02-01 01:00:00</td>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.0</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2003-02-02 19:00:00</td>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.2</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-02</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2003-02-02 22:00:00</td>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.1</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-02</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2003-02-03 02:00:00</td>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.1</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-03</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2003-02-05 02:00:00</td>
      <td>1650.5</td>
      <td>COOP:050843</td>
      <td>BOULDER 2 CO US</td>
      <td>0.1</td>
      <td>-105.28111</td>
      <td>40.03389</td>
      <td>2003</td>
      <td>2003-02-05</td>
    </tr>
  </tbody>
</table>
</div>




```python
# ``` {r plot-precip-hourly, echo=F, warning=F, fig.cap="precip plot w fixed dates"}



# # do we need to do something about NA VALUES?

# boulder_daily_precip <- read.csv("data/week2/precipitation/805325-precip-dailysum-2003-2013.csv",

#          header = TRUE,

#          na.strings = 999.99)





# # format date

# boulder_daily_precip$DATE <- as.Date(boulder_daily_precip$DATE,

#                                      format="%m/%d/%y")
```


```python
fig, ax = plt.subplots()
ax.scatter(boulder_daily_precip['DATE'].values, boulder_daily_precip['DAILY_PRECIP'].values)
ax.set(xlabel="Date", ylabel="Precipitation (Inches)", title="Hourly Precipitation - Boulder Station\n 2003-2013");
```


![png](2017-01-25-flood03-precipitation-data-in-R_files/2017-01-25-flood03-precipitation-data-in-R_20_0.png)



```python
# # plot the data using ggplot2

# prec_plot_daily <- ggplot(data=boulder_daily_precip,  # the data frame

#       aes(DATE, DAILY_PRECIP)) +   # the variables of interest

#       geom_point() +   # create a bar graph

#       xlab("Date") + ylab("Precipitation (Inches)") +  # label the x & y axes

#       ggtitle("Hourly Precipitation - Boulder Station\n 2003-2013")  # add a title



# prec_plot_daily



# ```
```



<i fa fa-star></i>**Data Tip:**For a more thorough review of date/time classes, see the NEON tutorial

<a href="http://www.neondataskills.org/R/time-series-convert-date-time-class-POSIX/" target="_blank"> *Dealing With Dates & Times in R - as.Date, POSIXct, POSIXlt*</a>.

{: .notice--success}





<div class="notice--warning" markdown="1">



## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Optional challenge



Take a close look at the plot.



* What does each point represent?

* Use the `min()` and `max()` functions to determine the minimum and maximum precipitation values for the 10 year span?



</div>



## Subset the Data



If we wanted to zoom in and look at some data over a smaller time period, we can

subset it. Let create a subset of data for the time period around the flood between 15

August to 15 October 2013. We will use the `filter()` function in the `dplyr` package

to do this.



### Introduction to the pipe %<%



Pipes let you take the output of one function and send it directly to the next,

which is useful when you need to do many things to the same data set. Pipes in R

look like %>% and are made available via the `magrittr` package, installed

automatically with `dplyr`.







```python
precip_boulder_AugOct = boulder_daily_precip.query('DATE > "2013-08-15" and DATE <= "2013-10-15"')
```


```python
# ```{r subset-data}

# # subset 2 months around flood

# precip_boulder_AugOct <- boulder_daily_precip %>%

#                         filter(DATE >= as.Date('2013-08-15') & DATE <= as.Date('2013-10-15'))



# ```

```



In the code above, we use the pipe to send the `boulder_daily_precip` data through

a filter step. In that filter step, we filter our only the rows withing the

date range that we specified. Since `%>%` takes the object on its left and passes

it as the first argument to the function on its right, we don’t need to explicitly include it as an argument to the `filter()` function.







```python
print(precip_boulder_AugOct['DATE'].min())
print(precip_boulder_AugOct['DATE'].max())
```

    2013-08-21 17:00:00
    2013-10-10 18:00:00



```python
# ```{r check-subset, fig.cap="precip plot subset" }

# # check the first & last dates

# min(precip_boulder_AugOct$DATE)

# max(precip_boulder_AugOct$DATE)
```


```python
fig, ax = plt.subplots()
ax.plot(precip_boulder_AugOct['DATE'], precip_boulder_AugOct['DAILY_PRECIP'], 'o')
plt.setp(ax.get_xticklabels(), rotation=30)
ax.set(xlabel="Date", ylabel="Precipitation (inches)",
       title="Daily Total Precipitation Aug - Oct 2013 for Boulder Creek",
       xlim=["2013-08-01", "2013-11-01"]);
```


![png](2017-01-25-flood03-precipitation-data-in-R_files/2017-01-25-flood03-precipitation-data-in-R_28_0.png)



```python
# # create new plot

# precPlot_flood2 <- ggplot(data=precip_boulder_AugOct, aes(DATE,DAILY_PRECIP)) +

#   geom_bar(stat="identity") +

#   xlab("Date") + ylab("Precipitation (inches)") +

#   ggtitle("Daily Total Precipitation Aug - Oct 2013 for Boulder Creek")



# precPlot_flood2



# ```
```





<div class="notice--warning" markdown="1">



## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Challenge



Create a subset from the same dates in 2012 to compare to the 2013 plot.

Use the ylim() argument to ensure the y axis range is the SAME as the previous

plot - from 0 to 10".



How different was the rainfall in 2012?



HINT: type `?lims` in the console to see how the `xlim` and `ylim` arguments work.





</div>





```python
precip_boulder_AugOct_2012 = boulder_daily_precip.query('DATE > "2012-08-15" and DATE <= "2012-10-15"')
```


```python
fig, ax = plt.subplots()
ax.plot(precip_boulder_AugOct_2012['DATE'], precip_boulder_AugOct_2012['DAILY_PRECIP'], 'o')
plt.setp(ax.get_xticklabels(), rotation=30)
ax.set(xlabel="Date", ylabel="Precipitation (inches)",
       title="Daily Total Precipitation Aug - Oct 2012 for Boulder Creek",
       xlim=["2012-08-01", "2012-11-01"])
```




    [<matplotlib.text.Text at 0x1171c3fd0>,
     (734716.0, 734808.0),
     <matplotlib.text.Text at 0x1170d52b0>,
     <matplotlib.text.Text at 0x1171e02e8>]




![png](2017-01-25-flood03-precipitation-data-in-R_files/2017-01-25-flood03-precipitation-data-in-R_32_1.png)



```python
# ```{r challenge, echo=FALSE, warning="hide", fig.cap="precip plot subset 2" }



# # subset 2 months around flood

# precip_boulder_AugOct_2012 <- boulder_daily_precip %>%

#                         filter(DATE >= as.Date('2012-08-15') & DATE <= as.Date('2012-10-15'))



# # create new plot

# precPlot_flood_2012 <- ggplot(data=precip_boulder_AugOct_2012, aes(DATE,DAILY_PRECIP)) +

#   geom_bar(stat="identity") +

#   xlab("Date") + ylab("Precipitation (inches)") +

#   ggtitle("Daily Total Precipitation Aug - Oct 2012 for Boulder Creek") +

#   ylim(0,10)



# precPlot_flood_2012



# ```

```


```python

```
