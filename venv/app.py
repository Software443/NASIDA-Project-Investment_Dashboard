import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import folium
from streamlit_folium import st_folium



# ---------- CONFIG ----------
st.set_page_config(page_title="NASIDA Dashboard", layout="wide")

# ---------- LOAD DATA ----------
# df = pd.read_excel(r"C:\Users\Hp\Documents\Copy of WK Investment Report dataset(1).xlsx", sheet_name="Sheet1", engine='openpyxl')

# Uncomment the line below to load data from Google Sheets
url = "https://docs.google.com/spreadsheets/d/13r0CIeA9pdQK1WwzmPsB9Klj44THwjDYFJylndrt_zs/export?format=csv"

# df = pd.read_csv(url, engine='python')
df = pd.read_csv(url, encoding='utf-8-sig')

df = pd.read_csv(url, encoding='utf-8-sig')

# Clean and convert 'Investment Amount' column to numeric
df["Investment Amount"] = df["Investment Amount"].astype(str).str.replace(",", "").str.strip()
df["Investment Amount"] = pd.to_numeric(df["Investment Amount"], errors="coerce")

# Clean and convert 'Jobs Created' column to numeric too (optional)
df["Jobs Created"] = pd.to_numeric(df["Jobs Created"], errors="coerce")


# df["Year"] = df["Year"].astype(str)
# df.dropna(subset=["Year", "Quarter", "Sector", "Project Status"], inplace=True)
# Convert 'Investment Amount' to numeric, handling errors
# df["Investment Amount"] = pd.to_numeric(df["Investment Amount"], errors='coerce')

# ---------- SIDEBAR FILTERS ----------
with st.sidebar:
    st.header("🔎 Filter Data")
    years = st.multiselect("Select Year(s)", sorted(df["Year"].notna().unique()), default=sorted(df["Year"].unique()))
    quarters = st.multiselect("Select Quarter(s)", df["Quarter"].unique(), default=df["Quarter"].unique())
    sectors = st.multiselect("Select Sector(s)", sorted(df["Sector"].unique()), default=sorted(df["Sector"].unique()))
    statuses = st.multiselect("Select Project Status", df["Project Status"].unique(), default=df["Project Status"].unique())

# ---------- APPLY FILTERS ----------
filtered_df = df[
    (df["Year"].isin(years)) &
    (df["Quarter"].isin(quarters)) &
    (df["Sector"].isin(sectors)) &
    (df["Project Status"].isin(statuses))
]

