from tortoise import Tortoise, run_async
from aiohttp import web
from models import User, Shell, Cpanel, UserDetail, Purshare_types, Purchase
from bs4 import BeautifulSoup
import cssutils

import json
import re
import datetime

async def cors_middleware(app, handler):
    async def middleware_handler(request):
        if request.method == 'OPTIONS':
            response = web.Response()
        else:
            response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = '*'  # Allow from all origins
        response.headers['Access-Control-Allow-Headers'] = '*'  # Allow all headers
        response.headers['Access-Control-Allow-Methods'] = '*'  # Allow all methods
        return response
    return middleware_handler

async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

# run_async is a helper function to run simple async Tortoise scripts.
run_async(init())

async def process_shell_data(data):
    for row in data:
        _id = row[1]
        machine_hostname = re.sub('<[^<]+?>', '', row[2]).strip() # Linux - PHP 7.4.33 Linux yisu-648bf556cc4e0 3.10.0-862.14.4.el7.x86_64 #1 SMP Wed Sep 26 15:12:11 UTC 2018 x86_64
        country = re.sub('<[^<]+?>', '', row[3]).strip() # Hong Kong SAR China
        type = re.sub('<[^<]+?>', '', row[4]).strip() # http
        tld = row[5]
        masked_domain = row[6]
        isp = row[7]
        seo = row[8]

        username = re.sub('<[^<]+?>', '', row[13]).strip()
        price = row[15]
        post_date = datetime.datetime.strptime(row[16],"%d/%m/%Y %I:%M:%S %p")

        seller_user, _ = await User.get_or_create(
            username=username
        )

        shell, _ = await Shell.get_or_create(
            id=int(_id),
            user = seller_user,
            machine_hostname = machine_hostname,
            country = country,
            http_type = type=='http',
            tld = tld,
            masked_domain = masked_domain,
            isp = isp,
            seo = seo,
            price = float(price), # we store 8.55 as 855 so we don't need float
            post_date = post_date
        )

        await shell.save()

async def process_cpanel_data(data):
    for row in data:
        _id = row[1]
        country = re.sub('<[^<]+?>', '', row[2]).strip() # Brazil
        type = re.sub('<[^<]+?>', '', row[3]).strip()
        tld = row[4]
        masked_domain = row[5]
        isp = row[6]
        cms = re.sub('<[^<]+?>', '', row[7]).strip()

        username = re.sub('<[^<]+?>', '', row[12]).strip()
        price = row[14]

        seller_user, _ = await User.get_or_create(
            username=username
        )

        await Cpanel.get_or_create(
            id=int(_id),
            user = seller_user,
            country = country,
            http_type = type=='http',
            tld = tld,
            masked_domain = masked_domain,
            isp = isp,
            cms = cms,
            price = float(price), # we store 8.55 as 855 so we don't need float
        )


async def process_seller_sales_data(data, seller_username):
    soup = BeautifulSoup(data)

    for row in soup.find_all('tr'):
        buyer_username = row.find_all('td')[3].text
        sold_date = datetime.datetime.strptime(row.find_all('td')[1].text,"%Y-%m-%d %H:%M:%S")
        purshare_type = row.find_all('td')[2].text # premium_cpanel
        review = row.find_all('td')[4].text

        seller_user, _ = await User.get_or_create(
            username=seller_username
        )

        buyer_user, _ = await User.get_or_create(
            username=buyer_username
        )

        purshare_type, _ = await Purshare_types.get_or_create(
            name=purshare_type
        )

        await Purchase.get_or_create(
            sold_date=sold_date,
            review=review,
            purshare_type=purshare_type,
            buyer=buyer_user,
            seller=seller_user,
        )




async def process_seller_details_data(data):
    soup = BeautifulSoup(data)
    username = None
    last_login = None
    last_register_date = None
    tatal_sales = None
    total_sold_items = None
    int_rating = None

    for row in soup.find_all('tr'):
        key = row.find('th').text
        value = row.find('td')

        if key == 'Seller':
            username = value.text
        
        if key == 'Last Login':
            last_login = datetime.datetime.strptime(value.text,"%d/%m/%Y %I:%M:%S %p")
        
        if key == 'Register Date':
            last_register_date = datetime.datetime.strptime(value.text,"%d/%m/%Y")
        
        if key == 'Total Sales':
            tatal_sales = int(float(value.text.replace("$", "").strip()))
        
        if key == 'Total Sold Items':
            total_sold_items = int(value.text)
        
        if key == 'Average Rating':
            percent_dating = cssutils.parseString(value.find("style").text).cssRules[0].style.width.replace("%", "")
            int_rating = int(float(percent_dating))

    seller_user, _ = await User.get_or_create(
        username=username
    )
    if seller_user:
        await UserDetail.get_or_create(
            user=seller_user,
            last_login=last_login,
            last_register_date=last_register_date,
            tatal_sales=tatal_sales,
            total_sold_items=total_sold_items,
            int_rating=int_rating
        )


async def hello(request):
    json_result = await request.json()

    if json_result['path'] == 'seller_sales':
        await process_seller_sales_data(json_result['response'], json_result['seller_username'])
        return web.Response(text="Hello, world")

    if json_result['path'] == 'seller_details':
        await process_seller_details_data(json_result['response'])
        return web.Response(text="Hello, world")

    data = json.loads(json_result['response'])['data']

    if json_result['path'] == 'divPage3.html':
        await process_shell_data(data)
        return web.Response(text="Hello, world")
    
    if json_result['path'] == 'divPage2.html':
        await process_cpanel_data(data)
        return web.Response(text="Hello, world")

app = web.Application(middlewares=[cors_middleware])
app.add_routes([web.post('/', hello)])

if __name__ == '__main__':
    web.run_app(app, port=8081)

