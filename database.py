import  sqlite3

def create_table():
    db = sqlite3.connect("houses.db")
    
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS houses (
        database_id SERIAL PRIMARY KEY,
        id TEXT,
        area TEXT,
        address TEXT,
        price INTEGER,
        description TEXT,
        time TEXT,
        notification INTEGER,
        link TEXT, 
        postcode TEXT
    )
    """)

    db.commit()


def get_houses(area):
    db = sqlite3.connect("houses.db")
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, address
        FROM houses
        WHERE area = ?
    """, (area,))

    info = cursor.fetchall()
    return info

import datetime

def get_all_ids(area):
    db = sqlite3.connect("houses.db")
    cursor = db.cursor()


    cursor.execute("""
        SELECT id
        FROM houses
        WHERE area = ?
        ORDER BY id ASC
    """, (area,))
    id_list = cursor.fetchall()
    db.close()
    return [i[0] for i in id_list]


def get_price_drop(area):
    db = sqlite3.connect("houses.db")
    cursor = db.cursor()

    price_drop_dict = {}

    if area == "":
        reply = "No area selected"
    else:
        all_id = get_all_ids(area)
        for id in all_id:
            val = id

            cursor.execute("""
                SELECT database_id, price, notification, link, address
                FROM houses
                WHERE id = ?
                ORDER BY time ASC
            """, (val.replace("'", ""),))
            price_over_time = cursor.fetchall()

            if len(price_over_time) > 1:
                price_before = int(price_over_time[-2][1])
                latest_rowid, price_after, notification, url, address = price_over_time[-1]
                if int(price_after) < int(price_before) and notification == 0:
                    price_drop_dict[id] = {
                        "address": address,
                        "price_before": price_before,
                        "price_after": int(price_after),
                        "url": url
                    }
                    cursor.execute("UPDATE houses SET notification = 1 WHERE database_id = >", (latest_rowid,))

        db.commit()

        reply = "<u>" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "</u>"

        if len(price_drop_dict) == 0:
            reply = f'area searching:{area}<br>Last time checked:{reply}<br>No houses with price drop'
        else:
            reply += "<br>"
            for id, info in price_drop_dict.items():
                reply += (
                    f"<li>{id}: {info['address']}, "
                    f"£{info['price_before']} → £{info['price_after']}, "
                    f"<a href='{info['url']}' target='_blank'>View</a></li>"
                )

        db.close()

    return str(reply)

def add_houses_row_to_database(id, area, address, price, description, time,notification,link,postcode):
    db = sqlite3.connect("houses.db")
    cursor = db.cursor()
    # Check the most recent price for this house
    cursor.execute("""
        SELECT price
        FROM houses
        WHERE id = ?
        ORDER BY time DESC
        LIMIT 1
    """, (id,))

    old_price = cursor.fetchone()


    # New house - no ID found
    if old_price is None:

        cursor.execute("""
        INSERT INTO houses
        (id, area, address, price, description, time,notification,link,postcode)
        VALUES(?,?,?,?,?,?,?,?,?)
        """,
        (id, area, address, price, description, time,notification,link,postcode))


    # Existing house - check if price changed
    else:

        old_price = old_price[0]

        if old_price != price:

            cursor.execute("""
            INSERT INTO houses
            (id, area, address, price, description, time,notification, link,postcode)
            VALUES(?,?,?,?,?,?,?,?,?)
            """,
            (id, area, address, price, description, time, notification, link,postcode))

        else:
            print("No price change:", id)


    db.commit()
    db.close()