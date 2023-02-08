vokaler = "aeiouy"
mening = str(input("Skriv en mening på svenska: "))
index = 0
mellanslag = 0
for letter in mening:
    if letter == " ":
        mellanslag += 1
print(str(len(mening) - mellanslag) + " är antalet bokstäver")
for letter in mening:
    if index + 3 <= len(mening):
        if letter in vokaler and mening[index+1] not in vokaler and mening[index+2] not in vokaler:
            print(letter + " är en snabb vokal ")
            mening = mening.replace(mening[index], "" )
    elif index + 2 <= len(mening):
        if letter in vokaler and mening[index + 1]:
            print(letter + " är en snabb vokal ")
            mening = mening.replace(mening[index], "")
    elif len(mening) == 1 and letter in vokaler:
        print(letter + " är en vokal, varken snabb eller långsam ")
        mening = mening.replace(mening[index], "")
    index += 1
index = 0
ReverseMening = ""
while index < len(mening):
    ReverseMening += mening[len(mening)-1 - index]
    index += 1
print("Meningen omvänd blir " + "\"" + ReverseMening + "\"" +" omman vänder på meningen utan snabba vokaler")