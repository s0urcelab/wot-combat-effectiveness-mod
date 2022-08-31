# -*- coding: utf-8 -*-
# https://www.apache.org/licenses/LICENSE-2.0.html

import json
import traceback
import re
import sys
if "urllib.request" in sys.modules:
    from urllib.request import quote
else:
    from urllib2 import quote

from mod_recent_stat_constant import PLAYER_ID_NOT_KNOWN, STAT_FIELDS
from mod_recent_stat_logging import logInfo, logError
from mod_recent_stat_network import getRawSiteText, getFormattedHtmlText, getJsonText
from mod_recent_stat_provider import StatProvider


class Kttc(StatProvider):
    name = "Kttc"

    def _getStatistics(self, region, nickname, playerId, playerIdToData):
        # type: (str, str, int, dict) -> None
        playerData = playerIdToData[playerId]

        qname = quote(nickname)
        full_url = "http://wotbox.ouj.com/wotbox/index.php?r=default/index&pn={}".format(qname)
        # logInfo(full_url)
        recentStatJson = getFormattedHtmlText(full_url)
        findCE = re.search(r"<span class='num'>(\d+)</span>", recentStatJson)
        findWR = re.search(r"win-rate='(\d+)'", recentStatJson)
        if findCE:
            playerData.xwn8 = int(findCE.group(1))
        if findWR:
            playerData.wn8 = int(findWR.group(1))
            
            playerData.hasRecentStat = True
