"""
GYM Management System — Streamlit UI
--------------------------------------
A Streamlit front-end for the GYM Management System.
Data is persisted in database.json (same format as the CLI version),
so an existing database.json from the CLI script keeps working here.

Run with:
    streamlit run app.py
"""

import json
import random
import string
import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

DB_FILE = "database.json"

# ----------------------------------------------------------------------
# Data layer
# ----------------------------------------------------------------------


def load_data():
    if Path(DB_FILE).exists():
        with open(DB_FILE) as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def new_gym_id():
    alpha = random.choices(string.ascii_lowercase, k=2)
    num = random.choices(string.digits, k=4)
    gym_id = alpha + num
    random.shuffle(gym_id)
    return "".join(gym_id)


def find_user(data, roll_no, password):
    for u in data:
        if u.get("Roll_No") == roll_no and u.get("Password") == password:
            return u
    return None


def find_user_by_roll(data, roll_no):
    for u in data:
        if u.get("Roll_No") == roll_no:
            return u
    return None


# ----------------------------------------------------------------------
# App setup / session state
# ----------------------------------------------------------------------

st.set_page_config(page_title="GYM Management System", page_icon="🏋️", layout="wide")

if "data" not in st.session_state:
    st.session_state.data = load_data()

if "logged_in_roll" not in st.session_state:
    st.session_state.logged_in_roll = None


def current_user():
    if not st.session_state.logged_in_roll:
        return None
    return find_user_by_roll(st.session_state.data, st.session_state.logged_in_roll)


def persist():
    save_data(st.session_state.data)


# ----------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------

st.sidebar.title("🏋️ GYM Menu")

user = current_user()

if user:
    st.sidebar.success(f"Logged in as **{user['Name']}**\nRoll No: {user['Roll_No']}")
    page = st.sidebar.radio(
        "Navigate",
        ["Profile", "Daily Update", "Update Profile", "Progress Charts", "Logout"],
    )
else:
    page = st.sidebar.radio("Navigate", ["Login", "Create Account"])

st.title("🏋️ GYM Management System")

# ----------------------------------------------------------------------
# Auth pages
# ----------------------------------------------------------------------

