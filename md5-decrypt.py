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
	("file", "dictionary/dic_1.txt"),
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

for source in tSources:
	if source[0] == "url":
		getUrlWords(source[1])
	if source[0] == "file":
		getFileWords(source[1])


# hashPassFile = open("PASSWORDS.md");
# for hashPass in hashPassFile:
# 	hashPassList.append(hashPass.replace("\n", ""))

# hashPassFile.close()
	
	
print(f'[i] Hash to check: {len(hashPassList)}')
print(f'[i] Hash dictionary: {len(hashWordsDictionary)}')
print("")

i = 0

for hashPass in hashPassList:
	saltVariable += 1
	if hashPass in hashWordsDictionary:
		clearPassword = hashWordsDictionary.get(hashPass)
		print("{} => ".format(saltVariable) + hashPass + ": " + clearPassword)
		i += 1

print("")	
print(f'[+] {i} hashes have been decrypted')