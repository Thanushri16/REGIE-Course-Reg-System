-- This script populates the database and the tables necessary for the REGIE system

use course_registration;

-- Populating Admin table
insert into Admin values(78684435,'Molly Stoner','Chicago,IL',7576347532,'mollystoner@uchicago.edu','passwordmolly');
insert into Admin values(78684436,'Karin Czaplewski','Chicago,IL',7573725615,'karin@uchicago.edu','passwordkarin');
insert into Admin values(78684439,'Borja','Chicago,IL',8604728573,'borja@uchicago.edu','passwordborja');

-- Populating Department table
insert into Department values(10053, 'Department of Computer Science', 'Physical Sciences Division','PSD');
insert into Department values(10059, 'Department of Biotechnology', 'Biological Sciences Division','BSD');

-- Populating Faculty table
insert into Faculty values(10023456, 'Alex James', 'Chicago, IL', 9144567990, 'alex@uchicago.edu', 'passwordalex', 'Professor', 10059, 'Full-Time');
insert into Faculty values(10034343, 'Mark Shacklette', 'Chicago, IL', 9144781842, 'mark@uchicago.edu', 'passwordmark', 'Adjunct Professor', 10053, 'Full-Time');
insert into Faculty values(10034567, 'Gerry Brady', 'Chicago, IL', 1489924012, 'gerrybrady@uchicago.edu', 'passwordbrady', 'Associate Professor', 10053, 'Full-Time');

-- Populating Student table
insert into Student values(11000000, 'Thanushri Rajmohan', 'Chicago, IL', 9847151245, 'thanushrir@uchicago.edu', 'passwordthanushri', '', 'Joseph Morgan', 3.9, True, 10053, date("2023-03-11"), 'Software Engineering'); 
insert into Student values(11000001, 'Zoya Freeman', 'Chicago, IL', 1234567990, 'zoya@uchicago.edu', 'passwordzoya', 'medical,course_load', 'Ramesh Kannibar', 3.7, False, null, null, null); 

-- Populating Course table
insert into Course values(90015325, 'Object Oriented Programming', 'OOD concepts, principles', 10053, 6500);
insert into Course values(90015326, 'Parallel Programming', 'Parallel Programming concepts', 10053, 6550);
insert into Course values(90015327, 'Advanced Algorithms', 'Advanced Programming concepts', 10053, 6500);

-- Populating Room Locations table
insert into RoomLocations values(205, 'JCL390', 30, 'John Crerar Library');

-- Populating Course Section table
insert into CourseSection values(900153251, 'Winter 2023', 90015325, 205, "Monday", time("17:30"), time("20:30"), True);
insert into CourseSection values(900153252, 'Winter 2023', 90015325, 205, "Tuesday", time("17:30"), time("20:30"), True);
insert into CourseSection values(900153271, 'Winter 2023', 90015327, 205, "Thursday", time("17:30"), time("20:30"), False);


-- Populating StudentCourseSection table
insert into StudentCourseSection values('Winter 2023', 900153251, 11000000, '93,95,100,96,97','A');
insert into StudentCourseSection values('Winter 2023', 900153251, 11000001, '93,92,94,93,90','B');
insert into StudentCourseSection values('Winter 2023', 900153252, 11000000, '93,92,94,93,90','B');
insert into StudentCourseSection values('Winter 2023', 900153271, 11000001, '93,92,94,93,90','A');
insert into StudentCourseSection values('Winter 2023', 900153251, 11000002, '93,92,94,93,90','C');
insert into StudentCourseSection values('Winter 2023', 900153251, 11000003, '93,92,94,93,90','A');
insert into StudentCourseSection values('Winter 2023', 900153251, 11000004, '93,92,94,93,90','B');

-- Populating FacultyCourseSection table
insert into FacultyCourseSection values('Winter 2023', 900153251, 10034343);
insert into FacultyCourseSection values('Winter 2023', 900153252, 10034567);
insert into FacultyCourseSection values('Winter 2023', 900153251, 10023456);

-- Populating CourseFeatures table
insert into CourseFeatures values(900153251,'Project-Based');
insert into CourseFeatures values(900153252,'Online Lectures');
insert into CourseFeatures values(900153251,'Online Lectures');
insert into CourseFeatures values(900153261,'Project-Based');

-- Populating CourseRegistration table
insert into CourseRegistration values('Fall 2022', '2022-09-10', '08:00', '2022-09-17', '17:00');
insert into CourseRegistration values('Winter 2023', '2022-11-28', '08:00', '2022-12-05', '17:00');