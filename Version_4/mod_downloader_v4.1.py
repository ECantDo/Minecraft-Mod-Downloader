import json
import os
import sys
import traceback

import requests

curseforge_mods = [
    "https://www.curseforge.com/minecraft/mc-mods/item-scroller",
    "https://www.curseforge.com/minecraft/mc-mods/tweakeroo",
    "https://www.curseforge.com/minecraft/mc-mods/minihud"
]

colors = {"reset": "\033[0m",
          'black': "\033[30m",
          'red': "\033[31m",
          'green': "\033[32m",
          'yellow': "\033[33m",
          'blue': "\033[34m",
          'magenta': "\033[35m",
          'cyan': "\033[36m",
          'white': "\033[37m",
          }
download_types = []
download_path = ""

mods_file_contents = []


def create_globals():
    global download_types
    download_types = ["mods", "resourcepacks", "shaderpacks"]

    global download_path
    exe_location = sys.executable
    file_location = exe_location[:1 + last_index_of(exe_location, "\\")]
    if exe_location.endswith("python.exe"):
        file_location += "testFolder\\"
    download_path = file_location
    print(f"{download_path = }")

    pass


def last_index_of(string: str, substring: str) -> int:
    index_of = string.find(substring, 0)
    test_index = index_of
    while test_index != -1:
        test_index = string.find(substring, index_of + 1)
        if test_index != -1:
            index_of = test_index
    return index_of
    pass


def get_urls_content(file_path: str) -> dict | None:
    try:
        with open(file_path, 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        print(f"{colors['red']}FILE CONTAINING URL'S Not Found{colors['reset']}")
        return None
    pass


def create_directories():
    for download_type in download_types:
        download_type += "\\"
        if not os.path.exists(download_path + download_type):
            os.makedirs(download_path + download_type)
            print(f"{colors['green']}Made Directory '{download_type[:-1]}'{colors['reset']}")


def download(mod_data: dict, version: str = "1.19.4", loader: str = "fabric"):
    # FIND MOD VERSION
    mod_found = False
    mod_version = None
    for mod in mod_data["versions"][::-1]:  # Reverse the list so the latest version is first
        if loader not in mod["loaders"]:
            continue
        if version not in mod["game_versions"]:
            continue
        mod_found = True
        mod_version = mod
        break

    if not mod_found:
        print(f"{colors['red']}Mod Not Found{colors['reset']}")
        return

    # CHECK IF THAT VERSION IS ALREADY DOWNLOADED
    if mod_version["filename"][0] in mods_file_contents:
        print(f"{colors['yellow']}Skipping, file already exists: {colors['reset']} {mod_version['filename'][0]}")
        return
    # CHECK IF A PREVIOUS VERSION IS ALREADY DOWNLOADED
    for mod in mod_data["versions"]:
        if mod["filename"][0] in mods_file_contents:
            print(f"{colors['red']}REMOVING previous version of mod {colors['reset']} {mod_version['filename'][0]} "
                  f"{colors['green']}({mod['filename'][0]})")
            # print(download_path + mod["type"] + "s\\" + mod["filename"][0])
            os.remove(download_path + mod_data["type"] + "s\\" + mod["filename"][0])
            print(f"REMOVED mod{colors['reset']}")
            break
    # DOWNLOAD THE MOD
    file_name = mod_version["filename"][0]
    url = mod_version["url"][0]
    file_download_path = download_path + mod_data["type"] + "s\\" + file_name
    try:
        print(f"{colors['blue']}getting response for {colors['reset']}{url}")
        response = requests.get(url=url, timeout=5)
        response.raise_for_status()

        if response.status_code == 200:
            print(f"{colors['green']}downloading: '{mod_data['title']}'")
            with open(file_download_path, 'wb') as file:
                file.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"{colors['red']}failed to get a response\n{e}")
    print(colors["reset"], end="")
    pass


def download_deprecated(mod_json: dict, version: str = "1.19.4", loader: str = "fabric"):
    mod_found = False
    for mod in mod_json["versions"][::-1]:
        if loader not in mod["loaders"]:
            continue
        if version not in mod["game_versions"]:
            continue
        mod_found = True

        print(f"{colors['green']}Downloading '{mod_json['title']}' for {loader} version {version}{colors['reset']}")

        file_name = mod["filename"][0]
        url = mod["url"][0]
        file_download_path = download_path + mod_json["type"] + "s\\" + file_name

        ####
        if os.path.exists(file_download_path):
            print(f"{colors['yellow']}Skipping, file already exists: {colors['reset']} {file_name}")
            break

        try:
            print(f"{colors['blue']}getting response for {colors['reset']}{url}")
            response = requests.get(url=url, timeout=5)
            response.raise_for_status()

            if response.status_code == 200:
                print(f"{colors['green']}downloading: '{mod_json['title']}'")
                with open(file_download_path, 'wb') as file:
                    file.write(response.content)
        except requests.exceptions.RequestException as e:
            print(f"{colors['red']}failed to get a response\n{e}")
        print(colors["reset"], end="")
        break

    if not mod_found:
        print(f"{colors['red']}Mod {mod_json['title']} Not Found for {loader} for version {version}{colors['reset']}")
        return

    pass


def main():
    print(f"{colors["yellow"]}", end="")
    url_file_path = "urls.json"
    create_globals()
    create_directories()
    file_contents = get_urls_content(url_file_path)
    working_path = os.path.abspath(os.path.curdir)

    global mods_file_contents
    mods_file_contents = os.listdir(download_path + "mods")
    print(f"{mods_file_contents = }")

    print(f"{colors['reset']}", end="")
    version = input("Version of Minecraft to download for (default: 1.19.4): ").strip()
    mod_loader = input("Loader to download (default: fabric): ").strip()
    if version == "":
        version = "1.19.4"
    if mod_loader == "":
        mod_loader = "fabric"

    confirm = input(f"Confirm Download for Version {version} and Loader {mod_loader}? (Y/n): ").strip()

    if confirm.lower() == "n":
        exit(0)

    if file_contents is not None:
        print(f"Getting Urls from directory: {os.path.abspath(url_file_path)}")
        print(f"{colors["reset"]}")
        # print(f"URLS to load:\n{file_contents}\n\n\n")
        for mod in file_contents["mods"]:
            download(mod, version, mod_loader)
            print("\n\n")
    else:
        print(f"{colors['red']}NO URL'S FOUND TO DOWNLOAD IN {working_path}\\")
        print(f"\nPlease make sure '{url_file_path}' exists in '{working_path}\\' and try again\n")

    print(f"{colors['green']}FINISHED")
    # print(f"Press Enter to Continue{colors['reset']}")

    if os.path.exists("C:/Users/ECanDo"):
        import webbrowser

        for url in curseforge_mods:
            webbrowser.open(url)
        pass
    input(f"Press Enter to Continue {colors['reset']}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(f"{colors['red']}An Error has occurred.{colors['reset']}")
        print(traceback.format_exc())
        input("Press Enter to Continue")
    pass
