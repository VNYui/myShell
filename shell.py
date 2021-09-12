import os
import sys
import re
import subprocess
from pathlib import Path

class myShell:
  def __init__(self):
      self.Parse = parser()
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

  def input(self,input):
    input = input.split()
    onion = re.compile(r"(?:https?://)?(?:www)?(\S*?\.onion)\b")
    ipv4  = re.compile(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
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
          Recon
            input IPV4 to start scan the target 

          TOR
            input an onion link to add it to database 
            Exemple : bcloudwenjxgcxjh6uheyt72a5isimzgg4kv5u74jb2s22y3hzpwh6id.onion/ description
            show : show tor links

          MISC 
            clear : clean the shell
            exit : quit the shell

        ''')

    if ipv4.match(input[0]):
        self.sub.exec()

    if input[0] == 'clear':
        os.system('cls' if os.name == 'nt' else 'clear')

    if input[0] == 'exit':
        sys.exit()  

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

  def exec(self, input):
    result = subprocess.run(
      [self.nmap, "-sV", input],capture_output=True, text=True
    )
    print(result.stdout)
if __name__ == '__main__':
  start = myShell()
