import os
import sys
import shutil
import py2exe
from distutils.core import setup

version = "0.2.2"
installName = 'DiversityViewer-' + version

if os.path.isdir('target/'):
    shutil.rmtree('target/')
installDir = 'target/' + installName + '/'

sys.argv.append('py2exe')
setup(
    windows=['DiversitySeeds.py'],
    options={
        'py2exe': {
            'dll_excludes': ['w9xpopen.exe'],
            'excludes':['_ssl', 'difflib', 'doctest', 'locale', 'optparse', 'pickle',
                        'calendar', 'unittest', 'pdb','inspect', '_codecs', 'logging',
                        'PIL.BmpImagePlugin', 'PIL.GifImagePlugin', 'PIL.GimpGradientFile',
                        'PIL.GimpPaletteFile', 'PIL.JpegImagePlugin', 'PIL.PpmImagePlugin',
                        'PIL.ImageChops', 'PIL.ImageColor', 'PIL.ImageFile', 'PIL.ImageMode',
                        'PIL.PaletteFile', 'TiffImagePlugin', 'TiffTags', 'array', 'pyreadline',
                        'PaletteFile', 'BmpImagePlugin', 'GifImagePlugin', 'GimpGradientFile',
                        'GimpPaletteFile', 'ImageChops', 'JpegImagePlugin', 'PpmImagePlugin'],
            'optimize': 2,
            'bundle_files': 1
        }
    },
    zipfile=None
)

shutil.copytree('dist/', installDir)
for root, dirs, files in os.walk(installDir + 'tcl/tcl8.5/', topdown=False):
    for name in files:
        if name not in ['auto.tcl', 'init.tcl', 'tclIndex']:
            os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root,name))
shutil.rmtree(installDir + 'tcl/tk8.5/demos')
shutil.rmtree(installDir + 'tcl/tk8.5/images')
shutil.rmtree(installDir + 'tcl/tk8.5/msgs')

shutil.copytree('characters/', installDir + 'characters/')
shutil.copytree('collectibles/', installDir + 'collectibles/')
shutil.copy('README.md', installDir + "/README.txt")
shutil.copy('items.txt', installDir + "/items.txt")
shutil.copy('options.json', installDir + "/options.json")

shutil.make_archive("target/" + installName, "zip", 'target', installName + "/")