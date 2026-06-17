import re
import arrow

from dateutil import parser
from pprint import pprint

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename

from canvasapi import Canvas

from automationVariables import *
from automationLogging import *
from automationMigration import MigrateSingleCourse
from automationUpdate import UpdateSingleCourse
from automationMigration import MigrateSingleCourse
from automationUpdate import UpdateSingleCourse

# Initializes GUI fields for required variables to run script
class AccessToken:
    def __init__(self, frame):
        self.frame = frame
        self.api_token_ok = False
 
        # TTK Create and add API Access Token widget elements
        api_token_row = ttk.Frame(self.frame)
        api_token_row.pack(fill=X, expand=YES, pady=(0,0))

        self.api_token = ttk.StringVar(frame)

        self.api_token_entry = ttk.Entry(api_token_row, width=70, textvariable=self.api_token)
        self.api_token_entry.pack(side=LEFT, fill=X, expand=YES)
        
        self.check_api_token_btn = ttk.Button(api_token_row,
                                              text="Check", 
                                              command=self.check_api_token)
        self.check_api_token_btn.pack(side=RIGHT, padx=(15, 0))

    # Checks if the API Token is usable before running the migration or update script
    def check_api_token(self):
        if len(self.api_token_entry.get()) != 0:
            canvas = Canvas(API_URL, self.api_token.get())
            
            try:
                current_user = canvas.get_current_user()
                update_log(f"Hello {current_user.name}! You are ready to use the scripts.")
                self.api_token_entry.config(bootstyle = "success")
                self.api_token_ok = True
            except:
                update_log("Access Token is not correct for Canvas access to use the scripts.")
                self.api_token_entry.config(bootstyle = "danger")
                self.api_token_ok = False
        else:
            update_log("Access Token field is empty. Please enter Access Token.")
            self.api_token_entry.config(bootstyle = "danger")
            self.api_token_ok = False
        

# Initializes GUI fields for single course migration/update input fields
class RequiredCourseInput:
    def __init__(self, frame, api_token_input):
        self.frame = frame
        self.api_token_input = api_token_input
        self.from_course = ttk.StringVar(frame)
        self.to_course = ttk.StringVar(frame)

        # TTK Create and add FROM Course widget elements
        from_input_row = ttk.Frame(self.frame)
        from_input_row.pack(fill=X, expand=YES, pady=(0,20))
    
        self.from_course_label = ttk.Label(from_input_row, text="FROM Course ID")
        self.from_course_label.pack(side=LEFT, fill=X, padx=(0, 10))

        self.from_course_entry = ttk.Entry(from_input_row, textvariable=self.from_course)
        self.from_course_entry.pack(side=LEFT, fill=X, expand=YES)

        self.check_from_course_btn = ttk.Button(from_input_row,
                                              text="Check", 
                                              command=lambda: self.check_course_name(self.from_course.get(), 0))
        self.check_from_course_btn.pack(side=LEFT, padx=(15, 0))

        self.from_start_date_label = ttk.Label(from_input_row, text="Start Date")
        self.from_start_date_label.pack(side=LEFT, padx=(10, 10))

        self.from_start_date_entry = ttk.DateEntry(from_input_row,startdate=datetime.today(), width=10)
        self.from_start_date_entry.pack(side=LEFT, fill=X, expand=YES, anchor=N)

        #self.from_auto_date_btn = ttk.Button(from_input_row,
                                              #text="Auto Date", 
                                              #command=lambda: self.from_auto_date(self.from_course.get()))
        #self.from_auto_date_btn.pack(side=LEFT, padx=(15, 0))

        # TTK Create and add TO Course widget elements
        to_input_row = ttk.Frame(self.frame)
        to_input_row.pack(fill=X, pady=(0, 0))   

        self.to_course_label = ttk.Label(to_input_row, text="TO Course ID")
        self.to_course_label.pack(side=LEFT, fill=X, padx=(20, 10))

        self.to_course_entry = ttk.Entry(to_input_row, textvariable=self.to_course)
        self.to_course_entry.pack(side=LEFT, fill=X, expand=YES)
        
        self.check_api_token_btn = ttk.Button(to_input_row,
                                              text="Check", 
                                              command=lambda: self.check_course_name(self.to_course.get(), 1))
        self.check_api_token_btn.pack(side=LEFT, padx=(15, 0))    

        self.to_start_date_label = ttk.Label(to_input_row, text="Start Date")
        self.to_start_date_label.pack(side=LEFT, padx=(10, 10))
        
        self.to_start_date_entry = ttk.DateEntry(to_input_row,startdate=datetime.today(), width=10)
        self.to_start_date_entry.pack(side=LEFT, fill=X, expand=YES, anchor=N)

        #self.to_auto_date_btn = ttk.Button(to_input_row,
                                           #text="Auto Date", 
                                           #command=lambda: self.to_auto_date())
        #self.to_auto_date_btn.pack(side=LEFT, padx=(15, 0))
     
    # Get FROM Course Start Date from Field formatted to datetime in US/Central Time
    def get_from_start_date(self):
        start_date = self.from_start_date_entry.entry.get()
        update_log("DateEntry FROM Date string: " + str(start_date))
        start_date = datetime.strptime(start_date, '%m/%d/%y')
        start_date = start_date.replace(hour=0, minute=0, second=0, tzinfo='US/Central')
        update_log("Datetime: " + str(start_date) + " " + str(start_date.tzname))
        return start_date

    # Get TO Course Start Date from Field formatted to datetime in US/Central Time
    def get_to_start_date(self):
        start_date = self.to_start_date_entry.entry.get()
        update_log("DateEntry TO Date string: " + str(start_date))
        start_date = datetime.strptime(start_date, '%m/%d/%y')
        start_date = start_date.replace(hour=0, minute=0, second=0, tzinfo='US/Central')
        update_log("Datetime: " + str(start_date) + " " + str(start_date.tzname))
        return start_date

    # Get FROM Course Start Date from Field formatted to ISO String format
    def get_from_start_date_str(self):
        start_date = self.from_start_date_entry.entry.get()
        start_date = str(parser.parse(start_date))
        return start_date

    # Get TO Course Start Date from Field formatted to ISO String format
    def get_to_start_date_str(self):
        start_date = self.to_start_date_entry.entry.get()
        start_date = str(parser.parse(start_date))
        return start_date
    
    # Checks the course name and prints it in console
    def check_course_name(self, course_id, course_type):
        if course_id != "":
            canvas = Canvas(API_URL,
                            self.api_token_input.api_token.get())
            
            course = Canvas.get_course(self=canvas, course=course_id, use_sis_id=False)

            if course_type == 0:
                update_log(f"FROM course {course_id} is {course.name}")
            else:
                update_log(f"TO course {course_id} is {course.name}")
        else:
            if course_type == 0:
                update_log("There is no course id entered for FROM Course ID")
            else:
                update_log("There is no course id entered for TO Course ID")

    # Sets the date for FROM course according to the date listed in page "Course Start Date"
    def from_auto_date(self,course_id):
        if course_id != "":
            regex_name = re.compile(r'Start Date', re.IGNORECASE) 
            
            canvas = Canvas(API_URL,
                            self.api_token_input.api_token.get())
            
            course = Canvas.get_course(self=canvas, 
                                       course=course_id, 
                                       use_sis_id=False)
        
            to_pages = course.get_pages(per_page=200)
            
            for page in to_pages:
                str(page.title)
                if bool(regex_name.search(str(page.title))):
                    todo_date = arrow.get(page.todo_date_date).to("US/Central")
                    self.from_start_date_entry.configure(startdate=todo_date)
                    update_log(f"Set FROM due date to {todo_date} based on date from {str(page.title)}")
                    return
            
            update_log("Could not find \"Course Start Date\" page in course.")
        else:
            update_log("There is no course id entered for FROM Course ID")

    # Sets the date for TO course
    def to_auto_date():
        pass

