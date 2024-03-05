import re
import pandas as pd
import datetime as dt
import argparse

parser = argparse.ArgumentParser(description='Process github url http or ssh')
parser.add_argument('repo_url', metavar='N', type=str, help='github url')

TITLE_QUERY_FILENAME = "title_query.txt"
PUBLIC_QUERY_FILENAME = "public_query.txt"
DASHBOARD_QUERY_FILENAME = "dashboard_url_query.txt"
CHARTS_QUERY_FILENAME = "charts_query.txt"
REQUIREMENTES_QUERY_FILENAME = "requirements_query.txt"

pattern = '^git@'
repo_url = parser.parse_args().repo_url
type_url = "ssh" if re.match(pattern, repo_url) else "http"
if type_url == "ssh":
    repo_url = repo_url.replace(".git", "/tree/master/").replace(":", "/").replace("git@", "https://")
else:
    repo_url = repo_url.replace(".git", "/tree/master/")

apply_url = lambda path_name: f"{repo_url}{path_name}"

df_data = pd.DataFrame()


with open(TITLE_QUERY_FILENAME) as file_title:
    raw_title = file_title.readlines()

folders = []
titles = []
urls = []
for line in raw_title:
    path, line_number, name = line.split(":")
    if line_number == '1':
        urls.append(apply_url(path.replace("/README.md", "")))
        folders.append(path.replace("/README.md", "").replace("templates/",""))
        titles.append(name.replace("# ", "").replace('\n', ""))


df_data["path"] = folders
df_data["title"] = titles
df_data["template_url"] = urls
number_templates = df_data.shape[0]

df_data["type"] = "Free Product"
df_data["stakeholder"] = "Shimoku Area"


with open(PUBLIC_QUERY_FILENAME) as file_public:
    raw_public = file_public.readlines()

is_public = [False] * number_templates
for line in raw_public:
    path, _, public = line.split(":")
    _, folder, _ = path.split("/")
    public = bool(public.split("is_public=")[1].replace(")", ""))
    index = df_data[df_data["path"]==folder].index.values[0]
    is_public[index] = public

df_data["public"] = is_public


with open(DASHBOARD_QUERY_FILENAME) as file_url:
    raw_url = file_url.readlines()

dashboard_url = [None] * number_templates
for line in raw_url:
    path, _, url = line.split(":", 2)
    _, folder, _ = path.split("/")
    url = url.split("](")[1].replace(")\n", "").replace(") \n", "")
    index = df_data[df_data["path"]==folder].index.values[0]
    dashboard_url[index] = url

df_data["dashboard_url"] = dashboard_url

blacklist = pd.read_csv("templates/key_results/data/nocharts_SDK.csv")

with open(CHARTS_QUERY_FILENAME) as file_charts:
    raw_charts = file_charts.readlines()

dict_charts = {}
for line in raw_charts:
    path, _, chart = line.split(":")
    folder = path.split("/")[1]
    chart = re.findall(r'plt\.\w+', chart)
    chart = chart[0].replace("(","").replace("plt.","")
    if not folder in dict_charts.keys():
        dict_charts[folder] = {chart: 1}
    else:
        if not chart in dict_charts[folder].keys():
            dict_charts[folder] |= {chart: 1}
        else:
            dict_charts[folder][chart] += 1
charts = []
charts_number = []
for each in folders:
    charts.append(" ".join([f"{key} {dict_charts[each][key]}" for key in dict_charts[each]]))
    charts_number.append(len(dict_charts[each]))
df_data["charts"] = charts
df_data["charts_number"] = charts_number

with open(REQUIREMENTES_QUERY_FILENAME) as file_requirements:
    raw_requirements = file_requirements.readlines()

patron = r'([0-9]+\.){2}[0-9]+'
versions =  [None] * number_templates
for line in raw_requirements:
    path, _, version = line.split(":", 2)
    _, folder, _ = path.split("/")
    version = version.split("==")[1].replace("\n", "")
    index = df_data[df_data["path"]==folder].index.values[0]
    verify_version = re.match(patron, version)
    if verify_version == None:
        if re.match(r'[0-9]+\.[0-9]+', version): version = version + ".0"
    versions[index] = version
df_data["version"] = versions

analysis_date = [dt.datetime.today().date()] * number_templates
df_data["analysis_date"] = analysis_date


df_data.to_csv("data_templates.csv",
    index=False,
    columns=[
        "title",
        "type",
        "stakeholder",
        "public",
        # "publication_date",
        "dashboard_url",
        "template_url",
        "charts",
        "charts_number",
        "version",
        "analysis_date",
        # "developer",
    ],
)