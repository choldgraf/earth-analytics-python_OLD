---
layout: single
title: "About arrays in python and data types including strings, numbers and logicals - Data Science for scientists 101"
excerpt: "This tutorial introduces numpy arrays in Python. It also introduces the differences between strings, numbers and logical or boolean values (True / False) in Python."
authors: ['Chris Holdgraf', 'Data Carpentry', 'Leah Wasser']
category: [course-materials]
class-lesson: ['get-to-know-python']
course: "earth-analytics-python"
permalink: /course-materials/earth-analytics-python/week-2/work-with-data-types-python/
nav-title: 'Numpy arrays'
dateCreated: 2017-05-23
modified: 2017-06-06
week: 2
sidebar:
  nav:
author_profile: false
comments: true
order: 3
---


{% include toc title="In This Lesson" icon="file-text" %}


<div class='notice--success' markdown="1">

## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives
At the end of this activity, you will be able to:

* Understand the structure of and be able to create a vector object in Python.

## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need

You need the anaconda distribution of Python 3.x and Jupyter Notebooks to complete this tutorial. Also we recommend have you
have an `earth-analytics` directory setup on your computer with a `/data`
directory with it.

# need to fix these links to be python...
* [How to Setup R / R Studio](/course-materials/earth-analytics/week-1/setup-r-rstudio/)
* [Setup your working directory](/course-materials/earth-analytics/week-1/setup-working-directory/)


</div>

To begin working with arrays in `python` we will first load the `numpy` library. 


```python
import numpy as np
```

## Numpy arrays and data types

An array is a common data structure used in `python`. An array is defined as a
group of values, which most often are either numbers or characters. You can
assign this list of values to an object or variable, just like you
can for a single value. For example we can create a vector of animal weights:


```python
weight_g = np.array([50, 60, 65, 82])
weight_g
```




    array([50, 60, 65, 82])



An array can also contain characters:


```python
animals = np.array(['mouse', 'rat', 'dog'])
animals
```




    array(['mouse', 'rat', 'dog'], 
          dtype='<U5')



There are many functions that allow you to inspect the content and structure of an
array. For instance, `len()` (short for **len**gth) tells you how many elements are in a particular vector:


```python
len(weight_g)
```




    4




```python
len(animals)
```




    3



## Array data types

An important feature of an array, is that all of the elements are the same data
type. The attribute `.dtype` shows us the the data type stored within an array:


```python
weight_g.dtype
```




    dtype('int64')




```python
animals.dtype
```




    dtype('<U5')



The function `type()` shows us the **structure** of the object. 


```python
# View the python object type
type(weight_g)
```




    numpy.ndarray



You can add elements to an array using the `.hstack()` function. 
Below, we add the value 90 to the end of the `weight_g` object.


```python
# add the number 90 to the end of the vector
weight_g = np.hstack([weight_g, 90])
```


```python
# add the number 30 to the beginning of the vector
weight_g = np.hstack([30, weight_g])
```


```python
weight_g
```




    array([30, 50, 60, 65, 82, 90])



In the examples above, we saw 2 of the 6 **data** types that `Python` uses:

1. `"character"` and
2. `"numeric"`.

These are the basic data tpes that all `R` objects are built
from. The other 4 are:

