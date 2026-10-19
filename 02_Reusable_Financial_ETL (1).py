#!/usr/bin/env python
# coding: utf-8

# 

# In[1]:


import pandas as pd 


# In[2]:


companies = {
    "Etsy": "ETSY",
    "Shake Shack": "SHAK",
    "Crocs": "CROX",
    "Boot Barn": "BOOT",
    "Duolingo": "DUOL"
}

companies


# In[3]:


import requests

sec_tickers_url = "https://www.sec.gov/files/company_tickers.json"

headers = {
    "User-Agent": "Yasmeen Data Project contact@example.com"
}

response = requests.get(
    sec_tickers_url,
    headers=headers
)

response.status_code


# In[4]:


data = response.json()

type(data)


# In[5]:


data.keys()


# In[6]:


data["0"]


# In[7]:


ticker_df = pd.DataFrame(data).T

ticker_df.head()


# In[8]:


target_tickers = list(companies.values())

target_tickers


# In[9]:


target_companies = ticker_df[
    ticker_df["ticker"].isin(target_tickers)
]

target_companies


# In[10]:


company_mapping = target_companies[
    ["title", "ticker", "cik_str"]
].reset_index(drop=True)

company_mapping


# In[11]:


cik = company_mapping.loc[
    company_mapping["ticker"] == "ETSY", "cik_str"
].iloc[0]

cik


# In[12]:


sec_companyfacts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{int(cik):010d}.json"

sec_companyfacts_url


# In[13]:


headers = {
    "User-Agent": "Yasmeen Data Project contact@example.com"
}

response = requests.get(
    sec_companyfacts_url,
    headers=headers
)

response.status_code


# In[14]:


company_facts = response.json()

company_facts.keys()


# In[15]:


company_facts["facts"].keys()


# In[16]:


us_gaap = company_facts["facts"]["us-gaap"]

revenue_candidates = [
    key for key in us_gaap.keys()
    if "Revenue" in key or "Revenues" in key
]

revenue_candidates


# In[17]:


for concept in [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "Revenues"
]:
    print(concept)
    print(us_gaap[concept]["description"])
    print()


# In[18]:


us_gaap["RevenueFromContractWithCustomerExcludingAssessedTax"]["units"].keys()


# In[19]:


revenue_concept = us_gaap[
    "RevenueFromContractWithCustomerExcludingAssessedTax"
]

revenue_concept["units"]["USD"][:5]


# In[20]:


len(revenue_concept["units"]["USD"])


# In[21]:


revenue_annual = [
    x for x in revenue_concept["units"]["USD"]
    if x.get("fp") == "FY" and x.get("form") == "10-K"
]

len(revenue_annual)


# In[22]:


revenue_annual


# In[23]:


revenue_target = [
    x for x in revenue_annual
    if x.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]

len(revenue_target)


# In[24]:


revenue_latest = {}

for x in revenue_target:
    year = int(x["start"][:4])
    
    if year not in revenue_latest or x["filed"] > revenue_latest[year]["filed"]:
        revenue_latest[year] = x

revenue_latest


# In[25]:


revenue_final = [
    {
        "year": year,
        "revenue_usd_000": data["val"] / 1000
    }
    for year, data in revenue_latest.items()
]

revenue_final


# In[26]:


len(revenue_final), [x["year"] for x in revenue_final]


# # Reusable ETL

# In[27]:


cik = company_mapping.loc[
    company_mapping["ticker"] == "ETSY", "cik_str"
].iloc[0]

cik


# In[28]:


sec_companyfacts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{int(cik):010d}.json"

sec_companyfacts_url


# In[29]:


response = requests.get(
    sec_companyfacts_url,
    headers=headers
)

response.status_code


# In[30]:


company_facts = response.json()

company_facts.keys()


# In[31]:


us_gaap = company_facts["facts"]["us-gaap"]

type(us_gaap)


# In[32]:


revenue_candidates = [
    key for key in us_gaap.keys()
    if "Revenue" in key or "Revenues" in key
]

revenue_candidates


# In[33]:


for concept in [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "Revenues"
]:
    print(concept)
    print(us_gaap[concept]["description"])
    print()


# In[34]:


revenue_concept = us_gaap[
    "RevenueFromContractWithCustomerExcludingAssessedTax"
]

revenue_concept.keys()


# In[35]:


revenue_concept["units"].keys()


# In[36]:


revenue_concept["units"]["USD"][:5]


# In[37]:


revenue_annual = [
    x for x in revenue_concept["units"]["USD"]
    if x.get("fp") == "FY" and x.get("form") == "10-K"
]

len(revenue_annual)


# In[38]:


revenue_target = [
    x for x in revenue_annual
    if x.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]

len(revenue_target)


# In[39]:


revenue_target


# In[40]:


revenue_latest = {}

for x in revenue_target:
    year = int(x["start"][:4])
    
    if year not in revenue_latest or x["filed"] > revenue_latest[year]["filed"]:
        revenue_latest[year] = x


# In[41]:


revenue_latest


# # unit standardization

# In[42]:


revenue_final = [
    {
        "year": year,
        "revenue_usd_000": data["val"] / 1000
    }
    for year, data in revenue_latest.items()
]

revenue_final


# In[43]:


len(revenue_final), [x["year"] for x in revenue_final]


# # Next metric: Gross Profit

# In[44]:


gross_profit_candidates = [
    key for key in us_gaap.keys()
    if "GrossProfit" in key or "Gross" in key
]

gross_profit_candidates


# In[45]:


us_gaap["GrossProfit"]["description"]


# In[46]:


gross_profit_concept = us_gaap["GrossProfit"]

gross_profit_concept.keys()


# In[47]:


gross_profit_concept["units"].keys()


# In[48]:


gross_profit_concept["units"]["USD"][:5]


# In[49]:


gross_profit_annual = [
    x for x in gross_profit_concept["units"]["USD"]
    if x.get("fp") == "FY" and x.get("form") == "10-K"
]

len(gross_profit_annual)


# In[50]:


gross_profit_target = [
    x for x in gross_profit_annual
    if x.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]

len(gross_profit_target)


# In[51]:


gross_profit_target


# In[52]:


gross_profit_latest = {}

for x in gross_profit_target:
    year = int(x["start"][:4])
    
    if year not in gross_profit_latest or x["filed"] > gross_profit_latest[year]["filed"]:
        gross_profit_latest[year] = x

gross_profit_latest


# In[53]:



gross_profit_final = [
    {
        "year": year,
        "gross_profit_usd_000": data["val"] / 1000
    }
    for year, data in gross_profit_latest.items()
]

gross_profit_final


# In[54]:


len(gross_profit_final), [x["year"] for x in gross_profit_final]


# In[55]:


operating_income_candidates = [
    key for key in us_gaap.keys()
    if "OperatingIncome" in key
]

operating_income_candidates


# In[56]:


us_gaap["OperatingIncomeLoss"]["description"]


# In[57]:


operating_income_concept = us_gaap["OperatingIncomeLoss"]

operating_income_concept.keys()


# In[58]:


operating_income_concept["units"].keys()


# In[59]:


operating_income_concept["units"]["USD"][:5]


# In[60]:


operating_income_annual = [
    x for x in operating_income_concept["units"]["USD"]
    if x.get("fp") == "FY" and x.get("form") == "10-K"
]

len(operating_income_annual)


# In[61]:


operating_income_target = [
    x for x in operating_income_annual
    if x.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]

len(operating_income_target)


# In[62]:


operating_income_target


# In[63]:


operating_income_latest = {}

for x in operating_income_target:
    year = int(x["start"][:4])
    
    if year not in operating_income_latest or x["filed"] > operating_income_latest[year]["filed"]:
        operating_income_latest[year] = x

operating_income_latest


# In[64]:


operating_income_final = [
    {
        "year": year,
        "operating_income_usd_000": data["val"] / 1000
    }
    for year, data in operating_income_latest.items()
]

operating_income_final


# In[65]:


len(operating_income_final), [x["year"] for x in operating_income_final]


# In[66]:



net_income_candidates = [
    key for key in us_gaap.keys()
    if "NetIncome" in key
]

net_income_candidates


# In[67]:


us_gaap["NetIncomeLoss"]["description"]


# In[68]:


net_income_concept = us_gaap["NetIncomeLoss"]


# In[69]:


net_income_concept.keys()


# In[70]:


net_income_concept["units"].keys()


# In[71]:


net_income_concept["units"]["USD"][:5]


# In[72]:


net_income_annual = [
    x for x in net_income_concept["units"]["USD"]
    if x.get("fp") == "FY" and x.get("form") == "10-K"
]


# In[73]:




len(net_income_annual)


# In[74]:


net_income_target = [
    x for x in net_income_annual
    if x.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]


# In[75]:


len(net_income_target)


# In[76]:


net_income_target


# In[77]:


net_income_latest = {}

for x in net_income_target:
    year = int(x["start"][:4])
    
    if year not in net_income_latest or x["filed"] > net_income_latest[year]["filed"]:
        net_income_latest[year] = x


# In[78]:


net_income_latest


# In[79]:


net_income_final = [
    {
        "year": year,
        "net_income_usd_000": data["val"] / 1000
    }
    for year, data in net_income_latest.items()
]


# In[80]:


net_income_final


# In[81]:


len(net_income_final), [x["year"] for x in net_income_final]


# In[82]:


operating_cash_flow_candidates = [
    key for key in us_gaap.keys()
    if "OperatingActivities" in key
]


# In[83]:


operating_cash_flow_candidates


# In[84]:


us_gaap["NetCashProvidedByUsedInOperatingActivities"]["description"]


# In[85]:


operating_cash_flow_concept = us_gaap["NetCashProvidedByUsedInOperatingActivities"]


# In[86]:


operating_cash_flow_concept.keys()


# In[87]:


operating_cash_flow_concept["units"].keys()


# In[88]:


operating_cash_flow_concept["units"]["USD"][:5]


# In[89]:


operating_cash_flow_annual = [
    x for x in operating_cash_flow_concept["units"]["USD"]
    if x.get("fp") == "FY" and x.get("form") == "10-K"
]


# In[90]:


len(operating_cash_flow_annual)


# In[91]:


operating_cash_flow_target = [
    x for x in operating_cash_flow_annual
    if x.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]


# In[92]:


len(operating_cash_flow_target)


# In[93]:


operating_cash_flow_target


# In[94]:


operating_cash_flow_latest = {}

for x in operating_cash_flow_target:
    year = int(x["start"][:4])
    
    if year not in operating_cash_flow_latest or x["filed"] > operating_cash_flow_latest[year]["filed"]:
        operating_cash_flow_latest[year] = x


# In[95]:


operating_cash_flow_latest


# In[96]:


operating_cash_flow_final = [
    {
        "year": year,
        "operating_cash_flow_usd_000": data["val"] / 1000
    }
    for year, data in operating_cash_flow_latest.items()
]


# In[97]:


operating_cash_flow_final


# In[98]:


len(operating_cash_flow_final), [x["year"] for x in operating_cash_flow_final]


# # Step 1 — Inspect our five metric objects

# In[99]:


print(revenue_final)
print(gross_profit_final)
print(operating_income_final)
print(net_income_final)
print(operating_cash_flow_final)


# In[100]:


etsy_financials = (
    pd.DataFrame(revenue_final)
    .merge(pd.DataFrame(gross_profit_final), on="year")
    .merge(pd.DataFrame(operating_income_final), on="year")
    .merge(pd.DataFrame(net_income_final), on="year")
    .merge(pd.DataFrame(operating_cash_flow_final), on="year")
)

etsy_financials


# In[101]:


etsy_financials.isna().sum()


# In[102]:


etsy_financials.duplicated(subset=["year"]).sum()


# In[103]:


etsy_financials["year"].tolist()


# In[104]:


(etsy_financials["gross_profit_usd_000"] <= etsy_financials["revenue_usd_000"]).all()


# In[105]:


(etsy_financials["operating_income_usd_000"] <= etsy_financials["gross_profit_usd_000"]).all()


# In[106]:


etsy_financials["operating_cash_flow_usd_000"] > etsy_financials["net_income_usd_000"]


# In[107]:


etsy_financials["revenue_growth_pct"] = (
    etsy_financials["revenue_usd_000"].pct_change() * 100
)

etsy_financials


# In[108]:


etsy_financials["gross_margin_pct"] = (
    etsy_financials["gross_profit_usd_000"]
    / etsy_financials["revenue_usd_000"]
    * 100
)

etsy_financials


# In[109]:



etsy_financials["operating_margin_pct"] = (
    etsy_financials["operating_income_usd_000"]
    / etsy_financials["revenue_usd_000"]
    * 100
)

etsy_financials


# In[110]:


etsy_financials["net_margin_pct"] = (
    etsy_financials["net_income_usd_000"]
    / etsy_financials["revenue_usd_000"]
    * 100
)

etsy_financials


# In[111]:


etsy_financials["cfo_margin_pct"] = (
    etsy_financials["operating_cash_flow_usd_000"]
    / etsy_financials["revenue_usd_000"]
    * 100
)

etsy_financials


# In[112]:


etsy_financials[
    [
        "revenue_growth_pct",
        "gross_margin_pct",
        "operating_margin_pct",
        "net_margin_pct",
        "cfo_margin_pct"
    ]
].isna().sum()


# In[113]:


margin_checks = pd.DataFrame({
    "gross_margin_check": (
        etsy_financials["gross_margin_pct"]
        - (
            etsy_financials["gross_profit_usd_000"]
            / etsy_financials["revenue_usd_000"]
            * 100
        )
    ).abs(),

    "operating_margin_check": (
        etsy_financials["operating_margin_pct"]
        - (
            etsy_financials["operating_income_usd_000"]
            / etsy_financials["revenue_usd_000"]
            * 100
        )
    ).abs(),

    "net_margin_check": (
        etsy_financials["net_margin_pct"]
        - (
            etsy_financials["net_income_usd_000"]
            / etsy_financials["revenue_usd_000"]
            * 100
        )
    ).abs(),

    "cfo_margin_check": (
        etsy_financials["cfo_margin_pct"]
        - (
            etsy_financials["operating_cash_flow_usd_000"]
            / etsy_financials["revenue_usd_000"]
            * 100
        )
    ).abs()
})

margin_checks


# # Phase 2 — Reusable Financial ETL

# In[114]:


target_company_mapping = company_mapping.copy()

target_company_mapping


# ## Step 1 — Create the financial concept configuration

# In[115]:


financial_concepts = {
    "revenue": "RevenueFromContractWithCustomerExcludingAssessedTax",
    "gross_profit": "GrossProfit",
    "operating_income": "OperatingIncomeLoss",
    "net_income": "NetIncomeLoss",
    "operating_cash_flow": "NetCashProvidedByUsedInOperatingActivities"
}

financial_concepts


# ## Step 2 — Create a reusable SEC URL

# In[116]:


def get_company_facts_url(cik):
    return f"https://data.sec.gov/api/xbrl/companyfacts/CIK{int(cik):010d}.json"


# 
# 
# 
# 
# 
# ## Step 3 — Test the function with Etsy

# In[117]:





etsy_cik = target_company_mapping.loc[
    target_company_mapping["ticker"] == "ETSY", "cik_str"
].iloc[0]

etsy_url = get_company_facts_url(etsy_cik)

etsy_url


# ## Step 4 — Create a reusable SEC data-fetching function

# In[118]:


def fetch_company_facts(cik):
    url = get_company_facts_url(cik)
    
    response = requests.get(
        url,
        headers=headers
    )
    
    response.raise_for_status()
    
    return response.json()


# ## Step 5 — Test the fetching function with Etsy

# In[119]:


etsy_facts = fetch_company_facts(etsy_cik)

etsy_facts.keys()


# ## Step 6 — Verify the returned company

# In[120]:


etsy_facts["entityName"]


# ## Step 7 — Build the reusable metric extractor

# In[121]:


def extract_metric(company_facts, concept_name):
    us_gaap = company_facts["facts"]["us-gaap"]
    concept = us_gaap[concept_name]
    
    return concept


# ## Step 8 — Test extract_metric()

# In[122]:


etsy_revenue_concept = extract_metric(
    etsy_facts,
    "RevenueFromContractWithCustomerExcludingAssessedTax"
)

etsy_revenue_concept.keys()


# ## Step 9 — Let's inspect the units

# In[123]:


etsy_revenue_concept["units"].keys()


# ## Step 10 — Get the raw USD observations

# In[124]:


observations = etsy_revenue_concept["units"]["USD"]

len(observations)


# ## Step 1 — Filter annual 10-K observations

# In[125]:


annual_observations = [
    x for x in observations
    if x.get("fp") == "FY" and x.get("form") == "10-K"
]

len(annual_observations)


# In[126]:


## Step 2 — Filter our target years


# In[127]:


target_observations = [
    x for x in annual_observations
    if x.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]

len(target_observations)


# In[128]:


## Step 3 — Inspect the 6 observations


# In[129]:


[
    {
        "start": x.get("start"),
        "end": x.get("end"),
        "val": x.get("val"),
        "filed": x.get("filed"),
        "accn": x.get("accn"),
        "frame": x.get("frame")
    }
    for x in target_observations
]


# In[130]:


## Step 4 — Select the latest filing for each year


# In[131]:


latest_observations = {}

for x in target_observations:
    year = int(x["start"][:4])
    
    if year not in latest_observations or x["filed"] > latest_observations[year]["filed"]:
        latest_observations[year] = x

latest_observations


# In[132]:


## Step 5 — Standardize the values


# In[133]:


revenue_final = [
    {
        "year": year,
        "revenue_usd_000": data["val"] / 1000
    }
    for year, data in latest_observations.items()
]

revenue_final


# In[134]:


## Step 6 — Basic QA check


# In[135]:


len(revenue_final), [x["year"] for x in revenue_final]


# In[136]:


## Step 7 — Check for duplicate years


# In[137]:


years = [x["year"] for x in revenue_final]

len(years) != len(set(years))


# In[138]:


all(
    x["revenue_usd_000"] is not None
    for x in revenue_final
)


# In[139]:


etsy_gross_profit_concept = extract_metric(
    etsy_facts,
    "GrossProfit"
)

etsy_gross_profit_concept.keys()


# In[140]:


## Step 8 — Check Gross Profit units


# In[141]:


etsy_gross_profit_concept["units"].keys()


# In[142]:


## Step 9 — Get the Gross Profit observations


# In[143]:


gross_profit_observations = etsy_gross_profit_concept["units"]["USD"]

len(gross_profit_observations)


# In[144]:


## Step 10 — Filter to annual 10-K observations


# In[145]:


gross_profit_annual = [
    x for x in gross_profit_observations
    if x.get("fp") == "FY" and x.get("form") == "10-K"
]

len(gross_profit_annual)


# In[146]:


## Step 11 — Filter Gross Profit to FY2023–FY2025


# In[147]:


gross_profit_target = [
    x for x in gross_profit_annual
    if x.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]

len(gross_profit_target)


# In[148]:


##Step 12 — Inspect the 6 observations


# In[149]:


[
    {
        "start": x.get("start"),
        "end": x.get("end"),
        "val": x.get("val"),
        "filed": x.get("filed"),
        "accn": x.get("accn"),
        "frame": x.get("frame")
    }
    for x in gross_profit_target
]


# In[150]:


## Step 13 — Select the latest filing for each year


# In[151]:


gross_profit_latest = {}

for x in gross_profit_target:
    year = int(x["start"][:4])
    
    if year not in gross_profit_latest or x["filed"] > gross_profit_latest[year]["filed"]:
        gross_profit_latest[year] = x

gross_profit_latest


# In[152]:


## Step 14 — Standardize Gross Profit to USD thousands


# In[153]:


gross_profit_final = [
    {
        "year": year,
        "gross_profit_usd_000": data["val"] / 1000
    }
    for year, data in gross_profit_latest.items()
]

gross_profit_final


# In[154]:


##Step 15 — Check count and years


# In[155]:


len(gross_profit_final), [x["year"] for x in gross_profit_final]


# In[156]:


## Step 16 — Duplicate-year QA


# In[157]:


years = [x["year"] for x in gross_profit_final]

len(years) != len(set(years))


# In[158]:


## Step 17 — Check for missing Gross Profit values


# In[159]:


all(
    x["gross_profit_usd_000"] is not None
    for x in gross_profit_final
)


# In[160]:


etsy_operating_income_concept = extract_metric(
    etsy_facts,
    "OperatingIncomeLoss"
)


# In[161]:


etsy_operating_income_concept.keys()


# In[162]:


## Step 18 — Check the unit


# In[163]:


etsy_operating_income_concept["units"].keys()


# In[164]:


## Step 19 — Get the observations


# In[165]:


operating_income_observations = etsy_operating_income_concept["units"]["USD"]

len(operating_income_observations)


# In[166]:


## Step 20 — Keep only annual 10-K observations


# In[167]:


operating_income_annual = [
    x for x in operating_income_observations
    if x.get("fp") == "FY" and x.get("form") == "10-K"
]

len(operating_income_annual)


# In[168]:


## Step 21 — Filter to FY2023–FY2025


# In[169]:


operating_income_target = [
    x for x in operating_income_annual
    if x.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]

len(operating_income_target)


# In[170]:


## Step 22 — Inspect the 6 observations


# In[171]:


for x in operating_income_target:
    print(
        x.get("start"),
        x.get("end"),
        x.get("val"),
        x.get("filed"),
        x.get("form"),
        x.get("frame")
    )


# In[172]:


## Step 23 — Select the latest observation for each year


# In[173]:


operating_income_latest = {}

for x in operating_income_target:
    year = int(x["start"][:4])
    
    if (
        year not in operating_income_latest
        or x["filed"] > operating_income_latest[year]["filed"]
    ):
        operating_income_latest[year] = x


# In[174]:


operating_income_latest


# In[175]:


## Step 23 — Standardize Operating Income


# In[176]:


operating_income_final = [
    {
        "year": year,
        "operating_income_usd_000": data["val"] / 1000
    }
    for year, data in operating_income_latest.items()
]


# In[177]:


operating_income_final


# In[178]:


## Step 24 — Check count and years


# In[179]:


len(operating_income_final), [x["year"] for x in operating_income_final]


# In[180]:


## Step 25 — Duplicate-year QA


# In[181]:


years = [x["year"] for x in operating_income_final]

len(years) != len(set(years))


# In[182]:


## Step 26 — Final Operating Income QA: missing values


# In[183]:


all(
    x["operating_income_usd_000"] is not None
    for x in operating_income_final
)


# In[184]:


etsy_net_income_concept = extract_metric(
    etsy_facts,
    "NetIncomeLoss"
)


# In[185]:


etsy_net_income_concept.keys()


# In[186]:


## Step 27 — Check Net Income unit


# In[187]:


etsy_net_income_concept["units"].keys()


# In[188]:


## Step 28 — Get the raw Net Income observations


# In[189]:


net_income_observations = etsy_net_income_concept["units"]["USD"]

len(net_income_observations)


# In[190]:


## Step 29 — Filter Net Income to annual 10-K observations


# In[191]:


net_income_annual = [
    x for x in net_income_observations
    if x.get("fp") == "FY" and x.get("form") == "10-K"
]

len(net_income_annual)


# In[192]:


## Step 30 — Filter to FY2023–FY2025


# In[193]:


net_income_target = [
    x for x in net_income_annual
    if x.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]

len(net_income_target)


# In[194]:


## Step 31 — Inspect the Net Income observations


# In[195]:


for x in net_income_target:
    print(
        x.get("start"),
        x.get("end"),
        x.get("val"),
        x.get("filed"),
        x.get("form"),
        x.get("frame")
    )


# In[196]:


## Step 32 — Select the latest Net Income observation


# In[197]:


net_income_latest = {}

for x in net_income_target:
    year = int(x["start"][:4])
    
    if (
        year not in net_income_latest
        or x["filed"] > net_income_latest[year]["filed"]
    ):
        net_income_latest[year] = x


# In[198]:


net_income_latest


# In[199]:


## Step 33 — Standardize Net Income


# In[200]:


net_income_final = [
    {
        "year": year,
        "net_income_usd_000": data["val"] / 1000
    }
    for year, data in net_income_latest.items()
]


# In[201]:


net_income_final


# In[202]:


##Step 34 — Check count and years


# In[203]:


len(net_income_final), [x["year"] for x in net_income_final]


# In[204]:


##Step 1 — Check duplicates


# In[205]:


net_income_years = [x["year"] for x in net_income_final]

len(net_income_years) != len(set(net_income_years))


# In[206]:


##Step 2 — Check for missing values


# In[207]:


any(x["net_income_usd_000"] is None for x in net_income_final)


# In[208]:


## Operating Cash Flow


# In[209]:


ocf_years = [x["year"] for x in operating_cash_flow_final]

len(ocf_years) != len(set(ocf_years))


# In[210]:


any(x["operating_cash_flow_usd_000"] is None for x in operating_cash_flow_final)


# In[211]:


##Step 1 — Combine the five metrics


# In[212]:


revenue_final


# In[213]:


gross_profit_final


# In[214]:


operating_income_final


# In[215]:


net_income_final


# In[216]:


operating_cash_flow_final


# In[217]:




etsy_financial_df = pd.DataFrame(revenue_final)

etsy_financial_df


# In[218]:


etsy_financial_df = etsy_financial_df.merge(
    pd.DataFrame(gross_profit_final),
    on="year",
    how="left"
)

etsy_financial_df


# In[219]:


etsy_financial_df = etsy_financial_df.merge(
    pd.DataFrame(operating_income_final),
    on="year",
    how="left"
)

etsy_financial_df


# In[222]:


etsy_financial_df = etsy_financial_df.merge(
    pd.DataFrame(net_income_final),
    on="year",
    how="left"
)

etsy_financial_df


# In[223]:


etsy_financial_df = etsy_financial_df.merge(
    pd.DataFrame(operating_cash_flow_final),
    on="year",
    how="left"
)

etsy_financial_df


# In[224]:


etsy_financial_df["year"].duplicated().any()


# In[225]:


etsy_financial_df.isna().any()


# In[226]:


## callculation


# In[227]:


etsy_financial_df["gross_margin_pct"] = (
    etsy_financial_df["gross_profit_usd_000"]
    / etsy_financial_df["revenue_usd_000"]
) * 100

etsy_financial_df[["year", "gross_margin_pct"]]


# In[228]:


etsy_financial_df["operating_margin_pct"] = (
    etsy_financial_df["operating_income_usd_000"]
    / etsy_financial_df["revenue_usd_000"]
) * 100

etsy_financial_df[["year", "operating_margin_pct"]]


# In[236]:


etsy_financial_df["net_margin_pct"] = (


    etsy_financial_df["net_income_usd_000"]


    / etsy_financial_df["revenue_usd_000"]



) * 100


etsy_financial_df[["year", "net_margin_pct"]]


# In[242]:


etsy_financial_df["cfo_margin_pct"] = (
    etsy_financial_df["operating_cash_flow_usd_000"]
    / etsy_financial_df["revenue_usd_000"]
) * 100

etsy_financial_df[["year", "cfo_margin_pct"]]


# In[243]:


etsy_financial_df["revenue_growth_pct"] = (
    etsy_financial_df["revenue_usd_000"].pct_change()
) * 100

etsy_financial_df[["year", "revenue_growth_pct"]]


# In[244]:


etsy_financial_df["gross_profit_usd_000"] <= etsy_financial_df["revenue_usd_000"]


# In[245]:


etsy_financial_df["operating_income_usd_000"] <= etsy_financial_df["gross_profit_usd_000"]


# In[246]:


etsy_financial_df[
    [
        "year",
        "operating_income_usd_000",
        "net_income_usd_000"
    ]
]


# In[247]:


etsy_financial_df[
    [
        "year",
        "net_income_usd_000",
        "operating_cash_flow_usd_000"
    ]
]


# In[248]:


etsy_financial_df[
    [
        "year",
        "revenue_usd_000",
        "gross_profit_usd_000",
        "operating_income_usd_000"
    ]
]


# In[249]:


(
    etsy_financial_df["gross_profit_usd_000"]
    / etsy_financial_df["revenue_usd_000"]
    * 100
).round(2)


# In[250]:


(
    etsy_financial_df["operating_income_usd_000"]
    / etsy_financial_df["revenue_usd_000"]
    * 100
).round(2)


# In[251]:


(
    etsy_financial_df["net_income_usd_000"]
    / etsy_financial_df["revenue_usd_000"]
    * 100
).round(2)


# In[252]:


(
    etsy_financial_df["operating_cash_flow_usd_000"]
    / etsy_financial_df["revenue_usd_000"]
    * 100
).round(2)


# In[253]:


etsy_financial_df["revenue_usd_000"].pct_change().mul(100).round(2)


# In[254]:


etsy_financial_df["year"].is_monotonic_increasing


# In[255]:


etsy_financial_df["revenue_usd_000"] > 0


# In[256]:


etsy_financial_df["gross_profit_usd_000"] > 0


# In[257]:


etsy_financial_df["operating_income_usd_000"] > 0


# In[258]:


etsy_financial_df["net_income_usd_000"] > 0


# In[259]:


etsy_financial_df["operating_cash_flow_usd_000"] > 0


# In[260]:


etsy_financial_df[
    [
        "gross_margin_pct",
        "operating_margin_pct",
        "net_margin_pct",
        "cfo_margin_pct"
    ]
].apply(lambda col: col.between(-100, 100)).all()


# In[261]:


etsy_financial_df[
    [
        "gross_margin_pct",
        "operating_margin_pct",
        "net_margin_pct",
        "cfo_margin_pct"
    ]
].apply(lambda column: column.between(-100, 100)).all()


# In[262]:


etsy_financial_df.loc[
    etsy_financial_df["year"] == 2023,
    "revenue_growth_pct"
].isna()


# In[263]:


etsy_financial_df.loc[
    etsy_financial_df["year"].isin([2024, 2025]),
    "revenue_growth_pct"
].notna()


# In[264]:


expected_revenue_growth = (
    etsy_financial_df["revenue_usd_000"].pct_change() * 100
)

(
    etsy_financial_df["revenue_growth_pct"]
    .fillna(0)
    .round(6)
    ==
    expected_revenue_growth
    .fillna(0)
    .round(6)
).all()


# In[265]:


etsy_financial_df.columns.tolist()


# In[266]:


etsy_financial_df


# In[267]:


etsy_financial_df.dtypes


# In[268]:


##Step 1A — Create the company configuration


# In[269]:


company_config = {
    "ETSY": {
        "company_name": "Etsy",
        "cik": "0001370637"
    },
    "SHAK": {
        "company_name": "Shake Shack",
        "cik": "0001620533"
    },
    "CROX": {
        "company_name": "Crocs",
        "cik": "0001334036"
    },
    "BOOT": {
        "company_name": "Boot Barn",
        "cik": "0001549993"
    },
    "DUOL": {
        "company_name": "Duolingo",
        "cik": "0001562088"
    }
}


# In[270]:


company_config


# In[271]:


etsy_config = company_config["ETSY"]

etsy_config


# In[272]:


##Step 1b — Build the SEC Company Facts URL dynamically


# In[273]:


cik = etsy_config["cik"]

sec_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

sec_url


# In[274]:


import requests


# In[275]:


headers = {
    "User-Agent": "Corporate Venture Investment Intelligence project shifanaazanalyst1@gmail.com"
}

response = requests.get(sec_url, headers=headers)

response.status_code


# In[276]:


##Step 1C — Convert the SEC response to JSON


# In[277]:


company_facts = response.json()


# In[278]:


type(company_facts)


# In[279]:


##Step 1D — Inspect the top-level structure


# In[280]:


company_facts.keys()


# In[281]:


##Step 1E — Access the XBRL facts


# In[282]:


facts = company_facts["facts"]

type(facts)


# In[283]:


##Step 1F — Inspect the available XBRL namespaces


# In[284]:


facts.keys()


# In[285]:


##Step 1G — Access the US-GAAP concepts


# In[286]:


us_gaap = facts["us-gaap"]

type(us_gaap)


# In[287]:


##Step 1H — Find our revenue-related XBRL concepts


# In[288]:


revenue_concepts = [
    key for key in us_gaap.keys()
    if "Revenue" in key
]

revenue_concepts


# In[289]:


##Step 1J — Inspect the actual Etsy revenue concept we previously validated


# In[290]:


revenue_fact = us_gaap["RevenueFromContractWithCustomerExcludingAssessedTax"]

type(revenue_fact)


# In[291]:


##Step 1K — Inspect the revenue concept structure


# In[292]:


revenue_fact.keys()


# In[293]:


##Step 1L — Inspect the available units


# In[294]:


revenue_fact["units"].keys()


# In[295]:


##Step 1M — Inspect the actual reported observations


# In[296]:


revenue_data = revenue_fact["units"]["USD"]

type(revenue_data)


# In[297]:


##Step 1N — Inspect one observation


# In[298]:


revenue_data[0]


# In[299]:


##Step 1o — Inspect recent observations


# In[300]:


revenue_data[-10:]


# In[301]:


##Step 1P — Create the annual revenue filter


# In[308]:


annual_revenue_data = [
    item for item in revenue_data
    if item.get("form") == "10-K"
    and item.get("fp") == "FY"
]


# In[309]:


len(annual_revenue_data)


# In[310]:


##Step 1Q — Inspect the annual records' periods


# In[311]:


[
    {
        "end": item.get("end"),
        "val": item.get("val"),
        "form": item.get("form"),
        "fp": item.get("fp"),
        "frame": item.get("frame")
    }
    for item in annual_revenue_data[-5:]
]


# In[312]:


##Step 1R — Filter to the annual calendar-year frames


# In[313]:


annual_revenue_data = [
    item for item in revenue_data
    if item.get("form") == "10-K"
    and item.get("fp") == "FY"
    and item.get("frame") in ["CY2023", "CY2024", "CY2025"]
]


# In[314]:


annual_revenue_data


# In[315]:


##Step 1S — Convert the SEC observations into our standardized structure


# In[316]:


revenue_records = [
    {
        "year": int(item["frame"].replace("CY", "")),
        "revenue_usd_000": item["val"] / 1000
    }
    for item in annual_revenue_data
]


# In[317]:


revenue_records


# In[318]:


etsy_revenue_reference = pd.DataFrame({
    "year": [2023, 2024, 2025],
    "revenue_usd_000": [2748377.0, 2808332.0, 2883501.0]
})

etsy_revenue_reference


# In[319]:


gross_profit_concepts = [
    key for key in us_gaap.keys()
    if "GrossProfit" in key
]

gross_profit_concepts


# In[320]:


gross_profit_fact = us_gaap["GrossProfit"]

gross_profit_fact.keys()


# In[321]:


gross_profit_fact["units"].keys()


# In[322]:


gross_profit_data = gross_profit_fact["units"]["USD"]

type(gross_profit_data)


# In[323]:


gross_profit_data[-10:]


# In[324]:


annual_gross_profit_data = [
    item for item in gross_profit_data
    if item.get("form") == "10-K"
    and item.get("fp") == "FY"
    and item.get("frame") in ["CY2023", "CY2024", "CY2025"]
]

annual_gross_profit_data


# In[325]:


gross_profit_records = [
    {
        "year": int(item["frame"].replace("CY", "")),
        "gross_profit_usd_000": item["val"] / 1000
    }
    for item in annual_gross_profit_data
]

gross_profit_records


# In[326]:


gross_profit_df = pd.DataFrame(gross_profit_records)

gross_profit_df


# In[327]:


etsy_gross_profit_reference = pd.DataFrame({
    "year": [2023, 2024, 2025],
    "gross_profit_usd_000": [1919702.0, 2033778.0, 2065701.0]
})

gross_profit_df.equals(etsy_gross_profit_reference)


# In[328]:


##oprating income


# In[329]:


operating_income_concepts = [
    key for key in us_gaap.keys()
    if "OperatingIncome" in key
]

operating_income_concepts


# In[330]:


operating_income_fact = us_gaap["OperatingIncomeLoss"]

operating_income_fact.keys()


# In[331]:


operating_income_fact["units"].keys()


# In[332]:


operating_income_data = operating_income_fact["units"]["USD"]

type(operating_income_data)


# In[333]:


operating_income_data[-10:]


# In[334]:


annual_operating_income_data = [
    item for item in operating_income_data
    if item.get("form") == "10-K"
    and item.get("fp") == "FY"
    and item.get("frame") in ["CY2023", "CY2024", "CY2025"]
]

annual_operating_income_data


# In[335]:


operating_income_records = [
    {
        "year": int(item["frame"].replace("CY", "")),
        "operating_income_usd_000": item["val"] / 1000
    }
    for item in annual_operating_income_data
]

operating_income_records


# In[336]:


operating_income_df = pd.DataFrame(operating_income_records)

operating_income_df


# In[337]:


##Next Step : Validate it against our Etsy prototype


# In[338]:


etsy_operating_income_reference = pd.DataFrame({
    "year": [2023, 2024, 2025],
    "operating_income_usd_000": [279841.0, 380208.0, 266210.0]
})

operating_income_df.equals(etsy_operating_income_reference)


# In[339]:


net_income_concepts = [
    key for key in us_gaap.keys()
    if "NetIncome" in key
]

net_income_concepts


# In[340]:


net_income_fact = us_gaap["NetIncomeLoss"]

net_income_fact.keys()


# In[341]:


net_income_fact["units"].keys()


# In[342]:


net_income_data = net_income_fact["units"]["USD"]

net_income_data[:3]


# In[343]:


annual_net_income_data = [
    item for item in net_income_data
    if item.get("form") == "10-K"
    and item.get("fp") == "FY"
    and item.get("frame") in ["CY2023", "CY2024", "CY2025"]
]

annual_net_income_data


# In[344]:


recent_net_income_annual = [
    item for item in net_income_data
    if item.get("form") == "10-K"
    and item.get("fp") == "FY"
]

recent_net_income_annual[-10:]


# In[345]:


annual_net_income_data = [
    item for item in recent_net_income_annual
    if item.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and item.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]

annual_net_income_data


# In[346]:


annual_net_income_df = pd.DataFrame(annual_net_income_data)

annual_net_income_df["year"] = (
    pd.to_datetime(annual_net_income_df["start"]).dt.year
)

annual_net_income_df = (
    annual_net_income_df
    .sort_values("filed")
    .drop_duplicates(subset="year", keep="last")
)

annual_net_income_df


# In[347]:


net_income_records = [
    {
        "year": int(row["year"]),
        "net_income_usd_000": row["val"] / 1000
    }
    for _, row in annual_net_income_df.iterrows()
]

net_income_records


# In[348]:


net_income_df = pd.DataFrame(net_income_records)

net_income_df


# In[349]:


etsy_net_income_reference = pd.DataFrame({
    "year": [2023, 2024, 2025],
    "net_income_usd_000": [307568.0, 303281.0, 162982.0]
})

net_income_df.equals(etsy_net_income_reference)


# In[350]:


##Next Step: Operating Cash Flow


# In[351]:


ocf_concepts = [
    key for key in us_gaap.keys()
    if "OperatingCashFlow" in key
]

ocf_concepts


# In[352]:


cash_flow_concepts = [
    key for key in us_gaap.keys()
    if "Cash" in key and "Operating" in key
]

cash_flow_concepts


# In[353]:


ocf_fact = us_gaap["NetCashProvidedByUsedInOperatingActivities"]

ocf_fact.keys()


# In[354]:


ocf_fact["units"].keys()


# In[355]:


ocf_data = ocf_fact["units"]["USD"]

ocf_data[:3]


# In[356]:


recent_ocf_annual = [
    item for item in ocf_data
    if item.get("form") == "10-K"
    and item.get("fp") == "FY"
]

recent_ocf_annual[-10:]


# In[357]:


annual_ocf_data = [
    item for item in recent_ocf_annual
    if item.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and item.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]

annual_ocf_data


# In[358]:


annual_ocf_df = pd.DataFrame(annual_ocf_data)

annual_ocf_df["year"] = (
    pd.to_datetime(annual_ocf_df["start"]).dt.year
)

annual_ocf_df = (
    annual_ocf_df
    .sort_values("filed")
    .drop_duplicates(subset="year", keep="last")
)

annual_ocf_df


# In[359]:


ocf_records = [
    {
        "year": int(row["year"]),
        "operating_cash_flow_usd_000": row["val"] / 1000
    }
    for _, row in annual_ocf_df.iterrows()
]

ocf_records


# In[360]:


operating_cash_flow_df = pd.DataFrame(ocf_records)

operating_cash_flow_df


# In[361]:


etsy_ocf_reference = pd.DataFrame({
    "year": [2023, 2024, 2025],
    "operating_cash_flow_usd_000": [705513.0, 752469.0, 693414.0]
})

operating_cash_flow_df.equals(etsy_ocf_reference)


# # Step: Merge the five validated DataFrames

# In[367]:


