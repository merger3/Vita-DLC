import requests
from time import sleep
import os
import json
import csv
from itertools import pairwise, chain
import os
import subprocess
import torf

tsvName = ""
tracker = ""

ID = 0
REGION = 1
NAME = 2
LINK = 3
ZRIF = 4
CONTENTID = 5

def main():
	names = {}
	with open("PSV_GAMES.tsv", 'r', encoding = 'utf-8') as n:
		nameLines = csv.reader(n, delimiter="\t")
		next(nameLines)
		for nl in nameLines:
			names[nl[ID]] = nl[NAME]
	seen = []
	my_env = os.environ.copy()
	subprocess.run(f'mkdir Torrents/', env=my_env, shell=True)
	subprocess.run(f'mkdir DLC/', env=my_env, shell=True)
	with open(f"{tsvName}.tsv", 'r', encoding = 'utf-8') as f:
		DLCs = csv.reader(f, delimiter="\t")
		next(DLCs)
		all_DLC = DLCs
		for DLC in all_DLC:
			if DLC[ID] not in seen:
				subprocess.run(f'mkdir "Torrents/{DLC[ID]} - {names[DLC[ID]]}"', env=my_env, shell=True)
				subprocess.run(f"nps_dlc.sh PSV_DLCS.tsv {DLC[ID]}", env=my_env, shell=True)
				seen.append(DLC[ID])

			filename = subprocess.run(f"bash -O extglob -c 'ls {DLC[ID]}_dlc/*{DLC[CONTENTID][DLC[CONTENTID].rfind('-') + 1:]}*'", env=my_env, shell=True, capture_output=True).stdout.decode("utf-8")[:-1].replace("\"", '')
			if filename == '':
				continue
			subprocess.run(f'mv "{filename}" DLC/', env=my_env, shell=True)
			newTorrent = torf.Torrent(f"DLC/{filename[filename.rfind('/') + 1:]}", trackers=[tracker], private=True)
			newTorrent.generate(threads=4)
			newTorrent.write(f'Torrents/{DLC[ID]} - {names[DLC[ID]]}/{filename[filename.rfind("/") + 1:].replace(".7z", ".torrent")}', validate=True, overwrite=True)

	subprocess.run("bash -O extglob -c 'rm -r *_dlc/'", env=my_env, shell=True)
main()
