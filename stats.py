import streamlit as st
import numpy as np
import pandas as pd

random_atributes=[45,45,22,78,12,53]

@st.cache
def get_data():
    columns=["age","date of birth","nationality","weight","heigh","team"]

    return pd.DataFrame([random_atributes],columns=columns)

df=get_data()
hdf=df.assign(hack="").set_index("hack")

st.write("atributes")
st.table(hdf)



st.markdown("""
# This is a header
## This is a sub header
### This is text
""")
df = pd.DataFrame({
    'first column': list(range(1, 11)),
    'second column': np.arange(10, 101, 10)
})

mean = df["second column"].mean()
n_rows = len(df)
md_results = f"The mean is **{mean:.2f}** and there are **{n_rows:,}**."
st.markdown(md_results)

"""
#using footbaler's face picture
img = "Image".open("streamlit.png")
st.image(img, height=200, width=200)

# and used in order to select the displayed lines
head_df = df.head(line_count)
head_df
"""

# TAKE WEIGHT INPUT in kgs
weight = st.number_input("Enter your weight (in kgs)")

status="cms"
# compare status value
if (status == 'cms'):
    # take height input in centimeters
    height = st.number_input('Centimeters')

    try:
        bmi = weight / ((height / 100)**2)
    except:
        st.text("Enter some value of height")

# print the BMI INDEX
st.text("Your BMI Index is {}.".format(bmi))

# give the interpretation of BMI index
if (bmi < 16):
    st.error("You are Extremely Underweight")
elif (bmi >= 16 and bmi < 18.5):
    st.warning("You are Underweight")
elif (bmi >= 18.5 and bmi < 25):
    st.success("Healthy")
elif (bmi >= 25 and bmi < 30):
    st.warning("Overweight")
elif (bmi >= 30):
    st.error("Extremely Overweight")
