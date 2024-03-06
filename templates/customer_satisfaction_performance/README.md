# Customer Satisfaction Performance Dashboard

This dashboard showcases the capabilities of the Shimoku SDK within the context of the Customer Satisfaction Performance. The dataset focuses on customer satisfaction metrics, including order ratings. The dashboard provides insights into customer satisfaction, order performance, revenue analysis, and more, all on a month-to-month basis. It offers a comprehensive view of customer satisfaction and business performance over time.

Experiencie our Dashboard: [Customer Satisfaction Performance Dashboard](https://shimoku.io/07c15316-4817-4ec4-aa6f-6fe0446b6efc/customer-satisfaction-performance?shared=true&token=c90443cf-c510-11ee-8fa6-f4c88a8a3fad) 

📅 Published on 2024-02-06 by [@arturolinares24](https://www.github.com/arturolinares24)

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
cd templates/customer_satisfaction_performance
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
python3 data/generate_customer_satisfaction_performance.py
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
