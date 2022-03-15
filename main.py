import dbTools as dbt

dbpath = "music_data.bin"

byte_array = []
with open(dbpath, "rb") as bin_file:
	for line in bin_file:
		byte_array += list(line)

bc = 0    #byte counter


magic_string = dbt.stringFromArray(byte_array, bc, 4)    #first 4 bytes are magic string (1 character per byte)
bc += 4

version = dbt.LEReadData(byte_array, bc, "int")                  #next 4 bytes are game version (integer)
bc += 4

entry_count = dbt.LEReadData(byte_array, bc, "short")    #next 2 bytes are amount of songs in db
bc += 2

index_count = dbt.LEReadData(byte_array, bc, "short")    #next 2 bytes are total amount of indices available, (version + 1) * 1000 in this case
bc += 2



bc += 4              #skip 4 empty bytes



#coming up is index_count * 2 bytes (2 bytes for each index). The value of each index tells of the value in the entries 

song_dict = dbt.getEntryDict(byte_array, bc, index_count)
bc += index_count * 2

music_db = dbt.makeDB(byte_array, bc, entry_count, song_dict)
bc += 1324 * entry_count

kkAlias = ["kors k", "Disconation", "StripE", "teranoid", "Eagle", "maras k", "The 4th"]

for song in music_db:
	found = False
	for alias in kkAlias:
		if found == False:
			if alias.lower() in song[4].lower():
				found = True
	
	if (found == False):
		continue

	song[1] = "kors k's How to make " + song[3]

	print(song[3])
	print(song[1])
	print(song[4] + "\n")

