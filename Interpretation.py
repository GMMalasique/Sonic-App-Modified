import lasio
import streamlit as st
import pandas as pd
import tempfile
import missingno as ms
import lascheck
import traceback
import math
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from plotly.subplots import make_subplots
    
def app():
    def create_option_menu():
        return option_menu(
            None,
            options=["Las File Specification", "Well Information", "Curve Information", "Curve Data Overview", "Log Visualization"],
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "nav-link": {"font-size": "13px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "green"},
            }
        )
    
    def visualization_option_menu():
        return option_menu(
            None,
            options=["Log Plot", "Depth vs Sonic Porosity", "Sonic Log vs Sonic Porosity", "Formation Evaluation"],
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "nav-link": {"font-size": "13px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "green"},
            }
        )
    
    def las_file_specification():
        st.subheader("LAS File Conformity Check")
        try:
            if tfile is None:
                las = lascheck.read(file)
            else:
                las = lascheck.read(tfile.name)  # Use the path of the temporary file
    
            st.text("Checking LAS file conformity...")
    
            # Initialize the progress bar
            progress_bar = st.progress(0)
            progress_status = st.empty()
    
            # Simulate progress by updating the progress bar
            for percent_complete in range(0, 101):
                progress_bar.progress(percent_complete)
                progress_status.text(f"Checking progress: {percent_complete}%")
    
            # Once the checking is complete, display the results
            st.write("LAS file conformity check complete.")
            if las.check_conformity() == True:
                st.write('**Result:** No non-conformities were found in the LAS file.')
            if las.check_conformity() == False:
                st.write('**Result:** Non-conformities were found in the LAS file.')
                st.write(las.get_non_conformities())
    
        except ValueError as ve:
            # Handle the specific error gracefully
            st.warning(f"An error occurred while processing the LAS file: {ve}")
            # Capture and display the traceback
            st.write("Traceback:")
            st.code(traceback.format_exc())
    
        except Exception as e:
            # Handle the exception gracefully
            st.warning(f"An error occurred while processing the LAS file: {e}")
            # Capture and display the traceback
            st.write("Traceback:")
            st.code(traceback.format_exc())
    
        st.warning('**Note**: "-999.25" is the standard value for a Null value ')
        st.divider()    
    
    def display_well_information():
        st.subheader('Well Information')
        st.markdown(f'Well Name : {well_name}')
        st.markdown(f'Start Depth : {start_depth}')
        st.markdown(f'Stop Depth : {stop_depth}')
        st.markdown(f'Step : {step}')
        st.markdown(f'Company : {company_name}')
        st.markdown(f'Logging Date : {date}')
        st.divider()
    
    def display_curve_information():
        st.subheader('Curve Information')
        st.text(f'================================================\n{curvename}')
        st.divider()
    
    def display_curve_data_overview():
        st.subheader('Curve Data Overview')
        st.markdown('''The value on the left figure is the number of rows. White space in each column of the curve is a missing value row/data. 
                        Expand to see more details''')
        st.pyplot(ms.matrix(las_df, sparkline=False, labels=100).figure)
        st.divider()
    
    def visualize_curve_data(las_file, las_df):
    
        selected_column = st.sidebar.selectbox("**Select curve data to visualize:**", las_df.keys())
    
        try:
            unit_curve = las_file.curves[selected_column].unit  # Get unit from the selected curve
            if unit_curve.upper() not in ('US/M', 'US/FT', 'US/F'):
                st.warning('**Note**: Unit must be either (us/m) or (us/ft). Assuming the selected curve data is Sonic and its unit is us/ft.')
        except KeyError:
            if selected_column == "DEPTH":
                unit_curve = las_file.curves[list(las_file.curves.keys())[0]].unit   # Get unit from the selected curve
            else:
                unit_curve = "Unknown"
    
        st.sidebar.write(f"Unit of {selected_column} curve: {unit_curve}")
    
        # Determine which unit to use based on unit_curve
        if unit_curve.upper() == 'US/M':
            correction_unit = 0.01
        elif unit_curve.upper() == 'US/FT' or unit_curve.upper() == 'US/F':
            correction_unit = 1
        else:
            correction_unit = 1
        
        return selected_column, correction_unit, unit_curve
    
    def hydrocarbon_correction():
        mode = st.sidebar.radio(
            "Hydrocarbon Correction:",
            ('None', 'Oil Correction', 'Gas Correction'))
        
        if mode == 'None':
            correction_hydrocarbon = 1
        elif mode == 'Oil Correction':
            correction_hydrocarbon = 0.9 
        elif mode == 'Gas Correction':
            correction_hydrocarbon = 0.7
        
        return correction_hydrocarbon        
    
    def parameters():
        global dt_matrix_sandstone
        global dt_matrix_limestone
        global dt_matrix_dolomite
        global dt_fluid_seawater
        global dt_fluid_freshwater
        
        dt_matrix_sandstone = 55.5
        dt_matrix_limestone = 47.5
        dt_matrix_dolomite = 43.5
        dt_fluid_seawater = 189
        dt_fluid_freshwater = 204
    
    
    st.set_option('deprecation.showfileUploaderEncoding', False)
    tfile = None
    file = None
    selected_tab = None
    selected_subtab = None
    max_values_df = pd.DataFrame()
    st.divider()
    mode = st.radio(
        "**Select an option:**",
        ('Upload LAS file', 'Use sample LAS file')
    )
    st.divider()
    
    if mode == 'Upload LAS file':
        file = st.file_uploader('Upload a LAS file containing Sonic Log.')
        if file is not None:
            # Create a temporary file and save the uploaded file's content into it
            with tempfile.NamedTemporaryFile(delete=False) as tfile:
                tfile.write(file.read())
                las_file = lasio.read(tfile.name)
                las_df = las_file.df()
                las_df[las_df < -9000] = None
            
    
    if mode == 'Use sample LAS file':
        file = r"Sample.las"
        las_file = lasio.read(file)
        las_df = las_file.df()
        las_df = las_df.replace(-9999.25, None)
    
    if file:
      selected_tab = create_option_menu()
      las_df.insert(0, 'DEPTH', las_df.index)
      las_df.reset_index(drop=True, inplace=True)
    
      try:
        well_name =  las_file.header['Well'].WELL.value
        start_depth = las_df['DEPTH'].min()
        stop_depth = las_df['DEPTH'].max()
        step = abs(las_df['DEPTH'][1]-las_df['DEPTH'][0])
        company_name =  las_file.header['Well'].COMP.value
        date =  las_file.header['Well'].DATE.value
        curvename = las_file.curves
      except:
        well_name =  'unknown'
        start_depth = 0.00
        stop_depth = 10000.00
        step = abs(las_df['DEPTH'][1]-las_df['DEPTH'][0])
        company_name =  'unknown'
        date =  'unknown'
        curvename = las_file.curves
    
        
    if selected_tab == "Las File Specification":
        las_file_specification()
        
    if selected_tab == "Well Information":
        display_well_information()
    
    if selected_tab == "Curve Information":
        display_curve_information()
      
    if selected_tab == "Curve Data Overview":
        display_curve_data_overview()
    
    if selected_tab == "Log Visualization":   
        selected_column, correction_unit, unit_curve = visualize_curve_data(las_file, las_df)
        correction_hydrocarbon = hydrocarbon_correction()
        parameters()
        st.sidebar.subheader('Parameters:')
        if file:
            mode_sandstone_seawater = st.sidebar.checkbox("Matrix: Sandstone | Fluid: Seawater")
            mode_limestone_seawater = st.sidebar.checkbox("Matrix: Limestone | Fluid: Seawater")
            mode_dolomite_seawater = st.sidebar.checkbox("Matrix: Dolomite | Fluid: Seawater")
            mode_sandstone_freshwater = st.sidebar.checkbox("Matrix: Sandstone | Fluid: Freshwater") 
            mode_limestone_freshwater = st.sidebar.checkbox("Matrix: Limestone | Fluid: Freshwater")
            mode_dolomite_freshwater = st.sidebar.checkbox("Matrix: Dolomite | Fluid: Freshwater")
            mode_average = st.sidebar.checkbox("Average Sonic Porosity")
        
    
            
        # Check if 'DT' is a valid curve in the LAS file
        data = []
        temporary = []
        
        if selected_column in las_file.keys():
            for depth, dt_log in zip(las_df['DEPTH'], las_df[selected_column]):
                # Always include depth and Sonic Log Reading
                row_data = {"Depth": depth, 'Sonic Log Reading': dt_log}
                if dt_log is not None:
            
                    # Apply correction factors and calculate sonic porosity
                    if mode_sandstone_seawater:
                        phi_sandstone_seawater = ((dt_log - dt_matrix_sandstone) / (dt_fluid_seawater - dt_matrix_sandstone)) * correction_hydrocarbon * correction_unit
                        row_data['Sandstone (Seawater)'] = phi_sandstone_seawater
            
                    if mode_limestone_seawater:
                        phi_limestone_seawater = ((dt_log - dt_matrix_limestone) / (dt_fluid_seawater - dt_matrix_limestone)) * correction_hydrocarbon * correction_unit
                        row_data['Limestone (Seawater)'] = phi_limestone_seawater
            
                    if mode_dolomite_seawater:
                        phi_dolomite_seawater = ((dt_log - dt_matrix_dolomite) / (dt_fluid_seawater - dt_matrix_dolomite)) * correction_hydrocarbon * correction_unit
                        row_data['Dolomite (Seawater)'] = phi_dolomite_seawater
            
                    if mode_sandstone_freshwater:
                        phi_sandstone_freshwater = ((dt_log - dt_matrix_sandstone) / (dt_fluid_freshwater - dt_matrix_sandstone)) * correction_hydrocarbon * correction_unit
                        row_data['Sandstone (Freshwater)'] = phi_sandstone_freshwater
            
                    if mode_limestone_freshwater:
                        phi_limestone_freshwater = ((dt_log - dt_matrix_limestone) / (dt_fluid_freshwater - dt_matrix_limestone)) * correction_hydrocarbon * correction_unit
                        row_data['Limestone (Freshwater)'] = phi_limestone_freshwater
            
                    if mode_dolomite_freshwater:
                        phi_dolomite_freshwater = ((dt_log - dt_matrix_dolomite) / (dt_fluid_freshwater - dt_matrix_dolomite)) * correction_hydrocarbon * correction_unit
                        row_data['Dolomite (Freshwater)'] = phi_dolomite_freshwater
            
                    # Add similar conditions for other checkboxes (e.g., mode_limestone_freshwater, mode_dolomite_freshwater, etc.)
                    data.append(row_data)
                    
      # Create the DataFrame with appropriate columns
        las_df_revised = pd.DataFrame(data)
        if mode_average:
          las_df_revised['Average Porosity'] = las_df_revised.iloc[:, 2:].mean(axis=1)  
    
        # Display the DataFrame as a presentable Excel-like table      
        if data == [] or selected_column == "DEPTH":
            for depth in (las_df["DEPTH"]):
                las_temporary = {"Depth": depth}
                temporary.append(las_temporary)
              
            temp = pd.DataFrame(temporary)
            with st.expander('Data Sets:', expanded=False):
                st.dataframe(temp)
        else:
            with st.expander('Data Sets:', expanded=True):

                st.dataframe(las_df_revised)
            st.divider()
            selected_subtab = visualization_option_menu()
     
    if selected_subtab == "Log Plot":  
        def track1_xaxis(fig, title):
            fig.update_xaxes(
                title=title,
                ticks="inside",
                nticks=10,
                minor_ticks='inside',
                minor_showgrid=True,
                showline=True,
                anchor='free', 
                position=1,
                autorange='reversed',
                rangemode='tozero',
                gridcolor='lightgray',
                gridwidth=2,
                side='top',
                range=[40, 140],
                row=1, col=1
            )
        
        def track1_yaxis(fig, title):
            fig.update_yaxes(
                title=title, 
                ticks="inside", 
                autorange='reversed',
                showline=True,
                gridcolor='lightgray',
                gridwidth=2,
                row=1, col=1
            )
        
        def track2_xaxis(fig, title):
            fig.update_xaxes(
                title=title,
                ticks="inside",
                nticks=10,
                minor_ticks='inside',
                minor_showgrid=True,
                showline=True,
                anchor='free', 
                position=1,
                autorange='reversed',
                rangemode='tozero',
                gridcolor='lightgray',
                gridwidth=2,
                side='top',
                range=[-0.15, 1.51],
                row=1, col=2
            )
        
        def track2_yaxis(fig, title):
            fig.update_yaxes(
                title=title, 
                ticks="inside", 
                autorange='reversed',
                showline=True,
                gridcolor='lightgray',
                gridwidth=2,
                showticklabels=True,
                row=1, col=2
            )
    
        def track3_xaxis(fig, title):
            fig.update_xaxes(
                title=title,
                ticks="inside",
                nticks=10,
                minor_ticks='inside',
                minor_showgrid=True,
                showline=True,
                anchor='free', 
                position=1,
                autorange='reversed',
                rangemode='tozero',
                gridwidth=2,
                side='top',
                range=[-0.15, 1.51],
                row=1, col=3
            )
        
        def track3_yaxis(fig, title):
            fig.update_yaxes(
                title=title, 
                ticks="inside", 
                autorange='reversed',
                showline=True,
                gridwidth=2,
                showticklabels=True,
                row=1, col=3
            )
    
        
        trackname_1 = f'''Sonic Log ({unit_curve})'''
        trackname_2 = 'Sonic Porosity (p.u.)'
        trackname_3 = 'Sonic Porosity (p.u.)'
              
        fig = make_subplots(rows=1, cols=3, shared_yaxes=True)
        
        #Track 1
        curve_1 = go.Scatter(x=las_df_revised['Sonic Log Reading'], y=las_df_revised['Depth'], name=trackname_1)
        fig.add_trace(curve_1, row=1, col=1)
        track1_xaxis(fig, trackname_1)
        track1_yaxis(fig, 'Depth')
        
        #Track 2
        columns_to_plot = [col for col in las_df_revised.columns if col not in ["Depth", "Sonic Log Reading"]] 
        for column in columns_to_plot:
            curve_2 = go.Scatter(x=las_df_revised[column], y=las_df_revised['Depth'], name=column)
            fig.add_trace(curve_2, row=1, col=2)
        track2_xaxis(fig, trackname_2)
        track2_yaxis(fig, 'Depth')
            
        
        #Track 3
        # Create an empty list to store the maximum values
    
        max_values = []
    
        # Iterate over the rows in the DataFrame
        for index, row in las_df_revised.iterrows():
            # Initialize the maximum value as negative infinity
            max_value = float('-inf')
            
            # Iterate over the columns you want to compare
            for column in columns_to_plot:
                # Get the value from the current column
                value = row[column]
                
                # Update the maximum value if the current value is greater
                if value > max_value:
                    max_value = value
            
            # Append the maximum value to the list
            max_values.append(max_value)
    
        # Add the 'Max Value' column to the DataFrame and rename it
        max_values_df = pd.DataFrame(max_values, columns=["Max Value"])
    
        # Now you can use 'Max Value' in the plot
        if mode_average:
            curve_3 = go.Scatter(x=las_df_revised['Average Porosity'], y=las_df_revised['Depth'], name='Average Porosity Value')
            fig.add_trace(curve_3, row=1, col=3)
        else:
            curve_3 = go.Scatter(x=max_values_df['Max Value'], y=las_df_revised['Depth'], name='Maximum Porosity Value')
            fig.add_trace(curve_3, row=1, col=3)
        
        track3_xaxis(fig, trackname_3)
        track3_yaxis(fig, 'Depth')
        
    
        fig.update_layout(
            title=None,
            height=1000,
            width=1000
        )
        
        fig.update_traces(legendgroup='track1', row=1, col=1)
        fig.update_traces(legendgroup='track2', row=1, col=2)
        fig.update_traces(legendgroup='track3', row=1, col=3)
        
        color_scheme = {
            (-0.15, 0): 'orange',
            (0, 0.467): 'green',
            (0.467, 1): 'gold',
            (1, 1.51): 'red',
        }
        
        # Iterate through color_scheme and add rectangles
        for (x0, x1), color in color_scheme.items():
            fig.add_shape(
                type="rect",
                x0=x0,
                y0=las_df_revised['Depth'].min(),
                x1=x1,
                y1=las_df_revised['Depth'].max(),
                fillcolor=color,
                opacity=0.3,  # Adjust opacity as needed
                layer="below",
                line=dict(width=0),
                row=1, col=3
            ) 
    
        
        st.plotly_chart(fig, use_container_width=True, theme=None)
        

            
        st.markdown('''Corresponding porosity value for each color:''')
        st.markdown('''
                    
                    | Color | Range |
                    | ----------- | ----------- |
                    | Orange | Less than 0 |
                    | Green | 0 to 0.476 |
                    | Yellow | 0.476 to 1 |
                    | Red | More than 1 |
                    
                    ''')

    if selected_subtab == "Depth vs Sonic Porosity":
        # Initialize the figure
        fig = go.Figure()
    
        # Plot the selected columns against 'Depth' in a line graph
        columns_to_plot = [col for col in las_df_revised.columns if col not in ["Depth", "Sonic Log Reading"]]
        for column in columns_to_plot:
            graph_1 = go.Scatter(x=las_df_revised['Depth'], y=las_df_revised[column], name=column)
            fig.add_trace(graph_1)
    
        # Update x-axis
        fig.update_xaxes(
            title="Depth",
            ticks="inside",
            minor_ticks='inside',
            minor_showgrid=True,
            showline=True,
            anchor='free', 
            gridcolor='lightgray',
            gridwidth=2
        )
    
        # Update y-axis
        fig.update_yaxes(
            title="Sonic Porosity", 
            ticks="inside", 
            showline=True,
            gridcolor='lightgray',
            gridwidth=2
        )
    
        # Update layout
        fig.update_layout(
            title=None,
            height=600,
            width=800
        )
    
        # Display the plot
        st.plotly_chart(fig, use_container_width=True, theme=None)
        
        
    if selected_subtab == "Sonic Log vs Sonic Porosity":
        # Initialize the figure
        fig = go.Figure()
    
        # Plot the selected columns against 'Depth' in a line graph
        columns_to_plot = [col for col in las_df_revised.columns if col not in ["Depth", "Sonic Log Reading"]]
        for column in columns_to_plot:
            graph_2 = go.Scatter(x=las_df_revised['Sonic Log Reading'], y=las_df_revised[column], name=column)
            fig.add_trace(graph_2)
    
        # Update x-axis
        fig.update_xaxes(
            title="Depth",
            ticks="inside",
            minor_ticks='inside',
            minor_showgrid=True,
            showline=True,
            anchor='free', 
            gridcolor='lightgray',
            gridwidth=2,
        )
    
        # Update y-axis
        fig.update_yaxes(
            title="Sonic Porosity", 
            ticks="inside", 
            showline=True,
            gridcolor='lightgray',
            gridwidth=2
        )
    
        # Update layout
        fig.update_layout(
            title=None,
            height=600,
            width=800
        )
    
        # Display the plot
        st.plotly_chart(fig, use_container_width=True, theme=None)
        
    if selected_subtab == "Formation Evaluation":
        
        def process_max_values(las_df, las_df_revised):
            interpretation_df = pd.DataFrame({'Depth': las_df['DEPTH']})
            
            max_values = []
            columns_to_plot = [col for col in las_df_revised.columns if col not in ["Depth", "Sonic Log Reading"]] 
        
            # Iterate over the rows in the DataFrame
            for index, row in las_df_revised.iterrows():
                # Initialize the maximum value as negative infinity
                max_value = float('-inf')
                
                # Iterate over the columns you want to compare
                for column in columns_to_plot:
                    # Get the value from the current column
                    value = row[column]
                    
                    # Update the maximum value if the current value is greater
                    if value > max_value:
                        max_value = value
                
                # Append the maximum value to the list
                max_values.append(max_value)
        
            # Add the 'Max Value' column to the DataFrame
            if mode_average:
                interpretation_df["Max Value"] = las_df_revised['Average Porosity']
                #st.table(interpretation_df)
            else:
                interpretation_df["Max Value"] = max_values
            
            return interpretation_df
        


        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            interpretation_df_result = process_max_values(las_df, las_df_revised)
            fig = go.Figure()
            graph_interpretation = go.Scatter(x=interpretation_df_result['Max Value'], y=las_df_revised['Depth'], name='Sonic Porosity Value')
            fig.add_trace(graph_interpretation) 

            fig.update_xaxes(
                title="Sonic Porosity (p.u.)",
                ticks="inside",
                nticks=10,
                minor_ticks='inside',
                minor_showgrid=True,
                showline=True,
                anchor='free', 
                position=1,
                autorange='reversed',
                rangemode='tozero',
                gridwidth=2,
                side='top',
                range=[-0.15, 1.51],
            )
        
            fig.update_yaxes(
                title="Depth", 
                ticks="inside", 
                autorange='reversed',
                showline=True,
                gridwidth=2,
                showticklabels=True

            )
            
            color_scheme = {
                (-0.15, 0): 'orange',
                (0, 0.467): 'green',
                (0.467, 1): 'gold',
                (1, 1.51): 'red',
            }
            
            # Iterate through color_scheme and add rectangles
            for (x0, x1), color in color_scheme.items():
                fig.add_shape(
                    type="rect",
                    x0=x0,
                    y0=las_df_revised['Depth'].min(),
                    x1=x1,
                    y1=las_df_revised['Depth'].max(),
                    fillcolor=color,
                    opacity=0.3,  # Adjust opacity as needed
                    layer="below",
                    line=dict(width=0),
                )
            
            # Update layout
            fig.update_layout(
                title=None,
                height=1000,
                width=1000
            )
        
            # Display the plot
            st.plotly_chart(fig, use_container_width=True, theme=None)
            st.divider()
            st.markdown('''Corresponding porosity value for each color:''')
            st.markdown('''
                            
                            | Color | Range |
                            | ----------- | ----------- |
                            | Orange | Less than 0 |
                            | Green | 0 to 0.476 |
                            | Yellow | 0.476 to 1 |
                            | Red | More than 1 |
                            
                            ''')
                      
        with col2:
            def filter_depth(interpretation_df_result, start_depth, stop_depth):
                top_depth = st.number_input('Top Depth', min_value=0.00, value=start_depth, step=100.00, key="top_depth")
                bot_depth = st.number_input('Bottom Depth', min_value=0.00, value=stop_depth, step=100.00, key="bot_depth")
                
                if st.button('Evaluate'):
                    depth_filtered_df = interpretation_df_result[
                        (interpretation_df_result['Depth'] >= top_depth) & (interpretation_df_result['Depth'] <= bot_depth)
                    ]
                else:
                    depth_filtered_df = interpretation_df_result
                    
                return depth_filtered_df, top_depth, bot_depth
        
            def analyze_max_values(max_values):
                result_message = None
                need_calibration = False
                have_anomaly = False
                need_correction = False
                no_error = True
            
                for max_value in max_values:
                    if max_value < 0 and not need_calibration:
                        need_calibration = True
                        no_error = False
            
                    elif max_value > 1 and not have_anomaly:
                        have_anomaly = True
                        no_error = False
            
                    elif 0.467 < max_value <= 1 and not need_correction:
                        need_correction = True
                        no_error = False
            
                return {
                    "result_message": result_message,
                    "need_calibration": need_calibration,
                    "have_anomaly": have_anomaly,
                    "need_correction": need_correction,
                    "no_error": no_error
                }
        
            def weighted_average_porosity(depth_filtered_df):
                sum_thickness_porosity = 0
                avg_message = ""
            
                for max_value in depth_filtered_df['Max Value']:
                    thickness_porosity = (1 * max_value)
                    sum_thickness_porosity += thickness_porosity
            
                weighted_average_porosity = sum_thickness_porosity / (1 * len(depth_filtered_df['Max Value']))
            
                rounded_weighted_average_porosity = round(weighted_average_porosity, 4)
                
                if math.isnan(rounded_weighted_average_porosity):
                    avg_message = '''The calculated thickness-weighted average porosity is marked as 'nan,' 
                    indicating an undefined value.
                    '''
                elif rounded_weighted_average_porosity == float('-inf'):
                    avg_message = '''The Thickness-Weighted Average Porosity is computed as '-inf',
                    indicating a negative porosity value.
                    '''
                else:
                    avg_message = f'''The calculated Weighted Average Porosity is {rounded_weighted_average_porosity}
                    '''

                    
           
                return rounded_weighted_average_porosity, avg_message

            def display_analysis_results(analysis_result):
                no_error_message = ""
                need_calibration_message = ""
                have_anomaly_message = ""
                need_correction_message = ""
                if analysis_result["no_error"]:
                    no_error_message = '''**Normal sonic porosity reading.**'''

            
                if analysis_result["need_calibration"]:
                    need_calibration_message = '''**Negative porosity value was found in the curve.**
                    This is unexpected for assumed matrix and fluid
                    and may be attributed to factors such as the use of the wrong matrix or cycle skipping.
                                    '''
            
                if analysis_result["have_anomaly"]:
                    have_anomaly_message = '''**Anomalies in the sonic porosity readings are detected, 
                    indicating the presence of more than one porosity value.** 
                    Possible contributing factors include cycle skipping, 
                    larger borehole conditions, or an air-filled borehole or mud affected by gas.'''
            
                if analysis_result["need_correction"]:
                    need_correction_message = '''**An overestimation of porosity is observed, 
                    indicating a need for correction.** 
                    Possible reasons for overestimation encompass uncompacted conditions, 
                    the presence of hydrocarbons, or a complex rock structure.'''
                
                result_message = f'''{no_error_message} {need_calibration_message} {have_anomaly_message} {need_correction_message}
                
                '''

                return result_message
            

        
            interpretation_df_result = process_max_values(las_df, las_df_revised)
            st.markdown('''**Evaluate certain range of depth:**''')
        
            depth_filtered_df, top_depth, bot_depth = filter_depth(interpretation_df_result, start_depth, stop_depth)
            
            st.subheader('Findings:')
            rounded_weighted_average_porosity, avg_message = weighted_average_porosity(depth_filtered_df)
            
            analysis_result = analyze_max_values(depth_filtered_df['Max Value'])
            
            result_message = display_analysis_results(analysis_result)
            
            orange = 0
            green = 0
            yellow = 0
            red = 0
            total_data = 0
            
            for data in depth_filtered_df['Max Value']:
                if data < 0:
                    orange += 1
                if 0 <= data <= 0.476:
                    green += 1
                if 0.476 < data <= 1:
                    yellow += 1
                if data > 1:
                    red += 1

            total_data = len(depth_filtered_df['Max Value'])
            
            orange_result = ""
            green_result = ""
            yellow_result = ""
            red_result = ""
            if orange != 0:
                orange_result = f"Orange: {(orange/total_data)*100:.2f}%"

            if green != 0:
                green_result = f"Green: {(green/total_data)*100:.2f}%"

            if yellow != 0:
                yellow_result = f"Yellow: {(yellow/total_data)*100:.2f}%"

            if red != 0:
                red_result = f"Red: {(red/total_data)*100:.2f}%"
             
            
            if mode_sandstone_seawater:
                matrix = "Sandstone"
                fluid = "Seawater"
            if mode_limestone_seawater:
                matrix = "Limestone"
                fluid = "Seawater"
            if mode_dolomite_seawater:
                matrix = "Dolomite"
                fluid = "Seawater"
            if mode_sandstone_freshwater:
                matrix = "Sandstone"
                fluid = "Freshwater"
            if mode_limestone_freshwater:
                matrix = "Limestone"
                fluid = "Freshwater"
            if mode_dolomite_freshwater:
                matrix = "Dolomite"
                fluid = "Freshwater"
            
            st.markdown(f'''
                        
                        Assuming the matrix was **{matrix}** and the fluid was **{fluid}**, 
                        the depth range of {top_depth} to {bot_depth} indicates the following findings:
                        \n- {avg_message}
                        \n- {result_message} 
                        \n Examining the sonic porosity curve and its alignment with the color-coded track, 
                        the distribution is as follows: 
                            \n **{orange_result}** 
                            \n **{green_result}**
                            \n **{yellow_result}**
                            \n **{red_result}**
                        
                        ''')

            

            st.cache
            with st.expander("Show Table"):
                # Rename the 'Max Value' column to 'Sonic Porosity'
                depth_filtered_df = depth_filtered_df.rename(columns={'Max Value': 'Sonic Porosity'})
                st.dataframe(depth_filtered_df)
        
                
                        
                        
                                
                        
                                
                                
                        
                        
                            