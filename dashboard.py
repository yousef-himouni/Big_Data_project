import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def set_background():
    # CSS to set the background image with overlay and black text
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)),
                        url("https://images3.alphacoders.com/280/280639.jpg");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Make all text black */
        .stMarkdown, .stTitle, .stHeader {{
            color: black !important;
        }}

        /* Style for headers */
        h1, h2, h3 {{
            color: black !important;
            text-shadow: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def create_visualizations(result, name):
    plt.style.use('ggplot')
    fig = None

    if name == 'the_growth_rate_of_cyclists':
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(result['st_year'], result['growth_percentage'],
                marker='o', linewidth=2, markersize=8, color='blue', label='Cumulative Growth Rate')

        # Value labels above each point
        for x, y in zip(result['st_year'], result['growth_percentage']):
            ax.text(x, y + 2, f'{y}%', ha='center', va='bottom', fontsize=10)

        ax.set_title('Cumulative Growth Rate of Cyclists', fontsize=14, fontweight='bold')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Cumulative Growth Percentage (%)', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()

    elif name == 'Popular_Stations':
        fig, ax = plt.subplots(figsize=(15, 8))
        ax.barh(result['start_station_name'], result['total_rides'], color='steelblue')
        ax.set_title('Top Popular Stations', fontsize=14, fontweight='bold')
        ax.set_xlabel('Total Rides', fontsize=12)
        ax.set_ylabel('Station Name', fontsize=12)
        ax.grid(axis='x', linestyle='--', alpha=0.7)

    elif name == 'Travel_duration_according_gender':
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(result['total_trips'],
               labels=result['gender'],
               autopct='%1.1f%%',
               startangle=90,
               colors=['lightcoral', 'lightskyblue'],
               wedgeprops={'edgecolor': 'black'})
        ax.set_title('Trip Distribution by Gender', fontsize=14, fontweight='bold')

    elif name == 'What_are_the_Age_target_of_the_company':
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(result['age_group'], result['total_rides'], color='royalblue')
        ax.set_title('Rides Distribution by Age Group', fontsize=14, fontweight='bold')
        ax.set_xlabel('Age Group', fontsize=12)
        ax.set_ylabel('Total Rides', fontsize=12)
        ax.set_xticks(range(len(result['age_group'])))
        ax.set_xticklabels(result['age_group'], rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    elif name == 'the_Month_and_the_day_of_trips':
        result['time_period'] = result['time_period'].astype(str)

        day_data = result[result['period_type'] == 'Day'].copy()
        month_data = result[result['period_type'] == 'Month'].copy()
        year_data = result[result['period_type'] == 'Year'].copy()

        if not day_data.empty:
            day_data['time_period'] = day_data['time_period'].astype(int)
            day_data.sort_values('time_period', inplace=True)

        month_order = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        if not month_data.empty:
            month_data['time_period'] = pd.Categorical(
                month_data['time_period'], categories=month_order, ordered=True
            )
            month_data.sort_values('time_period', inplace=True)

        if not year_data.empty:
            year_data.sort_values('time_period', inplace=True)

        busiest_day = day_data.loc[day_data['total_trips'].idxmax()] if not day_data.empty else None
        busiest_month = month_data.loc[month_data['total_trips'].idxmax()] if not month_data.empty else None
        busiest_year = year_data.loc[year_data['total_trips'].idxmax()] if not year_data.empty else None

        fig, axes = plt.subplots(3, 1, figsize=(15, 18))

        if not day_data.empty:
            axes[0].bar(day_data['time_period'], day_data['total_trips'],
                        color='lightblue', label='Trips')
            if busiest_day is not None:
                axes[0].bar(busiest_day['time_period'], busiest_day['total_trips'],
                            color='red', label=f"Busiest Day: {busiest_day['time_period']}")
            axes[0].set_title('Trips Per Day', fontsize=14, fontweight='bold')
            axes[0].set_xlabel('Day', fontsize=12)
            axes[0].set_ylabel('Total Trips', fontsize=12)
            axes[0].legend()
            axes[0].grid(axis='y', linestyle='--', alpha=0.7)
            axes[0].tick_params(axis='x', rotation=45)

        if not month_data.empty:
            axes[1].bar(month_data['time_period'], month_data['total_trips'],
                        color='orange', label='Trips')
            if busiest_month is not None:
                axes[1].bar(busiest_month['time_period'], busiest_month['total_trips'],
                            color='red', label=f"Busiest Month: {busiest_month['time_period']}")
            axes[1].set_title('Trips Per Month', fontsize=14, fontweight='bold')
            axes[1].set_xlabel('Month', fontsize=12)
            axes[1].set_ylabel('Total Trips', fontsize=12)
            axes[1].legend()
            axes[1].grid(axis='y', linestyle='--', alpha=0.7)
            axes[1].tick_params(axis='x', rotation=45)

        if not year_data.empty:
            axes[2].bar(year_data['time_period'], year_data['total_trips'],
                        color='green', label='Trips')
            if busiest_year is not None:
                axes[2].bar(busiest_year['time_period'], busiest_year['total_trips'],
                            color='red', label=f"Busiest Year: {busiest_year['time_period']}")
            axes[2].set_title('Trips Per Year', fontsize=14, fontweight='bold')
            axes[2].set_xlabel('Year', fontsize=12)
            axes[2].set_ylabel('Total Trips', fontsize=12)
            axes[2].legend()
            axes[2].grid(axis='y', linestyle='--', alpha=0.7)

    return fig


def show_questions():
    st.title("Questions")
    st.write("""
    Our analysis focuses on five key questions about the bike-sharing system:

    1. **Growth Rate Analysis**
    - How has the number of cyclists grown over time?
    - What are the year-over-year growth trends?

    2. **Gender Distribution**
    - How does trip duration vary by gender?
    - What is the gender distribution among riders?

    3. **Popular Stations**
    - Which stations see the most traffic?
    - What are the top 10 most frequently used stations?

    4. **Age Demographics**
    - What age groups use the bike-sharing service most?
    - How does ridership vary across different age brackets?

    5. **Temporal Patterns**
    - What are the busiest months, days, and years?
    - How does ridership vary across different time periods?
    """)


def show_story():
    st.title("Our Story")
    st.write("""
    Welcome to CycleCraft - Your Ultimate Bike Manufacturing Company!

    Our journey began with a passionate vision: to craft exceptional bicycles that transform the way people experience cycling. 
    
    At CycleCraft, we blend innovative engineering with timeless design to create bikes that inspire riders of all levels.

    Through our dedicated craftsmanship, we focus on:
    - Advanced frame technologies
    - Premium materials selection
    - Custom-fit solutions
    - Sustainable manufacturing practices

    This platform showcases our commitment to quality manufacturing, serving
     
    professional cyclists, urban commuters, and cycling enthusiasts with bikes
     
    that are built to perform and built to last.
    """)

def show_growth_rate_analysis(conn):
    st.markdown("## The Growth Rate of Cyclists - Interactive")
    df_growth = pd.read_sql_query("SELECT * FROM the_growth_rate_of_cyclists_results", conn)
    if not df_growth.empty:
        all_years = sorted(df_growth['st_year'].unique())
        if len(all_years) > 1:
            min_year, max_year = int(min(all_years)), int(max(all_years))
            st.markdown("### Select Year Range:")
            year_range = st.slider("", min_value=min_year, max_value=max_year, value=(min_year, max_year))
            df_growth_filtered = df_growth[
                (df_growth['st_year'] >= year_range[0]) &
                (df_growth['st_year'] <= year_range[1])
                ]
        else:
            df_growth_filtered = df_growth

        df_growth_filtered['st_year'] = df_growth_filtered['st_year'].astype(str)
        st.dataframe(df_growth_filtered.head(10))
        fig1 = create_visualizations(df_growth_filtered, 'the_growth_rate_of_cyclists')
        if fig1:
            st.pyplot(fig1)


def show_gender_analysis(conn):
    st.subheader("Travel Duration According to Gender")
    df_gender = pd.read_sql_query("SELECT * FROM Travel_duration_according_gender_results", conn)
    st.dataframe(df_gender.head(10))
    fig2 = create_visualizations(df_gender, 'Travel_duration_according_gender')
    if fig2:
        st.pyplot(fig2)


def show_popular_stations(conn):
    st.subheader("Popular Stations")
    df_stations = pd.read_sql_query("SELECT * FROM Popular_Stations_results", conn)
    df_stations_top10 = df_stations.sort_values('total_rides', ascending=False).head(10)
    st.dataframe(df_stations_top10)
    fig3 = create_visualizations(df_stations_top10, 'Popular_Stations')
    if fig3:
        st.pyplot(fig3)


def show_age_analysis(conn):
    st.subheader("Age Target of the Company - Interactive")
    df_age = pd.read_sql_query("SELECT * FROM What_are_the_Age_target_of_the_company_results", conn)

    if not df_age.empty:
        # Define the correct order of age groups
        age_order = ['Under 25', '25-35', '36-50', 'Over 50']

        # Convert age_group to categorical with custom order
        df_age['age_group'] = pd.Categorical(df_age['age_group'],
                                             categories=age_order,
                                             ordered=True)

        # Sort the dataframe by the ordered age_group
        df_age = df_age.sort_values('age_group')

        # Get unique age groups in the correct order
        all_groups = df_age['age_group'].unique().tolist()

        # Create multiselect with ordered options
        chosen_groups = st.multiselect("Select which age groups:",
                                       options=all_groups,
                                       default=all_groups)
        # Filter and maintain the order
        df_age_filtered = df_age[df_age['age_group'].isin(chosen_groups)]

        st.dataframe(df_age_filtered)
        fig4 = create_visualizations(df_age_filtered, 'What_are_the_Age_target_of_the_company')
        if fig4:
            st.pyplot(fig4)


def show_temporal_analysis(conn):
    st.subheader("The Month and the Day of Trips")
    df_periods = pd.read_sql_query("SELECT * FROM the_Month_and_the_day_of_trips_results", conn)
    st.dataframe(df_periods.head(20))
    fig5 = create_visualizations(df_periods, 'the_Month_and_the_day_of_trips')
    if fig5:
        st.pyplot(fig5)


def show_analytics():
    st.title("Analytics")
    conn = sqlite3.connect("sqlite_file.sqlite")

    show_growth_rate_analysis(conn)
    show_gender_analysis(conn)
    show_popular_stations(conn)
    show_age_analysis(conn)
    show_temporal_analysis(conn)

    conn.close()


# Add this new function to display small_data
def show_small_data():
    st.title("Small Data Overview")
    try:
        # Connect to SQLite database
        conn = sqlite3.connect("sqlite_file.sqlite")

        # Read the small_data table
        df = pd.read_sql_query("SELECT * FROM small_data", conn)

        st.write(f"Total Records: {len(df):,}")
        st.dataframe(df)
        conn.close()

    except Exception as e:
        st.error(f"Error loading data: {e}")


def show_about_us():
    st.title("About Us")

    # CEO Section
    st.header("Our Leadership")
    st.subheader("CEOs - Yousef Himouni & Razi Shibli")
    st.write("""
        Yosef Hymone and Razi Shibli are the visionary co-founders and CEOs of our data analytics company. 
        Their complementary skills and shared passion for data-driven insights have been instrumental in 
        shaping our company's direction.

        Together, they lead our team in:
        - Developing innovative data analysis solutions
        - Creating intuitive data visualization tools
        - Building robust analytical frameworks
        - Delivering actionable insights to clients

        Education and Background:
        
        Yosef Hymone:
        - BSc in Computer Science
        - Specialization in Data Analytics and Machine Learning

        Razi Shibli:
        - BSc in Computer Science
        - Expertise in Data Visualization and Analytics
    """)

    # Contact Information
    st.header("Contact Us")
    st.write("""
        📍 Headquarters: Jerusalem, IL
        
        📧 Email: CycleCraft@company.com
        
        📞 Phone: +972 50000001
    """)


# Modify the main function to include the new option
def main():
    set_background()

    st.sidebar.title("Navigation")
    # Add "Small Data" to the radio options
    page = st.sidebar.radio("Go to", ["Story", "Questions", "Analytics", "Small Data", "About Us"])

    if page == "Story":
        show_story()
    elif page == "Questions":
        show_questions()
    elif page == "Analytics":
        show_analytics()
    elif page == "Small Data":
        show_small_data()
    elif page == "About Us":
        show_about_us()


if __name__ == '__main__':
    main()
