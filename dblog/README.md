# dblog

_Note: Still in testing, if you're using this please get in touch so I can gather debugging data._


A weechat script to log to a database. Requires
[dataset](https://dataset.readthedocs.io/en/latest/) (`pip install dataset`).


## Installation
Place `dblog.py` in your weechat python scripts directory (eg `~/.weechat/python/`) and load
it by typing `/python load dblog` in any weechat buffer.

## Configuration
The default database is sqlite3 (basically a flat file) stored on disk in the cwd in a file called
`irclog.db`. This is probably not what you want, so go ahead and set the database connection string
of your choosing in `plugins.var.python.dblog.database`. For example, to stick with SQLite but keep
the database in `/home/finn/.weechat/logs.db`, you would run:

```
/set plugins.var.python.dblog.database sqlite:////home/finn/.weechat/logs.db
```

The other configuration option available is `plugins.var.python.dblog.table` to specify the name
of the table that the logs should go into. It defaults to `logs`, change if if you feel so inclined.

## Bugs
This script's got em! I just haven't found em yet. If you run into a bug, file an issue on this
repo. If you fix it, file a pull request.

## Possible Improvements
If you want to build these or others, please don't hesitate to get in touch or just do it and open
a pull request:

* A custom buffer that allows querying the database
