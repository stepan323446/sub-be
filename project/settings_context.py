import os
ENVIRONMENT = os.getenv('ENVIRONMENT', 'prod')

print("ENVIRONMENT: " + os.environ["ENVIRONMENT"])

if ENVIRONMENT == 'dev':
    from project.settings.dev import *
else:
    from project.settings.prod import *
    