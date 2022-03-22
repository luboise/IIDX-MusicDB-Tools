import argparse
import ctypes
import json
import sys
import struct


def read_string(infile, length, encoding='cp932'):
    return infile.read(length).decode(encoding).strip('\0')

def write_string_nonbinary(outfile, input, length, fill='\0', encoding='cp932'):
    string_data = input[:length].encode(encoding)
    outfile.write(string_data)

    if len(input) < length:
        outfile.write("".join([fill] * (length - len(string_data))).encode(encoding))

def write_string(outfile, input, length, fill='\0', encoding='cp932'):
    outfile.write(input)

# IIDX INFINITAS READER
def reader_19(infile, song_count):
    song_entries = []

    for i in range(song_count):
        title = read_string(infile, 0x40)
        title_ascii = read_string(infile, 0x40)
        genre = read_string(infile, 0x40)
        artist = read_string(infile, 0x40)

        texture_title, texture_artist, texture_genre, texture_load, texture_list = struct.unpack("<IIIII", infile.read(20))
        font_idx, game_version = struct.unpack("<IH", infile.read(6))
        other_folder, bemani_folder, splittable_diff = struct.unpack("<HHH", infile.read(6))

        SPB_diff, SPN_diff, SPH_diff, SPA_diff, SPL_diff, DPB_diff, DPN_diff, DPH_diff, DPA_diff, DPL_diff, = struct.unpack("<BBBBBBBBBB", infile.read(10))

        unk_sect1 = infile.read(0x146)

        song_id, volume = struct.unpack("<II", infile.read(8))

        SPB_ident = read_string(infile, 1)
        SPN_ident = read_string(infile, 1)
        SPH_ident = read_string(infile, 1)
        SPA_ident = read_string(infile, 1)
        SPL_ident = read_string(infile, 1)
        DPB_ident = read_string(infile, 1)
        DPN_ident = read_string(infile, 1)
        DPH_ident = read_string(infile, 1)
        DPA_ident = read_string(infile, 1)
        DPL_ident = read_string(infile, 1)

        bga_delay = ctypes.c_short(struct.unpack("<H", infile.read(2))[0]).value
        unk_sect2 = infile.read(2)
        bga_filename = read_string(infile, 0x20)

        unk_sect3 = infile.read(2)

        afp_flag = struct.unpack("<I", infile.read(4))[0]

        afp_data0 = read_string(infile, 0x20)
        afp_data1 = read_string(infile, 0x20)
        afp_data2 = read_string(infile, 0x20)
        afp_data3 = read_string(infile, 0x20)
        afp_data4 = read_string(infile, 0x20)
        afp_data5 = read_string(infile, 0x20)
        afp_data6 = read_string(infile, 0x20)
        afp_data7 = read_string(infile, 0x20)
        afp_data8 = read_string(infile, 0x20)
        afp_data9 = read_string(infile, 0x20)

        unk_sect4 = infile.read(4)

        song_entries.append({
            'song_id': song_id,
            'title': title,
            'title_ascii': title_ascii,
            'genre': genre,
            'artist': artist,
            'texture_title': texture_title,
            'texture_artist': texture_artist,
            'texture_genre': texture_genre,
            'texture_load': texture_load,
            'texture_list': texture_list,
            'font_idx': font_idx,
            'game_version': game_version,
            'other_folder': other_folder,
            'bemani_folder': bemani_folder,
            'splittable_diff': splittable_diff,
            'SPB_diff': SPB_diff,
            'SPN_diff': SPN_diff,
            'SPH_diff': SPH_diff,
            'SPA_diff': SPA_diff,
            'SPL_diff': SPL_diff,
            'DPB_diff': DPB_diff,
            'DPN_diff': DPN_diff,
            'DPH_diff': DPH_diff,
            'DPA_diff': DPA_diff,
            'DPL_diff': DPL_diff,
            'volume': volume,
            'SPB_ident': SPB_ident,
            'SPN_ident': SPN_ident,
            'SPH_ident': SPH_ident,
            'SPA_ident': SPA_ident,
            'SPL_ident': SPL_ident,
            'DPB_ident': DPB_ident,
            'DPN_ident': DPN_ident,
            'DPH_ident': DPH_ident,
            'DPA_ident': DPA_ident,
            'DPL_ident': DPL_ident,
            'bga_filename': bga_filename,
            'bga_delay': bga_delay,
            'afp_flag': afp_flag,
            'afp_data0': afp_data0,
            'afp_data1': afp_data1,
            'afp_data2': afp_data2,
            'afp_data3': afp_data3,
            'afp_data4': afp_data4,
            'afp_data5': afp_data5,
            'afp_data6': afp_data6,
            'afp_data7': afp_data7,
            'afp_data8': afp_data8,
            'afp_data9': afp_data9,
            'unk_sect1': unk_sect1.hex(),
            'unk_sect2': unk_sect2.hex(),
            'unk_sect3': unk_sect3.hex(),
            'unk_sect4': unk_sect4.hex(),
        })

    return song_entries

