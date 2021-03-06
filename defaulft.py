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
import os, sys
import urllib
import time

import SimpleDownloader as downloader 
from modules import create
from modules import dialoge
from modules import fileSys
from modules import guiTools
from modules import urlUtils
from modules import updateAll

import utils
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs
import service
# Debug option pydevd:
if True:
    import pydevd 
    pydevd.settrace(stdoutToServer=True, stderrToServer=True)

reload(sys)
sys.setdefaultencoding("utf-8")

#from modules import createNFO
addnon_id = 'plugin.video.osmosis'
addon = xbmcaddon.Addon(addnon_id)#
addon_version = addon.getAddonInfo('version')
ADDON_NAME = addon.getAddonInfo('name')
REAL_SETTINGS = xbmcaddon.Addon(id=addnon_id)# 
ADDON_SETTINGS = REAL_SETTINGS.getAddonInfo('profile')
MediaList_LOC = xbmc.translatePath(os.path.join(ADDON_SETTINGS,'MediaList.xml'))#
STRM_LOC = xbmc.translatePath(os.path.join(ADDON_SETTINGS,'STRM_LOC'))#
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))#
home = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))#
favorites = os.path.join(profile, 'favorites')
history = os.path.join(profile, 'history')
dialog = xbmcgui.Dialog()#
icon = os.path.join(home, 'icon.png')
iconRemove = os.path.join(home, 'iconRemove.png')
FANART = os.path.join(home, 'fanart.jpg')
source_file = os.path.join(home, 'source_file')
functions_dir = profile
downloader = downloader.SimpleDownloader()#
debug = addon.getSetting('debug')

if os.path.exists(favorites) == True:
    FAV = open(favorites).read()
else: FAV = []
if os.path.exists(favorites) == True:
    FAV = open(favorites).read()
else: FAV = []

DIRS = []
STRM_LOC = xbmc.translatePath(addon.getSetting('STRM_LOC'))

if __name__ == "__main__":
    try:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    except:
        pass
    try:
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
    except:
        pass
    try:
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    except:
        pass
    try:
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
    except:
        pass
    try:
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
    except:
        pass
    
    params = utils.get_params()
    name = None
    guiElem = None
    del_item = None
    url = None
    mode = None
    playlist = None
    iconimage = None
    fanart = FANART
    playlist = None
    fav_mode = None
    regexs = None
    album = None
    artist = None
    titl = None
    cType = None
   
