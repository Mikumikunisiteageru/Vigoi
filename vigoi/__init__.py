# vigoi/__init__.py

import argparse
import codecs
import configparser
import datetime
import os

from vigoi.new import newbookat
from vigoi.check import checkbookat

def configure(filename="vigoi.ini"):
	inipath = os.path.join(os.path.abspath(os.getcwd()), filename)
	config = configparser.ConfigParser()
	config.read(inipath, encoding="utf-8")
	if not config.has_section("PATH"):
		config.add_section("PATH")
	if not config.has_option("PATH", "book"):
		config.set("PATH", "book", "%%Y%%m_Accounts.yaml")
	if not config.has_option("PATH", "report"):
		config.set("PATH", "report", "")
	if not config.has_section("ACCOUNT"):
		config.add_section("ACCOUNT")
	if not config.has_option("ACCOUNT", "fakes"):
		config.set("ACCOUNT", "fakes", "[]")
	with codecs.open(inipath, "w") as fconfig:
		config.write(fconfig)
	return config

def nextdays(days=0):
	return datetime.date.today() + datetime.timedelta(days=days)

def newbook(date, config):
	bookpath = date.strftime(config.get("PATH", "book"))
	return newbookat(bookpath, date)

def main():
	config = configure()
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
			newbook(nextdays(3), config)
		elif nargs == 2:
			try:
				y = int(args.new[0])
				m = int(args.new[1])
			except ValueError:
				raise TypeError(
					"Arguments following `-n` or `--new` must be integers!")
			newbook(datetime.date(y, m, 15), config)
		else:
			parser.print_help()