# IIDX INFINITAS WRITER
def writer_19(outfile, data):
    DATA_VERSION = 80
    MAX_ENTRIES = 81000
    CUR_STYLE_ENTRIES = MAX_ENTRIES - 1000

    # Write header
    outfile.write(b"IIDX")
    outfile.write(struct.pack("<III", DATA_VERSION, len(data), MAX_ENTRIES))

    # Write song index table
    exist_ids = {}
    for song_data in data:
        exist_ids[song_data['song_id']] = True

    cur_song = 0
    for i in range(MAX_ENTRIES):
        if i in exist_ids:
            outfile.write(struct.pack("<H", cur_song))
            cur_song += 1
        elif i >= CUR_STYLE_ENTRIES:
            outfile.write(struct.pack("<H", 0x0000))
        else:
            outfile.write(struct.pack("<H", 0xffff))

    # Write song entries
    for song_data in data:
        write_string(outfile, song_data['title'], 0x40)
        write_string(outfile, song_data['title_ascii'], 0x40)
        write_string(outfile, song_data['genre'], 0x40)
        write_string(outfile, song_data['artist'], 0x40)

        outfile.write(struct.pack("<IIIII", song_data['texture_title'], song_data['texture_artist'], song_data['texture_genre'], song_data['texture_load'], song_data['texture_list']))
        outfile.write(struct.pack("<IH", song_data['font_idx'], song_data['game_version']))
        outfile.write(struct.pack("<HHH", song_data['other_folder'], song_data['bemani_folder'], song_data['splittable_diff']))

        outfile.write(struct.pack("<BBBBBBBBBB", song_data['SPB_diff'], song_data['SPN_diff'], song_data['SPH_diff'], song_data['SPA_diff'], song_data['SPL_diff'], song_data['DPB_diff'], song_data['DPN_diff'], song_data['DPH_diff'], song_data['DPA_diff'], song_data['DPL_diff']))

        outfile.write(bytes.fromhex(song_data.get('unk_sect1','00000000000001000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000030000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')))

        outfile.write(struct.pack("<II", song_data['song_id'], song_data['volume']))

        write_string(outfile, song_data['SPB_ident'], 1)
        write_string(outfile, song_data['SPN_ident'], 1)
        write_string(outfile, song_data['SPH_ident'], 1)
        write_string(outfile, song_data['SPA_ident'], 1)
        write_string(outfile, song_data['SPL_ident'], 1)
        write_string(outfile, song_data['DPB_ident'], 1)
        write_string(outfile, song_data['DPN_ident'], 1)
        write_string(outfile, song_data['DPH_ident'], 1)
        write_string(outfile, song_data['DPA_ident'], 1)
        write_string(outfile, song_data['DPL_ident'], 1)

        outfile.write(struct.pack("<h", song_data['bga_delay']))
        outfile.write(bytes.fromhex(song_data.get('unk_sect2','0000')))
        write_string(outfile, song_data['bga_filename'], 0x20)
        outfile.write(bytes.fromhex(song_data.get('unk_sect3','0000')))

        outfile.write(struct.pack("<I", song_data['afp_flag']))

        write_string(outfile, song_data['afp_data0'], 0x20)
        write_string(outfile, song_data['afp_data1'], 0x20)
        write_string(outfile, song_data['afp_data2'], 0x20)
        write_string(outfile, song_data['afp_data3'], 0x20)
        write_string(outfile, song_data['afp_data4'], 0x20)
        write_string(outfile, song_data['afp_data5'], 0x20)
        write_string(outfile, song_data['afp_data6'], 0x20)
        write_string(outfile, song_data['afp_data7'], 0x20)
        write_string(outfile, song_data['afp_data8'], 0x20)
        write_string(outfile, song_data['afp_data9'], 0x20)

        outfile.write(bytes.fromhex(song_data.get('unk_sect4','00000000')))