* `"logical"` for `TRUE` and `FALSE` (the boolean data type)
* `"integer"` for integer numbers (e.g., `2L`, the `L` indicates to R that it's an integer)
* `"complex"` to represent complex numbers with real and imaginary parts (e.g.,
  `1+4i`) and that's all we're going to say about them
* `"raw"` that we won't discuss further


## Data type vs. data structure

Vectors are one of the many **data structures** that `R` uses. Other important
ones include: lists (`list`), matrices (`matrix`), data frames (`data.frame`) and
factors (`factor`). We will look at `data.frames` when we open our `boulder_precip`
data in the next lesson!


<div class="notice--warning" markdown="1">

## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Optional challenge activity

* **Question**: What happens when we create a vector that contains both numbers
and character values? Give it a try and write down the answer.

<!-- * _Answer_: R implicitly converts them to all be the same type -->


* **Question**: What will happen in each of these examples? (hint: use `class()`
  to check the data type of your objects):


```python
num_char <- c(1, 2, 3, 'a')
num_logical <- c(1, 2, 3, '2.45')
char_logical <- c('a', 'b', 'c', frog)
tricky <- c(1, 2, 3, '4')
```

* **Question**: Why do you think it happens?

<!-- * _Answer_: Vectors can be of only one data type. Python tries to convert (=coerce)
  the content of this vector to find a "common denominator". -->

* **Question**: Can you draw a diagram that represents the hierarchy of the data
  types?

<!-- * _Answer_: `logical -> numeric -> character <-- logical` -->

</div>


```python
num_char = np.array([1, 2, 3, 'a'])

num_logical = np.array([1, 2, 3, True])

char_logical = np.array(['a', 'b', 'c', True])

tricky = np.array([1, 2, 3, '4'])
```

## Subset arrays

If we want to extract one or several values from a vector, we must provide one
or several indices in square brackets. For instance:


```python
animals = np.array(["mouse", "rat", "dog", "cat"])
animals[2]

```




    'dog'




```python
animals[[2, 3]]
```




    array(['dog', 'cat'], 
          dtype='<U5')



<i fa fa-star></i>**Data Tip:** R indexes start at 1. Programming languages like
Fortran, MATLAB, and R start counting at 1, because that's what human beings typically do. Languages in the C
family (including C++, Java, Perl, and Python) count from 0 because that's 
simpler for computers to do.
{: .notice }

# ChrisH Note: this is a big oversimplification of 0 vs. 1 based indexing. :-)

## Subset arrays

We can subset arrays too. For instance, if you want to select only the
values that are greater than 50:


```python
weight_g > 50
```




    array([False, False,  True,  True,  True,  True], dtype=bool)



Notice that the command above returns a BOOLEAN (TRUE / FALSE) array. We can then use 
that array to select all objects in our weight_g array that are greater than 50 as follows:



```python
# select only the values greater than 50
weight_g[weight_g > 50]
```




    array([60, 65, 82])



You can combine multiple tests using `&` (both conditions are true, AND) or `|`
(at least one of the conditions is true, OR):



```python
# select objects that are EITHER less than 30 OR greater than 50
weight_g[(weight_g < 30) | (weight_g > 50)]
```




    array([60, 65, 82])




```python
# select objects that are greater than or equal to 30 OR equal to 21
weight_g[(weight_g >= 30) & (weight_g == 21)]
```




    array([], dtype=int64)






Notice that we use two `==` signs to designate `equal to` so as not to confuse equals to with the assignment operator which is also `=` in Python.

When working with vectors of characters, if you are trying to combine many
conditions it can become tedious to type. 


```python
animals = np.array(['mouse', 'rat', 'dog', 'cat'])
animals[(animals == 'cat') | (animals == 'rat')]
```




    array(['rat', 'cat'], 
          dtype='<U5')



The function `intersection()` allows you to test
if a value is found in an array of values:



```python
# select objects in the animals array that are within the array [`rat`, `cat`, `dog`, `duck`]
set(animals).intersection(set(['rat', 'cat', 'dog', 'duck']))
```




    {'cat', 'dog', 'rat'}



# chris is the example below just another way of doing what you did above?


```python
animal_bool = [animal in animals for animal in ['rat', 'cat', 'dog', 'duck']]
animals[animal_bool]
```




    array(['mouse', 'rat', 'dog'], 
          dtype='<U5')




<div class="notice--warning" markdown="1">

## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Optional challenge

* Can you figure out why `"four" > "five"` returns `TRUE`?

</div>

## Answers

<!-- When using ">" or "<" on strings, R compares their alphabetical order. Here "four" comes after "five", and therefore is "greater than" it. -->
