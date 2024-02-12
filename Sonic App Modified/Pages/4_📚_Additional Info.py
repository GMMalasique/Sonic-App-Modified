import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = "Sonic Log Web App - Info",
    layout='wide'
    )

st.subheader('Porosity Calculation and Evaluation')


# Display the image in Streamlit
img_wyllie = Image.open("Sonic_Formula.png")
img_wyllie = img_wyllie.resize([int(img_wyllie.width/3), int(img_wyllie.height/3.5)])
st.image(img_wyllie, caption= 'Figure 1. Wyllie time average equation')
    
    
st.markdown('''The Wyllie time average method is used for estimating porosity from sonic measurements. 
            It requires the following input parameters:
            \n ϕs = Sonic Porosity
            \n Δtl = Sonic log interval transit time. Typically, its unit is μsec/ft
            \n Δtp = Pore fluid interval transit time.
            \n Δtma = Rock matrix interval transit time    
            ''')
    
img_transit = Image.open("Transit_Time.png")
img_transit = img_transit.resize([int(img_transit.width/3), int(img_transit.height/3.5)])
st.image(img_transit, caption= 'Figure 2. Typical interval transit time for lithologies and fluids')
st.divider()
    
st.subheader('Uncompacted Formation and Hydrocarbon-bearing Zone')
st.markdown('''The existing equation tends to produce higher porosity estimates when applied to uncompacted sandstones 
            and hydrocarbon-bearing reservoirs. 
            To mitigate this issue, we can introduce empirical corrections using two terms: the compaction factor (Cp) 
            and the hydrocarbon correction (Hy).
            \nCp quantifies the impact of pore pressure on the sonic porosity equation. 
            Typically, it is determined through a comparison of density and apparent sonic porosity or by 
            analyzing the sonic response in nearby shale (Cp = Δtsh/100.0).
            \nHy, on the other hand, is an approximate correction factor and is assigned a value of 0.9 for oil and 0.7 for gas reservoirs.
            \nWith these adjustments, the revised Wyllie time average equation is as follows:''')
img_correction = Image.open("Correction.png")
img_correction = img_correction.resize([int(img_correction.width/3), int(img_correction.height/3.5)])
st.image(img_correction, caption= 'Figure 3. Wyllie time average equation with correction')
st.markdown('''Cp = Compaction correction factor
            \nHy = Hydrocarbon correction factor  ''')
st.divider()
    
st.subheader("Common Log Curve Abbreviations")
    
st.markdown('''These are common mnemonics and names for log curves that you may encounter in well logging data. 
            Please note that the availability of these curves and their names can vary depending on the specific well logging tools 
            and data acquisition methods used during the logging operation. 
            Always refer to the specific LAS file's "Curve Information" section or documentation to determine the mnemonics 
            and descriptions of the log curves recorded in that file.
            ''')
file_url = "https://www.spwla.org/documents/spwla/Mnemonic/reevesmnemonics.pdf"  # Replace with the actual URL of your PDF file
st.markdown(f'<a href="{file_url}" download="document.pdf">Click here to download complete tools and curve mnemonics.</a>', unsafe_allow_html=True)

    # path_pdf_abbvr = r"C:\Users\Malasique\Documents\GitHub\Sonic-Log-Interpreter-Web-Application\reeves_mnemonics.pdf"
    # st.markdown(f'<a href = {path_pdf_abbvr} download="document.pdf">Click here to download complete tools and curve mnemonics.</a>', unsafe_allow_html=True)           
img_abbrv = Image.open("Curves_Abbrv.png")
img_abbrv = img_abbrv.resize([int(img_abbrv.width/1.5), int(img_abbrv.height/1.5)])
st.image(img_abbrv, caption= 'Figure 4. List of common log curve abbreviations (mnemonics) and their corresponding names or descriptions' )
