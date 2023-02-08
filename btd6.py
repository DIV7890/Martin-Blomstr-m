import subprocess
ans = "n"
while ans == "n":
    ans = str(input("Är du nörd? (y/n) "))
    if ans == "y":
        subprocess.call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 960090")
    else : print("Jo det är du, erkänn... \n")












