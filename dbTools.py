from json import dump as makeJSON
from json import load as getJSON
from multiprocessing.sharedctypes import Value
import struct
from dataStores import *
import os
import shutil
#from locale import format_string
#from multiprocessing.sharedctypes import Value




def arrayFromBinary(bin_path, starting_byte_index, fmt_string, iterations = 1, dict_type = "NONE"):
	if dict_type == "NONE":
		return_values = []
	else:
		return_values = {}
	
	bytes_size = struct.calcsize(fmt_string)

	struct_object = struct.Struct(fmt_string)    #instantiates Struct class to use for unpacking the binary (according to header format)

	with open(bin_path, "rb") as f:
		f.seek(starting_byte_index)     #starts reading from correct place in file

		for i in range(iterations):
			data = f.read(bytes_size)
			song_element = list(struct_object.unpack_from(data))

			if dict_type in ["AC", "INF"]:
				dict_entry = dictFromArray(song_element, dict_type)
				return_values[dict_entry["song_id"]] = dict_entry
			else:
				return_values.append(song_element)
			

	return return_values

def dictFromArray(array, dict_type):	
	return_dict = {}

	if dict_type == "AC":
		ref_list = AC_DICT_STRUCTURE
	else:
		ref_list = INF_DICT_STRUCTURE

	for i in range(len(ref_list)):
		return_dict[ref_list[i]] = array[i]

	return return_dict


def makeSubList(list, starting_index, sub_list_size):
	if starting_index < 0:
		raise ValueError("Incorrect index for start of sub list given: " + str(starting_index))
	if starting_index + sub_list_size > len(list):
		raise ValueError(f"Incorrect bounds used.\nSize of list: {len(list)}\nIndex of last value to be added to sublist: {len(list) + sub_list_size}")

	list[starting_index] = [list[starting_index]]
	for i in range(sub_list_size - 1):
		list[starting_index].append(list.pop(starting_index + 1))

	return list


def stringFromArray(array, start_index, char_count):
	return_string = ""

	if (start_index + char_count > len(array) or start_index < 0):
		return return_string

	for i in range(char_count):
		return_string += chr(array[start_index + i])
	
	return return_string

def LEReadData(array, start_index, data_type):
	if data_type == "int":
		length = 4
	elif data_type == "short":
		length = 2
	elif data_type == "long":
		length = 8
	else:
		raise ValueError("Incorrect data type given: " + data_type)

	if (start_index < 0) or (start_index + (length) > len(array)):
		raise ValueError("Invalid start index or data_type given:\nArray length: " + str(len(array)) + "\nStarting index: " + str(start_index) + "\nEnd index: " + str(start_index + length - 1))
	
	return_num = 0

	for i in range(length):
		byte = array[start_index + i]
		byte_HI = byte // 16
		byte_LO = byte % 16

		return_num += byte_HI * (16 ** (2*i + 1)) + byte_LO  * (16 ** (2*i))
	
	return return_num

'''def getEntryDict(array, start_index, num_entries):
	index_dict = {}
	
	for i in range(num_entries):
		index_short = LEReadData(array, start_index + (2 * i), "short")
		if index_short == 0:
			continue

		if (index_short != 65535 and index_short not in index_dict):
			index_dict[index_short] = i
	
	return index_dict'''

def korskify(music_db, aliases, title_template):
	genre_counts = {}
	genre_check = title_template.replace(b"{genre}", b"")

	for i in range(len(aliases)):
		aliases[i] = aliases[i].lower()

	for i in range(len(music_db)):
		song = music_db[i]
		if song[0].startswith(title_template) or song[0].endswith(title_template):
			continue


		found = False
		uni_artist = song[3].decode(encoding="utf-8", errors='ignore').lower()
		
		for alias in aliases:
			if found == False:
				if alias in uni_artist:
					found = True
		
		if (found == False):
			continue
		
		song_genre = song[2]
		new_title = title_template.replace(b"{genre}", song_genre)

		if song_genre in genre_counts:
			genre_counts[song_genre] += 1
			end_index = new_title.find(b"\x00")
			new_title = new_title[:end_index] + b" " + bytes(str(genre_counts[song_genre]), encoding="utf-8") + new_title[end_index:]
		else:
			genre_counts[song_genre] = 1

		new_title = new_title[:64]

		song[0] = new_title
		song[1] = new_title
		song[4] = 0
		song[7] = 0
		song[9] = 0
		
		music_db[i] = song

	return music_db


