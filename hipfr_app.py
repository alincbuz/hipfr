import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

# Load the trained model
loaded_model = tf.keras.models.load_model('hipfr_model.h5')

# Load the MinMaxScaler
scaler = MinMaxScaler()

# Define the input ranges for the MinMaxScaler
input_ranges = pd.DataFrame({ 'varsta': [0.0, 100.0],'sex':[0,1], 'mediu':[0,1],'TOR': [0.0, 150.0],'implant_initial':[0,1], 'HTA':[0,1], 'diabet':[0,1], 'status_mintal':[0,1], 'consum_alcool':[0,1], 'fumator':[0,1],'IMC': [0.0, 40.0]})

# Fit the MinMaxScaler
scaler.fit(input_ranges)

# Define the prediction function
def predict(varsta, sex, mediu, TOR, implant_initial, HTA, diabet, status_mintal, consum_alcool, fumator, IMC):

    # Preprocess the input variables
#Predicting the price of the carat
    if sex == 'Female':
        sex = 0
    else:
        sex = 1
    
    if mediu == 'Rural':
        mediu = 0
    else:
        mediu = 1
    
    if implant_initial == 'Placa':
        implant_initial = 0
    else:
        implant_initial = 1
    
    if HTA == 'No':
        HTA = 0
    else:
        HTA = 1

    if diabet == 'No':
        diabet = 1
    else:
        diabet = 2

    if status_mintal == 'Bad':
        status_mintal = 0
    else:
        status_mintal = 1

    if consum_alcool == 'No':
        consum_alcool = 0
    else:
        consum_alcool = 1

    if fumator == 'No':
        fumator = 0
    else:
        fumator = 1

    # Create a DataFrame with the input values
    data = pd.DataFrame([[varsta, sex, mediu, TOR, implant_initial, HTA, diabet, status_mintal, consum_alcool, fumator, IMC]],
                        columns=['varsta', 'sex', 'mediu', 'TOR', 'implant_initial', 'HTA', 'diabet', 'status_mintal', 'consum_alcool', 'fumator', 'IMC'])

    # Apply MinMaxScaler
    data_scaled = scaler.transform(data)

    # Make the prediction
    prediction = loaded_model.predict(data_scaled)
    return prediction

# Loading images
good = Image.open('0.JPG')
bad = Image.open('1.JPG')

st.title('Aplicatie screening osteoporoza si estimare risc fractura')
st.image('https://www.endocrine.org/-/media/endocrine/images/patient-engagement-webpage/condition-page-images/bone-health-and-osteoporosis/osteoporosis_pe_1796x943.jpg')
st.header('Introduceti variabilele predictor:')

varsta = st.number_input('Varsta in ani:', min_value=0.0, max_value=100.0, value=15.0, step=1.0)
sex = st.selectbox('Sex:', ('Male', 'Female'), index=0)
mediu = st.selectbox('Mediu:', ('Urban', 'Rural'), index=0)
TOR = st.number_input('Distanta de la osteosinteza la o noua fractura in luni:', min_value=0.0, max_value=150.0, value=20.0, step=1.0)
implant_initial = st.selectbox('Implant initial:', ('Tija', 'Placa'), index=0)
HTA = st.selectbox('Hipertensiune arteriala:', ('Yes', 'No'), index=0)
diabet = st.selectbox('Diabet:', ('Yes', 'No'), index=0)
status_mintal = st.selectbox('Status mintal:', ('Good', 'Bad'), index=0)
consum_alcool = st.selectbox('Consum alcool:', ('Yes', 'No'), index=0)
fumator = st.selectbox('Fumator:', ('Yes', 'No'), index=0)
IMC = st.number_input('Indicele de masa corporala:', min_value=0.0, max_value=40.0, value=20.0, step=1.0)

st.markdown('\n\n')

if st.button("Click Here to Predict TRG"):
    pred = predict(varsta, sex, mediu, TOR, implant_initial, HTA, diabet, status_mintal, consum_alcool, fumator, IMC)

    #st.write(pred)

    result_placeholder = st.empty()

    if np.round(pred) == 0:
        result_placeholder.image(good)
    else:
        result_placeholder.image(bad)
        st.write('Risc de fractura')
