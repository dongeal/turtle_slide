list =[[1,2,3],[4,5,6],[7,8,9]]
t= 5
for i ,factor in enumerate(list):
    print(i, factor)
    if t in factor:
        print(i, factor.index(t))

import turtle

screen = turtle.Screen()

key = turtle.Turtle()
key.shapesize(5)

screen.onclick(lambda a,b :key.goto(a,b))



turtle.mainloop()