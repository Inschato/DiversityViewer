# This build script requires two non-standard python libraries:
#
# You can install both using the pip commands:
# pip install pillow
# pip install pyinstaller
#
# pyinstaller should be in your system path to work correctly,
# which it will be in a default python configuration.

import os
import shutil
import subprocess


version = "0.5"
install_name = 'DiversityViewer-' + version

if os.path.isdir('target/'):
    shutil.rmtree('target/')
install_path = 'target/' + install_name + '/'

subprocess.call(['pyinstaller', '--onefile', '--windowed', 'DiversitySeeds.py'])

shutil.copytree('dist/', install_path)
shutil.copytree('collectibles/', install_path + 'collectibles/')
shutil.copy('README.md', install_path + "/README.txt")
shutil.copy('items.txt', install_path + "/items.txt")
shutil.copy('options.json', install_path + "/options.json")

shutil.make_archive("target/" + install_name, "zip", 'target', install_name + "/")