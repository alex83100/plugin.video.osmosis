# Copyright (C) 2016 stereodruid(J.G.) Mail: stereodruid@gmail.com
#
#
# This file is part of OSMOSIS
#
# OSMOSIS is free software: you can redistribute it. 
# You can modify it for private use only.
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OSMOSIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


# -*- coding: utf-8 -*-
import os
import time
import sys
from modules import create
from modules import guiTools
from modules import kodiDB

import utils
import xbmc, xbmcgui, xbmcaddon, xbmcvfs

# Debug option pydevd:
if False:
    import pydevd
    pydevd.settrace(stdoutToServer=True, stderrToServer=True)

global thelist
thelist = None

ADDON_ID = 'plugin.video.osmosis'
REAL_SETTINGS = xbmcaddon.Addon(id=ADDON_ID)
ADDON_ID = REAL_SETTINGS.getAddonInfo('id')
ADDON_NAME = REAL_SETTINGS.getAddonInfo('name').decode('utf-8')
ADDON_PATH = REAL_SETTINGS.getAddonInfo('path')
ADDON_SETTINGS = REAL_SETTINGS.getAddonInfo('profile')
ADDON_VERSION = REAL_SETTINGS.getAddonInfo('version')
# PC Settings Info
MediaList_LOC = xbmc.translatePath(os.path.join(ADDON_SETTINGS, 'MediaList.xml'))
STRM_LOC = REAL_SETTINGS.getSetting('STRM_LOC')
Path_Type = REAL_SETTINGS.getSetting('Path_Type')
Clear_Strms = REAL_SETTINGS.getSetting('Clear_Strms') == 'true'
Automatic_Update_Time = REAL_SETTINGS.getSetting('Automatic_Update_Time') 
Updat_at_startup = REAL_SETTINGS.getSetting('Updat_at_startup')
Automatic_Update_Delay = REAL_SETTINGS.getSetting('Automatic_Update_Delay')
Automatic_Update_Run = REAL_SETTINGS.getSetting('Automatic_Update_Run')
represent = os.path.join(ADDON_PATH, 'icon.png')
toseconds = 0.0
itime = 900000000000000  # in miliseconds  

def readMediaList(purge=False):
        try:
            if xbmcvfs.exists(MediaList_LOC):
                fle = open(MediaList_LOC, "r")
                thelist = fle.readlines()
                fle.close()
                return thelist
        except:
            pass
if xbmcvfs.exists(MediaList_LOC):           
    thelist = readMediaList()

    
def strm_update():
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (ADDON_NAME, "Updating!" , itime, represent))
    try:
        #kodiDB.musicDatabase()
        if xbmcvfs.exists(MediaList_LOC) and len(thelist) > 0:
            listLen = len(thelist)
            for i in range(len(thelist)):                     
                    cType , name, url = ((thelist[i]).strip().split('|', 2))
                    # time.sleep(2) # delays for 2 seconds just to make sure Hodor can read the message 
#                        pDialog.update(j, ADDON_NAME + " Update: " + name.decode('utf-8')) 
                    try:
                        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (name, " Items left: " + str(listLen) , itime, represent))
                        create.fillPluginItems(url, strm=True, strm_name=name, strm_type=cType)
                        listLen -= 1
                    except:  #
                        pass
                        
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (ADDON_NAME, "Next update in: " + Automatic_Update_Time + "h" , 5000, represent))
    except IOError as (errno, strerror):
        print ("I/O error({0}): {1}").format(errno, strerror)
    except ValueError:
        print ("No valid integer in line.")
    except:
        guiTools.infoDialog("Unexpected error: " + str(sys.exc_info()[1])+ (". Se your Kodi.log!"))
        utils.addon_log(("Unexpected error: ") + str(sys.exc_info()[1]))
        print ("Unexpected error:"), sys.exc_info()[1]
        pass 