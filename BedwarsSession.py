from PIL import ImageTk, Image
import tkinter as tk
import urllib.request
import io
import json
import os
import requests
from time import sleep


api_key = "YOUR API KEY HERE" # get a new one at https://developer.hypixel.net/dashboard


username = "YOUR USERNAME HERE"
refresh_interval = 60 # Refresh interval in seconds, the API is slow so a faster refresh is not always useful
overall = False # this will display your overall stats if true, not your change during the session


width = 720
height = 405
skin_size = 125
gui_mode = "" # mode for the gui to display, see list of modes below, blank = overall


modes = {
	"":"Overall",
	"eight_one_":"Solos",
	"eight_two_":"Duos",
	"four_three_":"Trios",
	"four_four_":"Squads",
	"two_four_":"4v4"
}
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


def refresh_stats():
	# data refresh
	global first_refresh
	global hypixel_user_data
	if first_refresh:
		first_refresh = False
		for mode in modes:
			for statistic in statistics:
				try:
					exec(f"{mode + statistic} = {hypixel_user_data[mode + statistic]}")
					if overall == False:
						exec(f"{mode + statistic} -= {eval("STARTING" + mode + statistic)}")
				except KeyError:
					pass
	else:
		r = requests.get(f'https://api.hypixel.net/player?key={api_key}&uuid={minecraft_user_id}')
		updated_hypixel_user_data = json.loads(r.text)
		updated_hypixel_user_data = updated_hypixel_user_data['player']["stats"]["Bedwars"]

		for mode in modes:
			for statistic in statistics:
				try:
					exec(f"{mode + statistic} = {updated_hypixel_user_data[mode + statistic]}")
					if overall == False:
						exec(f"{mode + statistic} -= {eval("STARTING" + mode + statistic)}")
				except KeyError:
					pass

	# console output
	os.system('cls')
	for mode in modes:
		games_played = eval(f"{mode}games_played_bedwars")
		if games_played == None:
			games_played = 0
		if games_played > 0:
			print(modes[mode])
			print()

			kills = eval(f"{mode}kills_bedwars") or 0
			deaths = eval(f"{mode}deaths_bedwars") or 0
			wins = eval(f"{mode}wins_bedwars") or 0
			losses = eval(f"{mode}losses_bedwars") or 0
			final_kills = eval(f"{mode}final_kills_bedwars") or 0
			final_deaths = eval(f"{mode}final_deaths_bedwars") or 0
			beds_broken = eval(f"{mode}beds_broken_bedwars") or 0
			beds_lost = eval(f"{mode}beds_lost_bedwars") or 0

			print(f"Kills: {kills}")
			print(f"Deaths: {deaths}")
			kdr = kills / deaths if deaths > 0 else kills
			print(f"KDR: {round(kdr, 2)}")
			print(f"Games Played: {games_played}")
			print(f"Wins: {wins}")
			print(f"Losses: {losses}")
			wlr = wins / losses if losses > 0 else wins
			print(f"WLR: {round(wlr, 2)}")
			print(f"Final Kills: {final_kills}")
			print(f"Final Deaths: {final_deaths}")
			fkdr = final_kills / final_deaths if final_deaths > 0 else final_kills
			print(f"FKDR: {round(fkdr, 2)}")
			print(f"Beds Broken: {beds_broken}")
			print(f"Beds Lost: {beds_lost}")
			bblr = beds_broken / beds_lost if beds_lost > 0 else beds_broken
			print(f"BBLR: {round(bblr, 2)}")
			print("============================================")

			# gui output
			if mode == gui_mode:
				canvas.itemconfig(wins_text, text=f"{wins:,}")
				wlr = wins / losses if losses > 0 else wins
				canvas.itemconfig(wlr_stat_text, text=f"{wlr:.2f}")
				canvas.itemconfig(losses_text, text=f"{losses:,}")

				canvas.itemconfig(kills_text, text=f"{kills:,}")
				kdr = kills / deaths if deaths > 0 else kills
				canvas.itemconfig(kdr_stat_text, text=f"{kdr:.2f}")
				canvas.itemconfig(deaths_text, text=f"{deaths:,}")

				canvas.itemconfig(fkills_text, text=f"{final_kills:,}")
				fkdr = final_kills / final_deaths if final_deaths > 0 else final_kills
				canvas.itemconfig(fkdr_stat_text, text=f"{fkdr:.2f}")
				canvas.itemconfig(fdeaths_text, text=f"{final_deaths:,}")

				canvas.itemconfig(bbroken_text, text=f"{beds_broken:,}")
				bblr = beds_broken / beds_lost if beds_lost > 0 else beds_broken
				canvas.itemconfig(bblr_stat_text, text=f"{bblr:.2f}")
				canvas.itemconfig(blost_text, text=f"{beds_lost:,}")

	root.after(refresh_interval * 1000, refresh_stats)


