import streamlit as st
from streamlit_option_menu import option_menu
from src.utils import initialise_db_connection, get_schema, build_few_shot_prompt, generate_sql_query, run_query, get_answers


def main():
    st.set_page_config(page_title="DBChatPro", layout="wide", page_icon="📊")

    if "database_connect" not in st.session_state:
        st.session_state.database_connect = {}

    # Sidebar menu options 
    with st.sidebar:
        selected = option_menu("DBChatPro", 
                               ["Dashboard", "Connection"],
                               menu_icon="menu-button-wide", 
                               icons=['house', 'plug'],
                               default_index=0)
        
    # Sidebar settings
    if selected == 'Connection':
        st.title("🔗 Connect to Database")
    
        with st.form("connection_form"):
            host = st.text_input("Host", "")
            user = st.text_input("Username", "")
            password = st.text_input("Password", type="password")
            db_name = st.text_input("Database Name")
            
            if st.form_submit_button("Connect"):
                with st.spinner("Connecting..."):
                    db = initialise_db_connection(user, password, host, db_name)
                    if db:
                        st.session_state.database_connect[db_name] = db
                        st.success(f"Connected to {db_name}")
                    else:
                        st.error("Connection failed. Please check your credentials and try again.")
            
    elif selected == 'Dashboard':
        st.title("💬 DBChatPro")
    
        if not st.session_state.database_connect:
            st.warning("Connect to a database first!")
        else:
            # Get the first available database connection
            db_name, db = next(iter(st.session_state.database_connect.items()))

            with st.expander(f"📊 Selected Database : {db_name}", expanded=False):
                for title in db.get_usable_table_names():
                    st.markdown(f"* {title}")
            
            # User question
            question = st.text_area("Your prompt")
            show_sql = st.checkbox("Show generated SQL query")

            if st.button("Submit"):
                with st.spinner("Getting the AI query..."):
                    # Generate few-shot prompt
                    few_shots_prompt = build_few_shot_prompt(db)

                    # Generate SQL query
                    sql_query = generate_sql_query(prompt=few_shots_prompt, user_question=question)
                    response = run_query(db, sql_query)

                    # Get answers
                    answers = get_answers(schema=get_schema(db), sql_response=response, user_question=question)

                    # Display results
                    st.subheader("Result:")
                    if show_sql:
                            with st.expander("Generated SQL"):
                                st.code(sql_query, language="sql")
                    st.write(answers)

            


if __name__ == "__main__":
    main()