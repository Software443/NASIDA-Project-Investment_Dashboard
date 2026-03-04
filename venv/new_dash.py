import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
from PIL import Image

# ---------- CONFIG ----------
st.set_page_config(page_title="NASIDA Dashboard", layout="wide", initial_sidebar_state="expanded")

# ---------- LOAD DATA ----------
# df = pd.read_excel(r"C:\Users\Hp\Documents\Copy of WK Investment Report dataset(1).xlsx", sheet_name="Sheet1", engine='openpyxl')

green_palette = [
    "#0B3D2E",  # deep forest green
    "#145A32",  # dark green
    "#1E8449",  # primary green
    "#27AE60",  # medium green
    "#52BE80",  # soft green
    "#A9DFBF"   # light green
]

url = "https://docs.google.com/spreadsheets/d/13r0CIeA9pdQK1WwzmPsB9Klj44THwjDYFJylndrt_zs/export?format=csv"

# df = pd.read_csv(url, engine='python')
df = pd.read_csv(url, encoding='utf-8-sig')

# Clean and convert 'Investment Amount' column to numeric
df["Worth"] = df["Worth"].astype(str).str.replace(",", "").str.strip()
df["Worth"] = pd.to_numeric(df["Worth"], errors="coerce")

# Clean and convert 'Jobs Created' column to numeric too (optional)
df["Jobs Created"] = pd.to_numeric(df["Jobs Created"], errors="coerce")


# df["Year"] = df["Year"].astype(str)
# df.dropna(subset=["Year", "Quarter", "Sector", "Project Status"], inplace=True)
# Convert 'Investment Amount' to numeric, handling errors
# df["Investment Amount"] = pd.to_numeric(df["Investment Amount"], errors='coerce')

# ---------- SIDEBAR FILTERS ----------
with st.sidebar:
    st.header("🔎 Filter Data")

    # Create options with "All"
    year_options = ["All"] + sorted(df["Year"].dropna().unique().tolist())
    quarter_options = ["All"] + sorted(df["Quarter"].dropna().unique().tolist())
    sector_options = ["All"] + sorted(df["Sector"].dropna().unique().tolist())
    status_options = ["All"] + sorted(df["Status"].dropna().unique().tolist())

    # Single select dropdown
    selected_year = st.selectbox("Select Year", year_options)
    selected_quarter = st.selectbox("Select Quarter", quarter_options)
    selected_sector = st.selectbox("Select Sector", sector_options)
    selected_status = st.selectbox("Select Project Status", status_options)

# ---------- APPLY FILTERS ----------
filtered_df = df[
    (df["Year"].isin([selected_year]) if selected_year != "All" else df["Year"].isin(df["Year"].unique())) &
    (df["Quarter"].isin([selected_quarter]) if selected_quarter != "All" else df["Quarter"].isin(df["Quarter"].unique())) &
    (df["Sector"].isin([selected_sector]) if selected_sector != "All" else df["Sector"].isin(df["Sector"].unique())) &
    (df["Status"].isin([selected_status]) if selected_status != "All" else df["Status"].isin(df["Status"].unique()))
]

st.title("📊 NASIDA Project Investment Dashboard")

st.markdown("""
<style>
.kpi-container {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 2rem;
}
.kpi-card {
    flex: 1;
    background-color: #0d5721;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.kpi-title {
    font-size: 14px;
    color: #f0f5f1;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 26px;
    font-weight: bold;
    color: #f0f5f1;
}
</style>
""", unsafe_allow_html=True)

# ---------- KPI CALCULATIONS ----------
total_investment = f"{filtered_df['Worth'].sum() / 1e9:.1f} B"
total_jobs = f"{filtered_df['Jobs Created'].sum()}"
total_projects = f"{len(filtered_df)}"
total_actualized = f"{filtered_df[filtered_df['Status'] == 'Actualized'].shape[0]}"
top_sector = filtered_df["Sector"].value_counts().idxmax() if not filtered_df.empty else "N/A"

# ---------- DISPLAY KPI CARDS ----------
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-title">Total Worth ($B)</div>
        <div class="kpi-value">{total_investment}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Total Jobs</div>
        <div class="kpi-value">{total_jobs}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Total Projects</div>
        <div class="kpi-value">{total_projects}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Total Actualized</div>
        <div class="kpi-value">{total_actualized}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Top Sector</div>
        <div class="kpi-value">{top_sector}</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

