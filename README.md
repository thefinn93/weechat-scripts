# Weechat Scripts

This is a collection of scripts I've written for Weechat. Feel free to use them and improve
on them.


## dblog
_Note: Still in testing, if you're using this please get in touch so I can gather debugging data._

`~/.weechat/logs` is increasingly full of interesting but unindexed data. I wanted this data
to be indexed and queryable, so I wrote `dblog.py` to write it all to a database as well as
a file. Requires [dataset](https://dataset.readthedocs.io/en/latest/) (`pip install dataset`)
and a driver to connect to your database of choice (`pip install sqlite3`,
  `pip install pycopg2`, etc).
