# <b>REGIE Course Registration System</b>
### _Thanushri Rajmohan_

## Description
This repository contains the sourse code for the REGIE Course Registration System, a mockup of an institution's course registration system.<br>
This project is a part of MPCS 51410: Object Oriented Programming. A detailed description of the project and its features can be found [here](https://www.classes.cs.uchicago.edu/archive/2022/winter/51410-1/project.description.html).

## Folder Structure
```
+--/src
|   +--/python        : Contains all the class files
|   +--/sql           : Contains all the database initialization files
|   +--/documentation : Contains all the reference materials and diagrams 
|   +--README.md      : Readme
```

## How to Run
REGIE is a console-based application written in python 3.10. To run the system, `cd` to the `/src/python` folder and run the following commands:
```Python
pip install -r requirements.txt
python main.py
```

## Databases Used
1. MySQL - For User and Course Management
2. MongoDB - For Logging

## Design Patterns Implemented
1. Abstract Factory Design Pattern
2. Template Design Pattern
3. Singleton Pattern
4. State pattern
5. Composite pattern
6. Observer pattern 

## S.O.L.I.D Principles of Object Oriented Design Incorporated
1. <b>S</b> ingle Responsibility Principle
2. <b>O</b> pen – Closed principle
3. <b>L</b> iskov Substitution Principle
4. <b>I</b> nterface Segregation Principle
5. <b>D</b> ependency Inversion Principle

## Notes
- If a student tries to register for a course section for Winter 2023, he/she will not be able to do it based on Winter 2023's course registration timings. However, adding a course sction to Spring 2023 will not give an error.<br>
You can test it by registering course section `900153272` and the student ID will be stored in the `PendingCourseSection` table.
- The course feature `Instructor Approval Required`, if added to a course section will invoke the Observer. 