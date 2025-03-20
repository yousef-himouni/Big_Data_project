import duckdb
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to connect to DuckDB
def connect_to_duckdb():
    """Connect to DuckDB and return the connection object."""
    try:
        conn = duckdb.connect(database='file_db.duckdb')
        logging.info("Connected to DuckDB successfully.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to DuckDB: {e}")
        raise


# Function to load data into DuckDB
def load_data_into_duckdb(conn):
    """Load the CSV file into DuckDB."""
    csv_path = r"1 Full Divvy Dataframe final.csv"
    try:
        # Load CSV into DuckDB
        conn.execute(f""" 
            CREATE TABLE IF NOT EXISTS divvy_data AS 
            SELECT * FROM read_csv_auto('{csv_path}')
        """)
        logging.info("Data loaded into DuckDB successfully.")
    except Exception as e:
        logging.error(f"Failed to load data into DuckDB: {e}")
        raise


# Main function
if __name__ == "__main__":
    try:
        # Connect to DuckDB
        conn = connect_to_duckdb()

        # Load data into DuckDB
        load_data_into_duckdb(conn)

        # Close connection
        conn.close()
        logging.info("Data loaded into DuckDB successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")