revenue_df = etsy_financial_df[["year", "revenue_usd_000"]].copy()

revenue_df


# In[368]:


etsy_financial_base = (
    revenue_df
    .merge(gross_profit_df, on="year", how="inner")
    .merge(operating_income_df, on="year", how="inner")
    .merge(net_income_df, on="year", how="inner")
    .merge(operating_cash_flow_df, on="year", how="inner")
    .sort_values("year")
    .reset_index(drop=True)
)

etsy_financial_base


# In[ ]:





# In[ ]:





# In[369]:


etsy_financial_df = etsy_financial_base.copy()

etsy_financial_df["gross_margin_pct"] = (
    etsy_financial_df["gross_profit_usd_000"]
    / etsy_financial_df["revenue_usd_000"]
) * 100

etsy_financial_df["operating_margin_pct"] = (
    etsy_financial_df["operating_income_usd_000"]
    / etsy_financial_df["revenue_usd_000"]
) * 100

etsy_financial_df["net_margin_pct"] = (
    etsy_financial_df["net_income_usd_000"]
    / etsy_financial_df["revenue_usd_000"]
) * 100

etsy_financial_df["cfo_margin_pct"] = (
    etsy_financial_df["operating_cash_flow_usd_000"]
    / etsy_financial_df["revenue_usd_000"]
) * 100

etsy_financial_df["revenue_growth_pct"] = (
    etsy_financial_df["revenue_usd_000"]
    .pct_change() * 100
)

etsy_financial_df


# In[370]:


etsy_financial_df.equals(
    pd.DataFrame({
        "year": [2023, 2024, 2025],
        "revenue_usd_000": [2748377.0, 2808332.0, 2883501.0],
        "gross_profit_usd_000": [1919702.0, 2033778.0, 2065701.0],
        "operating_income_usd_000": [279841.0, 380208.0, 266210.0],
        "net_income_usd_000": [307568.0, 303281.0, 162982.0],
        "operating_cash_flow_usd_000": [705513.0, 752469.0, 693414.0],
        "gross_margin_pct": [69.848569, 72.419429, 71.638643],
        "operating_margin_pct": [10.182046, 13.538570, 9.232180],
        "net_margin_pct": [11.190896, 10.799329, 5.652226],
        "cfo_margin_pct": [25.670168, 26.794161, 24.047642],
        "revenue_growth_pct": [float("nan"), 2.181469, 2.676642]
    })
)


# In[ ]:


##step — identify the mismatch


# In[371]:


etsy_financial_df.compare(
    pd.DataFrame({
        "year": [2023, 2024, 2025],
        "revenue_usd_000": [2748377.0, 2808332.0, 2883501.0],
        "gross_profit_usd_000": [1919702.0, 2033778.0, 2065701.0],
        "operating_income_usd_000": [279841.0, 380208.0, 266210.0],
        "net_income_usd_000": [307568.0, 303281.0, 162982.0],
        "operating_cash_flow_usd_000": [705513.0, 752469.0, 693414.0],
        "gross_margin_pct": [69.848569, 72.419429, 71.638643],
        "operating_margin_pct": [10.182046, 13.538570, 9.232180],
        "net_margin_pct": [11.190896, 10.799329, 5.652226],
        "cfo_margin_pct": [25.670168, 26.794161, 24.047642],
        "revenue_growth_pct": [float("nan"), 2.181469, 2.676642]
    })
)


# In[ ]:


##step — check the structure


# In[372]:


print("Current shape:", etsy_financial_df.shape)
print("Current columns:", list(etsy_financial_df.columns))
print("Current index:", etsy_financial_df.index.tolist())

print("\nDtypes:")
print(etsy_financial_df.dtypes)


# In[373]:


##small step — check the exact numerical difference


# In[374]:


prototype_df = pd.DataFrame({
    "year": [2023, 2024, 2025],
    "revenue_usd_000": [2748377.0, 2808332.0, 2883501.0],
    "gross_profit_usd_000": [1919702.0, 2033778.0, 2065701.0],
    "operating_income_usd_000": [279841.0, 380208.0, 266210.0],
    "net_income_usd_000": [307568.0, 303281.0, 162982.0],
    "operating_cash_flow_usd_000": [705513.0, 752469.0, 693414.0],
    "gross_margin_pct": [69.848569, 72.419429, 71.638643],
    "operating_margin_pct": [10.182046, 13.538570, 9.232180],
    "net_margin_pct": [11.190896, 10.799329, 5.652226],
    "cfo_margin_pct": [25.670168, 26.794161, 24.047642],
    "revenue_growth_pct": [float("nan"), 2.181469, 2.676642]
})

for column in etsy_financial_df.columns:
    print(
        column,
        "→",
        (etsy_financial_df[column] - prototype_df[column]).abs().max()
    )


# In[375]:


##Final Etsy validation


# In[376]:


import numpy as np

np.allclose(
    etsy_financial_df.drop(columns=["revenue_growth_pct"]),
    prototype_df.drop(columns=["revenue_growth_pct"]),
    equal_nan=True,
    atol=1e-6
)


# In[377]:


np.allclose(
    etsy_financial_df["revenue_growth_pct"],
    prototype_df["revenue_growth_pct"],
    equal_nan=True,
    atol=1e-6
)


# ## Next step: create a reusable SEC Company Facts retrieval function.

# In[378]:


##Step 1 — Create the reusable SEC retrieval function


# In[379]:


def get_company_facts(cik):
    sec_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    
    response = requests.get(
        sec_url,
        headers=headers
    )
    
    response.raise_for_status()
    
    return response.json()


# In[380]:


etsy_facts_test = get_company_facts(etsy_config["cik"])

type(etsy_facts_test)


# In[381]:


etsy_facts_test["entityName"]


# In[382]:


etsy_facts_test["facts"].keys()


# In[383]:


etsy_us_gaap_test = etsy_facts_test["facts"]["us-gaap"]

type(etsy_us_gaap_test)


# In[384]:


"RevenueFromContractWithCustomerExcludingAssessedTax" in etsy_us_gaap_test


# In[385]:


def get_us_gaap_facts(company_facts):
    return company_facts["facts"]["us-gaap"]


# In[386]:


etsy_us_gaap_test_2 = get_us_gaap_facts(etsy_facts_test)

type(etsy_us_gaap_test_2)


# In[387]:


"RevenueFromContractWithCustomerExcludingAssessedTax" in etsy_us_gaap_test_2


# In[388]:


def get_xbrl_concept(us_gaap, concept_name):
    return us_gaap[concept_name]


# In[389]:


etsy_revenue_test = get_xbrl_concept(
    etsy_us_gaap_test_2,
    "RevenueFromContractWithCustomerExcludingAssessedTax"
)

type(etsy_revenue_test)


# In[390]:


etsy_revenue_test.keys()


# In[391]:


etsy_revenue_test["units"].keys()


# In[392]:


etsy_revenue_test["units"]["USD"][:3]


# In[393]:


def get_xbrl_units(concept, unit):
    return concept["units"][unit]


# In[394]:


etsy_revenue_usd_test = get_xbrl_units(
    etsy_revenue_test,
    "USD"
)

type(etsy_revenue_usd_test)


# In[395]:


etsy_revenue_usd_test[-3:]


# In[396]:


annual_revenue_test = [
    item for item in etsy_revenue_usd_test
    if item.get("form") == "10-K"
    and item.get("fp") == "FY"
    and item.get("frame") in ["CY2023", "CY2024", "CY2025"]
]

len(annual_revenue_test)


# In[397]:


annual_revenue_test


# In[398]:


def filter_annual_observations(observations, target_years):
    return [
        item for item in observations
        if item.get("form") == "10-K"
        and item.get("fp") == "FY"
        and item.get("frame") in [f"CY{year}" for year in target_years]
    ]


# In[399]:


annual_revenue_test_2 = filter_annual_observations(
    etsy_revenue_usd_test,
    [2023, 2024, 2025]
)

len(annual_revenue_test_2)


# In[400]:


annual_revenue_test_2


# In[401]:


def standardize_usd_thousands(annual_observations):
    return [
        {
            "year": int(item["frame"].replace("CY", "")),
            "value_usd_000": item["val"] / 1000
        }
        for item in annual_observations
    ]


# In[402]:


annual_revenue_standardized = standardize_usd_thousands(
    annual_revenue_test_2
)

annual_revenue_standardized


# In[403]:


def rename_standardized_metric(records, metric_name):
    return [
        {
            "year": record["year"],
            metric_name: record["value_usd_000"]
        }
        for record in records
    ]


# In[404]:


revenue_records_test = rename_standardized_metric(
    annual_revenue_standardized,
    "revenue_usd_000"
)

revenue_records_test


# In[405]:


revenue_df_test = pd.DataFrame(revenue_records_test)

revenue_df_test.equals(revenue_df)


# In[406]:


def filter_annual_observations_robust(observations, target_years):
    target_years = set(target_years)

    annual_records = []

    for item in observations:
        if item.get("form") != "10-K":
            continue

        if item.get("fp") != "FY":
            continue

        start = item.get("start")
        end = item.get("end")

        if not start or not end:
            continue

        start_year = int(start[:4])
        end_year = int(end[:4])

        if start_year != end_year:
            continue

        if start_year not in target_years:
            continue

        annual_records.append(item)

    return annual_records


# In[407]:


annual_net_income_test = filter_annual_observations_robust(
    net_income_data,
    [2023, 2024, 2025]
)

len(annual_net_income_test)


# In[408]:


annual_net_income_df_test = pd.DataFrame(annual_net_income_test)

annual_net_income_df_test["year"] = (
    pd.to_datetime(annual_net_income_df_test["start"]).dt.year
)

annual_net_income_df_test = (
    annual_net_income_df_test
    .sort_values("filed")
    .drop_duplicates(subset="year", keep="last")
)

annual_net_income_df_test[["year", "val", "filed"]]


# In[409]:


def keep_latest_filing_per_year(annual_observations):
    df = pd.DataFrame(annual_observations)

    df["year"] = pd.to_datetime(df["start"]).dt.year

    df = (
        df
        .sort_values("filed")
        .drop_duplicates(subset="year", keep="last")
    )

    return df


# In[410]:


annual_net_income_df_test_2 = keep_latest_filing_per_year(
    annual_net_income_test
)

annual_net_income_df_test_2[["year", "val", "filed"]]


# In[411]:


annual_ocf_test = filter_annual_observations_robust(
    ocf_data,
    [2023, 2024, 2025]
)

len(annual_ocf_test)


# In[412]:


annual_ocf_df_test = keep_latest_filing_per_year(
    annual_ocf_test
)

annual_ocf_df_test[["year", "val", "filed"]]


# In[413]:


def standardize_annual_usd_thousands(annual_df):
    return [
        {
            "year": int(row["year"]),
            "value_usd_000": row["val"] / 1000
        }
        for _, row in annual_df.iterrows()
    ]


# In[414]:


annual_ocf_standardized = standardize_annual_usd_thousands(
    annual_ocf_df_test
)

annual_ocf_standardized


# In[415]:


ocf_records_test = rename_standardized_metric(
    annual_ocf_standardized,
    "operating_cash_flow_usd_000"
)

ocf_records_test


# In[416]:


ocf_df_test = pd.DataFrame(ocf_records_test)

ocf_df_test.equals(operating_cash_flow_df)


# In[417]:


annual_revenue_test = filter_annual_observations_robust(
    revenue_data,
    [2023, 2024, 2025]
)

len(annual_revenue_test)


# In[418]:


annual_revenue_df_test = keep_latest_filing_per_year(
    annual_revenue_test
)

annual_revenue_df_test[["year", "val", "filed"]]


# In[419]:


annual_revenue_standardized = standardize_annual_usd_thousands(
    annual_revenue_df_test
)

annual_revenue_standardized


# In[420]:


revenue_records_test_robust = rename_standardized_metric(
    annual_revenue_standardized,
    "revenue_usd_000"
)

revenue_df_test_robust = pd.DataFrame(revenue_records_test_robust)

revenue_df_test_robust.equals(revenue_df)


# In[421]:


annual_gross_profit_test = filter_annual_observations_robust(
    gross_profit_data,
    [2023, 2024, 2025]
)

len(annual_gross_profit_test)


# In[422]:


annual_gross_profit_df_test = keep_latest_filing_per_year(
    annual_gross_profit_test
)

annual_gross_profit_df_test[["year", "val", "filed"]]


# In[423]:


annual_gross_profit_standardized = standardize_annual_usd_thousands(
    annual_gross_profit_df_test
)

annual_gross_profit_standardized


# In[424]:


gross_profit_records_test_robust = rename_standardized_metric(
    annual_gross_profit_standardized,
    "gross_profit_usd_000"
)

gross_profit_df_test_robust = pd.DataFrame(
    gross_profit_records_test_robust
)

gross_profit_df_test_robust.equals(gross_profit_df)


# In[425]:


annual_operating_income_test = filter_annual_observations_robust(
    operating_income_data,
    [2023, 2024, 2025]
)

len(annual_operating_income_test)


# In[426]:


annual_operating_income_df_test = keep_latest_filing_per_year(
    annual_operating_income_test
)

annual_operating_income_df_test[["year", "val", "filed"]]


# In[427]:


annual_operating_income_standardized = standardize_annual_usd_thousands(
    annual_operating_income_df_test
)

annual_operating_income_standardized


# In[428]:


operating_income_records_test_robust = rename_standardized_metric(
    annual_operating_income_standardized,
    "operating_income_usd_000"
)

operating_income_df_test_robust = pd.DataFrame(
    operating_income_records_test_robust
)

operating_income_df_test_robust.equals(operating_income_df)


# In[429]:


##Build the metric extraction function


# In[430]:


def extract_financial_metric(
    us_gaap,
    concept_name,
    target_years,
    metric_name
):
    concept = get_xbrl_concept(
        us_gaap,
        concept_name
    )

    observations = get_xbrl_units(
        concept,
        "USD"
    )

    annual_observations = filter_annual_observations_robust(
        observations,
        target_years
    )

    annual_df = keep_latest_filing_per_year(
        annual_observations
    )

    standardized_records = standardize_annual_usd_thousands(
        annual_df
    )

    metric_records = rename_standardized_metric(
        standardized_records,
        metric_name
    )

    return pd.DataFrame(metric_records)


# In[431]:


##Test Revenue


# In[432]:


revenue_df_function_test = extract_financial_metric(
    us_gaap=us_gaap,
    concept_name="RevenueFromContractWithCustomerExcludingAssessedTax",
    target_years=[2023, 2024, 2025],
    metric_name="revenue_usd_000"
)

revenue_df_function_test


# In[433]:


revenue_df_function_test.equals(revenue_df)


# In[434]:


##Test Gross Profit,Operating Income, Net income, and Operating Cash Flow


# In[435]:


gross_profit_df_function_test = extract_financial_metric(
    us_gaap=us_gaap,
    concept_name="GrossProfit",
    target_years=[2023, 2024, 2025],
    metric_name="gross_profit_usd_000"
)

gross_profit_df_function_test.equals(gross_profit_df)


# In[436]:


operating_income_df_function_test = extract_financial_metric(
    us_gaap=us_gaap,
    concept_name="OperatingIncomeLoss",
    target_years=[2023, 2024, 2025],
    metric_name="operating_income_usd_000"
)

operating_income_df_function_test.equals(operating_income_df)


# In[437]:


net_income_df_function_test = extract_financial_metric(
    us_gaap=us_gaap,
    concept_name="NetIncomeLoss",
    target_years=[2023, 2024, 2025],
    metric_name="net_income_usd_000"
)

net_income_df_function_test.equals(net_income_df)


# In[438]:


operating_cash_flow_df_function_test = extract_financial_metric(
    us_gaap=us_gaap,
    concept_name="NetCashProvidedByUsedInOperatingActivities",
    target_years=[2023, 2024, 2025],
    metric_name="operating_cash_flow_usd_000"
)

operating_cash_flow_df_function_test.equals(operating_cash_flow_df)


# In[439]:


metric_config = {
    "revenue": {
        "concept": "RevenueFromContractWithCustomerExcludingAssessedTax",
        "column": "revenue_usd_000"
    },
    "gross_profit": {
        "concept": "GrossProfit",
        "column": "gross_profit_usd_000"
    },
    "operating_income": {
        "concept": "OperatingIncomeLoss",
        "column": "operating_income_usd_000"
    },
    "net_income": {
        "concept": "NetIncomeLoss",
        "column": "net_income_usd_000"
    },
    "operating_cash_flow": {
        "concept": "NetCashProvidedByUsedInOperatingActivities",
        "column": "operating_cash_flow_usd_000"
    }
}


# In[440]:


metric_config


# In[441]:


revenue_config = metric_config["revenue"]

revenue_config


# In[442]:


revenue_from_config = extract_financial_metric(
    us_gaap=us_gaap,
    concept_name=revenue_config["concept"],
    target_years=[2023, 2024, 2025],
    metric_name=revenue_config["column"]
)

revenue_from_config.equals(revenue_df)


# In[443]:


##Next step: automate all 5 metrics


# In[444]:


financial_metric_dfs = {}

for metric_name, config in metric_config.items():
    financial_metric_dfs[metric_name] = extract_financial_metric(
        us_gaap=us_gaap,
        concept_name=config["concept"],
        target_years=[2023, 2024, 2025],
        metric_name=config["column"]
    )


# In[445]:


financial_metric_dfs.keys()


# In[446]:


validation_results = {
    "revenue": financial_metric_dfs["revenue"].equals(revenue_df),
    "gross_profit": financial_metric_dfs["gross_profit"].equals(gross_profit_df),
    "operating_income": financial_metric_dfs["operating_income"].equals(operating_income_df),
    "net_income": financial_metric_dfs["net_income"].equals(net_income_df),
    "operating_cash_flow": financial_metric_dfs["operating_cash_flow"].equals(operating_cash_flow_df)
}

validation_results


# In[447]:


financial_metric_dfs


# In[448]:


etsy_financial_base_function = financial_metric_dfs["revenue"].copy()

for metric_name in [
    "gross_profit",
    "operating_income",
    "net_income",
    "operating_cash_flow"
]:
    etsy_financial_base_function = etsy_financial_base_function.merge(
        financial_metric_dfs[metric_name],
        on="year",
        how="inner"
    )

etsy_financial_base_function = (
    etsy_financial_base_function
    .sort_values("year")
    .reset_index(drop=True)
)


# In[449]:


etsy_financial_base_function


# In[450]:


etsy_financial_base_function.equals(etsy_financial_base)


# In[451]:


def add_derived_metrics(financial_df):
    financial_df = financial_df.copy()

    financial_df["gross_margin_pct"] = (
        financial_df["gross_profit_usd_000"]
        / financial_df["revenue_usd_000"]
    ) * 100

    financial_df["operating_margin_pct"] = (
        financial_df["operating_income_usd_000"]
        / financial_df["revenue_usd_000"]
    ) * 100

    financial_df["net_margin_pct"] = (
        financial_df["net_income_usd_000"]
        / financial_df["revenue_usd_000"]
    ) * 100

    financial_df["cfo_margin_pct"] = (
        financial_df["operating_cash_flow_usd_000"]
        / financial_df["revenue_usd_000"]
    ) * 100

    financial_df["revenue_growth_pct"] = (
        financial_df["revenue_usd_000"]
        .pct_change() * 100
    )

    return financial_df


# In[452]:


etsy_financial_function = add_derived_metrics(
    etsy_financial_base_function
)

etsy_financial_function


# In[453]:


etsy_financial_function.equals(etsy_financial_df)


# In[454]:


##step — inspect the fiscal periods


# In[455]:


revenue_concept = get_xbrl_concept(
    us_gaap,
    "RevenueFromContractWithCustomerExcludingAssessedTax"
)

revenue_observations = get_xbrl_units(
    revenue_concept,
    "USD"
)

[
    {
        "start": item.get("start"),
        "end": item.get("end"),
        "form": item.get("form"),
        "fp": item.get("fp"),
        "filed": item.get("filed")
    }
    for item in revenue_observations
    if item.get("form") == "10-K"
]


# # Let's start with Crocs (CROX)

# In[460]:


crocs_config = company_config["CROX"]

crocs_facts = get_company_facts(
    crocs_config["cik"]
)

crocs_us_gaap = get_us_gaap_facts(
    crocs_facts
)


# In[461]:


##Step 1 — Inspect Crocs annual Revenue periods


# In[462]:


crocs_revenue_concept = get_xbrl_concept(
    crocs_us_gaap,
    "RevenueFromContractWithCustomerExcludingAssessedTax"
)

