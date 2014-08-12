import sys, os, subprocess, shutil

# global var
g_pidstr = ''
g_volatility_opt = ''
g_volatility_cmd = 'vol.py'
g_srcdir = ''
g_dstdir = ''
g_issuppress = False

def help(param_str):
	print "Extract process and dll files from DISK with volatility dlllist output. made by @ykx100"
	print "  *Usage : extract_proc_bin.py -m [source_dir] -D [dest_dir] -P pid1,pid2,... -c vol.py -p MemImgProfile -f MemFileLocation"
	print "  *Example : python extract_proc_bin.py -m /mnt/volume -D /home/user/dump -P 1240,2302 -f memory.img -p WinXPSP2x86 -s\n"
	print " OPTION DESC"
	print "    -h : this output\n    -P : comma separated Target processes(if It was not use, then all processes targeted)\n    -m : mount volume directory=disk image as source\n    -D : dump directory"
	print "    -f : volatility file location option(You need to this, if you not using pre-SET enviorment)\n    -p : volatility profile(You need to this, if you not using pre-SET enviorment)\n    -c : volatility command string (default:vol.py)"
	print "    -s : Surpress output"
	exit(1)
def set_vol_filelocation(param_str):
	global g_volatility_opt
	g_volatility_opt += ' -f '+ param_str.strip()
def set_vol_profile(param_str):
	global g_volatility_opt
	g_volatility_opt += ' --profile='+ param_str.strip()
def set_pid(param_str):
	global g_pidstr
	g_pidstr = param_str.strip().replace(' ','')
def set_vol_cmd(param_str):
	global g_volatility_cmd
	g_volatility_cmd = param_str.strip()
def set_voldir(param_str):
	global g_srcdir
	g_srcdir = os.path.normpath(param_str.strip())
def set_dumpdir(param_str):
	global g_dstdir
	g_dstdir = os.path.normpath(param_str.strip())
def set_suppress(param_str):
	global g_issuppress
	g_issuppress = True
optionMap = {
	'f':set_vol_filelocation,
	'p':set_vol_profile,
	'c':set_vol_cmd,
	'P':set_pid,
	'm':set_voldir,
	'D':set_dumpdir,
	'h':help,
	's':set_suppress
}
def recognize_opt(argv):
	argval = str(argv[1:]).strip('[]\'').replace('\', \'', ' ').strip()
	argcol = argval.split('-')[1:]
	
	for argstr in argcol:
		argstr = argstr.strip()
		if optionMap.has_key(argstr[0]):
			optionMap.get(argstr[0])(argstr[1:])
		else:
			print "*Error Parameter*"
			return False
	if ((g_srcdir == '') or (g_dstdir == '')):
		return False
	return True

# Find Real filepath (prevent error character's case)base=src, target=dlllist value
def find_filepath(basedir, target_str):
	sep = '\\'
	if target_str.find('/')>=0:
		sep='/'
	elif target_str.find('\\')>=0:
		sep='\\'
	retval = ''
	tstrcol = target_str.split(sep, 1)
	if len(tstrcol) < 1:
		return 'ERROR'
	for objname in os.listdir(basedir):
		if (objname.lower() == tstrcol[0].lower()):
			if(os.path.isdir(os.path.join(basedir, objname))==True):
				if (len(tstrcol)>=2):
					retval = find_filepath(os.path.join(basedir, objname), tstrcol[1])
				break
			else:
				retval = objname
	if(retval != ''):
		return os.path.join(basedir, retval)
	
	for objname in os.listdir(basedir):
		t = tstrcol[0][:tstrcol[0].find('~')].lower()
		o = objname[:len(t)].lower()
		
		if (o==t):
			if(os.path.isdir(os.path.join(basedir, objname))==True):
				if (len(tstrcol)>=2):
					retval = find_filepath(os.path.join(basedir, objname), tstrcol[1])
				break
			else:
				retval = objname
	return os.path.join(basedir, retval)

# Begin Point
pidsig = 'pid: '
listheader = 'Base\tSize\tPath'

if (len(sys.argv) < 3) or (recognize_opt(sys.argv)== False):
	help(0)

g_volatility_cmd += g_volatility_opt + ' dlllist'
if g_pidstr != '':
	g_volatility_cmd += ' -p '+g_pidstr

print "Running with : "+ g_volatility_cmd
procpipe = subprocess.Popen(g_volatility_cmd, shell=True, stdout=subprocess.PIPE)
cmdrst = procpipe.communicate()[0]
if (cmdrst == ''):
	print "Volatility Execute Error"
	exit(1)

errcnt = 0
copycnt = 0
errfilelist =[]
#pick one file and copy
for rline in cmdrst.split('\n'):
	if(rline[0:2]=='0x'):
		while rline.find('  ')>=0:
			rline = rline.replace('  ',' ')
		
		rcol = rline.split(' ',2)
		rcol[2] = rcol[2].replace('\r','').replace("??\\",'').replace('?','').replace("\\\\",'').strip()
		if(len(rcol)>=2 and len(rcol[2])>=1):
			if (rcol[2][0] == "\\"):
				rcol[2] = rcol[2][1:]
		#nodrive = os.path.splitdrive(rcol[2])[1][1:]
		nodrive = rcol[2][rcol[2].find(':')+2:]
		srcfile = find_filepath(g_srcdir, nodrive)
		dstfile = os.path.normpath(g_dstdir+'/'+srcfile.replace(g_srcdir,''))
		
		if os.path.isfile(srcfile):
			if (os.path.exists(os.path.split(dstfile)[0])==False):
				os.makedirs(os.path.split(dstfile)[0])
			if g_issuppress==False:
				sys.stdout.write(" +" + srcfile.replace(g_srcdir,'') + " : ")
			if(os.path.exists(dstfile)):
				if g_issuppress==False: print "dup"
				continue
			try:
				shutil.copy(srcfile, dstfile)
			except:
				if g_issuppress==False: print "err"
				errfilelist.append(rcol[2])
				errcnt += 1
				pass
			if g_issuppress==False: print "Done"
			copycnt += 1
		else:
			if g_issuppress==False: print "--- Can't find File : "+rcol[2]
			errfilelist.append(rcol[2])
			errcnt += 1
print "------------------------------------------------------"
print "DONE with\tCopy : "+str(copycnt)+"\tError : " +str(errcnt)
print "------------------------------------------------------"
while(len(errfilelist)):
	errline = "Failed file : "+errfilelist.pop()
	if errline.replace("Failed file : ",'').strip() =='':
		continue
	print errline