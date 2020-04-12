from constants import GREETING_TEMPLATE, PREFIX

import sqlite3


class DatabaseProcessor:
    def __init__(self):
        self.db = sqlite3.connect('global.db')
        self.shell = self.db.cursor()

        self.shell.execute("create table if not exists guild_settings("
                "guild_id integer not null primary key,"
                "greeting text);")

        self.db.commit()

    def _create_row_guild_settings(self, guild_id):
        self.shell.execute("insert into guild_settings(guild_id, greeting) " \
                "values(?, ?);",
                (guild_id, GREETING_TEMPLATE,))
        self.db.commit()

    def _get_greeting(self, guild_id):
        self.shell.execute("select greeting from guild_settings where guild_id=?;",
                (guild_id,))

        return self.shell.fetchone()[0]

    def _get_guilds(self):
        self.shell.execute("select guild_id from guild_settings;")

        return self.shell.fetchall()

    def _remove_row_guild_settings(self, guild_id):
        self.shell.execute("delete from guild_settings where guild_id=?;",
                (guild_id,))
        self.db.commit()

    def _set_greeting(self, guild_id, greeting_text):
        self.shell.execute("update guild_settings set greeting=? where guild_id=?;",
                (greeting_text, guild_id,))
        self.db.commit()
