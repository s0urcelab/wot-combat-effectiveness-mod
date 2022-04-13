# 多玩盒子战斗力单体插件
An open-source mod displaying players' recent statistics in battle.

## Idea
The main difference of this mod from similar is the ability to display more informative **recent** efficiency rating (approximately of the last thousand battles, that is, of the last 50 hours of playing time). Otherwise, this is the same mod that you saw from *XVM*, *PolarFox* and, *Ekspoint*.

The mod allows displaying statistics in the following places:
- On the battle loading screen.
- On the battle players panel.
- In markers.
- On the Tab players panel.

## How does it look like?
Currently, statistics are displayed using players renaming: a prefix is added to the name. The prefix can be configured in the configuration file.

Also, there is an opportunity to modify badges – currently, two variants are available:
- XWN8 color (default).
- Team color in Battle of Bloggers 2020.

### Battle loading screen
Equal to the Tab players panel.
![recent-stat-battle-loading](screenshots/recent-stat-battle-loading.JPG)

### Battle players panel
![recent-stat-players-panel](screenshots/recent-stat-players-panel.JPG)

### Markers
![recent-stat-markers](screenshots/recent-stat-markers.JPG)

## How does it work?
Mod asks the providers of recent statistics, and if there is an answer, it displays recent stats instead of overall statistics.

Data is taken from [kttc.ru](https://kttc.ru/) (permission is granted) и [noobmeter.com](https://noobmeter.com/) (I couldn't contact the site developers, so I assume there is no prohibition to use the site).

## Contribute
Pull request opening to resolve planning tasks or any other tasks is appreciated. Any ideas on development will also be happy to be heard, you can leave your questions and suggestions in the "[Issues](https://github.com/SerVB/TheRecentStatOfYou/issues)" tab.

In the near future, I do not plan to improve the mod, because I have other projects. I use the mod in the current state, and it suits me.

## Planing tasks
are located in the "[Issues](https://github.com/SerVB/TheRecentStatOfYou/issues)" tab.

## Downloads
are located in the "[Releases](https://github.com/SerVB/TheRecentStatOfYou/releases)" tab.

## Installation
Place the `.wotmod` files into `mods/{game_version}/`. To change default mod settings, download the `configs` dir and place it into `mods/`.

## Build from sources
Run the `build.py` file, the mod will be built in the `build/` dir.

To build badges modification, run the `badgesModifier/battleBadgesModifier.py` file, save the `PNG` file from `target` dir as a `DDS` file, run the `badgesModifier/build.py` file, the badges modification will be built in the `badgesModifier/build/` dir.

## Known issues
- If you use the recent stat feature, at a battle loading start you can notice a lag of 3-10 seconds. It's because of the relatively big amount of data downloading from the Internet. I think there is no possible fix because speed is restricted by the provider.
- Sometimes there are messages in the log like "can't find player name, use slow search". Maybe it's because the mod just renames players. There are no symptoms have been noticed. Anyway, in future game versions, it can become a problem...

## FAQ
**Q**. The mod isn't adopted for a new World of Tanks version.
**A**. Check `mod_recent_stat_init.py` for the list of modified files. Find the same files in the game decompiled sources [WorldOfTanks-Decompiled](https://github.com/StranikS-Scan/WorldOfTanks-Decompiled/). If they haven't been changed, it's likely the mod will work. It's only needed to put the mod in the new dir. For example, the mod was working after an update from 1.1 to 1.2.

**Q**. Which clusters are supported?  
**A**. All clusters should be supported. Try to change it in `config_main.json`.

**Q**. How to change providers of recent stat or completely disable the recent stat feature?  
**A**. In `config_main.json`.

**Q**. How to completely disable statistics, but leave info about bloggers?  
**A**. In `config_main.json` choose `"badgeType": "bob2020TeamColor"` and in `config_format.json` choose `"playerName": ""`.

## Attributions
[ATTRIBUTIONS.MD](ATTRIBUTIONS.MD).
