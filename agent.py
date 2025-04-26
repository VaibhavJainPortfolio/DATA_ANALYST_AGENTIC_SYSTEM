import openai
import duckdb

def query_data_with_agent(api_key, table_name, user_query):
    # Set the OpenAI API key
    openai.api_key = api_key

    # Always use the fixed uploaded table: uploaded_data
    schema = duckdb.sql("DESCRIBE uploaded_data").fetchdf().to_string(index=False)

    # Prepare the prompt for GPT-4o
    prompt = f"""
    You are an AI SQL expert.

    The user has uploaded a table called 'uploaded_data' with the following schema:
    {schema}

    Translate the user's question into a valid DuckDB SQL query, assuming the table name is 'uploaded_data'.

    Important Instructions:
    - ONLY output the SQL query.
    - DO NOT add any explanations.
    - DO NOT add any triple backticks ``` or markdown.
    - Directly give pure SQL that can be executed on DuckDB.

    User question: "{user_query}"
    """

    # Call GPT-4o
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract the generated SQL
    sql_query = response.choices[0].message.content.strip()

    # Remove any unwanted backticks if still present
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    # 🚀 Now run the generated SQL directly
    try:
        df = duckdb.sql(sql_query).fetchdf()
        return {
            "answer": f"Here is the result of your query:\n```sql\n{sql_query}\n```",
            "df": df
        }
    except Exception as e:
        return {
            "answer": f"❌ Error: {e}"
        }
