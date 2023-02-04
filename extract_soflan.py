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
db_path = "RESIDENT 20221031 0626.bin"

sound_folder = "C:\\LDJ-003-2022101900\\contents\\data\\sound"
extra_folder = "C:\\LDJ-003-2022101900\\contents\\data_modss\\resident_omni\\sound"


if __name__ == "__main__":
	pog_db = dbt.IIDXMusicDB(db_path, "AC")

	song_objects = None
	chart_objects = None

	USE_EXISTING_OBJECTS = False
	if USE_EXISTING_OBJECTS:
		with open("song_objects.json", "r", encoding="utf-8") as f:
			song_objects = json.load(f)
		with open("chart_objects.json", "r", encoding="utf-8") as f:
			chart_objects = json.load(f)
	else:
		song_objects, chart_objects = pog_db.getSoflanCharts(sound_folder, extra_folder)

	script_path = os.path.dirname(__file__)
	OLD_THEORY_PATH = os.path.abspath(os.path.join(script_path, "..", "old_theory", "docs", "resources", "chartdirectory"))

	method_objects = pog_db.portOldTheoryMethods(chart_objects, OLD_THEORY_PATH)

	with open("song_objects_out.json", "w", encoding = "utf-8") as f:
		f.write(json.dumps(song_objects, indent=4, ensure_ascii=False))
	with open("chart_objects_out.json", "w", encoding = "utf-8") as f:
		f.write(json.dumps(chart_objects, indent=4, ensure_ascii=False))
	with open("method_objects_out.json", "w", encoding = "utf-8") as f:
		f.write(json.dumps(method_objects, indent=4, ensure_ascii=False))