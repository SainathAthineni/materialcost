import streamlit as st
import requests

# Base URL for the Flask API
BASE_URL = "http://127.0.0.1:5000"

st.title("Material Cost Lookup")

# Option to Add or Update Material
st.header("Add or Update Material")
material_name = st.text_input("Enter material name:")
material_cost = st.number_input("Enter material cost:", min_value=0.0, format="%.2f")

if st.button("Add Material"):
    if material_name and material_cost:
        response = requests.post(
            f"{BASE_URL}/add_material",
            json={"name": material_name, "cost": material_cost}
        )
        
        # Check for various response statuses
        if response.status_code == 201:
            st.success(f"Material '{material_name}' added successfully with cost {material_cost}!")
        elif response.status_code == 200:
            st.success(response.json()["message"])  # If the material exists, it updates
        else:
            # Handle unexpected error messages
            try:
                error_message = response.json().get("error", "Failed to add or update material.")
            except ValueError:
                error_message = "An unexpected error occurred."
            st.error(error_message)
    else:
        st.warning("Please enter both a name and a cost.")

st.markdown("---")

# Option to Get Material Cost
st.header("Get Material Cost")
search_name = st.text_input("Search material by name:")

if st.button("Get Cost"):
    if search_name:
        response = requests.get(f"{BASE_URL}/get_material_cost", params={"name": search_name})
        if response.status_code == 200:
            data = response.json()
            st.write(f"The cost of '{data['name']}' is: ${data['cost']}")
        else:
            # Handle the case when the material is not found
            try:
                error_message = response.json().get("error", "Material not found.")
            except ValueError:
                error_message = "An unexpected error occurred."
            st.error(error_message)
    else:
        st.warning("Please enter a material name to search.")
