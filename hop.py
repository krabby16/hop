#!/usr/bin/python3
import pexpect
import os, sys
import datetime
import json

USERNAME = 'CA759063'

DIR = os.path.abspath(os.path.dirname(__file__)) + '/'

#=======================================================
#Colors
#=======================================================

PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
DYELLOW = "\033[33m"
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
ENDC = '\033[0m'

#========================================================
#Classes
#========================================================

class Hopserver():
    def __init__(self, server, env = "prd"):
        self.ssh_newkey = 'Are you sure you want to continue connecting'

        try:
            self.jump = GetJump(server, env)
            self.server = self.jump["name"]
            self.host = self.jump["ip"]
            self.username = 'ca759063'
            self.password = GetPass('ca-account')
        except:
            #Default hopserver
            print("*HOP: Wrong hopserver settings, default is WEUR")
            self.server = "weur"
            self.host = '10.5.128.69'
            self.username = 'ca759063'
            self.password = GetPass('ca-account')

    def Login(self):
        print("*HOP: Logging in to " + self.server)
        self.child=pexpect.spawn('ssh ' + self.username + '@' + self.host, timeout=30)
        i = self.child.expect([self.ssh_newkey,'assword',pexpect.EOF,pexpect.TIMEOUT],5)
        if i==0:
            print("*HOP: Processing RSA fingerprint")
            self.child.sendline('yes')
            #i=self.child.expect([self.ssh_newkey,'assword:',pexpect.EOF])
        if i == 1:
            print("*HOP: Entering password for " + self.server)
            self.child.sendline(self.password)
        if i == 2:
            print("*HOP: Key or connection timeout")
            return 'timeout'
        if i == 3: #timeout
            print("*HOP: Connection to "+ self.server +" timed out")
            return 'timeout'
        return (self.child, self.child.before)

    def LoginNext(self, host, username, password, prompt):
        print("*HOP: Logging in to "+ host)
        #self.child.expect(self.server)
        self.child.sendline('ssh -l '+ username + ' ' + host)
        i=self.child.expect(["assword", self.ssh_newkey])
        if i == 0:
            self.child.sendline(password)
        if i == 1:
            print("*HOP: Processing RSA fingerprint")
            self.child.sendline('yes')
            #i=self.child.expect([self.ssh_newkey,'assword:',pexpect.EOF])              

        i=self.child.expect([prompt,pexpect.TIMEOUT,pexpect.EOF])
        if i == 0:
            self.child.sendline('')
        if i == 1:
            print("*HOP: Connection to host timed out")
            return False
        if i == 2:
            print("*HOP: Wrong password for "+prompt)
            return False

        return (self.child, self.child.before)

    def Interact(self):
        self.child.interact()

#========================================================
#Global Functions
#========================================================
def ShowBanner():
    print(DYELLOW)
    print("                   (    (    ")
    print(" (  (       (      )\ ) )\ ) ")
    print(" )\))(   '  )\    (()/((()/( ")
    print("((_)()\ )((((_)(   /(_))/(_))"+ YELLOW)
    print("_(())\_)())\ _ )\ (_)) (_))  ")
    print("\ \((_)/ /(_)_\(_)| _ \| _ \ ")
    print(" \ \/\/ /  / _ \  |   /|  _/ " + BOLD)
    print("  \_/\_/  /_/ \_\ |_|_\|_|   v0.2")
    print(ENDC)

def Menu():
    print("")
    print("hop [weur | neur | seas | auea] [fw1 | fw2]")
    print("")
    print("[x] to exit")
    print("")
    return input('Select: ')

# Get data from JSON files
def GetPass(key):
    with open(DIR + 'passdb.json', 'r') as f:
        file = f.read()
    f.close()
    passdb = json.loads(file)
    return passdb[key]

def GetJump(key, env = "prd"):
    with open(DIR + 'jumpdb.json', 'r') as f:
        file = f.read()
    f.close()
    jumpdb = json.loads(file)
    return jumpdb[env][key]

def GetHost(region, key, env = "prd"):
    with open(DIR + 'hostdb.json', 'r') as f:
        file = f.read()
    f.close()
    hostdb = json.loads(file)
    return hostdb[env][region][key]

# Call login functions
def Login(server):
    Connection = Hopserver(server)
    if Connection.Login() == 'timeout':
        return
    #Give back control
    print("*HOP: Interaction was given back to you")
    Connection.Interact()

def HostLogin(server, host):
    Connection = Hopserver(server)
    if Connection.Login() == 'timeout':
        return
    else:
        if Connection.LoginNext(GetHost(server,host)["ip"], USERNAME, GetPass('ca-account'), '>') != False:
            #Give back control
            print("*HOP: Interaction was given back to you")
            Connection.Interact()

#========================================================
#Main Function
#========================================================
if __name__ == '__main__':

    #Processing arguments
    if len(sys.argv) == 2:
        Login(sys.argv[1])
    elif len(sys.argv) == 3:
        HostLogin(sys.argv[1], sys.argv[2])
    else:
        #If program is executed without arguments
        if len(sys.argv) == 1:
            #Infinite loop for main menu
            while True:
                ShowBanner()
                selected = Menu()

                #Rollout
                if selected == '1':
                    pass

                #Login to host
                elif selected == '2':
                    print("*HOP: Login selected")
                    Login('weur')

                #Exit program
                elif selected == 'x':
                    print("*HOP: Bye!")
                    sys.exit(0)

                #Wrong input
                else:
                    print("*HOP: Wrong input!")
