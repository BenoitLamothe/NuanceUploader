import requests
import os
import sys
import re

def strip_twitter(str):
    # remove handles & hashtags
    str = re.sub(r"([@#])([a-z\d_]+)", "", str)
    str = re.sub(r"(https?|ftp)://[^\s/$.?#].[^\s]*", "", str)
    return str

JSESSIONID = "BFFC162DC9540160DAA2017501545E5D"
POST_URL = "https://nes.nuance.mobi/middleware/uploads/sample/companies/ConUHacks/projects/projectid/619260"
FIRST_LINE = 'transcription,count,intent,,'

read_file = open(sys.argv[1], 'r')
batch_size = 100
lines = []
batch_count = 0
with open(sys.argv[1], 'r') as readfile:
    readfilename = sys.argv[1]
    print "Working with %s" % (sys.argv[1])
    for line in readfile.readlines():
        if len(lines) % batch_size == 0:
            file_content = FIRST_LINE + '\n'
            file_content = file_content + ''.join(lines)
            filename = os.path.join('files/posted/', os.path.basename(readfilename).strip(".csv") + "_%d.csv" % batch_count)
            batch_count = batch_count + 1
            lines = []

            file(filename, 'w').write(file_content)
            file_t = {
                'file': open(filename, 'rb')
            }
            sess_cookies = dict(JSESSIONID=JSESSIONID)

            r = requests.post(POST_URL, files=file_t, cookies=sess_cookies)

            if r.status_code == 200:
                resp = r.json()
                if resp['status'] == "COMPLETED":
                    print "200 OK - Submitted %s" % filename
                else:
                    print "200 ERROR : %s" % resp['status']
                    print resp
            else:
                print "%d ERROR : %s" % (r.status_code, r.text)
        lines.append(strip_twitter(line))

#POST_URL = "https://nes.nuance.mobi/middleware/uploads/sample/companies/ConUHacks/projects/projectid/619260"

