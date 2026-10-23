# Branch-based-sales-management-system

<p>A comprehensive Sales Management Dashboard built using Python, Streamlit, MySQL, and Pandas to manage branch-wise sales operations, payment tracking, customer records, and business analytics through an interactive web interface.</p>

## 📌 Overview

The Branch-based Sales Management System is designed to automatically calculates pending amounts, tracks split payments, monitors branch performance, and provides real-time business insights through an interactive Streamlit dashboard.

The application offers an intuitive dashboard that allows users to:

- Stores branch-wise sales records.
- Tracks customer payments and pending balances.
- Supports split payment transactions.
- Automatically updates financial calculations using database triggers.
- Provides role-based access for Super Admin and Admin users.
- Generates sales and financial reports for business decision-making

## 🚀 Features

- Secure login with session-based authentication
- Role-based dashboard (Super Admin / Admin)
- Add new sales entries (branch-restricted for Admin)
- Add payments with automatic trigger-based balance updates
- Reports dashboard: KPIs, branch comparison, pending payments, sales status, payment method breakdown, monthly trends
- 15 executable predefined SQL queries, organized by category

## 🛠️ Tech Stack

- **Database:** MySQL
- **Backend:** Python (mysql-connector-python)
- **Frontend:** Streamlit
- **Data handling:** pandas

## 🗄️ Database Schema

| Table Name | Columns |
|------------|----------|
| **Branch** | branch_id, branch_name, branch_admin_name |
| **Customer_sales** | sale_id, branch_id, date, name, mobile_number, product_name, gross_sales, recieved_amount, pending_amount, status |
| **Users** | user_id, username, password, branch_id, role, email |
| **Payment_Splits** | payment_id, sale_id, payment_date, amount_paid, payment_method |

## 🎯 Key Design Decisions

#### Generated Column (pending_amt):

This means it recalculates automatically whenever received_amt changes — it's never set manually.

'''sql
pending_amount = gross_sales - recieved_amount
'''

#### Trigger:

- **✅ After Payment Insert:** Update received amount, recalculate pending amount, update payment status
- **✅ After Payment Delete:** Recalculate received amount, recalculate pending amount, update payment status

#### Role-Based Access Control:

Super Admins can access all branches, while Admins are restricted to their assigned branch. Access restrictions are enforced in both the Streamlit UI and SQL queries.

## ⚙️ How to Run This Project

### Clone the repository
   git clone https://github.com/ThereseRansey/sales-management-system.git
   cd sales-management-system
### Install dependencies
   pip install streamlit mysql-connector-python pandas
### Set up the database
- Run the schema/table creation statements from query.sql in MySQL Workbench
- Run the trigger creation statement from query.sql
- Insert your sample data
### Configure your database credentials Create a .streamlit/secrets.toml file in the project folder (not included in this repo for security):

   [mysql]
   host = "localhost"
   user = "root"
   password = "your_password"
   database = "branch_based_sales_management_system"
### Run the app
   streamlit run app.py

## Author
[Syed Mohamed Faize]




