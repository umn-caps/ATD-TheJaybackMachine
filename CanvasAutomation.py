import signal
import os

from datetime import datetime

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from automationVariables import *
from automationGUI import AccessToken, Options, RunButtons, RequiredCourseInput
from automationLogging import *

# App Class. Lays out frames and labelframes for the GUI. 
class App:
    def __init__(self, root):
        self.root = root

        self.frame = ttk.Frame(self.root, padding=15)
        self.frame.pack(fill=BOTH, expand=YES)       

        # Create Access Token labelframe
        access_token_lf = ttk.Labelframe(self.frame, text="Access Token", padding=15)
        access_token_lf.pack(fill=X, expand=YES, anchor=N, pady=(0,10))

        # Create FROM and TO Required Course Information labelframe
        required_course_fields_lf = ttk.Labelframe(self.frame, text="Required Course Information", padding=15)
        required_course_fields_lf.pack(fill=X, expand=YES, anchor=N, pady=(0,10))

        # Create Update Options labelframe
        options_lf = ttk.Labelframe(self.frame, text="Update Options", padding=15)
        options_lf.pack(fill=X, expand=YES, anchor=N, pady=(0,15))

        # Create Run buttons frame
        run_button_row = ttk.Frame(self.frame)
        run_button_row.pack(fill=X, expand=YES, pady=(5, 10))

        # Creates logging console labelframe
        console_frame = ttk.Labelframe(self.frame, text="Console", padding=15)
        console_frame.pack(fill=BOTH, expand=YES, anchor=N)
        
        # Initialize all frames
        self.access_token = AccessToken(access_token_lf)
        self.options_input = Options(options_lf)
        self.required_course_input = RequiredCourseInput(required_course_fields_lf, self.access_token)
        self.run_buttons = RunButtons(run_button_row, self.root, self, self.access_token, self.options_input, self.required_course_input)
        self.console = ConsoleUi(console_frame)

        self.pull_access_token()
        
        # Quits program when exiting window or when clicking Ctrl+Q
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        
        # Don't know what this does. But it's important. Don't touch it unless you know better than me.
        signal.signal(signal.SIGINT, self.quit)

    # Pulls Access Token from file "access_token.txt". Access token needs to be on the firs line with no additional enters or spaces.
    def pull_access_token(self):
        access_token_file = "access_token.txt"

        try: 
            with open(access_token_file) as text:
                token = text.readlines()
            
            update_log(f"Pulled Access Token from {access_token_file}")
            self.access_token.api_token_entry.insert(0, token)
            self.access_token.check_api_token()
            
        except:
            pass

    # Saves a simple log showing only what is in the app console
    def save_simple_log(self):
        if self.console.is_empty() == False:
            log_file_name = f"{os.getcwd()}/logs/simple_log {datetime.now().strftime('%d-%m-%Y %H_%M_%S')}.log"
            os.makedirs(os.path.dirname(log_file_name), exist_ok=True)
            with open(log_file_name, 'w') as writer:
                writer.write(self.console.get_all_text())

    # Quits program when clicking on the top-right "X" button. Saves simple log on close.
    def quit(self, *args):
        self.save_simple_log()
        self.root.destroy()


# Main loop
if __name__ == '__main__':
    # Saving long log file and setting up configuration for Logging object.
    # Overwrites old long log each time app runs
    log_file_name = f"{os.getcwd()}/logs/logging.log"
    os.makedirs(os.path.dirname(log_file_name), exist_ok=True)
    logging.basicConfig(filename=log_file_name, 
                        encoding='utf-8', 
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s')
    
    # Creates the window for the application and runs it through .mainloop()
    root = ttk.Window(title=APP_TITLE,
                      themename=APP_TTK_THEME,
                      resizable=['true','true'],
                      size=APP_TTK_WINDOW_SIZE)
    root.minsize(APP_WIDTH, APP_HEIGHT)
    
    try:
        root.iconbitmap("favicon.ico")
    except:
        pass

    app = App(root)
    app.root.mainloop()
