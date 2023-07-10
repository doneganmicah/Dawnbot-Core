from config import Config
import discord
import re
import random
import json


class Counting:
    def __init__(self, config):
        self.repeat_list = [12345]
        self.loop_list = [1, 2, 3, 4]
        self.config = config

        self.count_started = False
        self.current_count = 0
        self.record = 0
        self.load_data()
        self.gifs = [
            "http://giphygifs.s3.amazonaws.com/media/2WxWfiavndgcM/giphy.gif",
            "https://media.giphy.com/media/KDRv3QggAjyo/giphy.gif",
            "https://media.giphy.com/media/jSfiX3lj42RDG/giphy.gif",
            "https://media.giphy.com/media/DzIIiyZvSdzxu/giphy.gif",
            "https://media.giphy.com/media/y1WDIwAZRSmru/giphy.gif",
            "https://media.giphy.com/media/GjR6RPcURgiL6/giphy.gif",
            "http://giphygifs.s3.amazonaws.com/media/KKXAkRhvK5Tr2/giphy.gif",
            "https://media.giphy.com/media/bGzgOS4hJfazC/source.gif",
            "https://media.giphy.com/media/3eKdC7REvgOt2/giphy.gif",
            "https://media.giphy.com/media/ZSxK6a49mECic/giphy.gif",
            "https://media.giphy.com/media/l3V0H7bYv5Ml5TOfu/giphy.gif",
            "https://media.giphy.com/media/GfAD7Bl016Gfm/giphy.gif",
            "https://media.giphy.com/media/27EhcDHnlkw1O/giphy.gif",
            "http://giphygifs.s3.amazonaws.com/media/ilkfz8Mn5Yz7O/giphy.gif",
            "https://media.giphy.com/media/9Y5k0V15hfhk6CShXu/giphy.gif",
            "https://media.giphy.com/media/11StaZ9Lj74oCY/giphy.gif",
            "https://media.giphy.com/media/d2W7eZX5z62ziqdi/giphy.gif",
            "https://media.giphy.com/media/l1AsKxPkJ1H718KcM/giphy.gif",
            "https://media.giphy.com/media/l1AsKxPkJ1H718KcM/giphy.gif",
            "https://media.giphy.com/media/NQL7Wuo2JSQSY/giphy.gif",
            "https://media.giphy.com/media/EXHHMS9caoxAA/giphy.gif",
            "https://media.giphy.com/media/Ng8scBrPOjX2M/giphy.gif",
            "https://media.giphy.com/media/11tTNkNy1SdXGg/giphy.gif",
            "https://media.giphy.com/media/3o7bu8mwh3U6SXtLjy/giphy.gif",
            "https://media.giphy.com/media/tZiLOffTNGoak/giphy.gif",
            "https://media.giphy.com/media/qgZnIUPFcS3hC/giphy.gif",
            "https://media.giphy.com/media/jeqzmTfTK2Lxm/giphy.gif",
            "https://media.giphy.com/media/usALZW1G4aTde/giphy.gif",
            "https://media.giphy.com/media/ULKnZ7hW07rlS/giphy.gif",
            "https://media.giphy.com/media/Txh1UzI7d0aqs/giphy.gif",
            "https://media.giphy.com/media/yoJC2Olx0ekMy2nX7W/giphy.gif",
            "https://media.giphy.com/media/vzpy2NjOKdeyk/giphy.gif",
            "https://media.giphy.com/media/Ys2Z1pTvkGhH2/giphy.gif",
            "https://media.giphy.com/media/sT1K7rkPJOwh2/giphy.gif",
            "https://media.giphy.com/media/anuMFPLssX6SI/giphy.gif",
            "https://media.giphy.com/media/ii8cN04TWtDzjU7Nev/giphy.gif",
            "https://media.giphy.com/media/j6rV4pR3Ej3Wx6aZSN/giphy.gif",
            "https://media.giphy.com/media/3ohzdMCNziBITnbKDu/giphy.gif",
            "https://media.giphy.com/media/Jrl4FlTaymFFbNiwU5/giphy.gif",
            "https://media.giphy.com/media/QmJ3e9So5M9NdNkOGo/giphy.gif",
            "https://media.giphy.com/media/l41YtZOb9EUABnuqA/giphy.gif",
            "https://media.giphy.com/media/vLRxTAJKH3OSc/giphy.gif",
            "https://media.giphy.com/media/ZOFFvvABgG7dK/giphy.gif",
            "https://media.giphy.com/media/3ePb1CHEjfSRhn6r3c/giphy.gif",
            "https://media.giphy.com/media/26ybwvTX4DTkwst6U/giphy.gif",
            "https://media.giphy.com/media/TwtXMS5EnKDBK/giphy.gif",
            "https://media.giphy.com/media/XzeLltObRrsWjhXNYe/giphy.gif",
            "https://media.giphy.com/media/APqEbxBsVlkWSuFpth/giphy.gif",
            "https://media.giphy.com/media/JO8y56O9mTmeY/giphy.gif",
            "https://media.giphy.com/media/57coyMySySuuk/giphy.gif"
        ]

    def restart(self):
        return_var = False
        if self.current_count > self.record:
            self.record = self.current_count
            return_var = True
        self.current_count = 0
        self.count_started = False
        # del self.loop_list
        self.loop_list = [1, 2, 3, 4]
        # del self.repeat_list
        self.repeat_list = [1]
        self.save_data()
        return return_var

    def check_count(self, message):
        print("counting:")
        print(message.author.name)
        print(message.author.id)
        print(message.content)
        print(f"current: {self.current_count}")
        print(f'repeat list: {self.repeat_list}')
        print(f'loop list: {self.loop_list}')
        print
        number = message.content.split()[0].lower()
        number = re.sub("\D", '', number)

        # if count is started
        if not self.count_started:
            return "count is not started, type /count to begin."

        # if count is a number
        pattern = r'[a-b][A-B]'
        count = re.sub(pattern, '', number)
        print(count)
        if not count.isnumeric():
            return self.embed_builder(message, 1, self.restart())

        # if count was repeated by a player
        if (len(self.repeat_list) > 0):
            if (message.author.id == self.repeat_list[0]):
                return self.embed_builder(message, 2, self.restart())
        # if count was looped
        if (self.loop_list[0] == self.loop_list[2] and self.loop_list[1] == self.loop_list[3]):
            if (self.loop_list[0] == message.author.id):
                return self.embed_builder(message, 3, self.restart())
        # if count was ascending order
        print(int(count))
        print(self.current_count + 1)
        if (int(count) != self.current_count + 1):
            return self.embed_builder(message, 4, self.restart())

        # count is good
        self.repeat_list[0] = message.author.id
        self.loop_list.pop(0)
        self.loop_list.append(message.author.id)
        self.current_count += 1
        self.save_data()
        return

    def embed_builder(self, message, broken_rule, record_broke):

        description = ""
        if (broken_rule == 1):
            description = "You broke rule [3,4, or 5] which states that count has to be a whole Integer!"
        elif (broken_rule == 2):
            description = "You broke rule [1] by repeating a count and sending more than one number in your turn"
        elif (broken_rule == 3):
            description = "You broke rule [5] by looping the count!"
        elif (broken_rule == 4):
            description = "You broke rule [2] which states that count should be in ascending numerical order!"

        embed = discord.Embed(title="You Screwed Up!", description=description, color=0xfc4903)
        if (record_broke):
            embed.set_author(name="A new record has been set!",
                             icon_url="https://media.giphy.com/media/MViYNpI0wx69zX7j7w/giphy.gif")

        embed.set_image(url=self.messUpGIF())
        embed.set_footer(text=f"{message.author.name}: {message.content}", icon_url=message.author.display_avatar.url)

        return embed

    def messUpGIF(self):
        return random.choice(self.gifs)

    def count(self, number, user):
        if user.guild_permissions.administrator:
            self.current_count = number
            self.count_started = True
            return f"Count started at {number}!"
        self.count_started = True
        self.current_count = 0
        return "Count started at 0!"

    def records(self):
        return f"The current record is {self.record}!"

    def rules(self):
        return """If you want to participate in counting please follow these rules:
1. One number at a time.
2. Count must be in ascending numerical order.
3. Message must begin with the number and can have whatever you want after.
4. Whole Integers only, NO equations, spelled out numbers, emotes, gifs, images, videos, or other embedded links. Do not use MARKDOWN on the starting number. no bolds, underlines, strikethrough, code boxes, or spoilers can be used on the starting number. after is fine.
5. Arabic Numerals only.
6. No Looping, Looping is when 2 people count back and forth for more than 2 times. 
```Example of a loop:
        Me: 1 not a loop
        You: 2 not a loop
        Me: 3 not a loop
        You: 4 not a loop
        Me: 5 now a loop    
Example of what to do:
        Me: 1 not a loop
        Person 1: 2 not a loop
        Me: 3 not a loop
        Person1: 4 not a loop    
        Person2: 5 not a loop
        cont...```
7. No deleting your msgs.
8. Be honest if you mess up. Sometimes we make mistakes and its ok.
9. However, dont break the counting on purpose for any reason.
10. Have Fun!"""

    def count_received(self, message):
        if message.author.bot:
            return
        if message.content[0] != '!':
            return self.check_count(message)
        else:
            return "```Please use the new /commands\nExample: /count /record /rules```"

    def save_data(self):
        with open('./counting.sav', 'w+') as f:
            data = {}
            data['current_count'] = self.current_count
            data['counting_record'] = self.record
            data['started'] = self.count_started
            json.dump(data, f)

    def load_data(self):
        try:
            with open('./counting.sav', 'r') as f:
                data = json.load(f)
                self.count_started = data['started']
                self.current_count = data['current_count']
                self.record = data['counting_record']
        except FileNotFoundError:
            pass