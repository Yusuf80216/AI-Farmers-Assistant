import streamlit as st
from PIL import Image
import requests
# from decouple import config

# my_url = config("API_URL")
my_url = st.secrets["API_KEY"]

def disease_detector():
    uploaded_file = st.file_uploader("Please upload a crop image")

    if uploaded_file is not None:
        leaf = Image.open(uploaded_file)
        st.image(leaf, caption='Your uploaded image', width=200)
        if st.button("Analyze Leaf"):
            files = {'file': uploaded_file.getvalue()}
            response = requests.post(f"{my_url}/leafpredict", files=files)
            print(response.status_code)
            if response.status_code == 200:
                prediction = response.text
                st.markdown("### PREDICTION")
                st.success(prediction)
            else:
                st.write("Error making request to API")

def crop_predictor():
    form = st.form(key="CROP")
    c1, c2 = st.columns(2)
    with c1: 
        temp = st.text_input('Temperature', "100")
        humidity = st.text_input('Humidity', "25")
        pH = st.text_input('pH', 4.5)
        rainfall = st.text_input('Rainfall', "108.06")
    with c2:
        state = st.text_input('State', "Nagaland")
        season = st.text_input('Season', "Kharif")
        area = st.text_input('Area', "50.0")
        yieldd = st.text_input('Yield', "20")
    submitButton = form.form_submit_button(label = 'Calculate')
    if submitButton:
        data = {
            'temperature': temp,
            'humidity': humidity,
            'pH': pH,
            'rainfall': rainfall,
            'state': state,
            'season': season,
            'area': area,
            'yieldd': yieldd
        }
        response = requests.request("POST", f"{my_url}/cost", data=data)

        if response.status_code == 200:
            result = response.json()
            st.markdown("### PREDICTION")
            c1, c2 = st.columns(2)
            with c1:
                st.write("> Crop")
                st.info(result["crop"])
            with c2:
                st.write("> Production Cost")
                st.success(f'Rs. {result["cost"]}')
        else:
            st.write('Error: Unable to get a prediction from the API')


def disease_prediction():
    st.title("Crop Disease Detector")
    disease_detector()

def crop_price_prediction():
    st.title("Crop & Cost Predictor")
    crop_predictor()


PAGES = {
    "Crop Disease Detector": disease_prediction,
    "Crop & Cost Predictor": crop_price_prediction,
}

st.sidebar.title("AI Farmer's Assistant")
selection = st.sidebar.radio("", list(PAGES.keys()))
page = PAGES[selection]
page()
