import time 
import subprocess
import os

host = '10.130.6.62'
port = 8888
crash_key = ['SIGSEGC', 'SIGILL', 'SIGABRT', 'crash']

def begin_fuzz(page_id):

	print("clear former log")
	# clear is a byte type
	# parent process communicate with child through pipe
	clear = subprocess.Popen(['adb', 'logcat', '-c'], 
		stdout = subprocess.PIPE, stdeer = subprocess.STDOUT)

	# clear_stdout = clear.communicate()[0]

	# accessing page
	output = subprocess.(['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.VIEW',
        '-d', '"http://%s:%d/%s"' % (host, port, page_id)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output_stderr = output.communicate()[1]
	print("error:" + str(output_stderr, encoding = 'utf-8'))


	# dump log
	log = subprocess.Popen(['adb', 'logcat', '*:I', '-d'],
		stdout = subprocess.PIPE, stdeer = subprocess.STDOUT)
	log_stdout = log.communicate()[0]

	return log_stdout



def fuzz_analysis(log, page_id):
	if any(i in str(log, encoding = 'utf-8') for i in crash_key):
		crashfn = 'crashes' + '/' + page_id
		print("Crash! save log to %s.log"%crashfn)
		# crash then save the crash log
		# the html file has already been saved
		with open(crashfn + '.log', "wb") as f:
			f.write(log)
	else:




if __name__ == "__main__":
	page_id = 1
	while True:
		log = begin_fuzz(page_id)
		fuzz_analysis(log, page_id)
		page_id++