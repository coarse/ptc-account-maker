#!/usr/bin/python
import re
import time
import sys
import os
import json
from mechanize import Browser

def getEmails(email):
	emails = []
	# do the thing to get the array of emails
	return emails

with open('credentials.json') as f:
	credentials = json.load(f)

DOB = credentials.get('dob', None)
USERNAME = credentials.get('username', None)
PASSWORD = credentials.get('password', None)
EMAIL = credentials.get('email', None)

if len(sys.argv) == 1:
	print 'input number of accounts to generate'
	sys.exit(1)

limit = sys.argv[1]
count = 1
emails = getEmails(EMAIL)

while(True):
	time.sleep(2)
	br = Browser()
	br.set_handle_robots( False )
	br.addheaders = [('User-agent', 'Firefox')]

	br.open("https://club.pokemon.com/us/pokemon-trainer-club/sign-up/")
	br.select_form(name='verify-age')
	br.form['dob'] = DOB
	res = br.submit()
	print 'done submitting age verification!'

	br.select_form(name='create-account')
	br.form['username'] = USERNAME + str(count)
	br.form['password'] = PASSWORD
	br.form['confirm_password'] = PASSWORD
	br.form['email'] = EMAIL
	br.form['confirm_email'] = ('.'*(count-1)) + EMAIL + '@google.com'
	br.form['public_profile_opt_in'] = ['False']
	br.form['terms'] = ['on']
	res = br.submit() # submit
	print 'done submitting !'
	# time.sleep(5) # idk if this is needed
	content = res.read()

	with open("results.html", "a") as f:
	    f.write(content)

	if (br.geturl() != "https://club.pokemon.com/us/pokemon-trainer-club/parents/email"):
		print 'failed! continuing with next account'
	else:
		print 'success! created account' + USERNAME + str(count) + ":" + PASSWORD
		count = count + 1

	if (count > limit):
		break