# TravelScraper-MMT | Travel Data Scraper

## Overview

This repository contains a web scraping tool built with Selenium to extract hotel and flight data from MakeMyTrip.com. Follow the steps below to set up and run the scraper.

## Setup Instructions

## 1. Clone the Repository
### ---bash/terminal
git clone https://github.com/Parth-Gala/TravelScraper-MMT.git

## 2. Download and Set Up `chromedriver.exe`

Visit [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads) and download the version that aligns with your current Chrome version. Add the `chromedriver.exe` file to the root directory of the project.

## 3. Create a Plain `sample_hotel_dataset.csv` File

Create a CSV file with the following columns:

- `Hotel_Name`
- `Rating`
- `Rating Description`
- `Reviews`
- `Star Rating`
- `Location`
- `Nearest Landmark`
- `Distance to Landmark`
- `Price`
- `Tax`

## 4. Add CSV Path to the Code

Open the `hotel_scraper.py` file and locate the `CSV_PATH` variable. Update its value with the path to your `sample_hotel_dataset.csv` file.

### ---python
##### Example:
CSV_PATH = "path/to/TravelData.csv"

## 4. Run the Code

python hotel_scraper.py

**Note:**
Make sure to have the necessary dependencies installed. You can install them using:

### ---bash/terminal
- `pip install selenium`
- `pip install pygetwindow`

# Now you are ready to enjoy exploring the scraped travel data!

