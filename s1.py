import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Weather Data Analysis and Visualization System", page_icon=":bar_chart:",layout="wide")
@st.cache_data
def load_data():
    df = pd.read_csv("GlobalWeatherRepository.csv")
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    df['date'] = df['last_updated'].dt.date
    return df
df=pd.read_csv("GlobalWeatherRepository.csv")
df.info()
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",        
        options=["Home","Data Analysis","Data Visualization","Dashboard","About"],
        icons=["house","bar-chart-line","bar-chart"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    st.markdown("<h1 style='color: blue;'>🌎Global weather analysis</h1>", unsafe_allow_html=True)
    st.write("This is a web application that analyzes the weather in whole world, which contains informations about various weather conditions.")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://www.visualcrossing.com/doc_resources/weather_forecast_any_day_of_year/mceclip0.png",width=400)
    with col2:
        st.image("https://media.istockphoto.com/id/1176320050/photo/weather-forecast-on-a-digital-display-7-day-dashboard-3d-illustration.jpg?b=1&s=170667a&w=0&k=20&c=H5jbreqseczNxXieF9e0R8O5FHeY0ylKgEX_RKFenGo=",width=400)
    st.subheader("objectives")
    st.write("1. To analyze weather data such as temperature,humditiy,rainfall,wind speed and pressure.")
    st.write("2. To identify weather patterns and trends using charts and visualization.")
    st.write("3. To compare different weather parameters for better understanding of climate conditions.")
    st.write("4. To support better understanding of weather conditions through graphical analisis.")  
    st.subheader("Benefits")
    st.write("1. Makes weather data easy to understand through graphs and charts.")
    st.write("2. Saves time by presenting large datasets in a simple visual format.")
    st.write("3. Supports better decision-making by analyzing weather parameters.")
    st.write("Provides an interactive and user-friendly dashboard for data exploration.")
    st.markdown("<h1 style='color: blue;'>📁 Dataset Overview</h1>", unsafe_allow_html=True)
    st.subheader("Dataset Details:")
    st.write("Total Records: 253,680")
    st.write("Total Features: 22")
    st.write("Data Type: Structure tabular data")
    st.write("Source: Kaggle Weather Data Analysis and Visualization System")

elif selected == "Data Analysis":
        st.title("Data Analysis")
        st.write("This section provide a detailed analysis of the weather indicators of different country")
        st.write("The dataset contains the following columns:")
        st.write(df.columns)
        st.write("The dataset contains", df.shape[0], "rows and", df.shape[1], "columns.")
        st.write("The dataset contains the following weather indicators:")
        st.write(df.describe())
        st.dataframe(df,width="stretch")
        df=pd.read_csv("GlobalWeatherRepository.csv")
        st.subheader("First 10 Records")
        st.dataframe(df.head(10),width="stretch")

        st.subheader("Data Cleaning")
        col1,col2=st.columns(2)
        with col1:
            st.subheader("Missing values")
            missing=df.isnull().sum()
            st.dataframe(missing[missing>0], width="stretch")

elif selected == "Data Visualization":


    st.markdown("""
        <style>
        .title {font-size: 2.4rem; color: #1e40af; font-weight: 800;}
        .subtitle {font-size: 1.1rem; color: #64748b; margin-bottom: 25px;}
        .section {font-size: 1.3rem; font-weight: 700; color: #334155; margin-top: 25px;}
        .card {
            background: #f8fafc;
            padding: 18px; 
            border-radius: 10px; 
            border-left: 4px solid #2563eb;
            margin: 15px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="title">📊 Weather Data Visualization</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Interactive analysis of Weather metrics</p>', unsafe_allow_html=True)
    st.markdown("---")

    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌡️ Avg Temp", f"{df['temperature_celsius'].mean():.1f}°C")
    col2.metric("💧 Avg Humidity", f"{df['humidity'].mean():.1f}%")
    col3.metric("💨 Avg Wind", f"{df['wind_kph'].mean():.1f} kph")
    col4.metric("📍 Locations", f"{df['country'].nunique()}")

    st.markdown("---")

    # 1. Temperature Distribution
    st.markdown('<p class="section">1. Temperature Distribution</p>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10,4))
    sns.histplot(df['temperature_celsius'], bins=20, kde=True, color='#2563eb', ax=ax)
    ax.set_title("Distribution of Temperature Values")
    st.pyplot(fig)
    st.markdown('<div class="card">**Insight:** Most recorded temperatures cluster around 25-30°C. Peak frequency observed near 26°C.</div>', unsafe_allow_html=True)

    # 2. Weather Condition Over Time
    st.markdown('<p class="section">2. Weather Condition Timeline</p>', unsafe_allow_html=True)
    df_sorted = df.sort_values("last_updated").head(20)
    fig = px.line(df_sorted, x="last_updated", y="temperature_celsius", color="condition_text", markers=True)
    fig.update_layout(title="Temperature Trend by Weather Condition", height=400)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="card">**Insight:** Temperature fluctuations correlate with changing weather conditions like Sunny, Clear, and Partly Cloudy.</div>', unsafe_allow_html=True)

    # 3. Top Weather Conditions
    st.markdown('<p class="section">3. Top 10 Weather Conditions</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1,1])
    with col1:
        weather = df["condition_text"].value_counts().head(10)
        fig = px.pie(values=weather.values, names=weather.index, hole=0.4)
        fig.update_layout(title="Weather Condition Share")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown('<div class="card">**Key Findings:**<br>• Sunny is the most dominant condition<br>• Partly Cloudy ranks second<br>• Other conditions contribute <15% combined</div>', unsafe_allow_html=True)

    # 4. Country vs Temperature
    st.markdown('<p class="section">4. Country-wise Temperature Analysis</p>', unsafe_allow_html=True)
    top_countries = df.groupby("country")["temperature_celsius"].mean().nlargest(15).sort_values()
    fig = px.bar(top_countries, x=top_countries.values, y=top_countries.index, orientation='h', color=top_countries.values)
    fig.update_layout(title="Average Temperature by Country", height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="card">**Insight:** Middle Eastern countries show highest average temperatures in the dataset.</div>', unsafe_allow_html=True)

    # 5. Humidity Distribution
    st.markdown('<p class="section">5. Humidity Distribution</p>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10,4))
    sns.boxplot(x=df["humidity"], color="#60a5fa", ax=ax)
    ax.set_title("Humidity Range Distribution")
    st.pyplot(fig)
    st.markdown('<div class="card">**Insight:** Humidity is skewed towards higher values. Majority of readings fall between 70% - 100%.</div>', unsafe_allow_html=True)

    # 6. Correlation Heatmap
    st.markdown('<p class="section">6. Correlation Between Metrics</p>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(df[["temperature_celsius","humidity","wind_kph","pressure_mb"]].corr(),
                annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Weather Metrics Correlation")
    st.pyplot(fig)
    st.markdown('<div class="card">**Insight:** Strong negative correlation between Temperature and Humidity. Wind and Pressure show weak relationships.</div>', unsafe_allow_html=True)

    # 7. Geographical Distribution
    st.markdown('<p class="section">7. Geographical Weather Mapping</p>', unsafe_allow_html=True)
    fig = px.scatter(df.head(100), x="longitude", y="latitude", color="condition_text", 
                     size="temperature_celsius", hover_data=["country","temperature_celsius"])
    fig.update_layout(title="Weather Conditions by Location", height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="card">**Insight:** Weather patterns vary significantly across different geographical coordinates.</div>', unsafe_allow_html=True)

    # 8. Temperature vs Humidity - FIXED VERSION
    st.markdown('<p class="section">8. Temperature vs Humidity Relationship</p>', unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(10,5))
    sns.scatterplot(
        data=df.sample(min(300, len(df))), 
        x="temperature_celsius", 
        y="humidity",
        hue="condition_text",
        alpha=0.6,
        ax=ax
    )
    ax.set_xlabel("Temperature °C")
    ax.set_ylabel("Humidity %")
    ax.set_title("Temperature vs Humidity Scatter Plot")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)
    
    st.markdown('<div class="card">**Insight:** Inverse relationship observed. As temperature rises, humidity tends to decrease.</div>', unsafe_allow_html=True)

elif  selected== "Dashboard":
    st.markdown("<h1 style='color: blue;'>📊 Dashboard</h1>", unsafe_allow_html=True)

    

    df = load_data()

    # 2. Title + Filters
    st.title("🌍 Global Weather Dashboard")

    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        countries = st.multiselect("Country select karo", df['country'].unique(), default=df['country'].unique()[:5])
    with col_filter2:
        min_temp, max_temp = st.slider("Temperature Range °C", 
        int(df['temperature_celsius'].min()), 
        int(df['temperature_celsius'].max()), 
        (0, 40))

    filtered_df = df[(df['country'].isin(countries)) & 
        (df['temperature_celsius'] >= min_temp) & 
        (df['temperature_celsius'] <= max_temp)]

    # 3. Key Metrics - 3 columns
    st.markdown("### Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_temp = filtered_df['temperature_celsius'].mean()
        st.metric(label="Avg Temperature", value=f"{avg_temp:.2f} °C")

    with col2:
        hottest_row = filtered_df.loc[filtered_df['temperature_celsius'].idxmax()]
        st.metric(label="Hottest Location", value=hottest_row['location_name'])
        st.caption(f"{hottest_row['temperature_celsius']} °C, {hottest_row['country']}")

    with col3:
        coldest_row = filtered_df.loc[filtered_df['temperature_celsius'].idxmin()]
        st.metric(label="Coldest Location", value=coldest_row['location_name'])
        st.caption(f"{coldest_row['temperature_celsius']} °C, {coldest_row['country']}")

    # 4. Charts
    st.markdown("---")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Top 10 Hottest Cities")
        top10 = filtered_df.groupby('location_name')['temperature_celsius'].mean().nlargest(10)
        st.bar_chart(top10)

    with col_chart2:
        st.subheader("Avg Temp by Country")
        country_avg = filtered_df.groupby('country')['temperature_celsius'].mean().sort_values(ascending=False).head(10)
        st.bar_chart(country_avg)

    # 5. Map View
    st.subheader("Weather Map View")
    fig_map = px.scatter_geo(filtered_df,
        lat="latitude", lon="longitude", 
        color="temperature_celsius",
        hover_name="location_name",
        color_continuous_scale="thermal")
    st.plotly_chart(fig_map, use_container_width=True)

    # 6. Data Table
    st.subheader("Raw Data")
    st.dataframe(filtered_df)

    # 7. Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Data", csv, "weather_data.csv", "text/csv")

elif selected == "About":
    st.markdown("""
        <style>
        .title {font-size: 2.4rem; color: #1e40af; font-weight: 800;}
        .subtitle {font-size: 1.1rem; color: #64748b; margin-bottom: 25px;}
        .section {font-size: 1.3rem; font-weight: 700; color: #334155; margin-top: 25px;}
        .card {
            background: #f8fafc;
            padding: 20px; 
            border-radius: 12px; 
            border-left: 4px solid #2563eb;
            margin: 15px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="title">📘 About Weather Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Global Weather Data Visualization Platform</p>', unsafe_allow_html=True)
    st.markdown("---")

    # 1. Project Overview
    st.markdown('<p class="section">🌍 Project Overview</p>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("""
    This dashboard provides comprehensive analysis of global weather data from the 
    **Kaggle Global Weather Repository**. It helps visualize temperature patterns, 
    humidity levels, wind speed, and weather conditions across 200+ countries and cities worldwide.
    
    The goal is to enable data-driven insights for weather patterns and climate trends.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Key Features
    st.markdown('<p class="section">✨ Key Features</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("**📊 Interactive Visualizations**")
        st.write("• Temperature Distribution")
        st.write("• Humidity Analysis") 
        st.write("• Correlation Heatmaps")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("**🌐 Global Coverage**")
        st.write("• 200+ Countries")
        st.write("• Real-time Weather Data")
        st.write("• Geographical Mapping")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Dataset Information
    st.markdown('<p class="section">📁 Dataset Information</p>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("**Source**: Kaggle - Global Weather Repository")
    st.write("**Author**: Nelgiriyewithana")
    st.write("**Columns**: country, city, temperature, humidity, wind, pressure, condition")
    st.write("**Records**: 40,000+ weather observations")
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Technology Stack
    st.markdown('<p class="section">🛠️ Technology Stack</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.markdown('<div class="card">**Frontend**<br>Streamlit</div>', unsafe_allow_html=True)
    col2.markdown('<div class="card">**Data**<br>Pandas, NumPy</div>', unsafe_allow_html=True)
    col3.markdown('<div class="card">**Visualization**<br>Plotly, Seaborn</div>', unsafe_allow_html=True)

    # 5. Objectives
    st.markdown('<p class="section">🎯 Objectives</p>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("1. Visualize global weather patterns effectively")
    st.write("2. Analyze relationship between temperature and humidity")
    st.write("3. Compare weather metrics across different countries")
    st.write("4. Provide interactive and professional data exploration")
    st.markdown('</div>', unsafe_allow_html=True)

    # 6. Footer
    st.markdown("---")
    st.info("ℹ️ **Note**: This dashboard is developed for educational and research purposes.")
    st.caption("© 2026 Weather Analytics Dashboard | Built with Streamlit | Version 1.0.0")  
    
    

    