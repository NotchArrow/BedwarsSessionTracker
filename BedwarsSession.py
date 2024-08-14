import os
import time
from time import sleep

start_time = time.time()
auto_refresh = True
refresh_delay = 60
username = "YOUR_USERNAME_HERE"
log_path = "C:/Users/COMPUTER_USERNAME/AppData/Roaming/.minecraft/logs/latest.log"
fkdr_digits = 3

while True:

	file = open(log_path, "r")
	file_lines = file.readlines()

	final_kills = 0
	final_deaths = 0
	f_k_d_r = 0
	bed_breaks = 0
	games_played = 0
	games_won = 0

	for file_line in file_lines:
		if f"was {username}'s final " in file_line:
			final_kills += 1
			if final_deaths >= 1:
				f_k_d_r = final_kills / final_deaths
			else:
				f_k_d_r = final_kills
		elif username in file_line and "FINAL KILL!" in file_line:
			final_deaths += 1
			f_k_d_r = final_kills / final_deaths
		elif "Bed was bed #" in file_line and f"destroyed by {username}!" in file_line:
			bed_breaks += 1
		elif "Protect your bed and destroy the enemy beds." in file_line:
			games_played += 1
		elif "Nether Star!" in file_line:
			games_won += 1

	os.system('cls')
	print(f"Session Time: {time.strftime('%H:%M:%S', time.gmtime(int(time.time() - start_time)))}")
	print(f"Final Kills: {final_kills}")
	print(f"Final Deaths: {final_deaths}")
	print(f"FKDR: {round(f_k_d_r, fkdr_digits)}")
	print(f"Bed Breaks: {bed_breaks}")
	print(f"Games Played: {games_played}")
	print(f"Games Won: {games_won}")

	file.close()

	if auto_refresh:
		sleep(60)
	else:
		input("Press Enter To Refresh:")