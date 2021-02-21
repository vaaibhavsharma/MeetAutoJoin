import discord
import json
from datetime import datetime
from tokens import token


client = discord.Client()

def get_schedule(day=0):
    if day == 0:
        day = datetime.now().strftime("%a")
    print(day)
    f = open("classSchedule.json")
    y = json.load(f)
    y = y.get(day)
    return y

def addclass(classtime, classlink, classname, classdate):
    f = open("classSchedule.json")
    y = json.load(f)
    upd_dict = {classtime: [classname, classlink]}
    y[classdate].update(upd_dict)
    json_object = json.dumps(y, indent=4)
    with open("classSchedule.json", "w") as outfile:
        outfile.write(json_object)

@client.event
async def on_message(message):
    if message.content.find("!Hello") != -1:
        await message.channel.send("Hi")
    elif message.content == '!myclass':
        y = get_schedule()
        if y == None:
            await message.channel.send("No class Today")
        else:
            for classtime in y:
                await message.channel.send(f"""{y[classtime][0]} at {classtime} link {y[classtime][1]}""")

    elif message.content.find("!myclassn") != -1:
        l = message.content.split()
        y = get_schedule(l[1])

        if y == None:
            await message.channel.send("No class Today")
        else:
            for classtime in y:
                await message.channel.send(f"""{y[classtime][0]} at {classtime} link {y[classtime][1]}""")

    elif message.content.find("!addclass") != -1:
        l = message.content.split()
        addclass(l[1], l[2], l[3], l[4])


client.run(token)
