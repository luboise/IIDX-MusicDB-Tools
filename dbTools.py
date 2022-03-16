from json import dump as makeJSON

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


def getEntryList(array, start_index, num_entries):
	index_list = []
	
	for i in range(num_entries):
		index_short = LEReadData(array, start_index + (2 * i), "short")
		if (index_short == len(index_list)):
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


def exportDB(songDataArray, header_array, output_path = "db.json"):
	outputDict = {
		"data_ver": header_array[1],
		"data": makeSongData(songDataArray)
	}

	with open(output_path, "w", encoding = "utf-8") as json_path:
		makeJSON(outputDict, json_path, indent = 4)