crocs_revenue_observations = get_xbrl_units(
    crocs_revenue_concept,
    "USD"
)

[
    {
        "start": item.get("start"),
        "end": item.get("end"),
        "form": item.get("form"),
        "fp": item.get("fp"),
        "fy": item.get("fy"),
        "filed": item.get("filed")
    }
    for item in crocs_revenue_observations
    if item.get("form") == "10-K"
]


# In[463]:


crocs_annual_revenue = filter_annual_observations_robust(
    crocs_revenue_observations,
    [2023, 2024, 2025]
)

len(crocs_annual_revenue)


# In[464]:


##Step 2 — Deduplicate Crocs annual observations


# In[465]:


crocs_annual_revenue_df = keep_latest_filing_per_year(
    crocs_annual_revenue
)

crocs_annual_revenue_df[
    ["year", "start", "end", "filed", "val"]
]


# In[466]:


##step: standardize Crocs revenue


# In[467]:


crocs_revenue_records = standardize_annual_usd_thousands(
    crocs_annual_revenue_df
)

crocs_revenue_df = rename_standardized_metric(
    crocs_revenue_records,
    "revenue_usd_000"
)

crocs_revenue_df


# In[468]:


##Step: validate the reusable metric function


# In[469]:


crocs_revenue_function = extract_financial_metric(
    us_gaap=crocs_us_gaap,
    concept_name=metric_config["revenue"]["concept"],
    target_years=[2023, 2024, 2025],
    metric_name=metric_config["revenue"]["column"]
)

crocs_revenue_function


# In[470]:


##step — extract all 5 Crocs metrics automatically


# In[471]:


crocs_financial_metric_dfs = {}

for metric_name, config in metric_config.items():
    crocs_financial_metric_dfs[metric_name] = extract_financial_metric(
        us_gaap=crocs_us_gaap,
        concept_name=config["concept"],
        target_years=[2023, 2024, 2025],
        metric_name=config["column"]
    )

crocs_financial_metric_dfs.keys()


# In[472]:


##step — quick structural QA


# In[473]:


{
    metric_name: df.shape
    for metric_name, df in crocs_financial_metric_dfs.items()
}


# In[474]:


#step — merge the five Crocs metrics


# In[475]:


crocs_financial_base = crocs_financial_metric_dfs["revenue"].copy()

for metric_name in [
    "gross_profit",
    "operating_income",
    "net_income",
    "operating_cash_flow"
]:
    crocs_financial_base = crocs_financial_base.merge(
        crocs_financial_metric_dfs[metric_name],
        on="year",
        how="inner"
    )

crocs_financial_base = (
    crocs_financial_base
    .sort_values("year")
    .reset_index(drop=True)
)

crocs_financial_base


# In[476]:


#step — apply our reusable derived-metrics function


# In[477]:


crocs_financial_df = add_derived_metrics(
    crocs_financial_base
)

crocs_financial_df


# In[478]:


#step — validate the Crocs output against the extraction logic


# In[479]:


crocs_financial_df.shape


# In[480]:


crocs_financial_df.dtypes


# In[481]:


crocs_financial_df.isna().sum()


# In[482]:


crocs_financial_df["year"].duplicated().sum()


# In[483]:


#QA: check the financial calculation relationships


# In[484]:


crocs_financial_df[
    [
        "year",
        "revenue_usd_000",
        "gross_profit_usd_000",
        "operating_income_usd_000"
    ]
]


# In[485]:


#step: validate the margin calculations


# In[486]:


crocs_financial_df[
    [
        "year",
        "gross_margin_pct",
        "operating_margin_pct",
        "net_margin_pct",
        "cfo_margin_pct"
    ]
]


# In[487]:


margin_check = (
    (crocs_financial_df["gross_profit_usd_000"] /
     crocs_financial_df["revenue_usd_000"] * 100)
    .round(6)
    .equals(crocs_financial_df["gross_margin_pct"].round(6))
)

margin_check


# In[488]:


growth_check = (
    crocs_financial_df["revenue_usd_000"]
    .pct_change()
    .mul(100)
    .round(6)
    .equals(
        crocs_financial_df["revenue_growth_pct"].round(6)
    )
)

growth_check


# # Next company: Shake Shack

# In[489]:


shak_config = company_config["SHAK"]

shak_facts = get_company_facts(
    shak_config["cik"]
)

shak_us_gaap = get_us_gaap_facts(
    shak_facts
)


# In[490]:


shak_revenue_concept = get_xbrl_concept(
    shak_us_gaap,
    "RevenueFromContractWithCustomerExcludingAssessedTax"
)

shak_revenue_observations = get_xbrl_units(
    shak_revenue_concept,
    "USD"
)


# In[491]:


#step: inspect recent 10-K periods


# In[492]:


[
    {
        "start": item.get("start"),
        "end": item.get("end"),
        "fy": item.get("fy"),
        "filed": item.get("filed"),
        "form": item.get("form")
    }
    for item in shak_revenue_observations
    if item.get("form") == "10-K"
    and item.get("start", "").startswith(("2023", "2024", "2025"))
]


# In[493]:


#We need to find the actual FY2023 full-year period for Shake Shack. The output we got didn't show it because its start date probably doesn't begin with 2023


# In[494]:


[
    {
        "start": item.get("start"),
        "end": item.get("end"),
        "fy": item.get("fy"),
        "filed": item.get("filed"),
        "form": item.get("form")
    }
    for item in shak_revenue_observations
    if item.get("form") == "10-K"
    and item.get("fy") in [2023, 2024, 2025]
]


# In[495]:


#step — test our current filter on Shake Shack


# In[496]:


shak_annual_revenue = filter_annual_observations_robust(
    shak_revenue_observations,
    [2023, 2024, 2025]
)

len(shak_annual_revenue)


# In[497]:


shak_annual_revenue


# In[498]:


[
    {
        "start": item.get("start"),
        "end": item.get("end"),
        "days": (
            pd.to_datetime(item["end"])
            - pd.to_datetime(item["start"])
        ).days,
        "fy": item.get("fy"),
        "filed": item.get("filed")
    }
    for item in shak_revenue_observations
    if item.get("form") == "10-K"
    and item.get("fy") in [2023, 2024, 2025]
]


# In[499]:


[
    item
    for item in shak_revenue_observations
    if item.get("form") == "10-K"
    and item.get("fp") == "FY"
    and item.get("start")
    and item.get("end")
    and (
        pd.to_datetime(item["end"])
        - pd.to_datetime(item["start"])
    ).days >= 300
]


# In[500]:


shak_annual_revenue_duration = [
    item
    for item in shak_revenue_observations
    if item.get("form") == "10-K"
    and item.get("fp") == "FY"
    and item.get("start")
    and item.get("end")
    and (
        pd.to_datetime(item["end"])
        - pd.to_datetime(item["start"])
    ).days >= 300
]

len(shak_annual_revenue_duration)


# In[501]:


[
    {
        "start": item["start"],
        "end": item["end"],
        "year": pd.to_datetime(item["end"]).year,
        "days": (
            pd.to_datetime(item["end"])
            - pd.to_datetime(item["start"])
        ).days,
        "val": item["val"],
        "fy": item.get("fy"),
        "filed": item["filed"]
    }
    for item in shak_annual_revenue_duration
    if pd.to_datetime(item["end"]).year in [2023, 2024, 2025]
]


# In[502]:


def filter_annual_observations_robust_v2(observations, target_years):
    target_years = set(target_years)

    annual_records = []

    for item in observations:
        if item.get("form") != "10-K":
            continue

        if item.get("fp") != "FY":
            continue

        start = item.get("start")
        end = item.get("end")

        if not start or not end:
            continue

        duration_days = (
            pd.to_datetime(end)
            - pd.to_datetime(start)
        ).days

        if duration_days < 300:
            continue

        end_year = pd.to_datetime(end).year

        if end_year not in target_years:
            continue

        annual_records.append(item)

    return annual_records


# In[503]:


shak_annual_revenue_v2 = filter_annual_observations_robust_v2(
    shak_revenue_observations,
    [2023, 2024, 2025]
)

len(shak_annual_revenue_v2)


# In[504]:


def keep_latest_filing_per_year_v2(annual_observations):
    df = pd.DataFrame(annual_observations)

    df["year"] = pd.to_datetime(df["end"]).dt.year

    df = (
        df
        .sort_values("filed")
        .drop_duplicates(subset="year", keep="last")
    )

    return df


# In[505]:


shak_latest_revenue_v2 = keep_latest_filing_per_year_v2(
    shak_annual_revenue_v2
)

shak_latest_revenue_v2[
    ["year", "start", "end", "val", "fy", "filed"]
]


# In[506]:


etsy_annual_revenue_v2 = filter_annual_observations_robust_v2(
    get_xbrl_units(
        get_xbrl_concept(
            us_gaap,
            "RevenueFromContractWithCustomerExcludingAssessedTax"
        ),
        "USD"
    ),
    [2023, 2024, 2025]
)

etsy_latest_revenue_v2 = keep_latest_filing_per_year_v2(
    etsy_annual_revenue_v2
)

etsy_latest_revenue_v2[
    ["year", "start", "end", "val", "filed"]
]


# In[507]:


def filter_annual_observations_robust(observations, target_years):
    target_years = set(target_years)

    annual_records = []

    for item in observations:
        if item.get("form") != "10-K":
            continue

        if item.get("fp") != "FY":
            continue

        start = item.get("start")
        end = item.get("end")

        if not start or not end:
            continue

        duration_days = (
            pd.to_datetime(end)
            - pd.to_datetime(start)
        ).days

        if duration_days < 300:
            continue

        end_year = pd.to_datetime(end).year

        if end_year not in target_years:
            continue

        annual_records.append(item)

    return annual_records


# In[508]:


def keep_latest_filing_per_year(annual_observations):
    df = pd.DataFrame(annual_observations)

    df["year"] = pd.to_datetime(df["end"]).dt.year

    df = (
        df
        .sort_values("filed")
        .drop_duplicates(subset="year", keep="last")
    )

    return df


# In[509]:


shak_revenue_df = extract_financial_metric(
    us_gaap=shak_us_gaap,
    concept_name="RevenueFromContractWithCustomerExcludingAssessedTax",
    target_years=[2023, 2024, 2025],
    metric_name="revenue_usd_000"
)

shak_revenue_df


# In[510]:


shak_financial_metric_dfs = {}

for metric_name, config in metric_config.items():
    shak_financial_metric_dfs[metric_name] = extract_financial_metric(
        us_gaap=shak_us_gaap,
        concept_name=config["concept"],
        target_years=[2023, 2024, 2025],
        metric_name=config["column"]
    )


# In[511]:


[
    concept
    for concept in shak_us_gaap.keys()
    if "Gross" in concept
]


# In[512]:


[
    concept
    for concept in shak_us_gaap.keys()
    if any(word in concept.lower() for word in [
        "revenue",
        "costofrevenue",
        "costofgoods",
        "costofsales"
    ])
]


# In[513]:


##Shake Shack does not have a GrossProfit concep


# In[514]:


for concept_name in [
    "CostOfGoodsSoldDirectLabor",
    "CostOfGoodsSoldDirectMaterials"
]:
    concept = get_xbrl_concept(
        shak_us_gaap,
        concept_name
    )

    units = get_xbrl_units(
        concept,
        "USD"
    )

    annual = filter_annual_observations_robust(
        units,
        [2023, 2024, 2025]
    )

    latest = keep_latest_filing_per_year(
        annual
    )

    print(f"\n{concept_name}")
    print(
        latest[
            ["year", "start", "end", "val", "filed"]
        ]
    )


# In[515]:


concept = get_xbrl_concept(
    shak_us_gaap,
    "CostOfGoodsSoldDirectLabor"
)

units = get_xbrl_units(
    concept,
    "USD"
)

units[:10]


# In[516]:


missing_end = [
    item
    for item in units
    if "end" not in item
]

print("Total USD observations:", len(units))
print("Observations missing 'end':", len(missing_end))

missing_end[:10]


# In[517]:


annual_labor = filter_annual_observations_robust(
    units,
    [2023, 2024, 2025]
)

print("Matching annual observations:", len(annual_labor))

annual_labor


# In[518]:


labor_df = pd.DataFrame(units)

labor_df["duration_days"] = (
    pd.to_datetime(labor_df["end"])
    - pd.to_datetime(labor_df["start"])
).dt.days

labor_df[
    ["start", "end", "duration_days", "val", "fy", "fp", "form", "filed"]
].tail(20)


# In[519]:


[
    concept
    for concept in shak_us_gaap.keys()
    if any(word in concept.lower() for word in [
        "cost",
        "expense",
        "labor",
        "material",
        "restaurant"
    ])
][:100]


# In[520]:


for concept_name in [
    "CostDirectLabor",
    "CostDirectMaterial"
]:
    concept = get_xbrl_concept(
        shak_us_gaap,
        concept_name
    )

    units = get_xbrl_units(
        concept,
        "USD"
    )

    recent = pd.DataFrame(units)

    recent["duration_days"] = (
        pd.to_datetime(recent["end"])
        - pd.to_datetime(recent["start"])
    ).dt.days

    print(f"\n{concept_name}")
    print(
        recent[
            [
                "start",
                "end",
                "duration_days",
                "val",
                "fy",
                "fp",
                "form",
                "filed"
            ]
        ].tail(15)
    )


# In[521]:


concept = get_xbrl_concept(
    shak_us_gaap,
    "OperatingExpenses"
)

units = get_xbrl_units(
    concept,
    "USD"
)

operating_expenses_df = pd.DataFrame(units)

operating_expenses_df["duration_days"] = (
    pd.to_datetime(operating_expenses_df["end"])
    - pd.to_datetime(operating_expenses_df["start"])
).dt.days

operating_expenses_df.tail(20)


# In[522]:


shak_facts["facts"].keys()


# In[523]:


[
    concept
    for concept in shak_us_gaap.keys()
    if any(word in concept.lower() for word in [
        "costofrevenue",
        "costofsales",
        "costofgoods",
        "restaurantcost",
        "restaurantoperating"
    ])
]


# In[524]:


#The ETL handles company-level XBRL taxonomy variation and preserves missing metrics rather than substituting unsupported estimates.


# In[525]:


shak_available_metric_config = {
    "revenue": metric_config["revenue"],
    "operating_income": metric_config["operating_income"],
    "net_income": metric_config["net_income"],
    "operating_cash_flow": metric_config["operating_cash_flow"]
}

shak_financial_metric_dfs = {}

for metric_name, config in shak_available_metric_config.items():
    shak_financial_metric_dfs[metric_name] = extract_financial_metric(
        us_gaap=shak_us_gaap,
        concept_name=config["concept"],
        target_years=[2023, 2024, 2025],
        metric_name=config["column"]
    )

shak_financial_metric_dfs


# In[526]:


shak_financial_base = shak_financial_metric_dfs["revenue"].copy()

for metric_name in [
    "operating_income",
    "net_income",
    "operating_cash_flow"
]:
    shak_financial_base = shak_financial_base.merge(
        shak_financial_metric_dfs[metric_name],
        on="year",
        how="inner"
    )

shak_financial_base = (
    shak_financial_base
    .sort_values("year")
    .reset_index(drop=True)
)

shak_financial_base


# #Next step: add derived metrics
# 
# Now we want to turn this base financial dataset into the analytical dataset, just as we did with Etsy.
# 
# For SHAK, we should calculate:
# 
# Operating margin %
# = Operating Income / Revenue × 100
# Net margin %
# = Net Income / Revenue × 100
# CFO margin %
# = Operating Cash Flow / Revenue × 100
# Revenue growth %
# = Current-year Revenue growth versus previous year
# 
# We will not calculate gross margin % because we don't have a reliable gross-profit value for SHAK from our current SEC/XBRL extraction.

# In[527]:


shak_financial_base["operating_margin_pct"] = (
    shak_financial_base["operating_income_usd_000"]
    / shak_financial_base["revenue_usd_000"]
    * 100
)

shak_financial_base["net_margin_pct"] = (
    shak_financial_base["net_income_usd_000"]
    / shak_financial_base["revenue_usd_000"]
    * 100
)

shak_financial_base["cfo_margin_pct"] = (
    shak_financial_base["operating_cash_flow_usd_000"]
    / shak_financial_base["revenue_usd_000"]
    * 100
)

shak_financial_base["revenue_growth_pct"] = (
    shak_financial_base["revenue_usd_000"]
    .pct_change()
    * 100
)

shak_financial_base


# In[528]:


shak_financial_base.dtypes


# In[529]:


def add_derived_metrics(df):
    df = df.copy()

    if {
        "operating_income_usd_000",
        "revenue_usd_000"
    }.issubset(df.columns):
        df["operating_margin_pct"] = (
            df["operating_income_usd_000"]
            / df["revenue_usd_000"]
            * 100
        )

    if {
        "net_income_usd_000",
        "revenue_usd_000"
    }.issubset(df.columns):
        df["net_margin_pct"] = (
            df["net_income_usd_000"]
            / df["revenue_usd_000"]
            * 100
        )

    if {
        "operating_cash_flow_usd_000",
        "revenue_usd_000"
    }.issubset(df.columns):
        df["cfo_margin_pct"] = (
            df["operating_cash_flow_usd_000"]
            / df["revenue_usd_000"]
            * 100
        )

    if "revenue_usd_000" in df.columns:
        df["revenue_growth_pct"] = (
            df["revenue_usd_000"]
            .pct_change()
            * 100
        )

    if {
        "gross_profit_usd_000",
        "revenue_usd_000"
    }.issubset(df.columns):
        df["gross_margin_pct"] = (
            df["gross_profit_usd_000"]
            / df["revenue_usd_000"]
            * 100
        )

    return df


# In[530]:


shak_financial_test = add_derived_metrics(shak_financial_base)

shak_financial_test


# In[531]:


shak_financial_base = add_derived_metrics(shak_financial_base)

shak_financial_base


# In[532]:


#Next Step is SHAK final QA


# In[533]:


shak_financial_base.isna().sum()


# In[534]:


shak_financial_base["year"].duplicated().sum()


# In[535]:


shak_financial_base["year"].tolist()


# In[536]:


(shak_financial_base["revenue_usd_000"] > 0).all()


# In[537]:


(
    (shak_financial_base["operating_margin_pct"]
     == shak_financial_base["operating_income_usd_000"]
     / shak_financial_base["revenue_usd_000"] * 100)
    &
    (shak_financial_base["net_margin_pct"]
     == shak_financial_base["net_income_usd_000"]
     / shak_financial_base["revenue_usd_000"] * 100)
    &
    (shak_financial_base["cfo_margin_pct"]
     == shak_financial_base["operating_cash_flow_usd_000"]
     / shak_financial_base["revenue_usd_000"] * 100)
).all()


# In[538]:


(
    shak_financial_base["revenue_growth_pct"].iloc[1:]
    .reset_index(drop=True)
    .equals(
        (
            shak_financial_base["revenue_usd_000"]
            .pct_change()
            .mul(100)
            .iloc[1:]
            .reset_index(drop=True)
        )
    )
)


# In[539]:


shak_financial_base.shape


# # Next company: CROX

# In[540]:


#Step 1 — Confirm CROX configuration


# In[541]:


company_config["CROX"]


# In[542]:


#Step 2 — Fetch CROX Company Facts


# In[543]:


crox_facts = get_company_facts(
    company_config["CROX"]["cik"]
)

type(crox_facts)


# In[544]:


#Step 3 — Inspect CROX revenue concepts


# In[ ]:





# In[545]:


us_gaap = crox_facts["facts"]["us-gaap"]

revenue_candidates = [
    key for key in us_gaap.keys()
    if "Revenue" in key or "Revenues" in key
]

revenue_candidates


# In[546]:


#Step 4 — Compare the two revenue candidates


# In[547]:


for concept in [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "SalesRevenueNet"
]:
    print(f"\n--- {concept} ---")
    
    concept_data = us_gaap[concept]["units"]
    
    for unit, records in concept_data.items():
        print(f"Unit: {unit}")
        print(records[-10:])


# In[548]:


#Step 5 — Extract CROX revenue


# In[549]:


[name for name, obj in globals().items() if callable(obj) and not name.startswith("_")]


# In[550]:


import inspect

print(inspect.signature(extract_financial_metric))


# In[551]:


crox_revenue_df = extract_financial_metric(
    us_gaap,
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    [2023, 2024, 2025],
    "revenue"
)

crox_revenue_df


# In[552]:


#Step 6 — validate the CROX revenue structure


# In[553]:


crox_revenue_df.dtypes


# In[554]:


#Step 7 — extract CROX Operating Income


# In[555]:


crox_operating_income_candidates = [
    key for key in us_gaap.keys()
    if "OperatingIncome" in key
]

crox_operating_income_candidates


# In[556]:


#Step 8 — inspect the actual CROX data


# In[557]:


for concept in [
    "OperatingIncomeLoss",
    "OtherOperatingIncomeExpenseNet"
]:
    print(f"\n--- {concept} ---")
    
    concept_data = us_gaap[concept]["units"]
    
    for unit, records in concept_data.items():
        print(f"Unit: {unit}")
        print(records[-10:])


# In[558]:


#Step 9 — extract CROX operating income


# In[559]:


crox_operating_income_df = extract_financial_metric(
    us_gaap,
    "OperatingIncomeLoss",
    [2023, 2024, 2025],
    "operating_income"
)

crox_operating_income_df


# Year	Operating Income (USD ‘000)
# 2023	1,036,783
# 2024	1,021,911
# 2025	149,515
# 
# However, before we accept these values, I want to pause because the FY2025 drop from ~$1.02B to ~$149.5M is substantial. This may be legitimate, but in an ETL project we should validate an unexpected financial change rather than blindly trust the extraction.
# 
# The important question is whether the 2023/2024 values are actually the correct annual operating-income observations selected by our current extraction logic.

# In[560]:


#Step 10 — inspect the extracted rows


# In[561]:


crox_operating_income_df


# In[562]:


records = us_gaap["OperatingIncomeLoss"]["units"]["USD"]

[
    r for r in records
    if r.get("form") == "10-K"
    and r.get("fp") == "FY"
    and r.get("fy") in [2023, 2024, 2025]
]


# In[563]:


crox_operating_income_2025 = [
    r for r in records
    if r.get("start") == "2025-01-01"
    and r.get("end") == "2025-12-31"
]

crox_operating_income_2025


# In[564]:


#Step 11 — extract CROX Net Income


# In[565]:


crox_net_income_candidates = [
    key for key in us_gaap.keys()
    if "NetIncome" in key
]

crox_net_income_candidates


# In[566]:


#Step 12 — inspect the annual records


# In[567]:


crox_net_income_records = us_gaap["NetIncomeLoss"]["units"]["USD"]

[
    r for r in crox_net_income_records
    if r.get("form") == "10-K"
    and r.get("fp") == "FY"
    and r.get("fy") in [2023, 2024, 2025]
]


# In[568]:


#Step 13 — extract CROX net income


# In[569]:


crox_net_income_df = extract_financial_metric(
    us_gaap,
    "NetIncomeLoss",
    [2023, 2024, 2025],
    "net_income"
)

crox_net_income_df


# In[570]:


#Step 14 — identify CROX Operating Cash Flow concept


# In[571]:


crox_ocf_candidates = [
    key for key in us_gaap.keys()
    if "NetCashProvidedByUsedInOperatingActivities" in key
]

crox_ocf_candidates


# In[572]:


#Step 15 — inspect the annual records


# In[573]:


crox_ocf_records = us_gaap["NetCashProvidedByUsedInOperatingActivities"]["units"]["USD"]

[
    r for r in crox_ocf_records
    if r.get("form") == "10-K"
    and r.get("fp") == "FY"
    and r.get("fy") in [2023, 2024, 2025]
]


# In[574]:


#Step 16 — extract CROX Operating Cash Flow


# In[575]:


crox_operating_cash_flow_df = extract_financial_metric(
    us_gaap,
    "NetCashProvidedByUsedInOperatingActivities",
    [2023, 2024, 2025],
    "operating_cash_flow"
)

crox_operating_cash_flow_df


# In[576]:


#Next Step is: CROX Gross Profit


# In[577]:


crox_gross_profit_candidates = [
    key for key in us_gaap.keys()
    if "GrossProfit" in key
]

crox_gross_profit_candidates


# In[578]:


crox_gross_profit_records = us_gaap["GrossProfit"]["units"]["USD"]

[
    r for r in crox_gross_profit_records
    if r.get("form") == "10-K"
    and r.get("fp") == "FY"
    and r.get("fy") in [2023, 2024, 2025]
]


# In[579]:


crox_gross_profit_df = extract_financial_metric(
    us_gaap,
    "GrossProfit",
    [2023, 2024, 2025],
    "gross_profit"
)

crox_gross_profit_df


# In[580]:


crox_financial_base = crox_revenue_df.copy()

for metric_df in [
    crox_gross_profit_df,
    crox_operating_income_df,
    crox_net_income_df,
    crox_operating_cash_flow_df
]:
    crox_financial_base = crox_financial_base.merge(
        metric_df,
        on="year",
        how="inner"
    )

crox_financial_base = (
    crox_financial_base
    .sort_values("year")
    .reset_index(drop=True)
)

crox_financial_base


# In[581]:


crox_financial_base = crox_financial_base.rename(
    columns={
        "revenue": "revenue_usd_000",
        "gross_profit": "gross_profit_usd_000",
        "operating_income": "operating_income_usd_000",
        "net_income": "net_income_usd_000",
        "operating_cash_flow": "operating_cash_flow_usd_000"
    }
)

crox_financial_base


# In[582]:


crox_financial_df = add_derived_metrics(crox_financial_base)

crox_financial_df


# In[583]:


#Next step is CROX QA


# In[584]:


crox_financial_df.isna().sum()


# In[585]:


crox_financial_df["year"].duplicated().sum()


# In[586]:


crox_financial_df["year"].tolist()


# In[587]:


(crox_financial_df["revenue_usd_000"] > 0).all()


# In[588]:


(
    (
        crox_financial_df["operating_income_usd_000"]
        / crox_financial_df["revenue_usd_000"]
        * 100
    )
    .round(6)
    .equals(
        crox_financial_df["operating_margin_pct"].round(6)
    )
)


# In[589]:


(
    (
        crox_financial_df["net_income_usd_000"]
        / crox_financial_df["revenue_usd_000"]
        * 100
    )
    .round(6)
    .equals(
        crox_financial_df["net_margin_pct"].round(6)
    )
)


# In[590]:


(
    (
        crox_financial_df["operating_cash_flow_usd_000"]
        / crox_financial_df["revenue_usd_000"]
        * 100
    )
    .round(6)
    .equals(
        crox_financial_df["cfo_margin_pct"].round(6)
    )
)


# In[591]:


(
    crox_financial_df["revenue_usd_000"]
    .pct_change()
    .mul(100)
    .round(6)
    .equals(
        crox_financial_df["revenue_growth_pct"].round(6)
    )
)


# In[592]:


crox_financial_df.shape


# # Next is BOOT

# In[593]:


#Step 1 — Confirm BOOT configuration


# In[594]:


company_config["BOOT"]


# In[595]:


#Step 2 — Load BOOT's SEC Company Facts


# In[602]:


boot_facts = get_company_facts(
    company_config["BOOT"]["cik"]
)

boot_us_gaap = boot_facts["facts"]["us-gaap"]

type(boot_us_gaap)


# In[603]:


#Step 2A — Diagnose before changing anything


# In[604]:


boot_cik = company_config["BOOT"]["cik"]

boot_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{boot_cik}.json"

print("CIK:", boot_cik)
print("URL:", boot_url)

boot_response = requests.get(
    boot_url,
    headers=headers
)

print("Status code:", boot_response.status_code)
print("Response:", boot_response.text[:500])


# In[605]:


#Step 3 — Correct the BOOT configuration


# In[606]:


company_config["BOOT"]["cik"] = "0001610250"

company_config["BOOT"]


# In[607]:


#Step 4 — Load BOOT Company Facts again


# In[608]:


boot_facts = get_company_facts(
    company_config["BOOT"]["cik"]
)

boot_us_gaap = boot_facts["facts"]["us-gaap"]

type(boot_us_gaap)


# In[609]:


#Step 5 — Discover BOOT Revenue concepts


# In[610]:


boot_revenue_candidates = [
    key for key in boot_us_gaap.keys()
    if "Revenue" in key or "Revenues" in key
]

boot_revenue_candidates


# In[611]:


boot_us_gaap["RevenueFromContractWithCustomerExcludingAssessedTax"]["units"]["USD"][-10:]


# In[612]:


boot_us_gaap["Revenues"]["units"]["USD"][-10:]


# In[613]:


boot_us_gaap["SalesRevenueGoodsNet"]["units"]["USD"][-10:]


# In[614]:


#Step 6 — Extract BOOT Revenue


# In[615]:


boot_revenue_df = extract_financial_metric(
    boot_us_gaap,
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    [2023, 2024, 2025],
    "revenue"
)

boot_revenue_df


# In[616]:


#Step 7 — Discover BOOT Gross Profit


# In[617]:


boot_gross_profit_candidates = [
    key for key in boot_us_gaap.keys()
    if "GrossProfit" in key
]

boot_gross_profit_candidates


# In[618]:


#Step 8 — Inspect BOOT Gross Profit records


# In[619]:


boot_us_gaap["GrossProfit"]["units"]["USD"][-15:]


# In[620]:


#Step 9 — Extract BOOT Gross Profit


# In[621]:


boot_gross_profit_df = extract_financial_metric(
    boot_us_gaap,
    "GrossProfit",
    [2023, 2024, 2025],
    "gross_profit"
)

boot_gross_profit_df


# In[622]:


#Step 10 — Discover BOOT Operating Income


# In[623]:


boot_operating_income_candidates = [
    key for key in boot_us_gaap.keys()
    if "OperatingIncome" in key
]

boot_operating_income_candidates


# In[624]:


boot_us_gaap["OperatingIncomeLoss"]["units"]["USD"][-15:]


# In[625]:


#Step 11 — Extract BOOT Operating Income


# In[626]:


boot_operating_income_df = extract_financial_metric(
    boot_us_gaap,
    "OperatingIncomeLoss",
    [2023, 2024, 2025],
    "operating_income"
)

boot_operating_income_df


# In[627]:


#Step 12 — Discover BOOT Net Income


# In[628]:


boot_net_income_candidates = [
    key for key in boot_us_gaap.keys()
    if "NetIncome" in key
]

boot_net_income_candidates


# In[629]:


boot_us_gaap["NetIncomeLoss"]["units"]["USD"][-15:]


# In[630]:


#Step 13 — Extract BOOT Net Income


# In[631]:


boot_net_income_df = extract_financial_metric(
    boot_us_gaap,
    "NetIncomeLoss",
    [2023, 2024, 2025],
    "net_income"
)

boot_net_income_df


# In[632]:


#Next is discover BOOT's OCF concepts


# In[633]:


boot_ocf_candidates = [
    key for key in boot_us_gaap.keys()
    if "NetCashProvidedByUsedInOperatingActivities" in key
]

boot_ocf_candidates


# In[634]:


for concept in boot_ocf_candidates:
    print("\nCONCEPT:", concept)
    print(boot_us_gaap[concept]["units"]["USD"][-15:])


# In[635]:


# step — extract BOOT OCF


# In[636]:


boot_operating_cash_flow_df = extract_financial_metric(
    boot_us_gaap,
    "NetCashProvidedByUsedInOperatingActivities",
    [2023, 2024, 2025],
    "operating_cash_flow"
)

boot_operating_cash_flow_df


# In[637]:


#Next step — merge the five raw metrics


# In[638]:


boot_financial_base = boot_revenue_df.copy()

for metric_df in [
    boot_gross_profit_df,
    boot_operating_income_df,
    boot_net_income_df,
    boot_operating_cash_flow_df
]:
    boot_financial_base = boot_financial_base.merge(
        metric_df,
        on="year",
        how="inner"
    )

boot_financial_base = (
    boot_financial_base
    .sort_values("year")
    .reset_index(drop=True)
)

boot_financial_base


# In[639]:


boot_financial_base = boot_financial_base.rename(
    columns={
        "revenue": "revenue_usd_000",
        "gross_profit": "gross_profit_usd_000",
        "operating_income": "operating_income_usd_000",
        "net_income": "net_income_usd_000",
        "operating_cash_flow": "operating_cash_flow_usd_000"
    }
)

boot_financial_base


# In[640]:


boot_financial_df = add_derived_metrics(
    boot_financial_base
)

boot_financial_df


# In[641]:


#Next step — BOOT QA


# In[642]:


boot_financial_df.isna().sum()


# In[643]:


boot_financial_df["year"].duplicated().sum()


# In[644]:


sorted(boot_financial_df["year"].tolist())


# In[645]:


(boot_financial_df["revenue_usd_000"] > 0).all()


# In[646]:


(
    boot_financial_df["gross_profit_usd_000"]
    / boot_financial_df["revenue_usd_000"]
    * 100
).round(6).equals(
    boot_financial_df["gross_margin_pct"].round(6)
)


# In[647]:


(
    boot_financial_df["operating_income_usd_000"]
    / boot_financial_df["revenue_usd_000"]
    * 100
).round(6).equals(
    boot_financial_df["operating_margin_pct"].round(6)
)


# In[648]:


(
    boot_financial_df["net_income_usd_000"]
    / boot_financial_df["revenue_usd_000"]
    * 100
).round(6).equals(
    boot_financial_df["net_margin_pct"].round(6)
)


# In[649]:


(
    boot_financial_df["operating_cash_flow_usd_000"]
    / boot_financial_df["revenue_usd_000"]
    * 100
).round(6).equals(
    boot_financial_df["cfo_margin_pct"].round(6)
)


# In[650]:


(
    boot_financial_df["revenue_usd_000"]
    .pct_change()
    * 100
).round(6).equals(
    boot_financial_df["revenue_growth_pct"].round(6)
)


# In[651]:


boot_financial_df.shape


# # Next company is Duolingo

# In[652]:


#Step 1 — Load DUOL's SEC Company Facts


# In[653]:


duolingo_facts = get_company_facts(
    company_config["DUOL"]["cik"]
)

type(duolingo_facts)


# In[654]:


#Step 2 — Access the US-GAAP facts


# In[655]:


duolingo_us_gaap = duolingo_facts["facts"]["us-gaap"]

type(duolingo_us_gaap)


# In[656]:


#Step 3 — Discover DUOL revenue concepts


# In[657]:


duolingo_revenue_candidates = [
    key for key in duolingo_us_gaap.keys()
    if "Revenue" in key or "Revenues" in key
]

duolingo_revenue_candidates


# In[658]:


#Step 4 — Inspect the revenue concept


# In[659]:


duolingo_us_gaap[
    "RevenueFromContractWithCustomerExcludingAssessedTax"
]["units"]["USD"][-15:]


# In[660]:


#Step 5 — Extract DUOL revenue


# In[661]:


duolingo_revenue_df = extract_financial_metric(
    duolingo_us_gaap,
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    [2023, 2024, 2025],
    "revenue"
)

duolingo_revenue_df


# In[662]:


#step 6 - Gross Profit concept


# In[663]:


duolingo_gross_profit_candidates = [
    key for key in duolingo_us_gaap.keys()
    if "GrossProfit" in key
]

duolingo_gross_profit_candidates


# In[664]:


duolingo_us_gaap[
    "GrossProfit"
]["units"]["USD"][-15:]


# In[665]:


#Step 6 — Extract Duolingo Gross Profit


# In[666]:


duolingo_gross_profit_df = extract_financial_metric(
    duolingo_us_gaap,
    "GrossProfit",
    [2023, 2024, 2025],
    "gross_profit"
)

duolingo_gross_profit_df


# In[667]:


#Step 7 — Find Operating Income concepts


# In[668]:


duolingo_operating_income_candidates = [
    key for key in duolingo_us_gaap.keys()
    if "OperatingIncome" in key
]

duolingo_operating_income_candidates


# In[669]:


duolingo_us_gaap[
    "OperatingIncomeLoss"
]["units"]["USD"][-15:]


# In[670]:


#Step 8 — Extract Duolingo Operating Income


# In[671]:


duolingo_operating_income_df = extract_financial_metric(
    duolingo_us_gaap,
    "OperatingIncomeLoss",
    [2023, 2024, 2025],
    "operating_income"
)

duolingo_operating_income_df


# In[672]:


#Step 9 — Find Net Income concepts


# In[673]:


duolingo_net_income_candidates = [
    key for key in duolingo_us_gaap.keys()
    if "NetIncomeLoss" in key
]

duolingo_net_income_candidates


# In[674]:


duolingo_us_gaap[
    "NetIncomeLoss"
]["units"]["USD"][-15:]


# In[675]:


duolingo_net_income_df = extract_financial_metric(
    duolingo_us_gaap,
    "NetIncomeLoss",
    [2023, 2024, 2025],
    "net_income"
)

duolingo_net_income_df


# In[676]:


#Step 10 — Find Operating Cash Flow concepts


# In[677]:


duolingo_ocf_candidates = [
    key for key in duolingo_us_gaap.keys()
    if "NetCashProvidedByUsedInOperatingActivities" in key
]

duolingo_ocf_candidates


# In[678]:


duolingo_us_gaap[
    "NetCashProvidedByUsedInOperatingActivities"
]["units"]["USD"][-15:]


# In[679]:


duolingo_operating_cash_flow_df = extract_financial_metric(
    duolingo_us_gaap,
    "NetCashProvidedByUsedInOperatingActivities",
    [2023, 2024, 2025],
    "operating_cash_flow"
)

duolingo_operating_cash_flow_df


# In[680]:


#Step 11 — Merge Duolingo's five raw metrics


# In[681]:


duolingo_financial_base = duolingo_revenue_df.copy()

for metric_name in [
    "gross_profit",
    "operating_income",
    "net_income",
    "operating_cash_flow"
]:
    duolingo_financial_base = duolingo_financial_base.merge(
        globals()[f"duolingo_{metric_name}_df"],
        on="year",
        how="inner"
    )

duolingo_financial_base = (
    duolingo_financial_base
    .sort_values("year")
    .reset_index(drop=True)
)

duolingo_financial_base


# In[682]:


duolingo_financial_df = duolingo_financial_base.rename(
    columns={
        "revenue": "revenue_usd_000",
        "gross_profit": "gross_profit_usd_000",
        "operating_income": "operating_income_usd_000",
        "net_income": "net_income_usd_000",
        "operating_cash_flow": "operating_cash_flow_usd_000"
    }
)

duolingo_financial_df


# In[683]:


duolingo_financial_df = add_derived_metrics(
    duolingo_financial_df
)

duolingo_financial_df


# In[684]:


#Duolingo QA check


# In[685]:


duolingo_financial_df.isna().sum()


# In[686]:


duolingo_financial_df["year"].duplicated().sum()


# In[687]:


sorted(duolingo_financial_df["year"].tolist())


# In[688]:


(duolingo_financial_df["revenue_usd_000"] > 0).all()


# In[689]:


(
    duolingo_financial_df["gross_profit_usd_000"]
    / duolingo_financial_df["revenue_usd_000"]
    * 100
).round(6).equals(
    duolingo_financial_df["gross_margin_pct"].round(6)
)


# In[690]:


(
    duolingo_financial_df["operating_income_usd_000"]
    / duolingo_financial_df["revenue_usd_000"]
    * 100
).round(6).equals(
    duolingo_financial_df["operating_margin_pct"].round(6)
)


# In[691]:


(
    duolingo_financial_df["net_income_usd_000"]
    / duolingo_financial_df["revenue_usd_000"]
    * 100
).round(6).equals(
    duolingo_financial_df["net_margin_pct"].round(6)
)


# In[692]:


(
    duolingo_financial_df["operating_cash_flow_usd_000"]
    / duolingo_financial_df["revenue_usd_000"]
    * 100
).round(6).equals(
    duolingo_financial_df["cfo_margin_pct"].round(6)
)


# In[693]:


(
    duolingo_financial_df["revenue_usd_000"]
    .pct_change()
    * 100
).round(6).equals(
    duolingo_financial_df["revenue_growth_pct"].round(6)
)


# In[694]:


duolingo_financial_df.shape


# In[695]:


etsy_financial_df = etsy_financial_df.copy()
etsy_financial_df["company"] = "ETSY"

etsy_financial_df


# In[696]:


[name for name in globals() if "shak" in name.lower()]


# In[697]:


shak_financial_base = shak_financial_base.copy()
shak_financial_base["company"] = "SHAK"

shak_financial_base


# In[698]:


[name for name in globals() if "crox" in name.lower()]


# In[699]:


crox_financial_df = crox_financial_df.copy()
crox_financial_df["company"] = "CROX"

crox_financial_df


