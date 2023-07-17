from dateutil import parser
from pprint import pprint

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename

from canvasapi import Canvas

from automationVariables import *
from automationLogging import *
from automationMigration import MigrateSingleCourse, MigrateMultiCourses
from automationUpdate import UpdateSingleCourse, UpdateMultiCourses

# Initializes GUI fields for required variables to run script
class AccessToken:
    def __init__(self, frame):
        self.frame = frame

        # TTK Create and add API Access Token widget elements
        api_token_row = ttk.Frame(self.frame)
        api_token_row.pack(fill=X, expand=YES, pady=(0,0))

        self.api_token = ttk.StringVar(frame)

        self.api_token_entry = ttk.Entry(api_token_row, width=70, textvariable=self.api_token)
        self.api_token_entry.pack(side=LEFT, fill=X, expand=YES)


# Initializes GUI fields for script options
class Options:
    def __init__(self, frame):
        self.frame = frame
        
        row1 = ttk.Frame(self.frame)
        row1.pack(fill=X, expand=YES, pady=(0,20))

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
                                                   from_=0, to=15,
                                                   wrap=True)
        self.sb_weeks_to_start_entry.pack(side=LEFT, fill=X)
        self.sb_weeks_to_start_entry["state"] = "disabled"
    
    def sb_weeks_to_start_entry_state(self):
        if self.sb_weeks_to_start_checkbtn_value.get() == 1:
            self.sb_weeks_to_start_entry["state"] = "normal"
        else:
            self.sb_weeks_to_start_entry["state"] = "disabled"

# Initializes GUI buttons that will run an API Token check, the migration script and the update script
class RunButtons:
    def __init__(self, frame, root, main_app, api_token_input, options_input, course_input):
        self.frame = frame
        self.root = root
        self.main_app = main_app
        self.api_token_input = api_token_input
        self.options_input = options_input
        self.course_input = course_input

        self.api_token_input.api_token.trace("w", self.api_token_entry_change)

        self.close_btn = ttk.Button(self.frame, 
                                    text="Close", 
                                    command=self.close)
        self.close_btn.pack(side=RIGHT, padx=(10, 0))

        self.start_update_btn = ttk.Button(self.frame, 
                                           text="Start Updates", 
                                           command=self.run_update)
        self.start_update_btn.pack(side=RIGHT, padx=(10, 0))

        self.start_migration_btn = ttk.Button(self.frame,
                                              text="Start Migration", 
                                              command=self.run_migration)
        self.start_migration_btn.pack(side=RIGHT, padx=(10, 0))

        self.check_api_token_btn = ttk.Button(self.frame,
                                              text="Check Access Token", 
                                              command=self.check_api_token)
        self.check_api_token_btn.pack(side=RIGHT, padx=(0, 0))

    # Checks if the API Token is usable before running the migration or update script
    def check_api_token(self):
        try:
            canvas = Canvas(API_URL, self.api_token_input.api_token.get())
            current_user = canvas.get_current_user()
            update_log(f"Hello {current_user.name}! You are ready to use the scripts.")
            self.enable_run_buttons()
            self.check_api_token_btn.config(bootstyle = "primary")
            self.api_token_input.api_token_entry.config(bootstyle = "success")
            # self.api_token_input.api_token_label.config(bootstyle = "success")
        except:
            update_log("Access Token is not correct for Canvas access to use the scripts.")
            self.api_token_entry_change()

    # Run Migration script
    def run_migration(self):    
        self.disable_run_buttons()
        
        api_token = self.api_token_input.api_token.get()
        
        
        from_course_id = self.course_input.from_course.get()
        from_start_date = self.course_input.get_from_start_date_str()

        to_course_id = self.course_input.to_course.get()
        to_start_date = self.course_input.get_to_start_date_str()
        
        migrate_single_course = MigrateSingleCourse(api_token, from_course_id, to_course_id, from_start_date, to_start_date)
        migrate_single_course.start()
        
        self.enable_run_buttons()
        
    # Run Update script   
    def run_update(self):        
        self.disable_run_buttons()
        
        update_log("Update beginning. Please wait...")
        
        api_token = self.api_token_input.api_token.get()
        sb_start_week = int(self.options_input.sb_start_week.get())

        from_course_id = self.course_input.from_course.get()
        from_start_date = self.course_input.get_from_start_date_str()
        
        to_course_id = self.course_input.to_course.get()
        to_start_date = self.course_input.get_to_start_date_str()
        
        update_single_course = UpdateSingleCourse(api_token, from_course_id, to_course_id, from_start_date, to_start_date, sb_start_week)
        update_single_course.start()
        
        self.enable_run_buttons()
        
    def api_token_entry_change(self, *args):
        self.check_api_token_btn.config(bootstyle = "success")
        self.api_token_input.api_token_entry.config(bootstyle = "danger")
        # self.api_token_input.api_token_label.config(bootstyle = "danger")
        self.disable_run_buttons()

    # Disables Migration and Update run buttons
    def enable_run_buttons(self):
        self.start_migration_btn.config(state="normal")
        self.start_update_btn.config(state="normal")

    # Enables Migration and Update run buttons
    def disable_run_buttons(self):
        self.start_migration_btn.config(state="disabled")
        self.start_update_btn.config(state="disabled")
        
    # Closes window and program. Saves simple log on close.
    def close(self):
        self.main_app.save_simple_log()
        self.root.destroy()

