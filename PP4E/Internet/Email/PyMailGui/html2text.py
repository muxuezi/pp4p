"""
################################################################
*VERY* preliminary html-to-text extractor, for text to be 
quoted in replies and forwards, and displayed in the main
text display component.  Only used when the main text part
is HTML (i.e., no alternative or other text parts to show).
We also need to know if this is HTML or not, but findMainText
already returns the main text's content type.

This is mostly provided as a first cut, to help get you started
on a more complete solution.  It hasn't been polished, because 
any result is better than displaying raw HTML, and it's probably
a better idea to migrate to an HTML viewer/editor widget in the 
future anyhow.  As is, PyMailGUI is still plain-text biased.

If (really, when) this parser fails to render well, users can
instead view and cut-and-paste from the web browser popped up 
to display the HTML.  See Chapter 19 for more on HTML parsing.
################################################################
"""
from html.parser import HTMLParser     # Python std lib parser (sax-like model)

class Parser(HTMLParser):              # subclass parser, define callback methods
    def __init__(self):                # text assumed to be str, any encoding ok
        HTMLParser.__init__(self)
        self.text = '[Extracted HTML text]'
        self.save = 0
        self.last = ''

    def addtext(self, new):
        if self.save > 0:
            self.text += new
            self.last = new

    def addeoln(self, force=False):
        if force or self.last != '\n':
            self.addtext('\n')

    def handle_starttag(self, tag, attrs):    # + others imply content start?
        if tag in ('p', 'div', 'table', 'h1', 'h2', 'li'):
            self.save += 1
            self.addeoln()
        elif tag == 'td':
            self.addeoln()
        elif tag == 'style':                  # + others imply end of prior?
            self.save -= 1
        elif tag == 'br':
            self.addeoln(True)
        elif tag == 'a':
            alts = [pair for pair in attrs if pair[0] == 'alt']
            if alts:
                name, value = alts[0]
                self.addtext('[' + value.replace('\n', '') + ']')

    def handle_endtag(self, tag):
        if tag in ('p', 'div', 'table', 'h1', 'h2', 'li'):
            self.save -= 1
            self.addeoln()
        elif tag == 'style':
            self.save += 1

    def handle_data(self, data):
        data = data.replace('\n', '')          # what about <PRE>?
        data = data.replace('\t', ' ')
        if data != ' ' * len(data):
            self.addtext(data)           

    def handle_entityref(self, name):
        xlate = dict(lt='<', gt='>', amp='&', nbsp='').get(name, '?')
        if xlate:
            self.addtext(xlate)     # plus many others: show ? as is

def html2text(text):
    try:
        hp = Parser()
        hp.feed(text)
        return(hp.text)
    except: 
        return text

if __name__ == '__main__': 
    
    # to test me: html2text.py media\html2text-test\htmlmail1.html
    # parse file name in commandline, display result in tkinter Text
    # file assumed to be in Unicode platform default, but text need not be
    
    import sys, tkinter                       
    text = open(sys.argv[1], 'r').read()   
    text = html2text(text)                 
    t = tkinter.Text()
    t.insert('1.0', text)
    t.pack()
    t.mainloop()
