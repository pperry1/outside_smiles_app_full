import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("Outside Smiles | Plan My Day 🧭")

# Sidebar
st.sidebar.header("Customize Your Day")
selected_zip = st.sidebar.selectbox("Select ZIP Code", ["21201", "21217", "21223", "21205", "21215"])
time_window = st.sidebar.slider("Time Available (hours)", 1, 8, 3)
needs = st.sidebar.multiselect("What do you need today?", ["Grocery Stores", "Clinics", "Restrooms", "Walking Trails", "Community Gardens", "Maternal Health Hospitals"])

# Load data
def load_csv(name):
    return pd.read_csv(f"data/{name}.csv")

layer_map = {
    "Grocery Stores": ("grocery_stores_in_food_deserts", "green", "shopping-cart"),
    "Clinics": ("clinics", "blue", "plus-sign"),
    "Restrooms": ("public_restrooms", "cadetblue", "info-sign"),
    "Walking Trails": ("walking_trails", "purple", "road"),
    "Community Gardens": ("community_gardens", "darkgreen", "leaf"),
    "Maternal Health Hospitals": ("maternal_health_hospitals", "pink", "heart")
}

# Map init
m = folium.Map(location=[39.2904, -76.6122], zoom_start=12, control_scale=True)

# Add layers based on needs
for need in needs:
    file, color, icon = layer_map[need]
    df = load_csv(file)
    for _, row in df.iterrows():
        popup = f"<b>{row['name']}</b><br>{row['address']}<br><i>{row.get('description', '')}</i>"
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon=icon)
        ).add_to(m)

# Show map
st_data = st_folium(m, width=1300, height=600)

# Footer
st.markdown("💬 [Suggest a Resource](https://forms.gle/your-form-link)  |  🕒 Last Updated: April 2025")