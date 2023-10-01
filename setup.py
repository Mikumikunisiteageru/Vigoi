# setup.py

# import codecs
import setuptools

# with codecs.open("README.md", "r", "utf-8") as fin:
# 	longdescription = fin.read()

setuptools.setup(
	name = "vigoi",
	version = "0.0.1",
	author = "Yu-Chang YANG",
	author_email = "yang.yc.allium@gmail.com",
	description = "A tool to merge sequential PDFs",
	# long_description = longdescription,
	# long_description_content_type = "text/markdown",
	url = "https://github.com/Mikumikunisiteageru/Vigoi",
	packages = setuptools.find_packages(),
	entry_points = {
		"console_scripts": [
			"vigoi = vigoi:main",
		],
	},
	install_requires = [],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
