from flask import Flask, request
import random


filename = "glosor.txt"
lista = []

with open(filename, "rb") as file:
    lines = file.readlines()

for line in lines:
    line_decoded = line.decode("utf-8")
    words = line_decoded.split()
    for word in words:
            lista.append(word)

print(lista)
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    r = random.randint(1, 12)
    if request.method == 'POST' or index == 0:
        input_value = request.form['input']
        print("Din input: " + str(input_value))
        print("Rätt svar var: " + lista[r-1])
        if input_value == lista[r-1]:
            r = random.randint(1, 12)
            print("Du svarade rätt! ")

    return '''
        <p>  </p>
        <p> Hur stavar man ''' + str(lista[r-1]) + ''' </p>
        <audio controls>
        <source src="C:/Users/MartinBlomström/Downloads/småpotatis.mp3" type="audio/mpeg">
        <source src="småpotatis.ogg" type="audio/ogg">
        Your browser does not support the audio element.
        </audio>
        <form method="post">
            Input: <input type="text" name="input">
            <input type="submit" value="Submit">
        </form> '''


if __name__ == '__main__':
    app.run(debug=True)