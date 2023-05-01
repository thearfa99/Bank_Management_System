#Imports
from tkinter import *
import os
from PIL import ImageTk, Image
import uuid
import mysql.connector as sc
import time
from datetime import datetime as dt

#Main Screen
master = Tk()
master.title('Bank of Prosperity')

#Functions

#Registration
def register():
    #Vars
    global temp_name
    global temp_pno
    global temp_gender
    global temp_mailid
    global temp_username
    global temp_password
    global temp_confirm    
    global notif
    global ac_no
    global register_screen

    temp_name = StringVar()
    temp_pno = StringVar()
    temp_gender = StringVar()
    temp_mailid = StringVar()
    temp_username = StringVar()
    temp_password = StringVar()
    temp_confirm = StringVar()
    
    #Register Screen
    register_screen = Toplevel(master)
    register_screen.title('Register')

    #Account number
    ac_no= str(uuid.uuid4())

    #Labels
    Label(register_screen, text="Please enter your details below to register", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(register_screen, text="Full Name", font=('Calibri',12)).grid(row=1,sticky=W)
    Label(register_screen, text="Phone number", font=('Calibri',12)).grid(row=2,sticky=W)
    Label(register_screen, text="Gender", font=('Calibri',12)).grid(row=3,sticky=W)
    Label(register_screen, text="Email id", font=('Calibri',12)).grid(row=4,sticky=W)
    Label(register_screen, text="Username", font=('Calibri',12)).grid(row=5,sticky=W)
    Label(register_screen, text="Password", font=('Calibri',12)).grid(row=6,sticky=W)
    Label(register_screen, text="CONFIRM?(Y/N)", font=('Calibri',12)).grid(row=7,sticky=W)
    Label(register_screen, text="Your Account number is: "+ac_no, font=('Calibri',12)).grid(row=8,sticky=W)
    Label(register_screen, text="This window will automatically close once your account is created", font=('Calibri',12)).grid(row=9,sticky=W)
    notif = Label(register_screen, font=('Calibri',12))
    notif.grid(row=12,sticky=N,pady=10)

    #Entries
    Entry(register_screen,textvariable=temp_name).grid(row=1,column=0)
    Entry(register_screen,textvariable=temp_pno).grid(row=2,column=0)
    Entry(register_screen,textvariable=temp_gender).grid(row=3,column=0)
    Entry(register_screen,textvariable=temp_mailid).grid(row=4,column=0)
    Entry(register_screen,textvariable=temp_username).grid(row=5,column=0)
    Entry(register_screen,textvariable=temp_password,show="*").grid(row=6,column=0)
    Entry(register_screen,textvariable=temp_confirm).grid(row=7,column=0)

    #Buttons
    Button(register_screen, text="Register", command = finish_reg, font=('Calibri',12)).grid(row=10,sticky=N,pady=10)
    Button(register_screen, text="EXIT", command = exit_reg, font=('Calibri',12)).grid(row=11,sticky=N,pady=10)

def exit_reg():
    register_screen.destroy()

def finish_reg():
    name = temp_name.get()
    pno = temp_pno.get()
    gender = temp_gender.get()
    mailid = temp_mailid.get()
    username = temp_username.get()
    password = temp_password.get()
    balance = 0.0
    confirm = temp_confirm.get()

    #Pyton SQL connectivity
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()

    #Input constraints
    if name == "" or pno == "" or gender == "" or mailid=="" or username == "" or password == "":
        notif.config(fg="red",text="All fields requried * ")
        return

    elif len(pno)!=10:
        notif.config(fg="red",text="Phone number should be 10 characters long!")
        return

    elif gender not in ["MALE","FEMALE","OTHERS","M","F","O","m","f","o","Male","Female","Others","male","female","others"]:
        notif.config(fg="red",text="Please enter M/F/O in gender")
        return

    #CHECK FOR UNIQUE PH.NO. OR USERID OR MAIL ID
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for m in recs:
        if pno == m[2]:
            notif.config(fg="red",text="A different account is already registered with this phone number!")
            return
        elif username == m[1]:
            notif.config(fg="red",text="A different account is already registered with this username!")
            return
        elif mailid == m[4]:
            notif.config(fg="red",text="A different account is already registered with this mail id!")
            return

    #Pushing data into sql table cinfo
    cur.execute("insert into cinfo values('{}','{}','{}','{}','{}','{}','{}','{}')".format(ac_no,name,pno,gender,mailid,username,password,balance))

    if confirm in ['Y','y','yes','Yes','YES']:
        con.commit()
        time.sleep(1.8)
        register_screen.destroy()
   
    else:
        notif.config(fg="red",text="Please confirm all particulars are correct by typing Y/y")
        return
    con.close()




#Login and related
def login():
    #Vars
    global temp_login_name
    global temp_login_password
    global login_notif
    global login_screen
    temp_login_name = StringVar()
    temp_login_password = StringVar()
    #Login Screen
    login_screen = Toplevel(master)
    login_screen.title('Login')
    #Labels
    Label(login_screen, text="Login to your account", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(login_screen, text="Username", font=('Calibri',12)).grid(row=1,sticky=W)
    Label(login_screen, text="Password", font=('Calibri',12)).grid(row=2,sticky=W)
    login_notif = Label(login_screen, font=('Calibri',12))
    login_notif.grid(row=5,sticky=N)
    #Entry
    Entry(login_screen, textvariable=temp_login_name).grid(row=1,column=1,padx=5)
    Entry(login_screen, textvariable=temp_login_password,show="*").grid(row=2,column=1,padx=5)
    #Button
    Button(login_screen, text="Login", command=login_session, width=15,font=('Calibri',12)).grid(row=3,sticky=W,pady=5,padx=5)
    Button(login_screen, text="EXIT", command=exit_log, width=15,font=('Calibri',12)).grid(row=4,sticky=W,pady=5,padx=5)

def exit_log():
    login_screen.destroy()

def login_session():
    global full_name
    global Acc_no
    global account_dashboard
    login_name = temp_login_name.get()
    login_password = temp_login_password.get()
    pswd=""
    full_name=""
    Acc_no=""
    
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    all_records=cur.fetchall()
    for i in all_records:
        if login_name==i[5]:
            full_name=i[1]
            Acc_no=i[0]
            pswd=i[6]
            if login_password == pswd:
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title('Dashboard')
                #Labels
                Label(account_dashboard, text="Account Dashboard", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
                Label(account_dashboard, text="Welcome "+full_name, font=('Calibri',12)).grid(row=1,sticky=N,pady=5)
                #Buttons
                Button(account_dashboard, text="Personal Details",font=('Calibri',12),width=30,command=personal_details).grid(row=2,sticky=N,padx=10)
                Button(account_dashboard, text="Deposit",font=('Calibri',12),width=30,command=deposit).grid(row=3,sticky=N,padx=10)
                Button(account_dashboard, text="Withdraw",font=('Calibri',12),width=30,command=withdraw).grid(row=4,sticky=N,padx=10)
                Button(account_dashboard, text="Send money",font=('Calibri',12),width=30,command=send).grid(row=5,sticky=N,padx=10)
                Button(account_dashboard, text="Search recent transactions",font=('Calibri',12),width=30,command=search).grid(row=6,sticky=N,padx=10)
                Button(account_dashboard, text="LOG OUT",font=('Calibri',12),width=30,command=logout).grid(row=7,sticky=N,padx=10)
                Label(account_dashboard).grid(row=8,sticky=N,pady=10)
                return
            else:
                login_notif.config(fg="red", text="Password incorrect!!")
                return
    login_notif.config(fg="red", text="No account found !!")
    con.close()

def logout():
    account_dashboard.destroy()


#ACCOUNT DASHBOARD

#Personal info
def personal_details():
    #Vars
    global personal_details_screen
    acno=""
    n=""
    phno=""
    gen=""
    mid=""
    uname=""
    pword=""
    bal=""

    #connectivity
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for j in recs:
        if Acc_no==j[0] and full_name==j[1]:
            acno=j[0]
            n=j[1]
            phno=j[2]
            gen=j[3]
            mid=j[4]
            uname=j[5]
            pword=j[6]
            bal=str(j[7])
            
    #Personal details screen
    personal_details_screen = Toplevel(master)
    personal_details_screen.title('Personal Details')
    
    #Labels
    Label(personal_details_screen, text="Personal Details", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(personal_details_screen, text="ACCOUNT NUMBER : "+acno, font=('Calibri',12)).grid(row=1,sticky=W)
    Label(personal_details_screen, text="FULL NAME : "+n, font=('Calibri',12)).grid(row=2,sticky=W)
    Label(personal_details_screen, text="PHONE NUMBER : "+phno, font=('Calibri',12)).grid(row=3,sticky=W)
    Label(personal_details_screen, text="GENDER :"+gen, font=('Calibri',12)).grid(row=4,sticky=W)
    Label(personal_details_screen, text="MAIL ID :"+mid, font=('Calibri',12)).grid(row=5,sticky=W)
    Label(personal_details_screen, text="USERNAME :"+uname, font=('Calibri',12)).grid(row=6,sticky=W)
    Label(personal_details_screen, text="ACCOUNT BALANCE : Rs "+bal, font=('Calibri',12)).grid(row=7,sticky=W)

    #Button
    Button(personal_details_screen, text="EXIT",font=('Calibri',12),width=30,command=exit_pd).grid(row=9,sticky=N,padx=10)
    con.close()

def exit_pd():
    personal_details_screen.destroy()


#Deposit money
def deposit():
    #Vars
    global amount
    global deposit_notif
    global current_balance_label
    global deposit_screen
    amount = StringVar()

    #Pyton SQL connectivity
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for k in recs:
        if Acc_no==k[0] and full_name==k[1]:
            details_balance = str(k[7])
    con.close()       
    #Deposit Screen
    deposit_screen = Toplevel(master)
    deposit_screen.title('Deposit')
    #Label
    Label(deposit_screen, text="Deposit Funds", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    current_balance_label = Label(deposit_screen, text="Current Balance : Rs."+details_balance, font=('Calibri',12))
    current_balance_label.grid(row=1,sticky=W)
    Label(deposit_screen, text="Amount : ", font=('Calibri',12)).grid(row=2,sticky=W)
    deposit_notif = Label(deposit_screen,font=('Calibri',12))
    deposit_notif.grid(row=4, sticky=N,pady=5)
    #Entry
    Entry(deposit_screen, textvariable=amount).grid(row=2,column=1)
    #Button
    Button(deposit_screen,text="Finish",font=('Calibri',12),command=finish_deposit).grid(row=3,sticky=W,pady=5)
    Button(deposit_screen,text="EXIT",font=('Calibri',12),command=exit_d).grid(row=3,sticky=E,pady=5)
    
def exit_d():
    deposit_screen.destroy()

def finish_deposit():
    if amount.get() == "":
        deposit_notif.config(text='Amount is required!',fg="red")
        return
    if float(amount.get()) <=0:
        deposit_notif.config(text='Negative currency is not accepted', fg='red')
        return

    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for l in recs:
        if Acc_no==l[0] and full_name==l[1]:
            current_balance = str(l[7])
    con.close()
    updated_balance = current_balance
    updated_balance = float(updated_balance) + float(amount.get())
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for m in recs:
        if Acc_no==m[0] and full_name==m[1]:
            cur.execute("update cinfo set balance = %s where acc_no = %s",(updated_balance,Acc_no))
            con.commit()
    con.close()

    current_balance_label.config(text="Current Balance : Rs"+str(updated_balance),fg="green")
    deposit_notif.config(text='Balance Updated', fg='green')

    tad= str(uuid.uuid4())
    sad= Acc_no
    rad = sad
    amd= amount.get()
    nd = dt.now()
    d_td = dt.isoformat(nd)
    med = "Deposit"
    tyd = "d"

    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("insert into transactions values('{}','{}','{}','{}','{}','{}','{}')".format(tad,sad,rad,amd,d_td,med,tyd))
    con.commit()
    con.close()


#Withdraw money
def withdraw():
    #Vars
    global withdraw_amount
    global withdraw_notif
    global current_balance_label
    global withdraw_screen
    withdraw_amount = StringVar()

    #Pyton SQL connectivity
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for k in recs:
        if Acc_no==k[0] and full_name==k[1]:
            details_balance = str(k[7])
    con.close()    

    #withdraw Screen
    withdraw_screen = Toplevel(master)
    withdraw_screen.title('Withdraw')
    #Label
    Label(withdraw_screen, text="Withdraw Funds", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    current_balance_label = Label(withdraw_screen, text="Current Balance : Rs."+details_balance, font=('Calibri',12))
    current_balance_label.grid(row=1,sticky=W)
    Label(withdraw_screen, text="Amount : ", font=('Calibri',12)).grid(row=2,sticky=W)
    withdraw_notif = Label(withdraw_screen,font=('Calibri',12))
    withdraw_notif.grid(row=4, sticky=N,pady=5)
    #Entry
    Entry(withdraw_screen, textvariable=withdraw_amount).grid(row=2,column=1)
    #Button
    Button(withdraw_screen,text="Finish",font=('Calibri',12),command=finish_withdraw).grid(row=3,sticky=W,pady=5)
    Button(withdraw_screen,text="EXIT",font=('Calibri',12),command=exit_w).grid(row=3,sticky=E,pady=5)

def exit_w():
    withdraw_screen.destroy()

def finish_withdraw():
    if withdraw_amount.get() == "":
        withdraw_notif.config(text='Amount is required!',fg="red")
        return
    if float(withdraw_amount.get()) <=0:
        withdraw_notif.config(text='Negative currency is not accepted', fg='red')
        return

    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for l in recs:
        if Acc_no==l[0] and full_name==l[1]:
            current_balance = str(l[7])
    con.close()

    if float(withdraw_amount.get()) >float(current_balance):
        withdraw_notif.config(text='Insufficient Funds!', fg='red')
        return

    updated_balance = current_balance
    updated_balance = float(updated_balance) - float(withdraw_amount.get())
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for m in recs:
        if Acc_no==m[0] and full_name==m[1]:
            cur.execute("update cinfo set balance = %s where acc_no = %s",(updated_balance,Acc_no))
            con.commit()
    con.close()

    current_balance_label.config(text="Current Balance : Rs"+str(updated_balance),fg="green")
    withdraw_notif.config(text='Balance Updated', fg='green')

    #Vars
    ta= str(uuid.uuid4())
    sa= Acc_no
    ra = sa
    am = withdraw_amount.get()
    n = dt.now()
    d_t = dt.isoformat(n)
    me = "withdrawal"
    ty = "w"

    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("insert into transactions values('{}','{}','{}','{}','{}','{}','{}')".format(ta,sa,ra,am,d_t,me,ty))
    con.commit()
    con.close()


#Send money    
def send():
    #Vars
    global send_amount
    global send_notif
    global send_name
    global current_balance_label
    global clicked
    global send_screen
    send_amount = StringVar()
    send_name= StringVar()
    

    #Pyton SQL connectivity
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for k in recs:
        if Acc_no==k[0] and full_name==k[1]:
            details_balance = str(k[7])
    con.close()    

    #send Screen
    send_screen = Toplevel(master)
    send_screen.title('TRANSACTIONS')
    #Label
    Label(send_screen, text="SEND FUNDS", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    current_balance_label = Label(send_screen, text="Current Balance : Rs."+details_balance, font=('Calibri',12))
    current_balance_label.grid(row=1,sticky=W)
    Label(send_screen, text="Receiver's name : ", font=('Calibri',12)).grid(row=2,sticky=W)
    Label(send_screen, text="Amount: ", font=('Calibri',12)).grid(row=3,sticky=W)
    Label(send_screen, text="Choose a method of transaction: ", font=('Calibri',12)).grid(row=4,sticky=W)
    send_notif = Label(send_screen,font=('Calibri',12))
    send_notif.grid(row=7, sticky=N,pady=5)
    #Entry
    clicked = StringVar()
    clicked.set("NEFT")
    options = ["NEFT (National Electronic Fund Transfer)","RTGS (Real Time Gross Settlement)","IMPS (Immediate Payment Service)"]
    Entry(send_screen, textvariable=send_name).grid(row=2,column=1)
    Entry(send_screen,textvariable=send_amount).grid(row=3,column=1)
    OptionMenu(send_screen,clicked,*options).grid(row=4,column=1)
    #Button
    Button(send_screen,text="Finish transaction",font=('Calibri',12),command=finish_send).grid(row=6,sticky=W,pady=5)
    Button(send_screen,text="EXIT",font=('Calibri',12),command=exit_s).grid(row=6,sticky=E,pady=5)

def exit_s():
    send_screen.destroy()

def finish_send():
    #vars
    t_id=str(uuid.uuid4())
    s_acc_no= Acc_no
    r_acc_no = ""
    amt=send_amount.get()
    now = dt.now()
    dnt = dt.isoformat(now)
    method = clicked.get()
    typ = "s"

    #Receiver's acc no
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for i in recs:
        if str(send_name.get())==i[1]:
            r_acc_no += i[0]
    con.close()

    if r_acc_no=="":
        send_notif.config(text='Receiver account not found!',fg="red")
        return        

    #Constraints
    if send_amount.get() == "":
        send_notif.config(text='Amount is required!',fg="red")
        return
    if float(send_amount.get()) <=0:
        send_notif.config(text='Negative currency is not accepted', fg='red')
        return

    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for l in recs:
        if Acc_no==l[0] and full_name==l[1]:
            current_balance = str(l[7])
    con.close()

    if float(send_amount.get()) >float(current_balance):
        send_notif.config(text='Insufficient Funds!', fg='red')
        return

    if clicked == "":
        send_notif.config(text='Please choose a payment method!', fg='red')
        return

    #Appending record into transactions table
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("insert into transactions values('{}','{}','{}','{}','{}','{}','{}')".format(t_id,s_acc_no,r_acc_no,amt,dnt,method,typ))
    con.commit()
    con.close()
    
    #Updating cinfo for sender's balance
    updated_balance = current_balance
    updated_balance = float(updated_balance) - float(send_amount.get())
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for m in recs:
        if Acc_no==m[0] and full_name==m[1]:
            cur.execute("update cinfo set balance = %s where acc_no = %s",(updated_balance,Acc_no))
            con.commit()
    con.close()

    current_balance_label.config(text="Current Balance : Rs"+str(updated_balance),fg="green")
    send_notif.config(text='Balance Updated', fg='green')

    #Updating cinfo for receiver's balance
    r_balance=float(send_amount.get())
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("update cinfo set balance = balance + {} where acc_no = '{}'".format(r_balance,r_acc_no))
    con.commit()


#Search recent transactions
def search():
    #Vars
    global search_screen

    #Search transactions screen
    search_screen = Toplevel(master)
    search_screen.title('Search recent transactions')

    #Labels
    Label(search_screen, text = "BANK OF PROSPERITY", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(search_screen, text = "Search recent transactions", font=('Calibri',14)).grid(row=1,sticky=N)
    Label(search_screen, text = "Your Account number is "+Acc_no, font=('Calibri',14)).grid(row=2,sticky=W,pady=10)
    search_notif = Label(search_screen,font=('Calibri',12))
    search_notif.grid(row=10, sticky=N,pady=5)
    
    #Buttons
    Button(search_screen, text="All transactions",font=('Calibri',12),width=50,command=all_tr).grid(row=4,sticky=N,padx=10)
    Button(search_screen, text="Search by name of receiver",font=('Calibri',12),width=50,command=name_tr).grid(row=5,sticky=N,padx=10)
    Button(search_screen, text="Search by name of sender",font=('Calibri',12),width=50,command=namer_tr).grid(row=6,sticky=N,padx=10)
    Button(search_screen, text="View deposits",font=('Calibri',12),width=50,command=d_tr).grid(row=7,sticky=N,padx=10)
    Button(search_screen, text="View withdrawals",font=('Calibri',12),width=50,command=w_tr).grid(row=8,sticky=N,padx=10)
    Button(search_screen, text="EXIT",font=('Calibri',12),width=50,command=exit_search).grid(row=9,sticky=N,padx=10)

def exit_search():
    search_screen.destroy()


#All recent transactions    
def all_tr():
    from tkinter import ttk
    import tkinter as tk
    #All transactions screen
    all_screen = Toplevel(master)
    all_screen.geometry("1260x230")
    all_screen.title('ALL TRANSACTIONS')

    tree = ttk.Treeview(all_screen, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')

    tree.column("#1", anchor=tk.CENTER)

    tree.heading("#1", text="Transaction id")

    tree.column("#2", anchor=tk.CENTER)

    tree.heading("#2", text="Sender's account number")

    tree.column("#3", anchor=tk.CENTER)

    tree.heading("#3", text="Receiver's account number")

    tree.column("#4", anchor=tk.CENTER)

    tree.heading("#4", text="Amount")

    tree.column("#5", anchor=tk.CENTER)

    tree.heading("#5", text="Date and Time")

    tree.column("#6", anchor=tk.CENTER)

    tree.heading("#6", text="Method")

    tree.column("#7", anchor=tk.CENTER)

    tree.heading("#7", text="Type")

    tree.pack()
    
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from transactions where s_acc_no = '{}' or r_acc_no = '{}' order by dnt desc".format(Acc_no,Acc_no))
    recs=cur.fetchall()
    for i in recs:
        tree.insert("", tk.END, values=i)
    con.close()


#Search by name of reciever  
def name_tr():
    global s_n
    s_n = StringVar()
    global sn_screen
    global sn_notif
    #Search by name transactions screen
    sn_screen = Toplevel(master)
    sn_screen.title('TRANSACTIONS')

    #Label
    Label(sn_screen, text = "BANK OF PROSPERITY", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(sn_screen, text = "Search recent transactions", font=('Calibri',14)).grid(row=1,sticky=N)
    Label(sn_screen, text="Receiver's full name", font=('Calibri',12)).grid(row=3,sticky=W,pady=10)
    sn_notif = Label(sn_screen,font=('Calibri',12))
    sn_notif.grid(row=4, sticky=N,pady=5)
    
    #Entry
    Entry(sn_screen, textvariable=s_n).grid(row=3,column=1)

    #Button
    Button(sn_screen,text="Search",font=('Calibri',12),command=finish_name_tr).grid(row=5,sticky=W,pady=5)
    Button(sn_screen,text="EXIT",font=('Calibri',12),command=exit_name_tr).grid(row=6,sticky=E,pady=5)

def exit_name_tr():
    sn_screen.destroy()

def finish_name_tr():
    from tkinter import ttk
    import tkinter as tk
    rac="" 
    #Name acc no search
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for i in recs:
        if str(s_n.get())==i[1]:
            rac += i[0]
    con.close()
    
    if rac=="":
        sn_notif.config(text='Account not found!', fg='red')
        return
    
    #Checking if any previous records exist
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from transactions where s_acc_no = '{}' and r_acc_no = '{}'".format(Acc_no,rac))
    recs=cur.fetchall()
    if recs == []:
        sn_notif.config(text='No transactions with this account!', fg='red')
        return
    con.close()
    
    #Search by name transactions screen
    sn1_screen = Toplevel(master)
    sn1_screen.title('SEARCH RESULTS')

    tree = ttk.Treeview(sn1_screen, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')

    tree.column("#1", anchor=tk.CENTER)

    tree.heading("#1", text="Transaction id")

    tree.column("#2", anchor=tk.CENTER)

    tree.heading("#2", text="Sender's account number")

    tree.column("#3", anchor=tk.CENTER)

    tree.heading("#3", text="Receiver's account number")

    tree.column("#4", anchor=tk.CENTER)

    tree.heading("#4", text="Amount")

    tree.column("#5", anchor=tk.CENTER)

    tree.heading("#5", text="Date and Time")

    tree.column("#6", anchor=tk.CENTER)

    tree.heading("#6", text="Method")

    tree.column("#7", anchor=tk.CENTER)

    tree.heading("#7", text="Type")

    tree.pack()


    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from transactions where s_acc_no = '{}' and r_acc_no = '{}' order by dnt desc".format(Acc_no,rac))
    recs=cur.fetchall()         
    for q in recs:
        tree.insert("", tk.END, values=q)
    con.close()


#Search by name of sender     
def namer_tr():
    global s_nr
    s_nr = StringVar()
    global snr_screen
    global snr_notif
    #Search by name transactions screen
    snr_screen = Toplevel(master)
    snr_screen.title('TRANSACTIONS')

    #Label
    Label(snr_screen, text = "BANK OF PROSPERITY", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(snr_screen, text = "Search recent transactions", font=('Calibri',14)).grid(row=1,sticky=N)
    Label(snr_screen, text="Sender's full name", font=('Calibri',12)).grid(row=3,sticky=W,pady=10)
    snr_notif = Label(snr_screen,font=('Calibri',12))
    snr_notif.grid(row=4, sticky=N,pady=5)
    
    #Entry
    Entry(snr_screen, textvariable=s_nr).grid(row=3,column=1)

    #Button
    Button(snr_screen,text="Search",font=('Calibri',12),command=finish_namer_tr).grid(row=5,sticky=W,pady=5)
    Button(snr_screen,text="EXIT",font=('Calibri',12),command=exit_namer_tr).grid(row=6,sticky=E,pady=5)

def exit_namer_tr():
    snr_screen.destroy()

def finish_namer_tr():
    from tkinter import ttk
    import tkinter as tk
    racr="" 
    #Name acc no search
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from cinfo;")
    recs=cur.fetchall()
    for i in recs:
        if str(s_nr.get())==i[1]:
            racr += i[0]
    con.close()
    
    if racr=="":
        snr_notif.config(text='Account not found!', fg='red')
        return
    
    #Checking if any previous records exist
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from transactions where s_acc_no = '{}' and r_acc_no = '{}'".format(racr,Acc_no))
    recs=cur.fetchall()
    if recs == []:
        snr_notif.config(text='No transactions with this account!', fg='red')
        return
    con.close()
    
    #Search by name transactions screen
    sn2_screen = Toplevel(master)
    sn2_screen.title('SEARCH RESULTS')

    tree = ttk.Treeview(sn2_screen, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')

    tree.column("#1", anchor=tk.CENTER)

    tree.heading("#1", text="Transaction id")

    tree.column("#2", anchor=tk.CENTER)

    tree.heading("#2", text="Sender's account number")

    tree.column("#3", anchor=tk.CENTER)

    tree.heading("#3", text="Receiver's account number")

    tree.column("#4", anchor=tk.CENTER)

    tree.heading("#4", text="Amount")

    tree.column("#5", anchor=tk.CENTER)

    tree.heading("#5", text="Date and Time")

    tree.column("#6", anchor=tk.CENTER)

    tree.heading("#6", text="Method")

    tree.column("#7", anchor=tk.CENTER)

    tree.heading("#7", text="Type")

    tree.pack()


    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from transactions where s_acc_no = '{}' and r_acc_no = '{}' order by dnt desc".format(racr,Acc_no))
    recs=cur.fetchall()         
    for q in recs:
        tree.insert("", tk.END, values=q)
    con.close()


#Display deposits
def d_tr():
    from tkinter import ttk
    import tkinter as tk
    #Deposits transactions screen
    d_screen = Toplevel(master)
    d_screen.title('DEPOSITS')

    tree = ttk.Treeview(d_screen, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')

    tree.column("#1", anchor=tk.CENTER)

    tree.heading("#1", text="Transaction id")

    tree.column("#2", anchor=tk.CENTER)

    tree.heading("#2", text="Sender's account number")

    tree.column("#3", anchor=tk.CENTER)

    tree.heading("#3", text="Receiver's account number")

    tree.column("#4", anchor=tk.CENTER)

    tree.heading("#4", text="Amount")

    tree.column("#5", anchor=tk.CENTER)

    tree.heading("#5", text="Date and Time")

    tree.column("#6", anchor=tk.CENTER)

    tree.heading("#6", text="Method")

    tree.column("#7", anchor=tk.CENTER)

    tree.heading("#7", text="Type")

    tree.pack()
    
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from transactions where s_acc_no = '{}' and r_acc_no = '{}' and type = 'd'".format(Acc_no,Acc_no))
    recs=cur.fetchall()
    for i in recs:
        tree.insert("", tk.END, values=i)
    con.close()


#Display withdrawals  
def w_tr():
    from tkinter import ttk
    import tkinter as tk
    #Deposits transactions screen
    w_screen = Toplevel(master)
    w_screen.title('WITHDRAWALS')

    tree = ttk.Treeview(w_screen, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')

    tree.column("#1", anchor=tk.CENTER)

    tree.heading("#1", text="Transaction id")

    tree.column("#2", anchor=tk.CENTER)

    tree.heading("#2", text="Sender's account number")

    tree.column("#3", anchor=tk.CENTER)

    tree.heading("#3", text="Receiver's account number")

    tree.column("#4", anchor=tk.CENTER)

    tree.heading("#4", text="Amount")

    tree.column("#5", anchor=tk.CENTER)

    tree.heading("#5", text="Date and Time")

    tree.column("#6", anchor=tk.CENTER)

    tree.heading("#6", text="Method")

    tree.column("#7", anchor=tk.CENTER)

    tree.heading("#7", text="Type")

    tree.pack()
    
    con=sc.connect(host="localhost",user="root",passwd='7779777*',database="beast")
    cur=con.cursor()
    cur.execute("select * from transactions where s_acc_no = '{}' and r_acc_no = '{}' and type = 'w'".format(Acc_no,Acc_no))
    recs=cur.fetchall()
    for i in recs:
        tree.insert("", tk.END, values=i)
    con.close()
    
#Image import
img = Image.open('bank_logo.png')
img = img.resize((300,150))
img = ImageTk.PhotoImage(img)

#Labels
Label(master, text = "BANK OF PROSPERITY", font=('Calibri',14)).grid(row=0,sticky=N,pady=10)
Label(master, text = "Where Money and Dreams Meet", font=('Calibri',12)).grid(row=1,sticky=N)
Label(master, image=img).grid(row=2,sticky=N,pady=15)

#Buttons
Button(master, text="Register", font=('Calibri',12),width=20,command=register).grid(row=3,sticky=N)
Button(master, text="Login", font=('Calibri',12),width=20,command=login).grid(row=4,sticky=N,pady=10)

master.mainloop()