def getEntryList(array, start_index, num_entries, raw_binary = False):
	index_list = []
	
	if raw_binary == True:
		for i in range(num_entries):
			index_short = LEReadData(array, start_index + (2 * i), "short")
			if (index_short == len(index_list)):
				index_list.append(i)
	else:
		for i in range(num_entries):
			if (array[i] == len(index_list)):
				index_list.append(i)
	
	return index_list

def makeEntry(array, start_index, instructions):
	return_entry = []

	counter = start_index

	for instruction in instructions:
		if isInt(instruction):
			instruction = int(instruction)
			if instruction > 0:
				return_entry.append(stringFromArray(array, counter, instruction).strip("\x00"))
				counter += instruction
			elif instruction < 0:
				counter -= instruction
			else:
				raise ValueError("Instruction of 0 given")
		else:
			if instruction.startswith("i"):
				if instruction.lower() == "id":
					return_entry = [LEReadData(array, counter, "int")] + return_entry
					counter += 4
				else:
					return_entry.append(LEReadData(array, counter, "int"))
					counter += 4
			elif instruction.startswith("s"):
				return_entry.append(LEReadData(array, counter, "short"))
				counter += 2
			elif instruction.startswith("a"):
				subarray_size = int(instruction[1:])
				return_entry.append(array[counter:counter + subarray_size])
				counter += subarray_size
			else:
				raise ValueError("Invalid instruction given: " + instruction)

	return return_entry


def isInt(string):
	try:
		int(string)
		return True
	except:
		return False

def makeDB(array, start_index, song_indices):
	return_list = []
	entry_instructions = [64, 64, 64, 64, "i", "i", "i", "i", -8, "s", -6, "a5", "a5", -10, "i", -120, "i", -508, -4, -16, 16]
	
	for i in range(len(song_indices)):
		return_list.append([song_indices[i]] + makeEntry(array, start_index + 1324 * i, entry_instructions))

	return return_list



def makeSongData(songDataArray):
	return_list = []

	for i in range(len(songDataArray)):
		new_dict = {
			"song_id": songDataArray[i][0],
            "title": songDataArray[i][1],
            "title_ascii": songDataArray[i][2],
            "genre": songDataArray[i][3],
            "artist": songDataArray[i][4],
            "texture_title": songDataArray[i][5],
            "texture_artist": songDataArray[i][6],
            "texture_genre": songDataArray[i][7],
            "texture_load": songDataArray[i][8],
            #"texture_list": songDataArray[i][4],
            #"font_idx": 0,
            "game_version": songDataArray[i][9],
            #"other_folder": 1,          fskip 2
            #"bemani_folder": 0,         fskip 2
            #"splittable_diff": 0,       fskip 3
            "difficulties": songDataArray[i][10] + songDataArray[i][11],
            #"volume": 105,        fskip

#            "file_identifiers": [              fskip 10
#                48,
#                49,
#                97,
#                97,
#                48,
#                48,
#                50,
#                97,
#                97,
#                48
#            ],

            "bga_filename": songDataArray[i][14]
		}

		return_list.append(new_dict)
	return return_list


def exportDBJSON(header_array, songDataArray, output_path = "db.json"):
	outputDict = {
		"data_ver": header_array[1],
		"data": makeSongData(songDataArray)
	}

	with open(output_path, "w", encoding = "utf-8") as json_path:
		makeJSON(outputDict, json_path, indent = 4)

