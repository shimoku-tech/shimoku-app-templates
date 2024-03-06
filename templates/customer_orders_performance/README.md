# Customer Orders Performance template

## Introduction

Welcome to our GitHub repository!

📊 Dive into customer orders analytics with us!

🚀 Explore metrics & insightful charts.

📈 See our dashboard [Customer Orders Performance Template](https://shimoku.io/82535397-e791-4559-9e49-cbe983c2f8ba/customer-orders-performance?shared=true&token=c274a6da-c4f6-11ee-88fa-00155d9e011f)

![Screanshot 1](img/customer_orders_performance.png)

📅 Published on 2024-02-06 by [@jkahnc](https://www.github.com/jkahnc)

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
cd templates/customer_orders_performance
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

The data was randomly generated using the `generate_data` function located in `data/generate_customer_orders_performance.py`

If you want to generate new dataframes please go to data folder, import and run the function

```python
from data.generate_customer_orders_performance import generate_data
# updates .csv files in data/ folder with new data
generate_data()
```
