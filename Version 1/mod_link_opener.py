import os, sys, json, requests
import webbrowser

colors = {}
download_types = []
download_path = ""


def create_globals():
    global download_types
    download_types = ["mods", "resourcepacks", "shaderpacks"]

    global download_path
    exe_location = sys.executable
    file_location = exe_location[:1 + last_index_of(exe_location, "\\")]
    if exe_location.endswith("python.exe"):
        file_location += "testFolder\\"
    download_path = file_location
    print(download_path)

    global colors
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


def get_file_contents(file_path: str) -> []:
    with open(file_path, 'r') as file:
        url_dict_lines = file.readlines()
        pass

    url_dict_lines = ''.join([(line.replace("\n", "").strip()) for line in url_dict_lines])
    # print(url_dict_lines)
    if url_dict_lines[-2] == ",":
        url_dict_lines = url_dict_lines[:-2] + ']'
    return json.loads(url_dict_lines)
    pass


def opening(urls: [{}]):
    for url_dic in urls:
        # print(url_dic)
        if not download_types.__contains__(url_dic["type"]):
            continue
        webbrowser.open(url_dic['site_url'])

    pass


if __name__ == "__main__":
    create_globals()
    file_contents = get_file_contents("urls2.txt")
    print(f"URLS to load:\n{file_contents}")

    opening(file_contents)

    print(f"{colors['green']}FINISHED")
    print(f"Press Enter to Continue{colors['reset']}")
    input()
    pass
