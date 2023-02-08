file = open("myfile.txt", "w")
text1 = str(input("Välj någonting att skriva i filen: "))
file.write(text1) #För att skriva in inputen i dokumentet
file.write("\n")
file.write("\n")
file.write(text1)
file.close() #Stänger filen för att kunna öppna den i "read-läge"
file = open("myfile.txt", "r+")
print("\"file read(24)\": \n" + file.read(24)) #Skillnad mellan "file.read" och "file.readline"
print("\n")
file.seek(0) #För att börja om från toppen av dokumentet.
print("\"file readline(24)\": \n" + file.readline(24))
