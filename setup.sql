-- ==========================================
-- 1. DATABASE & SCHEMA SETUP
-- ==========================================
CREATE DATABASE IF NOT EXISTS PHARMA_DB;
CREATE SCHEMA IF NOT EXISTS PHARMA_DB.PHARMA_SUPPLY_CHAIN;

USE DATABASE PHARMA_DB;
USE SCHEMA PHARMA_SUPPLY_CHAIN;

-- ==========================================
-- 2. CORE TABLES DDL (RAW DATA LAYER)
-- ==========================================
CREATE OR REPLACE TABLE INVENTORY_STATUS (
    Warehouse_ID STRING,
    Drug_ID STRING,
    Qty_On_Hand INT,
    Daily_Demand INT
);

CREATE OR REPLACE TABLE SUPPLIER_METRICS (
    Supplier_Name STRING,
    Drug_ID STRING,
    On_Time_Delivery_Rate FLOAT,
    Defect_Rate FLOAT
);

-- ==========================================
-- 3. MOCK DATA INJECTION (INVENTORY & SUPPLIERS)
-- ==========================================
INSERT INTO INVENTORY_STATUS (Warehouse_ID, Drug_ID, Qty_On_Hand, Daily_Demand) VALUES
('WH-101', 'DRG-001-PARACETAMOL', 450, 150),
('WH-102', 'DRG-001-PARACETAMOL', 3200, 200),
('WH-101', 'DRG-002-AMOXICILLIN', 1500, 300),
('WH-103', 'DRG-002-AMOXICILLIN', 200, 250),
('WH-104', 'DRG-003-IBUPROFEN', 5000, 400),
('WH-105', 'DRG-004-METFORMIN', 800, 100);

INSERT INTO SUPPLIER_METRICS (Supplier_Name, Drug_ID, On_Time_Delivery_Rate, Defect_Rate) VALUES
('PharmaCure Ltd', 'DRG-001-PARACETAMOL', 0.98, 0.010),
('MediSource Inc', 'DRG-001-PARACETAMOL', 0.85, 0.030),
('GenericHealth Co', 'DRG-002-AMOXICILLIN', 0.95, 0.005),
('BioGen Pharma', 'DRG-003-IBUPROFEN', 0.99, 0.003),
('Apex Generics', 'DRG-004-METFORMIN', 0.89, 0.025);

-- ==========================================
-- 4. GOVERNED SEMANTIC VIEWS (LOGIC LAYER)
-- ==========================================
CREATE OR REPLACE VIEW INVENTORY_HEALTH_VIEW AS 
SELECT 
    Warehouse_ID, 
    Drug_ID, 
    Qty_On_Hand, 
    Daily_Demand, 
    (Qty_On_Hand / NULLIF(Daily_Demand, 0)) AS Days_Of_Inventory 
FROM INVENTORY_STATUS;

CREATE OR REPLACE VIEW SUPPLIER_RELIABILITY_VIEW AS 
SELECT 
    Supplier_Name, 
    Drug_ID, 
    On_Time_Delivery_Rate, 
    Defect_Rate, 
    (On_Time_Delivery_Rate - Defect_Rate) AS Supplier_Trust_Score 
FROM SUPPLIER_METRICS;

-- ==========================================
-- 5. CONTRACTS TABLE DDL & DATA (FOR RAG)
-- ==========================================
CREATE OR REPLACE TABLE SUPPLIER_CONTRACTS (
    CONTRACT_ID VARCHAR,
    SUPPLIER_NAME VARCHAR,
    CONTRACT_TEXT VARCHAR
);

INSERT INTO SUPPLIER_CONTRACTS (CONTRACT_ID, SUPPLIER_NAME, CONTRACT_TEXT) VALUES
('CTR-001', 'PharmaCure Ltd', 'Standard Service Level Agreement. On-time delivery must be > 95%. Penalty for late delivery is 5% of total invoice value. Quality defect penalty is $10,000 per incident.'),
('CTR-002', 'MediSource Inc', 'Premium Supplier Contract. Late deliveries beyond 3 days incur a strict 15% penalty fee. If the defect rate exceeds 0.02 for two consecutive months, the contract is subject to immediate termination review without severance.'),
('CTR-003', 'BioGen Pharma', 'Flex Agreement. No penalty for 1-day delays. Late delivery > 2 days incurs a $5,000 flat fee. Defect rate SLA is 0.005.'),
('CTR-004', 'GenericHealth Co', 'Standard Contract. Late delivery penalty is 2% per day late. All quality issues require a 24-hour RCA (Root Cause Analysis).');

-- ==========================================
-- 6. ENTERPRISE AUDIT LOG (GOVERNANCE LAYER)
-- ==========================================
CREATE OR REPLACE TABLE AI_AUDIT_LOG (
    LOG_ID INT AUTOINCREMENT,
    TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    USER_QUERY STRING,
    DETECTED_INTENT STRING,
    CORTEX_INSIGHT STRING,
    ACTION_TAKEN STRING
);

-- ==========================================
-- 7. WORKFLOW AUTOMATION (ACTION LAYER)
-- ==========================================
CREATE OR REPLACE PROCEDURE REBALANCE_INVENTORY(SOURCE_WH VARCHAR, DEST_WH VARCHAR, DRUG VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
    UPDATE INVENTORY_STATUS 
    SET Qty_On_Hand = Qty_On_Hand - 500 
    WHERE Warehouse_ID = :SOURCE_WH AND Drug_ID = :DRUG;
    
    UPDATE INVENTORY_STATUS 
    SET Qty_On_Hand = Qty_On_Hand + 500 
    WHERE Warehouse_ID = :DEST_WH AND Drug_ID = :DRUG;
    
    RETURN 'Rebalance Successful';
END;
$$;
