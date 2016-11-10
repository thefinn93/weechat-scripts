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

SCRIPT_NAME = 'dblog'
SCRIPT_AUTHOR = 'Finn Herzfeld <finn@finn.io>'
SCRIPT_VERSION = '0.1'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'Save chat logs to a database'

import_ok = True

try:
    import weechat
except:
    print('This script must be run under WeeChat.')
    print('Get WeeChat now at: http://www.weechat.org/')
    import_ok = False

try:
    import dataset
except ImportError as message:
    print('Missing package(s) for %s: %s' % (SCRIPT_NAME, message))
    import_ok = False

default_options = {
    'database': "sqlite:///irclog.db",
    'table': "logs"
}

options = {}
logtable = None


def init_config():
    global default_options, options, logtable
    for option, default_value in default_options.items():
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, default_value)
        options[option] = weechat.config_get_plugin(option)
    db = dataset.connect(options.get('database'))
    logtable = db[options.get('table', "logs")]


def config_changed(data, option, value):
    init_config()
    return weechat.WEECHAT_RC_OK


def on_print(_, buf, timestamp, tags, displayed, highlighted, prefix, message):
    global logtable
    row = dict()
    row['buffer'] = buf
    row['timestamp'] = int(timestamp)
    for tag in tags.split(","):
        kv = tag.split("_", 1)
        if len(kv) > 1:
            if kv[0] == "irc" and kv[1] == "smart_filter":
                row['smart_filtered'] = True
            else:
                i = 1
                while kv[0] in row:
                    kv[0] = "%s_%d" % (kv[0], i)
                    i += 1
                row[kv[0]] = kv[1]
    row['displayed'] = displayed == 1
    row['highlighted'] = highlighted == 1
    row['prefix'] = prefix
    row['message'] = message
    logtable.insert(row)
    return weechat.WEECHAT_RC_OK

if __name__ == '__main__' and import_ok:
    if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                        SCRIPT_LICENSE, SCRIPT_DESC, '', ''):
        init_config()
        weechat.hook_config('plugins.var.python.%s.*' % SCRIPT_NAME,
                            'config_changed', '')
        weechat.hook_print('', '', '', 1, 'on_print', '')
