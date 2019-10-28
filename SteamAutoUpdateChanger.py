"""
TODO: Implement checking to see if Steam is open.
TODO: If Steam is open, prompt to close automatically.
TODO: Menu system

AutoUpdateBehavior Settings:
0 = Always keep this game up to date
1 = Only update this game when I launch it
2 = High Priority - Always auto-update this game before others
"""
import glob
import os
import GeneralTools as Tools
import VDFReader

all_steam_directories = [
    "C:\\Program Files (x86)\\Steam"  # The default Steam installation directory
]

# Let's find out if this system has a custom Steam installation directory
# TODO: Find an alternative Steam installation directory when not default w/o user input
while not Tools.folder_exists(all_steam_directories[0]):
    all_steam_directories[0] = input("Please provide the path to your Steam installation: ")
# Let's find out if this system has more than one Steam library setup
# Load library folder VDF into memory
library_folders_vdf = VDFReader.VDFReader(f"{all_steam_directories[0]}\\steamapps\\libraryfolders.vdf")

# Add all Steam libraries we found in libraryfolders.vdf
index = 1
while index >= 1:
    alt_steam_library = library_folders_vdf.get(index)
    if alt_steam_library is None:
        index = -1
    else:
        all_steam_directories.append(alt_steam_library)
        index += 1

# Variables for keeping track of how many acf files were processed
num_updated_acf_files = 0
num_total_acf_files = 0

# TODO: Cleanup
for steamapp_directory in all_steam_directories:
    os.chdir(steamapp_directory + "\\steamapps")
    for appmanifest_path in glob.glob("appmanifest_*.acf"):
        num_total_acf_files += 1

        appmanifest = open(appmanifest_path, "r+")
        appmanifest_contents = appmanifest.read()
        if appmanifest_contents.__contains__('"AutoUpdateBehavior"		"0"'):
            appmanifest_contents = appmanifest_contents.replace('"AutoUpdateBehavior"		"0"',
                                                                '"AutoUpdateBehavior"		"1"')
            appmanifest.seek(0)
            appmanifest.write(appmanifest_contents)
            appmanifest.truncate()
            num_updated_acf_files += 1
        appmanifest.close()

print("AutoUpdateBehavior from 0 to 1")
print("------------------------------")
print(f"{num_updated_acf_files}/{num_total_acf_files} ACF files updated"
      f" in {len(all_steam_directories)} directories.")
