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
        access_token_lf.pack(fill=X, expand=YES, anchor=N)

        # Create FROM and TO Required Course Information labelframe
        required_course_fields_lf = ttk.Labelframe(self.frame, text="Required Course Information", padding=15)
        required_course_fields_lf.pack(fill=X, expand=YES, anchor=N)

        # Create Options labelframe
        options_lf = ttk.Labelframe(self.frame, text="Options", padding=15)
        options_lf.pack(fill=X, expand=YES, anchor=N, pady=(0,0))

        # Create Run buttons frame
        run_button_row = ttk.Frame(self.frame)
        run_button_row.pack(fill=X, expand=NO, pady=(0, 10))

        # Creates logging console labelframe
        console_frame = ttk.Labelframe(self.frame, text="Console", padding=15)
        console_frame.pack(fill=X, expand=YES, anchor=N)
        
        # Initialize all frames
        self.access_token = AccessToken(access_token_lf)
        self.options_input = Options(options_lf)
        self.required_course_input = RequiredCourseInput(required_course_fields_lf)
        self.run_buttons = RunButtons(run_button_row, self.root, self, self.access_token, self.options_input, self.required_course_input)
        self.console = ConsoleUi(console_frame)

        # For Testing. Populates fields with variables from automationVariables if True. Set IS_TESTING to False to stop function
        if IS_TESTING:
            self.test_entries()
        
        # Quits program when exiting window or when clicking Ctrl+Q
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        
        # Don't know what this does. But it's important. Don't touch it unless you know better than me.
        signal.signal(signal.SIGINT, self.quit)

    # Testing function. Pulls in data from automationVariables for data entry in the GUI
    def test_entries(self):
        with open('access_token.txt') as text:
            token = text.readlines()
        
        self.access_token.api_token_entry.insert(0, token)
        self.run_buttons.check_api_token()

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
                      resizable=['false','false'],
                      size=APP_TTK_WINDOW_SIZE)
    try:
        root.iconbitmap("favicon.ico")
    except:
        pass

    app = App(root)
    app.root.mainloop()
