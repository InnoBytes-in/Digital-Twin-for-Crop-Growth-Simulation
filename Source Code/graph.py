import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Load the dataset
@st.cache_data
def load_data():
    file_path = '../summary_lettuce.csv'  # Adjust path as needed
    return pd.read_csv(file_path)

dataset = load_data()

# User-inputted values for day 15
user_input = {
    'Temperature_mean': 30.5,
    'Humidity_mean': 65.0,
    'pH Level_mean': 6.5,
    'TDS Value_mean': 610,
}

# Initialize a dictionary to store deviations
deviations = {attr: [0] * 14 for attr in user_input}

# Calculate deviations from day 15 to day 48 using user-inputted values
for day in range(15, 49):
    day_data = dataset[dataset['Growth Day'] == day]
    for attr in user_input:
        deviation = day_data[attr].mean() - user_input[attr]
        deviations[attr].append(deviation)

# Prepare data for plotting
days = list(range(1, 49))

# Streamlit UI
st.title('Attribute Deviations Dashboard')

# Select attribute to display
selected_attr = st.selectbox('Select Attribute', list(user_input.keys()))

# Create plot
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=days,
    y=deviations[selected_attr],
    mode='markers+lines',
    name=selected_attr,
    line=dict(color='blue', width=2),
    marker=dict(size=8)
))

fig.update_layout(
    title=f'Attribute Deviations: {selected_attr}',
    xaxis=dict(title='Growth Day'),
    yaxis=dict(title='Deviation from User Input'),
    showlegend=True
)

st.plotly_chart(fig)
