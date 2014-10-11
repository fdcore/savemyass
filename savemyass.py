#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Dmitriy Nyashkin'

from fabric.api import env, run, get, cd, sudo
from datetime import datetime
import os
import yaml
import sys, getopt

date = datetime.now().strftime("%Y-%m-%d")
time = datetime.now().strftime("%H-%M-%S")

folder = 'tmp/'+date

def parse_command_line(line):
  global folder
  
  lines = line.split(' ')
  cmd = lines[0]
  del lines[0]

  command = " ".join(lines)
  
  if cmd == 'run':
    run(command)
    
  if cmd == 'cd':
    cd(command)
    
  if cmd == 'sudo':
    sudo(command)
        
  if cmd == 'get':
    if os.path.exists(folder) is False:
      os.makedirs(folder)
      
    get(command, folder)
  
# print yaml.dump(y, default_flow_style=False)

def main(argv):
   global folder
   
   inputfile = ''
   outputfile = ''
   directory = ''
   
   try:
      opts, args = getopt.getopt(argv,"hi:do:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'savemyass.py -i <inputfile> -d <directory> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'savemyass.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--input"):
         inputfile = arg
      elif opt in ("-o", "--output"):
         outputfile = arg
      elif opt in ("-d", "--directory"):
         directory = arg
         
   if inputfile == None and directory == None:
     print 'savemyass.py -i <inputfile> -d <directory> -o <outputfile> '
     return False
   
   if outputfile == None:
     outputfile = ''
     
   
   if directory:
      directory_list = os.listdir(directory)
      for dl in directory_list:
         f = open(directory+'/'+dl, 'r')
         y = yaml.load(f)
         env.host_string = "%s@%s:%s" % (y['login'], y['host'], y['port'])
         env.password = y['password']
         
         date = datetime.now().strftime("%Y-%m-%d")
         folder = "%s/%s/%s" % (outputfile, y['host'], date)
         
         for c in y['commands']:
            parse_command_line(c)
   else:
        f = open(inputfile, 'r')
        y = yaml.load(f)
        env.host_string = "%s@%s:%s" % (y['login'], y['host'], y['port'])
        env.password = y['password']

        date = datetime.now().strftime("%Y-%m-%d")
        folder = "%s/%s/%s" % (outputfile, y['host'], date)

        for c in y['commands']:
            parse_command_line(c)
   
if __name__ == "__main__":
   main(sys.argv[1:])