#     try:
#         markName = urllib.unquote_plus(params["url"]).decode('utf-8').split('|')[1]
#     except:
#         pass
    try:
        url = urllib.unquote_plus(params["url"]).decode('utf-8')
    except:
        try:
            url = urlUtils.getURL(sys.argv[2])
        except:
            pass
        pass
    try:
        name = urllib.unquote_plus(params["name"])
    except:
        name = None
    try:
        iconimage = urllib.unquote_plus(params["iconimage"])
    except:
        pass
    try:
        fanart = urllib.unquote_plus(params["fanart"])
    except:
        pass
    try:
        mode = int(params["mode"])
    except:
        pass
    try:
        playlist = eval(urllib.unquote_plus(params["playlist"]).replace('||', ','))
    except:
        pass
    try:
        fav_mode = int(params["fav_mode"])
    except:
        pass
    try:
        regexs = params["regexs"]
    except:
        pass
    
    utils.addon_log("Mode: " + str(mode))
 
    if not url is None:
        utils.addon_log("URL: " + str(url))
        utils.addon_log("Name: " + str(name))
    #createNFO.setNamePath(STRM_LOC + "\\TV-Shows(de)", 'The Walking Dead', STRM_LOC) 
    if mode == None:
        utils.addon_log("getSources")
        guiTools.getSources()
        try:
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        except:
            pass

        if not fileSys.writeTutList("select:PluginType"):
            tutWin = ["Adding content to your library",
                      "Welcome, this is your first time using OSMOSIS. Here, you can select the content type you want to add: ",
                      "Video Plugins: Select to add Movies,TV-Shows, YouTube Videos ",
                      "Music Plugins: Select to add Music"]             
            dialoge.PopupWindow(tutWin)
    elif mode == 1:   
        create.fillPlugins(url)
        if not fileSys.writeTutList("select:Addon"):
            tutWin = ["Adding content to your library",
                      "Here, you can select the Add-on: ",
                        "The selected Add-on should provide Video/Music content in the right structure ",
                    "Take a look at ++ Naming video files/TV shows ++ http://kodi.wiki/view/naming_video_files/TV_shows" ]               
            dialoge.PopupWindow(tutWin)
        try:
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        except:
            pass
    elif mode == 2:
        create.fillPluginItems(url)
        try:
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        except:
            pass 
    elif mode == 4:
        create.removeItemsFromMediaList('list') 
    elif mode == 5:
        create.removeItemsFromMediaList('list')
    elif mode == 666:
        updateAll.strm_update() 
    elif mode == 10:
        meta = ""
        # Split url to get tags
        purl = url.split('|')[0]
        utils.addon_log("setResolvedUrl")
        item = xbmcgui.ListItem(path=url)
        # Gest infos from selectet media
        sPatToItem = xbmc.getInfoLabel("ListItem.path")
        sTitle = xbmc.getInfoLabel("ListItem.title")

        try:
            # Exec play process
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
            # Wait until the media is started in player
            while meta.find("video") == -1:
                meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}')
            time.sleep(2)
            if xbmc.getInfoLabel("VideoPlayer.TVShowTitle") != "":
                guiTools.markSeries(xbmc.getInfoLabel("VideoPlayer.TVShowTitle"),xbmc.getInfoLabel("VideoPlayer.Episode"),xbmc.getInfoLabel("VideoPlayer.Season"))
            else:
                guiTools.markMovie(xbmc.getInfoLabel("VideoPlayer.Title"))
        except:
            pass 
    elif mode == 100:
        create.fillPlugins(url)
        try:
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        except:
            pass 
    elif mode == 101:
        create.fillPluginItems(url)
        if not fileSys.writeTutList("select:AddonNavi"):
            tutWin = ["Adding content to your library ",
                       "Search for your Movie, TV-Show or Music. ", 
                       "Mark/select content, do not play a Movie or enter a TV-Show.  ",   
                       "Open context menu on the selected and select *create strms*."]                            
            dialoge.PopupWindow(tutWin)

        try:
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        except:
            pass 
        
    elif mode == 200:
        utils.addon_log("write multi strms")
        try:
            # A dialog to rename the Change Title for Folder and MediaList entry:
            selectAction = ['No, continue with original Title!', 'Rename Title!']
            if not fileSys.writeTutList("select:Rename"):
                tutWin = ["Adding content to your library",
                    "You can rename your Movie, TV-Show or Music title. ", 
                    "To make your scraper recognize the content, some times it is necessary to rename the title ",
                    "Be careful, wrong title can also cause that your scraper can't recognize your content."]                
                dialoge.PopupWindow(tutWin)
            if guiTools.selectDialog(selectAction, header = 'Title for Folder and MediaList entry') == 1 or name == None or name == "":
                name = guiTools.editDialog(name).lstrip().rstrip() + "++RenamedTitle++"
            
            if not fileSys.writeTutList("select:ContentTypeLang"):
                tutWin = ["Adding content to your library",
                          "Now select your content type. ", 
                          "Select language or YouTube type  ",
                          "Wait for done message."]                
                dialoge.PopupWindow(tutWin)   
            cType = guiTools.getType(url)

            fileSys.writeMediaList(url, name, cType)
            dialog.notification(cType, name.replace('++RenamedTitle++', ''), xbmcgui.NOTIFICATION_INFO, 5000, False) 
            create.fillPluginItems(url, strm=True, strm_name=name, strm_type=cType)
            dialog.notification('Writing items...', "Done", xbmcgui.NOTIFICATION_INFO, 5000, False)
        except IOError as (errno, strerror):
            print ("I/O error({0}): {1}").format(errno, strerror)
        except ValueError:
            print ("No valid integer in line.")
        except:
            guiTools.infoDialog(url + " " +  name + " " +  cType)
            utils.addon_log(url + " " +  name + " " +  cType)
            print (url + " " +  name + " " +  cType)
            raise    
    elif mode == 201:
        utils.addon_log("write single strm")
        # create.fillPluginItems(url)
        # makeSTRM(name, name, url)
