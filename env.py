import os

from dotenv import load_dotenv
from alembic import context

load_dotenv()
config = context.config
config.set_main_option("MYSQL_DATABASE_URI", os.environ["MYSQL_DATABASE_URI"])
