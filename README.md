# DBChatPro

DBChatPro is a web application that allows users to query databases using natural language. It converts English questions into SQL queries and returns answers in plain English using the Gemini Pro API.

## Demo Screenshots

### 🏠 Home Page  
![Dashboard without connected to database](Web-App%20Images/Dashboard%20without%20connected%20to%20database.png)


### 📜 SQL Query Generation  
#![SQL Query Generation](images/sql_query_generation.png)

### 📝 Plain English Answer  
#![Plain English Answer](images/plain_english_answer.png)

## Features

- **Natural Language to SQL**: Converts English questions into structured SQL queries.
- **Plain English Answers**: Uses the Gemini Pro API to interpret query results in a human-readable format.
- **User-Friendly Interface**: Simple and intuitive web UI for seamless interaction.
- **Supports Multiple Databases**: Compatible with various SQL databases.

## How It Works

1. **Input an English question** – Users enter a question like _"What are the top 5 best-selling products?"_
2. **SQL Query Generation** – The app translates the question into an SQL query.
3. **Database Execution** – The query is run against the connected database.
4. **Answer Interpretation** – The result is processed and returned in plain English.

## Installation

### Prerequisites

- Python 3.10
- Required Python packages (listed in `requirements.txt`)
- Access to Gemini Pro API
- A supported SQL database (e.g., MySQL, PostgreSQL, SQLite)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/19aron98/DBChatPro.git
   ```
2. **Create a environment**
   ```bash
   conda create -p dbchatpro python==3.10 -y
   conda activate dbchatpro
   ```
3. **Set up environment variables**
   ```bash
   GEMINI_API_KEY="your_gemini_api_key"
   ```
4. **Install the Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run Webapp**
   ```bash
   streamlit run app.py
   ```
### Future Enhancements
- Support for NoSQL databases.
- Improved NLP model for more accurate SQL translations.
- Interactive query optimization suggestions.

### Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

### License
This project is licensed under the Apache License.

