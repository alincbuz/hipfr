import streamlit as st
import pandas as pd
import joblib
from PIL import Image

# Loading Our final trained Knn model
model = open("LARC.pickle.dat", "rb")
gb_clf = joblib.load(model)


# Define the prediction function
def predict(varsta, sex, mediu, TOR, implant initial, diabet, status mintal, consum alcool, fumator, IMC):
    # Predicting the probability of fracture
    if sex == 'Female':
        sex = 0
    elif sex == 'Male':
        sex = 1

    if mediu == 'R':
        mediu = 0
    elif mediu == 'U':
        mediu = 1
   
    if implant initial == 'Placa':
        implant initial = 0
    elif implant initial == 'Tija':
        implant initial = 1
    
    if diabet == 'Yes':
        diabet = 0
    elif diabet == 'No':
        diabet = 1

    if status mintal == 'Bad':
        status mintal = 0
    elif status mintal == 'Good':
        status mintal = 1

    if consum alcool == 'No':
        consum alcool = 0
    elif consum alcool == 'Yes':
        consum alcool = 1

    if fumator == 'No':
        fumator = 0
    elif fumator == 'Yes':
        fumator = 1
    
    prediction = gb_clf.predict(pd.DataFrame([[varsta, sex, mediu, TOR, implant initial, diabet, status mintal, consum alcool, fumator, IMC]],
                                            columns=['varsta', 'sex', 'mediu', 'TOR', 'implant initial', 'diabet', 'status mintal', 'consum alcool', 'fumator', 'IMC']))
    return prediction

# Loading images

bad = Image.open('0.png')
good = Image.open('1.png')

st.title('Neoadjuvant Chemoradiotherapy LARC Classification App')
st.image("""https://media.bzi.ro/unsafe/1060x596/smart/filters:contrast(5):format(webp):quality(80)/http://www.bzi.ro/wp-content/uploads/2020/03/Veste-buna-pentru-pacienti-cu-cancer-colorectal.jpg""")
st.header('Enter the predictor variables:')

varsta = st.number_input('Varsta in ani:', min_value=0.0, max_value=100.0, value=15.0,step = 1.0)
sex = st.selectbox('Sex:', ['Male', 'Female'],index=0)
mediu = st.selectbox('Mediu:', ['Urban', 'Rural'],index=0)
TOR = st.number_input('Distanta de la osteosinteza la o noua fractura in zile:', min_value=0.0, max_value=150.0, value=20.0,step=1.0)
implant initial = st.selectbox('Implant initial:', ['Tija', 'Placa'],index=0)
diabet = st.selectbox('Diabet:', ['Yes', 'No'],index=1)
status mintal = st.selectbox('Status mintal:', ['Good', 'Bad'],index=1)
consum alcool = st.selectbox('Consum alcool:', ['Yes', 'No'],index=1)
fumator = st.selectbox('Fumator:', ['Yes', 'No'],index=0)
IMC = st.number_input('Indicele de masa corporala:', min_value=0.0, max_value=40.0, value=20.0,step=1.0)

st.markdown('\n\n')

if st.button("Click Here to Predict TRG"):
    pred = predict(varsta, sex, mediu, TOR, implant initial, diabet, status mintal, consum alcool, fumator, IMC)
    st.image(bad) if pred == 0 else st.image(good)
