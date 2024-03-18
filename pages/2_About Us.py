import streamlit as st

# # Team member data (replace with your actual data)
team_members = [
    {"image": "/Users/atrijoshi/Downloads/AI&DS/Machine Learning/Code/Third_Eye_Modular/profiles/sameer.jpeg", "name": "Sameer Sharma", "role": "Team Lead", "tagline": "Third Eye"},
    {"image": "/Users/atrijoshi/Downloads/AI&DS/Machine Learning/Code/Third_Eye_Modular/profiles/Shubham.jpeg", "name": "Shubham Bhavsar", "role": "Machine Learning Lead", "tagline": "Third Eye"},
    {"image": "/Users/atrijoshi/Downloads/AI&DS/Machine Learning/Code/Third_Eye_Modular/profiles/Atri_joshi.jpeg", "name": "Atri Joshi", "role": "Data Lead", "tagline": "Third Eye"},
   
]
# cols = 4

# def create_team_card(member):
#   """Creates a Streamlit card for each team member"""
#   st.write(f"**{member['name']}**")
#   st.image(member['image'], width=150)
#   st.write(f"{member['role']}")
#   st.write(f"{member['tagline']}")
#   st.write("---")

# # Display team members in a grid layout
# num_rows = (len(team_members) // cols) + (len(team_members) % cols > 0)  # Calculate required rows
# for i in range(num_rows):
#   cols_in_row = cols if i < num_rows - 1 else len(team_members) % cols  # Adjust last row columns  

#   # Create columns within each row (no need for 'with' statement here)
#   inner_columns = st.columns(cols_in_row)

#   for j in range(cols_in_row):
#     member_index = i * cols + j
#     if member_index < len(team_members):
#       create_team_card(team_members[member_index])

# st.write("We are passionate about building innovative solutions. Get to know our amazing team!")


cols = 4

def create_team_card(member):
    """Creates a Streamlit card for each team member"""
    st.write(f"**{member['name']}**")
    st.image(member['image'], width=150)
    st.write(f"{member['role']}")
    st.write(f"{member['tagline']}")
    st.write("---")
# Display team members in a grid layout
num_rows = (len(team_members) + cols - 1) // cols
row_counter = 0
for i in range(num_rows):
    row_counter += 1
    cols_in_row = min(cols, len(team_members) - (i * cols))
    inner_columns = st.columns(cols_in_row)

    for j in range(cols_in_row):
        member_index = (i * cols) + j
        with inner_columns[j]:
            create_team_card(team_members[member_index])
    if row_counter < num_rows:
        st.write("---")  # Add horizontal line between rows

st.write("We are passionate about building innovative solutions. Get to know our amazing team!")