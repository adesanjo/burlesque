#!/usr/bin/env python3

import os
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("-d","--debug",action="store_true",help="Activate debug mode")
parser.add_argument("-f","--file",help="Interpret code from file")
parser.add_argument("-i","--input",nargs="*",help="Input for code in file")
args=parser.parse_args()

DEBUG=args.debug

if DEBUG:print("Offline Burlesque Interpreter: WIP!")

TOKENS={'!!','!=','!C','!~','#<','$$','&&','**','++','+.','+]','-.','-]','-~','.%','.*','.+','.-','./','.<','.>','/^','/v',';;','<-','<.','<=','<>','<]','<m','==','=[','=s','=~','>.','><','>=','>]','>m','?!','?*','?+','?-','?/','??','?^','?d','?i','?s','AV','B!','BS','Bc','Bp','C!','CB','CL','CM','CN','CO','CW','Cl','Cm','D!','DW','E!','F:','FF','FL','FM','FO','FZ','Ff','Fi','GO','GZ','HD','IC','IN','LD','LG','LI','LO','L[','M-','MP','MV','M[','M]','NB','PD','PI','P[','R@','RA','RN','RT','R_','R~','SD','SH','SI','SO','SP','S[','Sc','Sd','Sh','Sn','Sq','Su','Sw','TC','TS','TT','TW','Tc','Ts','Tt','UN','U[','U_','WD','WL','WW','W[','Wl','XX','ZZ','Z[','Z]','[+','[-','[M','[P','[S','[[','[]','[m','[~','j','\\[','\\\\','\\m',']m','^/','J','^m','^p','_+','aa','ab','ad','al','an','ap','av','ay','b0','b2','b6','bc','bs','bx','c!','cb','cc','cd','ch','ck','cl','cm','cn','co','cp','cq','ct','cy','d!','dg','di','dv','dw','e!','ec','ed','en','eq','es','f:','fC','fI','f[','fc','fe','ff','fi','fl','fo','fp','fu','fw','f~','gB','g_','gb','gc','gl','gn','gp','gr','gs','gw','hc','hd','hp','iR','iS','iT','ia','ic','ie','if','im','is','it','l0','l2','l_','ld','lg','ln','lp','m$','m&','m[','m]','m^','mm','mo','mp','ms','mu','mw','m|','n!','nc','nd','ng','nq','nr','nu','nz','p^','pa','pc','pd','pe','pm','pp','ps','pt','r&','r0','r1','r@','r[','r\\','r_','ra','rd','ri','rm','rn','ro','rp','rt','rz','r|','r~','#r','#R','s=','sH','sN','sa','sb','sc','sg','shQ','si','sl','sm','sn','so','sp','sr','ss','su','sw','t[','t]','td','th','ti','tl','to','tp','tt','tw','uN','u[','uc','ud','ug','un','uq','v/','vr','vv','w!','wD','wL','w[','wd','wl','ww','x/','z?','z[','zi','zz','|*','|+','|-','|/','|d','|i','||','~!','~&','~-','~;','~=','~?','~[','~]','~a','~~','{','}'}

IMPLEMENTED_TOKENS={"{","}","vv","j","J","x/","#r","#R","?+","?-","?*","?/",".%",".<",".>","==","!=","n!","<-","NB","<>","=[","e!","Q","sh","ps","++","if","ie","m[","z[","Z[","Z]","r[","f[","r@",".+"}

if DEBUG:
    print("Unimplemented tokens:")
    print(TOKENS-IMPLEMENTED_TOKENS)

def isNum(n):
    return len(n)>0 and n[n[0]=="-":].replace(".","",1).isdigit()

def parseBlocks(preParsedCode):
    i=0
    parsedCode=[]
    while i<len(preParsedCode):
        if preParsedCode[i]=="{":
            n=1
            j=i
            while n>0:
                j+=1
                if preParsedCode[j]=="{":
                    n+=1
                elif preParsedCode[j]=="}":
                    n-=1
            parsedCode.append(parseBlocks(preParsedCode[i+1:j]))
            i=j
        else:
            parsedCode.append(preParsedCode[i])
        i+=1
    return parsedCode

