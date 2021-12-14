from add_user import *
from common import *
from shutil import copyfile
import os

init()
for name in os.listdir(PATH_MODEL):
    os.remove(os.path.join(PATH_MODEL, name))
for name in os.listdir(PATH_DB):
    add_user(os.path.join(PATH_DB, name))