import streamlit.components.v1 as components

carousel_html = """
<style>
.slider {
  width: 100%;
  height: 350px;
  overflow: hidden;
  position: relative;
  border-radius: 15px;
}

.slides {
  display: flex;
  width: 400%;
  height: 100%;
  animation: slide 20s infinite;
}

.slides img {
  width: 100%;
  height: 350px;
  object-fit: cover;
}

@keyframes slide {
  0% {margin-left: 0%;}
  20% {margin-left: 0%;}
  25% {margin-left: -100%;}
  45% {margin-left: -100%;}
  50% {margin-left: -200%;}
  70% {margin-left: -200%;}
  75% {margin-left: -300%;}
  95% {margin-left: -300%;}
  100% {margin-left: 0%;}
}
</style>

<div class="slider">
  <div class="slides">
    <img src="https://nasida.na.gov.ng/img/test-bg.cf2780a8.png">
    <img src="https://nasida.na.gov.ng/img/test-bg1.3985ef28.png">
    <img src="https://nasida.na.gov.ng/img/mining.e3f9f7e1.png">
    <img src="https://nasida.na.gov.ng/img/main-3-bg.4038b733.png">
  </div>
</div>
"""

components.html(carousel_html, height=370)

# Sample GDP data (replace with actual data)
# gdp_data = pd.DataFrame({
#     'Year': [2017, 2018, 2019, 2020, 2021, 2022, 2023],
#     'GDP': [410, 455, 478, 460, 500, 530, 570]  # in ₦ Billion
# })

# # Create line chart
# fig = px.line(gdp_data, 
#               x='Year', 
#               y='GDP', 
#               title='Nasarawa State GDP Trend',
#               markers=True,
#               labels={'GDP': 'GDP (₦ Billion)', 'Year': 'Year'},
#               line_shape='linear')

# # Add to Streamlit
# st.markdown("### 📈 Nasarawa State GDP Trend")
# st.plotly_chart(fig, use_container_width=True)

# st.write("""
# Nasarawa is a state in the Northern central region of Nigeria, bordered by Kaduna to the north, Taraba and Plateau to the east, 
# Benue and Kogi to the south, and Federal Capital Territory to the west. It is known for its rich agricultural resources, mineral 
# deposits, and cultural heritage. The state capital is Lafia. Kaduna offers a wide range of opportunities to private sector investors
# in agriculture, mining and tourism amongst others. Nasarawa is a haven for investors, offering a unique combination of resources, market
# and business environment rivalled by no other state in Nigeria.
# """)

st.subheader("Nasarawa State Overview")

col1, col2 = st.columns([1, 1])  # equal width columns

with col1:
    st.markdown("""
    **Nasarawa State** is located in the North Central region of Nigeria.  
    - Capital: Lafia  
    - Population: ~2.5 million  
    - Key sectors: Agriculture, Solid Minerals, and Trade  
    - Known as: *Home of Solid Minerals*  
    """)

with col2:
    image = Image.open(r"C:\Users\Hp\Downloads\Nasarawa_map.jpg")  # path to your map image
    st.image(image, caption="Map of Nasarawa State")

# # ---------- GDP TREND CHART ----------
# gdp_data = pd.DataFrame({
#     'Year': [2010, 2011, 2012, 2013, 2014, 2015],
#     'Nasarawa': [3.02, 3.19, 3.38, 3.58, 3.81, 4.06],  # in $ Billion
#     # 'Benue': [0, 5.81, 10.58],  # in ₦ Billion
#     # 'Kogi': [0, 0, 9.14]  # in ₦ Billion
# })

# df = pd.DataFrame(gdp_data)

# df_melted = df.melt(id_vars='Year', var_name='State', value_name='GDP')

# # Create line chart
# fig = px.line(df_melted, 
#               x='Year', 
#               y='GDP', 
#               color_discrete_sequence=green_palette,
#               title='📈 Nasarawa State GDP Trend vs. Neighboring States',
#               markers=True,
#               labels={'GDP': 'GDP (₦ Billion)', 'Year': 'Year'},
#               line_shape='linear')

