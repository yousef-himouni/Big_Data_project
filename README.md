# Divvy Bike Trip Dataset

Submitted by: Yousef Himouni (324145010) & Razi Shibli (324259555)
User: yousefhi & razish

## Files included:

### Python Script:
- duck_data_proc.py: Loads CSV data into DuckDB, creates a table, and exports
  a small sample for analysis.
- data_analyzer.py: Runs SQL queries to analyze trends, user segmentation and
  Processes data in DuckDB and stores results in SQLite.
- dashboard.py: A Streamlit dashboard for visualizing trends, displaying data,
  and enabling interactive analysis.
- schema.py: Defines the data structure using Nodes & Relationships, mapping connections.
### Data Files:
- sqlite_file.sqlite: Stores processed query results for efficient retrieval in the dashboard.
- Small_data.csv: A sample dataset for testing and analysis.
### Documentation:
- README.md: This file

## How to run:
1. Install required packages: pip install -r requirements.txt
2. Loading Dataset: duck_data_proc.py
3. Processes data- analyze data - pass to SQLite : data_analyzer.py
4. Run the Streamlit dashboard: streamlit run dashboard.py
5. Schema (to see the Relationships & Nodes): schema.py
 
For any questions, please contact.
