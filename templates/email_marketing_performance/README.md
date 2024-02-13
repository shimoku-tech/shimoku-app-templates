# Email Marketing Performance

## Introduction

Welcome to our GitHub repository!

📊 Dive into user activity analytics with us!

🚀 Explore metrics & insightful charts.

📈 See our dashboard [Email Marketing Performance Template](https://shimoku.io/dac14dbb-226c-474d-8e5b-e0990bcbd5ef/overview?shared=true&token=50162748-caa6-11ee-a068-00155d66fd83)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system. You can download it from python.org.

- pip (Python Package Installer), should come installed with Python.


## Installation

Follow these steps to set up the project locally.


### Clone the repository:

```
git clone https://github.com/shimoku-tech/shimoku-app-templates.git
```
```
cd templates/email_marketing_performance
```

Create a virtual environment:

```
python3 -m venv venv
```

On Windows, you might need to use python instead of python3.

Activate the virtual environment:

On Linux/Mac:

```
source venv/bin/activate
```

On Windows:
```
 .\venv\Scripts\activate
```

Install the required packages:

```
pip install -r requirements.txt
```


## Configuring Environment Variables

The project requires certain environment variables to be set. These variables can be found in the .env.example file. To set them up:

Create a new file in the project root directory named .env.
Copy all content from .env.example to .env.

Replace the empty values with your specific configurations:
```
API_TOKEN=""
UNIVERSE_ID=""
WORKSPACE_ID=""
```


## Running the Application

Once the installation is done, and environment variables are set, you can run the application:

```
python3 main.py
```

## Generation of data

The data was randomly generated using the `generate_data` function located in `data/generate_email_marketing_performance.py`

If you want to generate new dataframes please go to data folder, import and run the function

```python
from data.generate_email_marketing_performance import generate_data
# updates .csv files in data/ folder with new data
generate_data()
```

## Screenshots

![Email Marketing Performance](img/email_marketing_performance.png)
![Email Marketing Performance](img/email_marketing_performance_campaign.png)