# In[700]:


[name for name in globals() if "boot" in name.lower()]


# In[701]:


boot_financial_df = boot_financial_df.copy()
boot_financial_df["company"] = "BOOT"

boot_financial_df


# In[702]:


duolingo_financial_df = duolingo_financial_df.copy()
duolingo_financial_df["company"] = "DUOL"

duolingo_financial_df


# # Consolidate the five company datasets

# In[703]:


consolidated_financial_df = pd.concat(
    [
        etsy_financial_df,
        shak_financial_base,
        crox_financial_df,
        boot_financial_df,
        duolingo_financial_df
    ],
    ignore_index=True,
    sort=False
)

consolidated_financial_df


# In[704]:


consolidated_financial_df["company"].value_counts()


# In[705]:


#QA check for all companies 


# In[706]:


consolidated_financial_df.duplicated(
    subset=["company", "year"]
).sum()


# In[707]:


consolidated_financial_df.shape


# In[708]:


consolidated_financial_df.isna().sum()


# In[709]:


(consolidated_financial_df["revenue_usd_000"] > 0).all()


# In[710]:


consolidated_financial_df.groupby("company")["year"].agg(["min", "max", "count"])


# In[711]:


consolidated_financial_df.dtypes


# In[712]:


sorted(consolidated_financial_df["company"].unique())


# # Next phase: Financial Intelligence

# In[713]:


#Step 1 — Recalculate revenue growth independently


# In[714]:


revenue_growth_check = (
    consolidated_financial_df
    .sort_values(["company", "year"])
    .groupby("company")["revenue_usd_000"]
    .pct_change()
    * 100
)

revenue_growth_check


# In[715]:


#Step 2 — Let's make the validation explicit


# In[716]:


growth_match = (
    revenue_growth_check.reset_index(drop=True)
    .equals(
        consolidated_financial_df
        .sort_values(["company", "year"])["revenue_growth_pct"]
        .reset_index(drop=True)
    )
)

growth_match


# In[717]:


#Step 3 — Create our first analytical view


# In[718]:


revenue_growth_analysis = (
    consolidated_financial_df[
        ["company", "year", "revenue_usd_000", "revenue_growth_pct"]
    ]
    .sort_values(["company", "year"])
    .reset_index(drop=True)
)

revenue_growth_analysis


# In[719]:


#Step 4 — Build the profitability analysis view


# In[720]:


profitability_analysis = (
    consolidated_financial_df[
        [
            "company",
            "year",
            "gross_margin_pct",
            "operating_margin_pct",
            "net_margin_pct"
        ]
    ]
    .sort_values(["company", "year"])
    .reset_index(drop=True)
)

profitability_analysis


# In[721]:


#Step 5 — Add operating cash-flow strength


# In[722]:


cash_flow_analysis = (
    consolidated_financial_df[
        [
            "company",
            "year",
            "operating_cash_flow_usd_000",
            "cfo_margin_pct"
        ]
    ]
    .sort_values(["company", "year"])
    .reset_index(drop=True)
)

cash_flow_analysis


# In[723]:


#Step 6 — Let's create the portfolio-level summary


# In[724]:


latest_year_df = (
    consolidated_financial_df[
        consolidated_financial_df["year"] == 2025
    ]
    .sort_values("company")
    .reset_index(drop=True)
)

latest_year_df


# In[725]:


#Step 7 — Calculate the change from FY2023 → FY2025


# In[726]:


operating_margin_trend = (
    consolidated_financial_df
    .sort_values(["company", "year"])
    .groupby("company")
    .agg(
        operating_margin_2023=("operating_margin_pct", "first"),
        operating_margin_2025=("operating_margin_pct", "last")
    )
    .reset_index()
)

operating_margin_trend["operating_margin_change_pct_points"] = (
    operating_margin_trend["operating_margin_2025"]
    - operating_margin_trend["operating_margin_2023"]
)

operating_margin_trend


# # Important analytical observations
# DUOL: operating margin moved from negative to positive, a 15.56 percentage-point improvement.
# SHAK: operating margin also improved, by 3.78 percentage points.
# BOOT: relatively small decline of 1.46 percentage points.
# ETSY: relatively small decline of 0.95 percentage points.
# CROX: much larger decline of 22.47 percentage points, which reinforces the FY2025 profitability change we already observed.
# 
# Notice how we're not saying which company is the "best." We're building measurable evidence that can later feed into a transparent target-selection framework.

# In[727]:


#Step 8 — Check the calculation independently


# In[728]:


operating_margin_check = (
    consolidated_financial_df
    .sort_values(["company", "year"])
    .groupby("company")["operating_margin_pct"]
    .agg(["first", "last"])
)

operating_margin_check["calculated_change"] = (
    operating_margin_check["last"]
    - operating_margin_check["first"]
)

operating_margin_check


# In[729]:


#Step 9 — Let's examine net-margin trajectory


# In[730]:


net_margin_trend = (
    consolidated_financial_df
    .sort_values(["company", "year"])
    .groupby("company")
    .agg(
        net_margin_2023=("net_margin_pct", "first"),
        net_margin_2025=("net_margin_pct", "last")
    )
    .reset_index()
)

net_margin_trend["net_margin_change_pct_points"] = (
    net_margin_trend["net_margin_2025"]
    - net_margin_trend["net_margin_2023"]
)

net_margin_trend


# In[731]:


#Step 10 — Validate the net-margin trajectory


# In[732]:


net_margin_check = (
    consolidated_financial_df
    .sort_values(["company", "year"])
    .groupby("company")["net_margin_pct"]
    .agg(["first", "last"])
)

net_margin_check["calculated_change"] = (
    net_margin_check["last"]
    - net_margin_check["first"]
)

net_margin_check


# In[733]:


#Step 11 — Let's calculate CFO-margin trajectory


# In[734]:


cfo_margin_trend = (
    consolidated_financial_df
    .sort_values(["company", "year"])
    .groupby("company")
    .agg(
        cfo_margin_2023=("cfo_margin_pct", "first"),
        cfo_margin_2025=("cfo_margin_pct", "last")
    )
    .reset_index()
)

cfo_margin_trend["cfo_margin_change_pct_points"] = (
    cfo_margin_trend["cfo_margin_2025"]
    - cfo_margin_trend["cfo_margin_2023"]
)

cfo_margin_trend


# # The important analytical picture
# 
# Now we're seeing something more interesting than simply "profit went up/down":
# 
# BOOT: operating margin declined modestly, while CFO margin increased.
# CROX: both operating margin and CFO margin declined substantially.
# DUOL: both operating margin and CFO margin increased substantially.
# ETSY: both operating margin and CFO margin declined, although the CFO-margin decline was relatively smaller.
# SHAK: both operating margin and CFO margin increased.
# 
# This is exactly why we needed multiple dimensions. Profitability and cash generation can move differently, and that difference itself is informative.

# In[735]:


#Step 12 — Validate CFO-margin trajectory


# In[736]:


cfo_margin_check = (
    consolidated_financial_df
    .sort_values(["company", "year"])
    .groupby("company")["cfo_margin_pct"]
    .agg(["first", "last"])
)

cfo_margin_check["calculated_change"] = (
    cfo_margin_check["last"]
    - cfo_margin_check["first"]
)

cfo_margin_check


# In[737]:


#Step 13 — Create a revenue-scale summary


# In[738]:


revenue_scale_trend = (
    consolidated_financial_df
    .sort_values(["company", "year"])
    .groupby("company")
    .agg(
        revenue_2023=("revenue_usd_000", "first"),
        revenue_2025=("revenue_usd_000", "last")
    )
    .reset_index()
)

revenue_scale_trend["revenue_change_usd_000"] = (
    revenue_scale_trend["revenue_2025"]
    - revenue_scale_trend["revenue_2023"]
)

revenue_scale_trend


# In[739]:


gross_margin_trend = (
    consolidated_financial_df
    .sort_values(["company", "year"])
    .groupby("company")
    .agg(
        gross_margin_2023=("gross_margin_pct", "first"),
        gross_margin_2025=("gross_margin_pct", "last")
    )
    .reset_index()
)

gross_margin_trend["gross_margin_change_pct_points"] = (
    gross_margin_trend["gross_margin_2025"]
    - gross_margin_trend["gross_margin_2023"]
)

gross_margin_trend


# In[740]:


#Step 14 — Build the Financial Intelligence Summary


# In[741]:


financial_intelligence_df = (
    latest_year_df[
        [
            "company",
            "revenue_usd_000",
            "gross_margin_pct",
            "operating_margin_pct",
            "net_margin_pct",
            "operating_cash_flow_usd_000",
            "cfo_margin_pct",
            "revenue_growth_pct"
        ]
    ]
    .merge(
        revenue_scale_trend[
            [
                "company",
                "revenue_2023",
                "revenue_change_usd_000"
            ]
        ],
        on="company",
        how="left"
    )
    .merge(
        gross_margin_trend[
            [
                "company",
                "gross_margin_change_pct_points"
            ]
        ],
        on="company",
        how="left"
    )
    .merge(
        operating_margin_trend[
            [
                "company",
                "operating_margin_change_pct_points"
            ]
        ],
        on="company",
        how="left"
    )
    .merge(
        net_margin_trend[
            [
                "company",
                "net_margin_change_pct_points"
            ]
        ],
        on="company",
        how="left"
    )
    .merge(
        cfo_margin_trend[
            [
                "company",
                "cfo_margin_change_pct_points"
            ]
        ],
        on="company",
        how="left"
    )
)

financial_intelligence_df


# In[742]:


#Step 15 — Validate the intelligence layer


# In[743]:


print("Shape:", financial_intelligence_df.shape)

print("\nCompany count:")
print(financial_intelligence_df["company"].nunique())

print("\nDuplicate companies:")
print(financial_intelligence_df["company"].duplicated().sum())

print("\nMissing values:")
print(financial_intelligence_df.isna().sum())


# In[744]:


#Next step: create a company-level trend view


# In[745]:


company_trend_summary = (
    financial_intelligence_df[
        [
            "company",
            "revenue_2023",
            "revenue_usd_000",
            "revenue_growth_pct",
            "gross_margin_change_pct_points",
            "operating_margin_change_pct_points",
            "net_margin_change_pct_points",
            "cfo_margin_change_pct_points"
        ]
    ]
    .sort_values("company")
    .reset_index(drop=True)
)

company_trend_summary


# # We can now clearly see several different financial patterns:
# 
# Company	FY2025 revenue growth	Op. margin change	Net margin change	CFO margin change
# BOOT	14.64%	-1.46 pp	-0.82 pp	+2.36 pp
# CROX	-1.50%	-22.47 pp	-22.01 pp	-5.90 pp
# DUOL	38.71%	+15.56 pp	+36.88 pp	+8.45 pp
# ETSY	2.68%	-0.95 pp	-5.54 pp	-1.62 pp
# SHAK	15.38%	+3.78 pp	+1.30 pp	+3.23 pp
# 
# A few things are particularly important for our project:
# 
# DUOL shows strong revenue expansion alongside substantial improvement in operating, net, and CFO margins.
# CROX shows a very different pattern: gross margin improved, but operating and net margins declined sharply. This tells us that gross margin alone cannot explain overall profitability.
# BOOT has moderate revenue expansion, with operating margin slightly lower but CFO margin higher.
# ETSY has relatively modest revenue growth and deterioration in operating, net, and CFO margins despite gross-margin improvement.
# SHAK shows revenue growth and improvement in the available profitability/cash-flow measures, while gross-margin analysis remains unavailable.
# 
# These are descriptive observations, not yet a target-selection ranking.

# In[746]:


#Next: quantify revenue expansion


# In[747]:


revenue_scale_trend["revenue_growth_2023_to_2025_pct"] = (
    (
        revenue_scale_trend["revenue_2025"]
        - revenue_scale_trend["revenue_2023"]
    )
    / revenue_scale_trend["revenue_2023"]
    * 100
)

revenue_scale_trend


# In[748]:


#Next step: create a financial trend matrix


# In[749]:


financial_trend_matrix = (
    revenue_scale_trend[
        [
            "company",
            "revenue_growth_2023_to_2025_pct"
        ]
    ]
    .merge(
        gross_margin_trend[
            [
                "company",
                "gross_margin_change_pct_points"
            ]
        ],
        on="company",
        how="left"
    )
    .merge(
        operating_margin_trend[
            [
                "company",
                "operating_margin_change_pct_points"
            ]
        ],
        on="company",
        how="left"
    )
    .merge(
        net_margin_trend[
            [
                "company",
                "net_margin_change_pct_points"
            ]
        ],
        on="company",
        how="left"
    )
    .merge(
        cfo_margin_trend[
            [
                "company",
                "cfo_margin_change_pct_points"
            ]
        ],
        on="company",
        how="left"
    )
    .sort_values("company")
    .reset_index(drop=True)
)

financial_trend_matrix


# ## The matrix shows why a serious investment-screening model needs multiple dimensions:
# 
# BOOT: revenue expanded 15.29%; operating margin declined slightly, while CFO margin improved.
# CROX: revenue was almost flat (+1.98%) and operating/net/CFO margins deteriorated substantially, despite gross-margin improvement.
# DUOL: revenue expanded 95.36%, with strong improvements in operating, net, and CFO margins, while gross margin declined slightly.
# ETSY: revenue expanded 4.92%, but operating, net, and CFO margins declined.
# SHAK: revenue expanded 32.90%, with improvement in the available operating, net, and CFO margins; gross-margin data remains unavailable.

# In[750]:


#Next analytical dimension: earnings quality


# In[751]:


earnings_quality_analysis = (
    consolidated_financial_df[
        [
            "company",
            "year",
            "net_income_usd_000",
            "operating_cash_flow_usd_000"
        ]
    ]
    .sort_values(["company", "year"])
    .reset_index(drop=True)
)

earnings_quality_analysis["cfo_to_net_income_ratio"] = (
    earnings_quality_analysis["operating_cash_flow_usd_000"]
    / earnings_quality_analysis["net_income_usd_000"]
)

earnings_quality_analysis


# In[752]:


earnings_quality_analysis["cfo_to_net_income_interpretation"] = (
    earnings_quality_analysis["net_income_usd_000"]
    .apply(
        lambda x: (
            "Negative net income"
            if x < 0
            else "Positive net income"
        )
    )
)

earnings_quality_analysis


# In[753]:


earnings_quality_analysis["cash_conversion_pct"] = (
    earnings_quality_analysis["cfo_to_net_income_ratio"]
    .where(
        earnings_quality_analysis["net_income_usd_000"] > 0
    )
    * 100
)

earnings_quality_analysis


# In[754]:


latest_earnings_quality = (
    earnings_quality_analysis[
        earnings_quality_analysis["year"] == 2025
    ][
        [
            "company",
            "net_income_usd_000",
            "operating_cash_flow_usd_000",
            "cfo_to_net_income_ratio",
            "cash_conversion_pct",
            "cfo_to_net_income_interpretation"
        ]
    ]
    .sort_values("company")
    .reset_index(drop=True)
)

latest_earnings_quality


# # Next: identify persistent financial patterns

# In[755]:


financial_trend_direction = financial_trend_matrix.copy()

trend_columns = [
    "revenue_growth_2023_to_2025_pct",
    "gross_margin_change_pct_points",
    "operating_margin_change_pct_points",
    "net_margin_change_pct_points",
    "cfo_margin_change_pct_points"
]

for col in trend_columns:
    financial_trend_direction[col + "_direction"] = (
        financial_trend_direction[col]
        .apply(
            lambda x: (
                1 if x > 0
                else -1 if x < 0
                else 0
            ) if pd.notna(x) else pd.NA
        )
    )

financial_trend_direction


# In[756]:


#Next step: build a financial profile for FY2025


# In[757]:


financial_profile_df = (
    financial_intelligence_df
    .merge(
        revenue_scale_trend[
            [
                "company",
                "revenue_growth_2023_to_2025_pct"
            ]
        ],
        on="company",
        how="left"
    )
    .sort_values("company")
    .reset_index(drop=True)
)

financial_profile_df


# In[758]:


financial_snapshot_df = (
    financial_profile_df[
        [
            "company",
            "revenue_usd_000",
            "revenue_growth_pct",
            "gross_margin_pct",
            "operating_margin_pct",
            "net_margin_pct",
            "operating_cash_flow_usd_000",
            "cfo_margin_pct"
        ]
    ]
    .sort_values("company")
    .reset_index(drop=True)
)

financial_snapshot_df


# In[759]:


#Next: measure operating leverage


# In[760]:


operating_income_trend = (
    consolidated_financial_df
    .sort_values(["company", "year"])
    .groupby("company")
    .agg(
        operating_income_2023=("operating_income_usd_000", "first"),
        operating_income_2025=("operating_income_usd_000", "last")
    )
    .reset_index()
)

operating_income_trend["operating_income_growth_2023_to_2025_pct"] = (
    (
        operating_income_trend["operating_income_2025"]
        - operating_income_trend["operating_income_2023"]
    )
    / operating_income_trend["operating_income_2023"]
    * 100
)

operating_income_trend


# In[761]:


operating_income_trend["operating_income_change_usd_000"] = (
    operating_income_trend["operating_income_2025"]
    - operating_income_trend["operating_income_2023"]
)

operating_income_trend


# In[762]:


#Next step — let's create a cleaner operating-income diagnostic


# In[763]:


operating_income_trend["operating_income_change_usd_mn"] = (
    operating_income_trend["operating_income_change_usd_000"] / 1000
)

operating_income_trend


# In[764]:


#Next: let's look at operating-income trajectory year by year


# In[765]:


operating_income_analysis = (
    consolidated_financial_df[
        [
            "company",
            "year",
            "operating_income_usd_000",
            "operating_margin_pct"
        ]
    ]
    .sort_values(["company", "year"])
    .reset_index(drop=True)
)

operating_income_analysis


# In[766]:


operating_income_analysis["operating_income_yoy_change_usd_000"] = (
    operating_income_analysis
    .groupby("company")["operating_income_usd_000"]
    .diff()
)

operating_income_analysis


# In[767]:


operating_income_trend_summary = (
    operating_income_analysis
    .groupby("company")
    .agg(
        operating_income_2023=("operating_income_usd_000", "first"),
        operating_income_2025=("operating_income_usd_000", "last"),
        operating_income_change_2023_to_2025=("operating_income_usd_000", lambda x: x.iloc[-1] - x.iloc[0]),
        operating_income_yoy_change_2024=("operating_income_yoy_change_usd_000", "first"),
        operating_income_yoy_change_2025=("operating_income_yoy_change_usd_000", "last"),
        operating_margin_2023=("operating_margin_pct", "first"),
        operating_margin_2025=("operating_margin_pct", "last")
    )
    .reset_index()
)

operating_income_trend_summary["operating_margin_change_pct_points"] = (
    operating_income_trend_summary["operating_margin_2025"]
    - operating_income_trend_summary["operating_margin_2023"]
)

operating_income_trend_summary


# In[768]:


#Next analytical dimension: net income trajectory


# In[769]:


net_income_analysis = (
    consolidated_financial_df[
        [
            "company",
            "year",
            "net_income_usd_000",
            "net_margin_pct"
        ]
    ]
    .sort_values(["company", "year"])
    .reset_index(drop=True)
)

net_income_analysis


# In[770]:


#Next step: calculate year-over-year absolute net-income changes


# In[771]:


net_income_analysis["net_income_yoy_change_usd_000"] = (
    net_income_analysis
    .groupby("company")["net_income_usd_000"]
    .diff()
)

net_income_analysis


# #Two particularly important cases
# 
# CROX:
# The 2025 net-income decline of $1.031 billion moved net income from +$950.071M to −$81.198M. This is a much more informative observation than trying to calculate a percentage growth rate from a positive number to a negative number.
# 
# DUOL:
# Net income increased by $72.507M in 2024 and another $325.491M in 2025. Its net margin moved from 3.03% → 11.84% → 39.91%. This is a strong example of why we want both absolute changes and margin trajectories.

# In[772]:


net_income_trend_summary = (
    net_income_analysis
    .groupby("company")
    .agg(
        net_income_2023=("net_income_usd_000", "first"),
        net_income_2025=("net_income_usd_000", "last"),
        net_income_change_2023_to_2025=(
            "net_income_usd_000",
            lambda x: x.iloc[-1] - x.iloc[0]
        ),
        net_income_yoy_change_2024=(
            "net_income_yoy_change_usd_000",
            "first"
        ),
        net_income_yoy_change_2025=(
            "net_income_yoy_change_usd_000",
            "last"
        ),
        net_margin_2023=("net_margin_pct", "first"),
        net_margin_2025=("net_margin_pct", "last")
    )
    .reset_index()
)

