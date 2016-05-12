import hashlib
import urllib
import schedule
import time
import pickle
import os.path

def job():

	urls = ["http://fbe.gazi.edu.tr/posts?type=news", "http://www.cs.hacettepe.edu.tr/lisansustu/", "http://www.cs.hacettepe.edu.tr/lisansustu/duyuru.html", "http://yyegm.meb.gov.tr/www/duyurular/kategori/2"]
	isFirstIteration = True
	if os.path.exists("pagecheckerhash"):
	    isFirstIteration = False

	hash_file = open("pagecheckerhash", "w+")

	if not isFirstIteration:
	    local_hashes = pickle.load(hash_file)
	else:
	    local_hashes = []
	    
	for i in range(0, len(urls)):
	    remote_data = urllib.urlopen(urls[i]).read()
	    remote_hash = hashlib.md5(remote_data).hexdigest()
	    print len(local_hashes)
	    if not isFirstIteration:
	        local_hash = local_hashes[i]
	        if remote_hash == local_hash:
	            print urls[i] + ' is NOT changed.'
	        else:
	            print urls[i] + ' is changed.'
	    else:
	        print "Created page hash for " + urls[i]

	    local_hashes.append(remote_hash)
	    
	pickle.dump(local_hashes, hash_file)

	hash_file.close()

job()
schedule.every().day.at("10:30").do(job)
schedule.every().day.at("17:15").do(job)
schedule.every().day.at("19:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
