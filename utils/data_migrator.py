# utils/data_migrator.py
from sqlalchemy import Table, insert, select

def migrate_data(src_engine, tgt_engine, table_name, mapping):
    src_table = Table(table_name, src_engine, autoload_with=src_engine)
    tgt_table = Table(table_name, tgt_engine, autoload_with=tgt_engine)

    conn_src = src_engine.connect()
    conn_tgt = tgt_engine.connect()

    rows = conn_src.execute(select(src_table)).fetchall()

    for row in rows:
        new_row = {mapping.get(col): row[col] for col in row.keys() if mapping.get(col)}
        stmt = insert(tgt_table).values(**new_row)
        conn_tgt.execute(stmt)

    conn_src.close()
    conn_tgt.close()