net_income_trend_summary["net_margin_change_pct_points"] = (
    net_income_trend_summary["net_margin_2025"]
    - net_income_trend_summary["net_margin_2023"]
)

net_income_trend_summary


# #A particularly important observation is CROX: net income went from +$792.566M in 2023 to -$81.198M in 2025, a change of -$873.764M. This is exactly why we avoided using a simple percentage-growth feature for net income.
# 
# Similarly, DUOL moved from $16.067M to $414.065M, while its net margin increased from 3.03% to 39.91%.
# 
# One important distinction
# 
# For the portfolio, we should not turn these into scores or rankings yet.
# 
# We're building the financial intelligence layer first:
# 
# Net income → YoY movement → absolute change → margin trajectory → interpretation
# 
# That gives us an auditable analytical trail that we can later use when defining the target-screening framework.

# In[773]:


#Next step: Cash-flow trajectory


# In[774]:


cash_flow_trend = (
    consolidated_financial_df
    .sort_values(["company", "year"])
    .groupby("company")
    .agg(
        operating_cash_flow_2023=(
            "operating_cash_flow_usd_000",
            "first"
        ),
        operating_cash_flow_2025=(
            "operating_cash_flow_usd_000",
            "last"
        )
    )
    .reset_index()
)

cash_flow_trend["operating_cash_flow_change_2023_to_2025"] = (
    cash_flow_trend["operating_cash_flow_2025"]
    - cash_flow_trend["operating_cash_flow_2023"]
)

cash_flow_trend["operating_cash_flow_change_usd_mn"] = (
    cash_flow_trend["operating_cash_flow_change_2023_to_2025"]
    / 1000
)

cash_flow_trend


# In[775]:


#Next step: year-over-year cash-flow movement


# In[776]:


cash_flow_analysis = (
    consolidated_financial_df[
        [
            "company",
            "year",
            "operating_cash_flow_usd_000",
            "cfo_margin_pct"
        ]
    ]
    .sort_values(["company", "year"])
    .reset_index(drop=True)
)

cash_flow_analysis["operating_cash_flow_yoy_change_usd_000"] = (
    cash_flow_analysis
    .groupby("company")["operating_cash_flow_usd_000"]
    .diff()
)

cash_flow_analysis


# In[777]:


cash_flow_trend_summary = (
    cash_flow_analysis
    .groupby("company")
    .agg(
        operating_cash_flow_2023=(
            "operating_cash_flow_usd_000",
            "first"
        ),
        operating_cash_flow_2025=(
            "operating_cash_flow_usd_000",
            "last"
        ),
        operating_cash_flow_change_2023_to_2025=(
            "operating_cash_flow_usd_000",
            lambda x: x.iloc[-1] - x.iloc[0]
        ),
        operating_cash_flow_yoy_change_2024=(
            "operating_cash_flow_yoy_change_usd_000",
            "first"
        ),
        operating_cash_flow_yoy_change_2025=(
            "operating_cash_flow_yoy_change_usd_000",
            "last"
        ),
        cfo_margin_2023=(
            "cfo_margin_pct",
            "first"
        ),
        cfo_margin_2025=(
            "cfo_margin_pct",
            "last"
        )
    )
    .reset_index()
)

cash_flow_trend_summary["cfo_margin_change_pct_points"] = (
    cash_flow_trend_summary["cfo_margin_2025"]
    - cash_flow_trend_summary["cfo_margin_2023"]
)

cash_flow_trend_summary


# In[778]:


#Next analytical question : How consistently does operating cash flow support reported net income?


# In[779]:


earnings_quality_trend_summary = (
    earnings_quality_analysis
    .sort_values(["company", "year"])
    .groupby("company")
    .agg(
        cfo_to_net_income_2023=(
            "cfo_to_net_income_ratio",
            "first"
        ),
        cfo_to_net_income_2025=(
            "cfo_to_net_income_ratio",
            "last"
        ),
        cash_conversion_2023=(
            "cash_conversion_pct",
            "first"
        ),
        cash_conversion_2025=(
            "cash_conversion_pct",
            "last"
        )
    )
    .reset_index()
)

earnings_quality_trend_summary


# In[780]:


earnings_cashflow_alignment = (
    consolidated_financial_df[
        [
            "company",
            "year",
            "net_income_usd_000",
            "operating_cash_flow_usd_000"
        ]
    ]
    .sort_values(["company", "year"])
    .reset_index(drop=True)
)

earnings_cashflow_alignment["net_income_yoy_change_usd_000"] = (
    earnings_cashflow_alignment
    .groupby("company")["net_income_usd_000"]
    .diff()
)

earnings_cashflow_alignment["operating_cash_flow_yoy_change_usd_000"] = (
    earnings_cashflow_alignment
    .groupby("company")["operating_cash_flow_usd_000"]
    .diff()
)

earnings_cashflow_alignment


# In[781]:


def classify_earnings_cashflow_alignment(row):
    if pd.isna(row["net_income_yoy_change_usd_000"]):
        return "Baseline"

    net_income_change = row["net_income_yoy_change_usd_000"]
    cash_flow_change = row["operating_cash_flow_yoy_change_usd_000"]

    if net_income_change > 0 and cash_flow_change > 0:
        return "Aligned positive"

    elif net_income_change < 0 and cash_flow_change < 0:
        return "Aligned negative"

    else:
        return "Divergent"


earnings_cashflow_alignment["earnings_cashflow_alignment"] = (
    earnings_cashflow_alignment.apply(
        classify_earnings_cashflow_alignment,
        axis=1
    )
)

earnings_cashflow_alignment


# In[782]:


#Next step: summarize the alignment pattern


# In[783]:


