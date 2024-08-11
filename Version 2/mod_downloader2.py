import os, sys, json, requests

colors = {}
url_dic = {}
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
    try:
        with open(file_path, 'r') as file:
            url_dict_lines = file.readlines()
            pass

        url_dict_lines = ''.join([(line.replace("\n", "").strip()) for line in url_dict_lines])
        # print(url_dict_lines)
        if url_dict_lines[-2] == ",":
            url_dict_lines = url_dict_lines[:-2] + ']'
        return json.loads(url_dict_lines)
    except FileNotFoundError:
        print(f"{colors['red']}FILE CONTAINING URL'S Not Found{colors['reset']}")
        return None
    pass


def read_json_file(file_path: str) -> []:
    try:
        return json.loads(open(file_path, 'r').read())
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


def download(urls: [{}]):
    global url_dic
    try:
        for url_dic in urls:
            # print(url_dic)
            if not download_types.__contains__(url_dic["type"]):
                continue

            file_name = url_dic['download_url'][last_index_of(url_dic['download_url'], "/") + 1:]
            file_download_path = download_path + url_dic["type"] + "\\" + file_name

            if os.path.exists(file_download_path):
                print(f"{colors['yellow']}Skipping{colors['reset']} {file_name}")
                continue

            try:
                print(f"{colors['blue']}getting response for {colors['reset']}{url_dic['download_url']}")
                response = requests.get(url=url_dic['download_url'], timeout=5)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"failed to get a response")
                print(e)
                continue
            if response.status_code == 200:
                name = str(url_dic['download_url'])
                name = name[name.find("/", name.find("versions/") + len("versions/")):]

                print(f"downloading: '{name}' from: {url_dic['download_url']}")
                with open(file_download_path, 'wb') as file:
                    file.write(response.content)
    except Exception as e:
        print(f"{colors['red']}ERROR IN: \n{url_dic}\n\n{colors['reset']}{e}")
    pass


if __name__ == "__main__":
    url_file_path = "urls_DEMO.json"

    create_globals()
    create_directories()
    file_contents = get_file_contents(url_file_path)

    if file_contents is not None:
        print(f"Getting Urls from directory: {os.path.abspath(url_file_path)}")
        print(f"URLS to load:\n{file_contents}\n\n\n")
        download(file_contents)
    else:
        print(f"{colors['red']}NO URL'S FOUND TO DOWNLOAD")

    print(f"{colors['green']}FINISHED")
    print(f"Press Enter to Continue{colors['reset']}")
    input()
    pass
