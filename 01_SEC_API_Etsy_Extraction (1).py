#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# # Step 1 — Import Python libraries

# In[95]:


import requests
import pandas as pd
import json


# In[96]:


cik = "0001370637"


# In[97]:


url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

print(url)


# In[98]:


headers = {
    "User-Agent": "Shifa_Naaz shifanaazanalyst1@gmail.com"
}


# In[99]:


response = requests.get(url, headers=headers)

print(response.status_code)


# # Step 2 — Convert the API response into Python data

# In[100]:


data = response.json()


# In[101]:


type(data)


# # Step 3 — See what's inside data

# In[102]:


data.keys()


# In[103]:


data["entityName"]


# In[104]:


data["facts"].keys()


# In[105]:


us_gaap = data["facts"]["us-gaap"]


# In[106]:


type(us_gaap)


# # Revenue

# In[107]:


list(us_gaap.keys())[:20]


# In[108]:


[key for key in us_gaap.keys() if "Revenue" in key]


# In[109]:


revenue_concept = us_gaap["RevenueFromContractWithCustomerExcludingAssessedTax"]


# In[110]:


revenue_concept.keys()


# In[111]:


revenue_concept["label"]


# In[112]:


revenue_concept["description"]


# In[113]:


revenue_concept["units"].keys()


# In[114]:


revenue_concept["units"]["USD"]


# In[115]:


revenue_data = revenue_concept["units"]["USD"]

type(revenue_data)


# In[116]:


len(revenue_data)


# In[117]:


revenue_data[0]


# In[118]:


annual_revenue = [
    x for x in revenue_data
    if x["form"] == "10-K"
]

len(annual_revenue)


# In[119]:


annual_revenue[:10]


# In[120]:


[x for x in annual_revenue if x["start"] == "2023-01-01"]


# In[121]:


[x for x in annual_revenue if x["start"] == "2025-01-01"]


# In[122]:


[x for x in annual_revenue if x["start"] == "2024-01-01"]


# In[123]:


for x in annual_revenue:
    if x["start"] in ["2023-01-01", "2024-01-01", "2025-01-01"]:
        print(
            x["start"],
            x["val"],
            x["fy"],
            x["filed"]
        )


# In[124]:


annual_revenue_sorted = sorted(
    annual_revenue,
    key=lambda x: x["filed"],
    reverse=True
)


# In[125]:


annual_revenue_sorted[:5]


# In[126]:


id="6xk2rm"
revenue_df = pd.DataFrame(annual_revenue_sorted)


# In[127]:


id="n2v8qa"
revenue_df.head()


# In[128]:


id="z8n4pk"
clean_revenue_df = revenue_df.drop_duplicates(
    subset=["start", "end"],
    keep="first"
)


# In[129]:


id="1j5f6a"
clean_revenue_df


# In[130]:


target_years = [2023, 2024, 2025]


# In[131]:


target_years


# In[132]:


project_revenue_df = clean_revenue_df[
    clean_revenue_df["start"].str[:4].astype(int).isin(target_years)
]


# In[133]:


project_revenue_df


# In[134]:


revenue_final = project_revenue_df.copy()


# In[135]:


revenue_final


# In[136]:


revenue_final["revenue_usd_000"] = revenue_final["val"] / 1000


# In[137]:


revenue_final[["start", "val", "revenue_usd_000"]]


# In[138]:


qa_check = (
    revenue_final["revenue_usd_000"] * 1000
    == revenue_final["val"]
)


# In[139]:


qa_check


# # Gross Profit

# In[140]:


[key for key in us_gaap.keys() if "GrossProfit" in key]


# In[141]:


gross_profit_concept = us_gaap["GrossProfit"]


# In[142]:


gross_profit_concept.keys()


# In[143]:


gross_profit_concept["description"]


# In[144]:


gross_profit_concept["units"].keys()


# In[145]:


gross_profit_data = gross_profit_concept["units"]["USD"]