earnings_cashflow_alignment_summary = (
    earnings_cashflow_alignment[
        earnings_cashflow_alignment["year"] != 2023
    ]
    .groupby(["company", "earnings_cashflow_alignment"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

earnings_cashflow_alignment_summary


# In[784]:


revenue_growth_trajectory = (
    revenue_growth_analysis
    .pivot(
        index="company",
        columns="year",
        values="revenue_growth_pct"
    )
    .reset_index()
)

def classify_growth(row):
    growth_2024 = row.get(2024)
    growth_2025 = row.get(2025)

    if pd.isna(growth_2024) or pd.isna(growth_2025):
        return "Insufficient history"

    if growth_2024 > 0 and growth_2025 > 0:
        return "Consistent positive growth"

    elif growth_2024 < 0 and growth_2025 < 0:
        return "Consistent negative growth"

    else:
        return "Changing direction"


revenue_growth_trajectory["growth_trajectory"] = (
    revenue_growth_trajectory.apply(
        classify_growth,
        axis=1
    )
)

revenue_growth_trajectory


# In[785]:


consolidated_financial_df.columns.tolist()


# In[786]:


#Step 1 — create the base company-level snapshot


# In[787]:


financial_intelligence_base = (
    consolidated_financial_df[
        consolidated_financial_df["year"] == 2025
    ][
        [
            "company",
            "revenue_usd_000",
            "revenue_growth_pct",
            "gross_margin_pct",
            "operating_margin_pct",
            "net_margin_pct",
            "operating_cash_flow_usd_000",
            "cfo_margin_pct"
        ]
    ]
    .sort_values("company")
    .reset_index(drop=True)
)

financial_intelligence_base


# In[788]:


#Step 2 — add the 2023→2025 trend features


# In[789]:


financial_intelligence_df = financial_intelligence_base.merge(
    company_trend_summary[
        [
            "company",
            "gross_margin_change_pct_points",
            "operating_margin_change_pct_points",
            "net_margin_change_pct_points",
            "cfo_margin_change_pct_points"
        ]
    ],
    on="company",
    how="left"
)

financial_intelligence_df


# In[790]:


#Step 3 — validate the company-level dataset


# In[791]:


print("Shape:", financial_intelligence_df.shape)

print("\nCompanies:")
print(financial_intelligence_df["company"].tolist())

print("\nDuplicate companies:")
print(financial_intelligence_df["company"].duplicated().sum())

print("\nMissing values:")
print(financial_intelligence_df.isna().sum())


# In[792]:


#Step 4 — add earnings quality


# In[793]:


financial_intelligence_df = financial_intelligence_df.merge(
    latest_earnings_quality[
        [
            "company",
            "cfo_to_net_income_ratio",
            "cash_conversion_pct",
            "cfo_to_net_income_interpretation"
        ]
    ],
    on="company",
    how="left"
)

financial_intelligence_df


# In[794]:


#Step 5 — add the revenue-growth trajectory


# In[795]:


financial_intelligence_df = financial_intelligence_df.merge(
    revenue_growth_trajectory[
        [
            "company",
            "growth_trajectory"
        ]
    ],
    on="company",
    how="left"
)

financial_intelligence_df


# In[796]:


#Step 6 — validate the complete Financial Intelligence Dataset


# In[797]:


print("Shape:", financial_intelligence_df.shape)

print("\nColumns:")
print(financial_intelligence_df.columns.tolist())

print("\nDuplicate companies:")
print(financial_intelligence_df["company"].duplicated().sum())

print("\nMissing values:")
print(financial_intelligence_df.isna().sum())


# In[798]:


comparison = financial_intelligence_df[
    [
        "company",
        "cfo_to_net_income_ratio",
        "cash_conversion_pct"
    ]
].copy()

comparison["ratio_as_pct"] = (
    comparison["cfo_to_net_income_ratio"] * 100
)

comparison


# In[799]:


financial_intelligence_df = financial_intelligence_df.drop(
    columns=["cash_conversion_pct"]
)

print("Shape:", financial_intelligence_df.shape)
print("\nColumns:")
print(financial_intelligence_df.columns.tolist())


# In[800]:


#Step 8 — add absolute operating-income change


# In[801]:


financial_intelligence_df = financial_intelligence_df.merge(
    operating_income_trend[
        [
            "company",
            "operating_income_change_usd_000"
        ]
    ],
    on="company",
    how="left"
)

financial_intelligence_df


# In[802]:


#Step 9 — convert operating-income change to USD millions


# In[803]:


financial_intelligence_df["operating_income_change_usd_mn"] = (
    financial_intelligence_df["operating_income_change_usd_000"] / 1000
)

financial_intelligence_df[
    [
        "company",
        "operating_income_change_usd_000",
        "operating_income_change_usd_mn"
    ]
]


# In[804]:


#Step 10 — final Financial Intelligence QA


# In[805]:


print("Shape:", financial_intelligence_df.shape)

print("\nDuplicate companies:")
print(financial_intelligence_df["company"].duplicated().sum())

print("\nMissing values:")
print(financial_intelligence_df.isna().sum())

print("\nData types:")
print(financial_intelligence_df.dtypes)


# In[806]:


#Step 11 — define the financial screening dimensions


# In[807]:


growth_screening = financial_intelligence_df[
    [
        "company",
        "revenue_usd_000",
        "revenue_growth_pct",
        "growth_trajectory"
    ]
].copy()

growth_screening


# In[808]:


#Step 13 — add the 2023→2025 cumulative revenue growth


# In[809]:


growth_screening = growth_screening.merge(
    revenue_scale_trend[
        [
            "company",
            "revenue_growth_2023_to_2025_pct"
        ]
    ],
    on="company",
    how="left"
)

growth_screening


# In[810]:


#Step 14 — build the Profitability Screening View


# In[811]:


profitability_screening = financial_intelligence_df[
    [
        "company",
        "gross_margin_pct",
        "operating_margin_pct",
        "net_margin_pct",
        "gross_margin_change_pct_points",
        "operating_margin_change_pct_points",
        "net_margin_change_pct_points"
    ]
].copy()

profitability_screening


# In[812]:


#Step 15 — build the Cash Generation Screening View


# In[813]:


cash_generation_screening = financial_intelligence_df[
    [
        "company",
        "operating_cash_flow_usd_000",
        "cfo_margin_pct",
        "cfo_margin_change_pct_points"
    ]
].copy()

cash_generation_screening = cash_generation_screening.merge(
    cash_flow_trend[
        [
            "company",
            "operating_cash_flow_change_2023_to_2025",
            "operating_cash_flow_change_usd_mn"
        ]
    ],
    on="company",
    how="left"
)

cash_generation_screening


# In[814]:


#Step 16 — build the Earnings Quality Screening View


# In[815]:


earnings_quality_screening = (
    consolidated_financial_df[
        consolidated_financial_df["year"] == 2025
    ][
        [
            "company",
            "net_income_usd_000",
            "operating_cash_flow_usd_000"
        ]
    ]
    .merge(
        financial_intelligence_df[
            [
                "company",
                "cfo_to_net_income_ratio",
                "cfo_to_net_income_interpretation"
            ]
        ],
        on="company",
        how="left"
    )
    .sort_values("company")
    .reset_index(drop=True)
)

earnings_quality_screening


# #A few observations we can document:
# 
# BOOT: CFO was below net income, ratio ≈ 0.82.
# CROX: net income was negative while CFO remained positive, so the ratio is mathematically negative and should not be interpreted as a conventional cash-conversion percentage.
# DUOL: CFO was close to net income, ratio ≈ 0.94.
# ETSY: CFO was substantially higher than net income, ratio ≈ 4.25.
# SHAK: CFO was substantially higher than net income, ratio ≈ 4.86.

# In[816]:


#Step 17 — build the Earnings–Cash Flow Alignment View


# In[817]:


earnings_cashflow_screening = (
    earnings_cashflow_alignment_summary.copy()
)

earnings_cashflow_screening


# In[818]:


#Step 18 — create the Operating Performance Screening View


# In[819]:


print("operating_income_trend columns:")
print(operating_income_trend.columns.tolist())

print("\noperating_income_trend_summary columns:")
print(operating_income_trend_summary.columns.tolist())


# In[820]:


#Step 18 — corrected Operating Performance Screening View


# In[821]:


operating_performance_screening = (
    consolidated_financial_df[
        consolidated_financial_df["year"] == 2025
    ][
        [
            "company",
            "operating_income_usd_000",
            "operating_margin_pct"
        ]
    ]
    .merge(
        operating_income_trend_summary[
            [
                "company",
                "operating_income_change_2023_to_2025",
                "operating_margin_change_pct_points"
            ]
        ],
        on="company",
        how="left"
    )
    .merge(
        operating_income_trend[
            [
                "company",
                "operating_income_change_usd_mn"
            ]
        ],
        on="company",
        how="left"
    )
    .sort_values("company")
    .reset_index(drop=True)
)

operating_performance_screening


# #What this tells us
# 
# We now have a clean descriptive view of operating performance:
# 
# BOOT: FY2025 operating income = $239.352M; operating margin = 12.52%; operating income increased by $7.565M since FY2023, while margin declined by 1.46 percentage points.
# CROX: FY2025 operating income = $149.515M; margin = 3.70%; operating income declined by $887.268M and margin declined by 22.47 percentage points.
# DUOL: FY2025 operating income = $135.570M; margin = 13.07%; operating income increased by $148.829M and margin improved by 15.56 percentage points.
# ETSY: FY2025 operating income = $266.210M; margin = 9.23%; operating income declined by $13.631M and margin declined by 0.95 percentage points.
# SHAK: FY2025 operating income = $62.508M; margin = 4.32%; operating income increased by $56.587M and margin improved by 3.78 percentage points.
# 
# Notice something important for your project methodology: we are not declaring one company the "winner." We're building multiple dimensions of financial evidence that can later support a corporate-venture screening decision.

# In[822]:


screening_views = {
    "growth": growth_screening,
    "profitability": profitability_screening,
    "cash_generation": cash_generation_screening,
    "earnings_quality": earnings_quality_screening,
    "earnings_cashflow": earnings_cashflow_screening,
    "operating_performance": operating_performance_screening
}

for name, df in screening_views.items():
    print(f"{name}:")
    print("  rows:", len(df))
    print("  unique companies:", df["company"].nunique())
    print("  duplicate companies:", df["company"].duplicated().sum())
    print()


# In[823]:


for name, df in screening_views.items():
    print(f"\n{name.upper()}")
    print(df.columns.tolist())


# In[824]:


#Next step — build the integrated intelligence table


# In[825]:


investment_intelligence_df = (
    growth_screening
    .merge(
        profitability_screening,
        on="company",
        how="left"
    )
    .merge(
        cash_generation_screening,
        on="company",
        how="left",
        suffixes=("", "_cash")
    )
    .merge(
        earnings_quality_screening,
        on="company",
        how="left",
        suffixes=("", "_earnings")
    )
    .merge(
        earnings_cashflow_screening,
        on="company",
        how="left"
    )
    .merge(
        operating_performance_screening,
        on="company",
        how="left",
        suffixes=("", "_operating")
    )
    .sort_values("company")
    .reset_index(drop=True)
)

print("Shape:", investment_intelligence_df.shape)
print("\nColumns:")
print(investment_intelligence_df.columns.tolist())


# In[826]:


#Next step: identify whether the duplicate columns are truly identical


# In[827]:


print(
    "Operating cash flow columns identical:",
    investment_intelligence_df["operating_cash_flow_usd_000"].equals(
        investment_intelligence_df["operating_cash_flow_usd_000_earnings"]
    )
)

print(
    "Operating margin columns identical:",
    investment_intelligence_df["operating_margin_pct"].equals(
        investment_intelligence_df["operating_margin_pct_operating"]
    )
)

print(
    "Operating margin change columns identical:",
    investment_intelligence_df["operating_margin_change_pct_points"].equals(
        investment_intelligence_df["operating_margin_change_pct_points_operating"]
    )
)


# In[828]:


#Step 19 — Remove only the validated duplicates


# In[829]:


investment_intelligence_df = investment_intelligence_df.drop(
    columns=[
        "operating_cash_flow_usd_000_earnings",
        "operating_margin_pct_operating",
        "operating_margin_change_pct_points_operating"
    ]
)

print("Shape:", investment_intelligence_df.shape)
print("\nColumns:")
print(investment_intelligence_df.columns.tolist())


# In[830]:


#Step 20 — Final structural QA


# In[831]:


print("Shape:", investment_intelligence_df.shape)

print("\nDuplicate companies:")
print(
    investment_intelligence_df["company"]
    .duplicated()
    .sum()
)

print("\nMissing values:")
print(
    investment_intelligence_df.isna().sum()
)

print("\nData types:")
print(
    investment_intelligence_df.dtypes
)


# # Next stage: Investment Intelligence

# In[832]:


#Step 21 — Create the core investment intelligence view


# In[833]:


investment_intelligence_core = investment_intelligence_df[
    [
        "company",
        "revenue_usd_000",
        "revenue_growth_pct",
        "revenue_growth_2023_to_2025_pct",
        "growth_trajectory",
        "gross_margin_pct",
        "operating_margin_pct",
        "net_margin_pct",
        "operating_margin_change_pct_points",
        "net_margin_change_pct_points",
        "operating_cash_flow_usd_000",
        "cfo_margin_pct",
        "cfo_margin_change_pct_points",
        "cfo_to_net_income_ratio",
        "cfo_to_net_income_interpretation",
        "Divergent",
        "operating_income_usd_000",
        "operating_income_change_usd_mn"
    ]
].copy()

print("Shape:", investment_intelligence_core.shape)
print("\nColumns:")
print(investment_intelligence_core.columns.tolist())

investment_intelligence_core


# In[834]:


#Step 22 — Create transparent financial evidence flags


# In[835]:


investment_intelligence_flags = investment_intelligence_core.copy()

investment_intelligence_flags["growth_flag"] = (
    investment_intelligence_flags["revenue_growth_pct"]
    .apply(
        lambda x:
        "Positive" if x > 0
        else "Negative" if x < 0
        else "Flat"
    )
)

investment_intelligence_flags["operating_margin_flag"] = (
    investment_intelligence_flags["operating_margin_change_pct_points"]
    .apply(
        lambda x:
        "Improved" if x > 0
        else "Declined" if x < 0
        else "Unchanged"
    )
)

investment_intelligence_flags["net_margin_flag"] = (
    investment_intelligence_flags["net_margin_change_pct_points"]
    .apply(
        lambda x:
        "Improved" if x > 0
        else "Declined" if x < 0
        else "Unchanged"
    )
)

investment_intelligence_flags["cash_generation_flag"] = (
    investment_intelligence_flags["cfo_margin_change_pct_points"]
    .apply(
        lambda x:
        "Improved" if x > 0
        else "Declined" if x < 0
        else "Unchanged"
    )
)

investment_intelligence_flags["operating_income_flag"] = (
    investment_intelligence_flags["operating_income_change_usd_mn"]
    .apply(
        lambda x:
        "Increased" if x > 0
        else "Decreased" if x < 0
        else "Unchanged"
    )
)

print("Shape:", investment_intelligence_flags.shape)
print("\nNew columns:")
print(
    investment_intelligence_flags[
        [
            "company",
            "growth_flag",
            "operating_margin_flag",
            "net_margin_flag",
            "cash_generation_flag",
            "operating_income_flag"
        ]
    ]
)


# In[836]:


#Step 23 — Add earnings–cash-flow alignment flag


# In[843]:


print(
    investment_intelligence_flags[
        [
            "company",
            "Divergent",
            "earnings_cashflow_flag"
        ]
    ]
)


# In[844]:


# Step 23 — Add earnings / cash-flow alignment flag

investment_intelligence_flags["earnings_cashflow_flag"] = (
    investment_intelligence_df.apply(
        lambda row:
        "Divergent periods present"
        if row["Divergent"] > 0
        else "Aligned positive"
        if row["Aligned positive"] > 0
        else "Aligned negative"
        if row["Aligned negative"] > 0
        else "No classified periods",
        axis=1
    )
)

print(
    investment_intelligence_flags[
        [
            "company",
            "Divergent",
            "earnings_cashflow_flag"
        ]
    ].to_string(index=False)
)


# In[845]:


print("Rows:", len(investment_intelligence_flags))
print("Unique companies:", investment_intelligence_flags["company"].nunique())
print("Duplicate companies:", investment_intelligence_flags["company"].duplicated().sum())
print("Missing earnings-cash-flow flags:",
      investment_intelligence_flags["earnings_cashflow_flag"].isna().sum())


# In[846]:


#Step 24 — First, let's create a compact profile dataset


# In[847]:


company_profile_df = investment_intelligence_flags[
    [
        "company",
        "revenue_growth_pct",
        "revenue_growth_2023_to_2025_pct",
        "growth_trajectory",
        "operating_margin_pct",
        "operating_margin_change_pct_points",
        "net_margin_pct",
        "net_margin_change_pct_points",
        "cfo_margin_pct",
        "cfo_margin_change_pct_points",
        "operating_income_change_usd_mn",
        "earnings_cashflow_flag"
    ]
].copy()

print("Shape:", company_profile_df.shape)
print("\nColumns:")
print(company_profile_df.columns.tolist())

company_profile_df


# In[848]:


#Step 25 — Build a structured evidence summary


# In[849]:


company_profile_df["financial_direction_summary"] = (
    "Growth: "
    + company_profile_df["growth_trajectory"]
    + "; Operating margin: "
    + company_profile_df["operating_margin_change_pct_points"]
        .apply(
            lambda x:
            "improved" if x > 0
            else "declined" if x < 0
            else "unchanged"
        )
    + "; Net margin: "
    + company_profile_df["net_margin_change_pct_points"]
        .apply(
            lambda x:
            "improved" if x > 0
            else "declined" if x < 0
            else "unchanged"
        )
    + "; CFO margin: "
    + company_profile_df["cfo_margin_change_pct_points"]
        .apply(
            lambda x:
            "improved" if x > 0
            else "declined" if x < 0
            else "unchanged"
        )
    + "; Operating income: "
    + company_profile_df["operating_income_change_usd_mn"]
        .apply(
            lambda x:
            "increased" if x > 0
            else "decreased" if x < 0
            else "unchanged"
        )
    + "; Earnings/CFO: "
    + company_profile_df["earnings_cashflow_flag"]
)

print(
    company_profile_df[
        [
            "company",
            "financial_direction_summary"
        ]
    ]
)


# In[850]:


for _, row in company_profile_df.iterrows():
    print(f"\n{row['company']}")
    print(row["financial_direction_summary"])


# In[851]:


#Step 26 — Add an explicit FY2025 financial status


# In[852]:


company_profile_df["fy2025_status_summary"] = (
    "FY2025 operating margin: "
    + company_profile_df["operating_margin_pct"].round(2).astype(str)
    + "%; Net margin: "
    + company_profile_df["net_margin_pct"].round(2).astype(str)
    + "%; CFO margin: "
    + company_profile_df["cfo_margin_pct"].round(2).astype(str)
    + "%"
)

for _, row in company_profile_df.iterrows():
    print(f"\n{row['company']}")
    print(row["fy2025_status_summary"])


# In[853]:


#Step 27 — Create growth magnitude classification


# In[854]:


def classify_growth_magnitude(x):
    if pd.isna(x):
        return "Unavailable"
    elif x < 5:
        return "Low growth"
    elif x < 20:
        return "Moderate growth"
    elif x < 50:
        return "High growth"
    else:
        return "Very high growth"


company_profile_df["growth_magnitude"] = (
    company_profile_df["revenue_growth_2023_to_2025_pct"]
    .apply(classify_growth_magnitude)
)

for _, row in company_profile_df.iterrows():
    print(
        f"{row['company']}: "
        f"{row['growth_magnitude']} "
        f"({row['revenue_growth_2023_to_2025_pct']:.2f}% "
        f"revenue change, FY2023→FY2025)"
    )


# In[855]:


#Step 28 — Create the final narrative-ready profile table


# In[856]:


company_narrative_df = company_profile_df[
    [
        "company",
        "growth_magnitude",
        "revenue_growth_pct",
        "revenue_growth_2023_to_2025_pct",
        "growth_trajectory",
        "operating_margin_pct",
        "operating_margin_change_pct_points",
        "net_margin_pct",
        "net_margin_change_pct_points",
        "cfo_margin_pct",
        "cfo_margin_change_pct_points",
        "operating_income_change_usd_mn",
        "earnings_cashflow_flag"
    ]
].copy()

print("Shape:", company_narrative_df.shape)

print("\nColumns:")
print(company_narrative_df.columns.tolist())

company_narrative_df


# In[857]:


#Step 29 — Start the company-level interpretation
#BOOT


# In[858]:


boot_profile = company_narrative_df[
    company_narrative_df["company"] == "BOOT"
].iloc[0]

print("COMPANY:", boot_profile["company"])

print("\nGROWTH")
print("Magnitude:", boot_profile["growth_magnitude"])
print("FY2025 growth:", round(boot_profile["revenue_growth_pct"], 2), "%")
print(
    "FY2023-FY2025 revenue change:",
    round(boot_profile["revenue_growth_2023_to_2025_pct"], 2),
    "%"
)
print("Trajectory:", boot_profile["growth_trajectory"])

print("\nPROFITABILITY")
print(
    "FY2025 operating margin:",
    round(boot_profile["operating_margin_pct"], 2),
    "%"
)
print(
    "Operating margin change:",
    round(boot_profile["operating_margin_change_pct_points"], 2),
    "pp"
)
print(
    "FY2025 net margin:",
    round(boot_profile["net_margin_pct"], 2),
    "%"
)
print(
    "Net margin change:",
    round(boot_profile["net_margin_change_pct_points"], 2),
    "pp"
)

print("\nCASH GENERATION")
print(
    "FY2025 CFO margin:",
    round(boot_profile["cfo_margin_pct"], 2),
    "%"
)
print(
    "CFO margin change:",
    round(boot_profile["cfo_margin_change_pct_points"], 2),
    "pp"
)

print("\nOPERATING PERFORMANCE")
print(
    "Operating income change:",
    round(boot_profile["operating_income_change_usd_mn"], 3),
    "USD million"
)

print("\nEARNINGS / CASH FLOW")
print(boot_profile["earnings_cashflow_flag"])


# In[859]:


#CROX


# In[860]:


crox_profile = company_narrative_df[
    company_narrative_df["company"] == "CROX"
].iloc[0]

print("COMPANY:", crox_profile["company"])

print("\nGROWTH")
print("Magnitude:", crox_profile["growth_magnitude"])
print("FY2025 growth:", round(crox_profile["revenue_growth_pct"], 2), "%")
print(
    "FY2023-FY2025 revenue change:",
    round(crox_profile["revenue_growth_2023_to_2025_pct"], 2),
    "%"
)
print("Trajectory:", crox_profile["growth_trajectory"])

print("\nPROFITABILITY")
print(
    "FY2025 operating margin:",
    round(crox_profile["operating_margin_pct"], 2),
    "%"
)
print(
    "Operating margin change:",
    round(crox_profile["operating_margin_change_pct_points"], 2),
    "pp"
)
print(
    "FY2025 net margin:",
    round(crox_profile["net_margin_pct"], 2),
    "%"
)
print(
    "Net margin change:",
    round(crox_profile["net_margin_change_pct_points"], 2),
    "pp"
)

print("\nCASH GENERATION")
print(
    "FY2025 CFO margin:",
    round(crox_profile["cfo_margin_pct"], 2),
    "%"
)
print(
    "CFO margin change:",
    round(crox_profile["cfo_margin_change_pct_points"], 2),
    "pp"
)

print("\nOPERATING PERFORMANCE")
print(
    "Operating income change:",
    round(crox_profile["operating_income_change_usd_mn"], 3),
    "USD million"
)

print("\nEARNINGS / CASH FLOW")
print(crox_profile["earnings_cashflow_flag"])


# In[861]:


#DUOL


# In[862]:


duol_profile = company_narrative_df[
    company_narrative_df["company"] == "DUOL"
].iloc[0]

print("COMPANY:", duol_profile["company"])

print("\nGROWTH")
print("Magnitude:", duol_profile["growth_magnitude"])
print("FY2025 growth:", round(duol_profile["revenue_growth_pct"], 2), "%")
print(
    "FY2023-FY2025 revenue change:",
    round(duol_profile["revenue_growth_2023_to_2025_pct"], 2),
    "%"
)
print("Trajectory:", duol_profile["growth_trajectory"])

print("\nPROFITABILITY")
print(
    "FY2025 operating margin:",
    round(duol_profile["operating_margin_pct"], 2),
    "%"
)
print(
    "Operating margin change:",
    round(duol_profile["operating_margin_change_pct_points"], 2),
    "pp"
)
print(
    "FY2025 net margin:",
    round(duol_profile["net_margin_pct"], 2),
    "%"
)
print(
    "Net margin change:",
    round(duol_profile["net_margin_change_pct_points"], 2),
    "pp"
)

print("\nCASH GENERATION")
print(
    "FY2025 CFO margin:",
    round(duol_profile["cfo_margin_pct"], 2),
    "%"
)
print(
    "CFO margin change:",
    round(duol_profile["cfo_margin_change_pct_points"], 2),
    "pp"
)

print("\nOPERATING PERFORMANCE")
print(
    "Operating income change:",
    round(duol_profile["operating_income_change_usd_mn"], 3),
    "USD million"
)

print("\nEARNINGS / CASH FLOW")
print(duol_profile["earnings_cashflow_flag"])


# In[863]:


#ETSY


# In[864]:


etsy_profile = company_narrative_df[
    company_narrative_df["company"] == "ETSY"
].iloc[0]

print("COMPANY:", etsy_profile["company"])

print("\nGROWTH")
print("Magnitude:", etsy_profile["growth_magnitude"])
print("FY2025 growth:", round(etsy_profile["revenue_growth_pct"], 2), "%")
print(
    "FY2023-FY2025 revenue change:",
    round(etsy_profile["revenue_growth_2023_to_2025_pct"], 2),
    "%"
)
print("Trajectory:", etsy_profile["growth_trajectory"])

print("\nPROFITABILITY")
print(
    "FY2025 operating margin:",
    round(etsy_profile["operating_margin_pct"], 2),
    "%"
)
print(
    "Operating margin change:",
    round(etsy_profile["operating_margin_change_pct_points"], 2),
    "pp"
)
print(
    "FY2025 net margin:",
    round(etsy_profile["net_margin_pct"], 2),
    "%"
)
print(
    "Net margin change:",
    round(etsy_profile["net_margin_change_pct_points"], 2),
    "pp"
)

print("\nCASH GENERATION")
print(
    "FY2025 CFO margin:",
    round(etsy_profile["cfo_margin_pct"], 2),
    "%"
)
print(
    "CFO margin change:",
    round(etsy_profile["cfo_margin_change_pct_points"], 2),
    "pp"
)

print("\nOPERATING PERFORMANCE")
print(
    "Operating income change:",
    round(etsy_profile["operating_income_change_usd_mn"], 3),
    "USD million"
)

print("\nEARNINGS / CASH FLOW")
print(etsy_profile["earnings_cashflow_flag"])


# In[865]:


#SHAK


# In[866]:


shak_profile = company_narrative_df[
    company_narrative_df["company"] == "SHAK"
].iloc[0]

print("COMPANY:", shak_profile["company"])

print("\nGROWTH")
print("Magnitude:", shak_profile["growth_magnitude"])
print("FY2025 growth:", round(shak_profile["revenue_growth_pct"], 2), "%")
print(
    "FY2023-FY2025 revenue change:",
    round(shak_profile["revenue_growth_2023_to_2025_pct"], 2),
    "%"
)
print("Trajectory:", shak_profile["growth_trajectory"])

print("\nPROFITABILITY")
print(
    "FY2025 operating margin:",
    round(shak_profile["operating_margin_pct"], 2),
    "%"
)
print(
    "Operating margin change:",
    round(shak_profile["operating_margin_change_pct_points"], 2),
    "pp"
)
print(
    "FY2025 net margin:",
    round(shak_profile["net_margin_pct"], 2),
    "%"
)
print(
    "Net margin change:",
    round(shak_profile["net_margin_change_pct_points"], 2),
    "pp"
)

print("\nCASH GENERATION")
print(
    "FY2025 CFO margin:",
    round(shak_profile["cfo_margin_pct"], 2),
    "%"
)
print(
    "CFO margin change:",
    round(shak_profile["cfo_margin_change_pct_points"], 2),
    "pp"
)

print("\nOPERATING PERFORMANCE")
print(
    "Operating income change:",
    round(shak_profile["operating_income_change_usd_mn"], 3),
    "USD million"
)

print("\nEARNINGS / CASH FLOW")
print(shak_profile["earnings_cashflow_flag"])


# In[867]:


portfolio_direction_summary = pd.DataFrame({
    "metric": [
        "Revenue growth",
        "Operating margin",
        "Net margin",
        "CFO margin",
        "Operating income"
    ],
    "improved_or_positive": [
        (company_narrative_df["revenue_growth_pct"] > 0).sum(),
        (company_narrative_df["operating_margin_change_pct_points"] > 0).sum(),
        (company_narrative_df["net_margin_change_pct_points"] > 0).sum(),
        (company_narrative_df["cfo_margin_change_pct_points"] > 0).sum(),
        (company_narrative_df["operating_income_change_usd_mn"] > 0).sum()
    ],
    "declined_or_negative": [
        (company_narrative_df["revenue_growth_pct"] < 0).sum(),
        (company_narrative_df["operating_margin_change_pct_points"] < 0).sum(),
        (company_narrative_df["net_margin_change_pct_points"] < 0).sum(),
        (company_narrative_df["cfo_margin_change_pct_points"] < 0).sum(),
        (company_narrative_df["operating_income_change_usd_mn"] < 0).sum()
    ]
})

print(portfolio_direction_summary)


# In[868]:


#Step 31 — Create the company × evidence matrix


# In[869]:


portfolio_evidence_matrix = investment_intelligence_flags[
    [
        "company",
        "growth_flag",
        "operating_margin_flag",
        "net_margin_flag",
        "cash_generation_flag",
        "operating_income_flag",
        "earnings_cashflow_flag"
    ]
].copy()

print(portfolio_evidence_matrix.to_string(index=False))


# In[870]:


#Step 32 — Add a portfolio-level consistency indicator


# In[871]:


portfolio_evidence_count = portfolio_evidence_matrix.copy()

portfolio_evidence_count["positive_direction_count"] = (
    (portfolio_evidence_count["growth_flag"] == "Positive").astype(int)
    + (portfolio_evidence_count["operating_margin_flag"] == "Improved").astype(int)
    + (portfolio_evidence_count["net_margin_flag"] == "Improved").astype(int)
    + (portfolio_evidence_count["cash_generation_flag"] == "Improved").astype(int)
    + (portfolio_evidence_count["operating_income_flag"] == "Increased").astype(int)
)

portfolio_evidence_count["negative_direction_count"] = (
    (portfolio_evidence_count["growth_flag"] == "Negative").astype(int)
    + (portfolio_evidence_count["operating_margin_flag"] == "Declined").astype(int)
    + (portfolio_evidence_count["net_margin_flag"] == "Declined").astype(int)
    + (portfolio_evidence_count["cash_generation_flag"] == "Declined").astype(int)
    + (portfolio_evidence_count["operating_income_flag"] == "Decreased").astype(int)
)

print(
    portfolio_evidence_count[
        [
            "company",
            "positive_direction_count",
            "negative_direction_count",
            "earnings_cashflow_flag"
        ]
    ].to_string(index=False)
)


# In[872]:


#Step 33 — Create the final analytical dataset


# In[873]:


final_screening_df = investment_intelligence_flags[
    [
        "company",
        "revenue_growth_pct",
        "revenue_growth_2023_to_2025_pct",
        "growth_trajectory",
        "operating_margin_pct",
        "operating_margin_change_pct_points",
        "net_margin_pct",
        "net_margin_change_pct_points",
        "cfo_margin_pct",
        "cfo_margin_change_pct_points",
        "operating_income_usd_000",
        "operating_income_change_usd_mn",
        "earnings_cashflow_flag",
        "growth_flag",
        "operating_margin_flag",
        "net_margin_flag",
        "cash_generation_flag",
        "operating_income_flag"
    ]
].copy()

final_screening_df = final_screening_df.merge(
    portfolio_evidence_count[
        [
            "company",
            "positive_direction_count",
            "negative_direction_count"
        ]
    ],
    on="company",
    how="left"
)

print("Shape:", final_screening_df.shape)
print("\nColumns:")
print(final_screening_df.columns.tolist())

print("\nFinal screening dataset:")
print(final_screening_df.to_string(index=False))


# In[874]:


#Step 34 — Final analytical QA


# In[875]:


print("FINAL ANALYTICAL QA")
print("=" * 50)

print("\n1. Shape:")
print(final_screening_df.shape)

print("\n2. Unique companies:")
print(final_screening_df["company"].nunique())

print("\n3. Duplicate companies:")
print(final_screening_df["company"].duplicated().sum())

print("\n4. Missing values:")
print(final_screening_df.isna().sum())

print("\n5. Directional count validation:")
print(
    final_screening_df[
        [
            "company",
            "positive_direction_count",
            "negative_direction_count"
        ]
    ].to_string(index=False)
)

print("\n6. Directional count totals:")
print(
    (
        final_screening_df["positive_direction_count"]
        + final_screening_df["negative_direction_count"]
    ).value_counts()
)


# In[876]:


#Step 35 — Actual dataset inspection


# In[877]:


print("FINAL DATASET")
print("=" * 50)

print("Shape:", final_screening_df.shape)

print("\nColumns:")
for i, column in enumerate(final_screening_df.columns, start=1):
    print(f"{i}. {column}")

print("\nData types:")
print(final_screening_df.dtypes)


# In[878]:


import importlib.util

print(
    "SQLAlchemy installed:",
    importlib.util.find_spec("sqlalchemy") is not None
)

print(
    "PyMySQL installed:",
    importlib.util.find_spec("pymysql") is not None
)


# In[879]:


get_ipython().run_line_magic('pip', 'install pymysql')


# In[880]:


import pymysql

print("PyMySQL version:", pymysql.__version__)


# In[881]:


print(final_screening_df.shape)


# In[882]:


#Create the Python → MySQL connection


# In[883]:


import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="Neymar@125",
    database="investment_intelligence"
)

print("MySQL connection successful!")


# In[884]:


#Load final_screening_df into MySQL


# In[885]:


final_screening_df.to_sql(
    "investment_screening",
    con=connection,
    if_exists="append",
    index=False
)

print("Data loaded successfully!")


# In[886]:


get_ipython().system('pip install sqlalchemy')


# In[889]:


from sqlalchemy import create_engine
from urllib.parse import quote_plus

mysql_password = "Neymar@125"

engine = create_engine(
    f"mysql+pymysql://root:{quote_plus(mysql_password)}@localhost/investment_intelligence"
)

print("SQLAlchemy engine created successfully!")


# In[890]:


final_screening_df.to_sql(
    "investment_screening",
    con=engine,
    if_exists="append",
    index=False
)

print("Data loaded successfully!")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




