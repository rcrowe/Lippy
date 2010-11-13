#!/usr/bin/env python
#encoding: utf-8

import sys

#Check Lippy is compatible
(series, major) = (sys.version_info)[:2]
 
if series is not 3:
    sys.stderr.write("Lippy needs python 3\n\n")
    sys.exit(1)

import os
import os.path
from   optparse import OptionParser
import configparser
import socketserver
import json

#Import correct platform library
if sys.platform == 'win32':
    import LippyWin as colour
else:
    import LippyNix as colour


class Lippy:

    host = None
    port = None
    config_file = 'lippy.cfg'
    config = None
    server = None

    def __init__(self):
        
        #Get server parameters
        #Either from command line parameters or config file
        
        #Check command line
        cmdline = OptionParser()
        
        #Server host
        cmdline.add_option("-H",
                           "--host", 
                           action="store", 
                           type="string", 
                           dest="host",
                           help="Host to connect server too")
        
        #Server port
        cmdline.add_option("-p", 
                           "--port", 
                           action="store", 
                           type="int", 
                           dest="port",
                           help="Port to connect to")
                           
        #Config file
        cmdline.add_option("-c", 
                           "--config", 
                           action="store", 
                           type="string", 
                           dest="config_file",
                           help="Name of config file to load default parameters from")
        
        #Parse arguments
        (options, args) = cmdline.parse_args()
        
        #If we don't have all the parameters, get from config file
        #Check new config file wasnt set
        if options.config_file is not None:
            self.config_file = options.config_file
        
        if options.host is None or options.port is None or options.buffer_size is None:
            (config_host, config_port) = self.get_config()
        
        #Check host
        if options.host is not None:
            #Host passed in command line, override config file
            self.host = options.host
        else:
            self.host = config_host
            
        #Check port
        if options.port is not None:
            self.port = options.port
        else:
            self.port = config_port

    def get_config(self):
        
        #Check file exists
        current_path = os.path.abspath(os.path.dirname(__file__))
        config_path  = os.path.join(current_path, self.config_file)
        
        if not os.path.exists(config_path):
            self.exit("Unable to find config file: %s\n" % config_path)
            
        #Return config items
        config = configparser.ConfigParser()
        config.read(self.config_file)
        
        config_host = config.get('Server', 'host')
        config_port = config.getint('Server', 'port')
        
        return (config_host, config_port)
        
    def exit(self, msg):
        sys.stderr.write("Lippy: %s" % msg)
        sys.exit(1)
        
    def header(self):
        print(('=' * 38))
        print('LIPPY - host:%s   port:%s' % (self.host, self.port))
        print(('=' * 38))
        
    def start(self):
        try:
            self.server = socketserver.TCPServer((self.host, self.port), LippyHandler)
            print("Listening...")
            print(('-' * 38))
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\nLippy is done\n")
            print(('-' * 38))
            

#Socket request handler
#Things kept really simple here, only getting data in then closing connection
class LippyHandler(socketserver.BaseRequestHandler):

    def handle(self):
    
        #Get the data and where its come from
        data = self.request.recv(8192).strip().decode("utf-8")
        addr = self.client_address[0]
        
        #Output that data
        lipout = LippyOutput(data, addr)
        lipout.output()
        
        #Let the connection go
        
        
class LippyOutput:

    data = None
    address = None
    json = None
        
    lvl_str = None
    lvl  = None
    msg  = None
    logged_data = None

    def __init__(self, data, address):
    
        self.data = data
        self.address = address
        
        #Decode json
        try:
            self.json = json.loads(self.data)
        except ValueError:
            print("Unable to decode JSON")
            return
            
        
        #Get message details
        self.lvl  = self.json['lvl']
        self.msg  = self.json['msg']
        
        if 'data' in self.json:
            self.logged_data = self.json['data']
            
        #Get level string
        if self.lvl == 1:
            self.lvl_str = 'DEBUG'
        elif self.lvl == 2:
            self.lvl_str = 'INFO'
        elif self.lvl == 3:
            self.lvl_str = 'WARNING'
        elif self.lvl == 4:
            self.lvl_str = 'ERRROR'
        elif self.lvl == 5:
            self.lvl_str = 'CRITICAL'
        else:
            self.lvl = 3
            self.lvl_str = 'WARNING'
            
    def output(self):

        #Output header with correct colours for platform
        colour.output(self.lvl, self.lvl_str, self.address)
           
        print("%s\n" % self.msg)
        
        if self.logged_data is not None:
            print("Data:")
            print(json.dumps(self.logged_data, sort_keys = True, indent = 4))
            print('')

        print(('-' * 38))
    
# -----------------------------------------------
#   Setup and run Lippy
# -----------------------------------------------
if __name__ == "__main__":
        
    #Setup up Lippy and run server
    #Use ctrl/cmd + c to exit
    lip = Lippy()
    lip.header()
    lip.start()