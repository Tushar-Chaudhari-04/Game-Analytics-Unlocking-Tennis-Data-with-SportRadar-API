import mysql.connector
import pandas as pd
import streamlit as st
import inspect

st.set_page_config(page_title="Tennis Game Analytics", layout="wide")


@st.cache_resource
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Root@1234",
            database="sports_db"
        )
        return conn
    except Exception as e:
        st.error("❌ Error:", e)
        return None,str(e)

def execute_query(query,connection):
   try:
    df=pd.read_sql(query,connection)
    return df
   except Exception as e:
      st.error(f"Error Executing Query: {e}")
      return None,str(e) 

def get_competitions_data(conn):
   query = """
    SELECT 
        c1.competition_id,
        c1.competition_name,
        c1.parent_id,
        c1.type,
        c1.gender,
        c1.category_id,
        c2.category_name
    FROM competitions c1
    INNER JOIN categories c2
    ON c1.category_id = c2.category_id
    """
   df2=execute_query(query,conn)
   return df2

def show_competitions_data(df):
# ==============================
# KPI SECTION
# ==============================
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Competitions", len(df))
    col2.metric("Categories", df['category_name'].nunique())
    col3.metric("Types", df['type'].nunique())

    search = st.sidebar.text_input("Search Competition", key="comp_search")

    category = st.sidebar.selectbox(
        "Select Category",
        ["All"] + sorted(df['category_name'].unique().tolist()),
        key="comp_category"
    )

    gender = st.sidebar.selectbox(
        "Select Gender",
        ["All"] + sorted(df['gender'].unique().tolist()),
        key="comp_gender"
    )

    comp_type = st.sidebar.selectbox(
        "Select Type",
        ["All"] + sorted(df['type'].unique().tolist()),
        key="comp_type"
    )
    # ==============================
    # FILTERS
    # ==============================
    st.sidebar.header("🔍 Filters")

    search = st.sidebar.text_input("Search Competition")

    category = st.sidebar.selectbox(
        "Select Category",
        ["All"] + sorted(df['category_name'].unique().tolist())
    )

    gender = st.sidebar.selectbox(
        "Select Gender",
        ["All"] + sorted(df['gender'].unique().tolist())
    )

    comp_type = st.sidebar.selectbox(
        "Select Type",
        ["All"] + sorted(df['type'].unique().tolist())
    )

    # ==============================
    # FILTER LOGIC
    # ==============================
    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered['competition_name'].str.contains(search, case=False, na=False)
        ]

    if category != "All":
        filtered = filtered[filtered['category_name'] == category]

    if gender != "All":
        filtered = filtered[filtered['gender'] == gender]

    if comp_type != "All":
        filtered = filtered[filtered['type'] == comp_type]

    # ==============================
    # DATA TABLE
    # ==============================
    st.subheader("📋 Competition Data")

    if filtered.empty:
        st.warning("No data found")
    else:
        st.dataframe(filtered, use_container_width=True)

    # ==============================
    # ANALYSIS
    # ==============================
    st.subheader("📊 Category-wise Competition Count")

    category_analysis = filtered.groupby("category_name")["competition_id"].count()

    st.bar_chart(category_analysis)

    # ==============================
    # TYPE ANALYSIS
    # ==============================
    st.subheader("🎾 Type Distribution")

    type_analysis = filtered["type"].value_counts()

    st.bar_chart(type_analysis)

    # ==============================
    # GENDER ANALYSIS
    # ==============================
    st.subheader("👥 Gender Distribution")

    gender_analysis = filtered["gender"].value_counts()

    st.bar_chart(gender_analysis)


def get_complex_data(conn):
   query = """
    SELECT
    v.venue_id,
    v.venue_name,
    v.city_name,
    v.country_name,
    v.country_code,
    v.timezone,
    v.complex_id,
    c.complex_name
    FROM venues AS v
    INNER JOIN complexes c
    on v.complex_id=c.complex_id
    """
   df2=execute_query(query,conn)
   return df2

def show_complex_data(df):

    # ==============================
    # KPIs
    # ==============================
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Venues", df.shape[0])
    col2.metric("Countries", df['country_name'].nunique())
    col3.metric("Complexes", df['complex_name'].nunique())

    # ==============================
    # FILTERS
    # ==============================
    st.subheader("🔍 Search & Filters")

    search = st.text_input("Search Venue")

    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered['venue_name'].str.contains(search, case=False, na=False)
        ]

    country = st.selectbox("Select Country", df['country_name'].dropna().unique())

    filtered = filtered[filtered['country_name'] == country]

    # ==============================
    # DISPLAY TABLE
    # ==============================
    st.subheader("📋 Filtered Results")

    if filtered.empty:
        st.warning("No matching records")
    else:
        st.dataframe(filtered, use_container_width=True)

    # ==============================
    # DETAILS VIEW
    # ==============================
    st.subheader("📌 Venue Details")

    if not filtered.empty:
        venue = st.selectbox("Select Venue", filtered['venue_name'].unique())

        details = df[df['venue_name'] == venue]

        if not details.empty:
            d = details.iloc[0]

            col1, col2 = st.columns(2)

            col1.write(f"**City:** {d['city_name']}")
            col1.write(f"**Country:** {d['country_name']}")
            col1.write(f"**Timezone:** {d['timezone']}")

            col2.write(f"**Complex:** {d['complex_name']}")
            col2.write(f"**Venue ID:** {d['venue_id']}")
            col2.write(f"**Country Code:** {d['country_code']}")

    # ==============================
    # COUNTRY ANALYSIS
    # ==============================
    st.subheader("🌍 Country-wise Analysis")

    country_df = df.groupby('country_name')['venue_id'].count().reset_index()
    country_df.columns = ['Country', 'Total Venues']

    st.dataframe(country_df)
    st.bar_chart(country_df.set_index('Country'))

    # ==============================
    # LEADERBOARDS
    # ==============================
    st.subheader("🏆 Leaderboards")

    # Top Countries
    top_countries = country_df.sort_values(by='Total Venues', ascending=False).head(10)

    st.write("### 🌍 Top Countries by Venues")
    st.dataframe(top_countries)

    # Top Complexes
    complex_df = df.groupby('complex_name')['venue_id'].count().reset_index()
    complex_df.columns = ['Complex', 'Total Venues']

    top_complex = complex_df.sort_values(by='Total Venues', ascending=False).head(10)

    st.write("### 🏟️ Top Complexes")
    st.dataframe(top_complex)

