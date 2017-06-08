---
layout: single
authors: ['Leah Wasser', 'Software Carpentry']
category: [course-materials]
title: 'Install & setup Python 3.x and Jupyter Notebook on your laptop'
attribution: 'These materials were adapted from Software Carpentry materials by Earth Lab.'
excerpt: 'This tutorial walks you through downloading and installing Python and Jupyter Notebook on your computer.'
dateCreated: 2017-06-06
modified: 2017-06-06
module-title: 'Setup Python 3.x, Jupyter Notebook and Your Working Directory'
module-description: 'This module walks you through getting Python 3.x and Jupyter notebook setup on your
laptop. It also introduces file organization strategies.'
computes. module-type: 'homework'
nav-title: 'Setup Python'
module-nav-title: 'Install Anaconda Python'
module-type: 'homework'
week: 1
sidebar:
  nav:
course: 'earth-analytics'
class-lesson: ['setup-python-jupyter']
permalink: /course-materials/earth-analytics-python/week-1/setup-anaconda-python-distribution/
author_profile: false
comments: true
order: 1
---



{% include toc title="In This Lesson" icon="file-text" %}





##  Python / Jupyter notebook setup

In this tutorial, we will download and install the anaconda distribution of `Python` which
comes with `Jupyter notebooks` on your computer.



>The installation instructions below were adapted from
<a href="http://software-carpentry.org/" target="_blank"> Software Carpentry</a>.


<div class='notice--success' markdown="1">



## <i class="fa fa-graduation-cap" aria-hidden="true"></i> Learning Objectives

At the end of this activity, you will:
* Be able to download and install `R` and `Rstudio` on your laptop.

</div>



<a href="http://python.org">Python</a> is a popular language for
    research computing, and great for general-purpose programming as
    well.  Installing all of its research packages individually can be
    a bit difficult, so we recommend
    <a href="https://www.continuum.io/anaconda">Anaconda</a>,
an all-in-one installer.

### Python 3.x

Regardless of how you choose to install it,
      <strong>please make sure you install Python version 3.x</strong>
(e.g., 3.4 is fine).

### Python in Jupyter notebooks

We will teach Python using the IPython notebook, a programming environment
      that runs in a web browser. For this to work you will need a reasonably
      up-to-date browser. The current versions of the Chrome, Safari and
      Firefox browsers are all
      <a href="http://ipython.org/ipython-doc/2/install/install.html#browser-compatibility">supported</a>
      (some older browsers, including Internet Explorer version 9
and below, are not).


## Windows

<h4 id="python-windows">Windows</h4>
      <a href="https://www.youtube.com/watch?v=xxQ0mzZ8UvA">Video Tutorial</a>
      <ol>
        <li>Open <a href="http://continuum.io/downloads">http://continuum.io/downloads</a> with your web browser.</li>
        <li>Download the Python 3 installer for Windows.</li>
        <li>Install Python 3 using all of the defaults for installation <em>except</em> make sure to check <strong>Make Anaconda the default Python</strong>.</li>
</ol>


<h4 id="python-macosx">Mac OS X</h4>
      <a href="https://www.youtube.com/watch?v=TcSAln46u9U">Video Tutorial</a>
      <ol>
        <li>Open <a href="http://continuum.io/downloads">http://continuum.io/downloads</a> with your web browser.</li>
        <li>Download the Python 3 installer for OS X.</li>
        <li>Install Python 3 using all of the defaults for installation.</li>
</ol>


<h4 id="python-linux">Linux</h4>
      <ol>
        <li>Open <a href="http://continuum.io/downloads">http://continuum.io/downloads</a> with your web browser.</li>
        <li>Download the Python 3 installer for Linux.<br>
          (Installation requires using the shell. If you aren't
           comfortable doing the installation yourself
           stop here and request help at the workshop.)
        </li>
        <li>
          Open a terminal window.
        </li>
        <li>
          Type <pre>bash Anaconda3-</pre> and then press
          tab. The name of the file you just downloaded should
          appear. If it does not, navigate to the folder where you
          downloaded the file, for example with:
          <pre>cd Downloads</pre>
          Then, try again.
        </li>
        <li>
          Press enter. You will follow the text-only prompts. To move through
          the text, press the space key. Type <code>yes</code> and
          press enter to approve the license. Press enter to approve the
          default location for the files. Type <code>yes</code> and
          press enter to prepend Anaconda to your <code>PATH</code>
          (this makes the Anaconda distribution the default Python).
        </li>
        <li>
          Close the terminal window.
</ol>


Once `Python 3.x` and `Jupyter notebooks` are installed, launch the Anaconda navigator to make sure that it works
and there are no errors when you open it.