def arrayToBinary(file_object, input_array, fmt_string, iterations = 1, offset = 0):
	struct_object = struct.Struct(fmt_string)    #instantiates Struct class to use for unpacking the binary (according to header format)
	if not isinstance(input_array[0], list):
		input_array = [input_array]
	
	data_offset = offset

	for i in range(iterations):
		array = input_array[i]
		fmt_copy = list(fmt_string)
		data_counter = 0

		bin_string = struct.pack(fmt_string, *array)
		file_object.write(bin_string)
		'''
		letter_index = -1
		while fmt_copy != []:
			for i in range(len(fmt_copy)):
				if not isInt(fmt_copy[i]):
					letter_index = i
					break
		
			if letter_index == -1:
				raise ValueError("Incorrect format given: " + fmt_string)


			current_instruction = fmt_copy[:letter_index + 1]
			for i in range(len(current_instruction)):
				fmt_copy.pop(0)

			amount = 0

			if len(current_instruction) > 1:
				for i in range(len(current_instruction) - 1):
					amount += int(current_instruction[len(current_instruction) - 2 - i]) + 10 ** i
			else:
				amount += 1
			
			if current_instruction[-1] == "s":
				file_object.write(array[data_counter])
				data_counter += 1
				data_offset += amount
				


			elif current_instruction[-1] == "i":
				struct_object = struct.Struct("i")
				for i in range(amount):
					converted_int = struct_object.pack("i", array[data_counter].to_bytes(4, byteorder = "little", signed=False))
					file_object.write(converted_int)
					data_counter += 1
				data_offset += amount * 4

			elif current_instruction[-1] == "h":
				struct_object = struct.Struct("h")
				for i in range(amount):
					struct_object.pack_into("h", file_object, data_offset, array[data_counter])
					data_counter += 1
				data_offset += amount * 2
			
			else:
				raise ValueError("Invalid instruction: " + current_instruction[-1])
		'''



def makeIDDB(array, version):
	return_list = [b"\xff\xff"] * ((version) * 1000)
	return_list += [b"\x00\x00"] * 1000
	found_zero = False


	for i in range(len(array)):
		if array[i] != -1:
			if ((found_zero == False and array[i] == 0) or (found_zero == True and array[i] != 0)):
				return_list[i] = struct.pack("<H", array[i])
			else:
				return_list[i] = struct.pack("<H", array[i])		
		
	
	return_string = b""
	for item in return_list:
		return_string += item

	return return_string

'''
def convertINFToAC(song_entry):
	if len(song_entry) == 51:
		print("Entry is already in AC format: " + song_entry[0].decode("cd932").strip("\0"))
		return song_entry
	elif len(song_entry) != 53:
		raise ValueError("Bad song data given. Has length of " + str(len(song_entry)))
'''





def exportDBBIN(header_array, index_db, songDataArray, fmt_header, fmt_chartstring, output_path = "music_data (modified).bin"):
	with open(output_path, "wb") as db_path:
		arrayToBinary(db_path, header_array, fmt_header)
		db_path.write(makeIDDB(index_db, header_array[1]))

		write_offset = struct.calcsize(fmt_header) + struct.calcsize(fmt_chartstring)
		arrayToBinary(db_path, songDataArray, fmt_chartstring, len(songDataArray), write_offset)


def encodeToBinary(in_string, length, fill = "\0"):
	encoded_string = in_string[:length].encode(encoding = "cp932")

	if len(in_string) < length:
		encoded_string += (fill * (length - len(encoded_string))).encode("cp932")

	return encoded_string


def changeID(entry, new_ID, new_version = -1):
	entry["song_id"] = new_ID

	bga_filename = entry["bga_filename"].decode(encoding = "cp932").strip("\0")
	found_int = findIntInString(bga_filename, length = 5)
	if found_int != None:
		entry["bga_filename"] = encodeToBinary(str(new_ID), 32)

	

	if new_version == -1:
		entry["game_version"] = new_ID // 1000
	else:
		entry["game_version"] = new_version

	return entry

def listDictInsert(main_list, new_element, attribute = "song_id"):
	for i in range(len(main_list)):
		if main_list[i][attribute] < new_element[attribute]:
			main_list.insert(i, new_element)
			return main_list

	print("Could not insert element into main list: ")
	print(new_element)
	print("\n")
	return main_list

def makeDiffList(song):
	return_list = []



	for diff in SONG_POSSIBLE_DIFFS:
		return_list.append(song[diff])
	
	return return_list

