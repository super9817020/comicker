import comFetch
import sys

def printUsage():
	print("[Usage]Directly type command:")
	print("\th, help : this page")
	print("\tq, exit:")
	print("\tf, s <comic-name>: search a comic book to get <comic e-name>")
	print("\tls <comic e-name>: get <comic e-name>'s chapter list")
	print("\td <comic e-name> <chapter id>: <chapter id> can be 'all' or chapter num")
	
def cmdHandler(cmd):
	cmd=cmd.split(' ')
	#print(cmd)
	if(cmd[0]=="q" or cmd[0]=="exit"):
		exit(0)
	elif(cmd[0]=="h" or cmd[0]=="help"):
		printUsage()
	elif(cmd[0]=="f" or cmd[0]=="s"):
		if(len(cmd)==2):
			comFetch.searchComic(cmd[1])
		else:
			printUsage()
	elif(cmd[0]=='ls'):
		if(len(cmd)==2):
			comFetch.showComic(cmd)
		else:
			printUsage()
	elif(cmd[0]=='d'):
		if(len(cmd)==3):
			comFetch.downComic(cmd)
		else:
			printUsage()
	else:
		printUsage()
		
if __name__ == "__main__":
	sys.stdout.write('>>')
	sys.stdout.flush()
	line=sys.stdin.readline()
	while(line!=None):
		command=line.strip('\r\n')
		cmdHandler(command)
		sys.stdout.write('>>')
		sys.stdout.flush()
		line=sys.stdin.readline()
		