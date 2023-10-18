import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# Sample data with common names, species, watering intervals, average sunlight exposure, and typical water consumption (ml).
PLANTS = {
    "Snake Plant": {"species": "Sansevieria trifasciata", "interval": 14, "avg_sunlight": 6, "typical_water": 200, "image": "https://indoorgardening.com/wp-content/uploads/2021/02/Vipers-Bowstring-Snake-Plant-150x150.jpg"},
    "Spider Plant": {"species": "Chlorophytum comosum", "interval": 7, "avg_sunlight": 6, "typical_water": 250, "image":"https://indoorgardening.com/wp-content/uploads/2021/03/Bonnie-Spider-Plant.jpg"},
    "Pothos": {"species": "Epipremnum aureum", "interval": 7, "avg_sunlight": 6, "typical_water": 250, "image":"https://indoorgardening.com/wp-content/uploads/2022/08/Global-Green-Pothos-768x432.jpg"},
    "Fiddle Leaf Fig": {"species": "Ficus lyrata", "interval": 10, "avg_sunlight": 6, "typical_water": 300, "image":"https://indoorgardening.com/wp-content/uploads/2022/08/Light-768x432.jpg"},
    "Peace Lily": {"species": "Spathiphyllum wallisii", "interval": 4, "avg_sunlight": 4, "typical_water": 200, "image":"https://indoorgardening.com/wp-content/uploads/2021/03/Peace-Lily-Guide-768x396.jpg"},
}

st.title('House Plant Buddy')
st.subheader('Smart Water Reminders')

# Add a new entry
st.sidebar.title('Add a new plant')
common_name = st.sidebar.selectbox('Common Name', list(PLANTS.keys()))
species = PLANTS[common_name]["species"]
watering_interval = PLANTS[common_name]["interval"]
avg_sunlight = PLANTS[common_name]["avg_sunlight"]
time_of_last_watering = st.sidebar.date_input('Date of Last Watering', datetime.datetime.now())
amount_of_water = st.sidebar.slider('Amount of Water (ml)', 10, 1000, 100)
medium_of_planting = st.sidebar.text_input('Medium of Planting')
location = st.sidebar.text_input('Location of the Plant')
height_of_plant = st.sidebar.number_input('Height of the Plant (cm)', min_value=0.1)
sunlight_exposure = st.sidebar.slider('Sunlight Exposure (hours/day)', 0.0, 12.0, float(avg_sunlight))

# Adjust watering interval based on sunlight exposure
adjustment_factor = 1 - 0.1 * (sunlight_exposure - avg_sunlight)
adjusted_interval = max(1, int(watering_interval * adjustment_factor))

if st.sidebar.button('Add Plant'):
    if 'plants' not in st.session_state:
        st.session_state.plants = []
    
    st.session_state.plants.append({
        "Common Name": common_name,
        "Species": species,
        "Watering Interval (days)": adjusted_interval,
        "Date of Last Watering": time_of_last_watering,
        "Amount of Water": amount_of_water,
        "Typical Water Amount": PLANTS[common_name]["typical_water"],
        "Medium of Planting": medium_of_planting,
        "Location": location,
        "Height of Plant": height_of_plant,
        "Sunlight Exposure": sunlight_exposure,
        "Next Watering Date": time_of_last_watering + datetime.timedelta(days=adjusted_interval)
    })
    st.sidebar.success('Plant added successfully!')

# Display the entries, reminders, and the graph
if 'plants' in st.session_state:
    df = pd.DataFrame(st.session_state.plants)
    st.write(df)

    st.subheader('Watering Reminders')
    today = datetime.datetime.now().date()
    for plant in st.session_state.plants:
        if plant["Next Watering Date"] <= today:
            st.write(f"Time to water your {plant['Common Name']} in {plant['Location']}!")
    
    # Plotting with Plotly
    st.subheader('Water Consumption Comparison')
    fig = px.bar(df, x="Common Name", y=["Amount of Water", "Typical Water Amount"],
                 title="Actual vs Typical Water Consumption", labels={'value': 'Water Amount (ml)'}, barmode='group')
    st.plotly_chart(fig)

else:
    st.write("No plants added yet.")

st.caption ("Demo. app by Prathmesh S")
