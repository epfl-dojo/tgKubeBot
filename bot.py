# projet de Kube Bot
# chercher quel last version de KuberNet S sur le web
# import
import urllib.request, json, pprint
import pickle, asyncio

from aiotg import Bot, Chat
from yaml import load

def private_bot_token():
    return load(open("PRIVATE.yml"))["token"]

bot = Bot(api_token=private_bot_token())

def get_last_ver():
    releases_json = urllib.request.urlopen("https://api.github.com/repos/kubernetes/kubernetes/releases").read()
    releases = json.loads(releases_json.decode())
    for r in sorted(releases, key=lambda r:r["tag_name"], reverse=True):
        if "-" not in r["tag_name"]:
            return r

@bot.command(r"/echo (.+)")
def echo(chat: Chat, match):
    return chat.reply(match.group(1))

@bot.command(r"/version")
def version(chat: Chat, unuse):
    return chat.reply(get_last_ver()["tag_name"])

@bot.command(r"/date")
def date_v (chat: Chat, unuse):
    return chat.reply(get_last_ver()["published_at"])

@bot.command(r"/flood")
async def flood (chat: Chat, unuse):
    for i in range(20):
        await asyncio.sleep(2)
        await chat.send_text("coucou")


STATE_FILE = "./k8s.state"



if __name__ == '__main__':
    try:
        state = pickle.load(open(STATE_FILE))
    except:
        state = {
            "latest" : None,
        }
    latest = get_last_ver()
    print("Latest version is : %s" % latest['tag_name'])
    print(latest['body'])

    bot.run()
