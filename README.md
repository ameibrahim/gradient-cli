Paperspace API for Python
=========================

Sample usage
============
1. Make sure you have a Paperspace account set up. Go to http://paperspace.com
   to register.

2. Send an email message to support@paperspace.com to request access to the
   Paperspace API Beta program.

   Wait for an email confirmation indicating your account has been approved
   before proceeding.

3. Use pip or pipenv to install the paperspace-python package:

    pip install paperspace

4. Download your api key by executing the following:

    python -m paperspace.login

  Follow the prompts to enter your Paperspace email and password.

  You can also enter your credentials directly on the command line as follows:

    python -m paperspace.login <email> <password> [<api_token_name>]

  Note: your api key is cached in ~/.paperspace/config.json
  You can remove your cached api key by executing:

    python -m paperspace.logout

5. Execute the sample script hello.py:

    python hello.py

  The script will be run on the remote job cluster node, and its output will be
  logged locally.


A slightly more complex example
===============================
# tests/test_remote.py
import os
import paperspace

paperspace.jobs.runas_job({'project': 'myproject', 'machineType': 'GPU+', 'container': 'Test-Container'})

print(os.getcwd())
print('something useful')


Other examples
==============
See the scripts in the test folder for other examples.


Other Authentication options
============================
1. Specify your apiKey explicitly on any of the paperspace.jobs methods, e.g.:

    paperspace.jobs.create({'apiKey': '1qks1hKsU7e1k...', 'project': 'myproject', 'machineType': 'GPU+', 'container': 'Test-Container'})

2. Set the package paperspace.config option in your python code:

    paperspace.config.PAPERSPACE_API_KEY = '1qks1hKsU7e1k...'


3. Set the PAPERSPACE_API_KEY environment variable:

    (on linux:) export PAPERSPACE_API_KEY=1qks1hKsU7e1k...

  Note: the above methods take precedence over use of the cached api key in
   ~/.paperspace/config.json

Contributing
============

Want to contribute?  Contact us at hello@paperspace.com