# In[146]:


type(gross_profit_data)


# In[147]:


len(gross_profit_data)


# In[148]:


gross_profit_data[0]


# In[149]:


annual_gross_profit = [
    x for x in gross_profit_data
    if x["form"] == "10-K"
]


# In[150]:


len(annual_gross_profit)


# In[151]:


[x for x in annual_gross_profit if x["start"] == "2023-01-01"]


# In[152]:


[x for x in annual_gross_profit if x["start"] == "2024-01-01"]


# In[153]:


[x for x in annual_gross_profit if x["start"] == "2025-01-01"]


# In[154]:


gross_profit_sorted = sorted(
    annual_gross_profit,
    key=lambda x: x["filed"],
    reverse=True
)


# In[155]:


gross_profit_df = pd.DataFrame(gross_profit_sorted)


# In[156]:


gross_profit_df.head()


# In[157]:


clean_gross_profit_df = gross_profit_df.drop_duplicates(
    subset=["start", "end"],
    keep="first"
)


# In[158]:


clean_gross_profit_df.head()


# In[159]:


project_gross_profit_df = clean_gross_profit_df[
    clean_gross_profit_df["start"].str[:4].astype(int).isin(target_years)
]


# In[160]:


project_gross_profit_df


# In[161]:


gross_profit_final = project_gross_profit_df.copy()


# In[162]:


gross_profit_final["gross_profit_usd_000"] = (
    gross_profit_final["val"] / 1000
)


# In[163]:


gross_profit_final[["start", "val", "gross_profit_usd_000"]]


# In[164]:


qa_gross_profit = (
    gross_profit_final["gross_profit_usd_000"] * 1000
    == gross_profit_final["val"]
)

qa_gross_profit


# ## Operating Income

# In[165]:


[key for key in us_gaap.keys() if "OperatingIncome" in key]


# In[166]:


operating_income_concept = us_gaap["OperatingIncomeLoss"]


# In[167]:


operating_income_concept.keys()


# In[168]:


operating_income_concept["description"]


# In[169]:


operating_income_concept["units"].keys()


# In[170]:


operating_income_concept["units"]["USD"][:3]


# In[171]:


operating_income_concept["units"]["USD"][-10:]


# In[172]:


[
    x for x in operating_income_concept["units"]["USD"]
    if x.get("fp") == "FY"
]


# In[173]:


[x for x in operating_income_concept["units"]["USD"]
 if x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
 and x.get("fp") == "FY"]


# In[174]:


[x for x in operating_income_concept["units"]["USD"]
 if x.get("frame") in ["CY2023", "CY2024", "CY2025"]
]


# In[175]:


279841000 / 1000


# In[176]:


operating_income_annual = [
    {
        "year": int(x["frame"].replace("CY", "")),
        "operating_income_usd_000": x["val"] / 1000
    }
    for x in operating_income_concept["units"]["USD"]
    if x.get("frame") in ["CY2023", "CY2024", "CY2025"]
]

operating_income_annual


# In[177]:


len(operating_income_annual)


# In[178]:


[x["year"] for x in operating_income_annual]


# In[179]:


[x for x in operating_income_annual if x["operating_income_usd_000"] is None]


# In[180]:


len(set(x["year"] for x in operating_income_annual))


# In[185]:


gross_profit_final[["start", "gross_profit_usd_000"]]


# In[186]:


[
    (
        op["year"],
        op["operating_income_usd_000"],
        gp["gross_profit_usd_000"],
        op["operating_income_usd_000"] <= gp["gross_profit_usd_000"]
    )
    for op, gp in zip(operating_income_annual, gross_profit_final.to_dict("records"))
]


# # Net Income

# In[187]:


[key for key in us_gaap.keys() if "NetIncome" in key]


# In[188]:


net_income_concept = us_gaap["NetIncomeLoss"]

net_income_concept.keys()


# In[189]:


net_income_concept["units"].keys()