# Initializes GUI fields for script options
class Options:
    def __init__(self, frame):
        self.frame = frame
        
        row1 = ttk.Frame(self.frame)
        row1.pack(fill=X, expand=YES, pady=(0,10))
        row1.pack(fill=X, expand=YES, pady=(0,10))

        # Sprink Break Options
        self.sb_weeks_to_start_checkbtn_value = ttk.IntVar()

        self.sb_weeks_to_start_checkbtn = ttk.Checkbutton(row1, text="Spring Break is on week:", 
                                                          onvalue=1, offvalue=0,
                                                          variable=self.sb_weeks_to_start_checkbtn_value,
                                                          command=self.sb_weeks_to_start_entry_state)
        self.sb_weeks_to_start_checkbtn.pack(side=LEFT, fill=X, padx=(0, 10))
        self.sb_weeks_to_start_checkbtn.state(['!alternate'])

        self.sb_start_week = ttk.StringVar(frame, value=8)

        self.sb_weeks_to_start_entry = ttk.Spinbox(row1, textvariable=self.sb_start_week,
                                                   width=10,
                                                   from_=4, to=12,
                                                   wrap=True)
        self.sb_weeks_to_start_entry.pack(side=LEFT, fill=X)
        self.sb_weeks_to_start_entry["state"] = "disabled"

        # Remove Title Spaces Options
        self.remove_title_spaces_checkbtn_value = ttk.IntVar(value=1)

        self.remove_title_spaces_checkbtn = ttk.Checkbutton(row1, text="Remove Title Spaces",
                                                            onvalue=1, offvalue=0,
                                                            variable=self.remove_title_spaces_checkbtn_value)
        self.remove_title_spaces_checkbtn.pack(side=LEFT, fill=X, padx=(15, 0))
        self.remove_title_spaces_checkbtn.state(['!alternate'])

        # Change Library Course Page Links Option
        self.library_links_checkbtn_value = ttk.IntVar(value=1)

        self.library_links_checkbtn = ttk.Checkbutton(row1, text="Change Library Course Page Links",
                                                      onvalue=1, offvalue=0,
                                                      variable=self.library_links_checkbtn_value)
        self.library_links_checkbtn.pack(side=LEFT, fill=X, padx=(15, 0))
        self.library_links_checkbtn.state(['!alternate'])
    
    # Sets Spring Break Entry State
    def sb_weeks_to_start_entry_state(self):
        if self.sb_weeks_to_start_checkbtn_value.get() == 1:
            self.sb_weeks_to_start_entry["state"] = "normal"
        else:
            self.sb_weeks_to_start_entry["state"] = "disabled"
            self.sb_start_week.set("8")


