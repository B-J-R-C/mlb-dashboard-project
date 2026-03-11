import pandas as pd
import sqlite3
import os

def build_database():
    # 1. database folder exists? yess
    os.makedirs("database", exist_ok=True)
    db_path = "database/baseball_history.db"
    
    print(f"Connecting to database at {db_path}...")
    
    try:
        # Connect to SQLite 
        conn = sqlite3.connect(db_path)
        
        # 2. Load CSV  into pandas dataframes
        print("Loading CSV files...")
        try:
            events_df = pd.read_csv("events.csv")
            stats_df = pd.read_csv("player_stats.csv")
        except FileNotFoundError as e:
            print(f"Error reading CSV files: {e}")
            print("Make sure you run scraper.py first so the CSVs exist!")
            return

        # 3. Data Cleaning & Transformation
        print("Cleaning data and formatting types...")
        # year column integar - ha why no reason
        events_df['Year'] = pd.to_numeric(events_df['Year'], errors='coerce').fillna(0).astype(int)
        stats_df['Year'] = pd.to_numeric(stats_df['Year'], errors='coerce').fillna(0).astype(int)
        
        # 4. Import Dataframes
        print("Importing data into SQLite tables...")
        events_df.to_sql("events", conn, if_exists="replace", index=False)
        stats_df.to_sql("player_stats", conn, if_exists="replace", index=False)
        
        print("\nSuccess! Created database tables: 'events' and 'player_stats'.")
        
    except sqlite3.Error as e:
        print(f"A database error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # 5. close the connection
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    build_database()