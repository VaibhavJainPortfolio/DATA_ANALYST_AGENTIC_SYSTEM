import openai
import duckdb

def query_data_with_agent(api_key, table_name, user_query):
    openai.api_key = api_key
    schema = duckdb.sql(f"DESCRIBE {table_name}").fetchdf().to_string(index=False)

    prompt = f"""
    You are an AI SQL expert.
    
    Given the following table schema:
    {schema}
    
    Translate the user's question into a valid DuckDB SQL query.
    
    Important Rules:
    - ONLY return the SQL query.
    - DO NOT explain anything.
    - DO NOT add any text before or after the SQL.
    - ONLY output pure SQL that can be executed directly.
    
    User question: "{user_query}"
    """

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    sql_query = response.choices[0].message.content.strip()
    
    try:
        df = duckdb.sql(sql_query).fetchdf()
        return {"answer": f"Here is the result of your query:\n```sql\n{sql_query}\n```", "df": df}
    except Exception as e:
        return {"answer": f"❌ Error: {e}"}
