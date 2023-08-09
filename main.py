from datetime import datetime

CARPARK_INFO_FILE = "carpark-information.csv"
CARPARK_INFO = []
OPTIONS = [
		f"Display Total Number of Caparks in '{CARPARK_INFO_FILE}'",
		f"Display All Basement Carparks in '{CARPARK_INFO_FILE}'",
		"Read Carpark Availability Data File",
		"Print Total Number of Carparks in the File Read in [3]",
		"Display Carparks Without Available Lots",
		"Display Carparks With At Least x% Available Lots",
		"Display Addresses of Carparks With At Least x% Available Lots",
		"Display All Carparks At Given Location",
		"Display Carpark With The Most Parking Lots",
		"Output Carpark Availability"
		]
CARPARK_AVAIL_INFO = []

def read_carpark_info(filename):
	data = []
	with open(filename, "r") as f:
		headers = f.readline()
		for i in f:
			i = i.strip("\n").split(',')
			info = {
				"Carpark Number": i[0],
				"Carpark Type": i[1],
				"Type of Parking System": i[2],
				"Address": i[3]
			}
			data.append(info)
		f.close()
	return data

def main_menu():
	SPACING = 6
	print("\nMENU\n====")
	for i in range(len(OPTIONS)):
		print(f"{f'[{i+1}]':<{SPACING}}{OPTIONS[i]}")
	print(f"{'[0]':<{SPACING}}EXIT")

# Display Total Number of Caparks
def display_total_carparks():
	print(f"{OPTIONS[0]}: {len(CARPARK_INFO)}")

# Display All Basement Carparks
def display_basement_carparks():
	headers = ["Carpark No", "Carpark Type", "Address"]
	print(f"{headers[0]:<11}{headers[1]:<15}{headers[2]}")
	count = 0
	for i in CARPARK_INFO:
		if "BASEMENT" in i["Carpark Type"]:
			count += 1
			print(f"{i['Carpark Number']:<11}{i['Carpark Type']:<15}{i['Address']}")
	print(f"Total Number: {count}")

# Read Carpark Availability Data File
def read_carpark_avail():
	global CARPARK_AVAIL_INFO
	CARPARK_AVAIL_INFO = []
	try:
		file = input("Enter the file name: ")
		with open(file, "r") as f:
			timestamp = f.readline()
			headers = f.readline()
			for i in f:
				i = i.strip('\n').split(',')
				info = {
					"Carpark Number": i[0],
					"Total Lots": int(i[1]),
					"Lots Available": int(i[2])
				}
				CARPARK_AVAIL_INFO.append(info)
			f.close()
		print(timestamp)
	except FileNotFoundError:
		print("[Error] File could not be found")

# Print Total Number of Carparks Available
def total_avail_carparks():
	print(f"Total Number of Carparks in the File: {len(CARPARK_AVAIL_INFO)}")

# Display Carparks Without Available Lots
def carpark_without_avail():
	count = 0
	print(CARPARK_AVAIL_INFO)
	for i in CARPARK_AVAIL_INFO:
		if i["Lots Available"] == 0:
			print(f"Carpark: {i['Carpark Number']}")
			count += 1
	print(f"Total number: {count}")

# find address using carpark number
def find_addr_from_num(num):
	for i in CARPARK_INFO:
		if i["Carpark Number"] == num:
			return i["Address"]
	return ""

# Display Carparks With At Least x% Available Lots
def display_carpark_percent_lots(address):
	try:
		count = 0
		percent = int(input("Enter the percentage required: "))
		print(f"{'Carpark No':<15}{'Total Lots':<15}{'Lots Available':<15}{'Percentage':<15}", end="")
		if address:
			print(f"{'Address':<15}")
		else:
			print()
		for i in CARPARK_AVAIL_INFO:
			try:
				lots_percent = (i["Lots Available"]/i["Total Lots"]) * 100
				if lots_percent >= percent:
					print(f"{i['Carpark Number']:<15}{i['Total Lots']:<15}{i['Lots Available']:<15}{round(lots_percent, 1):<15}", end="")
					if address:
						print(f"{find_addr_from_num(i['Carpark Number']):<15}")
					else:
						print()
					count += 1
			except ZeroDivisionError:
				pass
		print(f"Total number: {count}")
	except ValueError:
		print("[Error] Invalid Input")

