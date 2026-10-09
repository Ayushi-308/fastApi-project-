import sqlite3

def seed_roles_permissions():
    print("Connecting to database...")
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    # Clear existing data to avoid duplicates if run multiple times
    cursor.execute("DELETE FROM role_permissions")
    cursor.execute("DELETE FROM permissions")
    cursor.execute("DELETE FROM roles")

    # Define roles
    roles = ['admin', 'teacher', 'student', 'parent']
    
    # Define permissions
    permissions = [
        'create_record',
        'read_record',
        'update_record',
        'delete_record',
        'read_own_record',
        'read_child_record'
    ]
    
    # Define the mapping between roles and permissions
    role_perms = {
        'admin': ['create_record', 'read_record', 'update_record', 'delete_record'],
        'teacher': ['read_record', 'update_record'],
        'student': ['read_own_record'],
        'parent': ['read_child_record']
    }

    # Insert permissions
    print("Inserting permissions...")
    for p in permissions:
        cursor.execute("INSERT INTO permissions (name) VALUES (?)", (p,))
        
    # Insert roles
    print("Inserting roles...")
    for r in roles:
        cursor.execute("INSERT INTO roles (name) VALUES (?)", (r,))
        
    # Get the inserted IDs so we can map them
    cursor.execute("SELECT id, name FROM permissions")
    perm_dict = {name: p_id for p_id, name in cursor.fetchall()}
    
    cursor.execute("SELECT id, name FROM roles")
    role_dict = {name: r_id for r_id, name in cursor.fetchall()}
    
    # Insert mappings into role_permissions
    print("Mapping permissions to roles...")
    for role_name, perm_names in role_perms.items():
        role_id = role_dict[role_name]
        for perm_name in perm_names:
            perm_id = perm_dict[perm_name]
            cursor.execute(
                "INSERT INTO role_permissions (role_id, permission_id) VALUES (?, ?)", 
                (role_id, perm_id)
            )
            
    conn.commit()
    conn.close()
    print("Success! Roles and permissions have been created and mapped.")

if __name__ == "__main__":
    seed_roles_permissions()
