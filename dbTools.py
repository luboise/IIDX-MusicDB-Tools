from json import dump as makeJSON
from locale import format_string
import struct

def arrayFromBinary(bin_path, starting_byte_index, fmt_string, iterations = 1, condense_index = -1):
	return_values = []
	bytes_size = struct.calcsize(fmt_string)

	struct_object = struct.Struct(fmt_string)    #instantiates Struct class to use for unpacking the binary (according to header format)

	with open(bin_path, "rb") as f:
		f.seek(starting_byte_index)     #starts reading from correct place in file

		for i in range(iterations):
			data = f.read(bytes_size)
			song_element = list(struct_object.unpack_from(data))
			if condense_index >= 0:
				song_element = makeSubList(song_element, 14, 10)
			return_values.append(song_element)

	if len(return_values) == 1:
		return return_values[0]
	else:
		return return_values

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





def exportDBBIN(header_array, index_db, songDataArray, output_path = "music_data (modified).bin"):
	fmt_header = "<4sihh4x"
	fmt_chartstring = "<64s64s64s64siiiiiihhhh10B10si120si508si16s16s344s"
	with open(output_path, "wb") as db_path:
		arrayToBinary(db_path, header_array, fmt_header)
		db_path.write(makeIDDB(index_db, header_array[1]))

		write_offset = struct.calcsize(fmt_header) + struct.calcsize(fmt_chartstring)
		arrayToBinary(db_path, songDataArray, fmt_chartstring, len(songDataArray), write_offset)
