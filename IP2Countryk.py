# ===========================================
# input ordered IP list, output country list.
# 2009.07.29 Won Yongki
# ===========================================
import os, string, re
IPDBf=open(".\\IPDB.csv",'r')
listf=open(".\\ordIPlist.txt",'r')
resultf=open(".\\Result.csv",'w')
resultf.write("IP,Code,Name\n")
linecount=0
iptable = range(107410)

readline = IPDBf.readline()
while readline:
    readline = readline.replace('\"','')
    readline = readline.replace('\n','')
    iptable[linecount] = re.split(',',readline)
    readline = IPDBf.readline()
    linecount= linecount+1
IPDBf.close()

oldcnt = 0
ipcount = 0
readline = listf.readline()
while readline:
    readline = readline.replace('\n','')
    ipcol = re.split('\.',readline)
    ipvalue = string.atoi(ipcol[0])*16777216 + string.atoi(ipcol[1])*65536 + string.atoi(ipcol[2])*256 + string.atoi(ipcol[3])

    c_str = ' , '
    if ipcount >= linecount-1:
        ipcount = oldcnt
    while  ipcount < linecount:
        startip = string.atol(iptable[ipcount][2])
        endip = string.atol(iptable[ipcount][3])
        if ipvalue >= startip and ipvalue <= endip:
            c_str = iptable[ipcount][4]+','+iptable[ipcount][5]
            oldcnt = ipcount
            break
        ipcount = ipcount + 1
#===end while linecount>=0:
    resultf.write(readline+','+c_str+'\n')
    readline = listf.readline()
listf.close()
resultf.close()

print "All done.."