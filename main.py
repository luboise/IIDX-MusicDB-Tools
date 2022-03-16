import dbTools as dbt

dbpath = "music_data.bin"

byte_array = []
with open(dbpath, "rb") as bin_file:
	for line in bin_file:
		byte_array += list(line)

bc = 0    #byte counter

header_instructions = [4, "i", "s", "s"]      #magic_string, version, entry_number, index_number
header_array = dbt.makeEntry(byte_array, bc, header_instructions)

bc += 16              #skip 4 empty bytes



#coming up is index_count * 2 bytes (2 bytes for each index). The value of each index tells of the value in the entries 




'''
song_index_dict = dbt.getEntryDict(byte_array, bc, header_array[3])
bc += header_array[3] * 2
'''


song_index_list = dbt.getEntryList(byte_array, bc, header_array[3])
bc += header_array[3] * 2


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


#dbt.exportDB(music_db, header_array)


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