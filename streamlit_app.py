import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(layout="wide")
session = get_active_session()

st.title("💊 Pharma Supply Chain: Hybrid Copilot")
st.markdown("Dynamic Intent Routing -> Governed Data -> Qualitative Insights")

user_query = st.text_input("Ask a supply chain question (e.g., 'Check inventory health' or 'Check supplier reliability'):")

if st.button("Analyze"):
    if user_query:
        with st.spinner("🧠 1. Cortex LLM routing intent..."):
            # LLM ROUTING: Determine which semantic view to use using native SQL
            route_prompt = f"Categorize this question into strictly one of two words: 'INVENTORY' or 'SUPPLIERS'. Return ONLY the word, nothing else. Question: {user_query}"
            
            # Using $$ to safely escape the prompt string in SQL
            intent_query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3-8b', $${route_prompt}$$)"
            intent = session.sql(intent_query).collect()[0][0].strip().upper()
            
            st.info(f"**Intent Detected:** {intent} domain. Bypassing size limits by pointing to the scoped semantic view.")

        with st.spinner("📊 2. Querying Governed Semantic Layer..."):
            # GOVERNED SQL: Query the exact view based intent
            if "INVENTORY" in intent:
                df = session.sql("SELECT * FROM PHARMA_DB.PHARMA_SUPPLY_CHAIN.INVENTORY_HEALTH_VIEW ORDER BY Days_Of_Inventory ASC LIMIT 5").to_pandas()
            else:
                df = session.sql("SELECT * FROM PHARMA_DB.PHARMA_SUPPLY_CHAIN.SUPPLIER_RELIABILITY_VIEW ORDER BY Supplier_Trust_Score ASC LIMIT 5").to_pandas()
            
            st.dataframe(df)

        with st.spinner("💡 3. Generating Insights..."):
            # INSIGHT GENERATION: Feed data back to Cortex for qualitative analysis via SQL
            data_string = df.to_string()
            insight_prompt = f"You are a pharma supply chain expert. Analyze this governed data and provide a 2-sentence risk summary and recommendation. Data: {data_string}"
            
            try:
                insight_query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large', $${insight_prompt}$$)"
                insight = session.sql(insight_query).collect()[0][0]
                st.success(f"**Cortex Analyst Insight:** {insight}")
            except Exception as e:
                st.error(f"Could not generate insight. Error: {e}")

st.divider()
st.subheader("⚡ Automated Action")
st.write("Trigger emergency stock rebalancing based on insights.")
col1, col2, col3 = st.columns(3)
source = col1.text_input("Source Warehouse (e.g., WH-101)")
dest = col2.text_input("Destination Warehouse (e.g., WH-102)")
drug = col3.text_input("Drug ID (e.g., DRG-001-PARACETAMOL)") 

if st.button("Execute Emergency Rebalance"):
    if source and dest and drug:
        try:
            session.sql(f"CALL PHARMA_DB.PHARMA_SUPPLY_CHAIN.REBALANCE_INVENTORY('{source}', '{dest}', '{drug}')").collect()
            st.success(f"✅ Successfully moved 500 units of {drug} from {source} to {dest}!")
        except Exception as e:
            st.error(f"Error executing procedure: {e}")
    else:
        st.warning("Please fill in all three fields.")
