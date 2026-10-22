# Branch-based-sales-management-system

A comprehensive Sales Management Dashboard built using Python, Streamlit, MySQL, and Pandas to manage branch-wise sales operations, payment tracking, customer records, and business analytics through an interactive web interface.
-----------------------------------------------------------------------------------------------------------------------------

### Features
- Secure login with session-based authentication
- Role-based dashboard (Super Admin / Admin)
- Add new sales entries (branch-restricted for Admin)
- Add payments with automatic trigger-based balance updates
- Reports dashboard: KPIs, branch comparison, pending payments, sales status, payment method breakdown, monthly trends
- 15 executable predefined SQL queries, organized by category
-----------------------------------------------------------------------------------------------------------------------------

### Tech Stack
- Database: MySQL
- Backend: Python (mysql-connector-python)
- Frontend: Streamlit
- Data handling: pandas
-----------------------------------------------------------------------------------------------------------------------------

🗄️ ### Database Schema
## Branches
branch_id
branch_name
branch_admin_name
## Customer Sales
sale_id
branch_id
date
name
mobile_number
product_name
gross_sales
recieved_amount
pending_amount
status
## Users
user_id
username
password
branch_id
role
email
## Payment Splits
payment_id
sale_id
payment_date
amount_paid
payment_method
-----------------------------------------------------------------------------------------------------------------------------

### Key Design Decisions
## Generated Column (pending_amt) pending_amt is defined as gross_sales - received_amt using MySQL's GENERATED ALWAYS AS ... STORED. This means it recalculates automatically whenever received_amt changes — it's never set manually.

## Trigger (trg_update_received_amount) Fires AFTER INSERT on payments. It sums the new payment into received_amt on the matching customer_sales row, which in turn causes pending_amt to recalculate automatically.

## Role-Based Access Control

Super Admin — can view and add sales for all branches
Admin — restricted to their own branch_id, enforced both in the UI and in every SQL query
-----------------------------------------------------------------------------------------------------------------------------

### Automated Business Logic
## Generated Column
pending_amount =
gross_sales - recieved_amount
## Trigger Automation
## After Payment Insert
- Updates received amount
- Recalculates pending amount
- Updates status automatically
## After Payment Delete
- Recalculates received amount
- Recalculates pending amount
- Updates status automatically
-----------------------------------------------------------------------------------------------------------------------------

### How to Run This Project
## Clone the repository
   git clone https://github.com/ThereseRansey/sales-management-system.git
   cd sales-management-system
## Install dependencies
   pip install streamlit mysql-connector-python pandas
## Set up the database
- Run the schema/table creation statements from query.sql in MySQL Workbench
- Run the trigger creation statement from query.sql
- Insert your sample data
## Configure your database credentials Create a .streamlit/secrets.toml file in the project folder (not included in this repo for security):

   [mysql]
   host = "localhost"
   user = "root"
   password = "your_password"
   database = "branch_based_sales_management_system"
## Run the app
   streamlit run app.py
-----------------------------------------------------------------------------------------------------------------------------

### Author
[Syed Mohamed Faize]




