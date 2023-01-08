@echo off
:start
    git pull > tmp.txt
    set tmp_var=<tmp.txt
    del tmp.txt
    echo %tmp_var%| findstr 'fatal' >nul && (
        echo 'time out reGet...'
    ) || (
        echo 'success, start run App...'
        goto :runApp
    )
:runApp
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
    python app.py
for /l %a in (0,0,1) do goto :start