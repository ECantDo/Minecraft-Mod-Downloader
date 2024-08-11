import requests

if __name__ == '__main__':
    print(requests.get("https://api.modrinth.com/v2/project/worldedit").json())