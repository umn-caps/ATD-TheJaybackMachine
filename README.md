# The Jayback Machine: Canvas Migration and Update Automation Script

The Jayback Machine: Canvas Migration and Update Automation Script (or "The Jayback Machine" for short) is a script that was was developed in-house by Academic Technology and Design staff to migrate and update Canvas Learning Management System course sites for the University of Minnesota's College of Continuing and Professional Studies.

Specifically, the script opens a GUI that has fields that has the user to authenticate themselves to use the Canvas API with their access token as well as the minimum needed varibles for the migration and updates of courses. 

The first step of the with is the migration: 
* Copies group sets and groups to the new course. By copying the group sets to the new course before the Canvas migration, during the migration the assignments and discussions that are tied to group sets will keep their associations.
* Copies an old online course to a new blank online course shell shifting dates to the new semester using the Canvas migration tool.
* During the course copy, the script notifies the completion status of the migration. The migration script concludes when the script detects the course copy has reached 100% completion.

Next, the update component of the script:
* Clears extra spaces in titles for modules, pages, assignments, quizzes and discussions.
* If a course uses week-spans in the title, the modules are re-titled to contain the dates for the week-spans in the new course.
* If the course is moving to or from a Spring sememster course, the script will add/remove the Spring break module and shift the dates for pages, assignments, quizzes and dicussions 

## Parts of the Script
### CanvasAutomation.py
The main() function of the script runs out of CanvasAutomation.py. Here it creates the root for the tkinter window (more info under GUI) and also the App Class that initializes the GUI that connects to other parts of the script. 

### GUI
automationGUI.py tkinter window graphical user interface (GUI) with the buttons and input fields to make the script function. The tkinter GUI uses the tkinter theme extention ttkbootstrap (more infomation below). This script lays out the parts of the window and also triggers the work of the script that is done for the Migration (automationMigration.py) and Update (automationUpdate.py) 

### Global Variables
The Python script automationVariables.py contains a place with Global Variables that are used across the script. Here is a description of what 

## Dependancies
Below is a list of the Python dependencies and libraries that are needed to make the script run

### CanvasAPI (formerly PyCanvas)
According to [their GitHub page](https://github.com/ucfopen/canvasapi) “Python API wrapper for Instructure's Canvas LMS. Easily manage courses, users, gradebooks, and more.” Rather than making an infrastructure for REST API calls to Canvas, this library has various classes make scripts more simple

### ttkbootstrap
[ttkbootstrap](https://ttkbootstrap.readthedocs.io/en/latest/) is “A supercharged theme extension for tkinter that enables on-demand modern flat style themes inspired by Bootstrap.” This was used to make theming and coloring easier. It comes with a preset of themes which made making a good looking product easier than with tkinter alone.

### Arrow
Arrow is "a Python library that offers a sensible and human-friendly approach to creating, manipulating, formatting and converting dates, times and timestamps." Arrow is used for the Spring Break date shifting in the Update script, acting as the brains to manage daylight savings and timezones as a part of the date shifts.

### BeautifulSoup

## Credits
Avery Pierce-McGovern <mcgovera@umn.edu>, Project Lead/Project Manager
Paul McLagan <mclag011@umn.edu>, Project Lead/Lead Programmer and Designer
Annika Moe <moex0125@umn.edu>, Key Developer 
Nichole Salinas <sali0137@umn.edu>, Developer