def mergeDiffs(entry, main_diffs, sub_diffs):
	for i in range(10):
		if main_diffs[i] == 0:
			if sub_diffs[i] != 0:
				entry[SONG_POSSIBLE_DIFFS[i]] = sub_diffs[i]
	
	return entry


def mergeDBs(db_main, db_sub, merge_keys = {}, strip_only_inf = False, custom_version = -1, merge_diffs = True):
	for song_key in db_sub:         #Each song in new db
		if (strip_only_inf and song_key < 80000):
			continue
		
		if song_key in merge_keys:
			new_ID = merge_keys[song_key]
			new_entry = changeID(db_sub[song_key], new_ID, custom_version)
		else:
			new_ID = song_key
			new_entry = db_sub[song_key]
		
		if new_ID in db_main:
			if not merge_diffs:
				continue

			old_diffs = makeDiffList(db_main[new_ID])
			new_diffs = makeDiffList(db_sub[song_key])

			if new_diffs != old_diffs:
				new_entry = mergeDiffs(db_main[song_key], old_diffs, new_diffs)
				db_main[song_key] = new_entry
			else:
				continue
		
		else:
			db_main[new_entry["song_id"]] = new_entry

	return db_main


def stripLowers(music_db, max_removable_sp = 12, max_removable_dp = 12):
	if not (max_removable_sp in range(1, 13) or max_removable_dp in range(1, 13)):
		print(f"No songs are removable.\nSP: {max_removable_sp}\nDP: {max_removable_dp}")
		return

	for song_key in music_db:
		song = music_db[song_key]
		diffs = makeDiffList(song)
		new_diffs = diffs[:]

		if diffs[2] == 12:
			found = True

		if max_removable_sp in range(1, 13):
			max_sp = None
			for i in reversed(range(5)):
				if diffs[i] != 0:
					max_sp = i
					break
			
			if max_sp != None:
				# Ensures the legg and another are both kept
				for i in range(3 if (max_sp >= 3) else max_sp):
					if diffs[i] <= max_removable_sp:
						new_diffs[i] = 0			


		if max_removable_dp in range(1, 13):
			max_dp = None
			for i in reversed(range(0 + 5, 5 + 5)):
				if diffs[i] != 0:
					max_dp = i
					break
			
			if max_dp != None:
				if max_dp >= 3 + 5:
					for i in range(0 + 5, (3 + 5) if (max_dp >= 3 + 5) else max_dp):
						if diffs[i] <= max_removable_dp:
							new_diffs[i] = 0
		
		if diffs != new_diffs:
			for i in range(len(SONG_POSSIBLE_DIFFS)):
				song[SONG_POSSIBLE_DIFFS[i]] = new_diffs[i]

		

# def normStr(string, index):
# 	if index > len(string) - 1:
# 		return ""
# 	else:
# 		return string[index:]

def findIntInString(string, length = 5):
	if len(string) < length:
		return None
	
	for i in range(len(string) - length + 1):
		splice = string[i:i+length]
		if isInt(splice):
			return splice

	return None

def replaceFileDir(base_dir, filename, merge_keys):
	song_id = findIntInString(filename)

	if song_id == None:
		return False

	if int(song_id) in merge_keys:
		new_id = str(merge_keys[int(song_id)])

		if song_id == new_id:
			return False

		old_path = os.path.join(base_dir, filename)
		new_path = os.path.join(base_dir, filename.replace(song_id, new_id))
		os.rename(old_path, new_path)

		return True
	else:
		return False

def extractPreviews(base_path):
	previews_path = os.path.join(base_path, "preview")

	base_dirs = os.listdir(base_path)
	base_dirs.remove("preview")

	for dir in base_dirs:
		if not os.path.isdir(os.path.join(base_path, dir)):
			base_dirs.remove(dir)
	

	for (dirpath, dirnames, filenames) in os.walk(previews_path):
		for filename in filenames:

			preview_id = findIntInString(filename)

			if preview_id != None:
				old_path = os.path.join(dirpath, filename)
				if preview_id in base_dirs:
					new_path = os.path.join(base_path, preview_id)
					new_path = os.path.join(new_path, filename)
				else:
					new_path = os.path.join(base_path, filename)

				shutil.copyfile(old_path, new_path)

			else:
				continue
	
	if len(os.listdir(previews_path)) == 0:
		os.remove(previews_path)

