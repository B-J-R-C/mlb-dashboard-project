import streamlit as st
import pandas as pd
import sqlite3

# 1. page layout and titles
st.set_page_config(page_title="MLB History Dashboard", layout="wide")

st.title("⚾ Major League Baseball History Dashboard")
st.markdown("Welcome to the interactive MLB dashboard! Use the sidebar on the left to filter the historical data.")

# 2. Load Data 
@st.cache_data
def load_data():
    conn = sqlite3.connect("database/baseball_history.db")
    
    # Use JOIN query from earlier
    query = """
    SELECT e.Year, e.Detail AS Batting_Average_Leader, p.Player AS Home_Run_Leader
    FROM events e
    JOIN player_stats p ON e.Year = p.Year
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Adding simulated numerical data
    df['Games_Played'] = [162, 162, 60, 162, 162] # 2020 was shorter cos covid
    df['Top_Home_Runs'] = [48, 53, 22, 48, 62] 
    df['League_Batting_Avg'] = [0.248, 0.252, 0.245, 0.244, 0.243]
    
    return df

df = load_data()

# 3. Interactive 
st.sidebar.header("Filter Options")

# Slider
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
selected_years = st.sidebar.slider("Select Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# Dropdown
players = ["All Players"] + df['Home_Run_Leader'].unique().tolist()
selected_player = st.sidebar.selectbox("Filter by Home Run Leader", players)

# 4. Dynamic filter DataFrame
filtered_df = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])]

if selected_player != "All Players":
    filtered_df = filtered_df[filtered_df['Home_Run_Leader'] == selected_player]

# Display Data Table
st.subheader("Raw Data View")
st.dataframe(filtered_df, use_container_width=True)

# 5. Three Viz
st.markdown("---")
st.subheader("Historical Trends")

# Split the screen
col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Games Played per Season**")
    # set the index to 'Year'
    st.bar_chart(filtered_df.set_index('Year')['Games_Played'])

with col2:
    st.write("**Top Home Run Totals**")
    st.line_chart(filtered_df.set_index('Year')['Top_Home_Runs'])

with col3:
    st.write("**League Average Batting Avg**")
    st.area_chart(filtered_df.set_index('Year')['League_Batting_Avg'])