# Introduction
This script is for Pattern Recognition coarse homework in NYCU by Prof. Yen-Yu Lin. 
The student submit .zip or .rar file contain .ipynb coding file and .pdf writing and answering file. The script will check the submit format of each student and check if the code meet the need of PEP8 python whitespace coding style. At the end, open the PDF file for TA to grade easily.

# Requirements
- Some ubuntu packages should be install by `sudo apt install` in ==apt_install.txt==
    - `evince` and `okular` are PDF reader for linux, you should choose one of them to install
    - `evince` is a more lightweight version
- Some required python packages are in ==requirements.txt==
    - The number of `zipfile37` represent the version of python, you should modify to your own environment

# Quick start
1. Enter Main program
```
cd PR_HW_script
vim HWscript.py
```

2. modify your own settings
```
import zipFile[python version num] as zipFile

...

folderPath = <your own path to hw_dir>
startFrom = <the index of starting student>

...

ret = subprocess.Popen("okular", pdf)   # change "okular" to "evince" depends on your PDF reader
```

3. Run the program
```
python3 HWscript.py
```
