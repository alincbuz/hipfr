import streamlit as st
import pandas as pd
from PIL import Image
from keras.models import load_model

# Load the trained model
model = load_model('hipfr_model.h5')

# Define the prediction function
def predict(varsta, sex, mediu, TOR, implant_initial, diabet, status_mintal, consum_alcool, fumator, IMC):
    # Preprocess the input variables
    sex = 0 if sex == 'Female' else 1
    mediu = 0 if mediu == 'R' else 1
    implant_initial = 0 if implant_initial == 'Placa' else 1
    diabet = 0 if diabet == 'Yes' else 1
    status_mintal = 0 if status_mintal == 'Bad' else 1
    consum_alcool = 0 if consum_alcool == 'No' else 1
    fumator = 0 if fumator == 'No' else 1

    # Create a DataFrame with the input values
    data = pd.DataFrame([[varsta, sex, mediu, TOR, implant_initial, diabet, status_mintal, consum_alcool, fumator, IMC]],
                        columns=['varsta', 'sex', 'mediu', 'TOR', 'implant_initial', 'diabet', 'status_mintal', 'consum_alcool', 'fumator', 'IMC'])

    # Make the prediction
    prediction = model.predict(data)
    return prediction

# Loading images
bad = Image.open('0.png')
good = Image.open('1.png')

st.title('Neoadjuvant Chemoradiotherapy LARC Classification App')
st.image('https://media.bzi.ro/unsafe/1060x596/smart/filters:contrast(5):format(webp):quality(80)/http://www.bzi.ro/wp-content/uploads/2020/03/Veste-buna-pentru-pacienti-cu-cancer-colorectal.jpg')
st.header('Enter the predictor variables:')

varsta = st.number_input('Varsta in ani:', min_value=0.0, max_value=100.0, value=15.0, step=1.0)
sex = st.selectbox('Sex:', ['Male', 'Female'], index=0)
mediu = st.selectbox('Mediu:', ['Urban', 'Rural'], index=0)
TOR = st.number_input('Distanta de la osteosinteza la o noua fractura in zile:', min_value=0.0, max_value=150.0, value=20.0, step=1.0)
implant_initial = st.selectbox('Implant initial:', ['Tija', 'Placa'], index=0)
diabet = st.selectbox('Diabet:', ['Yes', 'No'], index=1)
status_mintal = st.selectbox('Status mintal:', ['Good', 'Bad'], index=1)
consum_alcool = st.selectbox('Consum alcool:', ['Yes', 'No'], index=1)
fumator = st.selectbox('Fumator:', ['Yes', 'No'], index=0)
IMC = st.number_input('Indicele de masa corporala:', min_value=0.0, max_value=40.0, value=20.0, step=1.0)

st.markdown('\n\n')

if st.button("Click Here to Predict TRG"):
    pred = predict(varsta, sex, mediu, TOR, implant_initial, diabet, status_mintal, consum_alcool, fumator, IMC)
    st.image(bad) if pred == 0 else st.image(good)
