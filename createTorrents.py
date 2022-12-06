import os
import csv
from itertools import pairwise, chain
import os
import subprocess
import torf

tsvName = os.environ['TSV']
tracker = os.environ['ANNOUNCE']

fullNames = {'US': 'USA', 'EU': 'Europe', 'JP': 'Japan', 'ASIA': 'Asia'}

ID = 0
REGION = 1
NAME = 2
LINK = 3
ZRIF = 4
CONTENTID = 5

def main():
	os.chdir("/output")
	names = {}
	regions = {}
	with open(f"{os.environ['HOME']}/PSV_GAMES.tsv", 'r', encoding = 'utf-8') as n:
		nameLines = csv.reader(n, delimiter="\t")

		for nl in nameLines:
			names[nl[ID]] = nl[NAME].replace('/', '|')
			regions[nl[ID]] = nl[REGION]
	seen = []
	my_env = os.environ.copy()
	subprocess.run('mkdir /output/Torrents/', env=my_env, shell=True)
	subprocess.run('mkdir /output/DLC/', env=my_env, shell=True)
	with open(f"/output/{tsvName}.tsv", 'r', encoding = 'utf-8') as f:
		DLCs = csv.reader(f, delimiter="\t")
		all_DLC = DLCs
		for DLC in all_DLC:
			if DLC[ID] not in seen:
				subprocess.run(f'mkdir "/output/Torrents/{DLC[ID]} - {names[DLC[ID]]}"', env=my_env, shell=True)
				subprocess.run(f"nps_dlc.sh ${{HOME}}/PSV_DLCS.tsv {DLC[ID]}", env=my_env, shell=True)
				seen.append(DLC[ID])

			filename = subprocess.run(f"bash -O extglob -c 'ls /output/{DLC[ID]}_dlc/*{DLC[CONTENTID][DLC[CONTENTID].rfind('-') + 1:]}*'", env=my_env, shell=True, capture_output=True).stdout.decode("utf-8")[:-1].replace("\"", '')
			if filename == '':
				continue
			subprocess.run(f'mv "{filename}" DLC/', env=my_env, shell=True)
			newTorrent = torf.Torrent(f"DLC/{filename[filename.rfind('/') + 1:]}", trackers=[tracker], private=True)
			newTorrent.generate(threads=4)
			replaceString = f" [{fullNames[regions[DLC[ID]]]}].torrent"
			newTorrent.write(f'/output/Torrents/{DLC[ID]} - {names[DLC[ID]]}/{filename[filename.rfind("/") + 1:].replace(".7z", replaceString)}', validate=True, overwrite=True)
	subprocess.run("bash -O extglob -c 'rm -r *_dlc/'", env=my_env, shell=True)
	subprocess.run(f'chmod -R 777 /output', env=my_env, shell=True)

main()
