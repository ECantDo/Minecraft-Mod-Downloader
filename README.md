
## Just a personal, 
custom mod downloader for Minecraft mods from [Modrinth](https://modrinth.com/).  It's only public so that I have access to the master urls file, so I can use this on any device without extra hassle of transferring the latest files around or an API key.  THIS BEING NOTED, It is not going to have much in the way of documentation as it is a **personal** project.

---
If you want to make your own downloader, you're going to want version 4.1 as that's the version without the web-based download of the json.  To do this download the `url_json_getter.py` and make a file called `raw_urls.txt` and paste in the modrinth URL to the mods you want to download.
Once that program has been run, all of the versions for each of your mods will have all of their respective data downloaded.  Then it's a matter of running the `v4.1.exe` input the version of choice, and all of your mods will be up to date.

#### **PLEASE NOTE**
- It does not get the mod data for the dependencies, you have to do that yourself.
- It does not check for incompatible mods or mod versions, you have to do that yourslef.
---