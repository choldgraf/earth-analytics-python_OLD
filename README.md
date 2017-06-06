# earth-analytics-python
This is a collection of course material for the python version of
Earth Analytics.

# Build Jekyll Materials
This repository is designed to do two primary conversion steps. Both of
these are done with python scripts in the `scripts` folder.

1. **Convert RMarkdown files into Jupyter Notebooks.** Run
   `python rmarkdown_to_ntbk.py` from within the `scripts` folder
    to generate Jupyter Notebooks that are ready to be converted to python.
2. **Manually convert these Jupyter Notebooks into python code.**
   The notebooks created above will still contain R code. You should then
   go inside each notebook and replace the R code with the corresponding
   Python code.
3. **Convert the Python Jupyter Notebooks into Jekyll Markdown files.**
   Do this by running `python generate_posts.py` from within the `scripts`
   folder. This will generate Markdown files from the Jupyter Notebooks,
   using the metadata in the first cell as the header for each markdown
   file. It will also insert images into the `images` folder.

> **NOTE:** Step 3 will only be run on notebooks that either don't have
a corresponding Markdown post, or whose timestamp on the notebook is newer
than the timestamp on the corresponding markdown post.

# Installing the Jekyll Site
The following sections describe how to get the earth-analytics-python
course building on your computer.

## Set up your environment

We recommend installing geo-related dependencies with `conda-forge`. Follow
these steps to get your environment ready.

1. First, create a **fresh** python installation. If you're using the anaconda
   distribution (recommended) then first create a new anaconda environment:

    `conda create --name earth-analytics`

2. Activate your newly-created environment with:

    `source activate earth-analytics`

3. Next install the packages we'll need for the class. To do this we need to
   use the `conda-forge` channel within the anaconda install manager. This is
   because many of the earth-related packages require non-python libraries
   that are a pain to install by themselves. This should take care
   of the install for us:

   `conda install -c conda-forge geopandas rasterio pysal fiona contextily numpy matplotlib jupyter geopy osmnx`

4. Finally, restart your terminal so that newly-installed packages will
   get properly-linked.


## Clone the repo

Next clone this repository to your local machine. Do so by running:

```
# clone the repository, , make the site, and serve it.
git clone $(The repo's URL)

cd $(The repo you just cloned)
```

## Install all gems

Next we'll install the correct version of each gem specified in
the gem file. This lets us build the site with Jekyll.
First `cd` into the cloned directory and run `bundle install`:

```
cd <cloned-directory>
bundle install
```

## Run locally

To build the site locally with the specified gems, run the following
command:

```
# run jekyll site locally
bundle exec jekyll serve
```

You can view the site locally using http://localhost:4000 in your browser.
NOTE: if the config siteURL is not correct, the site won't build locally properly.

## Build Notes:

* the site requires jekyll flavored markdown. Be sure to specify that if you are knitting.
* in rmd files - be sure to specify fig.cap="text here" to add alt text to any code chunks that output a FIGURE.

## CSS

Currently, we are using `sass` for all css.
