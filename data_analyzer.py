import sqlite3
import duckdb

queries = {
    'The_growth_rate_of_cyclists': """
        WITH yearly_totals AS (
            SELECT 
                st_year,
                COUNT(*) AS total_rides
            FROM divvy_data
            GROUP BY st_year
            ORDER BY st_year
        ),
        growth_calc AS (
            SELECT 
                st_year,
                total_rides,
                FIRST_VALUE(total_rides) OVER (ORDER BY st_year) AS initial_year_rides,
                ROUND(
                    ((total_rides - FIRST_VALUE(total_rides) OVER (ORDER BY st_year)) * 100.0 / 
                    FIRST_VALUE(total_rides) OVER (ORDER BY st_year)), 2
                ) AS growth_percentage
            FROM yearly_totals
        )
        SELECT * FROM growth_calc
        ORDER BY st_year;
    """,

    'Popular_Stations': """
       WITH popular_stations AS (
           SELECT start_station_name, 
               COUNT(*) as total_rides,
               AVG(trip_duration) as avg_ride_minutes
           FROM divvy_data
           GROUP BY start_station_name
           HAVING COUNT(*) > (
               SELECT AVG(ride_count)
               FROM (SELECT COUNT(*) as ride_count 
                     FROM divvy_data 
                     GROUP BY start_station_name)
           )
       )
       SELECT * FROM popular_stations
   """,

    'Travel_duration_according_gender': """
        SELECT 
           CASE 
               WHEN gender = 0 THEN 'Male'
               WHEN gender = 1 THEN 'Female'
           END as gender,
           COUNT(*) as total_trips,
           AVG(trip_duration/60) as avg_duration_minutes,
           COUNT(CASE WHEN trip_duration > 1800 THEN 1 END) as long_trips,
           ROUND(COUNT(CASE WHEN trip_duration > 1800 THEN 1 END) * 100.0 / COUNT(*), 2) as long_trip_percentage
        FROM divvy_data
        WHERE trip_duration < 7200 
        AND gender IN (0, 1)  -- הסרת -1
        GROUP BY gender
        ORDER BY gender;
   """,

    'What_are_the_Age_target_of_the_company': """
        SELECT 
            CASE 
                WHEN age < 25 THEN 'Under 25'
                WHEN age BETWEEN 25 AND 35 THEN '25-35'
                WHEN age BETWEEN 36 AND 50 THEN '36-50'
                ELSE 'Over 50'
            END as age_group,
            COUNT(*) as total_rides
        FROM divvy_data
        GROUP BY age_group;
   """,

    'The_Month_and_the_day_of_trips': """
        WITH daily_stats AS (
        SELECT 
            st_day,
            COUNT(*) AS daily_trips,
            AVG(trip_duration/60) AS daily_avg_duration
        FROM divvy_data
        GROUP BY st_day
    ),
    top_five_days AS (
        SELECT st_day, daily_trips, daily_avg_duration
        FROM daily_stats
        ORDER BY daily_trips DESC
        LIMIT 5
    ),

    monthly_stats AS (
        SELECT 
            st_month,
            CASE 
                WHEN st_month = 1 THEN 'January'
                WHEN st_month = 2 THEN 'February'
                WHEN st_month = 3 THEN 'March'
                WHEN st_month = 4 THEN 'April'
                WHEN st_month = 5 THEN 'May'
                WHEN st_month = 6 THEN 'June'
                WHEN st_month = 7 THEN 'July'
                WHEN st_month = 8 THEN 'August'
                WHEN st_month = 9 THEN 'September'
                WHEN st_month = 10 THEN 'October'
                WHEN st_month = 11 THEN 'November'
                WHEN st_month = 12 THEN 'December'
            END AS month_name,
            COUNT(*) AS monthly_trips,
            AVG(trip_duration/60) AS monthly_avg_duration
        FROM divvy_data
        GROUP BY st_month
    ),
    top_five_months AS (
        SELECT st_month, month_name, monthly_trips, monthly_avg_duration
        FROM monthly_stats
        ORDER BY monthly_trips DESC
        LIMIT 5
    ),
    
    yearly_stats AS (
        SELECT 
            st_year,
            COUNT(*) AS yearly_trips,
            AVG(trip_duration/60) AS yearly_avg_duration
        FROM divvy_data
        GROUP BY st_year
    ),
    top_five_years AS (
        SELECT st_year, yearly_trips, yearly_avg_duration
        FROM yearly_stats
        ORDER BY yearly_trips DESC
        LIMIT 5
    ),
    
    combined_top_five AS (
        SELECT 
            'Day' AS period_type,
            st_day::VARCHAR AS time_period,
            daily_trips AS total_trips,
            ROUND(daily_avg_duration, 2) AS avg_duration_minutes
        FROM top_five_days
    
        UNION ALL
    
        SELECT 
            'Month' AS period_type,
            month_name AS time_period,
            monthly_trips AS total_trips,
            ROUND(monthly_avg_duration, 2) AS avg_duration_minutes
        FROM top_five_months
    
        UNION ALL
    
        SELECT 
            'Year' AS period_type,
            st_year::VARCHAR AS time_period,
            yearly_trips AS total_trips,
            ROUND(yearly_avg_duration, 2) AS avg_duration_minutes
        FROM top_five_years
    )
    
    SELECT * FROM combined_top_five
    UNION ALL
    SELECT 'Day', st_day::VARCHAR, daily_trips, ROUND(daily_avg_duration, 2) FROM daily_stats
    UNION ALL
    SELECT 'Month', month_name, monthly_trips, ROUND(monthly_avg_duration, 2) FROM monthly_stats
    UNION ALL
    SELECT 'Year', st_year::VARCHAR, yearly_trips, ROUND(yearly_avg_duration, 2) FROM yearly_stats
    ORDER BY period_type, total_trips DESC;
    """
}

