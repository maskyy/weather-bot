import os

import dotenv

CONFIG = {
    **dotenv.dotenv_values(".env"),
    **os.environ,
}
