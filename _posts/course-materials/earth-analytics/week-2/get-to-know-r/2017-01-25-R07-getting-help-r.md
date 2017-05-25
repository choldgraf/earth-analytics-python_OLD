---
layout: single
title: "Getting Help with R"
excerpt: "This tutorial covers ways to get help when you are stuck in R. "
authors: ['Data Carpentry', 'Leah Wasser']
category: [course-materials]
class-lesson: ['get-to-know-r']
permalink: /course-materials/earth-analytics-python/week-2/about-and-get-help-with-R/
nav-title: 'About R / Getting Help'
dateCreated: 2016-12-13
modified: 2017-05-24
week: 2
sidebar:
  nav:
author_profile: false
comments: true
order: 7
---



{% include toc title="In This Lesson" icon="file-text" %}



Getting help



<div class='notice--success' markdown="1">



## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives

At the end of this activity, you will be able to:



* List 2 ways that you can get help when you are stuck using R.

* List several features of R that makes it a versatile tool for scientific programming.



## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need



A computer with internet access.



</div>



## Basics of R



`R` is a versatile, open source programming/scripting language that's useful both

for statistics but also data science. Inspired by the programming language S.



* Free/Libre/Open Source Software under the [GPL version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).

* Superior (if not just comparable) to commercial alternatives. R has over 7,000

  user contributed packages at this time. It's widely used both in academia and

  industry.

* Available on all platforms.

* Not just for statistics, but also general purpose programming.

* For people who have experience in programmming: R is both an object-oriented

  and a so-called [functional language](http://adv-r.had.co.nz/Functional-programming.html).

* Large and growing community of peers.



## Seeking help



Below we discuss a few ways that you can get help when you are stuck in R.





## I know the name of the function I want to use, but I'm not sure how to use it



If you need help with a specific function, let's say `barplot()`, you can type:





```python
import matplotlib.pyplot as plt
plt.bar?
```


```python
# ```{r, eval=FALSE, purl=FALSE}

# ?barplot

# ```

```



When you use the `?barplot` in the R console, you asking R to look for the documentation

for the `barplot()` function.



If you just need to remind yourself of the names of the arguments that can be used

with the function, you can use:





```python
# plt.bar(<TAB>
```


```python
# ```{r, eval=FALSE, purl=FALSE}

# args(lm)

# ```

```



## I want to use a function that does X, there must be a function for it but I don't know which one...



If you are looking for a function to do a particular task, you can use

`help.search()` function, which is called by the double question mark `??`.

However, this only looks through the installed packages for help pages with a

match to your search request





```python
# This doesn't exist in python (to my knowledge)
```


```python
# ```{r, eval=FALSE, purl=FALSE}

# ??kruskal

# ```

```
