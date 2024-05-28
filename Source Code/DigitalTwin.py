import streamlit as st
from streamlit_extras.colored_header import colored_header
# from streamlit_extras.switch_page_button import switch_page
import pandas as pd
from joblib import load
import os
import time
import plotly.graph_objs as go





dataset = pd.read_csv('summary_lettuce.csv')
# Load the model
model = load('random_forest_model.joblib')
a =True


@st.cache_data
def create_deviation_graph(deviation_data, selected_attr):
    fig = go.Figure()
    
    for day in range(1, 49):
        fig.add_trace(go.Scatter(
            x=list(range(1, day + 1)),
            y=[deviation_data[d][selected_attr] for d in range(1, day + 1)],
            mode='markers+lines',
            name=f'Day {day}',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))

    fig.update_layout(
        title=f'Attribute Deviations: {selected_attr}',
        xaxis=dict(title='Growth Day'),
        yaxis=dict(title='Deviation from User Input'),
        showlegend=False
    )

    # Add animation
    frames = [dict(data=[dict(x=list(range(1, day + 1)), 
                            y=[deviation_data[d][selected_attr] for d in range(1, day + 1)])],
                name=str(day)) for day in range(1, 49)]

    fig.frames = frames

    return fig

def find_conditions(growth_day):
    summary_data = pd.read_csv("summary_lettuce.csv")
    condition_row = summary_data[(summary_data["Growth Day"] == growth_day) & (summary_data["Condition"] == "Good")]
    if not condition_row.empty:
        min_temp = condition_row.iloc[0]["Temperature_min"]
        mean_temp = condition_row.iloc[0]["Temperature_mean"]
        max_temp = condition_row.iloc[0]["Temperature_max"]
        min_humidity = condition_row.iloc[0]["Humidity_min"]
        mean_humidity = condition_row.iloc[0]["Humidity_mean"]
        max_humidity = condition_row.iloc[0]["Humidity_max"]
        min_ph = condition_row.iloc[0]["pH Level_min"]
        mean_ph = condition_row.iloc[0]["pH Level_mean"]
        max_ph = condition_row.iloc[0]["pH Level_max"]
        min_tds = condition_row.iloc[0]["TDS Value_min"]
        mean_tds = condition_row.iloc[0]["TDS Value_mean"]
        max_tds = condition_row.iloc[0]["TDS Value_max"]
        return min_temp, mean_temp, max_temp, min_humidity, mean_humidity, max_humidity, min_ph, mean_ph, max_ph, min_tds, mean_tds, max_tds




