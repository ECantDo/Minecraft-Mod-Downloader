import json
import math

import requests
import time
import atexit


def get_json_file_contents(file_path: str):
    return json.loads(open(file_path, 'r').read())


def get_id_from_download_url(url: str):
    return url[30:url.find("/", 30)]


def get_id_from_modrinth_url(url: str) -> str:
    if not url.startswith("https://modrinth.com/mod/"):
        return url
    url = url.strip()
    r_idx = url.rfind("mod/") + 4
    l_idx = url.find("/", r_idx)
    if l_idx != -1:
        return url[r_idx:l_idx]
    else:
        return url[r_idx:]


def get_id_from_v2_urls_file(file_path: str) -> list:
    contents = json.loads(open(file_path, 'r').read())
    return [mod["project_id"] for mod in contents]


def list_index(list: list, item: str):
    try:
        return list.index(item)
    except ValueError:
        return -1


def build_new_mod(mod_json: dict) -> dict:
    return {"slug": mod_json["slug"],
            "title": mod_json["title"],
            "type": mod_json["project_type"],
            "versions": []
            }
    pass


def build_version_json(version_id: str) -> dict or None:
    req = requests.get(f"https://api.modrinth.com/v2/version/{version_id}", timeout=5)
    if req.status_code == 404:
        return None
    req_json = req.json()

    # for mod in req_json["dependencies"]:
    #     if mod["dependency_type"] == "required" and mod["project_id"] not in mod_ids:
    #         mod_ids.append(mod["project_id"])
    return {
        "id": version_id,
        "game_versions": req_json["game_versions"],
        "loaders": req_json["loaders"],
        "filename": [fl["filename"] for fl in req_json["files"]],
        "url": [fl["url"] for fl in req_json["files"]]
    }


def add_mod(mod_id: str, json_contents: dict):
    start_time = time.time()
    request_count = 1

    ####
    req = requests.get(f"https://api.modrinth.com/v2/project/{mod_id}")
    if req.status_code == 404:
        print(f"Skipping {mod_id} because it doesn't exist")
        return
    request_contents = req.json()
    # print(request_contents)
    # if request_contents["client_side"] == "unsupported":
    #     print(f"Skipping {request_contents['title']} ({request_contents['slug']}) because it is unsupported")
    #     return

    idx = list_index(json_contents["mod_ids"], request_contents["id"])

    ####
    if idx == -1:
        mod_data = build_new_mod(request_contents)
        json_contents["mod_ids"].append(request_contents["id"])
        json_contents["mods"].append(mod_data)
    else:
        mod_data = json_contents["mods"][idx]
        # mod_data["type"] = request_contents["project_type"]

    ####
    version_ids = [v["id"] for v in mod_data["versions"]]
    new_ids = [v for v in request_contents["versions"] if v not in version_ids]

    request_count += len(new_ids)
    print(f"Mod: {request_contents['title']}")
    for idx, id in enumerate(new_ids):
        print(
            f"\rAdding {idx + 1} of {len(new_ids)} new versions ({len(request_contents["versions"])} total)\t"
            f"({math.floor((idx + 1) / len(new_ids) * 100)}%)", end="")
        if id.strip() == "":
            continue

        version_json = build_version_json(id)
        if version_json is not None:
            mod_data["versions"].append(version_json)

    print(f"\nAll {len(request_contents["versions"])} versions added")

    # Sleep time for ratelimit #
    run_time = time.time() - start_time
    request_time = time_per_request * request_count
    time.sleep(0 if run_time > request_time else request_time - run_time)  # request_time - time_since_start
    pass


ratelimit = 300  # 300 per minute; 5 per second
time_per_request = 1 / (ratelimit / 60)  # in seconds


def save_json_file():
    with open(url_file_path, 'w') as outfile:
        json.dump(contents, outfile, indent=2)


def exit_handler():
    print("Saving json file...")
    save_json_file()
    print("Done")
    print("Saving mod ids...")
    import os
    if not os.path.exists("raw_urls_CRASH_SAVE.txt"):
        open("raw_urls_CRASH_SAVE.txt", 'x').close()
    with open("raw_urls_CRASH_SAVE.txt", "w") as file:
        file.write("\n".join(mod_ids))


atexit.register(exit_handler)
url_file_path = "urls.json"
contents = get_json_file_contents(url_file_path)

if __name__ == "__main__":
    mod_ids = [get_id_from_modrinth_url(url) for url in open("raw_urls.txt", 'r').readlines()]
    # mod_ids = get_id_from_v2_urls_file("E:\\Desktop\\Extra Minecraft Versions\\fabric-loader-0.14.19-1.19.4\\urls.json")
    print(mod_ids)
    idx = 1
    while len(mod_ids) > 0:
        mod_id = mod_ids.pop(0)
        print(f"\n\nMod {idx} of {idx + len(mod_ids)}")
        add_mod(mod_id, contents)
        idx += 1

    pass
