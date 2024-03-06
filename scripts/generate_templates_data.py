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
PUBLIC_DATE_DEVELOPER_QUERY_FILENAME = "public_date_developer_query.txt"

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
        path = path.replace("/README.md", "")
        urls.append(apply_url(path))
        folders.append(path.replace("templates/",""))
        titles.append(re.sub("# |\n", "", name))

df_data["path"] = folders
df_data["title"] = titles
df_data["template_url"] = urls
number_templates = df_data.shape[0]

df_data["type"] = "Free Product"
df_data["stakeholder"] = "Shimoku Area"


with open(PUBLIC_DATE_DEVELOPER_QUERY_FILENAME) as file_public_date:
    raw_public_date = file_public_date.readlines()
public_date = [None] * number_templates
developers = [None] * number_templates
for line in raw_public_date:
    path, _, info = line.split(":", 2)
    _, folder, _ = path.split("/")
    _, date, devs = re.split(r"Published on | by ", info)
    date = date.replace("/", "-")
    devs = re.findall(r"\[@\S+\]", devs)
    devs = " ".join([re.sub(r"\[@|\]", "", dev) for dev in devs])
    index = df_data[df_data["path"]==folder].index.values[0]
    public_date[index] = dt.datetime.strptime(date, '%Y-%m-%d').date()
    developers[index] = devs

df_data["public_date"] = public_date
df_data["developer"] = developers


with open(PUBLIC_QUERY_FILENAME) as file_public:
    raw_public = file_public.readlines()

is_public = [False] * number_templates
for line in raw_public:
    path, _, public = line.split(":")
    _, folder, _ = path.split("/")
    public = re.findall(r"True|False", public)[0]
    public = True if public == "True" else False
    index = df_data[df_data["path"]==folder].index.values[0]
    is_public[index] = public

df_data["public"] = is_public


with open(DASHBOARD_QUERY_FILENAME) as file_url:
    raw_url = file_url.readlines()

dashboard_url = [None] * number_templates
for line in raw_url:
    path, _, url = line.split(":", 2)
    _, folder, _ = path.split("/")
    url = re.findall(r"\(\S+\)", url)[0]
    url = re.sub(r"\(|\)", "", url)
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
    chart = re.findall(r'plt\.\w+', chart)[0]
    chart = re.sub(r"\(|plt\.", "",chart)
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

versions =  [None] * number_templates
for line in raw_requirements:
    path, _, version = line.split(":", 2)
    _, folder, _ = path.split("/")
    version = re.findall(r"\d+\.\d+\.*\d*", version)[0]
    index = df_data[df_data["path"]==folder].index.values[0]
    verify_version = re.match(r'([0-9]+\.){2}[0-9]+', version)
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
        "developer",
        "public",
        "public_date",
        "charts_number",
        "version",
        "analysis_date",
        "charts",
        "dashboard_url",
        "template_url",
    ],
)