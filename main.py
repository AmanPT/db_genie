# main.py placeholder
import streamlit as st
from utils.db_connection import connect_to_db
from utils.schema_mapper import map_schemas
from utils.query_optimizer import optimize_query
from utils.data_migrator import migrate_data

st.set_page_config(page_title="DB Genie: Optimizer & Migrator", layout="wide")
st.title("🧙 DB Genie – Optimize & Migrate Data Across Schemas")

# 1. Connect to Source & Target Databases
st.header("🔌 Database Connection")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Source DB")
    src_type = st.selectbox("Source DB Type", ["sqlite", "postgresql", "mysql"])
    src_uri = st.text_input("Source DB URI", "sqlite:///source.db")

with col2:
    st.subheader("Target DB")
    tgt_type = st.selectbox("Target DB Type", ["sqlite", "postgresql", "mysql"])
    tgt_uri = st.text_input("Target DB URI", "sqlite:///target.db")

if st.button("Connect to Databases"):
    try:
        src_engine, src_metadata = connect_to_db(src_uri)
        tgt_engine, tgt_metadata = connect_to_db(tgt_uri)
        st.session_state['src_engine'] = src_engine
        st.session_state['tgt_engine'] = tgt_engine
        st.success("Connected to both databases!")
    except Exception as e:
        st.error(f"Connection failed: {e}")
# 2. Optimize a SQL Query
st.header("⚡ Query Optimizer")
query = st.text_area("Paste your SQL query to optimize")
if st.button("Optimize Query"):
    if query.strip():
        optimized = optimize_query(query)
        st.code(optimized, language="sql")
    else:
        st.warning("Enter a SQL query to optimize.")

# 3. Schema Mapping & Data Migration
st.header("🔄 Schema Mapper & Migrator")
table_name = st.text_input("Table name to migrate")
if st.button("Map and Migrate"):
    if 'src_engine' in st.session_state and 'tgt_engine' in st.session_state:
        if table_name:
            try:
                mapping = map_schemas(st.session_state['src_engine'], st.session_state['tgt_engine'], table_name)
                migrate_data(st.session_state['src_engine'], st.session_state['tgt_engine'], table_name, mapping)
                st.success("Data migrated successfully!")
            except Exception as e:
                st.error(f"Migration failed: {e}")
        else:
            st.warning("Enter a table name.")
    else:
        st.warning("Please connect to the databases first.")
    
    # 4. Migrate Entire Database
    if st.button("Migrate Entire Database"):
        if 'src_engine' in st.session_state and 'tgt_engine' in st.session_state:
            try:
                from utils.data_migrator import migrate_entire_db
                results = migrate_entire_db(st.session_state['src_engine'], st.session_state['tgt_engine'])
                st.subheader("🔁 Migration Results")
                for tbl, status in results.items():
                    st.write(f"• **{tbl}**: {status}")
            except Exception as e:
                st.error(f"Full DB migration failed: {e}")
        else:
            st.warning("Please connect to the databases first.")