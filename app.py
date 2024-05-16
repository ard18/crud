import streamlit as st
import mysql.connector

# Establish connection to MySQL Server

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "credence",
    database = "crud_new1",
)

curs = db.cursor()
if curs:
    print("Connection Established")
else:
    print("Connection Failed")

# Streamlit app
st.title("CRUD Operations with MySQL")
# CRUD Operations
option = st.sidebar.selectbox("Select an operation", ("Create Table","Delete Table","Create","Read","Update","Delete"))

if option == "Create":
    st.subheader("Create a Record:")
    name = st.text_input("Enter the name:")
    email = st.text_input("Enter the email:")
    if st.button("Create"):
        insert_query = "insert into users (name, email) values (%s, %s)"
        val = (name, email)
        curs.execute(insert_query, val)
        db.commit()
        st.success("Record Created!")

elif option == "Read":
    st.subheader("Read Records:")
    if st.button("Read"):
        read_query = "select * from users"
        curs.execute(read_query)
        records = curs.fetchall()
        for i in records:
            st.write(i[0],":\t",i[1],":\t",i[2])

elif option == "Update":
    st.subheader("Update a record:")
    id_prime = st.number_input("Enter the identity:", min_value = 1)
    option = st.selectbox("Select the field to be updated",("1 - Name","2 - Email","3 - Both name and email"))
    if option == "1 - Name":
        name = st.text_input("Enter new name:")
        val = (name, id_prime)
        if st.button("Update"):
            update_query = "update users set name = %s where id = %s"
            curs.execute(update_query, val)
            db.commit()
            st.success("Name in record modified!")
    
    elif option == "2 - Email":
        email = st.text_input("Enter new email:")
        val = (email, id_prime)
        if st.button("Update"):
            update_query = "update users set email = %s where id = %s"
            curs.execute(update_query, val)
            db.commit()
            st.success("Email in record modified!")

    elif option == "3 - Both name and email":
        name = st.text_input("Enter new name:")
        email = st.text_input("Enter new email:")
        val = (name, email, id_prime)
        if st.button("Update"):
            update_query = "update users set name = %s, email = %s where id = %s"
            curs.execute(update_query, val)
            db.commit()
            st.success("Name and Email in record modified!")

elif option == "Delete":
    st.subheader("Delete a record:")
    id_prime = st.number_input("Enter the identity:", min_value = 1)
    if st.button("Delete"):
        delete_query = "delete from users where id = %s"
        val = (id_prime,)
        curs.execute(delete_query, val)
        db.commit()
        st.success("Record deleted!")

elif option == "Create Table":
    st.subheader("Create a table:")
    if st.button("Create"):
        create_query = "create table users (    id int auto_increment,     name varchar(50),       email varchar(50),      primary key(id))"
        curs.execute(create_query)
        db.commit()
        st.success("Table created!!")

elif option == "Delete Table":
    st.subheader("Delete existing table:")
    if st.button("Delete"):
        drop_query = "drop table users"
        curs.execute(drop_query)
        db.commit()
        st.success("Table deleted!!")

curs.close()
db.close()

