from tortoise import Tortoise, run_async
from aiohttp import web
from models import User, Shell, Cpanel
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

        cpanel, _ = await Cpanel.get_or_create(
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

        await cpanel.save()


async def hello(request):
    json_result = await request.json()
    data = json.loads(json_result['response'])['data']

    if json_result['path'] == 'divPage3.html':
        await process_shell_data(data)
    
    if json_result['path'] == 'divPage2.html':
        await process_cpanel_data(data)

    return web.Response(text="Hello, world")

app = web.Application(middlewares=[cors_middleware])
app.add_routes([web.post('/', hello)])

if __name__ == '__main__':
    web.run_app(app)

