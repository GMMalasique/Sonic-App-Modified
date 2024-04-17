import lasio
import streamlit as st
import pandas as pd
import tempfile
import missingno as msno
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from plotly.subplots import make_subplots
    
def app():
    def create_option_menu():
        return option_menu(
            None,
            options=["Sonic Porosity Calculation", "Formation Evaluation"],
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "nav-link": {"font-size": "21px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "green"},
            }
        )

    
    def visualize_curve_data(selected_curve):
        try:
            unit_curve = las_file.curves[selected_curve].unit  # Get unit from the selected curve
            st.sidebar.write(f"Unit of {selected_curve} curve: {unit_curve}")
            if unit_curve.upper() not in ('US/M', 'US/FT', 'US/F'):
                st.sidebar.warning('**Note**: Unit must be either (us/m) or (us/ft). Assuming the selected curve data is Sonic and its unit is us/ft.')
        except (NameError, KeyError):
            if selected_curve == "DEPTH":
                unit_curve = las_file.curves[list(las_file.curves.keys())[0]].unit   # Get unit from the selected curve
            else:
                unit_curve = "Unknown"
    
    def parameters():
        dt_matrix_sandstone = 55.5
        dt_matrix_limestone = 47.5
        dt_matrix_dolomite = 43.5
        dt_fluid_seawater = 185
        dt_fluid_freshwater = 189
        
        return dt_matrix_sandstone, dt_matrix_limestone, dt_matrix_dolomite, dt_fluid_seawater, dt_fluid_freshwater
    
    
    st.set_option('deprecation.showfileUploaderEncoding', False)
    tfile = None
    file = None
    selected_tab = None
    las_df = pd.DataFrame()
    
    st.divider()
    mode = st.sidebar.radio(
        "**Select data source:**",
        ('Upload LAS file', 'Use sample LAS file')
    )
    try:
        if mode == 'Upload LAS file':
            file = st.sidebar.file_uploader('Upload a LAS file containing Sonic Log.')
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
            
         
        selected_curve = st.sidebar.selectbox("**Select curve data to visualize:**", las_df.keys())
        visualize_curve_data(selected_curve)
        dt_matrix_sandstone, dt_matrix_limestone, dt_matrix_dolomite, dt_fluid_seawater, dt_fluid_freshwater = parameters()


            
    # Sonic Porosity Calculation
        data = []
        temporary = []
        
        
        if selected_curve in las_file.keys():
            for depth, sonic_log in zip(las_df['DEPTH'], las_df[selected_curve]):
                # Always include depth and Sonic Log Reading
                row_data = {"Depth": depth, 'Sonic Log': sonic_log}
                if sonic_log is not None:
            
                    phi_sandstone_seawater = round(((sonic_log - dt_matrix_sandstone) / (dt_fluid_seawater - dt_matrix_sandstone)), 4)
                    row_data['Sandstone (Seawater)'] = phi_sandstone_seawater
                    
                    phi_limestone_seawater = round(((sonic_log - dt_matrix_limestone) / (dt_fluid_seawater - dt_matrix_limestone)), 4)
                    row_data['Limestone (Seawater)'] = phi_limestone_seawater
                
        
                    phi_dolomite_seawater = round(((sonic_log - dt_matrix_dolomite) / (dt_fluid_seawater - dt_matrix_dolomite)), 4)
                    row_data['Dolomite (Seawater)'] = phi_dolomite_seawater
                
        
                    phi_sandstone_freshwater = round(((sonic_log - dt_matrix_sandstone) / (dt_fluid_freshwater - dt_matrix_sandstone)), 4)
                    row_data['Sandstone (Freshwater)'] = phi_sandstone_freshwater
                
        
                    phi_limestone_freshwater = round(((sonic_log - dt_matrix_limestone) / (dt_fluid_freshwater - dt_matrix_limestone)),4)
                    row_data['Limestone (Freshwater)'] = phi_limestone_freshwater
                
                    phi_dolomite_freshwater = round(((sonic_log - dt_matrix_dolomite) / (dt_fluid_freshwater - dt_matrix_dolomite)), 4)
                    row_data['Dolomite (Freshwater)'] = phi_dolomite_freshwater
        
            
                    # Add similar conditions for other checkboxes (e.g., mode_limestone_freshwater, mode_dolomite_freshwater, etc.)
                    data.append(row_data)
                  
        # Create the DataFrame with appropriate columns
        las_df_revised = pd.DataFrame(data)
    
    
    
        # Display the DataFrame as a presentable Excel-like table      
        if data == [] or selected_curve == "DEPTH":
            for depth in (las_df["DEPTH"]):
                las_temporary = {"Depth": depth}
                temporary.append(las_temporary)
              
            temp = pd.DataFrame(temporary)
            with st.expander('Data Set:', expanded=False):
                st.dataframe(temp)
        else:
            with st.expander('Data Set:', expanded=True):
        
                st.dataframe(las_df_revised)
            st.divider()

    except(UnboundLocalError):
        pass

