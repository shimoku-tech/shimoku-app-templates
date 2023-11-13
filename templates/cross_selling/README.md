Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.x installed on your system. You can download it from python.org.
pip (Python Package Installer), should come installed with Python.
Installation
Follow these steps to set up the project locally.

Clone the repository:

git clone https://github.com/your_username/your_project.git
cd your_project

Create a virtual environment:

python3 -m venv venv

On Windows, you might need to use python instead of python3.
Activate the virtual environment:

On Linux/Mac:

source venv/bin/activate

On Windows:

.\venv\Scripts\activate

Install the required packages:

pip install -r requirements.txt

Configuring Environment Variables
The project requires certain environment variables to be set. These variables can be found in the .env.example file. To set them up:

Create a new file in the project root directory named .env.

Copy all content from .env.example to .env.

Replace the empty values with your specific configurations:

API_TOKEN: Your API token.
UNIVERSE_ID: Your Universe ID.
WORKSPACE_ID: Your Workspace ID.
Leave ENVIRONMENT as "develop" for development purposes.

Your .env file should look like this (with your values):

makefile
Copy code
ENVIRONMENT="develop"

# SHIMOKU
API_TOKEN="your_api_token"
UNIVERSE_ID="your_universe_id"
WORKSPACE_ID="your_workspace_id"
Running the Application
Once the installation is done, and environment variables are set, you can run the application:

css
Copy code
python3 main.py
On Windows, you might need to use python instead of python3.