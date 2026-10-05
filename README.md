# 💊 Pharma Supply Chain: Hybrid AI Copilot

**Built for the Snowflake CoCo CLI Hackathon**

[![Snowflake](https://img.shields.io/badge/Powered_by-Snowflake-29B5E8.svg?style=for-the-badge&logo=snowflake&logoColor=white)](#)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](#)

## 🎥 Demo & Links
* **Demo Video:** [Insert your YouTube/Google Drive link here]
* **Live App (SiS URL):** [Insert your Snowflake App URL here] *(Note: Requires Snowflake account access. Please see the demo video for full interaction).*

---

## 🛑 The Problem: The Hallucination & Scaling Gap
At the enterprise level, supply chain data is scattered across ERP, logistics, and CRM systems. This creates two massive roadblocks for standard AI deployments:
1. **Mathematical Hallucinations:** If you ask an LLM to calculate "On-Time Delivery," it will guess the SQL logic, leading to untrustworthy, varying answers across departments.
2. **The Size Ceiling:** Trying to govern an *entire* global supply chain in a single Semantic Model (to prevent hallucinations) exceeds standard context/size limits. 
3. **The Insight Gap:** Standard Text-to-SQL AI can return the hard numbers, but business users need qualitative insights and the ability to take immediate action.

## 💡 The Solution: Dynamic Intent Routing & Governed Semantic Views
This project introduces a **Hybrid Copilot Architecture**. Instead of forcing the entire supply chain into one massive semantic model, this app uses Cortex LLMs to dynamically route the user's natural language question to highly scoped, mathematically hardcoded **Semantic Views**. 

Once the mathematically accurate data is retrieved, it is passed back into a secondary LLM for qualitative reasoning, and finally, presented alongside an automated action trigger.

### 🏆 Meeting the Judging Criteria

* **Real World Relevance (30%):** Models a critical Pharma use-case (preventing drug stockouts) similar to real-world challenges faced by enterprises like Cipla. Bridges the gap between raw data and actionable supply chain insights.
* **Technical Execution (40%):** Leverages multiple Snowflake primitives natively. Bypasses model size ceilings via programmatic prompt routing and ensures 100% accurate metric calculation by restricting the AI to query only the Semantic Views.
* **Solution Completeness (30%):** An end-to-end Intelligent Workflow Agent. It doesn't just answer questions—it analyzes the data and provides a 1-click execution button to rebalance inventory using Snowflake Stored Procedures.

---

## 🛠️ Snowflake Technologies Used

This project was built securely within Snowflake's perimeter using the following features:

* **Snowflake CoCo CLI:** Used as the primary AI coding agent to rapidly bootstrap the database schema, write the DDLs, and inject realistic mock data using natural language terminal prompts.
* **Snowflake Cortex (Complete):** 
  * Used `llama3-8b` for **Zero-Shot Intent Routing** (determining if a query relates to 'Inventory' or 'Suppliers').
  * Used `mistral-large` for **Data-to-Text Analysis** (translating governed dataframes into human-readable risk summaries).
* **Governed Semantic Views:** Hardcoded the mathematical formulas for `Days_Of_Inventory` and `Supplier_Trust_Score` directly in Snowflake views, acting as the absolute "Single Source of Truth."
* **Streamlit in Snowflake (SiS):** Provided the natural language chat interface and frontend routing logic, deployed seamlessly via "Run on Warehouse."
* **Snowflake Stored Procedures:** Handled the database mutation logic (transferring stock between warehouses) via an automated action button.

---

## 🏗️ Architecture Flow

1. **User Input:** Supply Chain Manager asks a natural language question (e.g., *"Which warehouses are running low on Paracetamol?"*).
2. **Intent Routing:** Streamlit calls Cortex `llama3-8b` to categorize the prompt into a specific domain (Inventory vs. Supplier).
3. **Governed SQL:** Streamlit routes the query to the strictly scoped **Semantic View**, bypassing size limitations and returning 100% mathematically accurate data.
4. **Insight Generation:** The returned DataFrame is converted to text and sent to Cortex `mistral-large` to generate a qualitative risk assessment.
5. **Workflow Automation:** The user clicks "Execute Emergency Rebalance", triggering a Snowflake Stored Procedure that instantly moves stock from a surplus warehouse to the deficit warehouse.

---

## 🚀 Repository Structure

* `streamlit_app.py` - The core Streamlit application containing the Python logic, Cortex LLM routing, and UI.
* `setup.sql` - The foundational DDL generated via CoCo CLI, including the mock data injection, Semantic Views, and the Action-oriented Stored Procedure.

## 💻 How to Replicate
1. Run the commands in `setup.sql` within your Snowflake environment to establish the data foundation.
2. Create a new Streamlit App in Snowflake (SiS) and set the execution environment to **Run on Warehouse**.
3. Paste the contents of `streamlit_app.py` into the editor and hit Run.
