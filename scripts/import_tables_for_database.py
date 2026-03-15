import pyodbc
import os
import time
import re
from datetime import datetime

# --- Configuration ---
config = {
    'server': '192.168.1.1',
    'database': 'target_database_name',
    'user': 'sa',
    'password': 'password',
    'input_dir': 'DB_Export_20240520_123456',  # Path to your export folder
}

# Connection String using ODBC Driver 17
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={config['server']};"
    f"DATABASE={config['database']};"
    f"UID={config['user']};"
    f"PWD={config['password']};"
    f"MultipleActiveResultSets=True;"
)

def run_import():
    if not os.path.exists(config['input_dir']):
        print(f"[ERROR] Directory not found: {config['input_dir']}")
        return

    # Filter and sort .sql files to ensure logical order
    sql_files = sorted([f for f in os.listdir(config['input_dir']) if f.endswith('.sql')])
    total_files = len(sql_files)
    
    print(f"[START] Preparing to import {total_files} files...")

    conn = None
    try:
        conn = pyodbc.connect(conn_str)
        conn.autocommit = True  # Significant speed boost for massive inserts
        cursor = conn.cursor()
        
        start_time = time.time()
        success_count = 0
        error_count = 0

        for i, file_name in enumerate(sql_files, 1):
            file_path = os.path.join(config['input_dir'], file_name)
            print(f"[{i}/{total_files}] Processing: {file_name}", end="\r")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Split by 'GO' (case-insensitive) as pyodbc cannot execute 'GO' directly
                batches = re.split(r'(?i)^\s*GO\s*$', content, flags=re.MULTILINE)
                
                for batch in batches:
                    clean_batch = batch.strip()
                    if clean_batch:
                        cursor.execute(clean_batch)
                
                success_count += 1
            except Exception as e:
                error_count += 1
                print(f"\n[ERROR] Failed in {file_name}: {e}")

        end_time = time.time()
        print(f"\n\n[COMPLETED] Task finished in {round(end_time - start_time, 2)}s")
        print(f"Success: {success_count} | Errors: {error_count}")

    except Exception as e:
        print(f"[CRITICAL] Connection failed: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    run_import()