if page == "Create Account":
    st.header("Create a New Account")

    with st.form("create_account_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        email = st.text_input("G-Mail ID")
        mobile = st.text_input("Mobile Number (10 digits)")
        age = st.number_input("Age", min_value=17, max_value=100, step=1)
        weight = st.text_input("Weight (Kg)")
        height = st.text_input("Height (Cm)")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        parent_contact = st.text_input("Parent's Mobile Number (10 digits)")
        password = st.text_input("Password (min 8 chars)", type="password")
        submitted = st.form_submit_button("Create Account")

    if submitted:
        errors = []
        if not name.strip():
            errors.append("Name is required.")
        if "@" not in email:
            errors.append("Enter a valid e-mail address.")
        if not (mobile.isdigit() and len(mobile) >= 10):
            errors.append("Mobile number must be at least 10 digits.")
        if not (parent_contact.isdigit() and len(parent_contact) >= 10):
            errors.append("Parent contact must be at least 10 digits.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            roll_no = "0156MG2610" + str(len(st.session_state.data) + 1)
            gym_id = new_gym_id()
            new_user = {
                "Name": name,
                "G_Mail": email,
                "Mobile": int(mobile),
                "Age": int(age),
                "Weight": weight,
                "Height": height,
                "Gender": gender,
                "Parent_Contact": int(parent_contact),
                "GYM_id": gym_id,
                "Roll_No": roll_no,
                "Password": password,
                "Steps": [],
                "Calories": [],
                "Exercises": [],
            }
            st.session_state.data.append(new_user)
            persist()
            st.success(
                f"Account created! Roll No: **{roll_no}** | GYM ID: **{gym_id}**  \n"
                "Save these — you'll need the Roll No and password to log in."
            )

elif page == "Login":
    st.header("Member Login")

    with st.form("login_form"):
        roll_no = st.text_input("Roll No")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        matched = find_user(st.session_state.data, roll_no, password)
        if matched:
            st.session_state.logged_in_roll = matched["Roll_No"]
            st.rerun()
        else:
            st.error("You are not a member of the gym (check Roll No / Password).")

elif page == "Logout":
    st.session_state.logged_in_roll = None
    st.success("Logged out.")
    st.rerun()

# ----------------------------------------------------------------------
# Member pages (require login)
# ----------------------------------------------------------------------

elif page == "Profile":
    st.header("Your Profile")
    cols = st.columns(2)
    fields = list(user.items())
    half = len(fields) // 2 + 1
    for col, chunk in zip(cols, [fields[:half], fields[half:]]):
        with col:
            for key, value in chunk:
                if key in ("Steps", "Calories", "Exercises", "Password"):
                    continue
                st.write(f"**{key}:** {value}")

elif page == "Daily Update":
    st.header("Log Today's Activity")
    today = datetime.date.today().isoformat()

    tab1, tab2, tab3 = st.tabs(["🚶 Steps", "🔥 Calories", "💪 Exercise"])

    with tab1:
        steps = st.number_input("Steps taken today", min_value=0, step=100, key="steps_input")
        if st.button("Log Steps"):
            cal = round(0.05 * steps, 2)
            user["Steps"].append({"date": today, "value": int(steps)})
            user["Calories"].append({"date": today, "value": cal})
            persist()
            st.success(f"Logged {int(steps)} steps (~{cal} kcal).")

    with tab2:
        cal_manual = st.number_input("Calories burned today", min_value=0, step=10, key="cal_input")
        if st.button("Log Calories"):
            user["Calories"].append({"date": today, "value": int(cal_manual)})
            persist()
            st.success(f"Logged {int(cal_manual)} kcal.")

    with tab3:
        exercise_map = {
            "Chest": 1, "Legs": 2, "Biceps": 3,
            "Triceps": 4, "Abs": 5, "Back": 6,
        }
        exercise = st.selectbox("Exercise type", list(exercise_map.keys()))
        duration = st.number_input("Duration (minutes)", min_value=1, step=5, key="dur_input")
        if st.button("Log Exercise"):
            cal_burned = 2 * int(duration)
            user["Exercises"].append({"date": today, "type": exercise, "duration": int(duration)})
            user["Calories"].append({"date": today, "value": cal_burned})
            persist()
            st.success(f"Logged {int(duration)} min of {exercise} (~{cal_burned} kcal).")

elif page == "Update Profile":
    st.header("Update Your Details")
    st.caption("Roll No, GYM ID, and Gender cannot be changed.")

    with st.form("update_form"):
        name = st.text_input("Name", value=user["Name"])
        email = st.text_input("G-Mail", value=user["G_Mail"])
        mobile = st.text_input("Mobile", value=str(user["Mobile"]))
        age = st.number_input("Age", min_value=17, max_value=100, value=int(user["Age"]))
        weight = st.text_input("Weight (Kg)", value=user["Weight"])
        height = st.text_input("Height (Cm)", value=user["Height"])
        parent_contact = st.text_input("Parent Contact", value=str(user["Parent_Contact"]))
        new_password = st.text_input(
            "New Password (leave blank to keep current)", type="password"
        )
        submitted = st.form_submit_button("Save Changes")

    if submitted:
        if "@" not in email:
            st.error("Invalid e-mail address — not saved.")
        else:
            user["Name"] = name
            user["G_Mail"] = email
            user["Mobile"] = int(mobile) if mobile.isdigit() and len(mobile) >= 10 else user["Mobile"]
            user["Age"] = int(age)
            user["Weight"] = weight
            user["Height"] = height
            user["Parent_Contact"] = (
                int(parent_contact) if parent_contact.isdigit() and len(parent_contact) >= 10
                else user["Parent_Contact"]
            )
            if len(new_password) >= 8:
                user["Password"] = new_password
            persist()
            st.success("Details updated successfully.")

elif page == "Progress Charts":
    st.header(f"Progress for {user['Name']} ({user['Roll_No']})")

    steps = user.get("Steps", [])
    calories = user.get("Calories", [])

    if not steps and not calories:
        st.info("No data logged yet — log some activity first.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Steps Over Time")
            if steps:
                df_steps = pd.DataFrame(steps).groupby("date", as_index=False)["value"].sum()
                df_steps = df_steps.rename(columns={"value": "Steps"}).set_index("date")
                st.line_chart(df_steps)
            else:
                st.write("No step data yet.")

        with col2:
            st.subheader("Calories Burned Over Time")
            if calories:
                df_cal = pd.DataFrame(calories).groupby("date", as_index=False)["value"].sum()
                df_cal = df_cal.rename(columns={"value": "Calories"}).set_index("date")
                st.bar_chart(df_cal)
            else:
                st.write("No calorie data yet.")

        st.subheader("Exercise Log")
        exercises = user.get("Exercises", [])
        if exercises:
            st.dataframe(pd.DataFrame(exercises), use_container_width=True)
        else:
            st.write("No exercises logged yet.")
