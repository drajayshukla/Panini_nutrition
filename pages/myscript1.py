import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Function to connect to Google Sheets
def connect_to_google_sheet(sheet_id):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("wired-rex-384216-022ef0ae8b96.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(sheet_id).sheet1
    return sheet

# Initialize dynamic lists in session state
def initialize_session_state():
    if "topics" not in st.session_state:
        st.session_state["topics"] = []
    if "subtopics" not in st.session_state:
        st.session_state["subtopics"] = []
    if "keywords" not in st.session_state:
        st.session_state["keywords"] = []
    if "facts" not in st.session_state:
        st.session_state["facts"] = set()

def load_data_to_session(sheet):
    all_data = sheet.get_all_records()
    for row in all_data:
        if row["Topic"] and row["Topic"] not in st.session_state["topics"]:
            st.session_state["topics"].append(row["Topic"])
        if row["Sub_topic"] and row["Sub_topic"] not in st.session_state["subtopics"]:
            st.session_state["subtopics"].append(row["Sub_topic"])
        if row["Key_word"] and row["Key_word"] not in st.session_state["keywords"]:
            st.session_state["keywords"].append(row["Key_word"])
        if row["Fact"]:
            st.session_state["facts"].add(row["Fact"])
    return all_data

def main():
    st.title("Scientific Data Collector with Fact-Based Duplicate Prevention")
    st.write("This app dynamically updates Topics, Subtopics, and Keywords and prevents duplicate entries based on Fact.")

    # Connect to Google Sheets
    sheet_id = "1sT6uOxefVB5sV8d_RU7mXFxKFbUfM8__gVnUnn-aY3M"
    try:
        sheet = connect_to_google_sheet(sheet_id)
    except Exception as e:
        st.error("Failed to connect to Google Sheet. Check the credentials and Sheet ID.")
        st.error(e)
        return

    # Initialize session state
    initialize_session_state()

    # Load data into session state
    try:
        all_data = load_data_to_session(sheet)
    except Exception as e:
        st.error("Failed to load data from Google Sheet.")
        st.error(e)
        return

    # Dropdowns for Topics, Subtopics, and Keywords
    selected_topic = st.selectbox("Select or Add Topic", options=[""] + st.session_state["topics"], key="topic_dropdown")
    new_topic = st.text_input("Or Add a New Topic", key="new_topic_input")

    selected_subtopic = st.selectbox("Select or Add Subtopic", options=[""] + st.session_state["subtopics"], key="subtopic_dropdown")
    new_subtopic = st.text_input("Or Add a New Subtopic", key="new_subtopic_input")

    selected_keyword = st.selectbox("Select or Add Keyword", options=[""] + st.session_state["keywords"], key="keyword_dropdown")
    new_keyword = st.text_input("Or Add a New Keyword", key="new_keyword_input")

    # Inputs for Reference and Fact
    reference = st.text_input("Reference (Optional)", placeholder="Enter the reference")
    fact = st.text_area(
        "Fact (Optional)",
        placeholder="Enter the fact",
        height=150,  # Increase height for better usability
        label_visibility="visible"
    )

    # Save Entry Button
    if st.button("Save Entry"):
        topic_to_save = new_topic if new_topic else selected_topic
        subtopic_to_save = new_subtopic if new_subtopic else selected_subtopic
        keyword_to_save = new_keyword if new_keyword else selected_keyword

        # Ensure non-empty fields and no duplicate Facts
        if not topic_to_save or not subtopic_to_save or not keyword_to_save:
            st.warning("Please provide values for Topic, Subtopic, and Keyword.")
        elif fact in st.session_state["facts"]:
            st.warning("Duplicate entry! This Fact already exists in the Google Sheet.")
        else:
            try:
                sheet.append_row([topic_to_save, subtopic_to_save, keyword_to_save, reference, fact])
                st.success("Entry saved successfully!")
                # Update session state
                if topic_to_save not in st.session_state["topics"]:
                    st.session_state["topics"].append(topic_to_save)
                if subtopic_to_save not in st.session_state["subtopics"]:
                    st.session_state["subtopics"].append(subtopic_to_save)
                if keyword_to_save not in st.session_state["keywords"]:
                    st.session_state["keywords"].append(keyword_to_save)
                st.session_state["facts"].add(fact)
            except Exception as e:
                st.error("Failed to save data to Google Sheet.")
                st.error(e)

    # Display Google Sheet content
    st.write("### Google Sheet Content")
    try:
        st.dataframe(sheet.get_all_records())
    except Exception as e:
        st.error("Failed to fetch data from Google Sheet.")
        st.error(e)


if __name__ == "__main__":
    main()
