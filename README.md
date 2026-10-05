# 💊 Pharma Supply Chain: Hybrid Enterprise AI Copilot

**An Autonomous, Governed, and Action-Oriented AI Solution Built for the Snowflake CoCo CLI Hackathon**

[![Powered by Snowflake](https://img.shields.io/badge/Powered_by-Snowflake-29B5E8.svg?style=for-the-badge&logo=snowflake&logoColor=white)](#)
[![Streamlit UI](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](#)
[![Cortex AI](https://img.shields.io/badge/AI_Engine-Snowflake_Cortex-29B5E8.svg?style=for-the-badge&logo=snowflake&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](#)

---

## 🎥 Demo & Live Access
* **🎥 Watch 2-Minute Video Demo:** [Insert YouTube / Google Drive Link Here]
* **🌐 Explore Live Streamlit App:** [Insert Streamlit Community Cloud URL Here]

---

## 🛑 The Enterprise Problem: Fragmentation, Hallucinations, & Scale
Global pharmaceutical supply chains are plagued by data silos spanning ERP systems, inventory logs, logistics feeds, and unstructured legal contracts. When enterprises attempt to deploy standard LLM assistants, they hit three critical roadblocks:
1. **Mathematical Hallucinations:** Asking general LLMs to compute critical KPIs (like *Days of Inventory* or *Supplier Trust Scores*) on raw database tables results in guessed formulas and inconsistent reporting across departments.
2. **The Context Size Ceiling:** Forcing an entire global supply chain database and thousands of complex vendor contracts into a single monolithic model exceeds size limits, increases latency, and causes context drift.
3. **The Governance & Action Gap:** Executives require more than static data tables; they need secure qualitative reasoning, tamper-proof audit trails, and the ability to trigger automated operational actions directly from the chat interface.

---

## 💡 The Solution: Hybrid Intent Routing & Unified Intelligence
This project introduces a production-ready **Hybrid Enterprise Copilot Architecture**. Instead of relying on a single generic model, our application combines **Dynamic Intent Routing** via Snowflake Cortex `llama3-8b` to route natural language prompts to either mathematically hardcoded **Governed Semantic Views** or **Native Vector Search RAG Pipelines**. 

Once insights and operational risks are identified by `mistral-large`, users can execute automated stock rebalancing via Snowflake Stored Procedures while logging every interaction to an immutable Enterprise Audit Trail.

---

## 🏆 How We Meet the Judging Criteria

* **Real-World Relevance (30%):** Directly solves high-stakes pharmaceutical stockout prevention and supplier compliance challenges faced by global leaders like Cipla and McKesson, bridging raw data with executive decision-making.
* **Technical Execution (40%):** Natively leverages Snowflake Cortex AI functions (`llama3-8b`, `mistral-large`, `e5-base-v2`), governed SQL semantic views, native SQL vector cosine similarity, and serverless stored procedures without requiring external vector databases or complex microservice layers.
* **Solution Completeness (30%):** Delivers a fully deployed, end-to-end application featuring conversational chat memory, dynamic auto-generated bar charts, legal document RAG, automated workflow triggers, and downloadable executive reporting packs.

---

## 🏗️ Technical Architecture & Stack

```text
[ User Prompt ] 
       │
       ▼
 [ Streamlit UI (SiS / Cloud) ] 
       │
       ├─► 1. Intent Routing (Cortex: llama3-8b)
       │         │
       │         ├─► [Inventory Domain] ──► Governed Semantic View (INVENTORY_HEALTH_VIEW)
       │         └─► [Supplier Domain]  ──► Governed Semantic View (SUPPLIER_RELIABILITY_VIEW)
       │
       ├─► 2. Contract RAG (Cortex: EMBED_TEXT_768 & VECTOR_COSINE_SIMILARITY)
       │         └─► Unstructured Legal Contracts (SUPPLIER_CONTRACTS)
       │
       ├─► 3. Risk & Financial Impact Analysis (Cortex: mistral-large)
       │
       ├─► 4. Workflow Automation (Snowflake Stored Procedure: REBALANCE_INVENTORY)
       │
       └─► 5. Compliance & Observability (Immutable Audit Table: AI_AUDIT_LOG)
Core Technologies Used:
Snowflake CoCo CLI: Used to rapidly bootstrap database DDLs, schemas, and mock operational data sets via natural language terminal commands.

Snowflake Cortex AI:

llama3-8b for zero-shot domain intent classification.

mistral-large for deep data-to-text risk summarization and financial impact estimation.

e5-base-v2 for generating 768-dimensional text embeddings for vector search.

Governed Semantic Layer: Hardcoded mathematical formulas (Days_Of_Inventory and Supplier_Trust_Score) directly in Snowflake SQL views to eliminate LLM calculation errors.

Native Vector Search: Computes VECTOR_COSINE_SIMILARITY directly in SQL to query supplier legal agreements and extract penalty clauses.

Enterprise Audit Logging: Records every prompt, intent, AI insight, and workflow action to a tamper-proof AI_AUDIT_LOG table for complete regulatory compliance.

🚀 Key Features & Capabilities
Conversational Chat Interface: Persistent session memory styled like a modern enterprise copilot.

Dynamic Visualizations: Automatically detects domain intent and plots interactive bar charts (st.bar_chart) alongside raw governed dataframes.

Unstructured Legal RAG: Seamlessly queries vendor service level agreements (SLAs) using native vector search to find penalty clauses.

1-Click Workflow Automation: Instantly triggers Snowflake stored procedures to rebalance stock between surplus and deficit warehouses.

Executive Briefing & Audit Exports: Provides a dedicated governance tab and sidebar reporting tools to download CSV executive audit packs on demand.

💻 Setup & Replication Instructions
Database Provisioning:
Run the full setup.sql script in a Snowflake SQL worksheet to initialize PHARMA_DB, raw tables, semantic views, vector contract embeddings, audit logs, and stored procedures.

Environment Configuration:
Configure your Streamlit app secrets or environment variables with your Snowflake credentials (account, user, password, role, warehouse, database, schema).

App Deployment:
Deploy streamlit_app.py via Streamlit Community Cloud or natively inside Snowflake via Streamlit in Snowflake (SiS).

📜 Repository Structure
streamlit_app.py - Core Python script powering the multi-tab Streamlit user interface, intent router, RAG search, and audit logger.

setup.sql - Complete backend DDL script for database setup, views, stored procedures, and tables.

requirements.txt - Python dependencies (snowflake-snowpark-python, pandas) for seamless cloud execution.
