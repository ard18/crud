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
st.title("CRUD++ Operations with MySQL")
# CRUD Operations
option = st.sidebar.selectbox("Select an operation", ("Create Table","Delete Table","Create","Read","Complex Search","Update","Delete"))

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

elif option == "Complex Search":
    option = st.selectbox("Search for a record by:", ("Name","Email"))
    if option == "Name":
        tab1, tab2, tab3 = st.tabs(["Starting Substring","Ending Substring","Containing Substring"])
        with tab1:
            search_query = "select * from users where name like %s"
            inp1 = st.text_input("Enter String:", key="1")

            if st.button("Search", key="11"):
                val = (inp1+"%",)
                curs.execute(search_query, val)
                records = curs.fetchall()
                for i in records:
                    st.write(i[0],":\t",i[1],":\t",i[2])
        
        with tab2:
            search_query = "select * from users where name like %s"
            inp2 = st.text_input("Enter String:", key="2")

            if st.button("Search", key="22"):
                val = ("%"+inp2,)
                curs.execute(search_query, val)
                records = curs.fetchall()
                for i in records:
                    st.write(i[0],":\t",i[1],":\t",i[2])
        
        with tab3:
            search_query = "select * from users where name like %s"
            inp3 = st.text_input("Enter String:", key="3")

            if st.button("Search", key="33"):
                val = ("%"+inp3+"%",)
                curs.execute(search_query, val)
                records = curs.fetchall()
                for i in records:
                    st.write(i[0],":\t",i[1],":\t",i[2])
    
    elif option == "Email":
        st.subheader("Containing Substring")
        search_query = "select * from users where email like %s"
        inp_e = st.text_input("Enter String:", key="4")

        if st.button("Search", key="44"):
            val = ("%"+inp_e+"%",)
            curs.execute(search_query, val)
            records = curs.fetchall()
            for i in records:
                st.write(i[0],":\t",i[1],":\t",i[2])

curs.close()
db.close()