def changeVers(music_db, old_ver, new_ver):
	for key in music_db:
		if music_db[key]["game_version"] == old_ver:
			music_db[key]["game_version"] = new_ver
	
	return music_db

def makeNewOmniFilesRec(path, merge_keys):
	for (dirpath, dirnames, filenames) in os.walk(path):
		for dirname in dirnames:
			makeNewOmniFilesRec(os.path.join(dirpath, dirname), merge_keys)
			replaceFileDir(dirpath, dirname, merge_keys)

		if os.path.exists(os.path.join(dirpath, "preview")):
			extractPreviews(dirpath)

		for filename in filenames:
			replaceFileDir(dirpath, filename, merge_keys)

def createDB(file_path, db_type):
	if db_type == "AC":
		header_fmt = AC_HEADER_FMTSTRING
		song_fmt = AC_CHART_FMTSTRING
	elif db_type == "INF":
		header_fmt = INF_HEADER_FMTSTRING
		song_fmt = INF_CHART_FMTSTRING
	else:
		raise ValueError("Invalid Music DB type given, AC or IIDX REQUIRED, " + str(db_type) + " given.")

	bc = 0

	header_array = arrayFromBinary(file_path, bc, header_fmt)
	bc += struct.calcsize(header_fmt)

	header_array = header_array[0]

	fmt_string = str(header_array[3]) + "H"
	indices_list = arrayFromBinary(file_path, bc, fmt_string)
	indices_list = indices_list[0]
	bc += header_array[3] * 2

	song_index_list = getEntryList(indices_list, 0, header_array[3], raw_binary=False)

	music_db = arrayFromBinary(file_path, bc, song_fmt, header_array[2], db_type)
	bc += header_array[3] * 2

	return header_array, song_index_list, music_db


def filterByLamps(music_db, filepath, sp_limit, dp_limit):
	try:
		with open(filepath, "r") as file:
			scores_db = getJSON(file)
	except Exception as e:
		print(f"Unable to open {filepath}. Exception printed below.")
		print(e.message)
		return
	
	#remove non song IDS
	for key in scores_db:
		if not isInt(key):
			scores_db.pop(key)
	



# def makeNewOmniFiles2(old_path, new_path, merge_keys):
# 	for (dirpath, dirnames, filenames) in os.walk(cwd):
# 		for dirname in dirnames:
# 			if dirname.startswith("8"):
# 				new_id = str(int(dirname) - 50,500)
# 				inside_dir = os.path.join(dirpath, dirname)
# 				for (x, y, infilenames) in os.walk(inside_dir):
# 					for infile in infilenames:
# 						if not infile.startswith("8"):
# 							old_path = os.path.join(inside_dir, infile)
# 							new_path = os.path.join(inside_dir, new_id + infile[5:])
# 							os.rename(old_path, new_path)


# def makeNewOmniFiles(old_path, new_path, merge_keys):
# 	old_data = os.path.join(old_path, "data")
# 	old_sound = os.path.join(old_data, "sound")
# 	old_previews = os.path.join(old_sound, "preview")

# 	new_data = os.path.join(new_path, "data")
# 	new_sound = os.path.join(new_data, "sound")
# 	new_previews = os.path.join(new_sound, "preview")

# 	for (dirpath, dirnames, filenames) in os.walk(old_previews):
# 		for filename in filenames:
# 			id = filename[:5]
# 			if int(id) in merge_keys:
# 				new_id = str(merge_keys[int(id)])
# 			else:
# 				new_id = id

# 			old_path = os.path.join(old_previews, filename)
# 			folder_path = os.path.join(new_sound, new_id)
# 			new_path = os.path.join(folder_path, new_id + "_pre.2dx")

# 			if not os.path.exists(folder_path):
# 				os.makedirs(folder_path)
			
# 			if not os.path.exists(new_path):
# 				shutil.copy(old_path, new_path)

	