---
layout: single
title: "Get to Know Python & Jupyter Notebooks"
excerpt: "This tutorial introduces the Python scientific programming language. It is
designed for someone who has not used Python before. We will work with precipitation and
stream discharge data for Boulder County."
authors: ['Chris Holdgraf', 'Leah Wasser', 'Data Carpentry']
category: [course-materials]
class-lesson: ['get-to-know-r']
permalink: /course-materials/earth-analytics-python/week-2/get-to-know-r/
nav-title: 'Get to Know Python'
dateCreated: 2016-12-13
modified: 2017-05-24
module-title: 'Get to Know Python'
module-nav-title: 'Get to Know Python'
module-description: 'This module introduces the Python scientific programming language.
We will work with precipitation and stream discharge data for Boulder County
to better understand the Python syntax, various data types and data import and plotting.'
module-type: 'class'
course: "earth-analytics-python"
week: 2
sidebar:
  nav:
author_profile: false
comments: true
order: 1
topics:
  reproducible-science-and-programming: ['Jupyter-notebooks']
---

{% include toc title="In This Lesson" icon="file-text" %}


In this tutorial, we will explore the basic syntax (structure) or the `R` programming
language. We will introduce assignment operators (`<-`, comments (`#`) and functions
as used in `R`.

<div class='notice--success' markdown="1">

## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives
At the end of this activity, you will be able to:

* Understand the basic concept of a function and be able to use a function in your code.
* Know how to use key operator commands in R (`<-`)

## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need

You need `R` and `RStudio` to complete this tutorial. Also you should have
an `earth-analytics` directory setup on your computer with a `/data`
directory with it.

* [How to Setup R / RStudio](/course-materials/earth-analytics/week-1/setup-r-rstudio/)
* [Setup your working directory](/course-materials/earth-analytics/week-1/setup-working-directory/)
* [Intro to the R & RStudio Interface](/course-materials/earth-analytics/week-1/intro-to-r-and-rstudio)

</div>

In the [previous module](/course-materials/earth-analytics/week-1/setup-r-rstudio), we
setup `RStudio` and `R` and got to know the `RStudio` interface.
We also created a basic
`Jupyter notebook` report using `Jupyter`. In this module, we will explore the basic
syntax of the `R` programming language. We will learn how to work with packages and
functions, how to work with vector objects in R and finally how to import data
into a pandas data.frame which is the `python` equivalent of a spreadsheet.

Let's start by looking at the code we used in the previous module. Here, we

1. Downloaded some data from figshare using the `urllib.request.urlretrieve` function which is a part of the urllib library that comes with python 3.x .
2. Imported the data into r using the `pd.read_csv` function
3. Plotted the data using the `.plot()` function (which is a part of the `pandas` library and utilizes matplotlib plotting)


```python
#import earthlab as et
import pandas as pd
import numpy as np
import urllib
import os
# i thought this won't work in all cases so we use plt.io??plt.ion()
%matplotlib inline


# be sure to set your working directory\n",
os.chdir("/Users/lewa8222/Documents/earth-analytics/")
os.getcwd()
```




    '/Users/lewa8222/Documents/earth-analytics'




```python
#db = et.EarthlabData()
# download file from Earth Lab figshare repository
urllib.request.urlretrieve(url='https://ndownloader.figshare.com/files/7010681', 
                           filename= 'data/boulder-precip.csv')
```




    ('data/boulder-precip.csv', <http.client.HTTPMessage at 0x11a91b550>)




```python
#path = db.get_data('week_02', name='boulder-precip.csv', zipfile=False, replace=True)
```


```python
# open data
data = pd.read_csv('data/boulder-precip.csv')
```

In python / pandas we can access 'columns' in our data using the syntax:

`['column-name-here']`

By adding .head() to the command we tell python to only return the first 6 rows of the DATE column. 


```python
# view the entire column (all rows) 
data['DATE'] 
```


```python
# view the first 6 rows of data in the DATE column
data['DATE'].head()
```




    0    2013-08-21
    1    2013-08-26
    2    2013-08-27
    3    2013-09-01
    4    2013-09-09
    Name: DATE, dtype: object




```python
# view first 6 lines of the entire data frame
data.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>DATE</th>
      <th>PRECIP</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>756</td>
      <td>2013-08-21</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>757</td>
      <td>2013-08-26</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>758</td>
      <td>2013-08-27</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>759</td>
      <td>2013-09-01</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>760</td>
      <td>2013-09-09</td>
      <td>0.1</td>
    </tr>
  </tbody>
</table>
</div>



We can view the structure or type of data in each column using the dtypes attribute. 
Notice below that our data have 2 columns. One is of type object and the other is a numeric type - float64. 




```python
# view the structure of the data 
data.dtypes
```




    DATE       object
    PRECIP    float64
    dtype: object



Finally, we can create a quick plot of the data using `.plot`. 


```python
data.plot(x='DATE', 
          y='PRECIP')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x11edf5630>




![png](../../../../../images/course-materials/earth-analytics//week-2/get-to-know-r/2017-01-25-R01-get-to-know-python_13_1.png)



```python


```

The code above, uses syntax that is unique the `Python` programming language.

Syntax represents the characters or commands that `Python` understands and associated
organization / format of the code including spacing and comments.

Let's break down the syntax of the code above, to better understand what it's doing.

## Intro to the Python Syntax

### Assignment operator =

First, notice the use of `=`. `=` is the assignment operator. It is similar to
the `<-` sign in `R`. The equals sign assigns values on the right to objects on the left. So, after executing `x = 3`, the
value of `x` is `3` (`x=3`). The arrow can be read as 3 **goes into** `x`.

In the example below, we assigned the data file that we read into Python named `boulder-precip.csv`
to the variable name `boulder_precip`. After you run the line of code below,
what happens in Python?


```python
data = pd.read_csv('data/boulder-precip.csv')
data
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>DATE</th>
      <th>PRECIP</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>756</td>
      <td>2013-08-21</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>757</td>
      <td>2013-08-26</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>758</td>
      <td>2013-08-27</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>759</td>
      <td>2013-09-01</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>760</td>
      <td>2013-09-09</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>761</td>
      <td>2013-09-10</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>762</td>
      <td>2013-09-11</td>
      <td>2.3</td>
    </tr>
    <tr>
      <th>7</th>
      <td>763</td>
      <td>2013-09-12</td>
      <td>9.8</td>
    </tr>
    <tr>
      <th>8</th>
      <td>764</td>
      <td>2013-09-13</td>
      <td>1.9</td>
    </tr>
    <tr>
      <th>9</th>
      <td>765</td>
      <td>2013-09-15</td>
      <td>1.4</td>
    </tr>
    <tr>
      <th>10</th>
      <td>766</td>
      <td>2013-09-16</td>
      <td>0.4</td>
    </tr>
    <tr>
      <th>11</th>
      <td>767</td>
      <td>2013-09-22</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>12</th>
      <td>768</td>
      <td>2013-09-23</td>
      <td>0.3</td>
    </tr>
    <tr>
      <th>13</th>
      <td>769</td>
      <td>2013-09-27</td>
      <td>0.3</td>
    </tr>
    <tr>
      <th>14</th>
      <td>770</td>
      <td>2013-09-28</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>15</th>
      <td>771</td>
      <td>2013-10-01</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>772</td>
      <td>2013-10-04</td>
      <td>0.9</td>
    </tr>
    <tr>
      <th>17</th>
      <td>773</td>
      <td>2013-10-11</td>
      <td>0.1</td>
    </tr>
  </tbody>
</table>
</div>




```python

```

<i class="fa fa-star"></i> **Data Tip:**  In Jupyter notebooks, typing <kbd>Esc</kbd> + <kbd>A</kbd> at the
same time will write add a new cell AFTER the cell that you're currently working in.  Similarly, typing <kbd>Esc</kbd> + <kbd>B</kbd> at the
same time will write add a new cell AFTER the cell that you're currently working in. Hint: B is for BEFORE and A is for AFTER.
{: .notice--success}


### Comments in Python (`#`)

Next, notice the use of the `#` sign in our code example above.
Use `#` sign is used to add comments to your code. A comment is a line of information
in your code that is not executed by R. Anything to the right of a `#` is ignored
by `Python`. Comments are a way for you
to DOCUMENT the steps of your code - both for yourself and for others who may
use your script.


```python
# this is a comment. Python will not try to run this line
# comments are useful when we want to document the steps in our code

```

### Functions and their arguments

Finally we have functions. Functions are "canned scripts" that automate a task
that may other take several lines of code that you have to type in.

For example:


```python
# calculate the square root of 16
np.sqrt(16)
```




    4.0




```python


```

In the example above, the `sqrt` function is built into `R` and takes the square
root of any number that you provide to it.

## Function Arguments

A function often has one or more inputs called *arguments*. In the example above,
the value 16 was the argument that we gave to the `sqrt()` function.
Below, we use the `.plot()` function which is a part of the `pandas` library.
`.plot()` needs two arguments to execute properly:

1. The value that you want to plot on the `x=` axis and
2. The value that you want to plot on the `y=` axis

note below that if we don't tell python what to plot on the x and y axis it tries to 
guess which variables to plot on which axis. This isn't quite what we want



```python
# what happens if we plot without any arguments?
data.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x111d168d0>




![png](../../../../../images/course-materials/earth-analytics//week-2/get-to-know-r/2017-01-25-R01-get-to-know-python_24_1.png)



```python
# what happens if we plot with the x and y arguments?
data.plot(x='DATE', 
         y='PRECIP')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x11ed75908>




![png](../../../../../images/course-materials/earth-analytics//week-2/get-to-know-r/2017-01-25-R01-get-to-know-python_25_1.png)


Functions return an output. Sometimes that output is a *figure* like the example
above. Sometimes it is a *value* or a set of values or even something else.

### Base functions vs. packages
There are a
set of functions that come with `Python 3.x` when you download it. These are called `base Python`
functions. Other functions are add-ons to base `Python`. These functions can be loaded by

1. Installing a particular library (using conda install library-name at the command line
2. Loading the library in our script using `import library as nickname` eg: import pandas as pd 

We can also write our own functions. We will learn how to write functions later in this course. 

### Functions that return values
The  `sqrt()` function is a numpy function. The input (the
argument) is a number, and the return value (the output)
is the square root of that number. Executing a function ('running it') is called
*calling* the function. An example of a function call is:

`b <- np.sqrt(a)`

Here, the value of `a` is given to the `np.sqrt()` function, the `np.sqrt()` function
calculates the square root, and returns the value which is then assigned to
variable `b`. This function is very simple, because it takes just one argument.


Let's run a function that can take multiple arguments: `np.round()`.


```python
np.round(3.14159)
```




    3.0




```python


```

Here, we've called `round()` with just one argument, `3.14159`, and it has
returned the value `3`.  That's because the default is to round to the nearest
whole number. If we want more digits we can see how to do that by getting
information about the `round` function.  We can use `args(round)` or look at the
help for this function using `?round`.

# what's the easiest way to get a function documentation in jupyter?
# what does the cell below do? is there a quick way to see all of the arguments available for a function and the methods /attributes available for an object?


```python
# np.round<tab>
```


```python


```





```python
# view documentation for the round() function in python
help(np.round)
```

    Help on function round_ in module numpy.core.fromnumeric:
    
    round_(a, decimals=0, out=None)
        Round an array to the given number of decimals.
        
        Refer to `around` for full documentation.
        
        See Also
        --------
        around : equivalent function
    


Note above that we see there is a **decimals** argument that we can add to our round function that will specify the number of decimal places that the function returns. If we specify decimals=3 then python will round the data to 3 decimal points. 

# why does 3 return so many decimal places??!! 2 works but nothing else


```python
# what does this argument value return?
np.round(3.23457457, 
         decimals=3)

```




    3.2349999999999999




```python
np.round(3.14159, 
         decimals=1)
```




    3.1000000000000001




```python
# ```{r, results='show', purl=FALSE}

# round(3.14159, digits=2)

# ```

```

If we provide the arguments in the exact same order as they are defined in the function documentation, then you don't have to explicetly call the argument name: 





```python
np.round(3.14159, 2)
```




    3.1400000000000001




```python
# but what happens here?
np.round(2, 3.14159)

```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    /Users/lewa8222/anaconda/lib/python3.6/site-packages/numpy/core/fromnumeric.py in _wrapfunc(obj, method, *args, **kwds)
         56     try:
    ---> 57         return getattr(obj, method)(*args, **kwds)
         58 


    AttributeError: 'int' object has no attribute 'round'

    
    During handling of the above exception, another exception occurred:


    TypeError                                 Traceback (most recent call last)

    <ipython-input-37-e54a09d8d9f3> in <module>()
    ----> 1 np.round(2, 3.14159)
    

    /Users/lewa8222/anaconda/lib/python3.6/site-packages/numpy/core/fromnumeric.py in round_(a, decimals, out)
       2781 
       2782     """
    -> 2783     return around(a, decimals=decimals, out=out)
       2784 
       2785 


    /Users/lewa8222/anaconda/lib/python3.6/site-packages/numpy/core/fromnumeric.py in around(a, decimals, out)
       2767 
       2768     """
    -> 2769     return _wrapfunc(a, 'round', decimals=decimals, out=out)
       2770 
       2771 


    /Users/lewa8222/anaconda/lib/python3.6/site-packages/numpy/core/fromnumeric.py in _wrapfunc(obj, method, *args, **kwds)
         65     # a downstream library like 'pandas'.
         66     except (AttributeError, TypeError):
    ---> 67         return _wrapit(obj, method, *args, **kwds)
         68 
         69 


    /Users/lewa8222/anaconda/lib/python3.6/site-packages/numpy/core/fromnumeric.py in _wrapit(obj, method, *args, **kwds)
         45     except AttributeError:
         46         wrap = None
    ---> 47     result = getattr(asarray(obj), method)(*args, **kwds)
         48     if wrap:
         49         if not isinstance(result, mu.ndarray):


    TypeError: integer argument expected, got float


Notice above python returned an error. At the very bottom of the error notice:
`TypeError: integer argument expected, got float`. Why do you think this happened?

Notice that we provided the arguments as follows:

`np.round(2, 3.14159)`

Python tried to round the value 2 to 3.14159 which is a decimal rather than an integer value. 

And we name the arguments, then we can switch their order:





```python
np.round(decimals=2, a=3.14159)
```




    3.1400000000000001




```python
# ```{r, results='show', purl=FALSE}

# round(digits=2, x=3.14159)

# ```

```

It's good practice to put the non-optional arguments (like the number you're
rounding) first in your function call, and to specify the names of all optional
arguments.  If you don't, someone reading your code might have to look up
definition of a function with unfamiliar arguments to understand what you're
doing.

## Get Information About A Function

If you need help with a specific function, let's say `barplot()`, you can type:


```python
import matplotlib.pyplot as plt
```


```python
plt.bar?
```


```python
# ```{r, eval=FALSE, purl=FALSE}

# ?barplot

# ```

```



If you just need to remind yourself of the names of the arguments, you can use:





```python
# plt.bar<tab>
```

<div class="notice--warning" markdown="1">

## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Optional challenge activity

Use the `RMarkdown` document that we created as homework for today's class. If
you don't have a document already, create a new one, naming it: "lastname-firstname-wk2.Rmd.
Add the code below in a code chunk. Edit the code that you just pasted into
your `.Rmd` document as follows

1. The plot isn't pretty. Let's fix the x and y labels.
Look up the arguments for the `qplot()` function using either args(qplot) OR `?qplot`
in the R console. Then fix the labels of your plot in your script.

HINT: google is your friend. Feel free to use it to help edit the code.

2. What other things can you modify to make the plot look prettier. Explore. Are
there things that you'd like to do that you can't?
</div>

# notice the code below needs to be the answer to the challenge above 
<!--


# load libraries 
library(ggplot2)

# download data from figshare
# note that we are downloaded the data into your
download.file(url = "https://ndownloader.figshare.com/files/7010681",
              destfile = "data/boulder-precip.csv")

# import data
boulder_precip <- read.csv(file="data/boulder-precip.csv")

# view first few rows of the data
head(boulder_precip)

# when we download the data we create a dataframe
# view each column of the data frame using it's name (or header)
boulder_precip$DATE

# view the precip column
boulder_precip$PRECIP

# q plot stands for quick plot. Let's use it to plot our data
qplot(x=boulder_precip$DATE,
      y=boulder_precip$PRECIP)

-->
