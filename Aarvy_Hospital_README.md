# 🏥 Aarvy Hospital Management System (CLI)

**Author:** Anupam Chaudhary  
**Department:** B.Tech. C.S.E (AI/ML) Section-A  
**Roll No:** 2501730151  

---

## 📘 Overview

The **Aarvy Hospital Management System** is a Python-based Command Line Interface (CLI) project that connects to a **MySQL database** to manage hospital operations.  
It provides a simple yet powerful interface for both **patients** and **doctors** to register, log in, book appointments, update availability, and manage attendance records.

---

## ⚙️ Features

### 👩‍⚕️ For Patients:
- Register new accounts with unique email IDs.  
- Log in securely using email and password.  
- Book appointments with available doctors.  
- View and cancel existing appointments.  

### 🧑‍⚕️ For Doctors:
- Log in using doctor ID.  
- View all scheduled appointments.  
- Mark attendance for appointments (`attended` / `no_show`).  
- Manage time slots (add/remove/view availability).  

### 🧩 System-Level Features:
- Auto-generate unique IDs for patients, doctors, and appointments.  
- Store all records persistently in a MySQL database.  
- Automatically create required tables if they do not exist.  
- Prevent duplicate patient registrations using the same email ID.  

---

## 🧱 Database Structure

The project connects to a **MySQL** database named `hospital`.  
Ensure that you have MySQL installed and create the database before running the script.

### Tables Used

| Table Name | Description |
|-------------|-------------|
| `patients` | Stores patient information such as ID, name, age, gender, contact, email, and password. |
| `appointments` | Stores all appointment details including doctor ID, patient ID, date, time slot, and status. |
| `id_list` | Maintains a list of all unique IDs to avoid duplication. |
| `doctors` | *(Expected to exist beforehand)* Stores details of all doctors and their available time slots. |

---

## 🧩 Functions Overview

### 🩺 Patient Functions
| Function | Purpose |
|-----------|----------|
| `register_patient()` | Registers a new patient and inserts their data into the database. |
| `login_patient()` | Verifies credentials and allows the patient to manage appointments. |
| `patient_book_appointment(patient_id)` | Books a new appointment with a doctor. |
| `patient_view_appointments(patient_id)` | Displays all appointments for the logged-in patient. |
| `patient_cancel_appointments(patient_id)` | Cancels a previously booked appointment. |

### 👨‍⚕️ Doctor Functions
| Function | Purpose |
|-----------|----------|
| `login_doctor()` | Allows doctors to log in using their doctor ID. |
| `doctor_view_appointments(doctor_id)` | Displays all booked appointments for the doctor. |
| `mark_attendance(doctor_id)` | Marks attendance for each appointment. |
| `update_doctor_availability(doctor_id)` | Adds, removes, or views available time slots. |

### ⚙️ Support Functions
| Function | Purpose |
|-----------|----------|
| `id_generation()` | Generates a unique random 9-digit ID and stores it in `id_list`. |
| `show_available_doctors()` | Displays all doctor entries from the `doctors` table. |

---

## 💻 How to Run the Program

### 🧰 Prerequisites
- **Python 3.x**
- **MySQL Server** installed and running  
- The following Python package:
  ```bash
  pip install mysql-connector-python
  ```

### 🪜 Steps to Run

1. Open **MySQL Workbench** or your MySQL command line and run:
   ```sql
   CREATE DATABASE hospital;
   ```

2. Save this script as `hospital_management.py`.

3. Open the terminal in the script’s directory and run:
   ```bash
   python hospital_management.py
   ```

4. When prompted, choose one of the following options:
   - `1` → Register Patient  
   - `2` → Login Patient  
   - `3` → Login Doctor  
   - `4` → Exit  

---

## 🧾 Example Console Flow

```
Welcome To Aarvy Hospital
 1. Register Patient
 2. Login Patient
 3. Login Doctor
 4. Exit
Enter the no. of your choice : 1

Enter Email Id : test@gmail.com
Enter Patient name : John Doe
Enter Patient age : 29
Enter Patient gender : Male
Enter Phone number : 9876543210
Enter a strong password : pass123
SUCCESSFULLY REGISTERED
```

---

## 🗂️ Example Database Records

### Table: `patients`
| patient_id | name | age | gender | contact | email | password |
|-------------|------|-----|--------|----------|--------|-----------|
| 100000123 | John Doe | 29 | Male | 9876543210 | test@gmail.com | pass123 |

### Table: `appointments`
| appointment_id | patient_id | doctor_id | date | time_slot | status |
|----------------|-------------|------------|------|------------|---------|
| 200000321 | 100000123 | 300000111 | 2025-11-12 | 10:30 | booked |

---

## 🚀 Future Enhancements

- Add admin module for hospital-wide management.  
- Integrate SMS/email notification for appointments.  
- Implement encrypted password storage.  
- Add billing and prescription records.  
- Create a GUI version using `tkinter` or `PyQt`.  

---

## 🧑‍💻 Author Info

**Name:** Anupam Chaudhary  
**Department:** B.Tech. C.S.E (AI/ML) Section-A  
**Roll No:** 2501730151  