# Data Visualization
    if selected_tab == "Sonic Porosity Calculation": 
        if selected_curve == "DEPTH":
            pass
        else:
            st.markdown("### Data Visualization")
            col1, col2 = st.columns(2)
            mode_sandstone_seawater = col1.checkbox("Matrix: Sandstone | Fluid: Seawater")
            mode_limestone_seawater = col1.checkbox("Matrix: Limestone | Fluid: Seawater")
            mode_dolomite_seawater = col1.checkbox("Matrix: Dolomite | Fluid: Seawater")
            mode_sandstone_freshwater = col2.checkbox("Matrix: Sandstone | Fluid: Freshwater") 
            mode_limestone_freshwater = col2.checkbox("Matrix: Limestone | Fluid: Freshwater")
            mode_dolomite_freshwater = col2.checkbox("Matrix: Dolomite | Fluid: Freshwater")
            
            count_parameters = 1    
            if mode_sandstone_seawater:
                count_parameters += 1       
            if mode_limestone_seawater:
                count_parameters += 1  
            if mode_dolomite_seawater:
                count_parameters += 1  
            if mode_sandstone_freshwater:
                count_parameters += 1  
            if mode_limestone_freshwater:
                count_parameters += 1  
            if mode_dolomite_freshwater:
                count_parameters += 1  
    
            def configure_track(fig, track_num, x_title, x_range, y_title):
                fig.update_xaxes(
                    title=x_title,
                    ticks="inside",
                    nticks=5,
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
                    range=x_range,
                    row=1,
                    col=track_num
                )
                fig.update_yaxes(
                    ticks="inside",
                    autorange='reversed',
                    showline=True,
                    gridcolor='lightgray',
                    gridwidth=2,
                    showticklabels=True,
                    row=1,
                    col=track_num
                )
            
            trackname_1 = '''Sonic Log'''
            trackname_2 = 'Sonic Porosity SS-SW Scale (p.u.)'
            trackname_3 = 'Sonic Porosity LS-SW Scale (p.u.)'
            trackname_4 = 'Sonic Porosity DL-SW Scale (p.u.)'
            trackname_5 = 'Sonic Porosity SS-FW Scale (p.u.)'
            trackname_6 = 'Sonic Porosity LS-SW Scale (p.u.)'
            trackname_7 = 'Sonic Porosity DL-SW Scale (p.u.)'
                  
            # Initialize the figure with the appropriate number of columns
            fig = make_subplots(rows=1, cols=count_parameters, shared_yaxes=True)
            
            # Counter for the current subplot column
            current_col = 1
            
            # Track 1
            curve_1 = go.Scatter(x=las_df_revised['Sonic Log'], y=las_df_revised['Depth'], name=trackname_1)
            fig.add_trace(curve_1, row=1, col=current_col)
            fig.update_xaxes(
                title='Sonic Log',
                ticks="inside",
                nticks=5,
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
                range=[140, 40],
                row=1,
                col=1
            )
            fig.update_yaxes(
                title='Depth',
                ticks="inside",
                autorange='reversed',
                showline=True,
                gridcolor='lightgray',
                gridwidth=2,
                showticklabels=True,
                row=1,
                col=1
            )
            
            # Increment the counter
            current_col += 1
            
            # Checkboxes for other parameters
            # Add traces and configure tracks based on the checked parameters, adjusting the current_col accordingly
            
            if mode_sandstone_seawater:
                curve_2 = go.Scatter(x=las_df_revised["Sandstone (Seawater)"], y=las_df_revised['Depth'], name=trackname_2)
                fig.add_trace(curve_2, row=1, col=current_col)
                configure_track(fig, current_col, 'Sandstone (Seawater)', [-0.15, 1.51], 'Depth')
                current_col += 1
            
            if mode_limestone_seawater:
                curve_3 = go.Scatter(x=las_df_revised["Limestone (Seawater)"], y=las_df_revised['Depth'], name=trackname_3)
                fig.add_trace(curve_3, row=1, col=current_col)
                configure_track(fig, current_col, 'Limestone (Seawater)', [-0.15, 1.51], 'Depth')
                current_col += 1
            
            if mode_dolomite_seawater:
                curve_4 = go.Scatter(x=las_df_revised["Dolomite (Seawater)"], y=las_df_revised['Depth'], name=trackname_4)
                fig.add_trace(curve_4, row=1, col=current_col)
                configure_track(fig, current_col, 'Dolomite (Seawater)', [-0.15, 1.51], 'Depth')
                current_col += 1
            
            if mode_sandstone_freshwater:
                curve_5 = go.Scatter(x=las_df_revised["Sandstone (Freshwater)"], y=las_df_revised['Depth'], name=trackname_5)
                fig.add_trace(curve_5, row=1, col=current_col)
                configure_track(fig, current_col, 'Sandstone (Freshwater)', [-0.15, 1.51], 'Depth')
                current_col += 1
            
            if mode_limestone_freshwater:
                curve_6 = go.Scatter(x=las_df_revised["Limestone (Freshwater)"], y=las_df_revised['Depth'], name=trackname_6)
                fig.add_trace(curve_6, row=1, col=current_col)
                configure_track(fig, current_col, 'Limestone (Freshwater)', [-0.15, 1.51], 'Depth')
                current_col += 1
            
            if mode_dolomite_freshwater:
                curve_7 = go.Scatter(x=las_df_revised["Dolomite (Freshwater)"], y=las_df_revised['Depth'], name=trackname_7)
                fig.add_trace(curve_7, row=1, col=current_col)
                configure_track(fig, current_col, 'Dolomite (Freshwater)', [-0.15, 1.51], 'Depth')
                current_col += 1
            
            # Update layout and display the plot
            fig.update_layout(
                title=None,
                height=1000,
                width=2000
            )
            
            # Update traces
            for i in range(1, count_parameters + 1):
                fig.update_traces(legendgroup=f'track{i}', row=1, col=i)
            
            st.markdown("### Log Plot")
            if current_col == 2:
                fig.update_layout(
                    title=None,
                    height=1000,
                    width=350
                )
                st.plotly_chart(fig, use_container_width=False, theme=None)
                
            elif current_col == 3:
                fig.update_layout(
                    title=None,
                    height=1000,
                    width=700
                )
                st.plotly_chart(fig, use_container_width=False, scroll=True, theme=None)

            elif current_col == 4:
                fig.update_layout(
                    title=None,
                    height=1000,
                    width=1050
                )
                st.plotly_chart(fig, use_container_width=False, scroll=True, theme=None)

            elif current_col == 5:
                fig.update_layout(
                    title=None,
                    height=1000,
                    width=1400
                )
                st.plotly_chart(fig, use_container_width=False, scroll=True, theme=None)

            elif current_col == 6:
                fig.update_layout(
                    title=None,
                    height=1000,
                    width=1750
                )
                st.plotly_chart(fig, use_container_width=False, scroll=True, theme=None)
                
            else:
                fig.update_layout(
                    title=None,
                    height=1000,
                    width=2100
                )
                st.plotly_chart(fig, use_container_width=False, scroll=True, theme=None)
    
          

    #Formation Evaluation  
    try:      
        if selected_tab == "Formation Evaluation":
    
            def display_well_information():
                st.subheader('Well Information')
                st.markdown(f'''
                    Well Name : {well_name}\n
                    Start Depth : {start_depth}\n
                    Stop Depth : {stop_depth}\n
                    Step : {step}\n
                    Company : {company_name}\n
                    Logging Date : {date}
                ''')
    
            def display_curve_information():
                st.subheader('Curve Information')
                st.text(f'{curvename}')
            
            def display_curve_data_overview():
                st.subheader('Curve Data Overview')
                st.markdown('''The value on the left figure is the number of rows. White space in each column of the curve is a missing value row/data. 
                                Expand to see more details''')
                st.pyplot(msno.matrix(las_df, sparkline=True, labels=100).figure)
                
            def filter_depth(las_df_revised, start_depth, stop_depth):
                top_depth = col1.number_input('Top Depth', min_value=0.00, value=start_depth, step=100.00, key="top_depth")
                bot_depth = col2.number_input('Bottom Depth', min_value=0.00, value=stop_depth, step=100.00, key="bot_depth")
                
                if col1.button('Evaluate'):
                    depth_filtered_df = las_df_revised[
                        (las_df_revised['Depth'] >= top_depth) & (las_df_revised['Depth'] <= bot_depth)]
    
                else:   
                    depth_filtered_df = las_df_revised
                    
    
                return depth_filtered_df, top_depth, bot_depth
            
            def interpolate_data(depth_filtered_df):
                interpolated_df = depth_filtered_df.interpolate(method='linear')
                
                return interpolated_df
            
            def categorize_porosity(column):
                negative_val = 0
                normal_val = 0
                abnormal_val = 0
                null_val = 0
                null_val = depth_filtered_df[column].isnull().sum()
                total_val = len(depth_filtered_df[column])
            
                for data in depth_filtered_df[column]:
                    if data < 0:
                        negative_val += 1
                    if 0 <= data <= 1:
                        normal_val += 1
                    if data > 1:
                        abnormal_val += 1
                
                return negative_val, normal_val, abnormal_val, null_val, total_val
            
            def interpretation(negative_val, normal_val, abnormal_val, null_val, total_val):
    # Porosity Distribution
                normal_percentage = (normal_val/total_val)*100
                negative_percentage = (negative_val/total_val)*100
                abnormal_percentage = (abnormal_val/total_val)*100
                null_percentage = (null_val/total_val)*100
    
    # Weighted Average Porosity            
                sum_thickness_porosity = 0
                
                for value in depth_filtered_df[column]:
                    thickness_porosity = (1 * value)
                    sum_thickness_porosity += thickness_porosity
                weighted_average_porosity = sum_thickness_porosity / (1 * len(depth_filtered_df[column]))
                rounded_average_porosity = round(weighted_average_porosity, 4)
    
                st.markdown('''
                            =======================================================
                            ''')
                
                st.markdown(f'''
                            **Matrix = {matrix}; Fluid = {fluid}**\n
                            Weighted average porosity = {rounded_average_porosity}
                            ''')
                if normal_percentage == 100:
                    st.markdown('''
                                All porosity values are within the typical range of 0 up to 1.
                                ''')
                else:
                    st.markdown(f'''
                                Not all porosity values are within the typical range of 0 up to 1. Normal value percentage = {normal_percentage: .4f}%
                                ''')
                    
                if negative_percentage == 0:
                    st.markdown('''
                                No porosity values less than 0 have been found
                                ''')
                else:
                    st.markdown(f'''
                                Porosity values less than 0 have been found. Negative value percentage = {negative_percentage: .4f}%\n
                                It is possible that the assumed matrix or lithology in the formation was not correct or cycle skipping occurred.
                                ''')
                    
                if abnormal_percentage == 0:
                    st.markdown('''
                                No porosity values greater than 0 have been found
                                ''')
                else:
                    st.markdown(f'''
                                Porosity values more than 0 have been found. Abnormal value percentage = {abnormal_percentage: .4f}%\n
                                Possible contributing factors include cycle skipping, larger borehole conditions, or an air-filled borehole or mud affected by gas.
                                ''')
                
                if null_percentage == 0:
                    st.markdown('''
                                No missing values have been found.
                                ''')
                else:
                    st.markdown(f'''
                                Missing values have been found. Null value percentage = {null_percentage: .4f}%\n
                                Linear interpolation was applied to fill missing data in the evaluation.
                                ''')
    
    
                
                
                st.markdown('''
                            =======================================================
                            ''')
                    
                    
    
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
    
            col1, col2 = st.columns(2)
            depth_filtered_df, top_depth, bot_depth = filter_depth(las_df_revised, start_depth, stop_depth)  
            interpolated_df = interpolate_data(depth_filtered_df)
            
    
            with st.expander("**Findings:**", expanded = False):
                st.divider()
                display_well_information()
                
                st.divider()
                display_curve_information()
                
                st.divider()
                display_curve_data_overview()
                
                st.divider()
                st.subheader('Evaluated Data')
                st.dataframe(interpolated_df)
                
                st.divider()
                st.markdown(f'''
                            **At depth of {top_depth} up to {bot_depth}**
                            ''')
                            
                matrix = "Sandstone"
                fluid = "Seawater"
                column = 'Sandstone (Seawater)'
                negative_val, normal_val, abnormal_val, null_val, total_val = categorize_porosity(column)
                interpretation(negative_val, normal_val, abnormal_val, null_val, total_val)
                
                matrix = "Limestone"
                fluid = "Seawater"
                column = 'Limestone (Seawater)'
                negative_val, normal_val, abnormal_val, null_val, total_val = categorize_porosity(column)
                interpretation(negative_val, normal_val, abnormal_val, null_val, total_val)
                
                matrix = "Dolomite"
                fluid = "Seawater"
                column = 'Dolomite (Seawater)'
                negative_val, normal_val, abnormal_val, null_val, total_val = categorize_porosity(column)
                interpretation(negative_val, normal_val, abnormal_val, null_val, total_val)
                
                matrix = "Sandstone"
                fluid = "Freshwater"
                column = 'Sandstone (Freshwater)'
                negative_val, normal_val, abnormal_val, null_val, total_val = categorize_porosity(column)
                interpretation(negative_val, normal_val, abnormal_val, null_val, total_val)
                
                matrix = "Limestone"
                fluid = "Freshwater"
                column = 'Limestone (Freshwater)'
                negative_val, normal_val, abnormal_val, null_val, total_val = categorize_porosity(column)
                interpretation(negative_val, normal_val, abnormal_val, null_val, total_val)
                
                matrix = "Dolomite"
                fluid = "Freshwater"
                column = 'Dolomite (Freshwater)'
                negative_val, normal_val, abnormal_val, null_val, total_val = categorize_porosity(column)
                interpretation(negative_val, normal_val, abnormal_val, null_val, total_val)
        

            st.markdown("### Data Visualization")
            col1, col2 = st.columns(2)
            mode_sandstone_seawater = col1.checkbox("Matrix: Sandstone | Fluid: Seawater")
            mode_limestone_seawater = col1.checkbox("Matrix: Limestone | Fluid: Seawater")
            mode_dolomite_seawater = col1.checkbox("Matrix: Dolomite | Fluid: Seawater")
            mode_sandstone_freshwater = col2.checkbox("Matrix: Sandstone | Fluid: Freshwater") 
            mode_limestone_freshwater = col2.checkbox("Matrix: Limestone | Fluid: Freshwater")
            mode_dolomite_freshwater = col2.checkbox("Matrix: Dolomite | Fluid: Freshwater")
            
            count_parameters = 1    
            if mode_sandstone_seawater:
                count_parameters += 1       
            if mode_limestone_seawater:
                count_parameters += 1  
            if mode_dolomite_seawater:
                count_parameters += 1  
            if mode_sandstone_freshwater:
                count_parameters += 1  
            if mode_limestone_freshwater:
                count_parameters += 1  
            if mode_dolomite_freshwater:
                count_parameters += 1  
    
            def configure_track(fig, track_num, x_title, x_range, y_title):
                fig.update_xaxes(
                    title=x_title,
                    ticks="inside",
                    nticks=5,
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
                    range=x_range,
                    row=1,
                    col=track_num
                )
                fig.update_yaxes(
                    ticks="inside",
                    autorange='reversed',
                    showline=True,
                    gridcolor='lightgray',
                    gridwidth=2,
                    showticklabels=True,
                    row=1,
                    col=track_num
                )
            
            trackname_1 = '''Sonic Log'''
            trackname_2 = 'Sonic Porosity SS-SW Scale (p.u.)'
            trackname_3 = 'Sonic Porosity LS-SW Scale (p.u.)'
            trackname_4 = 'Sonic Porosity DL-SW Scale (p.u.)'
            trackname_5 = 'Sonic Porosity SS-FW Scale (p.u.)'
            trackname_6 = 'Sonic Porosity LS-SW Scale (p.u.)'
            trackname_7 = 'Sonic Porosity DL-SW Scale (p.u.)'
                  
            # Initialize the figure with the appropriate number of columns
            fig = make_subplots(rows=1, cols=count_parameters, shared_yaxes=True)
            
            # Counter for the current subplot column
            current_col = 1
            
            # Track 1
            curve_1 = go.Scatter(x=interpolated_df['Sonic Log'], y=interpolated_df['Depth'], name=trackname_1)
            fig.add_trace(curve_1, row=1, col=current_col)
            fig.update_xaxes(
                title='Sonic Log',
                ticks="inside",
                nticks=5,
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
                range=[140, 40],
                row=1,
                col=1
            )
            fig.update_yaxes(
                title='Depth',
                ticks="inside",
                autorange='reversed',
                showline=True,
                gridcolor='lightgray',
                gridwidth=2,
                showticklabels=True,
                row=1,
                col=1
            )
            
            # Increment the counter
            current_col += 1
            
            # Checkboxes for other parameters
            # Add traces and configure tracks based on the checked parameters, adjusting the current_col accordingly
            
            if mode_sandstone_seawater:
                curve_2 = go.Scatter(x=interpolated_df["Sandstone (Seawater)"], y=interpolated_df['Depth'], name=trackname_2)
                fig.add_trace(curve_2, row=1, col=current_col)
                configure_track(fig, current_col, 'Sandstone (Seawater)', [-0.15, 1.51], 'Depth')
                current_col += 1
            
            if mode_limestone_seawater:
                curve_3 = go.Scatter(x=interpolated_df["Limestone (Seawater)"], y=interpolated_df['Depth'], name=trackname_3)
                fig.add_trace(curve_3, row=1, col=current_col)
                configure_track(fig, current_col, 'Limestone (Seawater)', [-0.15, 1.51], 'Depth')
                current_col += 1
            
            if mode_dolomite_seawater:
                curve_4 = go.Scatter(x=interpolated_df["Dolomite (Seawater)"], y=interpolated_df['Depth'], name=trackname_4)
                fig.add_trace(curve_4, row=1, col=current_col)
                configure_track(fig, current_col, 'Dolomite (Seawater)', [-0.15, 1.51], 'Depth')
                current_col += 1
            
            if mode_sandstone_freshwater:
                curve_5 = go.Scatter(x=interpolated_df["Sandstone (Freshwater)"], y=interpolated_df['Depth'], name=trackname_5)
                fig.add_trace(curve_5, row=1, col=current_col)
                configure_track(fig, current_col, 'Sandstone (Freshwater)', [-0.15, 1.51], 'Depth')
                current_col += 1
            
            if mode_limestone_freshwater:
                curve_6 = go.Scatter(x=interpolated_df["Limestone (Freshwater)"], y=interpolated_df['Depth'], name=trackname_6)
                fig.add_trace(curve_6, row=1, col=current_col)
                configure_track(fig, current_col, 'Limestone (Freshwater)', [-0.15, 1.51], 'Depth')
                current_col += 1
            
            if mode_dolomite_freshwater:
                curve_7 = go.Scatter(x=interpolated_df["Dolomite (Freshwater)"], y=interpolated_df['Depth'], name=trackname_7)
                fig.add_trace(curve_7, row=1, col=current_col)
                configure_track(fig, current_col, 'Dolomite (Freshwater)', [-0.15, 1.51], 'Depth')
                current_col += 1
            
            # Update layout and display the plot
            fig.update_layout(
                title=None,
                height=1000,
                width=2000
            )
            
            # Update traces
            for i in range(1, count_parameters + 1):
                fig.update_traces(legendgroup=f'track{i}', row=1, col=i)
            
            st.markdown("### Log Plot")
            if current_col == 2:
                fig.update_layout(
                    title=None,
                    height=1000,
                    width=350
                )
                st.plotly_chart(fig, use_container_width=False, theme=None)
                
            elif current_col == 3:
                fig.update_layout(
                    title=None,
                    height=1000,
                    width=700
                )
                st.plotly_chart(fig, use_container_width=False, scroll=True, theme=None)
    
            elif current_col == 4:
                fig.update_layout(
                    title=None,
                    height=1000,
                    width=1050
                )
                st.plotly_chart(fig, use_container_width=False, scroll=True, theme=None)
    
            elif current_col == 5:
                fig.update_layout(
                    title=None,
                    height=1000,
                    width=1400
                )
                st.plotly_chart(fig, use_container_width=False, scroll=True, theme=None)
    
            elif current_col == 6:
                fig.update_layout(
                    title=None,
                    height=1000,
                    width=1750
                )
                st.plotly_chart(fig, use_container_width=False, scroll=True, theme=None)
                
            else:
                fig.update_layout(
                    title=None,
                    height=1000,
                    width=2100
                )
                st.plotly_chart(fig, use_container_width=False, scroll=True, theme=None)
        
    except (KeyError):
        pass
        
