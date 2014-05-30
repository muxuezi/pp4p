"""
XML parsing: regular expressions (no robust or general)
"""
                                                
import re, pprint                            
text    = open('books.xml').read()                        # str if str pattern
pattern = '(?s)isbn="(.*?)".*?<title>(.*?)</title>'       # *?=nongreedy                      
found   = re.findall(pattern, text)                       # (?s)=dot matches /n 
mapping = {isbn: title for (isbn, title) in found}        # dict from tuple list
pprint.pprint(mapping)
