import streamlit as st
import requests
import pandas as pd

st.title("Weather Prediction App")

# User input for time period
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# Make a request to your Flask API for predictions
if st.button("Get Predictions"):
    # Convert the selected dates to the required format
    start_date_str = start_date.strftime('%Y-%m-%dT%H:%M')
    end_date_str = end_date.strftime('%Y-%m-%dT%H:%M')

    # Make a request to your Flask API
    payload = {
        'start_date_str': start_date_str,
        'end_date_str': end_date_str,
    }
    response = requests.post('http://localhost:5000/predict', data=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        predictions = result['predictions']
        future_timestamps = result['future_timestamps']
        columns = result['columns']

        # Format the predictions, split them
        #predictions_list = list(map(float, predictions.split(',')))

        # Create DataFrame
        df = pd.DataFrame(predictions, columns=columns)
        df['Time'] = pd.to_datetime(future_timestamps)

        # Set timestamp as index
        df.set_index('Time', inplace=True)

        # Streamlit app
        st.title('Weather Predictions')

        # Display the formatted table
        st.table(df)

    else:
        st.error("Error fetching predictions. Please check your input and try again.")
