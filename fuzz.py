import time
import subprocess
import os

host = '10.130.6.62'
port = 8888
def start_fuzzing():
    clear_logcat()
    tmpuri = 'fuzzyou?id=%d' % time.time()
    print("fuzz %s" % tmpuri)

    # ouput = subprocess.Popen(['adb', 'shell', 'am', 'start',
    #                         '-n', 'com.chrome.beta/com.google.android.apps.chrome.Main', 
    #                         '-a', 'android.intent.action.VIEW',
    #                         '-d', 'http://%s:%d/%s' % (host, port, tmpuri)
    # ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    ouput = subprocess.Popen(['adb', 'shell', 'am', 'start',
                            '-n', 'com.android.chrome/com.google.android.apps.chrome.Main', 
                            '-a', 'android.intent.action.VIEW',
                            '-d', 'http://%s:%d/%s' % (host, port, tmpuri)
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    wait_time = 30
    print("wait for" + str(wait_time) +"seconds")
    time.sleep(wait_time)

    print("check log")
    check_logcat(tmpuri)

def clear_logcat():
    subprocess.Popen(['adb', 'logcat', '-c']).wait()

def check_logcat(tmpuri):
    log = subprocess.Popen(['adb', 'logcat', '*:I', '-d'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).communicate()[0]
    # if log.find('SIGSEGV') != -1:
    crash_identifers = ['SIGSEGV', 'SIGFPE', 'SIGILL','crash']
    # path = 'C:/Users/lenovo/Desktop/fuzzing/android_browser_fuzz(easy)/android-browser-fuzz'
    if any(i in str(log, encoding = 'utf-8') for i in crash_identifers):
        crashfn = 'crashes' + '/' + tmpuri[8:]
        #os.path.join(path, 'crashes', tmpuri)
        print(" Crash!! save page/log to %s" % crashfn)
        #with open(crashfn, "wb") as f:
        #    f.write(self.server.page)
        with open(crashfn + '.log', "wb") as f:
            f.write(log)
    else:
        crashfn = 'non-crashes' + '/' + tmpuri[8:]
        print(crashfn)
        #os.path.join(path, 'non-crashes', tmpuri)
        with open(crashfn + '.log', "wb") as f:
            f.write(log)

class Fuzzer():
    def __init__(self):
        self.keep_going = True

    def run(self):
        while self.keep_going:
            start_fuzzing()

if __name__ == "__main__":
    fuzzer = Fuzzer()
    fuzzer.run()
