import time
import json
import requests

timeout_time = 4


def find_all_indexes(string: str, sub_string: str):
    indexes = []
    sub_str_len = len(sub_string)
    index = 0
    while True:
        index = string.find(sub_string, index)
        if index == -1:
            break
        indexes.append(index)
        index += sub_str_len
        pass
    return indexes
    pass


def search(query: str, version: str = None, loader_version: str = "fabric"):
    request = requests.get(f"https://api.modrinth.com/v2/search?query={query}", timeout=timeout_time).json()
    if version == "":
        version = None
    hit = request["hits"][0]
    # print(hit)
    if version not in hit['versions'] and version is not None:
        hit = None
    if loader_version not in hit['categories']:
        hit = None

    # print(f'Title: {hit["title"]} | Slug: {hit["slug"]}\nType: {hit["project_type"]} | Author: {hit["author"]}')
    # if input("Is this correct? (anything(y)/N) ").lower() != 'n':
    #     print("yes")
    #     break
    # else:
    #     hit = None

    # print(hit['project_id'])
    return hit
    pass


def get_project_data(project_id: str) -> {}:
    return requests.get(f"https://api.modrinth.com/v2/project/{project_id}").json()


def get_download_link(project_id: str, version: str, mod_loader_type: str = "Fabric"):
    # request_text = str(requests.get(f"https://modrinth.com/mod/{project_id}", timeout=timeout_time).text)
    request_text = str(
        requests.get(f'https://modrinth.com/mod/{project_id}/versions?g={version}', timeout=timeout_time).text)
    # https://modrinth.com/mod/carpet/versions?g=1.19.4
    # print(request_text)
    sub_str = f'href=\"https://cdn.modrinth.com/data/{project_id}/versions/'
    indexes = find_all_indexes(request_text, sub_str)
    # print(indexes)
    for index in indexes:
        link = request_text[index:request_text.find("</div>", index)]
        # print(link)
        if (mod_loader_type in link or mod_loader_type.lower() in link) and version in link:
            return link[6:link.find("\"", 6)]
        pass
    pass


def get_download_link2(project_id: str, version: str, mod_type):
    request = requests.get(f"https://modrinth.com/mod/{project_id}/versions?g={version}&l={mod_type}")
    status = request.status_code

    attempts = 0
    while request.status_code != 200:
        attempts += 1
        print(f"\rAHHH Status != 200 ({attempts})", end="")
        time.sleep(15)
        request = requests.get(f"https://modrinth.com/mod/{project_id}/versions?g={version}&l={mod_type}")
        status = request.status_code
        if status == 200:
            print()

    request_text = str(request.text)
    # print(request_text)
    sub_str = f'href=\"https://cdn.modrinth.com/data/{project_id}/versions/'
    # print(request_text.find(sub_str))
    # indexes = find_all_indexes(request_text, sub_str)
    index = request_text.find(sub_str) + 6
    return request_text[index:request_text.find("\"", index)]
    # print(indexes)

    pass


def read_txt(path: str) -> list:
    return [line.replace("\n", "") for line in open(path, 'r').readlines()]
    pass


def get_project_ids(version: str):
    queries = read_txt("queries.txt")
    print(f"Queries: {queries}")
    project_ids = []
    for query in queries:
        project_hit = search(query, version)
        if project_hit is None:
            continue
        # print(project_hit)
        project_ids.append(project_hit['project_id'])
        print(f"\rFound ID: {project_hit['project_id']}", end="")
        pass
    print()
    # print(f"Slugs: {slugs}")
    project_ids = [f"{project_id}\n" for (project_id) in project_ids]
    project_ids[-1] = project_ids[-1][:-1]
    open("project_id.pid", 'w').writelines(project_ids)
    pass


def get_download_urls(version: str):
    project_ids = read_txt("project_id.pid")
    # links = [get_download_link(project_id, version) for project_id in project_ids]
    download_json = []
    for idx, project_id in enumerate(project_ids):
        print(f"{idx + 1}/{len(project_ids)}")
        link = get_download_link2(project_id, version, "fabric")

        print(link)
        project_data = get_project_data(project_id)
        download_json.append({
            "download_url": link,
            "project_id": project_id,
            "name": project_data["title"],
            "type": f'{project_data["project_type"]}s'
        })
        # break
        pass
    json.dump(download_json, open("urls.json", 'w'))
    # print(project_ids)
    # print(links)
    pass


# print(get_download_link2("EsAfCjCV", "1.19.2", "fabric"))
#
# exit(0)

if __name__ == "__main__":
    get_project_ids("1.18.2")
    get_download_urls("1.18.2")
    # project_hit = search("Iris", "1.19.4")
    # print(get_download_link(project_hit, "1.19.4"))
    pass

# print(str(requests.get(f"https://modrinth.com/mod/P7dR8mSH", timeout=timeout_time).text))
