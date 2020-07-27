from constants import GREETING_TEMPLATE, PREFIX

import sqlite3


class DatabaseProcessor:
    def __init__(self):
        self.db = sqlite3.connect('global.db')
        self.shell = self.db.cursor()

        self.shell.execute("create table if not exists guild_settings("
                           "guild_id integer not null primary key,"
                           "greeting text,"
                           "enabled_greeting bool);"
                           )

        self.shell.execute("create table if not exists donators("
                           "id integer not null primary key autoincrement,"
                           "who varchar[7],"
                           "id_who integer,"
                           "unlimit bool,"
                           "lvl tinyint);"
                           )

        self.db.commit()

    def create_row_donators(self, who, id, unlimit, lvl):
        self.shell.execute("insert into donators(who, id_who, unlimit, lvl) "
                           "values(?, ?, ?, ?);",
                           (who, id, unlimit, lvl,))
        self.db.commit()

    def create_row_guild_settings(self, guild_id):
        self.shell.execute("insert into guild_settings(guild_id, greeting, enabled_greeting) "
                           "values(?, ?, ?);",
                           (guild_id, GREETING_TEMPLATE, True,))
        self.db.commit()

    def is_greeting_enabled(self, guild_id):
        self.shell.execute("select enabled_greeting from guild_settings where guild_id=?;",
                           (guild_id,))

        return self.shell.fetchone()[0]

    def get_greeting(self, guild_id):
        self.shell.execute("select greeting from guild_settings where guild_id=?;",
                           (guild_id,))

        return self.shell.fetchone()[0]

    def get_guilds(self):
        self.shell.execute("select guild_id from guild_settings;")

        return self.shell.fetchall()

    def get_donators_guilds(self):
        self.shell.execute("select id_who from donators where who='guild'")

        return [i[0] for i in self.shell.fetchall()]

    def get_donators_members(self):
        self.shell.execute("select id_who from donators where who='member'")

        return [i[0] for i in self.shell.fetchall()]

    def is_donator(self, id_who):
        self.shell.execute("select id from donators where id_who=?;",
                           (id_who,))
        return self.shell.fetchone() is not None

    def is_unlimit(self, id_who):
        self.shell.execute("select unlimit from donators where id_who=?;",
                           (id_who,))
        return self.shell.fetchone()[0] == 1

    def remove_row_donators(self, id_who):
        self.shell.execute("delete from donators where id_who=?",
                           (id_who,))
        self.db.commit()

    def remove_row_guild_settings(self, guild_id):
        self.shell.execute("delete from guild_settings where guild_id=?;",
                           (guild_id,))
        self.db.commit()

    def toggle_enabled_greeting(self, guild_id, is_enabled):
        self.shell.execute("update guild_settings set enabled_greeting=? where guild_id=?;",
                           (is_enabled, guild_id,))

        self.db.commit()

    def set_donator_unlimit(self, id_who):
        self.shell.execute("update donators set unlimit=true where id_who=?;",
                           (id_who,))
        self.db.commit()

    def unset_donator_unlimit(self, id_who):
        self.shell.execute("update donators set unlimit=false where id_who=?;",
                           (id_who,))
        self.db.commit()

    def set_greeting(self, guild_id, greeting_text):
        self.shell.execute("update guild_settings set greeting=? where guild_id=?;",
                           (greeting_text, guild_id,))
        self.db.commit()

    def update_donator_lvl(self, id_who, lvl):
        self.shell.execute("update donators set lvl=? where id_who=?;",
                           (lvl, id_who,))
        self.db.commit()
