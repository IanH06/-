import PyPDF2 as ppdf
path = "U2AQA.pdf"
reader = ppdf.PdfReader(open(path,"rb"))
d  = {}
def get_page(path, page):
    with open(path, "rb") as f:
        pdf = ppdf.PdfReader(f)

        page = pdf.pages[page].extract_text()
    if ":" in page:
        l = []
        a = []
        for i in page:
            if i != "\n":
                a.append(i)
            else:
                l.append("".join(a))
                a = []
        return l
    return False

def getkey(p,k):
    l = []
    for i , j in enumerate(p):
        x = ""
        c = 1
        if j:
            if k in p[i-1] and ":" in p[i]:
                print(i)
                while True:
                    for b in p[i+c]:
                        x += str(b)
                        if b == ".":
                            c = -1
                            break
                    if c == -1:
                        break
                    c += 1

                l.append((p[i][:-1],x))
    print(l)
    if l:
        return l

def getall(path):
    for i,j in enumerate(reader.pages):
        page = (j.extract_text())
        keys  = ["Key concept","Key principle","Key fact","Key point","Key term"]
        for key in keys:
            if key in page:
                l = []
                a = []
                for i in page:
                    if i != "\n":
                        a.append(i)
                    else:
                        l.append("".join(a))
                        a = []
                (getkey(l,key))
            #print(l)
#getall(path)
#for i in range(len(reader.pages)):
#for i in range(10,20):
    #print(i)
    #p =  get_page(path,i)
    #if p:
    #    print(i)
    #    gk = getkey(p)  
    #    if gk:
    #        for i in gk:
    #            d[i[0]] = i[1]
p = get_page(path,86)
for i, j in enumerate(p):
    print(i,j)
#print(d)


