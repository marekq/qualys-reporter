# qualys-reporter
Download reports from Qualys for easy ingestion into a Splunk index.

Description
-----------

The qualys-reporter script can be used to automatically download CSV's from the Qualysguard web portal whenever they become available. The folder with downloaded CSV's can then be imported into Splunk so that new vulnerabilities can automatically be triaged using a Splunk dashboard or Splunk events. It seems Qualys is no longer maintaining their app on Splunkbase, so I decided to make a version which works better for me. I've configured the script to download reports once a day using a cronjob - these are then picked up by Splunk through folder monitoring. 

Comparison to Splunkbase app
----------------------------

Compared to the built in Splunk app on [Splunkbase](https://splunkbase.splunk.com/app/2964/#/overview), this script leverages the built in reports available on the Qualysguard console, which means you can tweak the level of detail and scope of the automated report using the webconsole which I find more convenient. The script also uses less web requests than the built in Splunk app which I found to be timing out very frequently. In addition, using this script, you can download the CSV's on a standalone or internet facing box and only forward the actually downloaded data to Splunk - it means your Splunk server can be standalone.

Installation
------------

You need the following Python libraries which you can retrieve using 'python-pip' or your OS repository.;

	$ pip install datetime qualysapi xmltodict

I've tested the script on Debian and OS X, but I expect other OS should work too. If you face difficulties, please let me know!

Once you run the script, it will check whether a '.qcrc' file exists in your current directory. This file contains your QualysGuard credentials in clear text (!!!), so ensure to keep it secure using file read permissions. 

Usage
-----

First off, ensure that there are reports ready on the [QualysGuard webpage](https://qualysguard.qualys.com/fo/report/report_list.php) for your account. You can schedule these to be created automatically on daily, weekly or monthly basis. Once a report is generated and shown on the webpage, you can go ahead and use this script. 

Next, simply run the command below to store any new CSV's in the /results folder. The CSV's are stored with the <reportid>_<report_creation_epoch>.csv syntax, which I find convenient for archiving and storage in Splunk. 

	$ python qualys-get.py

I've added the command to a cronjob so that new reports are automatically retrieved once they become available.  From what I can tell, its possible to schedule report delivery only once a day, but the script will skip downloading any old reports it already has on disk so feel free to check multiple times per day. 

If your server needs to connect to the Internet using an (un)authenticated webproxy, you can manually add proxy details to the .qcrc file - an example configuration can be found [here](https://github.com/paragbaxi/qualysapi#example-config-file). 

Contact
-------

For any questions or fixes, please reach out to @marekq!