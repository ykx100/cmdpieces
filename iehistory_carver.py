import binascii
from datetime import datetime,timedelta

rf = file("carved.str",'r')
wf = file("parsed.tsv",'w')

rbase = rf.read(256)
while (len(rbase) > 1):
	rline = rf.read(256)
	if(rline[0:3] != 'URL'):
		rbase = rbase + rline
		rline = rf.read(256)
	
	sigchar = rbase[0:4]
	amountblock = rbase[4:8]
	
	dt = binascii.hexlify(rbase[8:16])
	dt = dt[14:16]+dt[12:14]+dt[10:12]+dt[8:10]+dt[6:8]+dt[4:6]+dt[2:4]+dt[0:2]
	time1 = datetime(1601,1,1) + timedelta(microseconds=int(dt, 16) / 10.)
	
	dt = binascii.hexlify(rbase[16:24])
	dt = dt[14:16]+dt[12:14]+dt[10:12]+dt[8:10]+dt[6:8]+dt[4:6]+dt[2:4]+dt[0:2]
	time2 = datetime(1601,1,1) + timedelta(microseconds=int(dt, 16) / 10.)
	
	etc = rbase[24:104]
	url_rec = rbase[104:len(rbase)]
	url_rec = url_rec.split('\x00')[0].strip()
	
	outline = sigchar+'\t'+str(time1)+'\t'+str(time2)+'\t'+url_rec+'\t'+str(amountblock)
	wf.write(outline+'\n')
	rbase = rline

rf.close()
wf.close()