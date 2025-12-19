CREATE DATABASE attendance_system;

USE attendance_system;

CREATE TABLE employee (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100) NOT NULL,
    department VARCHAR(50)
);


CREATE TABLE attendance (
    att_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_id INT,
    login_time DATETIME,
    logout_time DATETIME,
    work_hours FLOAT,
    date DATE,
    status VARCHAR(20),
    FOREIGN KEY (emp_id)
        REFERENCES employee (emp_id)
);
INSERT INTO employee (emp_id, emp_name, department) VALUES
(101, 'Tanisha', 'IT'),
(102, 'Ujjwal', 'HR'),
(103, 'Manasi', 'Finance');


SELECT * FROM employee;
SELECT * FROM attendance;


