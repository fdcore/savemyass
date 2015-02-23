#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Dmitriy Nyashkin'
__version__ = '0.2'

from fabric.api import env, run, get, cd, sudo, local
from datetime import datetime
import os
import yaml
import sys, getopt
import easywebdav

date = datetime.now().strftime("%Y-%m-%d")
time = datetime.now().strftime("%H-%M-%S")

folder = 'tmp/'+date
root_host_dir = "tmp/"
config = {}

def download_file(filename):
    global folder, root_host_dir
    
    get(filename, folder) # скачиваем файл

    _filename = filename.split('/')[-1]
    _size_path = root_host_dir+_filename+".size" 
    last_file_size = ''
    
    # если есть файл с данными размера файла
    if os.path.exists(_size_path):
        last_file_size = open(_size_path, 'rb').read()
    
    # текущий размер файла
    current_file_size = str(os.path.getsize(folder+'/'+_filename))
    
    # проверка на размер прошлого бекапа + защита от удаления если прошлый бекап был сегодня
    if last_file_size == current_file_size:
        print 'File deleted ' + folder+'/'+_filename
        os.remove(folder+'/'+_filename)
    else:
        _file = open(_size_path, "w")
        _file.write(current_file_size)
        _file.close()

# загружаем файл, пока что по WebDav
def upload_file(filename):
    global config, folder
    
    filename = folder+"/"+filename
    
    if 'webdav' not in config:
        return False
        
    if os.path.exists(filename) is False:
        return False
        
    if 'connected' not in config:
        webdav = easywebdav.connect(**config['webdav'])
        config['connected'] = webdav
    else:
        webdav = config['connected']
        
    dirname = os.path.dirname(filename)

    if webdav.exists(dirname) is False:
        webdav.mkdirs(dirname)

    webdav.upload(filename, filename)

# Парсим yaml файл
def yaml_parse(filename):
    y = False
    
    if os.path.exists(filename):
        f = open(filename, 'r')
        y = yaml.load(f)
    
    return y

def set_paths(outdir, hostname):
    global folder, root_host_dir
    
    date = datetime.now().strftime("%Y-%m-%d") # or %Y-%m-%d %H-%M
    folder = "%s/%s/%s" % (outdir, hostname, date)
    root_host_dir = "%s/%s/" % (outdir, hostname)
    
    if os.path.exists(folder) is False:
        os.makedirs(folder)
    
    
# команды для выполнения
def parse_command_line(line):
  global folder, root_host_dir
  
  lines = line.split(' ')
  cmd = lines[0]
  del lines[0]

  command = " ".join(lines)
  
  if cmd == 'run': run(command)
  if cmd == 'cd': cd(command)
  if cmd == 'local': local(command)
  if cmd == 'sudo': sudo(command)
  if cmd == 'get' or cmd == 'download': download_file(command) # передан путь к файлу
  if cmd == 'set' or cmd == 'upload': upload_file(command)

def main(argv):
   global folder, root_host_dir, config
   
   inputfile = ''
   outputfile = ''
   directory = ''
   
   try:
      opts, args = getopt.getopt(argv,"h:i:d:o:")

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
         y = yaml_parse(directory+'/'+dl)
         
         if y is False:
             continue
             
         env.host_string = "%s@%s:%s" % (y['login'], y['host'], y['port'])
         env.password = y['password']
         config = y
         set_paths(outputfile, y['host'])
         
         for c in y['commands']:
            parse_command_line(c)
   else:
        y = yaml_parse(inputfile)
        
        if y:
          env.host_string = "%s@%s:%s" % (y['login'], y['host'], y['port'])
          env.password = y['password']
          
          set_paths(outputfile, y['host'])
          config = y
          
          for c in y['commands']:
              parse_command_line(c)
        else:
          print 'config file not found'
          
if __name__ == "__main__":
   main(sys.argv[1:])