# get data
r = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
minecraft_user_data = json.loads(r.text)
minecraft_user_id = minecraft_user_data['id']

r = requests.get(f'https://api.hypixel.net/player?key={api_key}&uuid={minecraft_user_id}')
hypixel_user_data = json.loads(r.text)
hypixel_user_data = hypixel_user_data['player']["stats"]["Bedwars"]

for mode in modes:
	for statistic in statistics:
		try:
			exec(f"{"STARTING" + mode + statistic} = {hypixel_user_data[mode + statistic]}")
		except KeyError:
			pass

for mode in modes:
	for statistic in statistics:
		try:
			exec(f"{mode + statistic} = {hypixel_user_data[mode + statistic]}")
			if overall == False:
				exec(f"{mode + statistic} -= {eval("STARTING" + mode + statistic)}")
		except KeyError:
			pass


# window
root = tk.Tk()
root.title("Bedwars Stats Display")

# background
background_image = Image.open("Assets/Background.png")
bg_image_resized = background_image.resize((width, height))
bg_image_tk = ImageTk.PhotoImage(bg_image_resized)

canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()
canvas.create_image(0, 0, image=bg_image_tk, anchor=tk.NW)

# skin
response = requests.get(f"https://mineskin.eu/armor/body/{minecraft_user_id}/{skin_size}.png")
img_data = response.content
img = Image.open(io.BytesIO(img_data))
image_from_url = ImageTk.PhotoImage(img)
canvas.create_image(width/2, height/2, image=image_from_url, anchor=tk.CENTER)

# stats
font = ("Impact", int((height/16 + width/9)/4))

canvas.create_text(width * .5, height * .9, text=f"{username}", font=font, fill="gold", justify="center")
if overall:
	canvas.create_text(width * .5, height * .1, text=f"Lifetime {modes[gui_mode]}", font=font, fill="gold", justify="center")
elif overall == False:
	canvas.create_text(width * .5, height * .1, text=f"Session {modes[gui_mode]}", font=font, fill="gold", justify="center")

column1 = width * .083
column2 = width * .125
column3 = width * .2
column4 = width * .8
column5 = width * .875
column6 = width * .917

row1 = height * .1
row2 = height * .25
row3 = height * .41
row4 = height * .56
row5 = height * .72
row6 = height * .87

wins_text = canvas.create_text(column2, row1, text=f"0", font=font, fill="forest green", justify="left")
wlr_text = canvas.create_text(column1, row2, text=f"WLR", font=font, fill="forest green", justify="left")
wlr_stat_text = canvas.create_text(column3, row2, text=f"0.00", font=font, fill="forest green", justify="left")
losses_text = canvas.create_text(column2, row3, text=f"0", font=font, fill="forest green", justify="left")

kills_text = canvas.create_text(column2, row4, text=f"0", font=font, fill="firebrick4", justify="left")
kdr_text = canvas.create_text(column1, row5, text=f"KDR", font=font, fill="firebrick4", justify="left")
kdr_stat_text = canvas.create_text(column3, row5, text=f"0.00", font=font, fill="firebrick4", justify="left")
deaths_text = canvas.create_text(column2, row6, text=f"0", font=font, fill="firebrick4", justify="left")

fkills_text = canvas.create_text(column5, row1, text=f"0", font=font, fill="dark slate blue", justify="right")
fkdr_text = canvas.create_text(column6, row2, text=f"FKDR", font=font, fill="dark slate blue", justify="right")
fkdr_stat_text = canvas.create_text(column4, row2, text=f"0.00", font=font, fill="dark slate blue", justify="right")
fdeaths_text = canvas.create_text(column5, row3, text=f"0", font=font, fill="dark slate blue", justify="right")

bbroken_text = canvas.create_text(column5, row4, text=f"0", font=font, fill="dodgerblue4", justify="right")
bblr_text = canvas.create_text(column6, row5, text=f"BBLR", font=font, fill="dodgerblue4", justify="right")
bblr_stat_text = canvas.create_text(column4, row5, text=f"0.00", font=font, fill="dodgerblue4", justify="right")
blost_text = canvas.create_text(column5, row6, text=f"0", font=font, fill="dodgerblue4", justify="right")


first_refresh = True
root.after(0, refresh_stats)

root.mainloop()
