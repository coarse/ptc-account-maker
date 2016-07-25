#!/usr/bin/python
import re
import time
import sys
import os
import json
import mechanize

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
print 'trying to make ' + limit + 'accounts'
count = 1
emails = getEmails(EMAIL)

while(True):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Firefox')]

	if (count > 1):
		print 'sleeping for 2 seconds...'
		time.sleep(2)

	print 'trying to open verification form...'
	try:
		br.open("https://club.pokemon.com/us/pokemon-trainer-club/sign-up/")
	except mechanize.HTTPError, e:
		print 'error occured! restarting attempt...'
		print e
		continue
	print 'success!'

	print 'filling up form...'
	br.select_form(name='verify-age')
	br.form['dob'] = DOB
	print 'success!'
	res = br.submit()
	print 'done submitting age verification!'

	if (br.geturl() != "https://club.pokemon.com/us/pokemon-trainer-club/parents/sign-up"):
		print 'something went wrong! shutting down lol'
		sys.exit(1)
	else:
		print 'success! moving to the next form...'

	print 'filling up form...'
	br.select_form(name='create-account')
	br.form['username'] = USERNAME + str(count)
	br.form['password'] = PASSWORD
	br.form['confirm_password'] = PASSWORD
	br.form['email'] = EMAIL
	br.form['confirm_email'] = ('.'*(count-1)) + EMAIL + '@gmail.com'
	br.form['public_profile_opt_in'] = ['False']
	br.form['terms'] = ['on']
	print 'success!'
	res = br.submit()
	print 'done submitting registration form!'

	if (br.geturl() != "https://club.pokemon.com/us/pokemon-trainer-club/parents/email"):
		print 'failed! continuing with next account'
	else:
		print 'success! created account' + USERNAME + str(count) + ":" + PASSWORD
		count = count + 1

	if (count > limit):
		break