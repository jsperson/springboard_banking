## Table of Contents
- [Table of Contents](#table-of-contents)
- [Description](#description)
- [Data Model](#data-model)
- [Getting Started](#getting-started)
- [Instructions](#instructions)

## Description
This is a simple banking application that uses SQLAlchemy ORM
## Data Model
SQLAlchemy ORM is used to manage a SQLite database. The database is (re)initialized on package execution. This is solely for expedience as the goal is to demonstrate knowledge of OOP and data persistence. 
## Getting Started
Setup (two options): 
1. pip install -r requirements.txt
2. Install the contents of requirements.txt using your package manager of choice
## Instructions
Execute: python.exe banking.py
| Option                   | Description                                                          |
| ------------------------ | -------------------------------------------------------------------- |
| 0 - End Session          | Closes DB connection and ends the session                            |
| 1 - List Customers       | List customers in the database (initialized with two)                |
| 2 - Set Current Customer | Set the current customer (select from the list after using option 1) |
| 3 - Deposit              | Increases the account balance by the entered amount                  |
| 4 - Withdrawal           | Decreases the account balance by the entered amount                  |

___
Project format adapted from [The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/structure/).