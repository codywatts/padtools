import codecs
import os
import re

from setuptools import setup, find_packages

NAME = "padtools"
PACKAGES = find_packages()
KEYWORDS = ["puzzle", "dragons", "pad"]
CLASSIFIERS = [
	"Development Status :: 2 - Pre-Alpha",
	"Environment :: Console",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
	"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
	"License :: OSI Approved",
	"Natural Language :: English",
	"Operating System :: OS Independent",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.3",
	"Programming Language :: Python :: 3.4",
	"Programming Language :: Python :: 3.5",
	"Programming Language :: Python",
	"Topic :: Games/Entertainment :: Puzzle Games",
	"Topic :: Games/Entertainment",
	"Topic :: Utilities",
]
INSTALL_REQUIRES = []

def read(*path_segments):
	full_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), *path_segments)
	with codecs.open(full_path, "rb", "utf-8") as f:
		return f.read()

META_FILE = read("padtools", "__init__.py")
META_REGEX = re.compile(r'__(?P<attribute>\w+)__\s*=\s*[ru]?(?P<quote>{single_quote}|"""|")(?P<value>.*)(?P=quote)'.format(single_quote="'"))
META_ATTRIBUTES = dict((match.group("attribute"), match.group("value")) for match in META_REGEX.finditer(META_FILE))

LONG_DESCRIPTION = read("README.rst")

if __name__ == "__main__":
	setup(
		author=META_ATTRIBUTES["author"],
		author_email=META_ATTRIBUTES["email"],
		classifiers=CLASSIFIERS,
		description=META_ATTRIBUTES["description"],
		include_package_data=True,
		install_requires=INSTALL_REQUIRES,
		keywords=KEYWORDS,
		license=META_ATTRIBUTES["license"],
		long_description=LONG_DESCRIPTION,
		maintainer=META_ATTRIBUTES["author"],
		maintainer_email=META_ATTRIBUTES["email"],
		name=NAME,
		packages=PACKAGES,
		platforms=["any"],
		url=META_ATTRIBUTES["uri"],
		version=META_ATTRIBUTES["version"],
		zip_safe=False,
	)