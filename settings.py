import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("API_SECRET_KEY")
print(SECRET_KEY)

# TASK: INSTALL DOTEND AND READ ON THE COMOPANY FOR THE INTERVIEW