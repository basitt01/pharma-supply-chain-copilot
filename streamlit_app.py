import streamlit as st
import pandas as pd

# Universal Connection Pattern
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

st.set_page_config(layout="wide", page_title="Pharma Copilot", page_icon="💊")

# ==========================================
# SIDEBAR: EXECUTIVE BRIEFING & CONTROLS
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/pills.png", width=60)
    st.title("Executive Control")
    st.markdown("**System Status:** 🟢 Optimal")
    st.markdown("**Cortex Models:** `llama3-8b`, `mistral-large`, `e5-base-v2`")
    st.divider()
    
    st.subheader("📋 Executive Briefing")
    st.markdown("Generate an instant operational snapshot for leadership review.")
    
    if st.button("Generate Executive Briefing CSV"):
        # Pull audit and inventory health for a quick briefing export
        briefing_df = session.sql("SELECT * FROM PHARMA_DB.PHARMA_SUPPLY_CHAIN.AI_AUDIT_LOG").to_pandas()
        csv = briefing_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Audit & Ops Report",
            data=csv,
            file_name="Pharma_Copilot_Executive_Report.csv",
            mime="text/csv",
        )

st.title("💊 Pharma Supply Chain: Hybrid Enterprise Copilot")
st.markdown("Dynamic Intent Routing • Governed Metrics • Vector Search RAG • Automated Action • Enterprise Governance")

# Create UI Tabs
tab1, tab2, tab3 = st.tabs([
    "📊 Analytical Intelligence (Structured)", 
    "📄 Contract Intelligence (RAG)", 
    "🔒 Enterprise Governance & Audit"
])

# ==========================================
# TAB 1: ANALYTICAL COPILOT WITH AUTO-LOGGING
# ==========================================
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "dataframe" in message:
                st.dataframe(message["dataframe"], use_container_width=True)
            if "chart_data" in message:
                if message["chart_type"] == "INVENTORY":
                    st.bar_chart(data=message["chart_data"], x="DRUG_ID", y="DAYS_OF_INVENTORY")
                else:
                    st.bar_chart(data=message["chart_data"], x="SUPPLIER_NAME", y="SUPPLIER_TRUST_SCORE")

    if user_query := st.chat_input("Ask a supply chain metrics question (e.g., 'Check inventory health'):"):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("🧠 1. Routing intent via Llama 3..."):
                route_prompt = f"Categorize this question into strictly one of two words: 'INVENTORY' or 'SUPPLIERS'. Return ONLY the word. Question: {user_query}"
                intent = session.sql(f"SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3-8b', $${route_prompt}$$)").collect()[0][0].strip().upper()
                st.info(f"**Domain Router:** Triggering `{intent}` Semantic View.")

            with st.spinner("📊 2. Querying Governed Semantic Layer & Building Visuals..."):
                if "INVENTORY" in intent:
                    df = session.sql("SELECT * FROM PHARMA_DB.PHARMA_SUPPLY_CHAIN.INVENTORY_HEALTH_VIEW ORDER BY Days_Of_Inventory ASC LIMIT 5").to_pandas()
                else:
                    df = session.sql("SELECT * FROM PHARMA_DB.PHARMA_SUPPLY_CHAIN.SUPPLIER_RELIABILITY_VIEW ORDER BY Supplier_Trust_Score ASC LIMIT 5").to_pandas()
                
                st.dataframe(df, use_container_width=True)
                chart_x = "DRUG_ID" if "INVENTORY" in intent else "SUPPLIER_NAME"
                chart_y = "DAYS_OF_INVENTORY" if "INVENTORY" in intent else "SUPPLIER_TRUST_SCORE"
                st.bar_chart(data=df, x=chart_x, y=chart_y)

            with st.spinner("💡 3. Generating Insight & Logging Event..."):
                data_string = df.to_string()
                insight_prompt = f"You are a pharma supply chain expert. Analyze this data. Provide 1) A 1-sentence risk summary. 2) A 1-sentence recommendation. 3) The estimated financial/operational impact if ignored. Data: {data_string}"
                try:
                    insight = session.sql(f"SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large', $${insight_prompt}$$)").collect()[0][0]
                    st.success(f"**Cortex Analyst Insight:**\n\n{insight}")
                    
                    # LOG INTERACTION TO SNOWFLAKE AUDIT TABLE
                    safe_query = user_query.replace("'", "''")
                    safe_insight = insight.replace("'", "''")
                    session.sql(f"INSERT INTO PHARMA_DB.PHARMA_SUPPLY_CHAIN.AI_AUDIT_LOG (USER_QUERY, DETECTED_INTENT, CORTEX_INSIGHT, ACTION_TAKEN) VALUES ('{safe_query}', '{intent}', '{safe_insight}', 'None')").collect()

                    st.session_state.messages.append({
                        "role": "assistant", "content": f"**Cortex Insight:**\n\n{insight}",
                        "dataframe": df, "chart_type": intent, "chart_data": df
                    })
                except Exception as e:
                    st.error(f"Error: {e}")

    st.divider()
    with st.expander("⚡ Workflow Automation: Emergency Rebalance", expanded=True):
        col1, col2, col3 = st.columns(3)
        source = col1.text_input("Source Warehouse (e.g., WH-102)")
        dest = col2.text_input("Destination Warehouse (e.g., WH-101)")
        drug = col3.text_input("Drug ID (e.g., DRG-001-PARACETAMOL)") 

        if st.button("Execute Stock Transfer"):
            if source and dest and drug:
                session.sql(f"CALL PHARMA_DB.PHARMA_SUPPLY_CHAIN.REBALANCE_INVENTORY('{source}', '{dest}', '{drug}')").collect()
                
                # LOG ACTION TO AUDIT TABLE
                action_text = f"Rebalanced 500 units of {drug} from {source} to {dest}"
                session.sql(f"INSERT INTO PHARMA_DB.PHARMA_SUPPLY_CHAIN.AI_AUDIT_LOG (USER_QUERY, DETECTED_INTENT, CORTEX_INSIGHT, ACTION_TAKEN) VALUES ('Manual Workflow Trigger', 'AUTOMATION', 'Stock Rebalanced', '{action_text}')").collect()
                
                st.success(f"✅ Successfully moved 500 units of {drug} from {source} to {dest}! Logged to Enterprise Audit Trail.")

