# Saas active users overview template

## Introduction

Welcome to our GitHub repository!

📊 Dive into user engagement analytics with us! 

🚀 Explore metrics & insightful charts. 

🔍 Our Weekly Active Users Bar Chart offers a detailed look at user patterns. Plus, check out our pie chart for Newsletter Subscribers & dynamic line chart for New User Trends. 

📈 See our dashboard [SaaS - Active Users Overview](https://shimoku.io/5491c564-93be-4536-89be-c1cbf4108b3f/users-overview?shared=true&token=706fdb5b-c513-11ee-a004-50e549d07122)

<p align="center">
  <img src="img/1.png">
</p>

📅 Published on 2023-12-09 by [@rotorrest](https://www.github.com/rotorrest)

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
cd templates/saas_active_users_overview
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
