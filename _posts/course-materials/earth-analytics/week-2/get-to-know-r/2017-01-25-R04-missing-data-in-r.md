---
layout: single
title: "Missing data in R"
excerpt: "This tutorial introduces the concept of missing of no data values in R."
authors: ['Data Carpentry', 'Leah Wasser']
category: [course-materials]
class-lesson: ['get-to-know-r']
permalink: /course-materials/earth-analytics-python/week-2/missing-data-in-r-na/
nav-title: 'Missing data'
dateCreated: 2016-12-13
modified: 2017-05-24
week: 2
sidebar:
  nav:
author_profile: false
comments: true
order: 4
---



{% include toc title="In This Lesson" icon="file-text" %}



This lesson covers how to work with no data values in `R`.



<div class='notice--success' markdown="1">



## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives

At the end of this activity, you will be able to:



* Understand why it is important to make note of missing data values.

* Be able to define what a `NA` value is in `R` and how it is used in a vector.



## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need



You need R and RStudio to complete this tutorial. Also we recommend have you

have an `earth-analytics` directory setup on your computer with a `/data`

directory with it.



* [How to Setup R / R Studio](/course-materials/earth-analytics-python/week-1/setup-r-rstudio/)

* [Setup your working directory](/course-materials/earth-analytics-python/week-1/setup-working-directory/)





</div>



## Missing data - No Data Values



Sometimes, our data are missing values. Imagine a spreadsheet in Microsoft excel

with cells that are blank. If the cells are blank, we don't know for sure whether

those data weren't collected, or something someone forgot to fill in. To account

for data that are missing (not by mistake) we can put a value in those cells

that represents `no data`.



The `R` programming language uses the value `NA` to represent missing data values.





```python
import numpy as np
```


```python
planets = np.array(["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus",
                    "Neptune", np.nan])
```


```python
# ```{r no-data-values }



# planets <- c("Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus",

#              "Neptune", NA)



# ```

```



The default setting for most base functions that read data into `R` is to

interpret `NA` as a missing value.



## Customizing no data values



Sometimes, you'll find a dataset that uses another value for missing data. In some

disciplines, for example -999 is sometimes used. If there are multiple types of

missing values in your dataset, you can extend what `R` considers a missing value when it reads

the file in using  "`na.strings`" argument. For instance, if you wanted to read

in a `.CSV` file named `temperature_example.csv` that had missing values represented as an empty

cell, a single blank space, and the value -999, you would use:





```python
import earthlab as et
import pandas as pd
```


```python
path = et.download("https://ndownloader.figshare.com/files/7275959", 'temperature_example.csv',
                   '/Users/choldgraf/data_earthlab/week_02/')
```

    Replace is False and data exists, so doing nothing. Use replace==True to re-download the data.



```python
temp_df = pd.read_csv(path)
```


```python
temp_df2 = pd.read_csv(path, na_values=['NA', ' ', '-999'])
```


```python
# ```{r, read-na-values-custom }

# # download file

# download.file("https://ndownloader.figshare.com/files/7275959",

#               "data/week2/temperature_example.csv")



# # import data but don't specify no data values - what happens?

# temp_df <- read.csv(file = "data/week2/temperature_example.csv")



# # import data but specify no data values - what happens?

# temp_df2 <- read.csv(file = "data/week2/temperature_example.csv",

#                      na.strings = c("NA", " ", "-999"))



# ```

```



In the example below, note how a mean value is calculated differently depending

upon on how NA values are treated when the data are imported.







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
print(np.mean(temp_df['avg_temp'].dropna()))
print(np.mean(temp_df2['avg_temp'].dropna()))
```

    -231.54545454545453
    56.25



```python
# ```{r na-remove}



# mean(temp_df$avg_temp)

# mean(temp_df2$avg_temp)



# mean(temp_df$avg_temp, na.rm = TRUE)

# mean(temp_df2$avg_temp, na.rm = TRUE)

# ```

```



Notice a difference between `temp_df` and `temp_df2` ?



<div class="notice--warning" markdown="1">



## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Optional challenge



* **Question**: Why, in the the example above did mean(temp_df$avg_temp) return

a value of NA?



<!-- * _Answer_: Because if there are NA values in a dataset, R can not automatically

perform the calculation. you need to add a na.rm=TRUE to remove NA values. -->



* **Question**: Why, in the the example above did mean(temp_df$avg_temp, na.rm = TRUE)

also return a value of NA?



<!-- * _Answer_: Because we didn't remove NA values when we imported the first data.frame. thus

if there are NA values in a dataset, R can not automatically

perform the calculation even with using na.rm=TRUE because there are no NA values

in the data.frame . -->

</div>



When performing mathematical operations on numbers in `R`, most functions will

return the value `NA` if the data you are working with include missing values.

This allows you to see that you have missing data in your dataset. You can add the

argument `na.rm=TRUE` to calculate the result while ignoring the missing values.





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



The functions, `is.na()`, `na.omit()`, and `complete.cases()` are all useful for

figuring out if your data has assigned (`NA`) no-data values. See below for

examples.







```python
heights[~np.isnan(heights)]
```




    array([ 2.,  4.,  4.,  6.])




```python
# no "omit" function in python nor "complete cases"
```


```python
# ```{r, purl=FALSE}

# # Extract those elements which are not missing values.

# heights[!is.na(heights)]



# # Returns the object with incomplete cases removed. The returned object is atomic.

# na.omit(heights)



# # Extract those elements which are complete cases.

# heights[complete.cases(heights)]



# ```

```



<div class="notice--warning" markdown="1">



## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Challenge



* **Question**: Why does the following piece of code return a warning?





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
