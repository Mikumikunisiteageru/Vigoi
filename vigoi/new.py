# vigoi/new.py

import calendar
import codecs
import datetime
import os

def newbookat(bookpath, date):
	if os.path.isfile(bookpath):
		raise FileExistsError(f"File `{bookpath}` already exists!")
	weekday0, numdays = calendar.monthrange(date.year, date.month)
	with codecs.open(bookpath, "w", "utf-8") as fout:
		print(f"# {os.path.split(bookpath)[1]}", end="\n\n", file=fout)
		for day in range(numdays + 1):
			weekday = -1 if day == 0 else (weekday0 + day - 1) % 7 + 1
			print('\t'.join(['+'*3, str(day), str(weekday), '+'*32]), 
				end="\n\n\n", file=fout)
	print(f"New book `{bookpath}` created.")
	os.system(f"start {bookpath}")
