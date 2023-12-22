import pandas as pd
from utils import get_data

dfs = get_data(["data/sales_product_performance.csv"])
df = dfs["sales_product_performance"]

# Agregar columnas de mes y año
df['month'] = df['sale_date'].dt.month
df['year'] = df['sale_date'].dt.year

# Agrupar por mes, año y producto, sumando los valores de 'cost'
result = df.groupby(['year', 'month', 'product_name'])['cost'].sum().reset_index()
pivot_result = result.pivot_table(index=['year', 'month'], columns='product_name', values='cost', aggfunc='sum').reset_index()


# Imprimir el resultado
print(pivot_result.to_json())


#df_cost = df.groupby("product_name")["cost"].sum().reset_index()
#print(df_cost)

#df_campaign = df.groupby("origin_campaign")["revenue"].sum().reset_index()
#print(df_campaign)
#print(df_campaign.to_json())

#df_in_store = df[df["sale_type"] == "In-Store"]
#df_in_store = df_in_store.groupby(df_in_store["sale_date"].dt.month)["revenue"].sum().reset_index()
#print(df_in_store.to_json())

"""
data = [
    {
        "date": val1["sale_date"], 
        "x": val1["revenue"],
        "y": round(val2["revenue"],3)
    } 
    for (index1, val1), (index2, val2) 
    in zip(df_online.iterrows(),df_in_store.iterrows())
]

print(data)
"""

#print(grouped)
#print()
#print(data)