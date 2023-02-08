
h = 0.00001
x4 = int(input("Välj konstanten a till polynomutrycket (ax^4 + bx^3 + cx^2 + dx + e) "))
x3 = int(input("Välj konstanten b till polynomutrycket (ax^4 + bx^3 + cx^2 + dx + e) "))
x2 = int(input("Välj konstanten c till polynomutrycket (ax^4 + bx^3 + cx^2 + dx + e) "))
x1 = int(input("Välj konstanten d till polynomutrycket (ax^4 + bx^3 + cx^2 + dx + e) "))
x0 = int(input("Välj konstanten e till polynomutrycket (ax^4 + bx^3 + cx^2 + dx + e) "))
d = int(input("Välj ett startvärde för integralen: "))
e = int(input("Välj ett slutvärde för integralen: "))
integral = 0
z = d
def f(x):
    return x4*x**4 + x3*x**3 + x2*x**2 + x1*x + x0
while z < e:
    z += h
    integral += abs(f(z) * h)
    print(integral)
print(integral)
import turtle
turtle.speed(100)
z = d
print(z)
turtle.begin_fill()
turtle.forward(1800)
turtle.right(180)
turtle.forward(1800)
turtle.right(90)
turtle.forward(1800)
turtle.right(180)
turtle.forward(1800)
turtle.right(90)
turtle.forward(1800)
turtle.right(180)
turtle.forward(1800)
turtle.right(90)
turtle.forward(1800)
turtle.right(180)
turtle.forward(1800)
turtle.right(90)

while z < e:
    if z < 0:
        turtle.color("blue")
        turtle.right(90)
        turtle.setx(z*2)
        turtle.sety(f(z)*2)
        turtle.forward(f(z)*2)
        z += 0.2
        turtle.left(90)
    else:
        turtle.color("blue")
        turtle.right(90)
        turtle.setx(z * 2)
        turtle.sety(f(z) * 2)
        turtle.forward(f(z) * 2)
        z += 0.2
        turtle.left(90)
turtle.hideturtle()
turtle.exitonclick()

