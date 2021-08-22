# -*- coding: utf-8 -*-
import discord
import voiceflow
import json

num_emojis = ["0️⃣","1️⃣","2️⃣","3️⃣",
              "4️⃣","5️⃣","6️⃣","7️⃣",
              "8️⃣","9️⃣"]

def main():
    client = KnowledgeDunkBot()
    token = open('token.txt', 'r').read()
    client.run(token)

class KnowledgeDunkBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.__settings = json.load(open('config.json','r'))
        self.__prefix = self.__settings['prefix']
    async def on_ready(self):
        print('Logged in as {0}!'.format(self.user))
    async def on_message(self,message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == self.user or not message.content.startswith(self.__prefix):
            return
        payload = message.content[len(self.__prefix):]
        user = message.author.id
        print("{}: {}".format(user,payload))
        data = voiceflow.request(user,payload)
        sent_message = await message.channel.send(self.prepare(data))
        for i in range(len(data["options"])):
           await sent_message.add_reaction(num_emojis[i])
    def prepare(self,data):
        print(data)
        to_print = data["indications"]
        for i in range(len(data["options"])):
            to_print.append(num_emojis[i] + " " + data["options"][i])
        to_print = '\n'.join(to_print)
        return to_print
    async def on_reaction_add(self,reaction, user):
        if user == self.user:
            return
        if reaction.emoji in num_emojis:
            data = voiceflow.request(user.id,"repeat")
            data = voiceflow.request(user.id,data["options"][num_emojis.index(reaction.emoji)])
            sent_message = await reaction.message.channel.send(self.prepare(data))
            for i in range(len(data["options"])):
               await sent_message.add_reaction(num_emojis[i])
            await reaction.message.delete()

if __name__ == "__main__":
    main()
