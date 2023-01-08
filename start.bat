:start
    git pull > tmp.txt
    set tmp_var = <tmp.txt
    set b = fatal
    echo %tmp_var%| findstr %b% >nul && (
        echo time out re run get pull...
    ) || (
        echo success, start run App...
        goto :runApp
    )
:runApp
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
    python app.py
for /l %a in (0,0,1) do goto :start