# Daily Activities and Sports Biomechanics Analysis
As an avid sports fan and data/ML nerd, I love using my skills to analyze human performance for the purpose of physical therapy, performance enhancement, and activity optimization.

Unfortunately there aren't that many datasets out there that capture robust sensor data for a wide range of activities. This passion project analyzes one of the few reputed sources I could find. The dataset utilized here is from the UCI Machine Learning Repository: [Daily and Sports Activities Data Set](https://archive.ics.uci.edu/ml/datasets/daily+and+sports+activities#)

I venture to build a Streamlit dashboard that encompases relevant exploratory data analysis and machine learning for a variety of insights and objectives. I also plan to accompany a series on Medium to showcase what I built, found, and how others may join in on the fun.

DISCLAIMER: THIS PROJECT IS STILL IN PROGRESS.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Clone the Repository

Get a copy of this project by simply running the git clone command.

``` git
git clone https://github.com/AniMadurkar/Daily-Activities-and-Sports-Biomechanics-Analysis.git
```

### Prerequisites

Before running the project, we have to install all the dependencies from requirements.txt

``` pip
pip install -r requirements.txt
```

### Data Cleaning

Due to the volume of data files in the dataset, I don't include it here in the github but here's how you can run my data cleaning script to combine and clean the data to work with one csv in your local machine:

1. Download the data files from here: [Daily and Sports Activities Data Set](https://archive.ics.uci.edu/ml/datasets/daily+and+sports+activities#)

2. Download the data_cleaning.py script in this repo

3. Make sure the data cleaning scipt is at the same level as the data folder, like below:
-- /data
-- /data_cleaning.py

4. Change path variable where it says:
 ``` 
# ENTER PATH HERE TO DOWNLOADED DATA FOLDER
# Example: C:/Users/user1/Documents/Project Folder/data
path = ''
```

5. Run this in the terminal:
 ``` cmd
python data_cleaning.py
```

### Hosting

Last, get the project hosted on your local machine with a single command.

``` cmd
streamlit run streamlit_app.py
```

## Coming Soon...
Some intial ideas of what I'm hoping to build out in future versions. Ideas welcome!

Advanced Biometric Analysis
- Creating fatigue metric to identify when subject is getting tired/overextended

Unsupervised Learning
- Clustering accelerometer, gyrometer, and magnometer data to segment activities in high dimensional spaces
- Dimensionality reduction to investigate loading vectors

Supervised Learning
- Classification of activity/sport based on sensor readings
