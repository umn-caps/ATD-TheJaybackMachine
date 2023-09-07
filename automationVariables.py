from datetime import datetime

API_URL = "https://canvas.umn.edu"
DAYS_TO_SPRING_BREAK_START = 50

# GUI Window Variables
APP_TITLE = "The Jayback Machine: Canvas Migration and Update Automation Script"
APP_TTK_THEME = "darkly"
APP_HEIGHT = 600
APP_WIDTH = 815
APP_TTK_WINDOW_SIZE = (APP_WIDTH, APP_HEIGHT)

# Regex Varibles
WEEK_SPAN_REGEX = '[A-Za-z]* (\d\d|\d)[ ]{0,}(-|–)[ ]{0,}[A-Za-z]* (\d\d|\d)'
LIBRARY_EXT_REGEX = '(?<=courses\/)\d{6,}(?=\/external_tools\/12142)'

# GUI DateEntry 
FROM_DATEENTRY_START_DATE = datetime.today()
TO_DATEENTRY_START_DATE = datetime.today()

# Test Variables
IS_TESTING = False
