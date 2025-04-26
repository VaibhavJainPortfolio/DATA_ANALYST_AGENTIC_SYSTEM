import openai
import duckdb

def query_data_with_agent(api_key, table_name, user_query):
    openai.api_key = api_key
    schema = duckdb.sql(f"DESCRIBE {table_name}").fetchdf().to_string(index=False)

    prompt = f"""
    You are an AI data expert. Given the table schema:
    {schema}

    Translate the following user question into SQL:
    "{user_query}"
    """

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    sql_query = response.choices[0].message.content.strip()

    try:
        df = duckdb.sql(sql_query).fetchdf()
        return {"answer": f"Here is the result of your query:\n```sql\n{sql_query}```", "df": df}
    except Exception as e:
        return {"answer": f"❌ Error: {e}"}