# IIDX28 Bistrover reader
def reader_1a(infile, song_count):
    song_entries = []

    for i in range(song_count):
        title = read_string(infile, 0x40)
        title_ascii = read_string(infile, 0x40)
        genre = read_string(infile, 0x40)
        artist = read_string(infile, 0x40)

        texture_title, texture_artist, texture_genre, texture_load, texture_list = struct.unpack("<IIIII", infile.read(20))
        font_idx, game_version = struct.unpack("<IH", infile.read(6))
        other_folder, bemani_folder, splittable_diff = struct.unpack("<HHH", infile.read(6))

        SPB_diff, SPN_diff, SPH_diff, SPA_diff, SPL_diff, DPB_diff, DPN_diff, DPH_diff, DPA_diff, DPL_diff, = struct.unpack("<BBBBBBBBBB", infile.read(10))

        unk_sect1 = infile.read(646)

        song_id, volume = struct.unpack("<II", infile.read(8))

        SPB_ident = read_string(infile, 1)
        SPN_ident = read_string(infile, 1)
        SPH_ident = read_string(infile, 1)
        SPA_ident = read_string(infile, 1)
        SPL_ident = read_string(infile, 1)
        DPB_ident = read_string(infile, 1)
        DPN_ident = read_string(infile, 1)
        DPH_ident = read_string(infile, 1)
        DPA_ident = read_string(infile, 1)
        DPL_ident = read_string(infile, 1)

        bga_delay = ctypes.c_short(struct.unpack("<H", infile.read(2))[0]).value
        bga_filename = read_string(infile, 0x20)

        afp_flag = struct.unpack("<I", infile.read(4))[0]

        afp_data0 = read_string(infile, 0x20)
        afp_data1 = read_string(infile, 0x20)
        afp_data2 = read_string(infile, 0x20)
        afp_data3 = read_string(infile, 0x20)
        afp_data4 = read_string(infile, 0x20)
        afp_data5 = read_string(infile, 0x20)
        afp_data6 = read_string(infile, 0x20)
        afp_data7 = read_string(infile, 0x20)
        afp_data8 = read_string(infile, 0x20)
        afp_data9 = read_string(infile, 0x20)
		
        unk_sect3 = infile.read(4)

        song_entries.append({
            'song_id': song_id,
            'title': title,
            'title_ascii': title_ascii,
            'genre': genre,
            'artist': artist,
            'texture_title': texture_title,
            'texture_artist': texture_artist,
            'texture_genre': texture_genre,
            'texture_load': texture_load,
            'texture_list': texture_list,
            'font_idx': font_idx,
            'game_version': game_version,
            'other_folder': other_folder,
            'bemani_folder': bemani_folder,
            'splittable_diff': splittable_diff,
			'SPB_diff': SPB_diff,
            'SPN_diff': SPN_diff,
            'SPH_diff': SPH_diff,
            'SPA_diff': SPA_diff,
			'SPL_diff': SPL_diff,
			'DPB_diff': DPB_diff,
            'DPN_diff': DPN_diff,
            'DPH_diff': DPH_diff,
            'DPA_diff': DPA_diff,
			'DPL_diff': DPL_diff,
            'volume': volume,
			'SPB_ident': SPB_ident,
            'SPN_ident': SPN_ident,
            'SPH_ident': SPH_ident,
            'SPA_ident': SPA_ident,
			'SPL_ident': SPL_ident,
			'DPB_ident': DPB_ident,
            'DPN_ident': DPN_ident,
            'DPH_ident': DPH_ident,
            'DPA_ident': DPA_ident,
			'DPL_ident': DPL_ident,
            'bga_filename': bga_filename,
            'bga_delay': bga_delay,
            'afp_flag': afp_flag,
            'afp_data0': afp_data0,
			'afp_data1': afp_data1,
			'afp_data2': afp_data2,
			'afp_data3': afp_data3,
			'afp_data4': afp_data4,
			'afp_data5': afp_data5,
			'afp_data6': afp_data6,
			'afp_data7': afp_data7,
			'afp_data8': afp_data8,
			'afp_data9': afp_data9,
            'unk_sect1': unk_sect1.hex(),
            'unk_sect3': unk_sect3.hex(),
        })

    return song_entries

# IIDX28 Bistrover writer
def writer_1a(outfile, data, version):
    DATA_VERSION = version
    CUR_STYLE_ENTRIES = DATA_VERSION * 1000
    MAX_ENTRIES = CUR_STYLE_ENTRIES + 1000

    # Write header
    outfile.write(b"IIDX")
    outfile.write(struct.pack("<IHHI", DATA_VERSION, len(data), MAX_ENTRIES, 0))

    # Write song index table
    exist_ids = {}
    dk = list(data.keys())
    for i in range(len(dk)):
        exist_ids[data[dk[i]]['song_id']] = i

    cur_song = 0
    for i in range(MAX_ENTRIES):
        if i in exist_ids:
            outfile.write(struct.pack("<H", cur_song))
            cur_song += 1
        elif i >= CUR_STYLE_ENTRIES:
            outfile.write(struct.pack("<H", 0x0000))
        else:
            outfile.write(struct.pack("<H", 0xffff))

    # Write song entries
    for k in sorted(exist_ids.keys()):
        song_data = data[k]

        write_string(outfile, song_data['title'], 0x40)
        write_string(outfile, song_data['title_ascii'], 0x40)
        write_string(outfile, song_data['genre'], 0x40)
        write_string(outfile, song_data['artist'], 0x40)

        outfile.write(struct.pack("<IIIII", song_data['texture_title'], song_data['texture_artist'], song_data['texture_genre'], song_data['texture_load'], song_data['texture_list']))
        outfile.write(struct.pack("<IH", song_data['font_idx'], song_data['game_version']))
        outfile.write(struct.pack("<HHH", song_data['other_folder'], song_data['bemani_folder'], song_data['splittable_diff']))

        outfile.write(struct.pack("<BBBBBBBBBB", song_data['SPB_diff'], song_data['SPN_diff'], song_data['SPH_diff'], song_data['SPA_diff'], song_data['SPL_diff'], song_data['DPB_diff'], song_data['DPN_diff'], song_data['DPH_diff'], song_data['DPA_diff'], song_data['DPL_diff']))

        outfile.write(bytes.fromhex('00000000000001000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))


        #outfile.write(song_data.get('unk_sect1', bytes.fromhex('00000000000001000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')))
        
#        outfile.write(bytes.fromhex(song_data.get('unk_sect1','00000000000001000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000300000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')))

        outfile.write(struct.pack("<II", song_data['song_id'], song_data['volume']))

        write_string(outfile, song_data['SPB_ident'], 1)
        write_string(outfile, song_data['SPN_ident'], 1)
        write_string(outfile, song_data['SPH_ident'], 1)
        write_string(outfile, song_data['SPA_ident'], 1)
        write_string(outfile, song_data['SPL_ident'], 1)
        write_string(outfile, song_data['DPB_ident'], 1)
        write_string(outfile, song_data['DPN_ident'], 1)
        write_string(outfile, song_data['DPH_ident'], 1)
        write_string(outfile, song_data['DPA_ident'], 1)
        write_string(outfile, song_data['DPL_ident'], 1)

        outfile.write(struct.pack("<H", song_data['bga_delay']))
        write_string(outfile, song_data['bga_filename'], 0x20)

        outfile.write(struct.pack("<I", song_data['afp_flag']))

        write_string(outfile, song_data['afp_data0'], 0x20)
        write_string(outfile, song_data['afp_data1'], 0x20)
        write_string(outfile, song_data['afp_data2'], 0x20)
        write_string(outfile, song_data['afp_data3'], 0x20)
        write_string(outfile, song_data['afp_data4'], 0x20)
        write_string(outfile, song_data['afp_data5'], 0x20)
        write_string(outfile, song_data['afp_data6'], 0x20)
        write_string(outfile, song_data['afp_data7'], 0x20)
        write_string(outfile, song_data['afp_data8'], 0x20)
        write_string(outfile, song_data['afp_data9'], 0x20)
        outfile.write(bytes.fromhex('00000000'))
        #outfile.write(song_data.get('unk_sect3', bytes.fromhex('00000000')))

if __name__ == "__main__":
    read_handlers = {
        0x50: reader_19,
        0x1c: reader_1a,
    }

    write_handlers = {
        0x50: writer_19,
        0x1c: writer_1a,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Input file', required=True)
    parser.add_argument('--output', help='Output file', required=True)
    parser.add_argument('--extract', help='Extraction mode', default=False, action='store_true')
    parser.add_argument('--create', help='Creation mode', default=False, action='store_true')
    parser.add_argument('--convert', help='Conversion mode', default=False, action='store_true')
    parser.add_argument('--merge', help='Merge mode', default=False, action='store_true')
    parser.add_argument('--data-version', help='Force a data version (useful for converts)', default=None, type=int)
    parser.add_argument('--legg', help='Set Leggendaria songs to game version 65535', default=False, action='store_true')
    args = parser.parse_args()

    if args.create == False and args.extract == False and args.convert == False and args.merge == False:
        print("You must specify either --extract or --create or --convert or --merge")
        exit(-1)

    if args.convert == True:
        if args.data_version == None:
            print("You must specify a target --data-version with --convert")
            exit(-1)
        elif args.data_version not in write_handlers:
            print("Don't know how to handle specified data version")
            exit(-1)

    if args.extract:
        with open(args.input, "rb") as infile:
            if infile.read(4) != b"IIDX":
                print("Invalid", args.input)
                exit(-1)

            data_ver, available_entries, total_entries = struct.unpack("<III", infile.read(12))

            song_ids = {}
            for i in range(total_entries):
                song_id = struct.unpack("<H", infile.read(2))[0]

                if song_id != 0xffff and (len(song_ids) == 0 or song_id != 0):
                    song_ids[i] = song_id

            if data_ver in read_handlers:
                output_data = read_handlers[data_ver](infile, available_entries)
                output_data = {
                    'data_ver': data_ver,
                    'data': output_data,
                }

                json.dump(output_data, open(args.output, "w", encoding="utf8"), indent=4, ensure_ascii=False)
            else:
                print("Couldn't find a handler for this data version")
                exit(-1)

    elif args.create:
        data = json.load(open(args.input, "r", encoding="utf8"))
        data_ver = data.get('data_ver', args.data_version)

        if not data_ver:
            print("Couldn't find data version")
            exit(-1)

        if data_ver in write_handlers:
            write_handlers[data_ver](open(args.output, "wb"), data['data'])
        else:
            print("Couldn't find a handler for this data version")
            exit(-1)

    elif args.convert:
        with open(args.input, "rb") as infile:
            if infile.read(4) != b"IIDX":
                print("Invalid", args.input)
                exit(-1)

            data_ver, available_entries, total_entries, unk4 = struct.unpack("<IHIH", infile.read(12))

            song_ids = {}
            for i in range(total_entries):
                song_id = struct.unpack("<H", infile.read(2))[0]

                if song_id != 0xffff and (len(song_ids) == 0 or song_id != 0):
                    song_ids[i] = song_id

            if data_ver in read_handlers:
                output_data = read_handlers[data_ver](infile, available_entries)
                write_handlers[args.data_version](open(args.output, "wb"), output_data)
            else:
                print("Couldn't find a handler for this input data version")
                exit(-1)

    elif args.merge:
        with open(args.input, "rb") as infile:
            if infile.read(4) != b"IIDX":
                print("Invalid", args.input)
                exit(-1)

            data_ver, available_entries, total_entries, unk4 = struct.unpack("<IHIH", infile.read(12))

            song_ids = {}
            for i in range(total_entries):
                song_id = struct.unpack("<H", infile.read(2))[0]

                if song_id != 0xffff and (len(song_ids) == 0 or song_id != 0):
                    song_ids[i] = song_id

            if data_ver in read_handlers:
                old_data = read_handlers[data_ver](infile, available_entries)
            else:
                print("Couldn't find a handler for this input data version")
                exit(-1)

        with open(args.output, "rb") as infile:
            if infile.read(4) != b"IIDX":
                print("Invalid", args.output)
                exit(-1)

            data_ver, available_entries, total_entries, unk4 = struct.unpack("<IHIH", infile.read(12))

            song_ids = {}
            for i in range(total_entries):
                song_id = struct.unpack("<H", infile.read(2))[0]

                if song_id != 0xffff and (len(song_ids) == 0 or song_id != 0):
                    song_ids[i] = song_id

            if data_ver in read_handlers:
                new_data = read_handlers[data_ver](infile, available_entries)
            else:
                print("Couldn't find a handler for this input data version")
                exit(-1)

        # Create list of
        exist_ids_new = {}
        for song_data in new_data:
            exist_ids_new[song_data['song_id']] = True

        for song_data in old_data:
            if song_data['song_id'] not in exist_ids_new:
                new_data.append(song_data)

        write_handlers[data_ver](open(args.output, "wb"), new_data)
