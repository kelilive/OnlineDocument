import pyodbc
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import warnings

# Suppress pandas connection warnings
warnings.filterwarnings("ignore", category=UserWarning)

# --- Configuration ---
config = {
    'server': '192.168.1.1',
    'database': 'database_name',
    'user': 'sa',
    'password': 'password',
    'top_n': 10000, 
    'output_dir': f"DB_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
}

# Connection String
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={config['server']};"
    f"DATABASE={config['database']};"
    f"UID={config['user']};"
    f"PWD={config['password']}"
)

if not os.path.exists(config['output_dir']):
    os.makedirs(config['output_dir'])

def get_table_schema(cursor, table_name):
    """Extract table schema definition"""
    query = (
        f"SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE "
        f"FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' "
        f"ORDER BY ORDINAL_POSITION"
    )
    cursor.execute(query)
    columns = cursor.fetchall()
    
    if not columns: 
        return "-- Schema information unavailable\n"
        
    parts = []
    for col in columns:
        col_def = f"[{col[0]}] {col[1]}"
        if col[2]: 
            col_def += f"({col[2] if col[2] != -1 else 'MAX'})"
        if col[3] == 'NO': 
            col_def += " NOT NULL"
        parts.append(col_def)
        
    return f"CREATE TABLE [{table_name}] (\n  " + ",\n  ".join(parts) + "\n);\n"

def export_database():
    summary_data = []
    conn = None
    try:
        print(f"[INFO] Connecting to server: {config['server']}...")
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Fetch all user table names
        cursor.execute("SELECT name FROM sys.tables WHERE is_ms_shipped = 0 ORDER BY name ASC")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"[INFO] {len(tables)} tables identified. Initializing export...\n")

        for table in tables:
            error_details = ""
            status = "Pending"
            total_rows = 0
            exported_rows = 0
            sql_file = f"Table_{table}.sql"

            try:
                # 1. Get total row count
                count_query = (
                    f"SELECT SUM(st.row_count) FROM sys.dm_db_partition_stats st "
                    f"WHERE object_id = OBJECT_ID('{table}') AND index_id < 2"
                )
                cursor.execute(count_query)
                res = cursor.fetchone()
                total_rows = res[0] if res and res[0] else 0

                # 2. Fetch data
                data_query = f"SELECT TOP {config['top_n']} * FROM [{table}]"
                df = pd.read_sql(data_query, conn)
                exported_rows = len(df)

                # 3. Generate SQL script
                file_path = os.path.join(config['output_dir'], sql_file)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"-- Source Table: {table}\n")
                    f.write(f"IF OBJECT_ID('[{table}]', 'U') IS NOT NULL DROP TABLE [{table}];\n")
                    f.write(get_table_schema(cursor, table))
                    f.write(f"\nSET IDENTITY_INSERT [{table}] ON;\n")
                    
                    for _, row in df.iterrows():
                        cols = ", ".join([f"[{c}]" for c in df.columns])
                        vals = []
                        for v in row:
                            if pd.isna(v): vals.append("NULL")
                            elif isinstance(v, (int, float)): vals.append(str(v))
                            else: vals.append(f"'{str(v).replace('\'','\'\'')}'")
                        f.write(f"INSERT INTO [{table}] ({cols}) VALUES ({', '.join(vals)});\n")
                    
                    f.write(f"SET IDENTITY_INSERT [{table}] OFF;\nGO\n")
                
                status = "Success" if total_rows <= config['top_n'] else "Truncated"
                print(f"[DONE] {table:.<30} ({exported_rows}/{total_rows} rows)")

            except Exception as e:
                error_details = str(e).replace('<', '').replace('>', '')
                status = "Error"
                print(f"[FAIL] Table {table}: {error_details}")

            summary_data.append({
                'TableName': table,
                'TotalRows': str(total_rows),
                'ExportedRows': str(exported_rows),
                'FileName': sql_file if status != "Error" else "N/A",
                'Status': status,
                'ErrorMessage': error_details
            })

        # 4. Generate XML Summary Report
        root = ET.Element("ExportReport")
        root.set("Timestamp", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        for item in summary_data:
            node = ET.SubElement(root, "TableEntry")
            for key, val in item.items():
                child = ET.SubElement(node, key)
                child.text = val

        xml_raw = ET.tostring(root, encoding='utf-8')
        xml_pretty = minidom.parseString(xml_raw).toprettyxml(indent="  ")
        
        report_path = os.path.join(config['output_dir'], "_Summary_Report.xml")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(xml_pretty)

        print(f"\n[FINISH] Export task completed.")
        print(f"[INFO] Summary Report: {report_path}")

    except Exception as e:
        print(f"[CRITICAL] Database connection failed: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    export_database()