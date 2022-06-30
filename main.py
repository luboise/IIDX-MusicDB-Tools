import dbTools as dbt
import musicdata_tool_inf as infdbt
import os
from dataStores import CONVERSION_DICT

cwd = os.getcwd()
omni_data_folder = os.path.join(cwd, "omni_data")
output_data_folder = os.path.join(cwd, "data_output")

db_path = "music_data_0620.bin"
#bpl_path = "music_data_bpl.bin"
omni_path = "CH 0509+omni+inf.bin"
inf_db_path = "inf_music_data.bin"

header_array, song_index_list, music_db = dbt.createDB(db_path, "AC")
#header_array, song_index_list, music_db = dbt.createDB(bpl_path, "AC")
#header_array, song_index_list, music_db = dbt.createDB(secret_path, "AC")

omni_header_array, omni_song_index_list, omni_music_db = dbt.createDB(omni_path, "AC")
inf_header_array, inf_song_index_list, inf_music_db = dbt.createDB(inf_db_path, "INF")

# music_db = dbt.mergeDBs(music_db, omni_music_db, CONVERSION_DICT, strip_only_inf = False)
music_db = dbt.changeVers(music_db, 1, 0)
music_db = dbt.mergeDBs(music_db, omni_music_db, merge_keys = CONVERSION_DICT, strip_only_inf=False)
merged_db = dbt.mergeDBs(music_db, inf_music_db, CONVERSION_DICT, strip_only_inf = True, custom_version = 1)

with open("out.bin", "wb") as write_file:
	infdbt.writer_1a(write_file, merged_db, 29)

# omni_files = os.path.join(omni_data_folder, "data")
# dbt.makeNewOmniFilesRec(omni_files, merge_keys = CONVERSION_DICT)








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