# ==========================================
# TAB 2: UNSTRUCTURED CONTRACT RAG
# ==========================================
with tab2:
    st.subheader("📄 Chat with Supplier Contracts (Vector Search)")
    st.markdown("Uses Snowflake Cortex to embed text and calculate Cosine Similarity against contract SLAs.")
    
    rag_query = st.text_input("Ask a legal/compliance question (e.g., 'What is the late penalty for MediSource Inc?'):")
    
    if st.button("Search Contracts & Generate Answer"):
        if rag_query:
            with st.spinner("🔍 Embedding query and searching vector space..."):
                rag_sql = f"""
                SELECT SUPPLIER_NAME, CONTRACT_TEXT,
                       VECTOR_COSINE_SIMILARITY(
                           SNOWFLAKE.CORTEX.EMBED_TEXT_768('e5-base-v2', CONTRACT_TEXT),
                           SNOWFLAKE.CORTEX.EMBED_TEXT_768('e5-base-v2', $${rag_query}$$)
                       ) as sim_score
                FROM PHARMA_DB.PHARMA_SUPPLY_CHAIN.SUPPLIER_CONTRACTS
                ORDER BY sim_score DESC LIMIT 1;
                """
                rag_result = session.sql(rag_sql).collect()
                top_supplier = rag_result[0][0]
                top_context = rag_result[0][1]
                
                st.info(f"**Retrieved Highest-Matching Context (Supplier: {top_supplier}):**\n\n> *{top_context}*")

            with st.spinner("🤖 Synthesizing Answer..."):
                prompt = f"Based strictly on this contract context: '{top_context}', answer the user's question: '{rag_query}'. If the answer is not in the text, state that."
                answer = session.sql(f"SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large', $${prompt}$$)").collect()[0][0]
                st.success(f"**AI Legal Analyst Answer:** {answer}")

# ==========================================
# TAB 3: ENTERPRISE GOVERNANCE & AUDIT LOG
# ==========================================
with tab3:
    st.subheader("🔒 Enterprise AI Audit & Observability Log")
    st.markdown("Every prompt, intent routing decision, LLM insight, and workflow action is transparently recorded within Snowflake's governance perimeter.")
    
    audit_df = session.sql("SELECT * FROM PHARMA_DB.PHARMA_SUPPLY_CHAIN.AI_AUDIT_LOG ORDER BY TIMESTAMP DESC").to_pandas()
    st.dataframe(audit_df, use_container_width=True)
