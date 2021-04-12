import os
import sys
import glob
import time
import signal
import shutil
import rarfile
import threading
import subprocess
import zipfile37 as zipfile
from termcolor import colored       


# thread for detecting stop signal
def detect_break():
    ret = input(colored("Press the <Enter> key to pause!\n\n", "yellow"))

# signal (crtl + c) handler
def sig_handler(sig, frame):
    global input_thread
    os.chdir("../")
    if os.path.exists(glob.glob("*_files")[0]) and os.path.isdir(glob.glob("*_files")[0]):
        shutil.rmtree(glob.glob("*_files")[0])
    print(colored("\nStop by signal interrupt!\n", "yellow"))
    os._exit(1)

# clean up state variable when continue to new student
def refresh_state():
    os.chdir("../")
    global input_thread
    
    print(colored("\nPress the <Enter> key to continue...", "yellow"), flush=True, end="")
    input_thread.join()
    input_thread = threading.Thread(target=detect_break)
    input_thread.start()

# unzip .zip file
def unzip(fileName, dest):
    zipFile = zipfile.ZipFile(fileName)
    for name in zipFile.namelist():
        zipFile.extract(name, dest)
    zipFile.close()
    os.chdir(dest)

# unzip .rar file
def unrar(fileName, dest):
    rarFile = rarfile.RarFile(fileName)
    rarFile.extractall(dest)
    rarFile.close
    os.chdir(dest)

if __name__ == "__main__":
    # check argv correct
    try:
        startFrom = int(sys.argv[1])    # start from which student
    except:
        print(colored("You should specify the int index of student to start from as an argv!", "red"))
        exit()

    # set path
    folderPath = "/mnt/c/Users/bensonliu/Desktop/pr_TA/HW1/HW1_Regression"
    os.chdir(folderPath)
    
    # set signal handler
    signal.signal(signal.SIGINT, sig_handler)

    # set break threading
    input_thread = threading.Thread(target=detect_break)
    input_thread.start()

    # loop for submit homework
    folders = sorted(os.listdir("."))
    if startFrom <= 0 or startFrom > len(folders):
        print(colored("The range of index should be between [1, {}]".format(len(folders)), "red"))
        exit()
    for i, folder in enumerate(folders):
        if i+1 < startFrom:
            continue

        os.chdir(folder)
        print(colored(str(i+1)+": ", "cyan"), end='')
        print(folder)
        
        # check uploaded zip file
        print("\tChecking uploaded file...")
        file_list = os.listdir(".")
        if len(file_list) > 1:
            print(colored("\t\tUpload more than one file!", "red"))
            refresh_state()
            continue
        if len(file_list) == 0:
            print(colored("\t\tDidn't upload anything!", "red"))
            refresh_state()
            continue
        if not file_list[0].endswith(".zip") and not file_list[0].endswith(".rar"):
            print(colored("\t\tUploaded file not a .zip or .rar file!", "red"))
            refresh_state()
            continue
        
        # upzip .zip or .rar file
        zipFile = file_list[0]
        name = zipFile.split(".")[0]
        dest = name + "_files"
        if not os.path.isdir(dest):
            os.mkdir(dest)
        if zipFile.endswith(".zip") and zipfile.is_zipfile(zipFile):
            unzip(zipFile, dest)
        elif zipFile.endswith(".rar") and rarfile.is_rarfile(zipFile):
            unrar(zipFile, dest)
        else:
            print(colored("\t\tBroken ZIP file: "+zipFile, "red"))
            if os.path.isdir(dest):
                shutil.rmtree(dest)
            refresh_state()
            continue
        
        print(colored("\t\tPass!!", "green"))    
    
        pdf = name+".pdf"
        nb = name+".ipynb"
        py = name+".py"

        # check for wrond folder hierarchy
        print("\tChecking folder hierarchy...")
        if os.path.isdir(name):
            print(colored("\t\tWrong folder hierarchy!", "red"))
            inside_files = os.listdir(name)
            for inside_file in inside_files:
                shutil.move(os.path.join(name, inside_file), inside_file)
            shutil.rmtree(name)
        else:
            print(colored("\t\tPass!!", "green"))

        # check for missing file
        print("\tChecking for missing file...")

        if os.path.exists(pdf) and (os.path.exists(nb) or os.path.exists(py)) and len(os.listdir(".")) == 2:
            print(colored("\t\tPass!!", "green"))
        else:
            for files in os.listdir("."):
                if not files.endswith(".pdf") and not files.endswith(".ipynb") and not files.endswith(".py"):
                    print(colored("\t\tContain additional file " + files + "!", "red"))
            if not os.path.exists(pdf):
                if len(glob.glob("*.pdf")) != 0:
                    print(colored("\t\tWrong PDF file name!", "red"))
                    os.rename(glob.glob("*.pdf")[0], pdf)
                else:
                    print(colored("\t\tLoss PDF file!", "red"))
            if not os.path.exists(nb) and not os.path.exists(py):
                if len(glob.glob("*.ipynb")) != 0 or len(glob.glob("*.py")) != 0:
                    print(colored("\t\tWrong .py/.ipynb file name!", "red"))
                    if not os.path.exists(nb) and len(glob.glob("*.ipynb")) != 0:
                        os.rename(glob.glob("*.ipynb")[0], nb)
                    if not os.path.exists(py) and len(glob.glob("*.py")) != 0:
                        os.rename(glob.glob("*.py")[0], py)
                else:
                    print(colored("\t\tLoss ipynb file!", "red"))

        # convert .ipynb to .py
        if not os.path.exists(py) and os.path.exists(nb):
            try:
                ret = subprocess.run(["ipynb-py-convert", nb, py])
            except:
                print(colored("Error when converting .ipynb to .py!", "red"))

        # check if code meet PEP8 require
        if os.path.exists(py):
            print("\tChecking python coding style...")
#             ret = subprocess.run(["pycodestyle", "--statistics", "--show-source", "--show-pep8", py], capture_output=True, text=True)
            ret = subprocess.run(["pycodestyle", "--select=E20, E21, E23, E24", py], 
                    capture_output=True, text=True)

            info_list = ret.stdout.split('\n')
            if len(info_list) == 1 and info_list[0] == "":
                print(colored("\t\tPass!!", "green"))
            else:
                for info in info_list:
                    if info.find("E") != -1:
                        print(colored("\t\t"+info, "red"))
                    else:
                        print(colored("\t\t"+info, "yellow"))

        # open PDF file
        if os.path.exists(pdf):
#             ret = subprocess.Popen(["evince", pdf])
            ret = subprocess.Popen(["okular", pdf])
            ret.wait()
        else:
            refresh_state()
            shutil.rmtree(dest)
            os.chdir("../")
            continue
        
        # back to original dir and remove extract file
        os.chdir("../")
        shutil.rmtree(dest)
        os.chdir("../")
        
        if not input_thread.is_alive():
            input_thread.join()
            input(colored("Press the <Enter> key to continue...", "yellow"))
            input_thread = threading.Thread(target=detect_break)
            input_thread.start()
        else:
            print()

