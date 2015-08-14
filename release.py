import os, sys, shutil, py2exe
from distutils.core import setup

version = "0.1"
installName = 'DiversityViewer-' + version

if os.path.isdir('target/'):
  shutil.rmtree('target/')
installDir = 'target/' + installName + '/'

sys.argv.append('py2exe')
setup(
	windows = ['DiversitySeeds.py'],
	options = {
		'py2exe': {
			'dll_excludes': ['w9xpopen.exe']
		}
	}
)

shutil.copytree('dist/', installDir)
shutil.copytree('characters/', installDir + 'characters/')
shutil.copytree('collectibles/', installDir + 'collectibles/')
shutil.copy('README.md', installDir+"/README.txt")
shutil.copy('items.txt', installDir+"/items.txt")

shutil.make_archive("target/" + installName, "zip", 'target', installName + "/")