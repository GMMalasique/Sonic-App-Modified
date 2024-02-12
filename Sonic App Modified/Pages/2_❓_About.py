import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = "Sonic Log Web App - About",
    layout='wide'
    )

img_about = Image.open("About_us.jpg")    
st.image(img_about)