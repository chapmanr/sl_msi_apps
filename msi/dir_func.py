import os
import glob
import sys
from os import path
import psutil
import fnmatch
from distutils.dir_util import copy_tree

def create_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

def delete_dir(path):
    try:
        os.rmdir(path)
    except OSError:
        print ("Deletion of the directory %s failed" % path)
    else:
        print ("Successfully deleted the directory %s" % path)

def exists_dir(path):
    return os.path.isdir(path)

def exists_file(filename):
    return os.path.isfile(filename)

def delete_files_dir(path):
    files = glob.glob(path)
    for f in files:
        os.remove(f)


def check_create_dir(path, clearfiles=True):
    if not exists_dir(path):
        create_dir(path)
    elif clearfiles == True:
        delete_files_dir(path)
    if(exists_dir(path)):
        return True
    return False

def copy_all(srcdir, destdir):
    return copy_tree(srcdir, destdir)

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

def getdirname(path):
    #if(os.path.isdir(path)):
    dir_parts = splitall(path)
    if len(dir_parts) > 0:
        return dir_parts[len(dir_parts)-1]
    return None

def getdirparent(path):
    dir_parts = splitall(path)
    if len(dir_parts) > 1:
        parent=""
        for i in range(0, len(dir_parts)-1):
            parent = parent + dir_parts[i]
        return parent
    return None

def is_file_exists(filename):
    if path.exists(filename) and path.isfile(filename):
        return True
    return False

def list_drives():
    #I think we need only the mount points
    mounts = []
    for a_disk in  psutil.disk_partitions():
        mounts.append(a_disk[1])
    return mounts

def list_all_objs(path, pattern="*.*"):
    matched_dirs = []
    if(exists_dir(path)):
        dirs = os.listdir(path)
        for entry in dirs:
            if fnmatch.fnmatch(entry, pattern):
                matched_dirs.append(entry)
    return matched_dirs

def home_dir():
    return os.path.expanduser('~')

if(__name__=="__main__"):
    print(str(splitall("C:/data/May4_kidney_serial_S22 Analyte 1.raw/imaging")))
    print(str(list_drives()))
    print("--------------------------------------------------------")
    #print(str(list_all_objs("G:/Maldi_3D")))
    #print("--------------------------------------------------------")
    print(str(list_all_objs('D:/MouseDataRaw', "*.raw")))
    #print("--------------------------------------------------------")
    #print(str(list_all_objs("G:/Maldi_3D", "*.jpeg")))
    print(str(home_dir()))
    #docs = str(home_dir) + "/Documents"
    #print(str(list_all_objs(str(home_dir()))))
    