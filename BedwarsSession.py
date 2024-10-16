import json
import os
import requests
from time import sleep


api_key = "YOUR API KEY HERE" # get a new one at https://developer.hypixel.net/dashboard


username = "YOUR USERNAME HERE"
refresh_interval = 60 # Refresh interval in seconds, the API is slow so a faster refresh is not always useful


modes = [
	"",
	"eight_one_",
	"eight_two_",
	"four_three_",
	"four_four_",
	"two_four_"
]
statistics = [
	"kills_bedwars",
	"deaths_bedwars",
	"games_played_bedwars",
	"wins_bedwars",
	"losses_bedwars",
	"final_kills_bedwars",
	"final_deaths_bedwars",
	"beds_broken_bedwars",
	"beds_lost_bedwars"
]


while True:
	r = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
	minecraft_user_data = json.loads(r.text)
	minecraft_user_id = minecraft_user_data['id']

	r = requests.get(f'https://api.hypixel.net/player?key={api_key}&uuid={minecraft_user_id}')
	hypixel_user_data = json.loads(r.text)
	hypixel_user_data = hypixel_user_data["player"]["stats"]["Bedwars"]

	for mode in modes:
		for statistic in statistics:
			try:
				exec(f"{"STARTING" + mode + statistic} = {hypixel_user_data[mode + statistic]}")
			except KeyError:
				pass

	while True:
		sleep(refresh_interval)

		r = requests.get(f'https://api.hypixel.net/player?key={api_key}&uuid={minecraft_user_id}')
		hypixel_user_data = json.loads(r.text)
		hypixel_user_data = hypixel_user_data["player"]["stats"]["Bedwars"]

		os.system('cls')
		for mode in modes:
			for statistic in statistics:
				try:
					exec(f"{mode + statistic} = {hypixel_user_data[mode + statistic]}")
					exec(f"{mode + statistic} -= {"STARTING" + mode + statistic}")
				except KeyError:
					pass


		for mode in modes:
			if eval(mode + "games_played_bedwars") > 0:
				if mode == "":
					print("Overall")
				elif mode == "eight_one_":
					print("Solos")
				elif mode == "eight_two_":
					print("Duos")
				elif mode == "four_three_":
					print("Trios")
				elif mode == "four_four_":
					print("Squads")
				elif mode == "two_four_":
					print("4v4")
				print()

				print(f"Kills: {eval(mode + "kills_bedwars")}")
				print(f"Deaths: {eval(mode + "deaths_bedwars")}")
				try:
					print(f"KDR: {round(eval(mode + "kills_bedwars") / eval(mode + "deaths_bedwars"), 2)}")
				except ZeroDivisionError:
					print(f"KDR: {round(eval(mode + "kills_bedwars"), 2)}")
				print(f"Games Played: {eval(mode + "games_played_bedwars")}")
				print(f"Wins: {eval(mode + "wins_bedwars")}")
				print(f"Losses: {eval(mode + "losses_bedwars")}")
				try:
					print(f"WLR: {round(eval(mode + "wins_bedwars") / eval(mode + "losses_bedwars"), 2)}")
				except ZeroDivisionError:
					print(f"WLR: {round(eval(mode + "wins_bedwars"), 2)}")
				print(f"Final Kills: {eval(mode + "final_kills_bedwars")}")
				print(f"Final Deaths: {eval(mode + "final_deaths_bedwars")}")
				try:
					print(f"FKDR: {round(eval(mode + "final_kills_bedwars") / eval(mode + "final_deaths_bedwars"), 2)}")
				except ZeroDivisionError:
					print(f"FKDR: {round(eval(mode + "final_kills_bedwars"), 2)}")
				print(f"Beds Broken: {eval(mode + "beds_broken_bedwars")}")
				print(f"Beds Lost: {eval(mode + "beds_lost_bedwars")}")
				try:
					print(f"BBLR: {round(eval(mode + "beds_broken_bedwars") / eval(mode + "beds_lost_bedwars"), 2)}")
				except ZeroDivisionError:
					print(f"BBLR: {round(eval(mode + "beds_broken_bedwars"), 2)}")
				print("============================================")