# In[190]:


net_income_concept["units"]["USD"][:10]


# In[191]:


net_income_annual = [
    x for x in net_income_concept["units"]["USD"]
    if x.get("fp") == "FY" and x.get("form") == "10-K"
]

len(net_income_annual)


# In[192]:


[
    x for x in net_income_annual
    if x.get("frame") in ["CY2023", "CY2024", "CY2025"]
]


# In[193]:


[
    x for x in net_income_annual
    if x.get("fy") in [2023, 2024, 2025]
]


# In[194]:


net_income_target = [
    x for x in net_income_annual
    if x.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]

net_income_target


# In[195]:


net_income_latest = {}

for x in net_income_target:
    year = int(x["start"][:4])
    
    if year not in net_income_latest or x["filed"] > net_income_latest[year]["filed"]:
        net_income_latest[year] = x

net_income_latest


# In[196]:


net_income_final = [
    {
        "year": year,
        "net_income_usd_000": data["val"] / 1000
    }
    for year, data in net_income_latest.items()
]

net_income_final


# In[197]:


len(net_income_final)


# In[198]:


[x["year"] for x in net_income_final]


# In[199]:


[x for x in net_income_final if x["net_income_usd_000"] is None]


# In[200]:


len(set(x["year"] for x in net_income_final))


# In[201]:


[
    (
        ni["year"],
        ni["net_income_usd_000"],
        op["operating_income_usd_000"],
        ni["net_income_usd_000"] <= op["operating_income_usd_000"]
    )
    for ni, op in zip(net_income_final, operating_income_annual)
]


# # Operating Cash Flow

# In[202]:


[key for key in us_gaap.keys() if "Cash" in key and "Operating" in key]


# In[204]:


operating_cash_flow_concept = us_gaap["NetCashProvidedByUsedInOperatingActivities"]


# In[205]:


operating_cash_flow_concept.keys()


# In[206]:


operating_cash_flow_concept["units"].keys()


# In[207]:


operating_cash_flow_concept["units"]["USD"][:10]


# In[208]:


operating_cash_flow_annual = [
    x for x in operating_cash_flow_concept["units"]["USD"]
    if x.get("fp") == "FY" and x.get("form") == "10-K"
]

len(operating_cash_flow_annual)


# In[209]:


[
    x for x in operating_cash_flow_annual
    if x.get("fy") in [2023, 2024, 2025]
]


# In[210]:


operating_cash_flow_target = [
    x for x in operating_cash_flow_annual
    if x.get("start") in ["2023-01-01", "2024-01-01", "2025-01-01"]
    and x.get("end") in ["2023-12-31", "2024-12-31", "2025-12-31"]
]

operating_cash_flow_target


# In[211]:


operating_cash_flow_latest = {}

for x in operating_cash_flow_target:
    year = int(x["start"][:4])
    
    if year not in operating_cash_flow_latest or x["filed"] > operating_cash_flow_latest[year]["filed"]:
        operating_cash_flow_latest[year] = x

operating_cash_flow_latest


# In[212]:


operating_cash_flow_final = [
    {
        "year": year,
        "operating_cash_flow_usd_000": data["val"] / 1000
    }
    for year, data in operating_cash_flow_latest.items()
]

operating_cash_flow_final


# In[213]:


len(operating_cash_flow_final)


# In[214]:


[x["year"] for x in operating_cash_flow_final]


# In[215]:


[x for x in operating_cash_flow_final if x["operating_cash_flow_usd_000"] is None]


# In[216]:


len(set(x["year"] for x in operating_cash_flow_final))


# In[217]:


[
    (
        ocf["year"],
        ocf["operating_cash_flow_usd_000"],
        ni["net_income_usd_000"],
        ocf["operating_cash_flow_usd_000"] > ni["net_income_usd_000"]
    )
    for ocf, ni in zip(operating_cash_flow_final, net_income_final)
]


# In[ ]:




