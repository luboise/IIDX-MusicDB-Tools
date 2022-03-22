import os


cwd = "C:\\LDJ-003-2021111700\\contents\\data_mods\\omni\\sound"
for (dirpath, dirnames, filenames) in os.walk(cwd):
    for dirname in dirnames:
        if dirname.startswith("8"):
            new_id = str(int(dirname) - 50500)
            inside_dir = os.path.join(dirpath, dirname)
            for (x, y, infilenames) in os.walk(inside_dir):
                for infile in infilenames:
                    if not infile.startswith("8"):
                        old_path = os.path.join(inside_dir, infile)
                        new_path = os.path.join(inside_dir, new_id + infile[5:])
                        os.rename(old_path, new_path)
    
            old_path = inside_dir
            new_path = os.path.join(dirpath, new_id)
            os.rename(old_path, new_path)

            