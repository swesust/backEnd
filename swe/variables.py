"""
Variables

"""

# email configuration variables
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'info.swesociety@gmail.com'
EMAIL_HOST_PASSWORD = 'pass#1234'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

LOGIN_URL = '/login/'
LOGIN_TEMPLATE = 'auth/login.html'
LOGOUT_TEMPLATE = 'auth/logout.html'
INDEX_TEMPLATE = 'index.html'

FOLDER_STUDENT = 'data/student'
FOLDER_TEACHER = 'data/teacher'
FOLDER_POST = 'data/post'
