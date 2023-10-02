# vigoi/check.py

import codecs
import datetime
import re
import sys

class Cents:
	def __init__(self, arg):
		self.value = 0 if arg == "-" else round(100 * float(arg))
	def opposite(self):
		self.value = -self.value

class Line:
	def __init__(self, number, text):
		self.number = number
		self.text = text
		core = re.sub(r"(#|^\+{3,}).*", "", text).rstrip(" \t")
		if core == "":
			self.status = "empty"
			return
		r = re.match(r"^([^\t]*)\t([^\t]*)\t(.+)$", core)
		if r is None:
			raise ValueError("Line text malformed!")
		self.account = r.group(1)
		self.category = r.group(2)
		rest = r.group(3)
		if self.category.startswith("="):
			self.status = "section"
			self.cents = Cents(rest)
			if self.category == "=-":
				self.cents.opposite()
		else:
			ri = re.match(r"(\t?)[^\t]+\t(.+$)", rest)
			if ri.group(1) == "\t":
				if self.category == "":
					self.status = "empty"
					return
				else:
					self.status = "subitem"
			else:
				self.status = "item"
			self.cents = Cents(ri.group(2))

class Memory:
	def __init__(self):
		self.byaccount = {}
		self.bycategory = {}
	def pushaccount(self, line):
		self.byaccount.setdefault(line.account, [])
		self.byaccount[line.account].append(line)
	def pushcategory(self, line):
		self.bycategory.setdefault(line.category, [])
		self.bycategory[line.category].append(line)
	def getaccounts(self):
		return self.byaccount.keys()
	def getcategories(self):
		return self.bycategory.keys()

def eachredivide(lines, i, j, file=sys.stdout):
	# lines[i:j] constitute a group of subitems
	if i >= j:
		raise ValueError("Parental line (category `:`) not followed by filials!")
	for k in range(i, j):
		lines[k].account = lines[i-1].account
	sumcents = lines[i-1].cents.value
	subcents = [line.cents.value for line in lines[i:j]]
	if sumcents == sum(subcents):
		return
	# for k in range(i-1, j+1):
	# 	print(lines[k].number, lines[k].status, lines[k].cents.value)
	print(f"Redividing Line {lines[i-1].number} and filials,", 
		f"sum = {sumcents/100}:", file=file)
	print(f"\tBefore redividing: {[s/100 for s in subcents]}.", file=file)
	n = len(subcents)
	for k in range(1, n):
		subcents[k] += subcents[k-1]
	factor = sumcents / subcents[n-1]
	for k in range(0, n):
		subcents[k] = round(subcents[k] * factor)
	for k in range(n-1, 0, -1):
		subcents[k] -= subcents[k-1]
	print(f"\tAfter redividing: {[s/100 for s in subcents]}.", file=file)
	for (line, subcent) in zip(lines[i:j], subcents):
		line.cents.value = subcent
	# for k in range(i-1, j+1):
	# 	print(lines[k].number, lines[k].status, lines[k].cents.value)

def redivide(lines, file=sys.stdout):
	# ensure each group of subitems matches its parental item
	n = len(lines)
	i = 0
	while i < n:
		line = lines[i]
		if line.status == "item" and line.category == ":":
			j = i + 1
			while j < n and lines[j].status == "subitem":
				j += 1
			eachredivide(lines, i+1, j, file=file)
			i = j - 1
		i += 1

def balance(memory, account):
	if not account in memory.byaccount:
		return 0
	return sum(line.cents.value for line in memory.byaccount[account])

def addup(memory, category):
	if not category in memory.bycategory:
		return 0
	return sum(line.cents.value for line in memory.bycategory[category])

def checkbalance(memory, today, file=sys.stdout):
	print(file=file)
	unbalanced = 0
	for account in memory.getaccounts():
		delta = balance(memory, account)
		if delta != 0:
			unbalanced += 1
			print(account, delta / 100, file=file)
			for line in memory.byaccount[account]:
				print(f"\t[{line.number}]", line.text, file=file)
	if unbalanced == 0:
		print(file=file)
		print("#"*18, "Balance checked on", today, "#"*18, file=file)

def addupcategories(memory, today, file=sys.stdout):
	print(file=file)
	for category in sorted(memory.getcategories()):
		subsum = "%9.2f" % (addup(memory, category) / 100)
		print(f"#\t{category}\t{subsum}", file=file)
	print(file=file)
	print("#"*18, "Added up on", today, "#"*18, file=file)

def checkbookat(bookpath, fakeaccounts=[], file=sys.stdout):
	with codecs.open(bookpath, "r", "utf-8") as fin:
		lines = list(filter(lambda l: l.status != "empty", [Line(i, t) 
			for (i, t) in enumerate(fin.read().splitlines(), start=1)]))
	redivide(lines, file=file)
	# for (i, line) in enumerate(lines):
	# 	print(i, line.account, line.number, line.status, line.cents.value)
	memory = Memory()
	for line in lines:
		if not (line.status == "item" and line.category == ":"):
			memory.pushaccount(line)
		if line.status != "section":
			if line.category != ":" and not line.category in fakeaccounts:
				memory.pushcategory(line)
	date28hr = datetime.datetime.now() - datetime.timedelta(hours=4)
	today = date28hr.strftime("%Y%m%d")
	checkbalance(memory, today, file=file)
	addupcategories(memory, today, file=file)