# ---------- KPI STYLING ----------
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
    background-color: #f7f9fc;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.kpi-title {
    font-size: 14px;
    color: #6c757d;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 26px;
    font-weight: bold;
    color: #2c3e50;
}
</style>
""", unsafe_allow_html=True)

# ---------- KPI CALCULATIONS ----------
total_investment = f"{filtered_df['Investment Amount'].sum() / 1e9:.2f} B"
total_jobs = f"{filtered_df['Jobs Created'].sum()}"
total_projects = f"{len(filtered_df)}"
total_actualized = f"{filtered_df[filtered_df['Project Status'] == 'Actualized'].shape[0]}"
top_sector = filtered_df["Sector"].value_counts().idxmax() if not filtered_df.empty else "N/A"

# ---------- DISPLAY KPI CARDS ----------
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-title">Total Investment (₦B)</div>
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
    image = Image.open(r"C:\Users\Hp\Downloads\Nasarawa_map-removebg-preview.png")  # path to your map image
    st.image(image, caption="Map of Nasarawa State")


# ---------- GDP TREND CHART ----------
gdp_data = pd.DataFrame({
    'Year': [2010, 2018, 2022],
    'Nasarawa': [3.29, 3.10, 4.60],  # in $ Billion
    # 'Benue': [0, 5.81, 10.58],  # in ₦ Billion
    # 'Kogi': [0, 0, 9.14]  # in ₦ Billion
})

df = pd.DataFrame(gdp_data)

df_melted = df.melt(id_vars='Year', var_name='State', value_name='GDP')

# Create line chart
fig = px.line(df_melted, 
              x='Year', 
              y='GDP', 
              color='State',
              title='📈 Nasarawa State GDP Trend vs. Neighboring States',
              markers=True,
              labels={'GDP': 'GDP (₦ Billion)', 'Year': 'Year'},
              line_shape='linear')

st.markdown("### 📈 Nasarawa State GDP Trend vs. Neighboring States")
st.plotly_chart(fig, use_container_width=True)

# ----------KPI Cards for GDP----------
st.markdown("### 📊 GDP Overview in 2022")

latest_year = df["Year"].max()
previous_year = latest_year - 1

cols = st.columns(len(df.columns) - 1)  # One column per state (excluding Year)

for i, state in enumerate(df.columns[1:]):
    latest_gdp = df.loc[df["Year"] == latest_year, state].values[0]
    prev_gdp = df.loc[df["Year"] == previous_year, state].values[0]
    change = ((latest_gdp - prev_gdp) / prev_gdp) * 100

    with cols[i]:
        st.metric(
            label=f"{state} GDP",
            value=f"{latest_gdp:,}B",
            delta=f"{change:.2f}%" if prev_gdp != 0 else "n/a"
        )


st.markdown("---")
st.markdown("#### Definitions:")
st.markdown('''
**Investment
Announcement**: An Investment Announcement refers
to a public declaration or commitment by an investor, company, or
institution to invest in Nasarawa State This includes expressions of
intent made or official agreements such as Memorandums of
Understanding ( and Letters of Intent LoIs)
            
**Investment
Actualized**: An Investment Actualized refers to an
investment that has moved beyond the announcement stage and has
commenced implementation This includes investments where
financial commitments have been deployed, business operations have
commenced, construction has begun, or capital expenditures have
been made within the State
''')

st.markdown("---")

# Separate actualized (completed) and announced (not completed)
actualized_investment = filtered_df[filtered_df['Project Status'] == 'Actualized']['Investment Amount'].sum()
announced_investment = filtered_df[filtered_df['Project Status'] != 'Actualized']['Investment Amount'].sum()

# Create a DataFrame for plotting
portfolio_data = pd.DataFrame({
    'Category': ['Actualized Investment', 'Announced Investment'],
    'Amount ($)': [actualized_investment, announced_investment]
})
# ---------- PORTFOLIO PIE CHART ----------
st.markdown("##### 📊 Investment Portfolio Overview")
import plotly.express as px

fig = px.pie(portfolio_data,
             values='Amount ($)',
             names='Category',
             title='Investment Portfolio: Actualized vs. Announced',
             hole=0.4,
             color_discrete_sequence=['#00CC96', '#636EFA'])  # green and blue
             
st.plotly_chart(fig, use_container_width=True)

st.dataframe(portfolio_data, use_container_width=True)
st.markdown("---")

#  Replace these numbers with your actual data
fdi_amount = 458_000_000
ddi_amount = 8_780_000
total_amount = fdi_amount + ddi_amount

# Prepare DataFrame
data = pd.DataFrame({
    "Source": ["FDI", "DDI"],
    "Amount": [fdi_amount, ddi_amount]
})
# Convert amounts to millions for better readability
data["Amount"] = data["Amount"] / 1_000_000  # Convert to millions

# ---------- STREAMLIT UI ----------
# st.set_page_config(page_title="Investment Sources", layout="centered")

st.markdown("##### 💼 Actualized Investments by Source")
st.write(f"Total: ₦{total_amount:,.0f}")

# ---------- PLOTLY CHART ----------
fig = px.pie(
    data,
    values="Amount",
    names="Source",
    hole=0.5,  # donut style
    color="Source",
    color_discrete_map={"FDI": "#008B8B", "DDI": "#00CED1"}
)

# Add percentage + amount in labels
fig.update_traces(
    textinfo="label+percent+value",
    texttemplate="%{label}<br>₦%{value:,.2f}M"
)

fig.update_layout(
    showlegend=False,
    annotations=[dict(
        text=f"₦{total_amount/1e6:.2f}M<br>Total",
        x=0.5, y=0.5, font_size=16, showarrow=False
    )]
)

st.plotly_chart(fig, use_container_width=True)

# ---------- CHART 1: Investment Over Years ----------
inv_year = filtered_df.groupby("Year")["Investment Amount"].sum().reset_index()
fig1 = px.bar(inv_year, x="Year", y="Investment Amount", title="💰 Investment Over Years", text_auto=".2s")
st.plotly_chart(fig1, use_container_width=True)

# ---------- CHART 2: Jobs Created by Sector ----------
jobs_sector = filtered_df.groupby("Sector")["Jobs Created"].sum().reset_index()
fig2 = px.bar(jobs_sector, x="Sector", y="Jobs Created", color="Sector", title="👷 Jobs Created by Sector", text_auto=True)
st.plotly_chart(fig2, use_container_width=True)

# ---------- CHART 3: Investment by LGA ----------
inv_lga = filtered_df.groupby("LGA")["Investment Amount"].sum().reset_index().sort_values(by="Investment Amount", ascending=False)
fig3 = px.bar(inv_lga, x="Investment Amount", y="LGA", orientation="h", title="🏙️ Investment by LGA", text_auto=".2s")
st.plotly_chart(fig3, use_container_width=True)

# ---------- CHART 4: Investment by Sector ----------
inv_sector = filtered_df.groupby("Sector")["Investment Amount"].sum().reset_index().sort_values(by="Investment Amount", ascending=False)
fig4 = px.pie(inv_sector, names="Sector", values="Investment Amount", title="📌 Investment by Sector", hole=0.3)
st.plotly_chart(fig4, use_container_width=True)

# ---------- ANNEXURE SECTION ----------
st.markdown("##### 📎 Annexures")

st.markdown("""
**Investment Announcement**: An Investment Announcement refers to a public declaration or commitment by an investor, company, or institution to invest in Nasarawa State.

**Investment Actualized**: An Investment Actualized refers to an investment that has commenced implementation such as construction, operations, or capital deployment.
""")

# ---------- FILTERED ANNEXURE TABLES ----------
# st.markdown("###### ✅ Annexure 2: *Actualized Projects*")
# df2 = filtered_df[filtered_df['Project Status'] == 'Completed']
# st.dataframe(df2.head(10), use_container_width=True)

# st.markdown("###### 📣 Annexure 1: *Investment Announcements*")
# df1 = filtered_df[filtered_df['Project Status'] == 'Ongoing']
# st.dataframe(df1.head(10), use_container_width=True)
st.markdown("##### ✅ Annexure 2: *Actualized Projects*")
df2 = filtered_df[filtered_df['Project Status'] == 'Actualized'].copy()
df2["Year"] = df2["Year"].astype(str)
st.dataframe(df2.head(10), use_container_width=True, hide_index=True)

st.markdown("##### 📣 Annexure 1: *Investment Announcements*")
# df1 = filtered_df[filtered_df['Project Status'].isin(['Announced' or 'Delayed'])].copy()
df1 = filtered_df[(filtered_df['Project Status'] == 'Announced') | (filtered_df['Project Status'] == 'Delayed')].copy()
df1["Year"] = df1["Year"].astype(str)
st.dataframe(df1.head(10), use_container_width=True, hide_index=True)


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
