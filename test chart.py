import dbTools as dbt
import musicdata_tool_inf as infdbt
import os
from dataStores import CONVERSION_DICT

# USAGE SETTINGS              CHANGE YOUR SETTINGS HERE

#version of DB being output
GAME_VERSION = 30
OUTPUT_FILENAME = "test that it works.bin"

OMNI_SONG_PATH = None
#OMNI_SONG_PATH = "just_inf"

# Choose bin filenames here (put None to skip any)

# Enter a clean .bin here from IIDX
db_path = "RESIDENT 20221031.bin"

contents_folder = "C:\\LDJ-003-2022101900\\contents"

pog_db = dbt.IIDXMusicDB(db_path, "AC")
pog_db.getSoflanCharts(contents_folder)