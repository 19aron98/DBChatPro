# Import libraries
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.sql_database import SQLDatabase 
import warnings
import re
import os

warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Configure genAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')


# Define your database connection parameters
def initialise_db_connection(user, password, host, name):
    db_user = user
    db_password = password
    db_host = host
    db_name = name

    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    return db

# Get the structure of the database
def get_schema(db):
    schema = db.get_table_info()
    return schema

# Train based on few-shots prompt template
def build_few_shot_prompt(db):

    # Get schema
    db_schema = get_schema(db)

    few_shots = [
        {
            "input": "How many Distinct Products are present?",
            "query": "SELECT COUNT(DISTINCT product_id) FROM products;"
        },
        {
            "input": "What is the total number of orders placed?",
            "query": "SELECT COUNT(*) FROM orders;"
        },
        {
            "input": "Which product has the highest number of orders?",
            "query": "SELECT product_id, COUNT(*) AS order_count FROM order_item GROUP BY product_id ORDER BY order_count DESC LIMIT 1;"
        },
        {
            "input": "How many customers have placed at least one order?",
            "query": "SELECT COUNT(DISTINCT customer_id) FROM orders;"
        },
        {
            "input": "Which customer has placed the highest number of orders?",
            "query": "SELECT customer_id, COUNT(*) AS order_count FROM orders GROUP BY customer_id ORDER BY order_count DESC LIMIT 1;"
        },
        {
            "input": "Which category has the highest number of products?",
            "query": "SELECT category_id, COUNT(*) AS product_count FROM products GROUP BY category_id ORDER BY product_count DESC LIMIT 1;"
        },
        {
            "input": "Retrieve customer feedback along with their order details.",
            "query": "SELECT c.customer_id, c.customer_name, cf.feedback_id, o.order_id FROM customer c JOIN customer_feedbacks cf ON c.customer_id = cf.customer_id JOIN orders o ON c.customer_id = o.customer_id;"
        },
        {
            "input": "List top 5 customer names who ordered 3 times.",
            "query": "SELECT c.customer_name, COUNT(o.order_id) AS order_count FROM customer c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.customer_name HAVING order_count = 3 ORDER BY c.customer_name LIMIT 5;"
        }   
    ]

    prompt = [
        f"""
            You are an expert in converting English questions to SQL query!
            The SQL database has many tables, and these are the schemas: {db_schema}, 
            You can order the results by a relevant column to return the most interesting examples in the database,
            Never query for all the columns from a specific table, only ask for the relevant columns given the question.

            Important: Also the sql code should not have ``` in beginning or end and sql word in output. Please check the column names before executing any query 
            
            You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

            DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

            If the question does not seem related to the database, just return "I don't know" as the answer.

            Here are some examples of user inputs and their corresponding SQL queries:
            """,
        ]

    # Append each example to the prompt
    for sql_example in few_shots:
        prompt.append(
            f"\nExample - {sql_example['input']}, the SQL command will be something like this {sql_example['query']}")

    # Join prompt sections into a single string
    formatted_prompt = [''.join(prompt)]

    return formatted_prompt

def generate_sql_query(prompt, user_question):
    
    sql_query = model.generate_content([prompt[0], user_question])
    sql_query = re.sub(r"(\n|```sql|```|sql)", " ", sql_query.text).strip()
    return sql_query

def run_query(db, sql_query):
    return db.run(sql_query)

def get_answers(schema, sql_response, user_question):
    answer = model.generate_content(f"""
    Based on the sql response, Give answer based on given dataset {schema} and related to the {user_question} asked in proper human english and no sql query at output:

    SQL response: {sql_response}

    """)
    return answer.text