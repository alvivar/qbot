# Qbot

## Python bot that tweets on schedules, using json files as configuration!

### Instructions

- Use **'python qbot.py -w "somepath/somename.json"'** to create a **json** file somewhere
- Modify the **json** file with your stuff, including tweet schedule, messages, twitter account tokens
- Use **'python qbot.py -s'** to start the queue process!
- **Qbot** will tweet all messages based on your schedules for any **json** file you created with it
- Repeat!

### Tips

- Create a script that programatically add messages to the **json** file (I do this for all my bots)
- Run **'python cxfreezesetup.py build'** to create a executable using **cx_Freeze**
- Cron or task schedule **'python qbot.py -s'** or the executable
- The database is a sqlite named **data.db**, use a software like [sqlitebrowser](http://sqlitebrowser.org/) to read or modify it

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
