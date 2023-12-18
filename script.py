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
	("file", "wordlist.txt"),
	("url", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt"),
	("url", "https://raw.githubusercontent.com/hackingyseguridad/diccionarios/master/diccionario.txt"),
	("url", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Most-Popular-Letter-Passes.txt"),
	("url", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/UserPassCombo-Jay.txt"),
	("url", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/bt4-password.txt"),
	("url", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/cirt-default-passwords.txt"),
	("url", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/clarkson-university-82.txt"),
	("url", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/darkweb2017-top10000.txt"),
	("url", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/days.txt"),
	("url", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/months.txt"),
	("url", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/seasons.txt"),
	("url", "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/xato-net-10-million-passwords.txt"),
)

#Definimos la función lamba que compruaba si la url es valida
check_url = lambda url : requests.get(url).status_code == 200

#Definimos la función que obtiene el hash md5 de un texto pasado como parametro
def textToMd5Hash(text):
	return hashlib.md5(text.strip().encode("utf-8")).hexdigest()

#Definimos la función que obtiene el hash sha256 de un texto pasado como parametro
def textToSha256(text):
	return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

#Definimos la función que obtiene todas las palabras de un archivo obtenido atraves de una url
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

#Definimos la función que obtiene todas las palabras de un archivo obtenido atraves de un path
def getFileWords(path):
	try :
		fileWords = open(path)
		for word in fileWords :
			word = word.replace("\n", "")
			hashWordsDictionary[textToMd5Hash(word)] = word
	except KeyboardInterrupt :
		sys.exit()
	except Exception as e :
		print("[!] Error : " + str(e))

hashPassFile = open("PASSWORDS.md");
for hashPass in hashPassFile:
	hashPassList.append(hashPass.replace("\n", ""))

hashPassFile.close()

for source in tSources:
	if source[0] == "url":
		getUrlWords(source[1])
	if source[0] == "file":
		getFileWords(source[1])
	
	
print("[i] Hash to check: {}".format(len(hashPassList)))
print("[i] Hash dictionary: {}".format(len(hashWordsDictionary)))
print("")

clearPassFile = open("clearPassFile.txt", "w")
saltPassFile = open("saltPassFile.txt", "w")

i = 0
saltVariable = 0
saltFijo = "1salt2Hash3"

for hashPass in hashPassList:
	saltVariable += 1
	if hashPass in hashWordsDictionary:
		clearPassword = hashWordsDictionary.get(hashPass)
		print(hashPass + ": " + clearPassword)
		
		if saltVariable%2 == 0:
			saltClearPassword = "{}".format(saltVariable) + saltFijo + clearPassword
		else:
			saltClearPassword = saltFijo + "{}".format(saltVariable) + clearPassword
		
		saltPassword = textToSha256(saltClearPassword)

		clearPassFile.write(clearPassword + "\n")
		saltPassFile.write(saltPassword + "\n")
		i += 1
	else:
		clearPassFile.write("\n")
		saltPassFile.write("\n")
	

clearPassFile.close()
saltPassFile.close()

print("")	
print("[+] {} hashes have been decrypted".format(i))