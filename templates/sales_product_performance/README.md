# Sales Product Performance Overview Template

## Introduction

Welcome to our GitHub repository!
<br>
📊 Dive into sales product performance analytics with us! 
<br>
🚀 Explore metrics & insightful charts.

Experience Our Dashboard: [Sales Product Performance Dashboard](https://shimoku.io/0d3fba0c-90c1-41aa-a3b7-187adc55ea62/overview?shared=true&token=56b388bd-ab3d-11ee-bc1e-990ca51218f0)

<p align="center">
  <img src="img/capture.png">
</p>

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