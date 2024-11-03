import streamlit as st
import sqlite3

# Set up the SQLite database connection
def init_db():
    conn = sqlite3.connect('materials.db')
    cursor = conn.cursor()
    # Create the materials table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            cost REAL NOT NULL
        )
    ''')
    conn.commit()
    return conn

# Initialize the database
conn = init_db()

st.title("Material Cost Lookup")

# Option to Add or Update Material
st.header("Add or Update Material")
material_name = st.text_input("Enter material name:")
material_cost = st.number_input("Enter material cost:", min_value=0.0, format="%.2f")

if st.button("Add or Update Material"):
    if material_name and material_cost:
        cursor = conn.cursor()
        
        # Check if the material already exists
        cursor.execute("SELECT * FROM materials WHERE name = ?", (material_name,))
        result = cursor.fetchone()
        
        if result:
            # Update existing material
            cursor.execute("UPDATE materials SET cost = ? WHERE name = ?", (material_cost, material_name))
            conn.commit()
            st.success(f"Cost of '{material_name}' updated to {material_cost}")
        else:
            # Insert new material
            cursor.execute("INSERT INTO materials (name, cost) VALUES (?, ?)", (material_name, material_cost))
            conn.commit()
            st.success(f"Material '{material_name}' added with cost {material_cost}")
    else:
        st.warning("Please enter both a name and a cost.")

st.markdown("---")

# Option to Get Material Cost
st.header("Get Material Cost")
search_name = st.text_input("Search material by name:")

if st.button("Get Cost"):
    if search_name:
        cursor = conn.cursor()
        cursor.execute("SELECT cost FROM materials WHERE name = ?", (search_name,))
        result = cursor.fetchone()
        
        if result:
            st.write(f"The cost of '{search_name}' is: ${result[0]}")
        else:
            st.error("Material not found.")
    else:
        st.warning("Please enter a material name to search.")
