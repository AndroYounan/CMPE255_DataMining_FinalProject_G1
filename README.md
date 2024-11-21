# CMPE255 Final Project
Group 1: Ethan Yang, Andrew Younan, Andy Wu

# How to use

## File structure set up
The dataset is not included in the project files. Please visit [Yelp's dataset site](https://www.yelp.com/dataset) to download.
Once ready, your file structure should have at least the following files (optional files are omitted):

- LoadUtils.py
- Recommender.ipynb
- yelp_dataset
  - yelp_academic_dataset_business.json
  - yelp_academic_dataset_review.json

Once you have the necessary files, run Recommender.ipynb.

## Adjusting parameters
The value of `N_LINES` can be adjusted as needed to limit the amount of data that is read from the files.
Running the project on the full data takes very long (upwards of 15 minutes, depending on hardware).

The filter passed into `data_business = LoadUtils.load_matches(fn=...)` can be adjusted to switch which businesses are considered.
Currently, the data is limited to just open businesses within California.
Examples of filters can be found in the comments inside `LoadUtils.py`.

`optimal_k` can be adjusted to make a different number of clusters.