# st.markdown("### 📈 Nasarawa State GDP Trend vs. Neighboring States")
# st.plotly_chart(fig, use_container_width=True)

# ----------KPI Cards for GDP----------
# st.markdown("### 📊 GDP Overview in 2022")

# latest_year = df["Year"].max()
# previous_year = latest_year - 1

# cols = st.columns(len(df.columns) - 1)  # One column per state (excluding Year)

# for i, state in enumerate(df.columns[1:]):
#     latest_gdp = df.loc[df["Year"] == latest_year, state].values[0] if not df.loc[df["Year"] == latest_year, state].empty else 0
#     prev_gdp = df.loc[df["Year"] == previous_year, state].values[0] if not df.loc[df["Year"] == previous_year, state].empty else 0
#     change = ((latest_gdp - prev_gdp) / prev_gdp) * 100

#     with cols[i]:
#         st.metric(
#             label=f"{state} GDP",
#             value=f"{latest_gdp:,}B",
#             delta=f"{change:.2f}%" if prev_gdp != 0 else "n/a"
#         )


# ---------- CHARTS IN TWO COLUMNS ----------
col1, col2 = st.columns(2)

with col1:
    # CHART 1: Investment Over Years
    inv_year = filtered_df.groupby("Year")["Worth"].sum().reset_index()
    fig1 = px.bar(inv_year, x="Year", 
                  y="Worth", 
                  color_discrete_sequence=green_palette,
                  title="💰 Investment Over Years", 
                  text_auto=".2s")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # CHART 2: Jobs Created by Sector
    jobs_sector = filtered_df.groupby("Sector")["Jobs Created"].sum().reset_index()
    fig2 = px.bar(jobs_sector, x="Sector", 
                  y="Jobs Created", 
                  color_discrete_sequence=green_palette,
                  title="👷 Jobs Created by Sector", 
                  text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)

# Next row of two columns
col3, col4 = st.columns(2)

with col3:
    # CHART 3: Investment by LGA
    inv_lga = filtered_df.groupby("LGA")["Worth"].sum().reset_index().sort_values(by="Worth", ascending=False)
    fig3 = px.bar(inv_lga, x="Worth", 
                  y="LGA", 
                  color_discrete_sequence=green_palette,
                  orientation="h", 
                  title="🏙️ Investment by LGA", 
                  text_auto=".2s")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    # CHART 4: Investment by Sector
    inv_sector = filtered_df.groupby("Sector")["Worth"].sum().reset_index().sort_values(by="Worth", ascending=False)
    fig4 = px.pie(inv_sector, 
                  names="Sector", 
                  values="Worth", 
                  color_discrete_sequence=green_palette,
                  title="📌 Investment by Sector", 
                  hole=0.3)
    st.plotly_chart(fig4, use_container_width=True)

# ---------- ANNEXURE SECTION ----------

st.markdown("##### 📎 Annexures")

st.markdown("""
**Investment Announcement**: An Investment Announcement refers to a public declaration or commitment by an investor, company, or institution to invest in Nasarawa State.

**Investment Actualized**: An Investment Actualized refers to an investment that has commenced implementation such as construction, operations, or capital deployment.
""")

st.markdown("""
<style>
.green-table {
    width: 100%;               /* Make table take 100% of container */
    max-width: 100%;           /* Prevent overflow */
    table-layout: fixed;       /* Fix column widths to fit */
    border-collapse: collapse;
    border-radius: 12px;
    overflow: hidden;
}

.green-table thead {
    background-color: #0B3D2E;
    color: white;
}

.green-table th, .green-table td {
    padding: 10px;
    border-bottom: 1px solid #E8F5E9;
    text-align: center;       /* Center align text */
    word-wrap: break-word;    /* Wrap long text */
}

.green-table tr:nth-child(even) {
    background-color: #F4FBF6;
}

.green-table tr:hover {
    background-color: #E8F5E9;
}

/* Optional: make the table scrollable horizontally on small screens */
.green-table-container {
    overflow-x: auto;
}
</style>
""", unsafe_allow_html=True)
# ---------- FILTERED ANNEXURE TABLES ----------
# st.markdown("###### ✅ Annexure 2: *Actualized Projects*")
# df2 = filtered_df[filtered_df['Project Status'] == 'Completed']
# st.dataframe(df2.head(10), use_container_width=True)

