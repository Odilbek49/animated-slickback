import sqlite3


con = sqlite3.connect('./crazyysasha/game.sqlite');

cursor = con.cursor();

cursor.execute('create table if not exists users (id integer primary key autoincrement, name, telegram_id integer)');


def createUser(name, telegram_id):
    cursor.execute('insert into users (name, telegram_id) values (?, ?)', (name, telegram_id))
    con.commit();


def findUserByTelegramId(telegram_id):
    response =  cursor.execute(f'select * from users where telegram_id = {telegram_id}');
    rows = response.fetchall();
    if len(rows) >0:
        return rows[0];
    else:
        return None;


if __name__ == "__main__":
    createUser('Sasha', 21343223)