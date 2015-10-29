"""`appengine_config` gets loaded when starting a new application instance."""
import sys
import os
from google.appengine.api import app_identity
import os.path
# add `lib` subdirectory to `sys.path`, so our `main` module can load
# third-party libraries.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

SERVER_SOFTWARE = os.environ.get('SERVER_SOFTWARE')

IS_LOCAL_DEV_SERVER = True if not SERVER_SOFTWARE or SERVER_SOFTWARE.startswith('Development') else False



ENVIRONMENTS = {
    "thehillsfc":{

        "host_url": "www.thehillsfc.com"
    },
    "thehillsfc-dev":{
        "host_url": "thehillsfc-dev.appspot.com"
    },
    "dev-thehillsfc": {
        "host_url": "127.0.0.1:8090"
    }
}

import logging

logging.debug("DEV? {}".format(IS_LOCAL_DEV_SERVER))

running_app_id = app_identity.get_application_id() if not IS_LOCAL_DEV_SERVER else 'dev-thehillsfc'

host_url = ENVIRONMENTS.get(running_app_id).get('host_url')
