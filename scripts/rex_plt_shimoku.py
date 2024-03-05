import re
import os
import pandas as pd

with open('charts_query.txt', 'r') as f:
  raw_data = f.readlines()

template_names = []
chart_names = []

for line in raw_data:
    line_split = line.split(":")
    template_name = os.path.dirname(line_split[0]).split(os.sep)[1]
    chart_name_regex = re.findall(r'plt\.\w+', line_split[2])
    chart_name = chart_name_regex[0].replace("(","").replace("plt.","")
    template_names.append(template_name)
    chart_names.append(chart_name)

template = "template_name"
chart = "chart_name"

dict_charts_name = {
    template : template_names,
    chart : chart_names,
}

df_charts_name = pd.DataFrame(dict_charts_name)
df_charts_name = df_charts_name.sort_values(by=[template], key=lambda col: col.str.lower())
df_charts_name.to_csv("charts_name_templates.csv", index=False)