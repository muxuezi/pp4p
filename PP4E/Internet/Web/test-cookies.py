# inline cookie examples


import http.cookies, time
cook = http.cookies.SimpleCookie()
cook['visited'] = str(time.time())     # a dictionary
print(cook.output())                   # "Set-Cookie: visited=1137268854.98;"
print('Content-type: text/html\n')


import os, http.cookies
os.environ["HTTP_COOKIE"] = 'Cookie: visited=1276623053.89'
cooks = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
vcook = cooks.get("visited")     # a Morsel dictionary
if vcook != None:
    time = vcook.value
    print(time)
