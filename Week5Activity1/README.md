# University Management System --- UML Diagrams

## Overview

This project contains several UML and database-modeling diagrams for a
**University Management System**.\
The diagrams describe the main entities, system activities, user
interactions, and object-oriented class structure.

The diagrams are based on the following main concepts:

-   Students
-   Enrollments
-   Lectures
-   Lecturers
-   Subjects

The goal is to provide a simple visual representation of how these
elements are organized and how they interact with each other.

------------------------------------------------------------------------

## 1. ER Diagram

The **Entity-Relationship (ER) Diagram** describes the database
structure of the system.

### Main entities

-   **Student** --- stores student information such as first name, last
    name, national ID, and birth date.
-   **Enrollment** --- represents a student's enrollment in a course.
-   **Lecture** --- contains information about a lecture, including its
    subject, date, time, and name.
-   **Lecturer** --- stores lecturer information such as name, email,
    and address.
-   **Subjects** --- contains information about academic subjects.

### Main relationships

-   **Student --- Enrolls --- Enrollment**\
    A student can have multiple enrollments, while each enrollment
    belongs to a student.

-   **Enrollment --- Enrolls --- Lecture**\
    An enrollment can be associated with lectures.

-   **Lecturer --- Lectures --- Subjects**\
    Lecturers and subjects are connected through the lecture
    relationship.

The ER diagram focuses mainly on the data and relationships rather than
system behavior.

------------------------------------------------------------------------

## 2. Activity Diagram

The **Activity Diagram** shows the main operations that can be performed
in the system.

The process starts with **Start** and **Choose action**. The user can
then work with different parts of the system:

### Student management

The user can:

-   Create a student
-   Enter student information
-   Save the student
-   Modify an existing student
-   Delete a student

### Enrollment management

The user can:

-   Create an enrollment
-   Enter enrollment information
-   Save the enrollment
-   Modify an enrollment
-   Delete an enrollment

### Lecture management

The user can:

-   Create a lecture
-   Enter lecture information
-   Save the lecture
-   Modify a lecture
-   Delete a lecture

### Relationship management

The system also supports creating and deleting relationships:

-   Link an enrollment with a lecture
-   Link a lecture with a subject
-   Select the required records
-   Create or delete the relationship

After the selected operation is completed, the flow reaches **Action
completed** and then ends.

The Activity Diagram therefore focuses on **system behavior and
workflow**.

------------------------------------------------------------------------

## 3. Use Case Diagram

The **Use Case Diagram** gives a high-level view of how different users
interact with the University Management System.

### Actors

The diagram contains three main actors:

-   **Administrator**
-   **Lecturer**
-   **Student**

### Administrator

The Administrator is responsible for managing the main system data,
including:

-   Manage Students
-   Manage Enrollments
-   Manage Lectures
-   Manage Enrolls
-   Manage Subjects

The Administrator can also perform operations related to creating and
linking system records.

### Lecturer

The Lecturer interacts mainly with lecture-related information. The
diagram includes actions such as:

-   Select Lecture
-   Select Subject
-   Create Lecture

### Student

The Student has a more limited role and can view information such as:

-   View Lectures
-   View Enrollments

The Use Case Diagram intentionally provides a **high-level overview**
rather than describing every individual operation.

------------------------------------------------------------------------

## 4. UML Class Diagram

The **Class Diagram** represents the main classes of the system and
their relationships.

### Student

Main attributes include:

-   `student_code`
-   `F_name`
-   `L_name`
-   `NID`
-   `B_date`

Main operations:

-   `create()`
-   `update()`
-   `delete()`

### Enrollment

Main attributes include:

-   `student_code`
-   `course_name`
-   `CC#`
-   `date_of_enrollment`

Main operations:

-   `create()`
-   `update()`
-   `delete()`

### Lecture

Main attributes include:

-   `CC#`
-   `subject`
-   `time`
-   `date`
-   `lecture_name`

Main operations:

-   `create()`
-   `update()`
-   `delete()`

### Lecturer

Main attributes include:

-   `subject_code`
-   `L_firstname`
-   `L_lastname`
-   `L_email`
-   `L_address`

Main operations:

-   `create()`
-   `update()`
-   `delete()`

### Subject

Main attributes include:

-   `subject_code`
-   `subject_unit`
-   `subject_udsc`

Main operations:

-   `create()`
-   `update()`
-   `delete()`

The Class Diagram is intentionally kept at a **moderate level of
detail**. It shows the most important attributes, operations, and
relationships without describing implementation-specific details.

------------------------------------------------------------------------

## 5. How the Diagrams Relate to Each Other

The diagrams describe the same system from different perspectives:

  -----------------------------------------------------------------------
  Diagram                             Main purpose
  ----------------------------------- -----------------------------------
  **ER Diagram**                      Describes data entities and their
                                      relationships

  **Activity Diagram**                Describes system workflows and
                                      operations

  **Use Case Diagram**                Describes users and their
                                      interactions with the system

  **Class Diagram**                   Describes system classes,
                                      attributes, methods, and
                                      relationships
  -----------------------------------------------------------------------

Together, they provide a general model of the University Management
System:

**ER Diagram → Data structure**\
**Activity Diagram → System behavior**\
**Use Case Diagram → User interaction**\
**Class Diagram → Object-oriented structure**

------------------------------------------------------------------------

## 6. Project Scope

The diagrams are designed as a simplified academic model of a university
management system. They focus on the core functionality required to
manage students, enrollments, lectures, lecturers, subjects, and their
relationships.

The diagrams are not intended to represent a complete production system.
Authentication, permissions, payment processing, notifications,
scheduling conflicts, and other advanced functionality are outside the
current scope.
