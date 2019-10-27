"""
Valve Data File Reader
Resource: https://developer.valvesoftware.com/wiki/KeyValues#File_Format
"""
import GeneralTools as Tools


class VDFReader:
    def __init__(self, path):
        self.path = path  # store instance VDF path
        data = Tools.read_file(path).strip()  # Clear trailing newline/white space
        data = data.splitlines()  # transform into list
        self.top_level_parent_key = data[0].strip('"')  # remove unnecessary quotes
        data = data[2:-1]  # remove unnecessary '{' and '}'
        # iterate through each line, adding the key value data to memory
        self.kv_dict = {}
        for line in data:
            line = line[2:-1].replace('"\t\t"', '$split').split('$split')
            self.kv_dict[line[0]] = line[1]

    def get(self, key):
        key = str(key)  # All VDF keys will be strings
        return self.kv_dict.get(key, None)

    def set(self, key, value):
        if self.kv_dict.get(key, None) is None:
            # TODO: Tools.log(self.__class__.__name__)
            pass

    # TODO: Implement write_vdf
    def write_vdf(self):
        pass

    def __str__(self):
        output = ""
        for key, value in self.kv_dict.items():
            output += f"\t{key}: {value}\n"
        return f"VDFReader for {self.top_level_parent_key} @ {self.path}" \
               f"\n{output}"
