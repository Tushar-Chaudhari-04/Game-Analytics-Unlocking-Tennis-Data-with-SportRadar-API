import mysql.connector
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Tennis Game Analytics", layout="wide")

@st.cache_resource
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["database"]["host"],
            user=st.secrets["database"]["user"],
            password=st.secrets["database"]["password"],
            database=st.secrets["database"]["database"]
        )
        return conn
    except Exception as e:
        st.error("❌ Error:", e)
        return None,str(e)

# @st.cache_data
def execute_query(query,connection):
   try:
    df=pd.read_sql(query,connection)
    return df
   except Exception as e:
      st.error(f"Error Executing Query: {e}")
      return None,str(e) 


def get_master_data(conn):
    comp_df = get_competitions_data(conn)
    venue_df = get_complex_data(conn)
    rank_df = get_ranking_data(conn)

    # Add source columns
    comp_df['data_type'] = 'competition'
    venue_df['data_type'] = 'venue'
    rank_df['data_type'] = 'ranking'
    return comp_df, venue_df, rank_df


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
    LEFT JOIN categories c2
    ON c1.category_id = c2.category_id
    """
   df2=execute_query(query,conn)
   return df2


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
    LEFT JOIN complexes c
    on v.complex_id=c.complex_id
    """
   df2=execute_query(query,conn)
   return df2


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
    LEFT JOIN competitors c
    ON r.competitor_id = c.competitor_id
    """
    df3=execute_query(query,conn)
    return df3

def show_global_dashboard(comp_df, venue_df, rank_df):

    st.title("🌍 Global Tennis Analytics Dashboard")

    # =========================
    # GLOBAL FILTERS
    # =========================
    st.sidebar.header("🌐 Global Filters")

    # Country filter (common dimension)
    all_countries = sorted(
        set(venue_df['country_name'].dropna().unique()).union(
            set(rank_df['country'].dropna().unique())
        )
    )

    selected_country = st.sidebar.selectbox(
        "Select Country",
        ["All"] + all_countries
    )

    # Competition Type Filter
    comp_type = st.sidebar.selectbox(
        "Competition Type",
        ["All"] + sorted(comp_df['type'].dropna().unique().tolist())
    )

    # Rank Range
    rank_range = st.sidebar.slider(
        "Ranking Range",
        int(rank_df['ranking'].min()),
        int(rank_df['ranking'].max()),
        (1, 50)
    )

    # =========================
    # APPLY FILTERS
    # =========================
    filtered_comp = comp_df.copy()
    filtered_venue = venue_df.copy()
    filtered_rank = rank_df.copy()

    if selected_country != "All":
        filtered_venue = filtered_venue[
            filtered_venue['country_name'] == selected_country
        ]
        filtered_rank = filtered_rank[
            filtered_rank['country'] == selected_country
        ]

    if comp_type != "All":
        filtered_comp = filtered_comp[
            filtered_comp['type'] == comp_type
        ]

    filtered_rank = filtered_rank[
        (filtered_rank['ranking'] >= rank_range[0]) &
        (filtered_rank['ranking'] <= rank_range[1])
    ]

    # =========================
    # KPI SECTION
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Competitions", len(filtered_comp))
    col2.metric("Venues", len(filtered_venue))
    col3.metric("Players", len(filtered_rank))
    col4.metric(
        "Countries",
        len(set(filtered_venue['country_name']).union(set(filtered_rank['country'])))
    )

    # =========================
    # COUNTRY ANALYSIS
    # =========================
    st.subheader("🌍 Country Comparison")

    venue_country = filtered_venue.groupby('country_name')['venue_id'].count()
    player_country = filtered_rank.groupby('country')['competitor_id'].count()

    combined = pd.concat([venue_country, player_country], axis=1)
    combined.columns = ['Venues', 'Players']
    combined = combined.fillna(0)

    st.dataframe(combined)
    st.bar_chart(combined)

    # =========================
    # TOP COUNTRIES
    # =========================
    st.subheader("🏆 Top Countries by Players")

    top_players = filtered_rank['country'].value_counts().head(10)
    st.bar_chart(top_players)

    # =========================
    # COMPETITION ANALYSIS
    # =========================
    st.subheader("🎾 Competition Type Distribution")

    comp_dist = filtered_comp['type'].value_counts()
    st.bar_chart(comp_dist)

    st.subheader("📊 Category Distribution")

    cat_dist = filtered_comp['category_name'].value_counts()
    st.bar_chart(cat_dist)

    # =========================
    # PLAYER ANALYSIS
    # =========================
    st.subheader("📈 Ranking vs Points")

    st.scatter_chart(filtered_rank[['ranking', 'points']])

    st.subheader("🔥 Top 10 Players by Points")

    top_points = filtered_rank.sort_values("points", ascending=False).head(10)
    st.dataframe(top_points[['name', 'country', 'points', 'ranking']])

    # =========================
    # MOVEMENT ANALYSIS
    # =========================
    st.subheader("📊 Ranking Movement Analysis")

    movement_dist = filtered_rank['movement'].value_counts()
    st.bar_chart(movement_dist)

    # =========================
    # VENUE ANALYSIS
    # =========================
    st.subheader("🏟️ Venues per Complex")

    complex_analysis = filtered_venue.groupby('complex_name')['venue_id'].count().sort_values(ascending=False).head(10)
    st.bar_chart(complex_analysis)

    # =========================
    # ADVANCED INSIGHT
    # =========================
    st.subheader("📌 Avg Points by Country")

    avg_points = filtered_rank.groupby('country')['points'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(avg_points)

    # =========================
    # RAW DATA VIEW (OPTIONAL)
    # =========================
    with st.expander("🔍 View Raw Data"):
        st.write("### Competitions")
        st.dataframe(filtered_comp)

        st.write("### Venues")
        st.dataframe(filtered_venue)

        st.write("### Rankings")
        st.dataframe(filtered_rank)


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


def show_complex_data(df):

    st.title("🏟️ Venue & Complex Analytics Dashboard")

    # ==============================
    # KPI SECTION
    # ==============================
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Venues", df.shape[0])
    col2.metric("Countries", df['country_name'].nunique())
    col3.metric("Complexes", df['complex_name'].nunique())

    # ==============================
    # SIDEBAR FILTERS
    # ==============================
    st.sidebar.header("🔍 Venue Filters")

    # Search (Venue + City)
    search = st.sidebar.text_input("Search Venue / City")

    # Country Filter
    country = st.sidebar.selectbox(
        "Select Country",
        ["All"] + sorted(df['country_name'].dropna().unique().tolist())
    )

    # City Filter
    city = st.sidebar.selectbox(
        "Select City",
        ["All"] + sorted(df['city_name'].dropna().unique().tolist())
    )

    # Complex Filter
    complex_name = st.sidebar.selectbox(
        "Select Complex",
        ["All"] + sorted(df['complex_name'].dropna().unique().tolist())
    )

    # Timezone Filter
    timezone = st.sidebar.selectbox(
        "Select Timezone",
        ["All"] + sorted(df['timezone'].dropna().unique().tolist())
    )

    # Top N selector for charts
    top_n = st.sidebar.slider("Top N (Charts)", 5, 20, 10)

    # ==============================
    # FILTER LOGIC
    # ==============================
    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered['venue_name'].str.contains(search, case=False, na=False) |
            filtered['city_name'].str.contains(search, case=False, na=False)
        ]

    if country != "All":
        filtered = filtered[filtered['country_name'] == country]

    if city != "All":
        filtered = filtered[filtered['city_name'] == city]

    if complex_name != "All":
        filtered = filtered[filtered['complex_name'] == complex_name]

    if timezone != "All":
        filtered = filtered[filtered['timezone'] == timezone]

    # ==============================
    # DATA TABLE
    # ==============================
    st.subheader("📋 Filtered Venues")

    if filtered.empty:
        st.warning("No matching records found")
    else:
        st.dataframe(filtered, use_container_width=True)

    # ==============================
    # VENUE DETAILS
    # ==============================
    st.subheader("📌 Venue Details")

    if not filtered.empty:
        venue = st.selectbox("Select Venue", filtered['venue_name'].unique())

        details = filtered[filtered['venue_name'] == venue].iloc[0]

        col1, col2 = st.columns(2)

        col1.write(f"**City:** {details['city_name']}")
        col1.write(f"**Country:** {details['country_name']}")
        col1.write(f"**Timezone:** {details['timezone']}")

        col2.write(f"**Complex:** {details['complex_name']}")
        col2.write(f"**Venue ID:** {details['venue_id']}")
        col2.write(f"**Country Code:** {details['country_code']}")

    # ==============================
    # COUNTRY ANALYSIS
    # ==============================
    st.subheader("🌍 Top Countries by Venues")

    country_df = (
        filtered.groupby('country_name')['venue_id']
        .count()
        .sort_values(ascending=False)
        .head(top_n)
    )

    st.bar_chart(country_df)

    # ==============================
    # CITY ANALYSIS
    # ==============================
    st.subheader("🏙️ Top Cities")

    city_df = (
        filtered.groupby('city_name')['venue_id']
        .count()
        .sort_values(ascending=False)
        .head(top_n)
    )

    st.bar_chart(city_df)

    # ==============================
    # COMPLEX ANALYSIS
    # ==============================
    st.subheader("🏟️ Top Complexes")

    complex_df = (
        filtered.groupby('complex_name')['venue_id']
        .count()
        .sort_values(ascending=False)
        .head(top_n)
    )

    st.bar_chart(complex_df)

    # ==============================
    # TIMEZONE ANALYSIS
    # ==============================
    st.subheader("⏰ Timezone Distribution")

    timezone_df = filtered['timezone'].value_counts().head(top_n)
    st.bar_chart(timezone_df)

    # ==============================
    # ADVANCED INSIGHT
    # ==============================
    st.subheader("📊 Venues per Country vs City")

    pivot_df = filtered.pivot_table(
        index='country_name',
        columns='city_name',
        values='venue_id',
        aggfunc='count',
        fill_value=0
    )

    st.dataframe(pivot_df)

    # ==============================
    # RAW DATA
    # ==============================
    with st.expander("🔍 View Full Dataset"):
        st.dataframe(df)

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
        ["Global Dashboard","Competitions", "Venues", "Rankings"]
    )
   
   
    # ==============================
    # PAGE ROUTING
    # ==============================
   if page == "Global Dashboard":
    comp_df, venue_df, rank_df = get_master_data(conn)
    show_global_dashboard(comp_df, venue_df, rank_df)

   elif page == "Competitions":
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
