import streamlit as st
from PIL import Image

def app():
    
    img_about = Image.open("About_us.jpg")    
    st.image(img_about)