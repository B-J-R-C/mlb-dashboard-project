import sqlite3
import pandas as pd
import os

def run_query():
    db_path = "database/baseball_history.db"
    
    # Check if database there
    if not os.path.exists(db_path):
        print("Error: Database not found! Please run build_db.py first.")
        return

    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        
        print("\n" + "="*45)
        print(" ⚾ Welcome to the Baseball History Query Tool!")
        print("="*45)
        print("Available Years in Database: 2018 - 2022")
        
        while True:
            user_year = input("\nEnter a year to see the league leaders (or type 'quit' to exit): ")
            
            if user_year.lower() == 'quit':
                print("Thanks for using the tool. Goodbye!")
                break
                
            if not user_year.isdigit() or len(user_year) != 4:
                print("Error: Please enter a valid 4-digit year.")
                continue

            # JOIN Query
            query = """
            SELECT 
                e.Year, 
                e.Detail AS Batting_Avg_Leader, 
                p.Player AS Home_Run_Leader
            FROM events e
            JOIN player_stats p ON e.Year = p.Year
            WHERE e.Year = ?
            """
            
            results_df = pd.read_sql_query(query, conn, params=(user_year,))
            
            if results_df.empty:
                print(f"No data found for the year {user_year}.")
            else:
                print(f"\n--- Results for {user_year} ---")
                print(results_df.to_string(index=False))

    except sqlite3.Error as e:
        print(f"A database error occurred: {e}")
    finally:
        # closeconnection
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    run_query()