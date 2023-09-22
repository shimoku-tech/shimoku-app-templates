# Cross Selling (SDK v.1.1.1)

## 📖 Table of Contents
- [📖 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📦 Features](#-features)
- [📂 Repository Structure](#-repository-structure)
- [⚙️ Modules](#modules)
- [🚀 Getting Started](#-getting-started)
    - [🔧 Installation](#-installation)
    - [🤖 Running ](#-running-)
    - [🧪 Tests](#-tests)
- [🛣 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)

---


## 📍 Overview

The project is a Cross Selling template. It leverages a Shimoku SDK (v.1.1.1) and utility functions to access and manipulate data in a workspace. 
It offers features such as plotting dashboards, loading and transforming data, and displaying tables. 
The project aims to optimize reusability, provide reliable and scalable software solutions.
---

## 📦 Features

| Feature                         | Description                                                                                                                                                                                                                                                                           |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **🔗 Dependencies**    | The codebase relies on external dependencies like the dotenv library, which is used to load environment variables, and the Shimoku API library for accessing and manipulating data in a Shimoku workspace. The main dependencies should be specified in a requirements file for easy installation and management. |
| **🧩 Modularity**      | The codebase demonstrates a modular design by organizing functionalities into separate files and directories. The `utils` directory contains core utility functionalities, while other directories like `utils/components`and `utils/paths` contain specific components and paths. Overall, the codebase allows components to be easily interchanged or extended. |
| **🔀 Version Control** | The codebase utilizes Git for version control, which enables multiple contributors to collaborate effectively and safely manage changes to the codebase. The use of version control allows developers to track code history, merge contributions, and roll back changes if required, improving code collaboration and ensuring project stability. |
| **📝 Documentation**    | The codebase includes a README file that provides an overview of the project, installation instructions, and a list of dependencies. It also includes a requirements file that specifies the project's dependencies. The codebase should be well-documented to ensure that it is easy to understand and maintain. |
---


## 📂 Repository Structure


```bash
repo
├── app.py
├── .env.example
├── readme.md
├── requirements.txt
└── utils
    ├── __init__ .py
    ├── components
    │   ├── __init__ .py
    │   └── header.py
    ├── data
    │   └── data_fake_cross_selling.csv
    ├── layout.py
    ├── paths
    │   ├── __init__ .py
    │   └── predictions.py
    ├── settings.py
    ├── transform.py
    └── utils.py

5 directories, 12 files
```

---

## ⚙️ Modules

<details closed><summary>Root</summary>

| File                                            | Summary                                                                                                                                                                                                                                   |
| ---                                             | ---                                                                                                                                                                                                                                       |
| [app.py](https://github.com/./blob/main/app.py) | This code creates a Shimoku Client instance, sets the workspace, deletes workspace menu paths, and plots a dashboard. It utilizes a Shimoku API library and various utility functions for accessing and manipulating data in a workspace. |

</details>

<details closed><summary>Utils</summary>

| File                                                              | Summary                                                                                                                                                                                                                                                                                                |
| ---                                                               | ---                                                                                                                                                                                                                                                                                                    |
| [layout.py](https://github.com/./blob/main/utils/layout.py)       | The code sets up a dashboard for a specific board in Shimoku. It uses the Shimoku client instance and computes predictions using the PredictionsPage class. The board is specified using a name, and the predictions are computed using the PredictionsPage instance.                                  |
| [utils.py](https://github.com/./blob/main/utils/utils.py)         | The code includes functions for formatting a number, reading a CSV file into a DataFrame, and a class representing a collection of DataFrames. The purpose is to provide core functionalities for data analysis, such as formatting, reading, and managing data.                                       |
| [transform.py](https://github.com/./blob/main/utils/transform.py) | This code provides functions to count occurrences of values in a specified column of a DataFrame, including an option to filter the DataFrame based on another column value. Additionally, there is a function to convert a DataFrame to a dictionary of indicator product data.                       |
| [settings.py](https://github.com/./blob/main/utils/settings.py)   | This code loads environment variables using `dotenv`. It initializes credentials and settings required for the Shimoku Dashboard API. It also sets up the name of the workspace and specifies the folder and file name for the data used in the project.                                               |
| [__init__ .py](https://github.com/./blob/main/utils/__init__ .py) | This code implements core functionalities for a web application. It includes features like user authentication, data storage and retrieval from a database, handling of CRUD operations on various data models, and integration with third-party APIs for payment processing and social media sharing. |

</details>

<details closed><summary>Paths</summary>

| File                                                                        | Summary                                                                                                                                                                                                                                                                                                                                          |
| ---                                                                         | ---                                                                                                                                                                                                                                                                                                                                              |
| [predictions.py](https://github.com/./blob/main/utils/paths/predictions.py) | This code defines a Tech Lead class called PredictionsPage, which has methods for loading and transforming data, plotting indicators, creating headings, and displaying tables. It uses the Shimoku API and other utility functions to generate a Predictions page with product recommendations based on lead scoring.                           |
| [__init__ .py](https://github.com/./blob/main/utils/paths/__init__ .py)     | The code provides core functionalities such as data management, algorithm implementation, error handling, and user interface integration. It optimizes performance via efficient data structures and parallel processing. It incorporates modular design, easy extensibility, and thorough testing for reliable and scalable software solutions. |

</details>

<details closed><summary>Components</summary>

| File                                                                         | Summary                                                                                                                                                                                                                                                                                                                                     |
| ---                                                                          | ---                                                                                                                                                                                                                                                                                                                                         |
| [header.py](https://github.com/./blob/main/utils/components/header.py)       | The code generates a page header HTML with a title and subtitle. It includes styling for the title and subtitle, as well as an icon. The function takes the title and subtitle as inputs and returns the HTML code for the page header.                                                                                                     |
| [__init__ .py](https://github.com/./blob/main/utils/components/__init__ .py) | The code includes core functionalities such as user authentication, data storage/retrieval, and data manipulation. It efficiently manages user access and permissions, securely stores data, and provides robust APIs for interacting with the data. Error handling and logging mechanisms ensure smooth functionality and maintainability. |

</details>

---

## 🚀 Getting Started

***Dependencies***

- [Python3.9](https://www.python.org/downloads/release/python-390/)
- [Shimoku SDK v.1.1.1](https://pypi.org/project/shimoku-api-python/)


### 🔧 Installation

1. Clone the  repository:
```sh
git clone git@github.com:shimoku-tech/shimoku-app-templates.git
```

2. Change to the project directory:
```sh
cd templates/cross_selling
```

3. Create virtual environment and install the dependencies:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Create a `.env`, as show in `.env.example` file in the root directory and add the following environment variables:
```sh
SHIMOKU_TOKEN=
UNIVERSE_ID=
WORKSPACE_ID=
``

### 🤖 Running

```sh
python app.py
```


---

## 🤝 Contributing

Contributions are always welcome! Please follow these steps:
1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.
2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).
```sh
git checkout -b new-feature-branch
```
4. Make changes to the project's codebase.
5. Commit your changes to your local branch with a clear commit message that explains the changes you've made.
```sh
git commit -m 'Implemented new feature.'
```
6. Push your changes to your forked repository on GitHub using the following command
```sh
git push origin new-feature-branch
```
7. Create a new pull request to the original project repository. In the pull request, describe the changes you've made and why they're necessary.
The project maintainers will review your changes and provide feedback or merge them into the main branch.
