# Weechat Scripts

This is a collection of scripts I've written for Weechat. Feel free to use them and improve
on them. Please join me in `#thefinn93` on Freenode to discuss these scripts, dank maymays,
or whatever else strikes your fancy.


Note that all of these have Sentry Raven built into them, to help collect information about errors
that come up. It doesn't do anything by default, but you will need to install the `raven` pypi
package to avoid import errors.


## dblog
_Note: Still in testing, if you're using this please get in touch so I can gather debugging data._

`~/.weechat/logs` is increasingly full of interesting but unindexed data. I wanted this data
to be indexed and queryable, so I wrote `dblog.py` to write it all to a database as well as
a file. Requires [dataset](https://dataset.readthedocs.io/en/latest/) (`pip install dataset`).
