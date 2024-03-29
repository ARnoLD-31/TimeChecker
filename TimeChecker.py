# -*- coding: utf-8 -*-
import configparser
import os
import time
import datetime

def cls():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

def set_time():
	to_leave = False
	print("Set time. Ex: 14:50, 03:34. Or use empty string to set current time")
	while True:
		time = input(">>> ")
		if time == "":
			time = datetime.datetime.now().strftime("%H:%M")
			break
		for element in time:
			if not element.isdigit() and not element == ":":
				to_leave = True
				break
		if to_leave:
			to_leave = False
			continue
		elif len(time) == 5 and time[2] == ":":
			break
	print("Set date. Ex: 13.03.2024, 01.03.2024. Or use empty string to set current date")
	while True:
		date = input(">>> ")
		if date == "":
			date = datetime.datetime.now().strftime("%d.%m.%Y")
			break
		for element in date:
			if not element.isdigit() and not element == ".":
				to_leave = True
				break
		if to_leave:
			to_leave = False
			continue
		if len(date) == 10 and date[2] == "." and date[5] == "." and date[2] == ".":
			break
	print(f"Done. {time + ' ' + date}")
	return time + " " + date

def during(first, second):
	first = datetime.timedelta(days=int(first[6:8]), hours=int(first[:2]), minutes=int(first[3:5]))
	second = datetime.timedelta(days=int(second[6:8]), hours=int(second[:2]), minutes=int(second[3:5]))
	return first - second

def start_activity(type_of):
	cls()
	start_time = set_time()
	records[int(index_records) + 1] = {
		"Type": type_of,
		"Start_time": start_time,
		"End_time": ""}
	with open("records.ini", "w") as records_file:
		records.write(records_file)
	time.sleep(2)
	main()

def statistic_dbd():
	cls()
	picked = []
	index = 0
	try:
		while True:
			current_month = records[str(index)]["Start_time"][9:11]
			if not current_month in picked:
				picked.append(current_month)
			index += 1
	except:
		pass
	if len(picked) == 1:
		month = picked[0]
	else:
		print("Choose the month: ")
		index = 0
		for element in picked:
			print(f"[{index + 1}] - {element}")
			index += 1
		while True:
			try:
				choose = int(input(">>> "))
				month = picked[choose - 1]
				break
			except:
				pass
	picked = []
	index = 0
	try:
		while True:
			current_day = records[str(index)]["Start_time"][6:8]
			temp_month = records[str(index)]["Start_time"][9:11]
			if not current_day in picked and month == temp_month:
				picked.append(current_day)
			index += 1
	except:
		pass
	print("Choose the day: ")
	index = 0
	for element in picked:
		print(f"[{index + 1}] - {element}")
		index += 1
	while True:
		try:
			choose = int(input(">>> "))
			day = picked[choose - 1]
			break
		except:
			pass
	day_indexes = []
	type_time = {}
	index = 0
	try:
		while True:
			if records[str(index)]["Start_time"][6:8] == day and records[str(index)]["Start_time"][9:11] == month:
				day_indexes.append(str(index))
			index += 1
	except:
		pass
	for index in day_indexes:
		if not records[index]["Type"] in type_time.keys():
			type_time[records[index]["Type"]] = during(records[index]["End_time"], records[index]["Start_time"])
		else:
			type_time[records[index]["Type"]] += during(records[index]["End_time"], records[index]["Start_time"])
	cls()
	print(f"Statistic for {day}.{month}:")
	summary = datetime.timedelta()
	for element in type_time.keys():
		print(f"{element} - {type_time[element]} {int(type_time[element] / datetime.timedelta(hours=24) * 100)}%")
		summary += type_time[element]
	print(f"Other - {datetime.timedelta(hours=24) - summary} {int((datetime.timedelta(hours=24) - summary) / datetime.timedelta(hours=24) * 100)}%")
	print("Press any key to return to the main menu: ")
	input(">>> ")
	main()
		
	
	

def statistic_main():
	cls()
	is_first = True
	for index in range(0, int(index_records) + 1):
		current_time = records[str(index)]["Start_time"][6:8]
		current_month = records[str(index)]["Start_time"][9:11]
		try:
			next_time = records[str(index + 1)]["Start_time"][6:8]
			next_month = records[str(index + 1)]["Start_time"][9:11]
		except:
			next_month = current_month
			next_time = current_time
		if is_first or f"{current_month}{current_time}" != f"{next_month}{next_time}":
			print(f'{records[str(index)]["Start_time"][6:8]} {current_month}: ')
			if is_first:
				print("   ---------------------------------------------------")
			is_first = False
		start_time = records[str(index)]["Start_time"][0:5]
		end_time = records[str(index)]["End_time"][0:5]
		during_var = during(records[str(index)]["End_time"], records[str(index)]["Start_time"])
		percentage = round(during_var / datetime.timedelta(days=1) * 100, 2)
		print(f'  |   {records[str(index)]["Type"]}')
		print(f'  |     Start time - {start_time}')
		print(f'  |     End time - {end_time}')
		print(f'  |     During - {during_var}')
		print(f'  |     Percentage - {percentage}% of 24H')
		print("   ---------------------------------------------------")
	print("Press any key to return to the main menu: ")
	input(">>> ")
	main()

def statistic():
	cls()
	if index_records == "-1":
		print("There isn't any statistic yet!")
		time.sleep(2)
		main()
	print("Do you want [D]ay by day or [M]ain statistic?")
	while True:
		choose = input(">>> ")
		if choose.lower() == "d":
			statistic_dbd()
		elif choose.lower() == "m":
			statistic_main()
	

def main():
	global index_records, records
	cls()
	types = ["OGE", "School", "Programming", "Sleeping", "Homework", "Games"]
	try:
		os.stat("records.ini").st_size
	except:
		file = open("records.ini", "w")
		file.write("")
	records = configparser.ConfigParser()
	records.read("records.ini")
	index_records = 0
	try:
		records[str(index_records)]
		while True:
			index_records += 1
			records[str(index_records)]
	except:
		index_records -= 1
	index_records = str(index_records)
	if index_records == "-1" or records[index_records]["End_time"] != "":
		print("Choose the activity type: ")
		print("[E] - EXIT")
		print("[0] - STATISTICS")
		for index in range(len(types)):
			print(f"[{index + 1}] - {types[index]}")
		while True:
			choose = input(">>> ")
			if choose.lower() == "e":
				quit(0)
			try:
				int(choose)
			except:
				continue
			if int(choose) == 0:
				statistic()
			elif int(choose) <= len(types):
				start_activity(types[int(choose) - 1])
	else:
		print(f'Your last activity "{records[index_records]["Type"]} - {records[index_records]["Start_time"]}" is not end. Do you want to add End time? [Y/N]')
		while True:
			choose = input(">>> ")
			if choose.lower() == "y":
				end_time = set_time()
				records[index_records]["End_time"] = end_time
				with open("records.ini", "w") as records_file:
					records.write(records_file)
				time.sleep(2)
				main()
			elif choose.lower() == "n":
				quit(0)
main()
