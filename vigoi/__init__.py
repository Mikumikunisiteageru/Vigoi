# vigoi/__init__.py

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
	bookname = findbook(date)
	if os.path.isfile(bookname):
		raise FileExistsError(f"File `{bookname}` already exists!")
	weekday0, numdays = calendar.monthrange(date.year, date.month)
	with codecs.open(bookname, "w", "utf-8") as fout:
		for daym1 in range(numdays):
			weekday = (weekday0 + daym1) % 7 + 1
			day = daym1 + 1
			print('\t'.join(['+'*3, day, weekday, '+'*32]), end="\n\n\n",
				file=fout)
	return bookname

def main():
	print(inipath)
	findbook(datetime.date.today())
	with codecs.open(inipath, "w") as configfile:
		config.write(configfile)
	print(inipath)
