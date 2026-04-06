import os
import time
from adbutils import adb

timestr = time.strftime("%Y%m%d-%H%M%S")

def LogCatDump(filename,serial):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    file = filename +timestr+".txt"
    cmd = "adb -s %s shell logcat -d > " %serial +file
    os.popen(cmd)
    return  file

def LogCatClear(serial):
    os.popen("adb -s %s shell logcat -c" %serial)
