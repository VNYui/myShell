import os
import sys
import re
from pathlib import Path

class myShell:
  def __init__(self):
      self.links_path = Path.cwd() / 'db.txt'
      self.start_shell()

  def start_shell(self):
    while 'to keep prompt open':
        box = input('my dark shell : ')
        self.parse_input(box)      
  
  def create_file(self,file,input):
    with open(file, 'wt', encoding='utf-8') as f:
      f.write(f'{input} \n')

  def append_file(self,file,input):
    with open(file, 'a', encoding='utf-8') as f:
      f.write(f'{input} \n')
      
  def read_file(self,file): 
    with open(file,'r') as f:
      lines = f.readlines()
      return lines

  def parse_input(self,input):
    regex = re.compile(r"(?:https?://)?(?:www)?(\S*?\.onion)\b")
    if input == 'show':
        for line in self.read_file(self.links_path):
          print(line)

    if regex.match(input):
        print('ONION FOUND - link stored')
        if self.links_path.exists():
          self.append_file(self.links_path,input)
        else :
          self.create_file(self.links_path, input)
    
    if input == 'help':
      print('''
        copy an onion link to add it to database
        show : show tor links
        clear : clean the shell
        exit : quit the shell
      ''')
    if input == 'clear':
          os.system('cls' if os.name == 'nt' else 'clear')

    if input == 'exit':
        sys.exit()
    

if __name__ == '__main__':
  start = myShell()