def load_csv_to_sqlite(csv_file, sqlite_db, table_name):
    """
    Load a CSV file into SQLite database
    Returns:
    bool: True if successful, False if failed
    """
    try:
        import pandas as pd

        # Read the CSV file
        df = pd.read_csv(csv_file)

        # Connect to SQLite and load the data
        with sqlite3.connect(sqlite_db) as sqlite_conn:
            df.to_sql(table_name, sqlite_conn, if_exists='replace', index=False)
            print(f"Successfully loaded {csv_file} into SQLite table '{table_name}'.")
        return True

    except Exception as e:
        print(f"Error loading CSV to SQLite: {e}")
        return False

def run_queries():

    # First load the CSV into SQLite
    if not load_csv_to_sqlite('Small_data.CSV', 'sqlite_file.sqlite', 'small_data'):
        print("Failed to load CSV file. Aborting queries.")
        return
    try:
        with duckdb.connect('file_db.duckdb') as duckdb_conn, \
                sqlite3.connect('sqlite_file.sqlite') as sqlite_conn:

            duckdb_conn.execute("INSTALL sqlite;")
            duckdb_conn.execute("LOAD sqlite;")

            for name, query in queries.items():
                try:
                    # Create initial result table
                    create_table_query = f"""
                        CREATE OR REPLACE TABLE {name}_results AS {query}
                    """
                    duckdb_conn.execute(create_table_query)

                    row_count = duckdb_conn.execute(f"SELECT COUNT(*) FROM {name}_results").fetchone()[0]
                    if row_count > 500:
                        sample_query = f"""
                            CREATE OR REPLACE TABLE {name}_results AS 
                            SELECT * FROM {name}_results USING SAMPLE 500 ROWS;
                        """
                        duckdb_conn.execute(sample_query)
                        print(f"Table {name} had more than 500 rows, reduced to 500.")

                    # Export results
                    result = duckdb_conn.execute(f"SELECT * FROM {name}_results").fetchdf()

                    # Save to SQLite
                    result.to_sql(f"{name}_results", sqlite_conn, if_exists='replace', index=False)
                    print(f"Saved {name}_results table to SQLite.")

                    # Display preview
                    print(f"\nFirst 10 rows of {name}:")
                    print(result.head(10))

                except Exception as e:
                    print(f"Error in {name}: {e}")
                    continue
    except Exception as e:
        print(f"Error establishing database connections: {e}")
    finally:
        # Always close connections in finally block
        if duckdb_conn:
            try:
                duckdb_conn.close()
            except Exception as e:
                print(f"Error closing DuckDB connection: {e}")

        if sqlite_conn:
            try:
                sqlite_conn.close()
            except Exception as e:
                print(f"Error closing SQLite connection: {e}")


if __name__ == "__main__":
    run_queries()