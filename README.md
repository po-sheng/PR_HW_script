# Introduction
This script is for Pattern Recognition coarse homework in NYCU by Prof. Yen-Yu Lin. 
The student submit .zip or .rar file contain .ipynb coding file and .pdf writing and answering file. The script will check the submit format of each student and check if the code meet the need of PEP8 python whitespace coding style. At the end, open the PDF file for TA to grade easily.

# Requirements
- Some ubuntu packages should be install by `sudo apt install` in **apt_install.txt**
    - `evince` and `okular` are PDF reader for linux, you should choose one of them to install
    - `evince` is a more lightweight version
- Some required python packages are in **requirements.txt**
    - The number of `zipfile37` represent the version of python, you should modify to your own environment

# Check Items
- Only upload a ZIP file
- Only contain a .pdf file and .ipynb in ZIP file
- Whether an additional folder outside of .pdf and .ipynb (folder hierarchy)
- Whether the code in .ipynb follow the requirement of whitespace rule in PEP8 coding style

# Quick Start
### 1. Enter Main program
```
cd PR_HW_script
vim HWscript.py
```

### 2. modify your own settings in **HWscript.py**
```
import zipFile[python version num] as zipFile

...

folderPath = <your own path to hw_dir>

...

ret = subprocess.Popen("okular", pdf)   # change "okular" to "evince" depends on your PDF reader
```

### 3. Run the program
```
python3 HWscript.py 1
```
- argv[2] (which is "1" here) represent the index of starting student, from 1 to N

### 4. Usage
- Press < Enter> key to pause the program
- System call of <Ctrl + c> to stop the program
