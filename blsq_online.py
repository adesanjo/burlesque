#!/usr/bin/env python3

import sys
import requests
from urllib.parse import quote_plus as urlencode
from bs4 import BeautifulSoup as bs

def interpret(code):
    r=requests.get(f"http://cheap.int-e.eu/~burlesque/burlesque.cgi?q={urlencode(code)}")
    html=bs(r.content,"lxml")
    print("\n".join(span.text for span in html.body.div.pre.findAll("span")))

if __name__=="__main__":
    if len(sys.argv)>1:
        if len(sys.argv)>2:
            code="\""+" ".join(s for s in sys.argv[2:])+"\""
        else:
            code=""
        with open(sys.argv[1]) as f:
            code+=f.read()
        interpret(code)
    else:
        code=input("> ")
        while code!="exit":
            interpret(code)
            code=input("> ")
