import subprocess
ans = 25
while ans > 24:
    ans = int(input("Hur mycket cs har du spelat idag? "))
    if ans < 24 :
        subprocess.call("C:\Program Files (x86)\Steam\Steam.exe -applaunch 730")
    else:
        print("Omöjligt... \n")