def get_ranking_data(conn):
    query= """
    SELECT 
        c.competitor_id,
        c.name,
        c.country,
        c.country_code,
        c.abbreviation,
        r.rank_id,
        r.ranking,
        r.movement,
        r.points,
        r.competitions_played
    FROM competitor_rankings r
    INNER JOIN competitors c
    ON r.competitor_id = c.competitor_id
    """
    df3=execute_query(query,conn)
    return df3

def show_ranking_data(df):
# ==============================
# APP
# ==============================
    st.title("🏆 Competitor Leaderboard Dashboard")

    # ==============================
    # KPI SECTION
    # ==============================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Players", len(df))
    col2.metric("Countries", df['country'].nunique())
    col3.metric("Max Points", int(df['points'].max()))
    col4.metric("Top Rank", int(df['ranking'].min()))

    # ==============================
    # FILTERS
    # ==============================
    st.sidebar.header("🔍 Filters")

    search = st.sidebar.text_input("Search Player", key="rank_search")

    country = st.sidebar.selectbox(
        "Select Country",
        ["All"] + sorted(df['country'].unique().tolist()),
        key="rank_country"
    )

    rank_range = st.sidebar.slider(
        "Select Rank Range",
        int(df['ranking'].min()),
        int(df['ranking'].max()),
        (1, 50),
        key="rank_slider"
    )



    # search = st.sidebar.text_input("Search Player")

    # country = st.sidebar.selectbox(
    #     "Select Country",
    #     ["All"] + sorted(df['country'].unique().tolist())
    # )

    # rank_range = st.sidebar.slider(
    #     "Select Rank Range",
    #     int(df['ranking'].min()),
    #     int(df['ranking'].max()),
    #     (1, 50)
    # )

    # ==============================
    # FILTER LOGIC
    # ==============================
    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered['name'].str.contains(search, case=False, na=False)
        ]

    if country != "All":
        filtered = filtered[filtered['country'] == country]

    filtered = filtered[
        (filtered['ranking'] >= rank_range[0]) &
        (filtered['ranking'] <= rank_range[1])
    ]

    # ==============================
    # TABLE
    # ==============================
    st.subheader("📋 Leaderboard Data")

    if filtered.empty:
        st.warning("No data found")
    else:
        st.dataframe(filtered.sort_values("ranking"), use_container_width=True)

    # ==============================
    # TOP LEADERBOARDS
    # ==============================
    st.subheader("🏆 Top 10 Players")

    top_ranked = df.sort_values("ranking").head(10)
    st.dataframe(top_ranked)

    st.subheader("🔥 Highest Points")

    top_points = df.sort_values("points", ascending=False).head(10)
    st.dataframe(top_points)

    st.subheader("📈 Most Improved Players")

    top_movement = df.sort_values("movement", ascending=False).head(10)
    st.dataframe(top_movement)

    # ==============================
    # COUNTRY ANALYSIS
    # ==============================
    st.subheader("🌍 Country Analysis")

    country_analysis = df.groupby("country").agg({
        "name": "count",
        "points": "mean"
    }).rename(columns={
        "name": "Total Players",
        "points": "Avg Points"
    }).reset_index()

    st.dataframe(country_analysis)

    st.bar_chart(country_analysis.set_index("country"))

    # ==============================
    # POINTS VS RANK
    # ==============================
    st.subheader("📊 Points vs Ranking")

    st.scatter_chart(df[["ranking", "points"]])

def main():
   st.title("Tennis Ranking Explorer Dashboard")
   st.markdown("---")
   
    # ==============================
    # DB CONNECTION
    # ==============================
   conn = get_connection()

   if conn is None:
        st.warning("⚠️ Please configure database credentials.")
        st.error("❌ Database connection failed")
        st.stop()

   
    # ==============================
    # NAVIGATION
    # ==============================
   page = st.sidebar.selectbox(
        "📊 Select Dashboard",
        ["Competitions", "Venues", "Rankings"]
    )

    # ==============================
    # PAGE ROUTING
    # ==============================
   
   if page == "Competitions":
        df = get_competitions_data(conn)
        show_competitions_data(df)

   elif page == "Venues":
        df = get_complex_data(conn)
        show_complex_data(df)

   elif page == "Rankings":
        df = get_ranking_data(conn)
        show_ranking_data(df) 




if __name__=="__main__":
   main()
