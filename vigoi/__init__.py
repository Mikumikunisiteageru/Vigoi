# vigoi/__init__.py

import argparse
import calendar
import codecs
import configparser
import datetime
import os

path = os.path.abspath(os.getcwd())
inipath = os.path.join(path, "vigoi.ini")
config = configparser.ConfigParser()
config.read(inipath, encoding="utf-8")

def findbook(date):
	if not config.has_section("PATH"):
		config.add_section("PATH")
	if not config.has_option("PATH", "format"):
		config.set("PATH", "format", "%%Y%%m_Accounts.yaml")
	fnfmt = config.get("PATH", "format")
	return date.strftime(fnfmt)

def newbook(date = datetime.date.today() + datetime.timedelta(days=3)):
	bookpath = findbook(date)
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

def main():
	parser = argparse.ArgumentParser(
		description = "Tools for creating or checking accounting books.", 
		usage = "vigoi [-h] [-n [YEAR MONTH]] [-x [YEAR MONTH]]")
	parser.add_argument("-n", "--new", nargs="*", metavar=("YEAR", "MONTH"), 
		help="make a new book (0 or 2 arguments)")
	parser.add_argument("-x", "--check", nargs="*", metavar=("YEAR", "MONTH"), 
		help="check a full book (0 or 2 arguments)")
	args = parser.parse_args()
	if (args.new is None) == (args.check is None):
		parser.print_help()
		return
	if not args.new is None:
		nargs = len(args.new)
		if nargs == 0:
			newbook()
		elif nargs == 2:
			try:
				y = int(args.new[0])
				m = int(args.new[1])
			except ValueError:
				raise TypeError(
					"Arguments following `-n` or `--new` must be integers!")
			newbook(datetime.date(y, m, 15))
		else:
			parser.print_help()
	with codecs.open(inipath, "w") as configfile:
		config.write(configfile)
