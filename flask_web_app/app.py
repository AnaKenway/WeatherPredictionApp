from flask import Flask, render_template, request
import joblib
import pandas as pd
import http.client
from io import StringIO
from datetime import datetime, timezone
import urllib.parse
import json

app = Flask(__name__)

# Load your trained model
model = joblib.load('weather-prediction-model.pkl')

# Define route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define route for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get user input for the desired time period, that was sent in the Request Form
    # The Streamlit app gets the user input and sends it this way
    start_date_str = request.form.get('start_date_str')
    end_date_str = request.form.get('end_date_str')

    # Adjust the parsing for datetime-local format
    start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')

    # Convert timestamps to UTC
    start_date_utc = start_date.replace(tzinfo=timezone.utc)
    end_date_utc = end_date.replace(tzinfo=timezone.utc)

    # Format the dates as ISO 8601 strings
    start_date_iso = start_date_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    end_date_iso = end_date_utc.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Retrieve data from QuestDB for the desired time period
    conn = http.client.HTTPConnection("localhost", 9000)  # Assuming QuestDB is running on localhost:9000

    # Construct the URL with encoded query parameters
    query_params = {
        'query': f"SELECT * FROM input_data WHERE Time BETWEEN '{start_date_iso}' AND '{end_date_iso}'"
    }
    encoded_query = urllib.parse.urlencode(query_params)
    url = f"/exec?{encoded_query}"

    conn.request("GET", url)
    response = conn.getresponse()
    response_data = response.read().decode('utf-8')
    conn.close()

    # Convert the response data to a JSON object
    data = json.loads(response_data)

    # Access the dataset
    dataset = data['dataset']
    columns = data['columns']

    # Create DataFrame from the dataset
    df = pd.DataFrame(dataset, columns=[col['name'] for col in columns])
    df['Time'] = pd.to_datetime(df['Time'])  # Convert the 'Time' column to datetime

    # Make Predictions
    future_timestamps = pd.date_range(start=start_date_iso, end=end_date_iso, freq='h')
    future_data = df.copy()  # Use the retrieved data from QuestDB

    # Assuming X_train contains historical features and y_train contains the target variable
    future_predictions = model.predict(future_data[['Tsp', 'Tsr', 'Pts', 'Pnt', 'Tn', 'Tp', 'Q', 'E']])

    # List of the target variables
    response_columns = ['Temperature','Dew','Humidity','Snow Depth','Wind Speed']

    # Return predictions as JSON
    return {'predictions': future_predictions.tolist(),'future_timestamps': future_timestamps.tolist(),'columns':response_columns}

if __name__ == '__main__':
    app.run(debug=True)
