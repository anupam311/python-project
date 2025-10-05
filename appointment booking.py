from sys import exit
import random
import mysql.connector as sql
conn=sql.connect(host='localhost',user='root',passwd='1234',database='hospital')
if conn.is_connected():
    print('successfully connected')
c1=conn.cursor()
c1.execute('show tables')
lst=c1.fetchall()
print(lst)

if ('patients',) in lst:
    None
else:
    c1.execute('create table patients(patient_id int,name varchar(50),age int,gender varchar(10),contact varchar(15),email varchar(50),password varchar(50))')

if ('appointments',) in lst:
    None
else:
    c1.execute('create table appointments(appointment_id int,patient_id int,doctor_id int,date date,time_slot varchar(10),status varchar(20))')

if ("id_list",) in lst:
    None
else:
    c1.execute('create table id_list(id int)')

#------------------------------------------------
#    patient modules
#------------------------------------------------

def register_patient():
    patient_id=id_generation()
    c1.execute("select email from patients")
    em_list=c1.fetchall()
    while True:
        email=input('Enter Email Id :')
        out='yes'
        if email in em_list:
            print("Email Id already registered.")
            ans=input("Do you wish to retry ( y/n ) :")
            if ans.lower()=='y':
                continue
            else:
                out='no'
                break
        else:
            break
    if out=='yes':
        name=input('Enter Patient name :')
        age=int(input('Enter Patient age :'))
        gender=input('Enter Patient gender :')
        contact=input('Enter Phone number :')
        password=input('Enter a strong password :')
        sql_insert="insert into patients values("""+str(patient_id)+",'"+name+"',"+str(age)+",'"+gender+"','"+contact+"','"+email+"','"+password+"')"
        c1.execute(sql_insert)
        print('SUCCESSFULLY REGISTERED')
        conn.commit()

def login_patient():
    email=input("Enter Registered Email Id :")
    password=input("Enter password :")
    sql_insert="select * from patients where email=""'"+email+"'and password='"+password+"'"
    c1.execute(sql_insert)
    data=c1.fetchall()
    if len(data)!=0:
        print("Login Successful")
        patient_id=int(input("Enter Patient_id : "))
        ask='y'
        while ask.lower()=='y':
            print(" 1. Book Appointment")
            print(" 2. View appointments")
            print(" 3. Cancel appointment")
            print(" 4. Exit")
            choice2=int(input("Enter your choice : "))
            if choice2==1:
                patient_book_appointment(patient_id)
            elif choice2==2:
                patient_view_appointments(patient_id)
            elif choice2==3:
                patient_cancel_appointments(patient_id)
            elif choice2==4:
                exit()
            else:
                print("INVALID INPUT. TRY AGAIN.")
                continue
            ask=input("Do you wish to continue editing your appointments ( y/n )? :")

    else:
        print("Invalid login")

def patient_book_appointment(patient_id):
    show_available_doctors()
    doctor_id=int(input("Enter doctor_id : "))
    date=input("Enter date ( yyyy-mm-dd ) : ")
    time_slot=input("Enter time slot ( 24-hr format )( hh:mm ) : ")
    c1.execute("select time_slot from doctors where doctor_id="""+str(doctor_id)+"")
    time=c1.fetchall()
    if time_slot in time[0]:
        c1.execute("select date,time_slot from appointments where doctor_id="""+str(doctor_id)+" and date='"+date+"' and time_slot='"+time_slot+"'")
        data=c1.fetchall()
        print(data)
        if len(data)==0:
            appointment_id=id_generation()
            status="booked"
            c1.execute("insert into appointments values("""+str(appointment_id)+","+str(patient_id)+","+str(doctor_id)+",'"+date+"','"+time_slot+"','"+status+"')")
            conn.commit()
            print("Appointment Booked")
        else:
            print("The Time slot - ",time_slot," - on the date - ",date," - is already booked. PLease try again later or book another time slot.")
    else:
        print("Unavailable Time slot.")

def patient_view_appointments(patient_id):
    c1.execute("select * from appointments where patient_id="""+str(patient_id)+"")
    data=c1.fetchall()
    if len(data)!=0:
        for a in data:
            print(a)
    else:
        print("No scheduled appointment(s).")
        return "No scheduled appointment(s)."

def patient_cancel_appointments(patient_id):
    ans=patient_view_appointments(patient_id)
    if ans=="No scheduled appointment(s).":
        exit
    else:
        appointment_id=int(input("Enter appointment id to cancel : "))
        c1.execute("update appointments set status='canceled' where appointment_id="""+str(appointment_id)+"")
        conn.commit()
        print("Appointment canceled.")
        
#------------------------------------------------
#    doctor modules
#------------------------------------------------

