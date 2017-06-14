 __   ___  __   __   __     __  
|__) |__  |  \ |__) /  \ | |  \ 
|  \ |___ |__/ |  \ \__/ | |__/
      v0.7 - ethaniel.me

Requirements:
  apktool 2.2.3


Usage:
To initialize a new workspace in the CWD, use
  > redroid.py /path/to/target.apk
Once a workspace has been created, you can use the above to add a new branch or simply use
  > redroid.py

Commands:
  branch <description>	Branches modified.apk with a new description
  clear                 Clears the command line and prints branch list
  decompile             Decompiles the original.apk of current branch
  exit                  Exits the program
  help                  Shows this help dialog
  install               Install modified.apk to an adb device
  recompile             Recompiles the branch into modified.apk
  remove                Deletes the current branch
  reset                 Removes all decompiled/modified source code
  show                  Opens the current branch in a file browser
  sign                  Signs the apk
  switch/select <#>     Selects branch #


Obligatory Note:
This project was supported in part by an assignment with the Secretary's Honors Program Cyber Student Volunteer Initiative sponsored by the U.S. Department of Homeland Security (DHS). This program is administered by the Oak Ridge Institute for Science and Education (ORISE) through an interagency agreement between the US. Department of Energy (DOE) and DHS. ORISE is managed by ORAU under contract with DOE.
