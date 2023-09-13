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
 
        self.api_token_ok = False
 
        # TTK Create and add API Access Token widget elements
        api_token_row = ttk.Frame(self.frame)
        api_token_row.pack(fill=X, expand=YES, pady=(0,0))
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
            current_user = canvas.get_current_user()
            
            try:
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

        self.from_start_date_label = ttk.Label(from_input_row, text="Start Date")
        self.from_start_date_label.pack(side=LEFT, padx=(10, 10))

        self.from_start_date_entry = ttk.DateEntry(from_input_row,startdate=FROM_DATEENTRY_START_DATE)
        self.from_start_date_entry.pack(side=LEFT)

        self.check_from_course_btn = ttk.Button(from_input_row,
                                              text="Check", 
                                              command=lambda: self.check_course_name(self.from_course.get(), 0))
        self.check_from_course_btn.pack(side=LEFT, padx=(15, 0))

        # TTK Create and add TO Course widget elements
        to_input_row = ttk.Frame(self.frame)
        to_input_row.pack(fill=X, pady=(0, 0))   

        self.to_course_label = ttk.Label(to_input_row, text="TO Course ID")
        self.to_course_label.pack(side=LEFT, fill=X, padx=(20, 10))

        self.to_course_entry = ttk.Entry(to_input_row, textvariable=self.to_course)
        self.to_course_entry.pack(side=LEFT, fill=X, expand=YES)    

        self.to_start_date_label = ttk.Label(to_input_row, text="Start Date")
        self.to_start_date_label.pack(side=LEFT, padx=(10, 10))
        
        self.check_api_token_btn = ttk.Button(to_input_row,
                                              text="Check", 
                                              command=self.check_api_token)
        self.check_api_token_btn.pack(side=RIGHT, padx=(15, 0))

    # Checks if the API Token is usable before running the migration or update script
    def check_api_token(self):
        if len(self.api_token_entry.get()) != 0:
            canvas = Canvas(API_URL, self.api_token.get())
            current_user = canvas.get_current_user()
            
            try:
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

        self.from_start_date_label = ttk.Label(from_input_row, text="Start Date")
        self.from_start_date_label.pack(side=LEFT, padx=(10, 10))

        self.from_start_date_entry = ttk.DateEntry(from_input_row,startdate=FROM_DATEENTRY_START_DATE)
        self.from_start_date_entry.pack(side=LEFT)

        self.check_from_course_btn = ttk.Button(from_input_row,
                                              text="Check", 
                                              command=lambda: self.check_course_name(self.from_course.get(), 0))
        self.check_from_course_btn.pack(side=LEFT, padx=(15, 0))

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
        self.to_start_date_entry = ttk.DateEntry(to_input_row,startdate=TO_DATEENTRY_START_DATE)
        self.to_start_date_entry.pack(side=LEFT)

        self.check_to_course_btn = ttk.Button(to_input_row,
                                              text="Check", 
                                              command=lambda: self.check_course_name(self.to_course.get(), 1))
        self.check_to_course_btn.pack(side=LEFT, padx=(15, 0))

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
    

        self.check_to_course_btn = ttk.Button(to_input_row,
                                              text="Check", 
                                              command=lambda: self.check_course_name(self.to_course.get(), 1))
        self.check_to_course_btn.pack(side=LEFT, padx=(15, 0))

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
    
    def check_course_name(self, course_id, course_type):
        
        if course_id != "":
            api_token = self.api_token_input.api_token.get()
            canvas = Canvas(API_URL,api_token)
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


# Initializes GUI fields for script options
    
    def check_course_name(self, course_id, course_type):
        
        if course_id != "":
            api_token = self.api_token_input.api_token.get()
            canvas = Canvas(API_URL,api_token)
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


# Initializes GUI fields for script options
class Options:
    def __init__(self, frame):
        self.frame = frame
        
        row1 = ttk.Frame(self.frame)
        row1.pack(fill=X, expand=YES, pady=(0,10))
        row1.pack(fill=X, expand=YES, pady=(0,10))

        # Sprink Break Options
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
                                                   from_=0, to=15,
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
    
    def sb_weeks_to_start_entry_state(self):
        if self.sb_weeks_to_start_checkbtn_value.get() == 1:
            self.sb_weeks_to_start_entry["state"] = "normal"
        else:
            self.sb_weeks_to_start_entry["state"] = "disabled"


