from html.parser import HTMLParser
class ParsePage(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print('Tag start:', tag, attrs)
    def handle_endtag(self, tag):
        print('tag end:  ', tag)
    def handle_data(self, data):
        print('data......', data.rstrip())

page = """
<html>
<h1>Spam!</h1>
<p>Click this <a href="http://www.python.org">python</a> link</p>
</html>"""

parser = ParsePage()
parser.feed(page)




print('-'*40)
import html.parser, cgi
s = cgi.escape("1<2 <b>hello</b>")
print(html.parser.HTMLParser().unescape(s))

class Parse(html.parser.HTMLParser):
    def handle_data(self, data):
        print(data, end='')
    def handle_entityref(self, name):
        map = dict(lt='<', gt='>')
        print(map[name], end='')

p = Parse()
p.feed(s); print()




print('-'*40)
from html.entities import entitydefs
class Parse(html.parser.HTMLParser):
    def handle_data(self, data):
        print(data, end='')
    def handle_entityref(self, name):
        print(entitydefs[name], end='')

P = Parse()
P.feed(s); print()