# Initializes GUI fields for single course migration/update input fields
class RequiredCourseInput:
    def __init__(self, frame):
        self.frame = frame
        self.from_course = ttk.StringVar(frame)
        self.to_course = ttk.StringVar(frame)

        # TTK Create and add FROM Course widget elements
        from_input_row = ttk.Frame(self.frame)
        from_input_row.pack(fill=X, expand=YES, pady=(0,20))
    
        self.from_course_label = ttk.Label(from_input_row, text="FROM Course ID")
        self.from_course_label.pack(side=LEFT, fill=X, padx=(0, 10))

        self.from_course_entry = ttk.Entry(from_input_row, textvariable=self.from_course)
        self.from_course_entry.pack(side=LEFT, fill=X, expand=YES)

        self.from_start_date_label = ttk.Label(from_input_row, text="Start Date")
        self.from_start_date_label.pack(side=LEFT, padx=(10, 10))

        self.from_start_date_entry = ttk.DateEntry(from_input_row,startdate=FROM_DATEENTRY_START_DATE)
        self.from_start_date_entry.pack(side=LEFT)

        # TTK Create and add TO Course widget elements
        to_input_row = ttk.Frame(self.frame)
        to_input_row.pack(fill=X, pady=(0, 0))   

        self.to_course_label = ttk.Label(to_input_row, text="TO Course ID")
        self.to_course_label.pack(side=LEFT, fill=X, padx=(20, 10))

        self.to_course_entry = ttk.Entry(to_input_row, textvariable=self.to_course)
        self.to_course_entry.pack(side=LEFT, fill=X, expand=YES)    

        self.to_start_date_label = ttk.Label(to_input_row, text="Start Date")
        self.to_start_date_label.pack(side=LEFT, padx=(10, 10))

        self.to_start_date_entry = ttk.DateEntry(to_input_row,startdate=TO_DATEENTRY_START_DATE)
        self.to_start_date_entry.pack(side=LEFT)



    # Get FROM Course Start Date from Field formatted to datetime in US/Central Time
    def get_from_start_date(self):
        start_date = self.from_start_date_entry.entry.get()
        update_log("DateEntry FROM Date string: " + str(start_date))
        start_date = datetime.strptime(start_date, '%m/%d/%y')
        start_date = start_date.replace(hour=0, minute=0, second=0, tzinfo='US/Central')
        update_log("Datetime: " + str(start_date) + " " + str(start_date.tzname))
        return start_date

    # Get FROM Course Start Date from Field formatted in ISO String format
    def get_from_start_date_str(self):
        start_date = self.from_start_date_entry.entry.get()
        start_date = str(parser.parse(start_date))
        return start_date
    
    # Get TO Course Start Date from Field formatted to datetime in US/Central Time
    def get_to_start_date(self):
        start_date = self.to_start_date_entry.entry.get()
        update_log("DateEntry TO Date string: " + str(start_date))
        start_date = datetime.strptime(start_date, '%m/%d/%y')
        start_date = start_date.replace(hour=0, minute=0, second=0, tzinfo='US/Central')
        update_log("Datetime: " + str(start_date) + " " + str(start_date.tzname))
        return start_date

    # Get TO Course Start Date from Field formatted to ISO String format
    def get_to_start_date_str(self):
        start_date = self.to_start_date_entry.entry.get()
        start_date = str(parser.parse(start_date))
        return start_date