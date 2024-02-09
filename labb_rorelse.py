while True:
    inputV = float(input("Va hastigheten: "))
    inputM = float(input("Va massan: ")) + 0.273
    rorelse_energi = inputV*inputM
    print("Rörelsemängd: " + str(rorelse_energi))