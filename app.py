import streamlit as st
import mysql.connector
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Branch Based Sales Dashboard",
    layout="wide",
    page_icon="📊"
)

#Initializing Database
def get_connection():
    return mysql.connector.connect(  
    host = 'localhost',
    user = 'root',
    password = 'your_password',
    database = 'branch_based_sales_management_system')

connection = get_connection()

# Initialize session_state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.branch_id = None
    st.session_state.username = None
        

# Define Login Function
def login(username,password):
    cursor = connection.cursor(dictionary=True)
    query = "select * from users where username=%s and password=%s"
    cursor.execute(query,(username,password))
    result = cursor.fetchone()
    cursor.close()
    return result

# Login UI
def login_page():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.header("Login")
        
        username = st.text_input("Username")
        password = st.text_input("Password" , type ="password", max_chars=40 )

        if st.button("Login",type="primary"):
            result = login(username,password)
            if result:
                st.session_state.logged_in = True
                st.session_state.role = result['role']
                st.session_state.branch_id = result['branch_id']
                st.session_state.username = result['username']
                st.success("Welcome")
                st.rerun()
            else:
                st.error("Invalid Username or Password")

# Dashboard
def dashboard():
    #sidebar content
    st.sidebar.header("Navigation")
    
    options = st.sidebar.radio("Go To",["Dashboard & Reports","Data Entry Workspace","Advanced SQL Engine"])
    
    if options == "Dashboard & Reports":
             
            #Dashboard header
            st.header("🧑‍🎓 Student Enrollment dashboard")
            
            # Filters
            st.subheader("Filter Controls")  
        
            # Fetch Branches
            branches_df = pd.read_sql("select branch_id,branch_name from branches",connection)
            sales_df = pd.read_sql("select * from customer_sales",connection)
            product_name_df = pd.read_sql("select distinct product_name from customer_sales",connection)
            
            col1,col2,col3,col4 = st.columns(4)
            with col1:
                if st.session_state.role == "Super Admin":
                    selected_branch = st.selectbox("Branch Name", ["All"] + branches_df["branch_name"].tolist())
                else:
                    branch_name = branches_df.loc[branches_df["branch_id"] == st.session_state.branch_id,"branch_name"].iloc[0]
                    selected_branch = st.selectbox("Branch Name",[branch_name])         
            with col2:
                selected_product = st.selectbox("Product name",["All"] + product_name_df["product_name"].tolist())
            with col3:
                start_date = st.date_input("Start Date")
            with col4:
                end_date = st.date_input("End Date")
        
            # Apply filters
            filtered_df = sales_df.copy()
        
            if selected_branch != "All":
                branch_id = int(branches_df.loc[branches_df["branch_name"] == selected_branch, "branch_id"].iloc[0])
                filtered_df = filtered_df[filtered_df["branch_id"] == branch_id]
        
            if selected_product != "All":
                filtered_df = filtered_df[filtered_df["product_name"] == selected_product]
        
            if start_date and end_date:
                filtered_df['date'] = pd.to_datetime(filtered_df["date"]).dt.date
                filtered_df = filtered_df[(filtered_df["date"] >= (start_date)) &
                                (filtered_df["date"] <= (end_date))]
        
            # KPIs
            total_gross = filtered_df["gross_sales"].sum()
            total_recieved = filtered_df["recieved_amount"].sum()
            total_pending = filtered_df["pending_amount"].sum()
        
            pending_percentage = (total_pending / total_gross * 100) if total_gross > 0 else 0
        
            col1,col2,col3,col4 = st.columns(4)
            with col1:
                st.metric("Total Revenue(Gross)",f"{total_gross:,.2f}")
            with col2:
                st.metric("Total Recieved",f"{total_recieved:,.2f}")
            with col3:
                st.metric("Total Pending",f"{total_pending:,.2f}")
            with col4:
                st.metric("Pending percentage",f"{pending_percentage:,.2f}%")
        
        
            # Show filtered table
            st.subheader("Customer Sales Summary")
            st.dataframe(filtered_df, use_container_width=True)  
        
        
    elif options == "Data Entry Workspace":
        st.header("🧾 Data Entry Workspace")

        tab1,tab2 = st.tabs(["Add New Sales Entry","Log Payment Split Details"])

        with tab1:
            st.subheader("New Sale Generation")            

            with st.form("new_sale_form",clear_on_submit=True,border=False):
                branches_df = pd.read_sql("Select branch_id,branch_name from branches",connection)   
                
                if st.session_state.role == "superadmin":                    
                    branch_name = st.selectbox("Select Target Branch",branches_df["branch_name"].tolist())
                    branch_id = int(branches_df.loc[branches_df["branch_name"] == branch_name, "branch_id"].iloc[0])  
                else:
                    branch_id = st.session_state.branch_id
                   

                col1,col2 = st.columns(2)
                with col1:
                    student_name = st.text_input("Student Name")
                with col2:
                    product_name_df = pd.read_sql("select distinct product_name from customer_sales",connection)
                    product_name = st.selectbox("Select Course Name",product_name_df["product_name"].tolist())

                col5,col6 = st.columns(2)
                with col5:
                    mobile_number = st.text_input("Mobile Number")
                with col6:
                    joining_date = st.date_input("Joining Date")

                gross_sales = st.number_input("Gross Sales Amount",min_value=0.00,step=100.0,format="%.2f")

                status = st.selectbox("Initial Order Status",["Open","Close"])

                submitted = st.form_submit_button("Publish Sale Entry",type="primary")

                if submitted:
                    pending_amount = gross_sales
                    cursor = connection.cursor()
                    query = """INSERT INTO customer_sales 
                        (branch_id, date, name, mobile_number, product_name, gross_sales, recieved_amount, status) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(query,(branch_id, joining_date, student_name, mobile_number,
                                product_name, gross_sales,0.0, status))
                    connection.commit()
                    cursor.close()
                    st.success("New Sale entry published successfully!")            

        with tab2:
            st.subheader("Post Payment Installment Split")
            with st.form("payment_split_form",clear_on_submit=True,border=False):
                    
                active_sales_df = pd.read_sql("select sale_id, name, product_name, pending_amount from customer_sales where pending_amount > 0",connection)
                    
                if active_sales_df.empty:
                    st.info("No active sales with pending amounts")
                else:
                    sale_options = [f"ID{row.sale_id} - {row.name}({row.product_name}) - ₹{row.pending_amount:.2f} Pending"
                                        for row in active_sales_df.itertuples()]
                    selected_sale = st.selectbox("Select Target Active Sale ID Asset",sale_options)

                    import re
                    sale_id = int(re.search(r'ID(\d+)', selected_sale).group(1))

                    channel = st.selectbox("Payment Collection Channel",["Cash","Card","UPI","Bank Transfer"])
                    split_amount = st.number_input("Collected Split Amount Balance (₹)",min_value=0.0, step=100.0, format="%.2f")
                    payment_date = st.date_input("Payment Date")

                    if st.form_submit_button("Apply Payment Allocation", type="primary"):
                        cursor = connection.cursor()

                            # Update sale record
                        cursor.execute(
                                """
                                INSERT INTO payment_splits (sale_id, amount_paid, payment_method, payment_date)
                                VALUES (%s, %s, %s, %s)
                                 """,
                                (sale_id, split_amount, channel, payment_date)
                            )
                        connection.commit()
                        cursor.close()

                        st.success(f"✅ Payment of ₹{split_amount:.2f} applied to Sale ID {sale_id}")


    elif options == "Advanced SQL Engine":
        st.header("🔎 Execute Predefined SQL Queries")

        query = {
            "Retrieve all records from the customer_sales table":
                "SELECT * FROM customer_sales",

            "Retrieve all records from the branches table":
                "SELECT * FROM branches",

            "Retrieve all records from the payment_splits table":
                "SELECT * FROM payment_splits",

            "Display all sales with status = 'Open'":
                "SELECT * FROM customer_sales WHERE status = 'Open'",

            "Calculate the total gross sales across all branches":
                "SELECT SUM(gross_sales) AS total_gross_sales FROM customer_sales",

            "Calculate the total received amount across all sales":
                "SELECT SUM(recieved_amount) AS total_received FROM customer_sales",

            "Calculate the total pending amount across all sales":
                "SELECT SUM(pending_amount) AS total_pending FROM customer_sales",

            "Count the total number of sales per branch":
                "SELECT branch_id, COUNT(*) AS total_sales FROM customer_sales GROUP BY branch_id",

            "Retrieve sales details along with the branch name":
                "SELECT cs.sale_id, cs.name, cs.product_name, cs.gross_sales, cs.recieved_amount, cs.pending_amount, cs.status, b.branch_name "
                "FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id",

            "Retrieve sales details along with total payment received (using payment_splits)":
                "SELECT cs.sale_id, cs.name, cs.product_name, cs.gross_sales, IFNULL(SUM(ps.amount_paid),0) AS total_payment_received "
                "FROM customer_sales cs LEFT JOIN payment_splits ps ON cs.sale_id = ps.sale_id "
                "GROUP BY cs.sale_id, cs.name, cs.product_name, cs.gross_sales",

            "Show branch-wise total gross sales (using JOIN & GROUP BY)":
                "SELECT b.branch_name, SUM(cs.gross_sales) AS branch_total_gross_sales "
                "FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id "
                "GROUP BY b.branch_name",

            "Display sales along with payment method used":
                "SELECT cs.sale_id, cs.name, cs.product_name, ps.payment_method, ps.amount_paid, ps.payment_date "
                "FROM customer_sales cs JOIN payment_splits ps ON cs.sale_id = ps.sale_id",

            "Find sales where the pending amount is greater than 5000":
                "SELECT * FROM customer_sales WHERE pending_amount > 5000",

            "Retrieve top 3 highest gross sales":
                "SELECT * FROM customer_sales ORDER BY gross_sales DESC LIMIT 3",

            "Find the branch with highest total gross sales":
                "SELECT b.branch_name, SUM(cs.gross_sales) AS total_gross_sales "
                "FROM customer_sales cs JOIN branches b ON cs.branch_id = b.branch_id "
                "GROUP BY b.branch_name ORDER BY total_gross_sales DESC LIMIT 1"
                }

        selected_query = st.selectbox(
            "Select a query",list(query.keys())
        )

        if st.button("Execute Code",type="primary"):
            sql = query[selected_query]
            try:
                df = pd.read_sql(sql,connection)                   
                st.toast("Query Executed **Success !**",icon="✅")
                st.code(query[selected_query], language="sql")
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error executing query: {e}")
    


    
    st.sidebar.divider()

    st.sidebar.write(f"👨‍💻 User: **{st.session_state.username}**")
    st.sidebar.write(f"🔑 Role: **{st.session_state.role}**")
    
    #logout
    if st.sidebar.button("Logout",use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
   
# Condition
if st.session_state.logged_in:
    dashboard()
else:
    login_page()