def main():
    st.set_page_config(
        page_title="Plantify",
        page_icon="🍃",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("Welcome to Lettuce Tales")

    colored_header(
        label="",
        description="",
        color_name="green-90",
    )

    st.subheader(
        "Your Digital Twin Guide: Nurturing Healthy Lettuce Growth through Data Insights"
    )
    st.text("\n")
    st.text("\n")
    st.write("Plantify is a revolutionary digital garden laboratory designed to make your life easier and promote eco-friendly practices. We believe in virtually stimulating plant growth under diverse environmental conditions.")
    st.markdown("---")

    # Create inputs for new data
    st.sidebar.title("Plantify - A Digital Journey ")
    st.sidebar.header("Enter your plant growth day")
    growth_day = st.sidebar.number_input("Growth Day", min_value=1, max_value=48)
    st.sidebar.header("Enter your environmental condition")
    temperature_mean = st.sidebar.number_input("Mean Temperature")
    humidity_mean = st.sidebar.number_input("Mean Humidity")
    ph_mean = st.sidebar.number_input("Mean pH Level")
    tds_mean = st.sidebar.number_input("Mean TDS Value")

    # Create a DataFrame from the input data
    new_data = pd.DataFrame({
        'Growth Day': [growth_day],
        'Temperature_mean': [temperature_mean],
        'Humidity_mean': [humidity_mean],
        'pH Level_mean': [ph_mean],
        'TDS Value_mean': [tds_mean],
    })

    # Make predictions
    # if st.sidebar.button("Predict"):
    prediction = model.predict(new_data)

    # Display predictions
    st.text("\n")
    st.text("\n")
    st.subheader("Discover What's your Plant's condition")
    col1, col2 = st.columns(2)
    with col1:
        if prediction[0] == 'Bad':
            st.warning(f"WARNING ! WARNING ! The plant's health might deteriorate over a period of time.")
        else:
            st.success(f"The plant health is in a good condition. Still check the optimal factors.")

        conditions = find_conditions(growth_day)
        if conditions:
            min_temp, mean_temp, max_temp, min_humidity, mean_humidity, max_humidity, min_ph, mean_ph, max_ph, min_tds, mean_tds, max_tds = conditions
            st.text("\n")
            st.text("\n")
            st.markdown(f"<span style='font-size:20px;'>*Valid Conditions for Growth Day {growth_day}*</span>", unsafe_allow_html=True)

            with st.expander("Whats's optimal temperature?", expanded=False):
                st.text(f"Your deviation : {mean_temp - temperature_mean}")
                st.text(f"Minimum Temperature: {min_temp} °C")
                st.text(f"Maximum Temperature: {max_temp} °C")
            st.markdown("---")

            with st.expander("Whats's optimal humidity?", expanded=False):
                st.text(f"Your deviation : {mean_humidity - humidity_mean}")
                st.text(f"Minimum Humidity: {min_humidity} %")
                st.text(f"Maximum Humidity: {max_humidity} %")
            st.markdown("---")

            with st.expander("Whats's optimal pH Level?", expanded=False):
                st.text(f"Your deviation : {mean_ph - ph_mean}")
                st.text(f"Minimum pH Level: {min_ph}")
                st.text(f"Maximum pH Level: {max_ph}")
            st.markdown("---")

            with st.expander("Whats's optimal TDS Value?", expanded=False):
                st.text(f"Your deviation : {mean_tds - tds_mean}")
                st.text(f"Minimum TDS Value: {min_tds} ppm")
                st.text(f"Maximum TDS Value: {max_tds} ppm")
            st.markdown("---")

    with col2:
        st.info("Your optimal digital plant")
        image_path = os.path.join("bg_remove/", f"{growth_day}.png")
        if os.path.exists(image_path):
            st.image(image_path, caption=f"Virtual Plant for Growth Day {growth_day}",
                        output_format='auto')
        else:
            st.write("Image not found for this growth day.")
    
    # st.markdown("----")
    colored_header(
                label="",
                description="",
                color_name="green-90",
            )
    
    st.text("\n")
    st.text("\n")
    st.text("\n") 
        
    st.error("Know how your plant's deviation ")
    user_input_day = {
        'Temperature_mean': temperature_mean,
        'Humidity_mean': humidity_mean,
        'pH Level_mean': ph_mean,
        'TDS Value_mean': tds_mean
    }
    
    deviations = {attr: [0] * (growth_day - 1) for attr in user_input_day}
            
        # Calculate deviations from day to day 48 using user-inputted values
    for day in range(growth_day, 49):
        day_data = dataset[dataset['Growth Day'] == day]
        for attr in user_input_day:
            deviation = day_data[attr].mean() - user_input_day[attr]
            deviations[attr].append(deviation)
            
    # Prepare data for plotting
    days = list(range(1, 49))
    deviation_data = {day: {attr: deviations[attr][day-1] for attr in deviations} for day in days}

    # Select attribute to display
    selected_attr = st.selectbox('Select Attribute', list(user_input_day.keys()))

    # Create animated plot
    # fig = go.Figure()
    
    fig = create_deviation_graph(deviation_data, selected_attr)
    st.plotly_chart(fig)
    
        # for day in range(1, 49):
        #     fig.add_trace(go.Scatter(
        #         x=list(range(1, day + 1)),
        #         y=[deviation_data[d][selected_attr] for d in range(1, day + 1)],
        #         mode='markers+lines',
        #         name=f'Day {day}',
        #         line=dict(color='blue', width=2),
        #         marker=dict(size=8)
        #     ))

        # fig.update_layout(
        #     title=f'Attribute Deviations: {selected_attr}',
        #     xaxis=dict(title='Growth Day'),
        #     yaxis=dict(title='Deviation from User Input'),
        #     showlegend=False
        # )

        # # Add animation
        # frames = [dict(data=[dict(x=list(range(1, day + 1)), 
        #                         y=[deviation_data[d][selected_attr] for d in range(1, day + 1)])],
        #             name=str(day)) for day in range(1, 49)]

        # fig.frames = frames

        # st.plotly_chart(fig)
        
        
        
    
    
    
    colored_header(
                label="",
                description="",
                color_name="green-90",
            )
    
    st.text("\n")
    st.text("\n")
    st.text("\n") 
    
    a = st.button("Want to see your plant's digital journey ? Click here !")
    
    if a :
        # Sample dataset (replace with your own dataset)
        sample_data = pd.read_csv("lettuce_dataset.csv")

        def automatic_image_display_page(starting_growth_day):

            # Placeholder for the image and parameters
            image_placeholder = st.empty()
            parameters_placeholder_gd = st.empty()
            parameters_placeholder_temp = st.empty()
            parameters_placeholder_hum= st.empty()
            parameters_placeholder_tds= st.empty()
            parameters_placeholder_ph = st.empty()
            
            rerun_button = st.button("Exit", key=f"rerun_button_{time.time()}")
            
            index = sample_data.index[sample_data['Growth Day'] == growth_day].tolist()[0]

            # Loop until the end of the dataset or until Rerun button is clicked
            while index < len(sample_data) and not rerun_button:
                display_data(image_placeholder, parameters_placeholder_gd, parameters_placeholder_temp, parameters_placeholder_hum, parameters_placeholder_tds, parameters_placeholder_ph, sample_data.iloc[index])
                time.sleep(0.7)
                index += 1

            if rerun_button:
                automatic_image_display_page(growth_day)

        def display_data(image_placeholder, parameters_placeholder_gd, parameters_placeholder_temp, parameters_placeholder_hum, parameters_placeholder_tds, parameters_placeholder_ph, row):
            parameters_placeholder_gd.empty()
            parameters_placeholder_gd.write(f"#### Growth Day: {row['Growth Day']}")
            parameters_placeholder_temp.write(f"Temperature: {row['Temperature']}")
            parameters_placeholder_hum.write(f"Humidity: {row['Humidity']}")
            parameters_placeholder_tds.write(f"TDS Value: {row['TDS Value']}")
            parameters_placeholder_ph.write(f"pH Level: {row['pH Level']}")
            image_placeholder.image(f"./bg_remove/{row['Growth Day']}.png")


        automatic_image_display_page(growth_day)

        
        
        
                

    


            
            
            
    st.text("\n")
    st.text("\n")                   
    st.text("\n")
    st.text("\n")
    st.text("\n")
    st.text("\n")
    st.info("Plant It Right: Empowering Eco-Friendly Choices at Your Fingertips.")

if __name__ == "__main__":
    main()
