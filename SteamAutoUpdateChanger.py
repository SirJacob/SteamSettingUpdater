import glob
import os

all_steamapps_directories = [
    "C:\\Program Files (x86)\\Steam\\steamapps"
]

"""
AutoUpdateBehavior Settings:
0 = Always keep this game up to date
1 = Only update this game when I launch it
2 = High Priority - Always auto-update this game before others
"""

num_updated_acf_files = 0
num_total_acf_files = 0

for steamapp_directory in all_steamapps_directories:
    os.chdir(steamapp_directory)
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
      f" in {len(all_steamapps_directories)} directories.")
