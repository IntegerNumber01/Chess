import pygame

'''
from text import text

The text function can generator and render text onto a pygame surface.
'''


def generate(character, x, y, pixel_size):
    coordinates = []

    def add(x, y):
        coordinates.append((x, y))

    def line(x, y, direction, length):
        for i in range(length):
            if direction == 'left':
                add(x + (pixel_size * i), y)
            else:
                add(x, y + (pixel_size * i))

    if character == 'a' or character == 'A':
        line(x + pixel_size, y, 'left', 2)
        line(x, y + pixel_size, 'down', 4)
        line(x + pixel_size, y + (pixel_size * 2), 'left', 2)
        line(x + (pixel_size * 3), y + pixel_size, 'down', 4)

    if character == 'b' or character == 'B':
        line(x, y, 'left', 3)
        line(x, y + pixel_size, 'down', 3)
        line(x, y + (pixel_size * 2), 'left', 3)
        line(x, y + (pixel_size * 4), 'left', 3)
        add(x + (pixel_size * 3), y + pixel_size)
        add(x + (pixel_size * 3), y + (pixel_size * 3))

    if character == 'c' or character == 'C':
        line(x, y + pixel_size, 'down', 3)
        line(x + pixel_size, y, 'left', 2)
        line(x + pixel_size, y + (pixel_size * 4), 'left', 2)
        add(x + (pixel_size * 3), y + pixel_size)
        add(x + (pixel_size * 3), y + (pixel_size * 3))

    if character == 'd' or character == 'D':
        line(x, y, 'left', 3)
        line(x, y + pixel_size, 'down', 3)
        line(x, y + (pixel_size * 4), 'left', 3)
        line(x + (pixel_size * 3), y + pixel_size, 'down', 3)

    if character == 'e' or character == 'E':
        line(x, y, 'left', 4)
        line(x, y + pixel_size, 'down', 3)
        line(x, y + (pixel_size * 2), 'left', 3)
        line(x, y + (pixel_size * 4), 'left', 4)

    if character == 'f' or character == 'F':
        line(x, y, 'down', 5)
        line(x + pixel_size, y, 'left', 3)
        line(x + pixel_size, y + (pixel_size * 2), 'left', 2)

    if character == 'g' or character == 'G':
        line(x + pixel_size, y, 'left', 2)
        line(x, y + pixel_size, 'down', 3)
        line(x + pixel_size, y + (pixel_size * 4), 'left', 2)
        line(x + (pixel_size * 3), y + (pixel_size * 2), 'down', 2)
        add(x + (pixel_size * 2), y + (pixel_size * 2))

    if character == 'h' or character == 'H':
        line(x, y, 'down', 5)
        line(x + (pixel_size * 3), y, 'down', 5)
        line(x + pixel_size, y + (pixel_size * 2), 'left', 2)

    if character == 'i' or character == 'I':
        line(x + (pixel_size / 2), y, 'left', 3)
        line(x + (pixel_size / 2), y + (pixel_size * 4), 'left', 3)
        line(x + ((pixel_size / 2) + pixel_size), y + pixel_size, 'down', 3)

    if character == 'j' or character == 'J':
        line(x + (pixel_size * 3), y, 'down', 4)
        line(x + pixel_size, y + (pixel_size * 4), 'left', 2)
        add(x, y + (pixel_size * 3))

    if character == 'k' or character == 'K':
        line(x, y, 'down', 5)
        add(x + pixel_size, y + (pixel_size * 2))
        add(x + (pixel_size * 2), y + pixel_size)
        add(x + (pixel_size * 3), y)
        add(x + (pixel_size * 2), y + (pixel_size * 3))
        add(x + (pixel_size * 3), y + (pixel_size * 4))

    if character == 'l' or character == 'L':
        line(x, y, 'down', 5)
        line(x + pixel_size, y + (pixel_size * 4), 'left', 3)

    if character == 'm' or character == 'M':
        line(x, y, 'down', 5)
        line(x + (pixel_size * 4), y, 'down', 5)
        add(x + pixel_size, y + pixel_size)
        add(x + (pixel_size * 2), y + (pixel_size * 2))
        add(x + (pixel_size * 3), y + pixel_size)

    if character == 'n' or character == 'N':
        line(x, y, 'down', 5)
        line(x + (pixel_size * 3), y, 'down', 5)
        add(x + pixel_size, y + pixel_size)
        add(x + (pixel_size * 2), y + (pixel_size * 2))

    if character == 'o' or character == 'O':
        line(x + pixel_size, y, 'left', 2)
        line(x + pixel_size, y + (pixel_size * 4), 'left', 2)
        line(x, y + pixel_size, 'down', 3)
        line(x + (pixel_size * 3), y + pixel_size, 'down', 3)

    if character == 'p' or character == 'P':
        line(x + pixel_size, y, 'left', 2)
        line(x, y, 'down', 5)
        line(x + pixel_size, y + (pixel_size * 2), 'left', 2)
        add(x + (pixel_size * 3), y + pixel_size)

    if character == 'q' or character == 'Q':
        line(x + pixel_size, y, 'left', 2)
        line(x, y + pixel_size, 'down', 3)
        line(x + (pixel_size * 3), y + pixel_size, 'down', 2)
        add(x + pixel_size, y + (pixel_size * 4))
        add(x + (pixel_size * 2), y + (pixel_size * 3))
        add(x + (pixel_size * 3), y + (pixel_size * 4))

    if character == 'r' or character == 'R':
        line(x, y, 'left', 3)
        line(x, y + pixel_size, 'down', 4)
        line(x + pixel_size, y + (pixel_size * 2), 'left', 2)
        add(x + (pixel_size * 3), y + pixel_size)
        add(x + (pixel_size * 2), y + (pixel_size * 3))
        add(x + (pixel_size * 3), y + (pixel_size * 4))

    if character == 's' or character == 'S':
        line(x + pixel_size, y, 'left', 3)
        add(x, y + pixel_size)
        line(x + pixel_size, y + (pixel_size * 2), 'left', 2)
        add(x + pixel_size * 3, y + (pixel_size * 3))
        line(x, y + (pixel_size * 4), 'left', 3)

    if character == 't' or character == 'T':
        line(x, y, 'left', 5)
        line(x + (pixel_size * 2), y + pixel_size, 'down', 4)

    if character == 'u' or character == 'U':
        line(x, y, 'down', 4)
        line(x + (pixel_size * 3), y, 'down', 4)
        line(x + pixel_size, y + (pixel_size * 4), 'left', 2)

    if character == 'v' or character == 'V':
        line(x, y, 'down', 2)
        line(x + (pixel_size * 4), y, 'down', 2)
        line(x + pixel_size, y + (pixel_size * 2), 'down', 2)
        line(x + (pixel_size * 3), y + (pixel_size * 2), 'down', 2)
        add(x + (pixel_size * 2), y + (pixel_size * 4))

    if character == 'w' or character == 'W':
        line(x, y, 'down', 5)
        line(x + (pixel_size * 4), y, 'down', 5)
        add(x + pixel_size, y + (pixel_size * 3))
        add(x + (pixel_size * 2), y + (pixel_size * 2))
        add(x + (pixel_size * 3), y + (pixel_size * 3))

    if character == 'x' or character == 'X':
        line(x, y, 'down', 2)
        line(x + (pixel_size * 3), y, 'down', 2)
        line(x + pixel_size, y + (pixel_size * 2), 'left', 2)
        line(x, y + (pixel_size * 3), 'down', 2)
        line(x + (pixel_size * 3), y + (pixel_size * 3), 'down', 2)

    if character == 'y' or character == 'Y':
        line(x, y, 'down', 2)
        line(x + (pixel_size * 4), y, 'down', 2)
        line(x + pixel_size, y + (pixel_size * 2), 'left', 3)
        line(x + (pixel_size * 2), y + (pixel_size * 3), 'down', 2)

    if character == 'z' or character == 'Z':
        line(x, y, 'left', 4)
        add(x + (pixel_size * 2), y + pixel_size)
        add(x + pixel_size, y + (pixel_size * 2))
        add(x, y + (pixel_size * 3))
        line(x, y + (pixel_size * 4), 'left', 4)

    ####################

    if character == 0 or character == '0':
        add(x + pixel_size, y)
        add(x + (pixel_size * 2), y)
        add(x + pixel_size, y + (pixel_size * 4))
        add(x + (pixel_size * 2), y + (pixel_size * 4))
        for i in range(3):
            i = i + 1
            add(x, y + (pixel_size * i))
        for i in range(3):
            i = i + 1
            add(x + (pixel_size * 3), y + (pixel_size * i))

    if character == 1 or character == '1':
        add(x + pixel_size, y + pixel_size)
        for i in range(5):
            add(x + (pixel_size * 2), y + (pixel_size * i))
        add(x + pixel_size, y + (pixel_size * 4))
        add(x + (pixel_size * 3), y + (pixel_size * 4))

    if character == 2 or character == '2':
        add(x, y + pixel_size)
        add(x + pixel_size, y)
        add(x + (pixel_size * 2), y)
        add(x + (pixel_size * 3), y + pixel_size)
        add(x + (pixel_size * 2), y + (pixel_size * 2))
        add(x + pixel_size, y + (pixel_size * 3))
        for i in range(4):
            add(x + (pixel_size * i), y + (pixel_size * 4))

    if character == 3 or character == '3':
        add(x, y + pixel_size)
        add(x + pixel_size, y)
        add(x + (pixel_size * 2), y)
        add(x + (pixel_size * 3), y + pixel_size)
        add(x + (pixel_size * 2), y + (pixel_size * 2))
        add(x + (pixel_size * 3), y + (pixel_size * 3))
        add(x + (pixel_size * 2), y + (pixel_size * 4))
        add(x + pixel_size, y + (pixel_size * 4))
        add(x, y + (pixel_size * 3))

    if character == 4 or character == '4':
        add(x, y + (pixel_size * 2))
        add(x + pixel_size, y + (pixel_size * 1))
        for i in range(5):
            add(x + (pixel_size * 2), y + (pixel_size * i))

        for i in range(4):
            add(x + (pixel_size * i), y + (pixel_size * 3))

    if character == 5 or character == '5':
        for i in range(4):
            add(x + (pixel_size * i), y)
        add(x, y + pixel_size)
        add(x, y + (pixel_size * 2))
        add(x + pixel_size, y + (pixel_size * 2))
        add(x + (pixel_size * 2), y + (pixel_size * 2))
        add(x + (pixel_size * 3), y + (pixel_size * 3))
        for i in range(3):
            add(x + (pixel_size * i), y + (pixel_size * 4))

    if character == 6 or character == '6':
        add(x + pixel_size, y)
        add(x + (pixel_size * 2), y)
        for i in range(3):
            i = i + 1
            add(x, y + (pixel_size * i))
        add(x + pixel_size, y + (pixel_size * 2))
        add(x + (pixel_size * 2), y + (pixel_size * 2))
        add(x + (pixel_size * 3), y + (pixel_size * 3))
        add(x + pixel_size, y + (pixel_size * 4))
        add(x + (pixel_size * 2), y + (pixel_size * 4))

    if character == 7 or character == '7':
        for i in range(3):
            add(x + (pixel_size * i), y)
        add(x + (pixel_size * 3), y + pixel_size)
        add(x + (pixel_size * 3), y + (pixel_size * 2))
        add(x + (pixel_size * 2), y + (pixel_size * 3))
        add(x + (pixel_size * 2), y + (pixel_size * 4))

    if character == 8 or character == '8':
        add(x + pixel_size, y)
        add(x + (pixel_size * 2), y)
        add(x + pixel_size, y + (pixel_size * 2))
        add(x + (pixel_size * 2), y + (pixel_size * 2))
        add(x + pixel_size, y + (pixel_size * 4))
        add(x + (pixel_size * 2), y + (pixel_size * 4))

        add(x, y + pixel_size)
        add(x + (pixel_size * 3), y + pixel_size)
        add(x, y + (pixel_size * 3))
        add(x + (pixel_size * 3), y + (pixel_size * 3))

    if character == 9 or character == '9':
        add(x + pixel_size, y)
        add(x + (pixel_size * 2), y)
        add(x, y + pixel_size)
        add(x + pixel_size, y + (pixel_size * 2))
        add(x + (pixel_size * 2), y + (pixel_size * 2))
        for i in range(3):
            i = i + 1
            add(x + (pixel_size * 3), y + (pixel_size * i))
        add(x + (pixel_size * 2), y + (pixel_size * 4))

    ####################

    if character == ':':
        add(x + pixel_size + (pixel_size / 2), y + pixel_size)
        add(x + pixel_size + (pixel_size / 2), y + (pixel_size * 4))

    return coordinates


def text(screen, string, startingX, startingY, color, pixel_size):
    string = string.upper()  # Converts string to all uppercase
    generated = []
    x = startingX

    # Downloads pixels
    for a in range(len(string)):
        for b in range(len(string[a])):
            for c in range(len(string[a][b])):
                basic = string[a][b]
                generated.append(generate(basic[c], x, startingY, pixel_size))

    # Draws pixels
    for a in range(len(generated)):
        for b in range(len(generated[a])):
            basic = generated[a][b]
            pygame.draw.rect(screen, color, (basic[0] + x, basic[1],
                                             pixel_size, pixel_size))
        for i in range(len(string)):
            if string[a] == 'I':
                x = x + (pixel_size * 3) + (pixel_size / 2) + pixel_size

            elif (string[a] == 'M' or string[a] == 'T' or string[a] == 'V' or
                    string[a] == 'W' or string[a] == 'Y'):
                x = x + (pixel_size * 5) + pixel_size
            else:
                x = x + (pixel_size * 4) + pixel_size

            break
