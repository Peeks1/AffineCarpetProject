import turtle as t

def draw_sierpinski_triangle(length, level):
    if level == 0:
        t.color('red', 'yellow')
        t.begin_fill()
        for i in range(0, 3):
            t.fd(length)
            t.left(120)
        t.end_fill()
    else:
        t.begin_fill()
        draw_sierpinski_triangle(length / 2, level - 1)
        t.fd(length / 2)
        draw_sierpinski_triangle(length / 2, level - 1)
        t.bk(length / 2)
        t.left(60)
        t.fd(length / 2)
        t.right(60)
        draw_sierpinski_triangle(length / 2, level - 1)
        t.left(60)
        t.bk(length / 2)
        t.right(60)


def main():
    t.pensize(3)
    # to ask user for depth question
    level = int(input('Enter the number for depth: '))
    draw_sierpinski_triangle(200, level)
    t.done()


main()
