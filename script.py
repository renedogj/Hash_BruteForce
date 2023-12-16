try :
	import requests
	import sys
	import hashlib
except Exception as e :
	print(f"[!] Error : {e}")
	exit()

hashPassList = []
hashWordsDictionary = {}
tSources = (
	("",""),
	("url", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt"),
	("file", "wordlist.txt")
)

#Definimos la función lamba que compruaba si la url es valida
check_url = lambda url : requests.get(url).status_code == 200

#Definimos la función que obtiene el hash md5 de un 	texto pasado como parametro
def textToMd5Hash(text) :
	return hashlib.md5(text.strip().encode("utf-8")).hexdigest()

def getUrlWords(url):
	try :
		if check_url(url) :
			urlWords = requests.get(url).text.split("\n")
			for word in urlWords :
				hashWordsDictionary[textToMd5Hash(word)] = word
		else :
			print("[!] Error : " + f"Cannot Reach {url}")
	except KeyboardInterrupt :
		sys.exit()
	except Exception as e :
		print("[!] Error : " + str(e))

def getFileWords(path):
	try :
		fileWords = open(path);
		for word in fileWords :
			word = word.replace("\n", "")
			hashWordsDictionary[textToMd5Hash(word)] = word
	except KeyboardInterrupt :
		sys.exit()
	except Exception as e :
		print("[!] Error : " + str(e))

passFile = open("PASSWORDS.md");
for hashPass in passFile:
	hashPassList.append(hashPass.replace("\n", ""))

passFile.close()

for source in tSources:
	if source[0] == "url":
		getUrlWords(source[1])
	if source[0] == "file":
		getFileWords(source[1])
	
print("[i] Hash to check: {}".format(len(hashPassList)))
print("[i] Hash dictionary: {}".format(len(hashWordsDictionary)))
print("")

i = 0
for hashPass in hashPassList:
	if hashPass in hashWordsDictionary:
		print(hashPass + ": " + hashWordsDictionary.get(hashPass))
		i += 1
	# else:
	# 	print("")
		
print("")	
print("[+] {} hashes have been decrypted".format(i))