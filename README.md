# Daily Activities and Sports Biomechanics Analysis

THIS PROJECT IS STILL IN PROGRESS.

As an avid sports fan and data/ML nerd, I love using my skills to analyze human performance for the purpose of physical therapy, performance enhancement, and activity optimization.

Unfortunately there aren't that many datasets out there that capture robust sensor data for a wide range of activities. This passion project analyzes one of the few reputed sources I could find. The dataset utilized here is from the UCI Machine Learning Repository: [Daily and Sports Activities Data Set](https://archive.ics.uci.edu/ml/datasets/daily+and+sports+activities#)

I venture to build a Streamlit dashboard that encompases relevant exploratory data analysis and machine learning for a variety of insights and objectives. I also plan to accompany a series on Medium to showcase what I built, found, and how others may join in on the fun.

- Link to Streamlit dashboard: https://animadurkar-daily-activities-and-sports-bi-streamlit-app-akeaba.streamlitapp.com/
- Link to DagsHub project to view modeling experiments: https://dagshub.com/AniMadurkar/sports-science

DISCLAIMER: The streamlit dashboard that is deployed here is running only on 5% of the total dataset due to Github's large data file limitations. Follow the steps below to run the dashboard on the full dataset.

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

3. Make sure the data cleaning scipt is at the same level as the data folder

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
Some intial ideas of what I'm hoping to build out in future iterations. Ideas welcome!

Advanced Biometric Analysis
- Creating fatigue metric to identify when subject is getting tired/overextended
- Density estimation with Bayesian modeling

Unsupervised Learning
- Clustering of peaks to segment form and technique
- Analysis write up of clustering results
- Building biplot to analyze loaded vectors after dimensionality reduction

Supervised Learning
- Experiment with more classification models to predict activity for each subject
- Model post prediction analysis write up (feature importances, ablation testing, etc.)
- Potential classification objectives based on new metrics constructed

General
- Document code more effectively
- Tweak streamlit dashboard design to be more user friendly
- Medium write up with analyses

Will be integrating this app with DagsHub as well to build in MLOps functionality.
