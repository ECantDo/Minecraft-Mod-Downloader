import sys, os, datetime


def last_index_of(string: str, substring: str) -> int:
    index_of = string.find(substring, 0)
    test_index = index_of
    while test_index != -1:
        test_index = string.find(substring, index_of + 1)
        if test_index != -1:
            index_of = test_index
    return index_of


exe_location = sys.executable
print(exe_location)
exe_path = exe_location[:1 + last_index_of(exe_location, "\\")]
if exe_location.endswith("python.exe"):
    exe_path += "testFolder\\"

configs = [
    {"file name": "ComplementaryShaders_v4.7.1.zip.txt",
     "file path": "shaderpacks\\",
     "content": f"""#Writen in by ECanDo's Config Writer at {datetime.datetime.now()}
#Settings Created: --Wed Oct 11 12:05:01 MDT 2023--
MOON_PHASE_LIGHTING=true
CLOUD_HEIGHT=50.0
STAR_BRIGHTNESS=2.00
LIGHT_NI=1.05
AMBIENT_NI=0.15
LIGHT_MI=0.80
LIGHT_NG=108
BLOCKLIGHT_FLICKER=true
CLOUD_BRIGHTNESS=0.25
LIGHT_DI=1.00
COLORED_LIGHT_DEFINE=true
LIGHT_NR=108
LIGHT_EI=0.95
NIGHT_BRIGHTNESS=0.12
DYNAMIC_LIGHT_DISTANCE=8.0
NIGHT_LIGHTING_PARTIAL_MOON=0.55
CLOUD_AMOUNT=14.0
MIN_LIGHT=0
STAR_AMOUNT=2
BLOOM_STRENGTH=0.15
NIGHT_LIGHTING_NEW_MOON=0.05
CLOUD_OPACITY=0.1
""",
     "update": False  # Overwrites what was there
     },
    {"file name": "config.json",
     "file path": "config\\WaterPlayer\\",
     "content": '{"APPLE_MUSIC":{"MEDIA_API_TOKEN":"","COUNTRY_CODE":"us"},"ENABLE_CHANGE_TITLE":false,"SPOTIFY":'
                '{"CLIENT_SECRET":"","CLIENT_ID":"","COUNTRY_CODE":"us"},"YANDEX_MUSIC_TOKEN":"",'
                '"CURRENT_MUSIC_VOLUME":7,"ENABLE_OVERLAY":false,"SELECT_MUSIC_VOLUME":1,"ENABLE_NOTICE":false,'
                '"LAST_REQUEST_MUSIC":"https://www.youtube.com/watch?v=SOktcEUEnS0","DEEZER_DECRYPTION_KEY":"",'
                '"FLOWERY_TTS_VOICE":"Alena"}',
     "update": False  # Overwrites what was there
     },
    {"file name": "options.txt",
     "file path": "",
     "content": """autoJump:false
renderDistance:5
guiScale:3
resourcePacks:["vanilla","fabric","continuity:default","continuity:glass_pane_culling_fix","filefile/ECanDo%27s%20Just%20Connected%20%280.2%29%201.19.4.zip","file/From-The-Fog-1.20-v1.9.2-Data-Resource-Pack.zip.zip"]
narrator:0
tutorialStep:none
key_waterplayer.key.load:key.keyboard.i
key_waterplayer.key.pause:key.keyboard.o
key_waterplayer.key.skip:key.keyboard.grave.accent
key_waterplayer.key.reset:key.keyboard.unknown
key_waterplayer.key.shuffle:key.keyboard.unknown
key_waterplayer.key.repeating:key.keyboard.unknown
key_waterplayer.key.volume.up:key.keyboard.right
key_waterplayer.key.volume.down:key.keyboard.left
key_iris.keybind.shaderPackSelection:key.keyboard.left.bracket
soundCategory_music:0.0
""",
     "update": True,  # Keeps data, just replaces the lines with the content
     "seperator": ":"
     },
    {"file name": "betterdays-common.toml",
     "file path": "config\\",
     "content": """\tenableSleepFeature = false
\tnightSpeed = 0.8
\tsleepSpeedMax = 0.0
\tsleepSpeedMin = 0.0
\tsleepSpeedAll = 0.0
\tsleepSpeedCurve = 0.0
\tclearWeatherOnWake = false""",
     "update": True,
     "seperator": "="
     }

]

print(f"DIRECTORY: {exe_path}")
for config_data in configs:
    print(f"Starting for {config_data['file name']}")
    file_location = exe_path + config_data["file path"]
    if not os.path.exists(file_location):
        os.makedirs(file_location)
        print(f"Made Directory {file_location}")
    pass

    file_location += config_data["file name"]
    if not config_data["update"]:
        with open(file_location, 'w') as file:
            file.write(config_data["content"])
        print("Wrote Data")
    else:
        if not os.path.exists(file_location):
            print("\033[91m File does not exist, skipping - run Minecraft to create \033[0m")
            continue


        with open(file_location, 'r') as file:
            config_lines = file.readlines()
            content_lines = config_data["content"].splitlines()

            implemented_lines = []
            for i, config_line in enumerate(config_lines):
                try:
                    config_name = config_line[:config_line.index(config_data["seperator"])]

                except ValueError:
                    continue

                for content_line in content_lines:
                    if content_line.startswith(config_name):
                        # print(content_line)
                        break
                    content_line = None
                    pass

                if content_line is not None:
                    config_lines[i] = content_line + "\n"
                    implemented_lines.append(content_line)

            for content_line in content_lines:
                if not (content_line in implemented_lines):
                    config_lines.append(content_line + "\n")

            with open(file_location, 'w') as file_:
                file_.writelines(config_lines)
            print(f"Updated {config_data['file name']}")

print("Press Enter to Continue")
input()
