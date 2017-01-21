import requests
import os

JSESSIONID = "19FE45FFE2B09FE845162CAE5713E084"
POST_URL = "https://nes.nuance.mobi/middleware/uploads/sample/companies/ConUHacks/projects/projectid/619260"

def get_csv_files(dir):
    complete_dir = os.path.join("files/", dir + "/")
    return [os.path.join(complete_dir, f) for f in os.listdir(complete_dir)]

to_post_files = get_csv_files("to_post")

for post_file in to_post_files:
    print "-----------"
    print "Starting posting %s" % post_file

    file_t = {
        'file': open(post_file, 'rb')
    }
    sess_cookies = dict(JSESSIONID=JSESSIONID)
    r = requests.post(POST_URL, files=file_t, cookies=sess_cookies)

    if r.status_code == 200:
        dest_path = os.path.join("files/posted/", os.path.basename(post_file))
        os.rename(post_file, dest_path)
        print "200 OK - Moved %s to %s" % (post_file, dest_path)
    else:
        print "%d ERROR : %s" % (r.status_code, r.text)



#POST_URL = "https://nes.nuance.mobi/middleware/uploads/sample/companies/ConUHacks/projects/projectid/619260"
