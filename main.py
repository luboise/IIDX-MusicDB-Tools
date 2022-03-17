import dbTools as dbt
import struct

db_path = "music_data.bin"

bc = 0

header_array = dbt.arrayFromBinary(db_path, bc, "4sihh4x")
bc += 16              #skip 4 empty bytes


fmt_string = str(header_array[3]) + "h"
indices_list = dbt.arrayFromBinary(db_path, bc, fmt_string)
bc += header_array[3] * 2

song_index_list = dbt.getEntryList(indices_list, 0, header_array[3], raw_binary=False)


#coming up is index_count * 2 bytes (2 bytes for each index). The value of each index tells of the value in the entries 


fmt_string = "64s64s64s64siiiiiihhhh10B10si120si508si16s16s344s"
music_db = dbt.arrayFromBinary(db_path, bc, fmt_string, header_array[2])
bc += header_array[3] * 2





kkAlias = ["kors k", "disconation", "stripe", "teranoid", "eagle", "maras k", "the 4th"]

music_db = dbt.korskify(music_db, kkAlias, b"kors k's How to make {genre}")



dbt.exportDBBIN(header_array, indices_list, music_db)




'''
song_index_dict = dbt.getEntryDict(byte_array, bc, header_array[3])
bc += header_array[3] * 2
'''

'''
song_index_list = dbt.getEntryList(byte_array, bc, header_array[3], raw_binary = True)
bc += header_array[3] * 2
'''

'''
song_array = []

bc_copy = bc

for i in range(header_array[2]):
	song_array.append(byte_array[bc_copy:bc_copy + 1324])
	bc_copy += 1324



for i in range(0, 5):
	print(dbt.stringFromArray(song_array[i], 0, 64))





if len(song_index_list) != header_array[2]:
	raise ValueError("Scores in array do not match number in header.\nEntries listed in header: " + str(header_array[2]) + "\nEntries successfully found: " + len(song_index_list))

music_db = dbt.makeDB(byte_array, bc, song_index_list)
bc += 1324 * len(song_index_list)


#dbt.exportDBJSON(header_array, music_db)
'''

'''
kkAlias = ["kors k", "Disconation", "StripE", "teranoid", "Eagle", "maras k", "The 4th"]

for song in music_db:
	found = False
	for alias in kkAlias:
		if found == False:
			if alias.lower() in song[4].lower():
				found = True
	
	if (found == False):
		continue
	
	print(song)
'''