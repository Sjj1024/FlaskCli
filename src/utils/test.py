import re


dengji = "Lv1 初涉江湖"

deng = re.search("\d", dengji).group(0)

print(deng)