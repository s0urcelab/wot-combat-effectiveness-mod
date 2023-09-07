# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import sys
from threading import Thread
import time
import traceback

from mod_recent_stat_config_format import ConfigFormat
from mod_recent_stat_config_main import ConfigMain
from mod_recent_stat_config_wg_id import ConfigWgId
from mod_recent_stat_converter import isPlayerFake
from mod_recent_stat_constant import BADGE_TYPE
from mod_recent_stat_logging import logInfo, logError
from mod_recent_stat_wg_stats import WgStats


class ModRecentStat:
    notificationsShowed = False

    def __init__(self, configFormat=None, configMain=None, configWgId=None):
        # type: (ConfigFormat, ConfigMain, ConfigWgId) -> None
        logInfo("Mod loading is started.")
        logInfo("Python version: %s." % sys.version)

        self._configFormat = configFormat or ConfigFormat()
        self._configMain = configMain or ConfigMain()
        self._configWgId = configWgId or ConfigWgId()

        self._playerIdToData = dict()
        self._wgStats = WgStats(self._configMain, self._configWgId)

        self._welcomeMessage = self._loadWelcomeMessage()
        # self._infoMessage = self._loadInfoMessage()

        self._isAnonymousHost = False

        logInfo("Mod loading is finished: main = %s, format = %s." % (self._configMain, self._configFormat))

    def getWelcomeMessage(self):
        # type: () -> str
        return self._welcomeMessage

    def getInfoMessage(self):
        # type: () -> str
        return self._infoMessage

    @staticmethod
    def _loadWelcomeMessage():
        # type: () -> str
        defaultMessage = "盒子战斗力纯净版<br>" + \
                        "插件版本: 1.22-0<br>" + \
                        "官网: <a href='event:https://wot.src.moe/box-ce-mod'>https://wot.src.moe/box-ce-mod</a><br>"
        return defaultMessage

    def _loadInfoMessage(self):
        # type: () -> str
        return (
                       "Configs:<br>" +
                       "<br>" +
                       "main = %s<br>" +
                       "<br>" +
                       "format = %s"
               ) % (self._configMain, self._configFormat)

    def _checkIfHostIsAnonymous(self, vehicles):
        # type: (dict) -> None
        try:
            for _vehicleID, vehicleData in vehicles.items():
                if vehicleData["name"] != vehicleData["fakeName"]:
                    self._isAnonymousHost = True
        except BaseException:
            logError("Can't check if host is anonymous.", traceback.format_exc())

    def loadPlayerDataByVehicleList(self, vehicles):
        # type: (dict) -> None
        self._checkIfHostIsAnonymous(vehicles)

        startTime = time.time()
        self._wgStats.loadPlayerDataByVehicleList(vehicles, self._playerIdToData)

        try:
            vehicleInfoTasks = set()

            for _vehicleID, vehicleData in vehicles.items():
                if "name" in vehicleData and "accountDBID" in vehicleData:
                    playerName = vehicleData["name"]
                    playerId = vehicleData["accountDBID"]

                    if playerId in self._playerIdToData and self._playerIdToData[playerId].hasRecentStat:
                        continue

                    for provider in self._configMain.recentStatProviders:
                        task = Thread(
                            target=provider.getStatistics,
                            args=(self._configMain.region, playerName, playerId, self._playerIdToData)
                        )
                        vehicleInfoTasks.add(task)
                        task.start()

            logInfo("Vehicle info task count: %d." % len(vehicleInfoTasks))

            for task in vehicleInfoTasks:
                task.join()

            logInfo("Tasks are joined.")
        except BaseException:
            logError("Can't load recent stats by vehicle list.", traceback.format_exc())

        withStat = 0
        withRecentStat = 0
        withoutStat = 0

        for _vehicleID, vehicleData in vehicles.items():
            if "accountDBID" in vehicleData:
                playerId = vehicleData["accountDBID"]

                if playerId in self._playerIdToData:
                    withStat += 1  # TODO if all nulls then withoutStat

                    if self._playerIdToData[playerId].hasRecentStat:
                        withRecentStat += 1
                else:
                    withoutStat += 1

        logInfo("Stats loaded in %s ms. With stats: %s, with recent stats: %s, without stats: %s." %
                (int(round((time.time() - startTime) * 1000)), withStat, withRecentStat, withoutStat))

    def formatPlayerName(self, accountDBID, playerName):
        # type: (int, str) -> str
        if self._isAnonymousHost:
            return "? %s" % playerName  # TODO move to config_format

        if isPlayerFake(accountDBID):
            return "? %s" % playerName  # TODO move to config_format

        playerInfo = self._playerIdToData.get(accountDBID, None)
        if playerInfo is not None:
            try:
                formattedPlayerStat = self._configFormat.playerName.format(**playerInfo.createDict(self._configFormat))
                newPlayerName = formattedPlayerStat + playerName
                return newPlayerName
            except BaseException:
                logError("Can't format player name", traceback.format_exc())
                return playerName

        return playerName

    def getPlayerBadgeIcon(self, accountDBID):
        if self._configMain.badgeType == BADGE_TYPE.BOB2020_TEAM_COLOR:
            teamId = self._getPlayerBob2020TeamId(accountDBID)
            if teamId is None:
                return None

            return "badge_%s" % (20 + teamId)

        colorId = self._getPlayerColorId(accountDBID)
        if colorId is None:
            return None

        return "badge_%s" % (10 + colorId)

    def _getPlayerColorId(self, accountDBID):
        # type: (int) -> [int, None]
        """the worst is 0 and the best is 5"""
        if self._isAnonymousHost:
            return None  # todo: don't clear badges in such situation

        playerInfo = self._playerIdToData.get(accountDBID, None)
        if playerInfo is None:
            return None

        xwn8 = playerInfo.xwn8
        if xwn8 is None:
            return None

        # 国服盒子战斗力分档
        if xwn8 < 600:
            return 0

        if xwn8 < 800:
            return 1

        if xwn8 < 1000:
            return 2

        if xwn8 < 1200:
            return 3

        return 4

    def _getPlayerBob2020TeamId(self, accountDBID):
        # type: (int) -> [int, None]
        if self._isAnonymousHost:
            return None  # todo: don't clear badges in such situation

        playerInfo = self._playerIdToData.get(accountDBID, None)
        if playerInfo is None:
            return None

        achievements = playerInfo.achievements
        if achievements is None:
            return None

        # the numbers are in sync with badges modifier:

        if "medalBobKorbenDallas" in achievements.keys():
            return 0

        if "medalBobAmway921" in achievements.keys():
            return 1

        if "medalBobLebwa" in achievements.keys():
            return 2

        if "medalBobYusha" in achievements.keys():
            return 3

        return None