def login_doctor():
    doctor_id=int(input("Enter Doctor_id : "))
    c1.execute("select distinct doctor_id from doctors")
    data=c1.fetchall()
    lst=[]
    for a in data:
        lst.append(a[0])
    if doctor_id in lst:
        print("Login Successful")
        ask='y'
        while ask.lower()=='y':
            print(" 1. View appointments")
            print(" 2. Mark Attendance")
            print(" 3. Update time slots")
            print(" 4. Exit")
            choice2=int(input("Enter your choice : "))
            if choice2==1:
                doctor_view_appointments(doctor_id)
            elif choice2==2:
                mark_attendance(doctor_id)
            elif choice2==3:
                update_doctor_availability(doctor_id)
            elif choice2==4:
                exit()
            else:
                print("INVALID INPUT. TRY AGAIN.")
                continue
            ask=input("Do you wish to continue editing the records ( y/n )? :")
    else:
        print("Invalid Login")
        
def doctor_view_appointments(doctor_id):
    status="booked"
    c1.execute("select * from appointments where doctor_id=%s and status=%s",(doctor_id,status))
    data=c1.fetchall()
    c1.execute("select * from appointments order by status")
    lst=c1.fetchall()
    if len(data)==0:
        print("No Scheduled Appointments.")
        for a in lst:
            print(a)
    else:
        print("Scheduled Appointments.")
        for a in data:
            print(a)

def update_doctor_availability(doctor_id):
    c1.execute("select * from doctors where doctor_id="""+str(doctor_id)+"")
    data=c1.fetchall()
    for a in data:
        print(a)
    print('--------------------------')
    print('1. ADD TIME SLOTS')
    print('2. REMOVE TIME SLOTS')
    print('3. CHECK TIME SLOTS')
    print('4. EXIT')
    print('--------------------------')
    
    name=data[0][1]
    specialization=data[0][2]
    fee=float(data[0][3])
    
    ans='y'
    while ans.lower()=='y':
        choice=int(input('Enter the no. of your choice : '))
        if choice==1:
            ask='y'
            while ask.lower()=='y':
                time_slot=input("Enter Time Slot ( 24-hr format )( HH:MM ) :")
                sql_insert="insert into doctors values("""+str(doctor_id)+",'"+name+"','"+specialization+"',"+str(fee)+",'"+time_slot+"')"
                c1.execute(sql_insert)
                conn.commit()
                ask=input("Enter more time slots ( y/n ) :")
        elif choice==2:
            ask='y'
            while ask.lower()=='y':
                time_slot=input("Enter slot time to be removed ( 24-hr format )( HH:MM ) :")
                c1.execute("delete from doctors where time_slot=""'"+time_slot+"' and doctor_id="+str(doctor_id)+"")
                conn.commit()
                ask=input("Remove more time slots ( y/n ) :")
        elif choice==3:
            c1.execute("select * from doctors where doctor_id="""+str(doctor_id)+"")
            data=c1.fetchall()
            for a in data:
                print(a)
        elif choice==4:
            ans='n'
        else:
            print("INVALID INPUT")
            continue

def mark_attendance(doctor_id):
    c1.execute("select appointment_id,status from appointments where doctor_id=""'"+str(doctor_id)+"'")
    data=c1.fetchall()
    if len(data)==0:
        print("No Scheduled Appointments")
    else:
        l=len(data)
        for a in range(l):
            lst=['attended','no_show']
            print("Appointment_id : ",data[a][0])
            while True:
                atten=input("Attendance ( Attended/No_show) :")
                if atten.lower() in lst:
                    c1.execute("update appointments set status=""'"+atten+"' where appointment_id="+str(data[a][0])+"")
                    conn.commit()
                    print("Attendance Updated.")
                    break
                else:
                    print("INVALID INPUT. PLEASE ENTER AGAIN.")
                    continue
    


#------------------------------------------------
#    support modules
#------------------------------------------------
def id_generation():
    c1.execute('select id from id_list')
    value_list=c1.fetchall()
    while True:
        random_id=random.randint(100000000,999999999)
        if random_id not in value_list:
            c1.execute("insert into id_list(id) values("""+str(random_id)+")")
            conn.commit()
            return random_id
        else:
            continue

def show_available_doctors():
    c1.execute("select * from doctors")
    data=c1.fetchall()
    for a in data:
        print(a)

#------------------------------------------------
#    Main program
#------------------------------------------------

print("Welcome To Aarvy Hospital")
ans='y'
while ans.lower()=='y':
    print(" 1. Register Patient")
    print(" 2. Login Patient")
    print(" 3. Login Doctor")
    print(" 4. Exit")
    choice1=int(input("Enter the no. of your choice :"))

    if choice1==1:
        ans='n'
        register_patient()
        
    elif choice1==2:
        ans='n'
        login_patient()
            
    elif choice1==3:
        ans='n'
        login_doctor()

    elif choice1==4:
        exit()
    else:
        print("Invalid Input. Try Again")
        continue
