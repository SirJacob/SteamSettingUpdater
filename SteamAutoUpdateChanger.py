"""
TODO: Integrate with SteamCMD to allow for downloading of multiple Steam games at once (+ limit bandwidth and priority)?
TODO: Wish-list manager
-----
TODO: Implement config saving (maybe to a .json file)
"""
import glob
import os

import psutil
import vdf

import GeneralTools as Tools

""" SETUP """
all_steam_directories = [
    "C:\\Program Files (x86)\\Steam"  # The default Steam installation directory for most users
]


def close_steam():
    for p in psutil.process_iter():
        if p.name() == "Steam.exe":
            process_info = f"{p.name()} (PID: {p.pid})"
            Tools.log(f"{process_info} is running")

            all_steam_directories[0] = p.exe()[
                                       :p.exe().rindex('\\')]  # p.exe() points to the exe and we need the directory

            terminate_request_timeout = 10
            Tools.log(f"Asking {process_info} to exit... (request will timeout in {terminate_request_timeout} seconds)")
            p.terminate()
            gone, alive = psutil.wait_procs([p], timeout=terminate_request_timeout, callback=None)

            if len(alive) > 0:
                p.kill()
                Tools.log(f"{process_info} ended forcibly (killed)", Tools.LEVEL_WARN)
            elif len(gone) > 0:
                Tools.log(f"{process_info} closed peacefully (terminated)")
            break


def find_steam_install_dir():
    # Let's find out if this system has a custom Steam installation directory
    # TODO: Find an alternative Steam installation directory when not default w/o user input; maybe via running process?
    while not Tools.folder_exists(all_steam_directories[0]):
        all_steam_directories[0] = input("Please provide the path to your Steam installation: ")
    # Let's find out if this system has more than one Steam library setup
    # TODO: Switch to Steam\config\config.vdf -> BaseInstallFolder for non-main library?
    # Load library folder VDF into memory
    library_folders_vdf = vdf.load(open(f"{all_steam_directories[0]}\\steamapps\\libraryfolders.vdf"))

    # Add all Steam libraries we found in libraryfolders.vdf
    index = 1
    while index >= 1:
        alt_steam_library = library_folders_vdf["LibraryFolders"].get(str(index))
        if alt_steam_library is None:
            index = -1
        else:
            all_steam_directories.append(alt_steam_library)
            index += 1


""" MAIN MENU """


def return_to_main_menu():
    input(f"\nPress enter to return to the menu...")
    display_main_menu()


def display_main_menu():
    menu_options = {
        1: "AutoUpdateBehavior",
        2: "DownloadThrottle",
        9: "Quit"
    }
    user_input = 0
    while not menu_options.__contains__(user_input):
        Tools.clear_console()
        # Setup menu display
        print("Steam Setting Updater")
        for num, option in menu_options.items():
            print(f"{num}: {option}")
        user_input = input("Select a number: ")
        # Validate input
        if user_input.isdigit():
            user_input = int(user_input)
        else:
            user_input = 0

    Tools.clear_console()
    if user_input == 1:
        print(menu_options[1])
        print("0 = Always keep this game up to date\n"
              "1 = Only update this game when I launch it\n"
              "2 = High Priority - Always auto-update this game before others")

        allowed_input = [0, 1, 2]
        new_auto_update_behavior = input("Select an option: ")
        while not allowed_input.__contains__(new_auto_update_behavior):
            if new_auto_update_behavior.isdigit():
                new_auto_update_behavior = int(new_auto_update_behavior)
            else:
                new_auto_update_behavior = -1

        auto_update_behavior(new_auto_update_behavior)
    if user_input == 2:
        while True:
            Tools.clear_console()
            rate = str(input("Enter a download rate in Kbps (0=disable): "))
            if rate.isdigit():
                break
        download_throttle(int(rate))
    elif user_input == 9:
        Tools.stop_program()

    return_to_main_menu()


""" AutoUpdateBehavior """


def auto_update_behavior(new_auto_update_behavior):
    close_steam()

    # Variables for keeping track of how many acf files were processed
    num_updated_acf_files = 0
    num_total_acf_files = 0

    # Define which AutoUpdateBehavior should be searched for and overwritten
    old_auto_update_behavior = [0, 1, 2]
    old_auto_update_behavior.remove(new_auto_update_behavior)

    # TODO: Cleanup code using new vdf reader/writer
    for steamapp_directory in all_steam_directories:
        os.chdir(steamapp_directory + "\\steamapps")
        for appmanifest_path in glob.glob("appmanifest_*.acf"):
            num_total_acf_files += 1

            appmanifest = open(appmanifest_path, "r+")
            appmanifest_contents = appmanifest.read()

            if appmanifest_contents.__contains__(f"\"AutoUpdateBehavior\"		\"{old_auto_update_behavior[0]}\"") or \
                    appmanifest_contents.__contains__(
                        f"\"AutoUpdateBehavior\"		\"{old_auto_update_behavior[1]}\""):
                appmanifest_contents = appmanifest_contents.replace(
                    f"\"AutoUpdateBehavior\"		\"{old_auto_update_behavior[0]}\"",
                    f"\"AutoUpdateBehavior\"		\"{new_auto_update_behavior}\"")
                appmanifest_contents = appmanifest_contents.replace(
                    f"\"AutoUpdateBehavior\"		\"{old_auto_update_behavior[1]}\"",
                    f"\"AutoUpdateBehavior\"		\"{new_auto_update_behavior}\"")

                appmanifest.seek(0)
                appmanifest.write(appmanifest_contents)
                appmanifest.truncate()
                num_updated_acf_files += 1
            appmanifest.close()

    if num_updated_acf_files == 0:
        print(f"All {num_total_acf_files} games already had the requested AutoUpdateBehavior.")
    elif num_updated_acf_files == num_total_acf_files:
        print(f"All {num_total_acf_files} games were updated to the requested AutoUpdateBehavior.")
    else:
        print(f"{num_updated_acf_files}/{num_total_acf_files} games were updated to the requested AutoUpdateBehavior.\n"
              f"(some already had the requested AutoUpdateBehavior.)")
    print(f"{len(all_steam_directories)} Steam library folder(s) were searched.")


""" DownloadThrottle """


# "DownloadThrottleKbps"		"0"
def download_throttle(rate):
    close_steam()

    path = f"{all_steam_directories[0]}\\config\\config.vdf"
    config_vdf = vdf.load(open(path), mapper=vdf.VDFDict)  # Load VDF file
    old_value = config_vdf['InstallConfigStore']['Software']['Valve']['steam']['DownloadThrottleKbps']

    if int(old_value) == rate:
        print(f"Your download rate was not changed because it was already set to"
              f" {'unlimited' if old_value == '0' else f'{old_value} Kbps'}.")
        return

    # Delete old value and add new value
    del config_vdf['InstallConfigStore']['Software']['Valve']['steam']['DownloadThrottleKbps']
    config_vdf['InstallConfigStore']['Software']['Valve']['steam'].update({'DownloadThrottleKbps': rate})
    # Backup and then output to file
    Tools.backup_file(path)
    vdf.dump(config_vdf, open(path, "w"), pretty=True)

    print(f"Your download rate was change from {'unlimited' if old_value == '0' else f'{old_value} Kbps'} to"
          f" {'unlimited' if rate == 0 else f'{rate} Kbps'}.")


""" INIT """


def __init__():
    find_steam_install_dir()
    display_main_menu()


__init__()
