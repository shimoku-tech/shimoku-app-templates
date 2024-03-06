# Sales Product Performance Overview Template

## Introduction

Welcome to our GitHub repository!

📊 Dive into sales product performance analytics with us! 

🚀 Explore metrics & insightful charts. 

📈 See our dashboard [eCommerce - Sales Product Performance](https://shimoku.io/a2771688-f696-46b1-9d6a-464e854a7a61/overview?shared=true&token=03b0c41a-c4f7-11ee-9543-50e549d07122)


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
cd templates/sales_product_performance
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

The data was randomly generated using the `generate_data` function located in `data/generate_sales_product_performance.py`

If you want to generate new dataframes please go to data folder, import and run the function

```python
from data.generate_sales_product_performance import generate_data
# updates .csv files in data/ folder with new data
generate_data()
```