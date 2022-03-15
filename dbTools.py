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

def getEntryDict(array, start_index, num_entries):
	index_dict = {}
	
	for i in range(num_entries):
		index_short = LEReadData(array, start_index + (2 * i), "short")

		if index_short != 65535:
			index_dict[index_short] = i
	
	return index_dict

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

def makeDB(array, start_index, num_entries, entry_dict):
	return_list = []
	entry_instructions = [64, 64, 64, 64, "i", "i", "i", "i", -8, "s", -6, "a5", "a5", -10, "i", -120, "i", -508, "id", -16, 16]
	
	for i in range(num_entries):
		return_list.append(makeEntry(array, start_index + 1324 * i, entry_instructions))

	return return_list
