# QueryGenie

QueryGenie is a sophisticated tool that allows users to interact with a SQL database using natural language queries. Leveraging advanced AI models, it translates English questions into SQL queries, executes them on the database, and returns the results in a well-formatted, user-friendly manner.

## Features

- Convert natural language questions to SQL queries
- Execute SQL queries on a MySQL database
- Return results in a well-formatted, user-friendly manner
- Use Google Generative AI for natural language processing
- Maintain conversational context for seamless interactions

## Getting Started

### Prerequisites

- Python 3.10
- MySQL database
- Google Generative AI API Key

### Installation

1. Clone the repository:
   
   git clone https://github.com/yourusername/QueryGenie.git
   cd QueryGenie

2. Install the required Python Package

    pip install -r requirements.txt

3. Set up the Environment Variable

    Create a .env file in the root directory of the project.
    Add the following content to the .env file: 

        GOOGLE_API_KEY=your_google_api_key

4. Set up the MySQL Database Connection

    Ensure MySQL server is running and accessible.
    Create a database named XYZ. (In my case: 26ideas)
    Update database connection details in the create_connection function in the script.

### Usage

1. Run the python file or the Jupyter notebook cells individually. 

2. Follow the prompts to interact with the system using natural language queries:
    - Who are the contacts working for Microsoft?
    - How many entries of records are present in newContacts?
    - List all contacts who are investors.
    - List all contacts who are working in software companies but are not software developers.
    - What is the designation of Sahil Shah?
    - Provide LinkedIn URLs of all companies.

### Project Structure 
├── Final_Gemini_Query_Model.ipynb / Final_Gemini_Query_Model.py <br />
├── requirements.txt <br />
├── README.md <br />
├── .env <br />

### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements
[Google GenerativeAi](https://ai.google.dev/api/python/google/generativeai) <br />
[MySQL Connector](https://dev.mysql.com/doc/connector-python/en/) <br />
