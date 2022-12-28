import dbTools as dbt
import musicdata_tool_inf as infdbt
import os
from dataStores import CONVERSION_DICT

# USAGE SETTINGS              CHANGE YOUR SETTINGS HERE

#version of DB being output
GAME_VERSION = 30
OUTPUT_FILENAME = "iphone (edited).bin"

OMNI_SONG_PATH = None
#OMNI_SONG_PATH = "just_inf"

# Choose bin filenames here (put None to skip any)

# Enter a clean .bin here from IIDX
db_path = "iphone.bin"

# Enter an omnimix bin here
omni_path = None #"ch_v1.1.bin"

# Enter an infinitas bin here
inf_db_path = None #"inf-20221221.bin"

# Custom folder for merged songs  (enter game version 0-29, 0 for 1st style, 1 for substream, 29 for CH etc etc)
use_custom_folder = False

# Enter -1 to skip this feature
custom_inf_folder = 1
# Move songs out of custom infinitas folder before putting them in (same input as above)
move_orig_folder_to = 0
# Decides whether to relocate the omni db or JUST the inf db
change_all_versions = True


# Strip diffs below top difficulty (keeps both another and legg if both exist)
strip_lower_diffs = False

# Choose the max difficulty for removable difficulties
# (eg. using 10 means that 11s and 12s wont be removed)
# Use 0 to leave a gamemode unaffected
remove_sp = 10
remove_dp = 0



#remove charts based on your lamp
#limits are 0 NP, 1 F, 2 AC, 3 EC, 4 NC, 5 HC, 6 EX, 7 FC
#EG using 5 will remove all charts you lack a HC on
fervi_scorepath = None
lamp_limit_sp = 5
lamp_limit_dp = 0




songs_to_remove = ["gigadelic", "Innocent Walls"]





# PROGRAM STARTS HERE
if __name__ == "__main__":
	cwd = os.getcwd()

	if db_path != None:
		header_array, song_index_list, music_db = dbt.createDB(db_path, "AC")

	if omni_path != None:
		omni_header_array, omni_song_index_list, omni_music_db = dbt.createDB(omni_path, "AC")
		
		if use_custom_folder and change_all_versions:
			music_db = dbt.changeVers(music_db, custom_inf_folder, move_orig_folder_to)
		
		music_db = dbt.mergeDBs(music_db, omni_music_db, merge_keys = CONVERSION_DICT, strip_only_inf = False, custom_version = (custom_inf_folder if use_custom_folder else -1))

	if inf_db_path != None:
		inf_header_array, inf_song_index_list, inf_music_db = dbt.createDB(inf_db_path, "INF")

		if use_custom_folder:
			music_db = dbt.changeVers(music_db, custom_inf_folder, move_orig_folder_to)

		music_db = dbt.mergeDBs(music_db, inf_music_db, merge_keys = CONVERSION_DICT, strip_only_inf = False, custom_version = (custom_inf_folder if use_custom_folder else -1))

	if strip_lower_diffs:
		dbt.stripLowers(music_db, max_removable_sp = remove_sp, max_removable_dp = remove_dp)

	if fervi_scorepath is not None and (lamp_limit_sp > 0 or lamp_limit_dp > 0):
		dbt.filterByLamps(music_db, filepath = fervi_scorepath, sp_limit = lamp_limit_sp, dp_limit = lamp_limit_dp)


	with open(OUTPUT_FILENAME, "wb") as write_file:
		infdbt.writer_1a(write_file, music_db, GAME_VERSION)


	if len(songs_to_remove):
		for song in songs_to_remove:
			dbt.removeByTitle(music_db, song)


	if OMNI_SONG_PATH is not None:
		omni_data_folder = os.path.join(cwd, OMNI_SONG_PATH)
		dbt.makeNewOmniFilesRec(omni_data_folder, merge_keys = CONVERSION_DICT, GAME_VERSION = GAME_VERSION)








# bc = 0

# header_array = dbt.arrayFromBinary(db_path, bc, AC_HEADER_FMTSTRING)
# bc += 16

# header_array = header_array[0]

# fmt_string = str(header_array[3]) + "H"
# indices_list = dbt.arrayFromBinary(db_path, bc, fmt_string)
# indices_list = indices_list[0]
# bc += header_array[3] * 2

# song_index_list = dbt.getEntryList(indices_list, 0, header_array[3], raw_binary=False)



