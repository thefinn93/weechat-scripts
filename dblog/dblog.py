# -*- coding: UTF-8 -*-
#
# Copyright (C) 2016 Finn Herzfeld <finn@finn.io>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import weechat
import dataset
import logging
import raven

SCRIPT_NAME = 'dblog'
SCRIPT_AUTHOR = 'Finn Herzfeld <finn@finn.io>'
SCRIPT_VERSION = '0.3'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'Save chat logs to a database'


default_options = {
    'database': "sqlite:///irclog.db",
    'table': "logs",
    'debug': '',
    'sentry_dsn': ''
}

options = {}
logtable = None
sentry_args = {
    "dsn": None,
    "release": SCRIPT_VERSION
}
sentry = raven.Client(**sentry_args)


def init_config():
    global default_options, options, logtable, sentry, sentry_args
    for option, default_value in default_options.items():
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, default_value)
        options[option] = weechat.config_get_plugin(option)
    if options.get('debug', '') != '':
        logging.basicConfig(filename=options.get('debug'), level=logging.DEBUG)

    sentry_args["dsn"] = options.get('sentry_dsn', '')
    sentry = raven.Client(**sentry_args)

    db = dataset.connect(options.get('database'))
    logtable = db[options.get('table', "logs")]


def config_changed(data, option, value):
    try:
        init_config()
    except Exception:
        logging.exception("Failed to reload config")
        sentry.captureException()
    return weechat.WEECHAT_RC_OK


def on_print(_, buf, timestamp, tags, displayed, highlighted, prefix, message):
    global logtable
    try:
        row = dict()
        row['buffer'] = buf
        row['timestamp'] = int(timestamp)
        for tag in tags.split(","):
            kv = tag.split("_", 1)
            if len(kv) > 1:
                if kv[0] == "irc" and kv[1] in ["smart_filter", "numeric"]:
                    row[kv[1]] = True
                elif kv[0] == "no":
                    row[kv[1]] = False
                else:
                    i = 1
                    while kv[0] in row:
                        logging.info("Duplicate tag name! %s (#%d)", tag, i)
                        kv[0] = "%s_%d" % (kv[0], i)
                        i += 1
                    row[kv[0]] = kv[1]
        row['displayed'] = displayed == 1
        row['highlighted'] = highlighted == 1
        row['prefix'] = prefix
        row['message'] = message
        logtable.insert(row)
    except Exception:
        logging.exception("Failed to store message")
        sentry.captureException()
    return weechat.WEECHAT_RC_OK

if __name__ == '__main__':
    try:
        if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                            SCRIPT_LICENSE, SCRIPT_DESC, '', ''):
            init_config()
            weechat.hook_config('plugins.var.python.%s.*' % SCRIPT_NAME,
                                'config_changed', '')
            weechat.hook_print('', '', '', 1, 'on_print', '')
    except Exception:
        logging.exception("Failed to initialize plugin.")
        sentry.captureException()
