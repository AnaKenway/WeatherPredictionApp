# WeatherPredictionApp

This is a ML app done in Python. It predicts the weather for a desired period of time, based on the data collected from the Heating Plant.

The ML Model was created in Jupyter Notebook. The data was also merged and formatted with the help of Jupyter Notebook.
The user interacts with the app through a Streamlit Front End app. On the Back End is a Flask app.
For the Database, QuestDB is used. It stores the input data for a cerain time period.

The predictions are made based on the following data collected from the Heating Plant in Nis:  
**Tsp (°C):** Setpoint temperature (desired or target temperature).  
**Tsr (°C):** Temperature at a specific stage or location.  
**Pts (MW):** Power measurement in megawatts.  
**Pnt (MW):** Another power measurement in megawatts.  
**Tn (°C):** Temperature of incoming water or fluid.  
**Tp (°C):** Temperature of outgoing water or fluid.  
**Q (m³/h):** Volume flow rate of the water or fluid in cubic meters per hour.  
**E (MWh):** Energy consumption measured in megawatt-hours.

The weather conditions being predicted are the following:  
**Temperature (°C)**  
**Dew Point (°C)**  
**Humidity (%)**  
**Snow Depth (cm)**  
**Wind Speed ((km/h))**  
  
The user enters the desired time period for which they want the prediction to be made. The results are then displayed in a table view, ordered by time (predictions are hourly).

![image](https://github.com/AnaKenway/WeatherPredictionApp/assets/81249687/c7e23c85-a713-4d9d-ae93-988e22a2e6d3)
![image](https://github.com/AnaKenway/WeatherPredictionApp/assets/81249687/0d80f852-fc16-4be9-bc8c-6261bc5b2b03)
![image](https://github.com/AnaKenway/WeatherPredictionApp/assets/81249687/d79303d8-06ef-4ab6-909f-c787b9760f37)
