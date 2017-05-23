# earth-analytics-python
Space where we convert earth analytics class in R to  python

# Installation

We recommend installing geo-related dependencies with `conda-forge`. Use the following command on a **fresh** python installation:

`conda install -c conda-forge geopandas rasterio pysal`
# note that We may recommend not using conda forge -- needs more testing
 
## 1. Clone the repo
```
# clone the repository, , make the site, and serve it.
git clone $(The repo's URL)
cd $(The repo you just cloned)
```

## 2. Install all gems

```
# install the correct version of each gem specified in the gem file. Run this IN the cloned directory
bundle install
```

# 3. Run locally
## To build the site locally with the specified gems

You can view the site locally using http://localhost:4000 in your browser.
NOTE: if the config BASEURL is not correct, the site won't build locally properly.

```
# run jekyll site locally
bundle exec jekyll serve
```


## Build Notes:

* the site requires jekyll flavored markdown. Be sure to specify that if you are knitting.
* in rmd files - be sure to specify fig.cap="text here" to add alt text to any code chunks that output a FIGURE.

## CSS

Currently, we are using less. to install less

1. install nodejs (npm) https://nodejs.org/en/
2. install less : `sudo npm install less -g` NOTE: you need administration access to install 

