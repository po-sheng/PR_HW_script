import os 
import shutil
import rarfile
from termcolor import colored       
import subprocess
import zipfile37 as zipfile


def unzip(fileName, dest):
    zipFile = zipfile.ZipFile(fileName)
    for name in zipFile.namelist():
        zipFile.extract(name, dest)
    zipFile.close()
    os.chdir(dest)

def unrar(fileName, dest):
    rarFile = rarfile.RarFile(fileName)
    rarFile.extractall(dest)
    rarFile.close
    os.chdir(dest)

if __name__ == "__main__":
#     folderPath = "../hw_test"
    folderPath = "/mnt/c/Users/bensonliu/Desktop/pr_TA/HW1/HW1_Regression"
    startFrom = 1               # start from first student
    os.chdir(folderPath)

    folders = sorted(os.listdir("."))
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
            continue
        if len(file_list) == 0:
            print(colored("\t\tDidn't upload anything!", "red"))
            continue
        if not file_list[0].endswith(".zip") and not file_list[0].endswith(".rar"):
            print(colored("\t\tUploaded file not a .zip or .rar file!", "red"))
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
        else
            print(colored("\t\tBroken ZIP file: "+zipFile, "red"))
            continue
        
        print(colored("\t\tPass!!", "green"))    
    
        pdf = name+".pdf"
        nb = name+".ipynb"
        py = name+".py"

        # check for wrond folder hierarchy
        print("\tChecking folder hierarchy...")
        if os.path.isdir(name):
            print(colored("\t\tWrong folder hierarchy!", "red"))
            pdf = os.path.join(folder, name+".pdf")
            nb = os.path.join(folder, name+".ipynb")
            py = os.path.join(folder, name+".py")
        else:
            print(colored("\t\tPass!!", "green"))

        # check for missing file
        print("\tChecking for missing file...")
        for files in os.listdir("."):
            if not files.endswith(".pdf") and not files.endswith(".ipynb"):
                print(colored("\t\tContain additional file " + files + "!", "red"))
        if not os.path.exists(pdf) or not os.path.exists(nb): 
            if not os.path.exists(pdf):
                print(colored("\t\tLoss PDF file!", "red"))
            if not os.path.exists(nb):
                print(colored("\t\tLoss ipynb file!", "red"))
        else:
            print(colored("\t\tPass!!", "green"))

        # convert .ipynb to .py
        try:
            ret = subprocess.run(["ipynb-py-convert", nb, py])
        except:
            print(colored("Error when converting .ipynb to .py!", "red"))

        # check if code meet PEP8 require
        print("\tChecking python coding style...")
#         ret = subprocess.run(["pycodestyle", "--statistics", "--show-source", "--show-pep8", py], capture_output=True, text=True)
        ret = subprocess.run(["pycodestyle", "--select=E2, W2", py], capture_output=True, text=True)

        for info in ret.stdout.split('\n'):
            if info.find("E") != -1:
                print(colored("\t\t"+info, "red"))
            else:
                print(colored("\t\t"+info, "yellow"))

        # open PDF file
#         ret = subprocess.Popen(["evince", pdf])
        ret = subprocess.Popen(["okular", pdf])
        ret.wait()
        
        # back to original dir and remove extract file
        os.chdir("../")
        shutil.rmtree(dest)
        os.chdir("../")
        
        print()
        input("Press the <Enter> key to next student...")

