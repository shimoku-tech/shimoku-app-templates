import re
import datetime as dt
import pandas as pd

from subprocess import PIPE, Popen


ls_cmd = ["ls", "templates"]
ls_proc = Popen(ls_cmd, stdout=PIPE, stderr=PIPE)
wc_cmd = ["wc", "-l"]
wc_proc = Popen(wc_cmd,stdin=ls_proc.stdout, stdout=PIPE)
wc_output, _= wc_proc.communicate()

version = "1.0.0"
with open("requirements.txt") as f:
    libs = f.readlines()
    for line in libs:
        if re.match(r"shimoku.*==", line):
            version = line.split("==")[1].replace("\n","")

blacklist = pd.read_csv("templates/key_results/data/nocharts_SDK.csv")

templates = pd.read_csv("charts_name_templates.csv")
templates = templates[~templates["chart_name"].isin(blacklist["chart_name"])]

sdk = pd.read_csv("charts_name_SDK.csv")
sdk = sdk[~sdk["chart_name"].isin(blacklist["chart_name"])]

template_chart_number = templates["chart_name"].unique().shape[0]
sdk_chart_number = sdk.shape[0]
df_chart_counts = sdk.copy()
counts = templates["chart_name"].value_counts()

frequency = []
for index, row in df_chart_counts.iterrows():
    if row["chart_name"] in counts.index:
        frequency.append(counts[row["chart_name"]])
    else:
        frequency.append(0)

df_chart_counts["frequency"] = frequency
df_chart_counts = df_chart_counts.sort_values(by="frequency", ascending=False)

dict_okr = [
    {
        "name": "OBJ-1 KR-2",
        "analysis_date": dt.datetime.now().date(),
        "value(%)": round(100 * template_chart_number / sdk_chart_number,2),
        "SDK_version": version,
        "SDK_chart_number": sdk_chart_number,
        "template_chart_number": template_chart_number,
        "template_number": int(wc_output),
    }
]

df_okr = pd.DataFrame(dict_okr)
df_okr.to_csv("OBJ-1_KR-2.csv", index=False)
df_chart_counts.to_csv("charts_frequency.csv", index=False)