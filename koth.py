from config import Config
import discord
import datetime
import json
import time


class Koth:
    def __init__(self, config):
        self.config = config

        self.reset()
        self.load_data()

    def reset(self):
        self.player_info = {}
        self.id_name_mappings = {}
        self.king = None
        self.king_time = None

    # returns a json for an embed that contains the message
    # that the frontend should send. returns None if no message
    # should be sent. well, at some point itll return an embed.
    # for now ill return a string for testing.
    def get_response_to_message(self, message):
        if message.author.bot:
            return

        self.id_name_mappings[message.author.id] = message.author.name

        try:
            result = {
                'climb': self.climb,
                'push': self.push,
                'king': self.king_me,
                'queen': self.queen_me,
                'look': self.look,
                'top': self.top
            }[message.content.split()[0].lower()](message)
            self.save_data()

            return result
        except KeyError:
            return

    def climb(self, message):
        current_level = self.get_user_level(message.author.id)

        if current_level < self.config.top_level:
            self.make_sure_player_info_is_initialized(message.author.id)

            self.player_info[message.author.id]['level'] = current_level + 1
            print("uwu")

    def push(self, message):
        current_level = self.get_user_level(message.author.id)
        id_to_push = message.mentions[0].id

        users_at_level = self.get_users_at_level(current_level)
        if id_to_push in users_at_level:
            self.make_sure_player_info_is_initialized(id_to_push)

            self.player_info[id_to_push]['level'] = 0
            if self.king == id_to_push:
                self.king = None
                self.player_info[id_to_push]['time'] += time.time() - self.king_time

            return f"{self.id_name_mappings[id_to_push]} has been pushed!"

    def queen_me(self, message):
        return self.make_me_leader(message, "queen")

    def king_me(self, message):
        return self.make_me_leader(message, "king")

    def make_me_leader(self, message, title):
        current_level = self.get_user_level(message.author.id)
        print(current_level)

        if current_level == self.config.top_level and self.king == None:
            self.king = message.author.id
            self.king_time = time.time()

            return f"{message.author.name} is the new " + title + "!"

    def look(self, message):
        level = self.get_user_level(message.author.id)
        ids = self.get_users_at_level(level)
        users_at_level = [self.id_name_mappings[id] for id in ids]
        return f"The people at your level ({level}) are: {', '.join(users_at_level)}"

    def top(self, message):
        return_string = ""

        if self.king != None:
            self.player_info[self.king]['time'] += time.time() - self.king_time
            self.king_time = time.time()

        leaderboard = [(player_id, info['time']) for player_id, info in self.player_info.items()]
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        embed = discord.Embed(title="Top Times", description=" ", color=0xfc9803)
        embed.set_author(name="King Of The Hill",
                         icon_url="https://cdn.discordapp.com/avatars/917974224323366975/dc8e7ff24141adb01d758669903bda21.webp")
        place = 1
        for leaderboard_info in leaderboard:
            hours = int(leaderboard_info[1] // 3600)
            minutes = int((leaderboard_info[1] % 3600) // 60)
            seconds = int(leaderboard_info[1] % 60)

            embed.add_field(name="---------",
                            value=f"#{place}: {self.id_name_mappings[leaderboard_info[0]]} (hours: {hours}, minutes: {minutes}, seconds: {seconds})\n",
                            inline=False)
            place += 1
        return embed

    def get_user_level(self, id):
        level = 0
        if id in self.player_info.keys():
            level = self.player_info[id]['level']

        return level

    def get_users_at_level(self, requested_level):
        return [id for id, info in self.player_info.items() if info['level'] == requested_level]

    def make_sure_player_info_is_initialized(self, id):
        if (not id in self.player_info.keys()):
            self.player_info[id] = {
                'level': 0,
                'time': 0
            }

    def save_data(self):
        with open('./bot.sav', 'w+') as f:
            data = {}
            data['player_info'] = self.player_info
            data['id_name_mappings'] = self.id_name_mappings
            json.dump(data, f)

    def load_data(self):
        try:
            with open('./bot.sav', 'r') as f:
                data = json.load(f)
                self.player_info = data['player_info']
                self.id_name_mappings = data['id_name_mappings']

                # convert string key to int key
                self.player_info = {int(id): key for id, key in self.player_info.items()}
                self.id_name_mappings = {int(id): key for id, key in self.id_name_mappings.items()}
        except FileNotFoundError:
            pass