# st.markdown("###### 📣 Annexure 1: *Investment Announcements*")
# df1 = filtered_df[filtered_df['Project Status'] == 'Ongoing']
# st.dataframe(df1.head(10), use_container_width=True)
st.markdown("##### ✅ Annexure 2: *Actualized Projects*")
df2 = filtered_df[filtered_df['Status'] == 'Actualized'].copy()
df2["Year"] = df2["Year"].astype(str)
# st.dataframe(df2.head(10), use_container_width=True, hide_index=True)
st.markdown(df2.head(10).to_html(classes="green-table", index=False), unsafe_allow_html=True)

st.markdown("##### 📣 Annexure 1: *Investment Announcements*")
# df1 = filtered_df[filtered_df['Project Status'].isin(['Announced' or 'Delayed'])].copy()
df1 = filtered_df[(filtered_df['Status'] == 'Announced') | (filtered_df['Status'] == 'Delayed')].copy()
df1["Year"] = df1["Year"].astype(str)
# st.dataframe(df1.head(10), use_container_width=True, hide_index=True)
st.markdown(df1.head(10).to_html(classes="green-table", index=False), unsafe_allow_html=True)

# =============================
# Folium Map interactive map
# =============================

st.markdown("##### 🗺️ Investment Locations Map")

# coordinates roughly based on Nasarawa State
map_center = folium.Map(location=[8.5, 8.5], zoom_start=7)

# Add markers for Lafia
# folium.Marker(
#     location=[8.5, 8.5],
#     popup="Lafia",
#     icon=folium.Icon(color='blue', icon='info-sign')
# ).add_to(map_center)

# Add markers for other LGAs (example coordinates, replace with actual)
lgas = {
     "Akwanga": [8.9167, 8.4000],
    "Awe": [8.0833, 9.1333],
    "Doma": [8.4000, 8.3667],
    "Karu": [9.0167, 7.6333],
    "Keana": [8.1500, 8.8000],
    "Keffi": [8.8500, 7.8833],
    "Kokona": [8.9167, 8.0000],
    "Lafia": [8.5000, 8.5000],
    "Nasarawa": [8.5333, 7.7167],
    "Nasarawa Egon": [8.7667, 8.5333],
    "Obi": [8.3833, 8.7500],
    "Toto": [8.3833, 7.0833],
    "Wamba": [8.9333, 8.6000]
}

# Add markers for each LGA
for lga, coords in lgas.items():
    folium.Marker(
        location=coords,
        popup=f"{lga}",
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(map_center)


# Display the map in Streamlit
st_folium(map_center, width=1200, height=500)

current_year = pd.to_datetime("today").year

# Add footer
st.markdown("---")
st.markdown(f"""<div style='text-align: center; color: #555; font-size: 12px'> &copy; {current_year} NASIDA Dashboard. All rights reserved.
            </div>""", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 10px'> <em> Powered by Streamlit and Plotly and proudly sponsored by Gabriel Simeon </em></p>", unsafe_allow_html=True)

st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <div style='text-align: center; padding: 15px; font-size: 14px; color: #555;'>
        <div style='margin-top: 5px;'>
            <a href="https://facebook.com/nasa" target="_blank" style="margin: 0 10px; color: #3b5998;">
                <i class="fab fa-facebook fa-lg"></i>
            </a>
            <a href="https://x.com/NasarawaInvest" target="_blank" style="margin: 0 10px; color: #1da1f2;">
                <i class="fab fa-twitter fa-lg"></i>
            </a>
            <a href="https://www.linkedin.com/company/nasarawa-investment-and-development-agency/" target="_blank" style="margin: 0 10px; color: #0077b5;">
                <i class="fab fa-linkedin fa-lg"></i>
            </a>
            <a href="https://www.instagram.com/nasarawa_invest/" target="_blank" style="margin: 0 10px; color: #e1306c;">
                <i class="fab fa-instagram fa-lg"></i>
            </a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