def parseCode(code):
    if DEBUG:print("parsing:",code)
    preParsedCode=[]
    token=""
    isString=False
    i=-1
    while i<len(code)-1:
        i+=1
        c=code[i]
        if c=="\"":
            token+=c
            isString=not isString
            if not isString:
                preParsedCode.append(token)
                token=""
            continue
        if isString:
            token+=c
            continue
        if c.isspace():
            if len(token)>0:
                preParsedCode.append(token)
                token=""
            continue
        if token in TOKENS:
            if DEBUG and token not in IMPLEMENTED_TOKENS:print(f"WARNING :: Unimplemented token: {token}")
            preParsedCode.append(token)
            token=""
            i-=1
            continue
        if isNum(token) and (not isNum(token+c) or (c=="." and not code[i+1].isdigit())):
            preParsedCode.append(token)
            token=""
            i-=1
            continue
        token+=c
    if len(token)>0:
        if token in TOKENS:
            if DEBUG and token not in IMPLEMENTED_TOKENS:print(f"WARNING :: Unimplemented token: {token}")
        preParsedCode.append(token)
    if DEBUG:print("pre-parsed code:",preParsedCode)
    parsedCode=parseBlocks(preParsedCode)
    if DEBUG:print("parsed code:",parsedCode)
    return parsedCode

