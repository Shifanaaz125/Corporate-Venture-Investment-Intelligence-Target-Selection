CREATE DATABASE investment_intelligence;
#Step 1 - Create the project database

USE investment_intelligence;
SELECT DATABASE();
SELECT DATABASE() AS active_database;
SHOW TABLES;
#Step 2 — Create the screening table
CREATE TABLE investment_screening (
    company VARCHAR(50),

    revenue_growth_pct DECIMAL(12,2),
    revenue_growth_2023_to_2025_pct DECIMAL(12,2),
    growth_trajectory VARCHAR(50),

    operating_margin_pct DECIMAL(12,2),
    operating_margin_change_pct_points DECIMAL(12,2),

    net_margin_pct DECIMAL(12,2),
    net_margin_change_pct_points DECIMAL(12,2),

    cfo_margin_pct DECIMAL(12,2),
    cfo_margin_change_pct_points DECIMAL(12,2),

    operating_income_usd_000 DECIMAL(15,2),
    operating_income_change_usd_mn DECIMAL(15,2),

    earnings_cashflow_flag VARCHAR(50),
    growth_flag VARCHAR(50),
    operating_margin_flag VARCHAR(50),
    net_margin_flag VARCHAR(50),
    cash_generation_flag VARCHAR(50),
    operating_income_flag VARCHAR(50),

    positive_direction_count INTEGER,
    negative_direction_count INTEGER
);

#Step 3 — Inspect the SQL table structure
DESCRIBE investment_screening;

USE investment_intelligence;

SHOW TABLES;
DESCRIBE investment_screening;
SELECT COUNT(*) AS total_companies
FROM investment_screening;

#Verify the actual records
SELECT *
FROM investment_screening;

#SQL analysis
SELECT
    company,
    positive_direction_count,
    negative_direction_count
FROM investment_screening
ORDER BY positive_direction_count DESC;

#Identify the strongest candidates
SELECT
    company,
    positive_direction_count,
    negative_direction_count
FROM investment_screening
WHERE positive_direction_count >= 4
ORDER BY positive_direction_count DESC;

SELECT
    company,
    revenue_growth_2023_to_2025_pct,
    operating_margin_pct,
    net_margin_pct,
    cfo_margin_pct,
    operating_income_change_usd_mn
FROM investment_screening
WHERE positive_direction_count >= 4
ORDER BY revenue_growth_2023_to_2025_pct DESC;

#compare all 5 companies
SELECT
    company,
    revenue_growth_2023_to_2025_pct,
    operating_margin_pct,
    net_margin_pct,
    cfo_margin_pct,
    operating_income_change_usd_mn,
    positive_direction_count,
    negative_direction_count
FROM investment_screening
ORDER BY
    positive_direction_count DESC,
    revenue_growth_2023_to_2025_pct DESC;
    
    #Risk/weakness analysis
    SELECT
    company,
    operating_margin_flag,
    net_margin_flag,
    cash_generation_flag,
    operating_income_flag
FROM investment_screening
ORDER BY
    negative_direction_count DESC,
    company;
    
    #Find the biggest financial improvement
    SELECT
    company,
    operating_income_usd_000,
    operating_income_change_usd_mn,
    operating_income_flag
FROM investment_screening
ORDER BY operating_income_change_usd_mn DESC;

#Growth vs profitability
SELECT
    company,
    revenue_growth_2023_to_2025_pct,
    operating_margin_pct,
    net_margin_pct
FROM investment_screening
ORDER BY
    revenue_growth_2023_to_2025_pct DESC;
    
    #Cash-flow quality
    SELECT
    company,
    net_margin_pct,
    cfo_margin_pct,
    cfo_margin_change_pct_points,
    cash_generation_flag
FROM investment_screening
ORDER BY
    cfo_margin_pct DESC;
    
    #Earnings vs cash-flow consistency
    SELECT
    company,
    earnings_cashflow_flag,
    net_margin_pct,
    cfo_margin_pct
FROM investment_screening
ORDER BY
    company;
    
    #Build the final screening score
    SELECT
    company,
    positive_direction_count,
    negative_direction_count,
    (positive_direction_count - negative_direction_count) AS net_direction_score,
    revenue_growth_2023_to_2025_pct,
    operating_margin_pct,
    net_margin_pct,
    cfo_margin_pct
FROM investment_screening
ORDER BY
    net_direction_score DESC,
    revenue_growth_2023_to_2025_pct DESC;
    
    #Identify the strongest overall financial profile
    SELECT
    company,
    revenue_growth_2023_to_2025_pct,
    operating_margin_pct,
    net_margin_pct,
    cfo_margin_pct,
    operating_income_change_usd_mn,
    net_direction_score
FROM (
    SELECT
        company,
        revenue_growth_2023_to_2025_pct,
        operating_margin_pct,
        net_margin_pct,
        cfo_margin_pct,
        operating_income_change_usd_mn,
        (positive_direction_count - negative_direction_count) AS net_direction_score
    FROM investment_screening
) AS screening
WHERE net_direction_score = 5
ORDER BY
    revenue_growth_2023_to_2025_pct DESC;
    
    #identify the strongest and weakest metric for each company
    SELECT
    company,
    revenue_growth_2023_to_2025_pct,
    operating_margin_pct,
    net_margin_pct,
    cfo_margin_pct,
    operating_income_change_usd_mn,
    positive_direction_count,
    negative_direction_count
FROM investment_screening
ORDER BY
    company;
    
    #Create the final investment-screening classification
    SELECT
    company,
    positive_direction_count,
    negative_direction_count,
    (positive_direction_count - negative_direction_count) AS net_direction_score,
    CASE
        WHEN (positive_direction_count - negative_direction_count) >= 5
            THEN 'Strong Candidate'
        WHEN (positive_direction_count - negative_direction_count) >= 0
            THEN 'Watchlist'
        ELSE 'Weak Candidate'
    END AS investment_screening_class
FROM investment_screening
ORDER BY
    net_direction_score DESC,
    company;
    
    #Final investment screening summary
    SELECT
    company,
    CASE
        WHEN (positive_direction_count - negative_direction_count) >= 5
            THEN 'Strong Candidate'
        WHEN (positive_direction_count - negative_direction_count) >= 0
            THEN 'Watchlist'
        ELSE 'Weak Candidate'
    END AS investment_screening_class,
    revenue_growth_2023_to_2025_pct,
    operating_margin_pct,
    net_margin_pct,
    cfo_margin_pct,
    operating_income_change_usd_mn,
    positive_direction_count,
    negative_direction_count,
    earnings_cashflow_flag
FROM investment_screening
ORDER BY
    positive_direction_count DESC,
    revenue_growth_2023_to_2025_pct DESC;