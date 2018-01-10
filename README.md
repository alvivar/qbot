# QBot
## Python bot that tweets on schedules, using json files as configuration!

### Instructions

- Use **'python qbot.py -w "somepath/somename.json"'** to create a **json** file somewhere
- Modify the **json** file with your info, including tweet schedule, messages, twitter account tokens
- Use **'python qbot.py -s'** to start the queue process!
- Repeat!

### Tips

- Use **'python setup.py build'** to create a cx_Freeze executable
- Create a script that programatically add messages to the **json** file

### More details

```
     ["]
    /[_]\
     ] [
usage: qbot.py [-h] [-w WATCH_JSON [WATCH_JSON ...]] [-s] [-p] [-r REPEAT]

Bot that tweets on schedules, using json files as configuration

optional arguments:
  -h, --help            show this help message and exit
  -w WATCH_JSON [WATCH_JSON ...], --watch-json WATCH_JSON [WATCH_JSON ...]
                        create or add to the watch list a json file to be used
                        as configuration and data input for a schedule
  -s, --start-queue     start the queue process, updates data from the files
                        in the watch list, then tweets based on the schedules
  -p, --prune           remove orphan files from the watch list
  -r REPEAT, --repeat REPEAT
                        seconds to wait between queue processes, 300s default,
                        use 0 or less to not repeat at all
```
