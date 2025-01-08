
import os
import streamlit as st
import sqlite3
import pandas as pd

# Establish a connection to the SQLite database (or create it if it doesn't exist)
PATH = os.environ.get("STREAMLIT_SQLIT_PATH")
conn = sqlite3.connect(PATH)  # Replace 'your_database.db' with your desired filename
cursor = conn.cursor()

def delete_items(selected_indices, df):  # Refactor into a function
    try:
        for index in selected_indices:
            item_id = df.loc[index, "id"]
            st.write(item_id)
            cursor.execute("DELETE FROM items WHERE id = ?", (int(item_id),))
        conn.commit() # Commit AFTER the loop for efficiency
        st.success("Selected items deleted successfully!")
        return True  # Indicate success
    except Exception as e:
        conn.rollback()  # Rollback in case of error
        st.error(f"Error deleting items: {e}")
        return False # Indicate failure



def fetch_data(): # Function to fetch data fresh each time
    df = pd.read_sql_query("SELECT * FROM items", conn) # or however you get your df
    return df


def update_items( df):

    try:
        for index, row in df.iterrows():
            new_quantity = st.number_input(f"Quantity for {row['name']}:", min_value=0, value=row['quantity'], key=f"quantity_{row['id']}")  # Unique key for each input
            if st.button(f"Update {row['name']}", key=f"update_button_{row['id']}"):  # Unique key for each button
                cursor.execute("UPDATE items SET quantity = ? WHERE id = ?", (new_quantity, row['id']))
        conn.commit()
        st.success(f"Updated quantity for {row['name']}.")  # Provide specific feedback 
        return True  # Indicate success  
    except Exception as e:
        conn.rollback()  # Rollback in case of error
        st.error(f"Error deleting items: {e}")
        return False # Indicate failure      

# Streamlit interaction example:

# # Add items to the database
st.subheader("Add Item")
item_name = st.text_input("Item Name")
item_quantity = st.number_input("Quantity", min_value=0, step=1)

if st.button("Add"):
    try:
        cursor.execute("INSERT INTO items (name, quantity) VALUES (?, ?)", (item_name, item_quantity))
        conn.commit()
        st.success(f"Added {item_name} to the database.")

    except Exception as e:
        conn.rollback()  # Rollback in case of error
        st.error(f"Error deleting items: {e}")


# Display the database contents
st.subheader("Database Contents")
try:
    #df = pd.read_sql_query("SELECT * FROM items", conn)  # Use pandas for easy display
    df = fetch_data()
    st.dataframe(df)
except Exception as e:
    st.error(f"Error reading from database: {e}")  # Handle potential errors gracefully


    # Option to delete items
selected_indices = st.multiselect("Select items to delete:", df.index)
if st.button("Delete"):
    delete_items(selected_indices,df )

with st.expander("Update Quantities"):  # Makes the update section collapsible

    update_items( df)






# Close the connection when the app is done (important!)
conn.close()

















#Example: Create a table (if it doesn't already exist)
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS items (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         quantity INTEGER
#     )
# ''')

# # Commit the changes (if you created a table or inserted data)
# conn.commit()