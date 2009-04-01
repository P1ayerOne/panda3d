#!/usr/bin/python
########################################################################
#
# Caution: there are two separate, independent build systems:
# 'makepanda', and 'ppremake'.  Use one or the other, do not attempt
# to use both.  This file is part of the 'makepanda' system.
#
# To install panda using this script, type 'installpanda.py'.
# To specify an alternate location than the filesystem root /,
# set the DESTDIR environment variable.
# This script only functions on Linux, for now.
#
########################################################################

import os, sys, platform, compileall
from distutils.sysconfig import get_python_lib
from makepandacore import *

if (platform.architecture()[0] == "64bit"):
  libdir = "/lib64"
else:
  libdir = "/lib"

def InstallPanda(destdir="", prefix="/usr", outputdir="built"):
    if (not prefix.startswith("/")): prefix = "/" + prefix
    PPATH=get_python_lib()
    oscmd("mkdir -p "+destdir+prefix+"/bin")
    oscmd("mkdir -p "+destdir+prefix+"/include")
    oscmd("mkdir -p "+destdir+prefix+"/share/panda3d")
    oscmd("mkdir -p "+destdir+prefix+"/share/panda3d/direct")
    oscmd("mkdir -p "+destdir+prefix+libdir+"/panda3d")
    oscmd("mkdir -p "+destdir+prefix+libdir+"/"+os.path.abspath(PPATH+"/../lib-dynload"))
    oscmd("mkdir -p "+destdir+prefix+libdir+"/"+PPATH+"/site-packages")
    oscmd("mkdir -p "+destdir+"/etc/ld.so.conf.d")
    WriteFile(destdir+prefix+"/share/panda3d/direct/__init__.py", "")
    oscmd("sed -e 's@model-cache-@# model-cache-@' -e 's@$THIS_PRC_DIR/[.][.]@"+prefix+"/share/panda3d@' < "+outputdir+"/etc/Config.prc > "+destdir+"/etc/Config.prc")
    oscmd("cp "+outputdir+"/etc/Confauto.prc    "+destdir+"/etc/Confauto.prc")
    oscmd("cp -R "+outputdir+"/include          "+destdir+prefix+"/include/panda3d")
    oscmd("cp -R direct/src/*                   "+destdir+prefix+"/share/panda3d/direct")
    oscmd("cp -R "+outputdir+"/pandac           "+destdir+prefix+"/share/panda3d/pandac")
    oscmd("cp -R "+outputdir+"/models           "+destdir+prefix+"/share/panda3d/models")
    if os.path.isdir("samples"):             oscmd("cp -R samples               "+destdir+prefix+"/share/panda3d/samples")
    if os.path.isdir(outputdir+"/Pmw"):      oscmd("cp -R "+outputdir+"/Pmw     "+destdir+prefix+"/share/panda3d/Pmw")
    if os.path.isdir(outputdir+"/plugins"):  oscmd("cp -R "+outputdir+"/plugins "+destdir+prefix+"/share/panda3d/plugins")
    oscmd("cp doc/LICENSE                       "+destdir+prefix+"/share/panda3d/LICENSE")
    oscmd("cp doc/LICENSE                       "+destdir+prefix+"/include/panda3d/LICENSE")
    oscmd("cp doc/ReleaseNotes                  "+destdir+prefix+"/share/panda3d/ReleaseNotes")
    oscmd("echo '"+prefix+libdir+"/panda3d'>    "+destdir+"/etc/ld.so.conf.d/panda3d.conf")
    oscmd("echo '"+prefix+"/share/panda3d' >    "+destdir+prefix+libdir+PPATH+"/panda3d.pth")
    oscmd("echo '"+prefix+libdir+"/panda3d'>>   "+destdir+prefix+libdir+PPATH+"/panda3d.pth")
    oscmd("cp "+outputdir+"/bin/*               "+destdir+prefix+"/bin/")
    for base in os.listdir(outputdir+"/lib"):
        oscmd("cp "+outputdir+"/lib/"+base+" "+destdir+prefix+libdir+"/panda3d/"+base)
    # rpmlint doesn't like it if we compile it.
    #for base in os.listdir(destdir+prefix+"/share/panda3d/direct"):
    #    if ((base != "extensions") and (base != "extensions_native")):
    #        compileall.compile_dir(destdir+prefix+"/share/panda3d/direct/"+base)
    #compileall.compile_dir(destdir+prefix+"/share/panda3d/Pmw")
    DeleteCVS(destdir)
    # rpmlint doesn't like these files, for some reason.
    DeleteCXX(destdir+"/usr/share/panda3d")
    if (os.path.isfile(destdir+"/usr/share/panda3d/direct/leveleditor/copyfiles.pl")):
      os.remove(destdir+"/usr/share/panda3d/direct/leveleditor/copyfiles.pl")

if (__name__ == "__main__"):
    if (sys.platform != "linux2"):
        exit("This script only works on linux at the moment!")
    destdir = ""
    if (os.environ.has_key("DESTDIR")):
        print "Reading out DESTDIR"
        destdir = os.environ["DESTDIR"]
        if (destdir.endswith("/")):
            destdir = destdir[:-1]
        if (destdir != "" and not os.path.isdir(destdir)):
            exit("Directory '%s' does not exist!" % destdir)
        print "Installing Panda3D into " + destdir
    else:
        print "Installing Panda3D into /"
    InstallPanda(destdir)
    print "Install done!"
