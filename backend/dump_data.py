import sqlite3
import json
import os

db_path = os.path.join(os.path.dirname(__file__), "backup_backend", "rental_blossoms.db")
output_path = os.path.join(os.path.dirname(__file__), "Readable_Database.json")

def dump_db_to_json():
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()
        
        data = [dict(row) for row in rows]
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        print(f"Successfully dumped {len(data)} records to Readable_Database.json")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    dump_db_to_json()
