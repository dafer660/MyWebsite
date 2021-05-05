import os
import ssl

from pathlib import Path, PureWindowsPath, PurePosixPath

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # We should create an environ variable
    DEBUG = True
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
    SITE_NAME = "FerreiraTech.pt"

    # SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://mariadb:mariadb@127.0.0.1:3306/flaskapp')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Roles
    ROLES = ['admin', 'blogger', 'user']
    PERMISSIONS_ADMIN = ['admin_read', 'admin_write', 'admin_full']
    PERMISSIONS_BLOGGER = ['blogger_read', 'blogger_write', 'blogger_full']
    PERMISSIONS_USER = ['user_read', 'user_write', 'user_full']

    # Flask-Security
    SECURITY_BLUEPRINT_NAME = 'auth'
    SECURITY_URL_PREFIX = '/auth'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_FLASH_MESSAGES = True
    SECURITY_REGISTERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_UNIFIED_SIGNIN = False

    # Security API
    SECURITY_LOGIN_URL = '/login'
    SECURITY_LOGOUT_URL = '/logout'
    SECURITY_REGISTER_URL = '/register'
    SECURITY_CONFIRM_URL = '/confirm'
    SECURITY_CONFIRM_ERROR_VIEW = "/confirm-error"
    SECURITY_RESET_VIEW = "/reset"
    SECURITY_RESET_ERROR_VIEW = "/reset-password"
    SECURITY_POST_LOGIN_VIEW = '/login-success'
    SECURITY_POST_REGISTER_VIEW = '/register-success'
    SECURITY_POST_RESET_VIEW = '/reset-success'
    SECURITY_POST_CONFIRM_VIEW = "/confirmed-success"
    SECURITY_POST_CHANGE_VIEW = '/account-updated'

    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT") or '146585145368132386173505678016728509634'
    SECURITY_MSG_UNAUTHORIZED = ("Not authorized", "unauthorized")
    SECURITY_MSG_INVALID_PASSWORD = ("Bad username or password", "error")
    SECURITY_MSG_PASSWORD_NOT_PROVIDED = ("Bad username or password", "error")
    SECURITY_MSG_USER_DOES_NOT_EXIST = ("Bad username or password", "error")
    SECURITY_MSG_CONFIRM_REGISTRATION = ("Thank you. Confirmation instructions have been sent to %(email)s.", "success")
    SECURITY_MSG_LOGIN = ("Please log in to access this page.", "info")
    SECURITY_MSG_EMAIL_CONFIRMED = ("Thank you for confirming your email", "success")
    SECURITY_MSG_FORGOT_PASSWORD = ("Forgot password", "info")
    SECURITY_MSG_ALREADY_CONFIRMED = ("Email already confirmed!", "warning")
    SECURITY_MSG_API_ERROR = ("API Error", "error")
    SECURITY_MSG_ANONYMOUS_USER_REQUIRED = ("Anon Req", "error")
    SECURITY_MSG_CONFIRMATION_EXPIRED = ("Confirmation token expired", "info")
    SECURITY_MSG_CONFIRMATION_REQUEST = ("New confirmation request submitted", "info")
    SECURITY_MSG_CONFIRMATION_REQUIRED = ("New confirmation required!", "warning")
    SECURITY_MSG_DISABLED_ACCOUNT = ("Your account has been disabled!", "danger")
    SECURITY_MSG_EMAIL_ALREADY_ASSOCIATED = ("Email already taken", "info")
    SECURITY_MSG_EMAIL_NOT_PROVIDED = ("Email not provided", "info")
    # SECURITY_MSG_FAILED_TO_SEND_CODE = ()
    # SECURITY_MSG_IDENTITY_ALREADY_ASSOCIATED = ()
    # SECURITY_MSG_INVALID_CODE = ()
    # SECURITY_MSG_INVALID_CONFIRMATION_TOKEN = ()
    # SECURITY_MSG_INVALID_EMAIL_ADDRESS = ()
    # SECURITY_MSG_INVALID_LOGIN_TOKEN = ()
    # SECURITY_MSG_INVALID_PASSWORD_CODE = ()
    # SECURITY_MSG_INVALID_REDIRECT = ()
    # SECURITY_MSG_INVALID_RESET_PASSWORD_TOKEN = ()
    # SECURITY_MSG_LOGIN_EMAIL_SENT = ()
    SECURITY_MSG_LOGIN_EXPIRED = ()
    SECURITY_MSG_PASSWORDLESS_LOGIN_SUCCESSFUL = ("Welcome...", "success")
    # SECURITY_MSG_PASSWORD_BREACHED = ()
    # SECURITY_MSG_PASSWORD_BREACHED_SITE_ERROR = ()
    SECURITY_MSG_PASSWORD_CHANGE = ("Your account's password has been changed successfully...!", "success")
    # SECURITY_MSG_PASSWORD_INVALID_LENGTH = ("Password not long enough", "info")
    # SECURITY_MSG_PASSWORD_IS_THE_SAME = ()
    # SECURITY_MSG_PASSWORD_MISMATCH = ()
    # SECURITY_MSG_PASSWORD_NOT_SET = ()
    SECURITY_MSG_PASSWORD_RESET = ("Your password has been reset successfully...!", "success")
    SECURITY_MSG_PASSWORD_RESET_EXPIRED = ("Password reset token expired", "info")
    SECURITY_MSG_PASSWORD_RESET_REQUEST = ("New Password reset requested", "info")
    SECURITY_MSG_PASSWORD_TOO_SIMPLE = ("Password is too simple", "info")
    # SECURITY_MSG_PHONE_INVALID = ()
    # SECURITY_MSG_REAUTHENTICATION_REQUIRED = ()
    # SECURITY_MSG_REAUTHENTICATION_SUCCESSFUL = ()
    # SECURITY_MSG_REFRESH = ()
    # SECURITY_MSG_RETYPE_PASSWORD_MISMATCH = ()
    # SECURITY_MSG_TWO_FACTOR_INVALID_TOKEN = ()
    # SECURITY_MSG_TWO_FACTOR_LOGIN_SUCCESSFUL = ()
    # SECURITY_MSG_TWO_FACTOR_CHANGE_METHOD_SUCCESSFUL = ()
    # SECURITY_MSG_TWO_FACTOR_PERMISSION_DENIED = ()
    # SECURITY_MSG_TWO_FACTOR_METHOD_NOT_AVAILABLE = ()
    # SECURITY_MSG_TWO_FACTOR_DISABLED = ()
    SECURITY_MSG_UNAUTHENTICATED = ("Not authorized", "unauthorized")
    # SECURITY_MSG_US_METHOD_NOT_AVAILABLE = ()
    # SECURITY_MSG_US_SETUP_EXPIRED = ()
    # SECURITY_MSG_US_SETUP_SUCCESSFUL = ()
    # SECURITY_MSG_US_SPECIFY_IDENTITY = ()
    # SECURITY_MSG_USE_CODE = ()

    SECURITY_CSRF_COOKIE = {"key": "XSRF-TOKEN"}
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_TIME_LIMIT = 3600

    # CSRF protection
    SECURITY_CSRF_PROTECT_MECHANISMS = ["session", "basic"]
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True

    # SimpleMDE
    SIMPLEMDE_USE_CDN = True
    SIMPLEMDE_JS_IIFE = True

    # Dropzone <-- Not being used -->
    DROPZONE_DEFAULT_MESSAGE = "Drop files to upload"
    DROPZONE_INVALID_FILE_TYPE = "You can't upload files of this type."
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = ".png, .jpg, .jpeg, .gif"
    DROPZONE_PARALLEL_UPLOADS = 2
    DROPZONE_ENABLE_CSRF = True

    BLOGGING_ALLOW_FILEUPLOAD = True
    BLOGGING_TAGS = ["flask", "linux", "server", "python",
                     "javascript", "microsoft", "office 365",
                     "virtualization", "networking", "other"]
    BLOGGING_DEFAULT_TAG = ['other']
    BLOGGING_POSTS_PER_PAGE = 5
    BLOGGING_RENDER_TEXT = True
    BLOGGING_GOOGLE_ANALYTICS = True

    FILEUPLOAD_PATH = Path("app/static/fileuploads")
    FILEUPLOADED_PATH = Path("static/fileuploads")
    FILEUPLOAD_MAX_CONTENT_LENGTH = 4 * 1024 * 1024
    FILEUPLOAD_ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".gif"]

    INDEX_IMAGES_FULLPATH = Path("app/static/images/index")
    INDEX_IMAGES_PATH = Path("/static/images/index")
    INDEX_POST_LIMIT = 6

    # Google SMTP Config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'danielferr18@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'xykmlblpbupzisdg'
    MAIL_ADMIN = ['danielf18@hotmail.com']

    # LDAP Configuration
    HOSTNAMES = ['google.com']
    LDAP_PORT = 636
    LDAP_DOMAIN = 'INTERNATIONAL' or os.environ.get('DOMAIN')
    LDAP_BASE_DN = 'DC=int,DC=marrcorp,DC=marriott,DC=com'
    LDAP_USER_RDN_ATTR = 'cn'
    LDAP_USER_LOGIN_ATTR = 'cn'
    LDAP_BIND_USER_DN = None
    LDAP_BIND_USER_PASSWORD = None
    LDAP_USE_SSL = True
    LDAP_ADD_SERVER = False

    # Service Values and RC:
    RC_VALUES = {
        'Service Value #1': "I build strong relationships and create Ritz-Carlton guests for life.",
        'Service Value #2': "I am always responsive to the expressed and unexpressed wishes and needs of our guests.",
        'Service Value #3': "I am empowered to create unique, memorable and personal experiences for our guests.",
        'Service Value #4': "I understand my role in achieving the Key Success Factors, embracing "
                            "Community Footprints and creating The Ritz-Carlton Mystique.",
        'Service Value #5': "I continuously seek opportunities to innovate and improve The Ritz-Carlton experience.",
        'Service Value #6': "I own and immediately resolve guest problems.",
        'Service Value #7': "I create a work environment of teamwork and lateral service so that the needs "
                            "of our guests and each other are met.",
        'Service Value #8': "I have the opportunity to continuously learn and grow.",
        'Service Value #9': "I am involved in the planning of the work that affects me.",
        'Service Value #10': "I am proud of my professional appearance, language and behavior.",
        'Service Value #11': "I protect the privacy and security of our guests, my fellow employees and "
                             "the company's confidential information and assets.",
        'Service Value #12': "I am responsible for uncompromising levels of cleanliness and creating a safe "
                             "and accident-free environment.",
        'Employee Promise': "At The Ritz-Carlton, our Ladies and Gentlemen are the most important resource in our "
                            "service commitment to our guests.\n"
                            "By applying the principles of trust, honesty, respect, integrity and commitment, "
                            "we nurture and maximize talent to the benefit of each individual and the company.\n"
                            "The Ritz-Carlton fosters a work environment where diversity is valued, quality "
                            "of life is enhanced, individual aspirations are fulfilled, and "
                            "The Ritz-Carlton Mystique is strengthened.",
        'The Motto': "We are Ladies and Gentlemen serving Ladies and Gentlemen.",
        "The Credo": "The Ritz-Carlton is a place where the genuine care and comfort of our guests "
                     "is our highest mission.\n"
                     "We pledge to provide the finest personal service and facilities for our "
                     "guests who will always enjoy a warm, relaxed, yet refined ambience.\n"
                     "The Ritz-Carlton experience enlivens the senses, instills well-being, and "
                     "fulfills even the unexpressed wishes and needs of our guests."
    }

