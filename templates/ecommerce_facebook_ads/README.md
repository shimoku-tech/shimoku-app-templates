# Facebook Ads Template

## Introduction

Welcome to our GitHub repository!

📊 Dive into ecommerce facebook ads analytics with us! 

🚀 Explore metrics & insightful charts. 

📈 See our dashboard [eCommerce - Facebook Ads](https://shimoku.io/e62c4b45-4807-4f26-96a5-477981eb7b48/ad-metrics?shared=true&token=4ac65d00-c520-11ee-9525-50e549d07122)


<p align="center">
  <img src="img/capture.png">
</p>

📅 Published on 2024-02-06 by [@FelipeIdmeShimoku](https://www.github.com/FelipeIdmeShimoku)

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
cd templates/ecommerce_facebook_ads
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

The data was randomly generated using the `generate_data` function located in `data/generate_facebook_ads.py`

If you want to generate new dataframes please go to data folder, import and run the function

```python
from data.generate_facebook_ads import generate_data
# updates .csv files in data/ folder with new data
generate_data()
```