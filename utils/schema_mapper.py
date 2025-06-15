# utils/schema_mapper.py
import openai
import json
from sqlalchemy import inspect

openai.api_key = os.getenv("OPENAI_API_KEY")

def map_schemas(src_engine, tgt_engine, table_name):
    insp_src = inspect(src_engine)
    insp_tgt = inspect(tgt_engine)

    src_columns = insp_src.get_columns(table_name)
    tgt_columns = insp_tgt.get_columns(table_name)

    prompt = f"""
Map the source table schema to the target table schema.
Source columns: {src_columns}
Target columns: {tgt_columns}
Return a JSON with key as source column and value as target column.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)
