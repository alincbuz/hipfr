import streamlit as st
import pandas as pd
import joblib
from PIL import Image

# Loading Our final trained Knn model
model = open("LARC.pickle.dat", "rb")
gb_clf = joblib.load(model)


# Define the prediction function
def predict(sex, pT, pN, i_limfatica, i_venoasa, i_perineurala, grading, varsta, RT_CHIR):
    # Predicting the price of the carat
    if sex == 'Female':
        sex = 0
    elif sex == 'Male':
        sex = 1

    if pT == '0':
        pT = 0
    elif pT == '1':
        pT = 1
    elif pT == '2':
        pT = 2
    elif pT == '3':
        pT = 3
    elif pT == '4':
        pT = 4

    if pN == '0':
        pN = 0
    elif pN == '1':
        pN = 1
    elif pN == '2':
        pN = 2

    if i_limfatica == 'No':
        i_limfatica = 0
    elif i_limfatica == 'Yes':
        i_limfatica = 1

    if i_venoasa == 'No':
        i_venoasa = 0
    elif i_venoasa == 'Yes':
        i_venoasa = 1

    if i_perineurala == 'No':
        i_perineurala = 0
    elif i_perineurala == 'Yes':
        i_perineurala = 1

    if grading == '1':
        grading = 1
    elif grading == '2':
        grading = 2
    elif grading == '3':
        grading = 3
    elif grading == '4':
        grading = 4

    prediction = gb_clf.predict(pd.DataFrame([[sex, pT, pN, i_limfatica, i_venoasa, i_perineurala, grading, varsta, RT_CHIR]],
                                            columns=['sex', 'pT', 'pN', 'i_limfatica', 'i_venoasa', 'i_perineurala', 'grading', 'varsta',
                                                     'RT_CHIR']))
    return prediction

# Loading images

bad = Image.open('0.png')
good = Image.open('1.png')

st.title('Neoadjuvant Chemoradiotherapy LARC Classification App')
st.image("""https://media.bzi.ro/unsafe/1060x596/smart/filters:contrast(5):format(webp):quality(80)/http://www.bzi.ro/wp-content/uploads/2020/03/Veste-buna-pentru-pacienti-cu-cancer-colorectal.jpg""")
st.header('Enter the predictor variables:')

sex = st.selectbox('Sex:', ['Male', 'Female'],index=0)
pT = st.selectbox('pT:', ['0', '1', '2', '3', '4'],index=0)
pN = st.selectbox('pN:', ['0', '1', '2'],index=0)
i_limfatica = st.selectbox('Invazie limfatica:', ['Yes', 'No'],index=1)
i_venoasa = st.selectbox('Invazie venoasa:', ['Yes', 'No'],index=1)
i_perineurala = st.selectbox('Invazie perineurala:', ['Yes', 'No'],index=1)
grading = st.selectbox('Grading:', ['1', '2', '3', '4'],index=0)
varsta = st.number_input('Varsta in ani:', min_value=0.0, max_value=100.0, value=15.0,step = 1.0)
RT_CHIR = st.number_input('Distanta de la RT la CHT in zile:', min_value=0.0, max_value=70.0, value=20.0,step=1.0)

st.markdown('\n\n')

if st.button("Click Here to Predict TRG"):
    pred = predict(sex, pT, pN, i_limfatica, i_venoasa, i_perineurala, grading, varsta, RT_CHIR)
    st.image(bad) if pred == 0 else st.image(good)
