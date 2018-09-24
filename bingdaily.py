#!/usr/local/bin/python3
"""
For OSX only run python3 bingdaily.py install to install
"""

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"s
end tell
END"""

from pathlib import Path
from time import sleep
import sys, json, os, requests, subprocess, schedule
from multiprocessing import Pool
HOME = str(Path.home())
apiURL = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n='
baseURL = "http://www.bing.com/"
outputPath = HOME + "/Pictures/BingDailyWallpaper/"
installLocation =  "/usr/local/bin/bingdaily"

launchPlist = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
   <key>Label</key>
   <string>com.user.bingdaily</string>
   <key>ProgramArguments</key>
   <array><string>/usr/local/bin/bingdaily</string></array>
   <key>RunAtLoad</key>
   <true/>
</dict>
</plist>"""
plistLocation = HOME + "/Library/LaunchAgents/com.user.bingdaily.plist"

def downloadImage(data: (str, str)) -> None:
    name = data[1]
    r = requests.get(data[0], stream=True)
    if r.status_code == 200 and not os.path.exists(name):
        with open(name, 'wb') as f:
            for chunk in r:
                f.write(chunk)
        print("Downloaded photo " + name)

if __name__ == "__main__":
    if "install" in sys.argv:
        if sys.argv[0] != installLocation:
            scriptLocation = sys.argv[0]
            subprocess.call(["chmod", "+x", scriptLocation])
            subprocess.call(["cp", scriptLocation, installLocation])
            os.makedirs(os.path.dirname(plistLocation), exist_ok=True)
            with open(plistLocation, "w") as f:
                f.write(launchPlist) 
            subprocess.call(["launchctl", "load",  plistLocation])
            if scriptLocation != installLocation:
                #subprocess.call(["rm", scriptLocation])
                pass
            print("Installed bing daily!\nRun (bingdaily uninstall) to uninstall.")
        else:
            print("bingdaily installed already try running (bingdaily update) to update.")
    elif "uninstall" in sys.argv:
        if os.path.exists(installLocation):
            subprocess.call(["rm", installLocation])
            subprocess.call(["rm", plistLocation])
            subprocess.call(["launchctl", "remove", "com.user.bingdaily"])
            print("Uninstalled bing daily!\nDownload bingdaily and run (python3 bingdaily.py install) to reinstall.")
        else:
            print("bingdaily is not installed.")
    elif "update" in sys.argv:
        #curl new script and install
        pass
    elif sys.argv[0] == installLocation:
        def run():
            try:
                images = json.loads(requests.get(apiURL+ '1').text)["images"]
            except KeyError:
                print("Request failed.")
            if not os.path.isdir(outputPath):
                os.mkdir(outputPath)
            files = list(zip([baseURL + i["url"] for i in images], [outputPath + i["url"].split("/")[-1] for i in images]))
            p = Pool(8)
            p.map(downloadImage,  files)
            wallpaper = files[0][1]
            if os.path.exists(wallpaper):
                subprocess.Popen(SCRIPT%(wallpaper), shell=True)
                print('Wallpaper set to ' + wallpaper.split("/")[-1])
        run()
        schedule.every(24).hour.do(run)
        while True:
            schedule.run_pending()
            sleep(60*60)
    else:
        print("Please install bingdaily by running (python3 bingdaily.py install)")
        