# Display All Carparks At Given Location
def display_carpark_loc():
	loc = input("Enter Location: ")
	cp = []
	count = 0
	for i in CARPARK_INFO:
		if loc.upper() in i["Address"]:
			cp.append(i["Carpark Number"])

	if len(cp) == 0:
		print("No Carparks Found")
		return

	print(f"{'Carpark No':<15}{'Total Lots':<15}{'Lots Available':<15}{'Percentage':<15}{'Address':<15}")
	for i in CARPARK_AVAIL_INFO:
		try:
			lots_percent = (i["Lots Available"]/i["Total Lots"]) * 100
			if i['Carpark Number'] in cp:
				print(f"{i['Carpark Number']:<15}{i['Total Lots']:<15}{i['Lots Available']:<15}{round(lots_percent, 1):<15}{find_addr_from_num(i['Carpark Number']):<15}")
				count += 1
		except ZeroDivisionError:
			pass
	print(f"Total number: {count}")

# Display Carpark With The Most Parking Lots
def display_most_lots():
	print(f"{'Carpark No':<15}{'Total Lots':<15}{'Lots Available':<20}{'Carpark Type':<30}{'Type of Parking System':<30}{'Address':<15}")
	most = {'Lots Available': 0}
	for i in CARPARK_AVAIL_INFO:
		if i['Lots Available'] > most['Lots Available']:
			most = i

	info = {}
	for i in CARPARK_INFO:
		if i['Carpark Number'] == most['Carpark Number']:
			info = i
			break
	print(f"{most['Carpark Number']:<15}{most['Total Lots']:<15}{most['Lots Available']:<20}{info['Carpark Type']:<30}{info['Type of Parking System']:<30}{info['Address']:<15}")

def quick_sort_carpark(ls):
	def partition(ls, a, b):
		pivot = ls[b]
		i = a - 1
		for j in range(a, b):
			if ls[j]['Lots Available'] <= pivot['Lots Available']:
				i = i + 1
				(ls[i], ls[j]) = (ls[j], ls[i])
		(ls[i + 1], ls[b]) = (ls[b], ls[i + 1])
		return i + 1
	 
	def quickSort(ls, a, b):
		if a < b:
			pi = partition(ls, a, b)
			quickSort(ls, a, pi - 1)
			quickSort(ls, pi + 1, b)

	quickSort(ls, 0, len(ls) -1)
	return ls

# Output carpark availability
def out_carpark_avail():
	timestamp = f"Timestamp: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S%Z')}"
	filename = "carpark-availability-with-addresses.csv"
	headers = "Carpark Number,Total Lots,Lots Available,Address"
	data = []
	for i in CARPARK_AVAIL_INFO:
		i["Address"] = find_addr_from_num(i['Carpark Number'])
		data.append(i)

	data = quick_sort_carpark(data)
	with open(filename, 'w') as f:
		f.write(f"{timestamp}\n")
		f.write(headers)	
		for i in data:
			f.write(f"{i['Carpark Number']},{i['Total Lots']},{i['Lots Available']},{i['Address']}\n")
		f.close()
	print(f"{len(data)} Lines written - {filename}")


def select_option():
	try:
		option = int(input("Enter your option: "))
		if option == 0:
			exit()

		elif option == 1:
			display_total_carparks()

		elif option == 2:
			display_basement_carparks()

		elif option == 3:
				read_carpark_avail()

		elif option in [4, 5, 6, 7, 8, 9, 10]:
			if not len(CARPARK_AVAIL_INFO):
				print("Please select a file in [3]")
			else:
				if option == 4:
					total_avail_carparks()
				elif option == 5:
					carpark_without_avail()
				elif option == 6:
					display_carpark_percent_lots(False)
				elif option == 7:
					display_carpark_percent_lots(True)
				elif option == 8:
					display_carpark_loc()
				elif option == 9:
					display_most_lots()
				elif option == 10:
					out_carpark_avail()

		else:
			print("Select a valid option")


	except ValueError:
		print("[Error] Please select a valid option")

def main():
	main_menu()
	select_option()

if __name__ == "__main__":
	run = True
	CARPARK_INFO = read_carpark_info(CARPARK_INFO_FILE)

	while run:
		main()