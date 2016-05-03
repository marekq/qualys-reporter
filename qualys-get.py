#!/usr/bin/python
# @marekq
# www.marek.rocks

import qualysapi, xmltodict, datetime, time, os.path

folder		= os.getcwd()+'/results/'
resid		= []
result		= []

# check if the credential file ".qcrc" is in the cwd, else create it
def connect_api():
	print os.getcwd()+'/.qcrc'
	if not os.path.isfile(os.getcwd()+'/.qcrc'):

		# create the qcrc, enter your qualys credentials
		print 'creating .qcrc in '+folder+', enter your qualysguard credentials below;'
		qgs	= qualysapi.connect(remember_me=True)
	else:
		# connect using existing .qcrc
		qgs	= qualysapi.connect()

	# connect to the API and list reports as an XML
	ret 	= qgs.request('/api/2.0/fo/report', {'action': 'list'})
	root	= xmltodict.parse(ret)

	# iterate over available reports for your account, parse timestamps in epoch
	for x in root['REPORT_LIST_OUTPUT']['RESPONSE']['REPORT_LIST']['REPORT']:
		y1	= x['LAUNCH_DATETIME']
		y2	= datetime.datetime.strptime(str(y1), '%Y-%m-%dT%H:%M:%SZ').strftime('%s')

		z1	= x['EXPIRATION_DATETIME']
		z2	= datetime.datetime.strptime(str(z1), '%Y-%m-%dT%H:%M:%SZ').strftime('%s')

		a	= x['ID']+','+y1+','+y2+','+z1+','+z2+','+x['USER_LOGIN']+','+x['OUTPUT_FORMAT']+','+x['SIZE']
		print a
		result.append(str(a)+'\n')
		resid.append(int(x['ID']))

	print ''

	# check for reports that arent downloaded yet, else skip
	for x in resid:
		fname	= str(x)+'_'+str(y2)+'.csv'

		print 'checking '+str(folder)+str(fname)

		if not os.path.isfile(folder+fname):
			print 'downloading '+fname
			download_report(x, fname)
		else:
			print 'skipping '+fname
	
	# write an overview of report metadata to a csv
	f	= open(folder+'reports.csv', 'wb')
	for x in result:
		f.write(x+'\n')
	f.close

# download reports based on their ID value
def download_report(rid, fname):
	qgs	= qualysapi.connect()
	ret 	= qgs.request('/api/2.0/fo/report', {'action': 'fetch', 'id': rid})
	
	# write the report  as csv to disk with the id and timestamp in fname
	f	= open(str(folder+fname), 'wb')
	f.write(ret)
	f.close

### 

connect_api()
