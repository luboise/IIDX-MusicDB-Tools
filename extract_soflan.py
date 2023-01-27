import dbTools as dbt
import musicdata_tool_inf as infdbt
import os
from dataStores import CONVERSION_DICT
import json

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


if __name__ == "__main__":
	pog_db = dbt.IIDXMusicDB(db_path, "AC")
	song_objects, chart_objects = pog_db.getSoflanCharts(contents_folder)

	with open("song_objects.json", "w", encoding = "cp932") as f:
		f.write(json.dumps(song_objects, indent=4, ensure_ascii=False))
	with open("chart_objects.json", "w", encoding = "cp932") as f:
		f.write(json.dumps(chart_objects, indent=4, ensure_ascii=False))