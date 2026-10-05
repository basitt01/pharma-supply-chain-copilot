import streamlit as st

# Universal Connection Pattern
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

st.set_page_config(layout="wide", page_title="Pharma Copilot", page_icon="💊")

st.title("💊 Pharma Supply Chain: AI Copilot")
st.markdown("Dynamic Intent Routing • Governed Metrics • Financial Impact • Automated Action")

# 1. Initialize chat history for the ChatGPT-style UI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages and charts
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "dataframe" in message:
            st.dataframe(message["dataframe"], use_container_width=True)
        if "chart_data" in message:
            # Render the correct chart type from history
            if message["chart_type"] == "INVENTORY":
                st.bar_chart(data=message["chart_data"], x="DRUG_ID", y="DAYS_OF_INVENTORY")
            else:
                st.bar_chart(data=message["chart_data"], x="SUPPLIER_NAME", y="SUPPLIER_TRUST_SCORE")

# 2. Chat Input Box (Appears at bottom of screen)
if user_query := st.chat_input("Ask a supply chain question (e.g., 'Check inventory health'):"):
    
    # Add user question to screen
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("🧠 1. Routing intent via Llama 3..."):
            route_prompt = f"Categorize this question into strictly one of two words: 'INVENTORY' or 'SUPPLIERS'. Return ONLY the word. Question: {user_query}"
            intent_query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3-8b', $${route_prompt}$$)"
            intent = session.sql(intent_query).collect()[0][0].strip().upper()
            st.info(f"**Domain Router:** Triggering `{intent}` Semantic View.")

        with st.spinner("📊 2. Querying Governed Semantic Layer & Building Visuals..."):
            if "INVENTORY" in intent:
                df = session.sql("SELECT * FROM PHARMA_DB.PHARMA_SUPPLY_CHAIN.INVENTORY_HEALTH_VIEW ORDER BY Days_Of_Inventory ASC LIMIT 5").to_pandas()
                st.dataframe(df, use_container_width=True)
                # Dynamic Bar Chart for Inventory
                st.bar_chart(data=df, x="DRUG_ID", y="DAYS_OF_INVENTORY")
            else:
                df = session.sql("SELECT * FROM PHARMA_DB.PHARMA_SUPPLY_CHAIN.SUPPLIER_RELIABILITY_VIEW ORDER BY Supplier_Trust_Score ASC LIMIT 5").to_pandas()
                st.dataframe(df, use_container_width=True)
                # Dynamic Bar Chart for Suppliers
                st.bar_chart(data=df, x="SUPPLIER_NAME", y="SUPPLIER_TRUST_SCORE")

        with st.spinner("💡 3. Generating Insight & Cost Impact..."):
            data_string = df.to_string()
            
            # The Upgraded Mistral Prompt (Now asks for Financial/Business Impact)
            insight_prompt = f"You are a pharma supply chain expert. Analyze this exact data. Provide 1) A 1-sentence risk summary. 2) A 1-sentence recommendation. 3) The estimated financial or operational impact if we ignore this. Data: {data_string}"
            
            try:
                insight_query = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large', $${insight_prompt}$$)"
                insight = session.sql(insight_query).collect()[0][0]
                st.success(f"**Cortex Analyst Insight:**\n\n{insight}")
                
                # Save assistant response to memory so it stays on screen
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"**Cortex Insight:**\n\n{insight}",
                    "dataframe": df,
                    "chart_type": intent,
                    "chart_data": df
                })
            except Exception as e:
                st.error(f"Could not generate insight. Error: {e}")

# 3. Action Form (Pinned below the chat)
st.divider()
with st.expander("⚡ Workflow Automation: Emergency Rebalance", expanded=True):
    col1, col2, col3 = st.columns(3)
    source = col1.text_input("Source Warehouse (e.g., WH-102)")
    dest = col2.text_input("Destination Warehouse (e.g., WH-101)")
    drug = col3.text_input("Drug ID (e.g., DRG-001-PARACETAMOL)") 

    if st.button("Execute Stock Transfer"):
        if source and dest and drug:
            try:
                session.sql(f"CALL PHARMA_DB.PHARMA_SUPPLY_CHAIN.REBALANCE_INVENTORY('{source}', '{dest}', '{drug}')").collect()
                st.success(f"✅ Successfully moved 500 units of {drug} from {source} to {dest}! ERB/CRM updated.")
            except Exception as e:
                st.error(f"Error executing procedure: {e}")
        else:
            st.warning("Please fill in all three fields.")
