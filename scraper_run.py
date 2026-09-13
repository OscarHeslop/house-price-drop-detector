#python -m playwright install chromium
from scraper_func import *
import datetime
from database import create_table


from database import add_houses_row_to_database


import sqlite3
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
                WHERE id = %s
                ORDER BY time ASC
            """, (val.replace("'", ""),))
            price_over_time = cursor.fetchall()

            if len(price_over_time) > 1:
                price_before = int(price_over_time[-2][1])
                latest_rowid, price_after, notification, url, address = price_over_time[-1]
                if int(price_after) < int(price_before) and notification == 0:
                    print(id, price_after, price_before)
                    price_drop_dict[id] = {
                        "address": address,
                        "price_before": price_before,
                        "price_after": int(price_after),
                        "url": url
                    }
                    cursor.execute("UPDATE houses SET notification = 1 WHERE database_id = %s", (latest_rowid,))
            else:
                print("price over time is nothing")

        db.commit()

        reply = "<u>" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "</u>"
        print(price_drop_dict)

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
def web_scrape(area):



    create_table()

    page, browser = open_browser()

    if press_accept_all(page):

        send_area_to_browser(page, area)#only area needed

        set_min_and_max_price(page)
        set_min_and_max_beds(page)

        # wait for Rightmove to refresh results
        # wait for new cards
        page.wait_for_selector(
            '[data-monitor-testid="propertyCard-img-link"]',
            timeout=2000
        )

        page.wait_for_timeout(3000)
        num_pages = int(
            page.locator('[aria-label="pagination dropdown"] option').last.inner_text()
        )


        # getting num houses
        total = 0

        for page_number in range(1, num_pages + 1):

            if page_number > 1:
                page.select_option(
                    '[aria-label="pagination dropdown"]',
                    str(page_number)
                )

            house_links = page.locator(
                '[data-monitor-testid="propertyCard-img-link"]'
            )

            total += house_links.count()



        # START SCRAPING AGAIN
        for page_number in range(1, num_pages + 1):

            if page_number > 1:
                page.select_option(
                    '[aria-label="pagination dropdown"]',
                    str(page_number)
                )

                page.wait_for_selector(
                    '[data-monitor-testid="propertyCard-img-link"]'
                )

                page.wait_for_timeout(1000)


            house_links = page.locator(
                '[data-monitor-testid="propertyCard-img-link"]'
            )

            number_of_houses = house_links.count()


            for i in range(number_of_houses):
                
                new_house_page, url = go_to_house_card(page, browser, i)

                press_accept_all(new_house_page)

                rightmove_id = get_house_id(url)
                link = "https://www.rightmove.co.uk" + url

                price = get_house_price(new_house_page)
                if price is None:
                    new_house_page.close()
                else:
                    price = int(price.replace("£","").replace(",",""))

                    address = get_house_address(new_house_page)
                    postcode = get_house_postcode(new_house_page)
                    

                    description = ", ".join(
                        get_house_key_features(new_house_page)
                    )

                    time = datetime.datetime.now()

                    val = add_houses_row_to_database(
                        rightmove_id,
                        area,
                        address,
                        price,
                        description,
                        time,
                        0,       # notification starts at 0
                        link,
                        postcode
                    )
                    print(val)

                    new_house_page.close()
    browser.close()