# Initializes GUI buttons that will run an API Token check, the migration script and the update script
class RunButtons:
    def __init__(self, frame, root, main_app, api_token_input, options_input, course_input):
        self.frame = frame
        self.root = root
        self.main_app = main_app
        self.api_token_input = api_token_input
        self.options_input = options_input
        self.course_input = course_input

        self.close_btn = ttk.Button(self.frame, 
                                    text="Close", 
                                    command=self.close)
        self.close_btn.pack(side=RIGHT, padx=(10, 0))

        self.clear_id_btn = ttk.Button(self.frame, 
                                           text="Clear Course IDs", 
                                           command=self.clear_ids)
        self.clear_id_btn.pack(side=RIGHT, padx=(10, 0))

        self.start_update_btn = ttk.Button(self.frame, 
                                           text="Run Update", 
                                           command=self.run_update)
        self.start_update_btn.pack(side=RIGHT, padx=(10, 0))

        self.start_migration_btn = ttk.Button(self.frame,
                                              text="Run Migration", 
                                              command=self.run_migration)
        self.start_migration_btn.pack(side=RIGHT, padx=(10, 0))

    # Run Migration script
    def run_migration(self):   
        if self.check_api_token() == True and self.check_course_ids() == True:
            self.disable_run_buttons()
            
            migrate_single_course = MigrateSingleCourse(self.api_token_input.api_token.get(), 
                                                        self.course_input.from_course.get(), 
                                                        self.course_input.to_course.get(), 
                                                        self.course_input.get_from_start_date_str(), 
                                                        self.course_input.get_to_start_date_str(), 
                                                        self)
            migrate_single_course.start()
 
    # Run Update script   
    def run_update(self):        
        if self.check_api_token() == True and self.check_course_ids() == True:
            self.disable_run_buttons()
            
            update_log("Update beginning. Please wait...")
            
            sb_start_week = int(self.options_input.sb_start_week.get())
            options = [self.options_input.remove_title_spaces_checkbtn_value.get(), self.options_input.library_links_checkbtn_value.get()]

            update_single_course = UpdateSingleCourse(self.api_token_input.api_token.get(), 
                                                      self.course_input.from_course.get(), 
                                                      self.course_input.to_course.get(), 
                                                      self.course_input.get_from_start_date_str(), 
                                                      self.course_input.get_to_start_date_str(), 
                                                      sb_start_week, options, self)
            update_single_course.start()

    def clear_ids(self):
        self.course_input.from_course_entry.delete(0, END)
        self.course_input.to_course_entry.delete(0, END)
    
    # Checks API token before running migration or update     
    def check_api_token(self):
        if self.api_token_input.api_token_ok == False:
            update_log("Script cannot start until your Access Token is entered or correct.")
            self.danger_run_buttons()
            return False
        else:
            self.normal_run_buttons()
            return True

    # Checks to see if course ids have been filled out in Required Entry fields
    def check_course_ids(self):
        if len(self.course_input.from_course.get()) < 6 or len(self.course_input.to_course.get()) < 6:
            self.danger_run_buttons()
            update_log("Script cannot begin until you check that your Access Token is entered or correct.")
            return False
        else:
            self.normal_run_buttons()
            return True

    # Disables Migration and Update run buttons
    def enable_run_buttons(self):
        self.clear_id_btn.config(state="normal")
        self.start_migration_btn.config(state="normal")
        self.start_update_btn.config(state="normal")

    # Enables Migration and Update run buttons
    def disable_run_buttons(self):
        self.clear_id_btn.config(state="disabled")
        self.start_migration_btn.config(state="disabled")
        self.start_update_btn.config(state="disabled")

    # Sets run buttons to display red in "danger" mode. No other functionality.
    def danger_run_buttons(self):
        self.start_migration_btn.config(bootstyle = "danger")
        self.start_update_btn.config(bootstyle = "danger")

    # Sets run buttons to display normally. No other functionality.
    def normal_run_buttons(self):
        self.start_migration_btn.config(bootstyle = "normal")
        self.start_update_btn.config(bootstyle = "normal")

    # Closes window and program. Saves simple log on close.
    def close(self):
        self.main_app.save_simple_log()
        self.root.destroy()
