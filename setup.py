#!/usr/bin/env python
from distutils.core import setup
from distutils.sysconfig import get_python_lib
import sys
import os
from glob import glob

MAIN_VERSION = '0.4dev'

if os.system("bzr version-info --format=python > zgoubi/version.py") == 0:
	# run from a bzr repo, can use version info
	print "updated zgoubi/version.py"
	vfile = open("zgoubi/version.py","a")
else:
	vfile = open("zgoubi/version.py","w")
	vfile.write("#!/usr/bin/env python\n")
vfile.write("MAIN_VERSION = '%s'\n"%MAIN_VERSION)
vfile.close()


setup(name='pyzgoubi',
	version=MAIN_VERSION,
	packages=['zgoubi'],
	scripts=['pyzgoubi'],
	#package_data={'zgoubi': ['defs/*.py', 'defs/*.defs']},
	data_files=[('share/pyzgoubi/definitions',glob('defs/*')),
	            ('share/pyzgoubi/examples',glob('examples/*')),
	            ('share/pyzgoubi/test',glob('tests/*.py')),
	            ('share/pyzgoubi/doc', glob('doc/*'))
	            ]
	)

is_cygwin = False
if ("install" in sys.argv) and not ( "--help" in sys.argv):
	#find the log
	try:
		logfile = [x for x in sys.argv if x.startswith('--record')][-1]
		#strip away quotes, and expand path
		logfile = logfile.split('=')[-1].strip('"\'')
		logfile = os.path.expanduser(logfile)
	except IndexError:
		logfile = "install.log"

	try:
		for line in open(logfile):
			line = line.strip()
			if line.endswith("bin/pyzgoubi"):
				bin_path = os.path.dirname(line)
			if line.endswith("Scripts\pyzgoubi"):
				bin_path = line.rpartition('\\')[0]
				is_cygwin = True
			if line.endswith("zgoubi/__init__.py"):
				lib_path = os.path.normpath(os.path.join(os.path.dirname(line),".."))
			if line.endswith("zgoubi\__init__.py"):
				lib_path = line.rpartition('\\')[0].rpartition('\\')[0]
	except IOError:
		print "Could not see install log, install may have failed."
		print "Can't give help with setting up path"
		sys.exit(1)
		
	try:
		print "\nyou may need to add the following to your .bashrc"
		if is_cygwin:
			print "export PYTHONPATH=$PYTHONPATH:%s"%lib_path
			print "export PATH=$PATH:%s"%bin_path
			print "or"
			print 'alias pyzgoubi="PYTHONPATH=%s python %s\pyzgoubi"'%(lib_path, bin_path)
		else:
			print "export PYTHONPATH=$PYTHONPATH:%s"%lib_path
			print "export PATH=$PATH:%s"%bin_path
			print "or"
			print 'alias pyzgoubi="PYTHONPATH=%s python %s/pyzgoubi"'%(lib_path, bin_path)
			print 'alias pyzgoubii="PYTHONPATH=%s python -i %s/pyzgoubi"'%(lib_path, bin_path)
			print 'alias pyzgoubip="PYTHONPATH=%s python -m cProfile -o prof.log %s/pyzgoubi"'%(lib_path, bin_path)
	except NameError:
		print "Could not find all paths in logfile"


