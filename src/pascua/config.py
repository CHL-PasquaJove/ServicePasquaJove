import os

# Database configuration
database = os.environ['PASQUAJOVE_DATABASE_NAME']
url = os.environ['PASQUAJOVE_DATABASE_URL']

# Mail Configuration
mail_address = os.environ['PASQUAJOVE_MAIL_ADDRESS']
mail_password = os.environ['PASQUAJOVE_MAIL_PASSWORD']
mail_from = 'Responsables Pasqua Jove'


# Login configuration
jwt_secret = os.environ['PASQUAJOVE_JWT_SECRET']

# Log level
log_level = ""
if 'PASQUAJOVE_LOG_LEVEL' in os.environ:
    log_level = os.environ['PASQUAJOVE_LOG_LEVEL']
else:
    log_level = "INFO"
