from datetime import datetime
import sqlite3


con = sqlite3.connect('./crazyysasha/game.sqlite');

cursor = con.cursor();

cursor.execute('create table if not exists users (id integer primary key autoincrement, name, telegram_id integer)');

cursor.execute('create table if not exists games (id integer primary key autoincrement, winner, played_at, players)')
try:
    cursor.execute('alter table games add column if not exists status default "end"')

except:
    print('status added early');

def createUser(name, telegram_id):
    cursor.execute('insert into users (name, telegram_id) values (?, ?)', (name, telegram_id))
    con.commit();


def createGameHistory(who:str, players:list):
    cursor.execute('insert into games (winner, played_at, players) values(?, ?, ?)', (who, datetime.now(), str(players)))
    con.commit();



def getAllUserResults(who: str):
    response =  cursor.execute(f'select * from games where players like "%{who}%"')
    rows = response.fetchall();

    if len(rows) > 0:
        return rows
    
    return None

def findUserByTelegramId(telegram_id):
    response =  cursor.execute(f'select * from users where telegram_id = {telegram_id}');
    rows = response.fetchall();
    if len(rows) >0:
        return rows[0];
    else:
        return None;


if __name__ == "__main__":
    
    # createGameHistory('bot', ['bot', 2312312]);
    print(getAllUserResults('bot'));
    # createUser('Sasha', 21343223)