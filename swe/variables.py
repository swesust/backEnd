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

# storage folder locations
FOLDER_STUDENT = 'data/students'
FOLDER_TEACHER = 'data/teachers'
FOLDER_POST = 'data/posts'

DEFAULT_PROFILE_IMAGE = 'data/image.PNG'
DEFAULT_COVER_IMAGE = 'data/cover.JPEG'

FILE_CHUNK_SIZE = 2500000

# email text
EMAIL_SUBJECT_TOKEN = "SWE Society account password reset token"
EMAIL_SUBJECT_PASSWORD_CHANGE = "SWE Society account password changed"
EMAIL_TEXT_TOKEN = ""
EMAIL_TEXT_PASSWORD_RESET = ""

