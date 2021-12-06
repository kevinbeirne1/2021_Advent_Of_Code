from pathlib import Path

def read_txt_file_contents(filename_to_read):
    """
    Read depths from txt file and return as a list
    """
    with open(Path.cwd()/filename_to_read) as f:
        contents = (f.readlines())
    return contents