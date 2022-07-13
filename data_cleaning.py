import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

if __name__ == "__main__":

    units_codes = ['T', 'RA', 'LA', 'RL', 'LL']
    sensors_codes = ['xacc', 'yacc', 'zacc', 'xgyro', 'ygyro', 'zgyro', 'xmag', 'ymag', 'zmag']

    data_columns = []

    for unit in units_codes:
        for sensor in sensors_codes:
            data_columns.append(unit + '_' + sensor)
    
    # ENTER PATH HERE
    path = ''

    # Getting all folders with data files in directory
    activity_folders = [f for f in listdir(path) if not isfile(join(path, f))]
    activities_codes = ['Sitting', 'Standing', 'Lying on Back', 'Lying on Right Side', 'Ascending Stairs',
                        'Descending Stairs', 'Standing in an Elevator', 'Moving in an Elevator', 'Walking in a Parking Lot',
                        'Walking on a Treadmill', 'Walking on a Treadmill with an Incline', 'Running on a Treadmill', 'Exercising on a Stepper',
                        'Exercising on a Cross Trainer', 'Cycling on an Exercise Bike in a Horizontal Position', 'Cycling on an Exercise Bike in a Vertical Position',
                        'Rowing', 'Jumping', 'Playing Basketball']
    activities_mapping = dict(zip(activity_folders, activities_codes))

    # Looping through folders to read in each respective file and creating dataframes for each activity
    activities = {}
    for activity in activity_folders:
        print(f"Activity: {activity}")
        # Getting all folders with data files in activity directory
        subject_folders = [f for f in listdir(f'{path}/{activity}') if not isfile(join(path, f))]
        
        # Looping through folders to read in each respective file and creating dataframes for each subject
        subjects = {}
        for subject in subject_folders:
            print(f"Activity: {activity}, Subject: {subject}")
            # Getting all data files in subject directory
            segment_files = [f for f in listdir(f'{path}/{activity}/{subject}')]
            
            # Looping through files to read in each respective file and creating dataframes for each segment
            segments = {}
            for segment in segment_files:
                print(f"Activity: {activity}, Subject: {subject}, Segment: {segment}...")
                segment_data = pd.read_csv(f'{path}/{activity}/{subject}/{segment}', names=data_columns)
                
                # Calculating second values
                # for col in segment_data.columns:
                #     segment_data[f'{col}_sec'] = segment_data[col].rolling(25, min_periods=1).mean()

                segment_data['segment'] = segment[:-4]
                segments[segment] = segment_data

            # Compiling the segments together for each subject
            all_segments = pd.concat(segments.values(), ignore_index=True)
            all_segments['subject'] = subject
            subjects[subject] = all_segments
        
        # Compiling the subjects together for each activity
        all_subjects = pd.concat(subjects.values(), ignore_index=True)
        all_subjects['activity'] = activity
        activities[activity] = all_subjects
        
    # Compiling all the data together to one dataframe
    complete_dataset = pd.concat(activities.values(), ignore_index=True)
    complete_dataset['activity_name']= complete_dataset['activity'].map(activities_mapping)

    # Writing file to disk
    print("Writing complete dataset to file...")
    complete_dataset.to_csv('sports_science_dataset.csv', index=False)
    print("Completed!")
