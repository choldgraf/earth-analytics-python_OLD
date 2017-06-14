---
layout: single
title: "Get Help with Python"
excerpt: "This tutorial covers ways to get help when you are stuck in Python. "
authors: ['Chris Holdgraf', 'Data Carpentry', 'Leah Wasser']
category: [course-materials]
class-lesson: ['write-clean-python-code']
course: 'earth-analytics-python'
permalink: /course-materials/earth-analytics-python/week-2/about-and-get-help-with-Python/
nav-title: 'About Python & Get Help'
dateCreated: 2017-05-05
modified: 2017-06-13
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

* List 2 ways that you can get help when you are stuck using Python.
* List several features of Python that makes it a versatile tool for scientific programming.

## <i class="fa fa-check-square-o fa-2" aria-hidden="true"></i> What you need

A computer with internet access.

</div>



## Basics of Python

`Python` is a versatile, open source programming/scripting language that's useful both
for statistics but also data science.

# Add some stats on python here...

* Free/Libre/Open Source Software under the [GPL version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
* Superior (if not just comparable) to commercial alternatives. R has over 7,000
  user contributed packages at this time. It's widely used both in academia and
  industry.
* Available on all platforms.
* Not just for statistics, but also general purpose programming.
* For people who have experience in programmming: Python is both an object-oriented

  and a so-called [functional language](http://adv-r.had.co.nz/Functional-programming.html).
* Large and growing community of peers.



## Seeking help

Below we discuss a few ways that you can get help when you are stuck in Python.

## I know the name of the function I want to use, but I'm not sure how to use it

If you need help with a specific function, let's say creating a barplot `.bar()`, you can type:



```python
import matplotlib.pyplot as plt
plt.bar?
```

When you type `plt.bar?` in the Python console, you are asking Python to look for the documentation
for the `.bar()` function.

If you just need to remind yourself of the names of the arguments that can be used
with the function, you can use the tab button as you type in the function name for help:

# is there a way to list all arguments for a function?



```python
# plt.bar(<TAB>
```
