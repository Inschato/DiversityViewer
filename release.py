import os
import sys
import shutil
import py2exe
from distutils.core import setup

version = "0.3"
install_name = 'DiversityViewer-' + version

if os.path.isdir('target/'):
    shutil.rmtree('target/')
install_path = 'target/' + install_name + '/'

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

shutil.copytree('dist/', install_path)
for root, dirs, files in os.walk(install_path + 'tcl/tcl8.5/', topdown=False):
    for name in files:
        if name not in ['auto.tcl', 'init.tcl', 'tclIndex']:
            os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root,name))
shutil.rmtree(install_path + 'tcl/tk8.5/demos')
shutil.rmtree(install_path + 'tcl/tk8.5/images')
shutil.rmtree(install_path + 'tcl/tk8.5/msgs')

shutil.copytree('characters/', install_path + 'characters/')
shutil.copytree('collectibles/', install_path + 'collectibles/')
shutil.copy('README.md', install_path + "/README.txt")
shutil.copy('items.txt', install_path + "/items.txt")
shutil.copy('options.json', install_path + "/options.json")

shutil.make_archive("target/" + install_name, "zip", 'target', install_name + "/")