def interpret(stack,code):
    errorCode=0
    if DEBUG:
        print()
        print("interpreting:",code)
        print("stack:",stack)
    for i in code:
        if DEBUG:print("instruction:",i)
        if isinstance(i,list):
            stack.append(i)
        elif i.isdigit() or (i[0]=="-" and i[1:].isdigit()):
            stack.append(int(i))
        elif i.replace(".","",1).isdigit() or (i[0]=="-" and i.replace(".","",1)[1:].isdigit()):
            stack.append(float(i))
        elif i[0]=="\"" and i[-1]=="\"":
            stack.append(i)
        elif i=="vv":
            stack.pop()
        elif i=="j":
            stack[-1],stack[-2]=stack[-2],stack[-1]
        elif i=="J":
            stack.append(stack[-1])
        elif i=="x/":
            stack[-1],stack[-2],stack[-3]=stack[-3],stack[-1],stack[-2]
        elif i=="#r":
            stack[:]=stack[-1:]+stack[:-1]
        elif i=="#R":
            stack[:]=stack[1:]+stack[:1]
        elif i=="?+":
            a=stack.pop()
            b=stack.pop()
            if isinstance(a,int) and isinstance(b,int):
                stack.append(b+a)
            else:
                l=[]
                for j in range(min(len(a),len(b))):
                    interpret(l,[b[j],a[j],"?+"])
                stack.append(l)
        elif i=="?-":
            a=stack.pop()
            b=stack.pop()
            if isinstance(a,int) and isinstance(b,int):
                stack.append(b-a)
            else:
                l=[]
                for j in range(min(len(a),len(b))):
                    interpret(l,[b[j],a[j],"?-"])
                stack.append(l)
        elif i=="?*":
            a=stack.pop()
            b=stack.pop()
            if isinstance(a,int) and isinstance(b,int):
                stack.append(b*a)
            else:
                l=[]
                for j in range(min(len(a),len(b))):
                    interpret(l,[b[j],a[j],"?*"])
                stack.append(l)
        elif i=="?/":
            a,b=stack.pop(),stack.pop()
            if isinstance(a,int) and isinstance(b,int):
                stack.append(b//a)
            elif isinstance(a,float) or isinstance(b,float):
                stack.append(b/a)
            else:
                l=[]
                for j in range(min(len(a),len(b))):
                    interpret(l,[b[j],a[j],"?/"])
                stack.append(l)
        elif i==".%":
            a,b=stack.pop(),stack.pop()
            stack.append(b%a)
        elif i==".<":
            stack.append(int(stack.pop()>stack.pop()))
        elif i==".>":
            stack.append(int(stack.pop()<stack.pop()))
        elif i=="==":
            stack.append(int(stack.pop()==stack.pop()))
        elif i=="!=":
            stack.append(int(stack.pop()!=stack.pop()))
        elif i=="n!":
            stack.append(int(stack.pop()==0))
        elif i=="<-":
            stack.append(stack.pop()[::-1])
        elif i=="NB":
            l=[]
            block=stack.pop()
            for e in block:
                if e not in l:
                    l.append(e)
            stack.append(l)
        elif i=="<>":
            stack[-1].sort(reverse=True)
        elif i=="=[":
            l=[]
            block=stack.pop()
            for e in block:
                grouped=False
                for g in l:
                    if g[0]==e:
                        g.append(e)
                        grouped=True
                        break
                if not grouped:
                    l.append([e])
            stack.append(l)
        elif i=="e!":
            errorCode=interpret(stack,stack.pop())
        elif i in ["Q","sh"]:
            s=stack.pop()
            if isinstance(s,str):
                ns=s.replace("\"","").replace("\\'","\"").replace("\\\\","\\")
            else:
                ns=s
            stack.append(ns)
        elif i=="ps":
            stack.append(parseCode(stack.pop().replace("\"","").replace("\\'","\"").replace("\\\\","\\")))
        elif i=="++":
            a=stack.pop()
            if isinstance(a,int):
                b=stack.pop()
                stack.append(int(str(b)+str(a)))
            else:
                stack.append(sum(int(d) for d in a))
        elif i=="if":
            ifCode=stack.pop()
            if stack.pop()!=0:
                interpret(stack,ifCode)
        elif i=="ie":
            cond=stack.pop()
            elseCode=stack.pop()
            ifCode=stack.pop()
            if cond:
                interpret(stack,ifCode)
            else:
                interpret(stack,elseCode)
        elif i=="m[":
            l=[]
            c=stack.pop()
            b=stack.pop()
            for j in b:
                interpret(l,[j])
                interpret(l,c)
            stack.append(l)
        elif i=="z[":
            l=[]
            a=stack.pop()
            b=stack.pop()
            for j in range(min(len(a),len(b))):
                l.append([b[j],a[j]])
            stack.append(l)
        elif i=="Z[":
            l=[]
            c=stack.pop()
            a=stack.pop()
            b=stack.pop()
            for j in range(min(len(a),len(b))):
                l.append([b[j],a[j]])
            b=l
            l=[]
            for j in b:
                interpret(l,[j])
                interpret(l,c)
            stack.append(l)
        elif i=="Z]":
            l=[]
            c=stack.pop()
            a=stack.pop()
            b=stack.pop()
            for j in range(min(len(a),len(b))):
                interpret(l,[b[j],a[j]])
                interpret(l,c)
            stack.append(l)
        elif i=="r[":
            c=stack.pop()
            b=stack.pop()
            r=[]
            interpret(r,b[0:1])
            for j in b[1:]:
                interpret(r,[j])
                interpret(r,c)
            stack.append(r[-1])
        elif i=="f[":
            l=[]
            c=stack.pop()
            b=stack.pop()
            for j in b:
                interpret(l,[j])
                interpret(l,c)
            stack.append([b[j] for j in range(len(b)) if l[j]!=0])
        elif i=="r@":
            a,b=stack.pop(),stack.pop()
            l=[str(j) for j in range(b,a+1)]
            stack.append(l)
        elif i==".+":
            a,b=stack.pop(),stack.pop()
            stack.append(b+a)
        if DEBUG:print("stack:",stack)
    if DEBUG:
        print("finished interpreting:",code)
        print()
    return errorCode

if __name__=="__main__":
    code=""

    if args.file:
        if args.input:
            code="\""+" ".join(s for s in args.input)+"\""
        else:
            code=""
        with open(args.file) as f:
            code+=f.read().strip()
        stack:list=[]
        interpret(stack,parseCode(code))
        if DEBUG:print("Output:")
        while len(stack)>0:
            print(stack.pop())
    else:
        try:
            code=input("> ")
            while code!="exit":
                if code=="clear":
                    os.system("clear")
                    code=input("> ")
                    continue
                stack=[]
                interpret(stack,parseCode(code))
                if DEBUG:print("Output:")
                while len(stack)>0:
                    print(stack.pop())
                code=input("> ")
        except KeyboardInterrupt:
            pass
