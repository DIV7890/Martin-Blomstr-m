
while True:
    inputV = float(input("Skriv Hastigheten: "))
    inputM = float(input("Skriv Massan: ")) + 0.273
    Kinetisk_energi = inputV * inputV * inputM / 2
    print("Kinetisk energi: " + str(Kinetisk_energi))