import sqlite3

def dump_db():
    print("Connecting to database...")
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table_name in tables:
        table_name = table_name[0]
        print(f"\n======================================")
        print(f"TABLE: {table_name}")
        print(f"======================================")
        
        # Get columns
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [info[1] for info in cursor.fetchall()]
        print("Columns:", " | ".join(columns))
        print("-" * 40)
        
        # Get data
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        
        if not rows:
            print("(Table is empty)")
        else:
            for row in rows:
                print(row)
            
    conn.close()

if __name__ == "__main__":
    dump_db()
