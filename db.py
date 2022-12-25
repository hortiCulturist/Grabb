import sqlite3 as sqlt

db_name = 'channels_database.db'

# **********************************************************************************************************************
# СОЗДАНИЕ БАЗЫ ДАННЫХ


def start_db():
    base = sqlt.connect(db_name)
    base.execute('CREATE TABLE IF NOT EXISTS "Channels" ("id"	INTEGER NOT NULL UNIQUE,'
                 '"name"            BLOB,'
                 '"donor_channel"   INTEGER,'
                 '"link"            BLOB,'
                 '"promo"           BLOB,'
                 'PRIMARY KEY("id" AUTOINCREMENT))')
    base.execute('CREATE TABLE IF NOT EXISTS "my_channel" ("id"	INTEGER,'
                 '"name"            BLOB,'
                 '"my_channel"	    INTEGER)')
    base.execute('CREATE TABLE IF NOT EXISTS "promocodes" ("id"	INTEGER,'
                 '"name"            BLOB,'
                 '"promo"	        BLOB)')
    base.commit()


# **********************************************************************************************************************
# **********************************************************************************************************************
# КОМАНДЫ

def add_pattern(data):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    name = data[3]
    id = int(data[4])
    link = data[5]
    promo = data[6]
    cur.execute('INSERT INTO Channels VALUES (null, ?, ?, ?, ?)', (name, id, link, promo))
    base.commit()
    base.close()


def add_my_channel(name, channel):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    id = cur.execute('SELECT id from Channels WHERE name = ?', [name]).fetchone()
    cur.execute('INSERT INTO my_channel(id, name, my_channel) VALUES (?, ?, ?)', [id[0], name, channel])
    base.commit()
    base.close()


def add_promocode(name, promo):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    id = cur.execute('SELECT id from Channels WHERE name = ?', [name]).fetchone()
    cur.execute('INSERT INTO promocodes(id, name, promo) VALUES (?, ?, ?)', [id[0], name, promo])
    base.commit()
    base.close()


def delete_channel(id):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    cur.execute('DELETE FROM my_channel WHERE my_channel = ?', (id,))
    base.commit()
    base.close()


def delete_promocode(promo):

    base = sqlt.connect(db_name)
    cur = base.cursor()
    cur.execute('DELETE FROM promocodes WHERE promo = ?', (promo,))
    base.commit()
    base.close()


def get_my_channel(name):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    channels = cur.execute('SELECT * from my_channel WHERE name = ?', (name[0],)).fetchall()
    base.close()
    return channels


def get_promocode(name):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    channels = cur.execute('SELECT * from promocodes WHERE name = ?', (name[0],)).fetchall()
    base.close()
    return channels


def delete_pattern(name):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    cur.execute('DELETE FROM Channels WHERE name = ?', (name,))
    base.commit()
    base.close()


def update_donor_channel(name, channel_id):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    cur.execute('UPDATE Channels SET donor_channel = ? WHERE name = ?', (channel_id, name))
    base.commit()
    base.close()


def update_link(name, link):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    cur.execute('UPDATE Channels SET link = ? WHERE name = ?', (link, name))
    base.commit()
    base.close()


def update_promocode(name, promo):
    base = sqlt.connect(db_name)
    cur = base.cursor()
    cur.execute('UPDATE Channels SET promo = ? WHERE name = ?', (promo, name))
    base.commit()
    base.close()


def view_all_pattern():
    base = sqlt.connect(db_name)
    cur = base.cursor()
    all = cur.execute('SELECT * from Channels').fetchall()
    base.close()
    return all


# **********************************************************************************************************************
# **********************************************************************************************************************
# ОСНОВНАЯ ФУНКЦИЯ

def get_channels_data():
    base = sqlt.connect(db_name)
    cur = base.cursor()
    data_list = cur.execute('SELECT Channels.donor_channel, my_channel.my_channel, Channels.link,'
                            ' Channels.promo, promocodes.promo from Channels '
                            'join my_channel on Channels.id = my_channel.id '
                            'join promocodes on promocodes.id = Channels.id ').fetchall()
    base.close()
    return data_list
# **********************************************************************************************************************