# fmt_string = AC_CHART_FMTSTRING
# music_db = dbt.arrayFromBinary(db_path, bc, fmt_string, header_array[2], "AC")
# bc += header_array[3] * 2






# infbc = 0

# inf_header_array = dbt.arrayFromBinary(inf_db_path, infbc, INF_HEADER_FMTSTRING)
# inf_header_array = inf_header_array[0]
# infbc += 16              #skip 4 empty bytes


# fmt_string = str(inf_header_array[3]) + "H"
# inf_indices_list = dbt.arrayFromBinary(inf_db_path, infbc, fmt_string)
# inf_indices_list = inf_indices_list[0]
# infbc += inf_header_array[3] * 2

# song_index_list = dbt.getEntryList(inf_indices_list, 0, inf_header_array[3], raw_binary=False)


# fmt_string = INF_CHART_FMTSTRING
# inf_music_db = dbt.arrayFromBinary(inf_db_path, infbc, fmt_string, inf_header_array[2], "INF")
# infbc += inf_header_array[3] * 2










# data_path = "D:\\Python Projects\\IIDX MusicDB Tools\\omni_data\\data"
# dbt.makeNewOmniFilesRec(data_path, CONVERSION_DICT)









# dbt.exportDBBIN(header_array, indices_list, merged_db, "final.bin.bin", AC_HEADER_FMTSTRING, AC_CHART_FMTSTRING)


#dbt#.makeNewOmniFiles(omni_data_folder, output_data_folder, CONVERSION_DICT)


# for song in inf_music_db:
# 	if song["song_id"] >= 80000:
# 		print(song["genre"].decode(encoding = "cp932").strip("\0"))
# 		print(song["title"].decode(encoding = "cp932").strip("\0"))
# 		print(song["artist"].decode(encoding = "cp932").strip("\0") + "\n")

		
# 		song["song_id"] = 29999
# 		song["game_version"] = 29
# 		music_db.append(song)
# 		indices_list[29999] = header_array
# 		header_array[2] += 1
# 		break
		
























#kkAlias = ["kors k", "disconation", "stripe", "teranoid", "eagle", "maras k", "the 4th"]







# with open("weirdtitles.txt", "wb") as file:
# 	for song in music_db:
# 		if song[0] != song[1]:
# 			file.write(song[0].strip(b"\x00"))
# 			file.write(b"\n")
# 			file.write(song[1].strip(b"\x00"))
# 			file.write(b"\n\n")





# song_index_dict = dbt.getEntryDict(byte_array, bc, header_array[3])
# bc += header_array[3] * 2



# song_index_list = dbt.getEntryList(byte_array, bc, header_array[3], raw_binary = True)
# bc += header_array[3] * 2



# song_array = []

# bc_copy = bc

# for i in range(header_array[2]):
# 	song_array.append(byte_array[bc_copy:bc_copy + 1324])
# 	bc_copy += 1324



# for i in range(0, 5):
# 	print(dbt.stringFromArray(song_array[i], 0, 64))





# if len(song_index_list) != header_array[2]:
# 	raise ValueError("Scores in array do not match number in header.\nEntries listed in header: " + str(header_array[2]) + "\nEntries successfully found: " + len(song_index_list))

# music_db = dbt.makeDB(byte_array, bc, song_index_list)
# bc += 1324 * len(song_index_list)


#dbt.exportDBJSON(header_array, music_db)


# kkAlias = ["kors k", "Disconation", "StripE", "teranoid", "Eagle", "maras k", "The 4th"]

# for song in music_db:
# 	found = False
# 	for alias in kkAlias:
# 		if found == False:
# 			if alias.lower() in song[4].lower():
# 				found = True
	
# 	if (found == False):
# 		continue
	
# 	print(song)













# for i in range(len(music_db)):
# 	if music_db[i][0] == (b"\x83\x73\x83\x41\x83\x6D\x8B\xA6\x91\x74\x8B\xC8\x91\xE6\x82\x50\x94\xD4\x81\x68\xE5\xB6\x89\xCE\x81\x68\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"):
# 		music_db[i][0] = (b"Piano Concerto Op. 1 (SASORIBI)\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
# 		music_db[i][0] = music_db[i][0][:64]


#dbt.exportDBBIN(header_array, indices_list, music_db, "sasori.bin", AC_HEADER_FMTSTRING, AC_CHART_FMTSTRING)

