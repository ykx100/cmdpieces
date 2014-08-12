import struct, time, sys
from time import strftime

def who():
        f       = open(utmpfile,"rb")
        utmpstr    = f.read();	f.close()
        cut     = lambda s: str(s).split("\0",1)[0]
        name    = ["type","pid","line","id","user","host",
                   "term","exit","session","sec","usec"]
        out     = []

        for entry in [utmpstr[i:i+384] for i in range(0,len(utmpstr),384)]:
		data = struct.unpack("hi32s4s32s256shhiii36x",entry)
		out.append(
			dict([[name[i],cut(data[i])]
			for i in range(len(data))]))
		
        return out
        
if len(sys.argv) != 3:
	print >> sys.stderr,'utmp parser\t\tMade by @ykx100\n\tUsage : python utmp_parser.py [utmpfile] [result_filename]\n\tExample : python utmp_parser.py ./utmp result.txt'
	exit(1)
utmpfile = sys.argv[1]
result_file = sys.argv[2]

wf = file(result_file,'w')
wf.write('term'+'\t'+'usec'+'\t'+'pid'+'\t'+'host'+'\t'+'session'+'\t'+'exit'+'\t'+'user'+'\t'+'sec'+'\t'+'line'+'\t'+'type'+'\t'+'id'+'\n')
entries = who()
for i in range(0, len(entries)):
	#lotime = strftime("%Y.%m.%d. %H:%M:%S",time.gmtime(float(entries[i]['sec'])))
	lotime = strftime("%Y.%m.%d. %H:%M:%S",time.localtime(float(entries[i]['sec'])))
	
	eline = entries[i]['term']+'\t'+entries[i]['usec']+'\t'+entries[i]['pid']+'\t'+entries[i]['host']+'\t'+entries[i]['session']+'\t'+entries[i]['exit']+'\t'+entries[i]['user']+'\t'+lotime+'\t'+entries[i]['line']+'\t'+entries[i]['type']+'\t'+entries[i]['id']
	wf.write(eline+'\n')

print 'done'
wf.close()