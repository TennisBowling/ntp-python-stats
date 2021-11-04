from sanic import Sanic, response
import asyncpg
import asyncio

async def setup():
    global app
    app = Sanic('ntp-stats')
    app.ctx.db = await asyncpg.connect('a', loop=app.loop)

asyncio.run(setup())

@app.route('/unique', methods=['GET'])
async def ntp_unique(request):
    data = await app.ctx.db.fetchrow("""SELECT count(ip) FROM clients;""")
    return response.json({'count': data['count']})

@app.route('/used/<ip>')
async def ntp_used(request, ip):
    data = await app.ctx.db.fetchrow("""SELECT "amount" FROM clients WHERE "ip" = $1;""", ip)
    if not data:
        return response.json({'amount': 0})
    return response.json({'amount': data['amount']})

async def run():
    app.run('0.0.0.0', port=8081)
    await app.ctx.db.close()

asyncio.run(run())
