import time 
import subprocess
import os

host = '10.130.6.62'
port = 8888
crash_key = ['SIGSEGC', 'SIGILL', 'SIGABRT', 'crash']

def begin_fuzz(page_id):

	print("clear former log")
	# Clear is a byte type
	# Parent process communicate with child through pipe
	subprocess.Popen(['adb', 'logcat', '-c']).wait()

	# clear_stdout = clear.communicate()[0]

	# Accessing page
	output = subprocess.Popen(['adb', 'shell', 'am', 'start', 
		'-n', 'com.android.chrome/com.google.android.apps.chrome.Main',
		'-a', 'android.intent.action.VIEW',
        '-d', '"http://%s:%d/fuzz?%d"' % (host, port, page_id),
        '--es', '"com.android.browser.application_id"', '"com.android.browser"'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	# output_stderr = output.communicate()[1]
	# print("error:" + str(output_stderr, encoding = 'utf-8'))

	wait_time = 5
	print("wait for" + str(wait_time) + "seconds")
	time.sleep(wait_time)

	# Dump log
	log = subprocess.Popen(['adb', 'logcat', '*:I', '-d'],
		stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
	log_stdout = log.communicate()[0]

	return log_stdout



def fuzz_analysis(log, page_id):
	if any(i in str(log, encoding = 'utf-8') for i in crash_key):
		# Crash, save the crash log to crash folder
		crashfn = 'crash' + '/' + str(page_id)
		print("Crash! save log to %s.log"%crashfn)
		with open(crashfn + '.log', "wb") as f:
			f.write(log)

		# Copy the html file to crash folder
		src_html = 'test' + '/' + str(page_id) + '.html'
		dst_html = 'crash' + '/' + str(page_id) + '.html'
		copyfile(src_html, dst_html)
	else:
		# No crash, save the log file to non_crash folder
		non_crash = 'non_crash' + '/' + str(page_id)
		with open(non_crash + '.log', "wb") as f:
			f.write(log)


if __name__ == "__main__":
	page_id = 1
	while page_id < 0x100:
		log = begin_fuzz(page_id)
		fuzz_analysis(log, page_id)
		page_id = page_id + 1