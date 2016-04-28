#### DEPENDENCIES ####
## Python 2.7, with requests package installed
## Ghostscript installed in the environment
## An account that can hit the SQL report manager and use the http request API to download the report
## Install target printer in the environment (incl drivers and print prompt inclusion)
## Ability for account (user logged in and using task scheduler) to direct print

## Will want to add a batch file to have this execute from task scheduler. Make sure to map PYTHON and PYTHON_PATH or use path name in batch file

import requests, subprocess
from requests_ntlm import HttpNtlmAuth

# function to pull report using HTTP request from SQL Report Manager
# returns list with content and useful variable for naming if needed
def exec_dump(facility, cred_1, cred_2):
	url_string = ('http://SERVERNAME/ReportServer/Pages/ReportViewer.aspx?'
						'%2fFOLDERNAME%2f'
						'REPORTNAME'
						'&FACILITYPARAMETERNAME={fac_string}'
						'&rs:format=pdf').format(fac_string = facility)

	r = requests.get(url_string, auth = HttpNtlmAuth(cred_1,cred_2))
	return [facility,__name__,r]

# run the function to get response list
response_list = exec_dump('FACILITY_MNEMONIC','DOMAIN\\USERNAME','PASSWORD')

# (over)write the returned pdf file
f = open("to_printer.pdf", 'wb')
f.write(response_list[2].content)
f.close()

# execute ghostscript command to have printer print the pdf
subprocess.Popen([
	"C:\\Program Files\\gs\\gs9.19\\bin\\gswin64c.exe",
	'-dBATCH',
	'-dNOPAUSE',
	'-dNumCopies=1',
	'-sPAPERSIZE=a4',
	'-dFIXEDMEDIA',
	'-dPDFFitPage',
	'-sDEVICE=mswinpr2', 
	r'-sOutputFile=%printer%\\SERVERNAME\\PRINTERNAME', 
	'to_printer.pdf'], 
	stdout=subprocess.PIPE, 
	stderr=subprocess.STDOUT)