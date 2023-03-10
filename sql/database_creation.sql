-- This script creates the database and the tables necessary for the REGIE system
drop database if exists course_registration;

-- Creating Database
create database if not exists course_registration;

-- Using that database
use course_registration;

-- Creating Admin table
drop table if exists Admin;
create table Admin
(
id int primary key, 
name varchar(30), 
address varchar(100), 
mobile bigint, 
email varchar(30), 
password varchar(20)
);

-- Creating Department table
drop table if exists Department;
create table Department
(
id int primary key, 
name varchar(40),
division varchar(40), 
division_id varchar(4)
);

-- Creating Faculty table
drop table if exists Faculty; 
create table Faculty
(
id int primary key, 
name varchar(30), 
address varchar(100), 
mobile bigint, 
email varchar(30), 
password varchar(20),
position varchar(30),
dept_id int,
status varchar(30)
-- foreign key(dept_id) references Department(id) ON UPDATE CASCADE ON DELETE SET NULL
);

-- Creating Student table
drop table if exists Student; 
create table Student
(
id int primary key, 
name varchar(30), 
address varchar(100), 
mobile bigint, 
email varchar(30), 
password varchar(20),
restrictions text, 
advisor varchar(30), 
gpa float, 
status boolean, 
dept_id int default null, 
expected_graduation date default null,
concentration varchar(30) default null
-- foreign key(dept_id) references Department(id) ON UPDATE CASCADE ON DELETE SET NULL
);

-- Creating Course table
drop table if exists Course;
create table Course
(
id int primary key, 
name varchar(30), 
description varchar(50),
dept_id int, 
fee int
-- foreign key(dept_id) references Department(id) ON UPDATE CASCADE ON DELETE SET NULL
);

-- Creating Room Locations table
drop table if exists RoomLocations;
create table RoomLocations
(
id int primary key, 
name varchar(30),
capacity int not null,
building varchar(30)
);

-- Creating Course Section table
drop table if exists CourseSection;
create table CourseSection
(
course_section_id int primary key,
quarter_id varchar(20), 
course_id int,
room_id int, 
course_day varchar(20),
start_time time, 
end_time time, 
permission_required boolean
-- foreign key(course_id) references Course(id) ON UPDATE CASCADE ON DELETE CASCADE,
-- foreign key(room_id) references RoomLocations(id) ON UPDATE CASCADE ON DELETE SET NULL
);

-- Creating StudentCourseSection table
drop table if exists StudentCourseSection;
create table StudentCourseSection
(
quarter_id varchar(20),
course_section_id int,
student_id int, 
scores text,
grade varchar(2) default null,
primary key(quarter_id, course_section_id, student_id)
-- foreign key(student_id) references Student(id) ON UPDATE CASCADE ON DELETE CASCADE,
-- foreign key(course_section_id) references CourseSection(course_section_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Creating FacultyCourseSection table
drop table if exists FacultyCourseSection;
create table FacultyCourseSection
(
quarter_id varchar(20),
course_section_id int,
faculty_id int, 
primary key(quarter_id, course_section_id, faculty_id)
-- foreign key(faculty_id) references Faculty(id) ON UPDATE CASCADE ON DELETE CASCADE,
-- foreign key(course_section_id) references CourseSection(course_section_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Creating CourseFeatures table
drop table if exists CourseFeatures;
create table CourseFeatures
(
course_section_id int, 
feature varchar(30),
primary key(course_section_id, feature)
);

-- Creating Course Registration table
drop table if exists CourseRegistration;
create table CourseRegistration
(
quarter_id varchar(20) primary key,
reg_start_date date,
start_time time, 
reg_end_date date,
end_time time
);

-- Creating PendingCourseSection table
drop table if exists PendingCourseSection;
create table PendingCourseSection
(
quarter_id varchar(20),
course_section_id int,
pending_student_id int, 
primary key(quarter_id, course_section_id, pending_student_id)
);