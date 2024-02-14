import streamlit as st
from streamlit_option_menu import option_menu
import Home, About, Guide, Info, Interpretation


st.set_page_config(
    page_title = "Sonic Log Web App",
    layout='wide'
    )
class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self, main_menu):
        for app in self.apps:   
            if main_menu == app["title"]:
                app["function"]()

# Create an instance of MultiApp
multi_app = MultiApp()

# Add your apps to the MultiApp instance
multi_app.add_app("Home", Home.app)
multi_app.add_app("About", About.app)
multi_app.add_app("User's Guide", Guide.app)
multi_app.add_app("Additional Info", Info.app)
multi_app.add_app("Interpretation", Interpretation.app)


main_menu = option_menu(
    None,
    options=["Home", "About", "User's Guide", "Additional Info", "Interpretation"],
    icons=["house", "patch-question", "journal-bookmark", "lightbulb", "calculator"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)

# Run the selected app
multi_app.run(main_menu)
