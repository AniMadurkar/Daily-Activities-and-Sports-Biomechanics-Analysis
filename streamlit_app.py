import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import plotly.express as px
import scipy.signal as sig

def main():
    # Use the full page instead of a narrow central column
    st.set_page_config(page_title="Biomechanics Analysis for Daily and Sports Activities", layout="wide")

    # Main option on top of sidebar
    st.title("Biomechanics Analysis for Daily and Sports Activities")
    
    # Set random seed
    RANDOM_SEED = 179

    @st.cache()
    def load_data(filename):
        """
        Loads in complete dataset after data_cleaning.py file.

        Args: 
            None
        Returns:
            sports_science = outputted complete sports_science dataset 
        """
        
        try:
            sports_science = pd.read_csv(f"{filename}.csv")
        except:
            sports_science = pd.read_csv(f"{filename}_subset.csv")

        return sports_science

    @st.cache()
    def sensor_codes_and_labels(sensors_codes, sensors_labels, unit_code):

        if sensor_selected == "Accelerometers":
            filtered_sensor_codes = [unit_code + x for x in sensors_codes if "acc" in x]
            filtered_sensor_labels = [x for x in sensors_labels if "Acc" in x]
        elif sensor_selected == "Gyroscopes":
            filtered_sensor_codes = [unit_code + x for x in sensors_codes if "gyro" in x]
            filtered_sensor_labels = [x for x in sensors_labels if "Vel" in x]
        elif sensor_selected == "Magnetometers":
            filtered_sensor_codes = [unit_code + x for x in sensors_codes if "mag" in x]
            filtered_sensor_labels = [x for x in sensors_labels if "Mag" in x]

        return filtered_sensor_codes, filtered_sensor_labels

    def sensor_linechart(df, filtered_sensor_codes, sensors_labels, unit_code):
        
        if unit_selected in ["Arms", "Legs"]:
            tick_stepsize = 4
            if ("LA" in unit_code) or ("LL" in unit_code):
                title = f"{sensor_selected} on Left {unit_selected} while {activity_selected}"
            elif ("RA" in unit_code) or ("RL" in unit_code):
                title = f"{sensor_selected} on Right {unit_selected} while {activity_selected}"
        else:
            tick_stepsize = 2
            title = f"{sensor_selected} on {unit_selected} while {activity_selected}"

        fig, axes = plt.subplots(3, 1, figsize=(12,12))
        plt.rcParams.update({"font.size": 12, "font.weight": "normal"})

        named_colors = ["tab:blue", "navy", "darkcyan"]

        for i, ax_i in enumerate(axes):

            df_prom_idx = sig.find_peaks(df[filtered_sensor_codes[i]], prominence=prominence_selected)[0]
            df_prom = df.iloc[df_prom_idx]

            ax_i = sns.lineplot(data=df, x=df.index, y=filtered_sensor_codes[i], 
                                color=named_colors[i], 
                                ax=ax_i)
            ax_i = sns.scatterplot(data=df_prom, x=df_prom.index, y=filtered_sensor_codes[i], 
                                    color="red", 
                                    ax=ax_i)

            ax_i.set(ylabel=sensors_labels[i])
            ax_i.spines['top'].set_visible(False)
            ax_i.spines['right'].set_visible(False)

        st.subheader(title)

        st.pyplot(fig)

    def sensor_3dplot(df, filtered_sensor_codes):

        x = [x for x in filtered_sensor_codes if 'x' in x][0]
        y = [x for x in filtered_sensor_codes if 'y' in x][0]
        z = [x for x in filtered_sensor_codes if 'z' in x][0]

        fig = px.scatter_3d(df, x=x, y=y, z=z, 
                            color=df.index, color_continuous_scale="Magma",
                            width=800, height=800)

        st.subheader(f"{sensor_selected} in 3D Space Over Time")

        st.plotly_chart(fig)

    def sensor_pearson_correlation(df, filtered_sensor_codes, unit_code):
        
        if ("LA" in unit_code) or ("LL" in unit_code):
            title = f"Pearson Correlation of Left {unit_selected} {sensor_selected}"
        elif ("RA" in unit_code) or ("RL" in unit_code):
            title = f"Pearson Correlation of Right {unit_selected} {sensor_selected}"
        else:        
            title = f"Pearson Correlation of {unit_selected} {sensor_selected}"

        fig, ax = plt.subplots(figsize=(12,16))
        plt.rcParams.update({"font.size": 12, "font.weight": "normal"})

        colormap = sns.diverging_palette(220, 10, as_cmap = True)

        ax = sns.heatmap(df.corr()[filtered_sensor_codes], 
                        cmap=colormap, cbar_kws={"shrink":.65}, annot=True, vmin=-1, vmax=1, linecolor="white", annot_kws={"fontsize":10})

        st.subheader(title)
        
        st.pyplot(fig)

    def sensor_distribution(df, filtered_sensor_codes, sensors_labels, unit_code):

        if ("LA" in unit_code) or ("LL" in unit_code):
            title = f"Distribution of Left {unit_selected} {sensor_selected}"
        elif ("RA" in unit_code) or ("RL" in unit_code):
            title = f"Distribution of Right {unit_selected} {sensor_selected}"
        else:        
            title = f"Distribution of {unit_selected} {sensor_selected}"

        fig, axes = plt.subplots(3, 1, figsize=(12,12))
        plt.rcParams.update({"font.size": 12, "font.weight": "normal"})

        named_colors = ["tab:blue", "navy", "darkcyan"]

        for i, ax_i in enumerate(axes):

            ax_i = sns.histplot(data=df, x=filtered_sensor_codes[i],
                                stat="density", kde=True, color=named_colors[i], 
                                ax=ax_i)

            ax_i.set(xlabel=sensors_labels[i])
            ax_i.spines['top'].set_visible(False)
            ax_i.spines['right'].set_visible(False)

        st.subheader(title)

        st.pyplot(fig)

    def motion_boxplots(df, filtered_sensor_code, filtered_sensor_label):

        fig, ax = plt.subplots(figsize=(30, 10))
        ax = sns.boxplot(data=df, x="activity_name", y=filtered_sensor_code)
        
        ax.set_xticklabels(list(df.activity_name.unique()), rotation=90)
        ax.set(ylabel=filtered_sensor_label)
        
        st.subheader(f"Boxplot Analysis of {filtered_sensor_label} Across Multiple Activities")
        st.pyplot(fig)

    data = load_data("sports_science_dataset")

    xyz = ["X", "Y", "Z"]
    motion = ["Acc", "Gyro", "Mag"]
    motion_labels = ["Acceleration", "Angular Velocity", "Magnetic Fields"]
    sensors_labels = [i + f' {j}' for j in motion_labels for i in xyz]
    sensors_codes = [i.lower() + j.lower() for j in motion for i in xyz]

    row1_1, row1_2 = st.columns((2, 3))

    with row1_1:

        person_selected = st.selectbox(
            "Select a person to begin:", 
            ("p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9"), 
            index=0,
            key="person"
        )
        dashboard_type = st.radio(
            "Select a desired dashboard type:",
            ("Exploratory Data Analysis", "Machine Learning"),
            index=0,
            key="dashboard"
        )

    with row1_2:

        st.write(
            """
        ##
        This dataset contains eight subjects (4 males, 4 females, between the ages of 20 and 30) that performed 19 activities for 5 minutes at the Bilkent University Sports Hall, 
        in the Electrical and Electronics Engineering Building and in a flat outdoor area on campus. The signal duration is 5 minutes for each activity for each subject. The subjects are asked to perform the activities 
        in their own style and were not restricted on how the activities should be performed so we are likely to find quite a bit of variation for the activities for each subject.         
        The segments provided are: T - Torso, LA & RA - Left Arm & Right Arm, LL & RL - Left Leg & Right Leg.
        The sensors used are: accelerometers, gyrometers, and magnometers in x, y, and z directions.

        Disclaimer: The streamlit dashboard that is deployed here is running only on 5% of the total dataset due to Github's large data file limitations. 
        Follow the steps in the Github readme to run the dashboard on the full dataset.
        """
        )

    if dashboard_type == 'Exploratory Data Analysis':
        row2_1, row2_2, row2_3, row2_4 = st.columns((1.25, 1.25, 1.25, 1.25))  

        with row2_1:
            activity_selected = st.selectbox(
                "Which activity would you like to analyze?", 
                ("Sitting", "Standing", "Lying on Back", "Lying on Right Side", "Ascending Stairs",
                "Descending Stairs", "Standing in an Elevator", "Moving in an Elevator", "Walking in a Parking Lot",
                "Walking on a Treadmill", 'Walking on a Treadmill with an Incline', 'Running on a Treadmill', "Exercising on a Stepper",
                "Exercising on a Cross Trainer", "Cycling on an Exercise Bike in a Horizontal Position", "Cycling on an Exercise Bike in a Vertical Position",
                "Rowing", "Jumping", "Playing Basketball"),
                index=0,
                key="activity"
            )         
        
        with row2_2:
            unit_selected = st.selectbox(
                "What body unit do you want to specify on?",
                ("Torso", "Arms", "Legs"),
                key="unit"
            )
        
        with row2_3:
            sensor_selected = st.selectbox(
                "Which sensors would you like to focus on?",
                ("Accelerometers", "Gyroscopes", "Magnetometers"),
                key="unit"
            )
        
        with row2_4:
            prominence_selected = st.slider(
                "Select the prominence to identify peaks:",
                min_value=0.0,
                max_value=20.0,
                value=0.01,
                key="prominence"
            )

        if unit_selected == "Torso":
            row3_1, row3_2 = st.columns((2.5, 2.5))

            filtered_subject_and_activity = data[(data["subject"]==person_selected) & (data["activity_name"]==activity_selected)]

            unit_code = "T_"
            filtered_sensor_codes, filtered_sensor_labels = sensor_codes_and_labels(sensors_codes, sensors_labels, unit_code)

            filtered_data = filtered_subject_and_activity[filtered_sensor_codes+["segment"]]

            with row3_1:
                sensor_linechart(filtered_data, filtered_sensor_codes, filtered_sensor_labels, unit_code)
                st.write("")
                st.write("")
                sensor_distribution(filtered_data, filtered_sensor_codes, filtered_sensor_labels, unit_code)
            
            with row3_2:
                sensor_3dplot(filtered_data, filtered_sensor_codes)
                st.write("")
                st.write("")
                sensor_pearson_correlation(filtered_subject_and_activity, filtered_sensor_codes, unit_code)

            row3_3, row3_4 = st.columns((2.5, 2.5))

            with row3_3:
                activity_multi = st.multiselect(
                    "Select what kinds of activities to measure together:",
                    list(data.activity_name.unique()),
                    default=list(data.activity_name.unique()),
                    key="activities"
                )

            with row3_4:
                sensor_selected2 = st.selectbox(
                    f"Select type of {sensor_selected} to analyze activities by:",
                    (f"X {sensor_selected}", f"Y {sensor_selected}", f"Z {sensor_selected}"),
                    index=0,
                    key="sensor_selected2"
                )            

            filtered_subject_multi_activities = data[(data["subject"]==person_selected) & (data["activity_name"].isin(activity_multi))]

            filtered_sensor_code = [x for x in filtered_sensor_codes if sensor_selected2[0].lower() in x][0]

            motion_boxplots(filtered_subject_multi_activities, filtered_sensor_code, sensor_selected2)

        else:
            row3_1, row3_2 = st.columns((2.5, 2.5))

            filtered_subject_and_activity = data[(data["subject"]==person_selected) & (data["activity_name"]==activity_selected)]

            if unit_selected == "Arms":
                with row3_1:            

                    unit_code = "LA_"
                    filtered_sensor_codes, filtered_sensor_labels = sensor_codes_and_labels(sensors_codes, sensors_labels, unit_code)
                    
                    filtered_data_left = filtered_subject_and_activity[filtered_sensor_codes+["segment"]]

                    sensor_linechart(filtered_data_left, filtered_sensor_codes, filtered_sensor_labels, unit_code)
                    st.write("")
                    st.write("")                    
                    sensor_3dplot(filtered_data_left, filtered_sensor_codes)
                    st.write("")
                    st.write("")
                    sensor_distribution(filtered_data_left, filtered_sensor_codes, filtered_sensor_labels, unit_code)
                    st.write("")
                    st.write("")
                    sensor_pearson_correlation(filtered_subject_and_activity, filtered_sensor_codes, unit_code)

                with row3_2:        

                    unit_code = "RA_"
                    filtered_sensor_codes, filtered_sensor_labels = sensor_codes_and_labels(sensors_codes, sensors_labels, unit_code)

                    filtered_data_right = filtered_subject_and_activity[filtered_sensor_codes+["segment"]]

                    sensor_linechart(filtered_data_right, filtered_sensor_codes, filtered_sensor_labels, unit_code)
                    st.write("")
                    st.write("")                    
                    sensor_3dplot(filtered_data_right, filtered_data_right)
                    st.write("")
                    st.write("")                    
                    sensor_distribution(filtered_data_right, filtered_sensor_codes, filtered_sensor_labels, unit_code)
                    st.write("")
                    st.write("")                    
                    sensor_pearson_correlation(filtered_subject_and_activity, filtered_sensor_codes, unit_code)

            elif unit_selected == "Legs":
                with row3_1:            

                    unit_code = "LL_"
                    filtered_sensor_codes, filtered_sensor_labels = sensor_codes_and_labels(sensors_codes, sensors_labels, unit_code)

                    filtered_data_left = filtered_subject_and_activity[filtered_sensor_codes+["segment"]]  

                    sensor_linechart(filtered_data_left, filtered_sensor_codes, filtered_sensor_labels, unit_code)
                    st.write("")
                    st.write("")                    
                    sensor_3dplot(filtered_data_left, filtered_sensor_codes)
                    st.write("")
                    st.write("")                    
                    sensor_distribution(filtered_data_left, filtered_sensor_codes, filtered_sensor_labels, unit_code)
                    st.write("")
                    st.write("")                    
                    sensor_pearson_correlation(filtered_subject_and_activity, filtered_sensor_codes, unit_code)

                with row3_2:            

                    unit_code = "RL_"
                    filtered_sensor_codes, filtered_sensor_labels = sensor_codes_and_labels(sensors_codes, sensors_labels, unit_code)

                    filtered_data_right = filtered_subject_and_activity[filtered_sensor_codes+["segment"]]       

                    sensor_linechart(filtered_data_right, filtered_sensor_codes, filtered_sensor_labels, unit_code)
                    st.write("")
                    st.write("")                    
                    sensor_3dplot(filtered_data_right, filtered_data_right)
                    st.write("")
                    st.write("")                    
                    sensor_distribution(filtered_data_right, filtered_sensor_codes, filtered_sensor_labels, unit_code)
                    st.write("")
                    st.write("")                    
                    sensor_pearson_correlation(filtered_subject_and_activity, filtered_sensor_codes, unit_code)

    elif dashboard_type == 'Machine Learning':
        st.write("In Progress...")

if __name__ == '__main__':
    main()