# Initializes GUI buttons that will run an API Token check, the migration script and the update script
# Initializes GUI buttons that will run an API Token check, the migration script and the update script
class RunButtons:
    def __init__(self, frame, root, main_app, api_token_input, options_input, course_input):
        self.frame = frame
        self.root = root
        self.main_app = main_app
        self.api_token_input = api_token_input
        self.api_token_input = api_token_input
        self.options_input = options_input
        self.course_input = course_input
        self.course_input = course_input

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

    # Run Migration script
    def run_migration(self):    
        
        if self.check_api_token() == True and self.check_course_ids() == True:
            self.disable_run_buttons()
            
            api_token = self.api_token_input.api_token.get()
            
            from_course_id = self.course_input.from_course.get()
            from_start_date = self.course_input.get_from_start_date_str()

            to_course_id = self.course_input.to_course.get()
            to_start_date = self.course_input.get_to_start_date_str()
            
            migrate_single_course = MigrateSingleCourse(api_token, from_course_id, to_course_id, from_start_date, to_start_date, self)
        
        if self.check_api_token() == True and self.check_course_ids() == True:
            self.disable_run_buttons()
            
            api_token = self.api_token_input.api_token.get()
            
            from_course_id = self.course_input.from_course.get()
            from_start_date = self.course_input.get_from_start_date_str()

            to_course_id = self.course_input.to_course.get()
            to_start_date = self.course_input.get_to_start_date_str()
            
            migrate_single_course = MigrateSingleCourse(api_token, from_course_id, to_course_id, from_start_date, to_start_date, self)
            migrate_single_course.start()
 
 
    # Run Update script   
    def run_update(self):        

        if self.check_api_token() == True and self.check_course_ids() == True:
            self.disable_run_buttons()
            

        if self.check_api_token() == True and self.check_course_ids() == True:
            self.disable_run_buttons()
            
            update_log("Update beginning. Please wait...")
            
            api_token = self.api_token_input.api_token.get()
            sb_start_week = int(self.options_input.sb_start_week.get())
            options = [self.options_input.remove_title_spaces_checkbtn_value.get(),
                    self.options_input.library_links_checkbtn_value.get()]

            from_course_id = self.course_input.from_course.get()
            from_start_date = self.course_input.get_from_start_date_str()
            
            to_course_id = self.course_input.to_course.get()
            to_start_date = self.course_input.get_to_start_date_str()
            
            update_single_course = UpdateSingleCourse(api_token, from_course_id, to_course_id, from_start_date, to_start_date, sb_start_week, options, self)
            
            api_token = self.api_token_input.api_token.get()
            sb_start_week = int(self.options_input.sb_start_week.get())
            options = [self.options_input.remove_title_spaces_checkbtn_value.get(),
                    self.options_input.library_links_checkbtn_value.get()]

            from_course_id = self.course_input.from_course.get()
            from_start_date = self.course_input.get_from_start_date_str()
            
            to_course_id = self.course_input.to_course.get()
            to_start_date = self.course_input.get_to_start_date_str()
            
            update_single_course = UpdateSingleCourse(api_token, from_course_id, to_course_id, from_start_date, to_start_date, sb_start_week, options, self)
            update_single_course.start()
        
    def check_api_token(self):
        if self.api_token_input.api_token_ok == False:
            update_log("Script cannot start until your Access Token is filled out or correct.")
            self.danger_run_buttons()
            return False
        else:
            self.normal_run_buttons()
            return True

    def check_course_ids(self):
        if len(self.course_input.from_course.get()) < 6 or len(self.course_input.to_course.get()) < 6:
            self.danger_run_buttons()
            update_log("Script cannot begin until you check that your Access Token is correct.")
            return False
        else:
            self.normal_run_buttons()
            return True

    def check_api_token(self):
        if self.api_token_input.api_token_ok == False:
            update_log("Script cannot start until your Access Token is filled out or correct.")
            self.danger_run_buttons()
            return False
        else:
            self.normal_run_buttons()
            return True

    def check_course_ids(self):
        if len(self.course_input.from_course.get()) < 6 or len(self.course_input.to_course.get()) < 6:
            self.danger_run_buttons()
            update_log("Script cannot begin until you check that your Access Token is correct.")
            return False
        else:
            self.normal_run_buttons()
            return True


    # Disables Migration and Update run buttons
    def enable_run_buttons(self):
        self.start_migration_btn.config(state="normal")
        self.start_update_btn.config(state="normal")

    # Enables Migration and Update run buttons
    def disable_run_buttons(self):
        self.start_migration_btn.config(state="disabled")
        self.start_update_btn.config(state="disabled")

    def danger_run_buttons(self):
        self.start_migration_btn.config(bootstyle = "danger")
        self.start_update_btn.config(bootstyle = "danger")

    def normal_run_buttons(self):
        self.start_migration_btn.config(bootstyle = "normal")
        self.start_update_btn.config(bootstyle = "normal")


    def danger_run_buttons(self):
        self.start_migration_btn.config(bootstyle = "danger")
        self.start_update_btn.config(bootstyle = "danger")

    def normal_run_buttons(self):
        self.start_migration_btn.config(bootstyle = "normal")
        self.start_update_btn.config(bootstyle = "normal")

    # Closes window and program. Saves simple log on close.
    def close(self):
        self.main_app.save_simple_log()
        self.root.destroy()