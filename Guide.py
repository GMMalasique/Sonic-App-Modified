import streamlit as st
from PIL import Image
    
    
def app():    

    st.divider()
    img = {
        '1': Image.open('Guide_1.png'),
        '2': Image.open('Guide_2.png'),
        '3': Image.open('Guide_3.png'),
        '4': Image.open('Guide_4.png'),
        '5': Image.open('Guide_5.png'),
        '6': Image.open('Guide_6.png'),
        '7': Image.open('Guide_7.png'),
        '8': Image.open('Guide_8.png'),
        '9': Image.open('Guide_9.png'),
        '10': Image.open('Guide_10.png'),
        '11': Image.open('Guide_11.png'),
        
    }


    
    st.markdown('''

## User's Guide
**Welcome to Sonic Log Interpretation Web Application! To begin using the application, follow these steps:**

---
### Choose a Source for LAS Files
You have two options for providing LAS files to the Web Application:

### Option 1: Upload LAS File
1. Click on the "Browse Files" button to upload your LAS file.
2. Navigate to your LAS file and select it in the file dialog.
3. Click "Open" to upload the selected LAS file.
    
### Option 2: Use Sample LAS File
- Select "Use Sample LAS File" to explore the application without uploading your own file.
- Experience the features using a pre-loaded sample LAS file.
''')

    st.image(img['2'], width=1000)

    st.markdown('''
    ---                
    
    ### Options After LAS File Selection
    Once the user selected or uploaded the LAS file, the user can explore and analyze the data using the following options:
    
    ### 1. LAS File Specification
    Click on **LAS File Specification** in the navigation menu for detailed information about LAS file specifications.
    ''')
    st.image(img['3'], width=1000)
    
    
    st.markdown('''
    
    ### 2. Well Information
    Click on **Well Information** in the navigation menu to access well-related details such as name, location, and metadata.
    ''')
    st.image(img['4'], width=1000)
    
    st.markdown('''
    ### 3. Curve Information
    Click on **Curve Information** in the navigation menu to view details about curves present in the LAS file.
    ''')
    st.image(img['5'], width=1000)
    
    st.markdown('''
    ### 4. Curve Data Overview
    Click on **Curve Data Overview** in the navigation menu for a summarized view of the dataset within the curves.
    ''')
    st.image(img['6'], width=1000)
    
    st.markdown('''
    ### 5. Log Visualization
    Click on **Log Visualization** in the navigation menu to visually analyze log data through interactive charts and graphs.
    
    
    **Sonic Porosity Calculation:**
    
    - Go to the selection of Curve Data.
    - Select "DT" (Sonic Log) curve.
    - After selecting Curve Data, choose checkboxes from the parameters to calculate sonic porosity.
    
    *Not familiar with curve mnemonics? Learn more in the Additional Info tab in the Web Application Main Menu.*
    

    ''')
    st.image(img['7'], width=1000)
    
    st.markdown('''
    ---
    ### Data Visualization
    The web application visualizes the data into the following:
    
    **Log Plot**
    - Sonic Log (Track 1)
    - Sonic Porosity (Track 2)
    - Interpretation (Track 3)
    ''')
    st.image(img['8'], width=1000)
    
    st.markdown('''
    **Graphs**
    - Depth vs Sonic Porosity Graph
    ''')
    st.image(img['10'], width=1000)
    st.markdown('''
    - Sonic Log vs Sonic Porosity Graph             
    ''')
    st.image(img['11'], width=1000)
    
    
    st.markdown('''
    ---
    ### Formation Evaluation
    Under the Log Plot tab, the user can allow the web application to perform formation evaluation by clicking the formation evaluation checkbox.                
                    
                    ''')
    st.image(img['9'], width=1000)