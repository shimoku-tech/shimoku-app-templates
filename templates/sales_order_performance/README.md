# Sales Order Performance Dashboard

This dashboard showcases the capabilities of the Shimoku SDK using the context of Sales Order Performance. The dataset revolves around sales orders, expenses, and the visualization of monthly income and expenses, along with the corresponding profits, over time. The analysis provides a comprehensive view of the financial performance on a month-to-month basis.

Experiencie our Dashboard: [Sales Orders Performance Dashboard](https://shimoku.io/c5553c8c-c960-4090-853d-df8b9501af3f/overview?shared=true&token=ad53cec2-ab31-11ee-a2d5-517a12806ea2) 

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
cd templates/sales_order_performance
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

Replace the empty values with your specific configurations:
```
API_TOKEN=""
UNIVERSE_ID=""
WORKSPACE_ID=""
```

## Generate example dataset

To generate the example dataset, execute the following command:

```
python3 generate_sales_orders_performance.py
```

## Running the Application

After completing the dataset generation and ensuring that the environment variables are correctly set, you can launch the application using the following command:

```
python3 app.py
```

## Screens

<p align="center">
  <img src="img/screen.JPG">
</p>
