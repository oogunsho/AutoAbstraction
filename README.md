# AutoAbstraction
The app automate the extraction of key words and abstracts from documents.

Uncompress and enter the file to access the code for the app.

Starting

Before Kivy can be installed, Python and pip needs to be pre-installed, please go online to search for how to install them and install the newest versions if possible (python 3.0+ at least, 2.7 is no longer supported) (newer pythons do not even need you to download pip or virtuale nv). Then, start a new terminal that has Python available.

How to install python is at the website below:

https://realpython.com/installing-python/

Installing pip (if you do not have it)

python get-pip.py

Setup terminal and pip¶

In the terminal, update pip and other installation dependencies so you have the latest version as follows (for linux users you may have to substitute python3 instead of python and also add a --user flag in the subsequent commands outside the virtual environment):

python -m pip install --upgrade pip setuptools virtualenv

Create virtual environment¶

Create a new virtual environment for your Kivy project. A virtual environment will prevent possible installation conflicts with other Python versions and packages. It’s optional but strongly recommended:

Create the virtual environment named kivy_venv in your current directory:

python -m virtualenv kivy_venv

Activate the virtual environment.

You will have to do this step from the current directory every time you start a new terminal. This sets up the environment so the new kivy_venv Python is used.

For Windows default CMD, in the command line do:

kivy_venv\Scripts\activate

If you are in a bash terminal on Windows, instead do:

source kivy_venv/Scripts/activate

If you are in linux, instead do:

source kivy_venv/bin/activate

Your terminal should now preface the path with something like (kivy_venv), indicating that the kivy_venv environment is active. If it doesn’t say that, the virtual environment is not active and the following won’t work.

Install Kivy¶

Finally, install Kivy using one of the following options:

Pre-compiled wheels¶

The simplest is to install the current stable version of kivy and optionally kivy_examples from the kivy-team provided PyPi wheels. Simply do:

python -m pip install kivy[base] kivy_examples

This also installs the minimum dependencies of Kivy. To additionally install Kivy with audio/video support, install either kivy[base,media] or kivy[full]. See Kivy’s dependencies for the list of selectors.

Install all dependencies:

python -m pip install pypandoc pdfminer ntlk rake-ntlk

To run the app:

python app.py

NOTE: Everything activate virtual environment should be done in the virtual environment to make sure the installations do not mess with you laptop.

After following the instructions you just need to make sure the virtual environment is activated before you run the app.
