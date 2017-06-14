#!/usr/bin/env python3

import os
import sys
import subprocess


# CONFIG
keystorePath = os.path.expanduser("~") + "/android.keystore"
keyName = "debug"


version = "v0.8"
logo = " __   ___  __   __   __     __  \n|__) |__  |  \ |__) /  \ | |  \ \n|  \ |___ |__/ |  \ \__/ | |__/\n      "+version+" - ethaniel.me\n"
branches = list()
selectedBranch = -1
workspaceDir = ""

def writeDat():
    global branches, workspaceDir
    file = open(workspaceDir + "/redroid.dat", "w")
    for i in range(len(branches)):
        file.write(branches[i] + "\n")
    file.close()

def loadDat():
    global branches
    file = open(workspaceDir + "/redroid.dat", "r")
    branches = [line.strip() for line in file.readlines()]
    file.close()

def printHeader():
    global branches
    subprocess.run(["clear"])
    print(logo)
    i = 0
    for branch in branches:
        print("*" if i == selectedBranch else " ", end="")
        print(i, "  ", branch)
        i += 1
    print()

def printHelp():
    print(
        '''Commands:
  branch <description>	Branches modified.apk with a new description
  clear                 Clears the command line and prints branch list
  decompile             Decompiles the original.apk of current branch
  diff <branch #>       Outputs diff of current branch and arg branch
  exit                  Exits the program
  help                  Shows this help dialog
  install               Install modified.apk to an adb device
  recompile             Recompiles the branch into modified.apk
  remove                Deletes the current branch
  reset                 Removes all decompiled/modified source code
  show                  Opens the current branch in a file browser
  sign                  Signs the apk
  switch/select <#>     Selects branch #'''
    )

def poll():
    global branches, selectedBranch, keystorePath
    command = input("> ")
    if command.startswith("help"):
        printHelp()
    elif command.startswith("switch") or command.startswith("select"):
        args = command.split(' ')
        if len(args) < 2:
            print("Usage: select <branch #>")
        elif args[1].isdigit() and int(args[1]) < len(branches):
            selectedBranch = int(args[1])
            printHeader()
        else:
            print("Invalid branch #")
    elif command == "clear":
        printHeader()
    elif command == "exit":
        return
    elif selectedBranch != -1:
        moddedPath = workspaceDir + "/" + str(selectedBranch) + "/modified.apk"
        if command.startswith("branch"):
            args = command.split("branch ")
            if len(args) < 2:
                print("Usage: branch <description>")
            elif (os.path.isfile(moddedPath)):
                addBranch(moddedPath, command.lstrip('branch '))
                printHeader()
            else:
                print("Current branch has not been recompiled yet")
        elif command == "decompile" or command == "d":
            decompile(selectedBranch)
        elif command == "reset":
            subprocess.run(['rm', '-rf', workspaceDir + "/" + str(selectedBranch) + '/original/'])
        elif command == "recompile" or command == "r":
            recompile(selectedBranch)
        elif command == "remove":
            removeBranch(selectedBranch)
            printHeader()
        elif command.startswith("diff"):
            args = command.split(" ")
            if (len(args) < 2):
                print("Usage: diff <target #>")
            elif args[1].isdigit() and int(args[1]) < len(branches):
                diffProcess = subprocess.Popen(["diff", "-rq", str(selectedBranch) + "/", str(args[1]) + "/"], stdout=subprocess.PIPE)
                for line in iter(diffProcess.stdout.readline, b''):
                    print(line.decode('utf-8').strip())
            else:
                print("Invalid branch #")
        elif command == "sign":
            if (os.path.isfile(moddedPath)):
                signProcess = subprocess.Popen(['jarsigner', '-verbose', '-sigalg', 'SHA1withRSA', '-digestalg', 'SHA1', '-keystore', keystorePath, moddedPath, 'debug'], stdout=subprocess.PIPE)
                for line in iter(signProcess.stdout.readline, b''):
                    print(line.decode('utf-8').strip())
            else:
                print("Current branch has not been recompiled yet")
        elif command == "show":
            subprocess.run(['nautilus', workspaceDir+"/"+str(selectedBranch)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif command == "install":
            if (os.path.isfile(workspaceDir + "/" + str(selectedBranch) +"/modified.apk")):
                signProcess = subprocess.Popen(['adb', 'install', workspaceDir+'/'+str(selectedBranch)+'/modified.apk'], stdout=subprocess.PIPE)
                for line in iter(signProcess.stdout.readline, b''):
                    print(line.decode('utf-8').strip())
            else:
                print("Current branch has not been recompiled yet")
        else:
            print("Invalid command. Select a branch or type help for commands.")
    else:
        print("Invalid command. Select a branch or type help for commands.")
    poll()

def loadWorkSpace():
    global branches

    if (os.path.isfile("./redroid.dat")):
        loadDat()
        for i in range(len(branches)):
            if not os.path.isdir("./" + str(i)):
                print("Corrupted redroid.dat")
                return
    elif len(sys.argv) == 1:
        print("Workspace not detected. Use:")
        print("    redroid /path/to/target.apk")
        print("to initialize a workspace in the cwd")
        return

    if len(sys.argv) > 1:
        addBranch(sys.argv[1])

    printHeader()
    poll()

def addBranch(apkPath, desc=""):
    global branches, selectedBranch
    branchID = len(branches)
    os.chdir(workspaceDir)
    subprocess.run(["mkdir", str(branchID)])
    print("Created Directory")
    subprocess.run(["cp", apkPath, str(branchID) + "/original.apk"])
    print("Copied APK")
    decompile(branchID)
    if desc == "":
        desc = input("Enter a branch description: ")
    branches.append(desc)
    writeDat()
    selectedBranch = branchID

def removeBranch(branchID):
    global selectedBranch
    subprocess.run(["rm", "-rf", workspaceDir + "/" + str(branchID)])
    branches.pop(branchID)
    while branchID < len(branches):
        subprocess.run(["mv", workspaceDir + "/" + str(branchID+1), workspaceDir + "/" + str(branchID)])
        branchID += 1
    writeDat()
    selectedBranch = -1

def decompile(branchID):
    os.chdir(workspaceDir + "/" + str(branchID))
    decompileProcess = subprocess.Popen(["apktool", "d", "original.apk"], stdout=subprocess.PIPE)
    for line in iter(decompileProcess.stdout.readline, b""):
        print(line.decode("utf-8").strip())

def recompile(branchID):
    os.chdir(workspaceDir + "/" + str(branchID))
    recompileProcess = subprocess.Popen(["apktool", "b", "original"], stdout=subprocess.PIPE)
    for line in iter(recompileProcess.stdout.readline, b""):
        print(line.decode("utf-8").strip())
    moveProcess = subprocess.Popen(["cp", "./original/dist/original.apk", "./modified.apk"], stdout=subprocess.PIPE)
    for line in iter(moveProcess.stdout.readline, b""):
        print(line.decode("utf-8").strip())

if __name__ == "__main__":
    workspaceDir = os.getcwd()
    loadWorkSpace()