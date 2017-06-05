---
layout: single
title: "Objects and variables in Python"
excerpt: "This tutorial introduces the Python programming language. It is
designed for someone who has not used Python before. We will work with precipitation and
stream discharge data for Boulder County."
authors: ['Chris Holdgraf', 'Leah Wasser', 'Data Carpentry']
category: [course-materials]
class-lesson: ['get-to-know-python']
permalink: /course-materials/earth-analytics-python/week-2/objects-and-variables-in-python/
nav-title: 'Objects in Python'
dateCreated: 2017-05-23
modified: 2017-05-25
course: "earth-analytics-python"
week: 2
sidebar:
  nav:
author_profile: false
comments: true
order: 2
---

{% include toc title="In This Lesson" icon="file-text" %}


<div class='notice--success' markdown="1">

## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives
At the end of this activity, you will be able to:

* Be able to create, modify and use objects or variables in `Python`.
* Be able to define the key differences between the str (string) and num (number) classes in `Python` in terms of how R can or can not perform calculations with each.

## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need

You need R and RStudio to complete this tutorial. Also we recommend have you
have an `earth-analytics` directory setup on your computer with a `/data`
directory with it.

* [How to Setup R / R Studio](/course-materials/earth-analytics-python/week-1/setup-r-rstudio/)
* [Setup your working directory](/course-materials/earth-analytics-python/week-1/setup-working-directory/)

</div>


## Creating objects

You can get output from `Python` by typing a mathematical equation into the console -
For example, if you type in `3 + 5`, `R` will calculate the output value.


```python
# add 3 + 5
3 + 5
```




    8




```python
# divide 12 by 7
12 / 7
```




    1.7142857142857142



However, is it more useful to assign _values_ to _objects_. To create an object, we need to give it a name followed by the assignment operator `=`, and the value we want to give it:


```python
# assign weight_kg to the value of 55
weight_kg = 55

# view object value
weight_kg
```




    55



## Use Useful Object Names
# Be sure to fix the link below to reserved names for python if that exists...
Objects can be given any name such as `x`, `current_temperature`, or
`subject_id`. However, it is best to use clear and descriptive words when naming
objects to ensure your code is easy to follow.

We will discuss best practicing for coding in this module - in the [clean coding
lesson](/course-materials/earth-analytics-python/week-2/write-clean-code-with-r/).

1. **Keep object names short:** this makes them easier to read when scanning through code.
2. **Use meaningful names:** For example: `precip` is a more useful name that tells us something about the object compared to `x`
3. **Don't start names with numbers!** Objects that start with a number are NOT VALID in R.
4. **Avoid names that are existing functions in Python:** e.g.,
`if`, `else`, `for`, see
[here](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Reserved.html)

A few other notes about object names in `Python`:

* `R` is case sensitive (e.g., `weight_kg` is different from `Weight_kg`).
* Avoid other function names (e.g., `c`, `T`, `mean`, `data`, `df`, `weights`).
* Use nouns for variable names, and verbs for function names.
* Avoid using dots in object names - e.g. `my.dataset` - dots have a special meaning in R (for methods) and other programming languages. Instead use underscores `my_dataset`.

## View object value
When assigning a value to an object, `Python` does not print anything. You can force
it to print the value by using parentheses or by typing the name:


```python
weight_kg = 55  # Doesn't print anything 
weight_kg # putting it at the end of a cell will print whatever is in the final line of the cell

```




    55



Now that `Python` has `weight_kg` in memory, we can do arithmetic with it. For
instance, we may want to convert this weight in pounds (weight in pounds is 2.2
times the weight in kg):


```python
2.2 * weight_kg
```




    121.00000000000001





We can also change a variable's value by assigning it a new one:





```python
weight_kg = 57.6
2.2 * weight_kg
```




    126.72000000000001



This means that assigning a value to one variable does not change the values of
other variables.  For example, let's store the animal's weight in pounds in a new
variable, `weight_lb`:


```python
weight_lb = 2.2 * weight_kg
```



and then change `weight_kg` to 100.





```python
weight_kg = 100
```



What do you think is the current content of the object `weight_lb`? 126.5 or 200?



<div class="notice--warning" markdown="1">



## <i class="fa fa-pencil-square-o" aria-hidden="true"></i> Optional challenge activity



What are the values of each object defined in EACH LINE OF code below?





```python
mass = 47.5            # mass?
age  = 122             # age?
mass = mass * 2.0      # mass?
age  = age - 20        # age?
mass_index = mass / age  # mass_index?
```

<!-- Answers to go here... -->
