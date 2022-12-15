@echo off 
echo Checking dependencies...
pip freeze | Find "pyperclip==1.8.2" > NUL || pip install pyperclip==1.8.2
pip freeze | Find "selenium==4.7.2" > NUL || pip install selenium==4.7.2
python main.py
pause