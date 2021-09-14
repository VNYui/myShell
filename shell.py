import os
import sys
import re
import subprocess
from pathlib import Path
import socket 
#VOC
import pyaudio 
import speech_recognition as sr 

class myShell:
  def __init__(self):
      self.Parse = parser()
      self.r = sr.Recognizer()
      self.subproc = subProc()
      self.subproc.exec_elisa()
      self.start_shell()
      

  def start_shell(self):
      while 'to keep prompt open':
        box = input('my dark shell : ')
        self.Parse.input(box)
          
class parser:
  def __init__(self):
      self.links_path = Path.cwd() / 'db.txt'
      self.mf = manageFile()
      self.sub = subProc()
      self.net = network()

  def input(self,input):
    input = input.split()
    onion = re.compile(r"(?:https?://)?(?:www)?(\S*?\.onion)\b")
    ipv4  = re.compile(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    try :
      if input[0] == 'show':
          for line in self.mf.read_file(self.links_path):
            print(line)

      if onion.match(input[0]):
          print('ONION FOUND - link stored')
          if self.links_path.exists():
            self.mf.append_file(self.links_path,input)
          else :
            self.mf.create_file(self.links_path, input)

      if input[0] == 'help':
          print('''
            Scan
              input IPV4 to start nmap scan:
                Eg : 127.0.0.1 -sV -A --script=*  

            TOR
              input an onion link to add it to database 
                Eg : bcloudwenjxgcxjh6uheyt72a5isimzgg4kv5u74jb2s22y3hzpwh6id.onion/ description
              show : show tor links
            
            Network:
              dns = resolve ip addr by hostname
                Eg : dns 127.0.0.1 8.8.8.8 
              rdns = resolve hostname by ip addr
                Eg : www.google.com www.yahoo.fr

            MISC 
              clear : clean the shell
              exit : quit the shell

          ''')

      if ipv4.match(input[0]):
          self.sub.exec(input)

      if input[0] == 'clear':
          os.system('cls' if os.name == 'nt' else 'clear')
          

      if input[0] == 'dns':
          self.net.dns_lookup(input)
      if input[0] == 'rdns':
          self.net.dns_reverse_lookup(input)
      if input[0] == 'exit':
          sys.exit()  
    except IndexError:
      print('Enter a valid command')
      
class manageFile:
  def create_file(self,file,input):
    with open(file, 'wt', encoding='utf-8') as f:
      if len(input) > 1:
        f.write(f'{input[0]} ({input[1]})\n')
      elif len(input) == 1 :
        f.write(f'{input[0]}\n')

  def append_file(self,file,input):
    with open(file, 'a', encoding='utf-8') as f:
      if len(input) > 1:
        f.write(f'{input[0]} ({input[1]})\n')
      elif len(input) == 1 :
        f.write(f'{input[0]}\n')
        
  def read_file(self,file): 
    with open(file,'r') as f:
      lines = f.readlines()
      return lines

class subProc:
  def __init__(self):
      self.nmap = Path.cwd() / 'Nmap/nmap.exe'
      self.Elisa = Path.cwd() / 'Elisa.py'

  def exec(self, input):
    result = subprocess.run(
      [self.nmap, *input[1:], input[0]],capture_output=True, text=True
    )
  
  def exec_elisa(self):
    cmd = 'python3 Elisa.py'
    proc = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    return proc
  

    #print(result.args)
    #print(result.stdout)

class network:
  def __init__(self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  
  def dns_lookup(self, input):
    for dns in input[1:]:
      ip = socket.gethostbyname(dns)
      print(ip)
    return ip    
  
  def dns_reverse_lookup(self,input):
    for ip in input[1:]:
      dns = socket.gethostbyaddr(ip)
      print(dns)
    return dns
  
if __name__ == '__main__':
  start = myShell()
