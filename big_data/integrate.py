def function(x, y):
    return x * x + y * y


def main():
    v = 0
    end_x = 30
    end_y = 30
    start_x = 20
    start_y = 20
    current_x = start_x
    delta = .01
    while 1:
        current_y = start_y
        if current_x >= end_x:
            break
        while 1:
            if current_y >= end_y:
                break
            v += function(current_x, current_y) * delta * delta
            current_y += delta
        current_x += delta
    print(3 * v/380000)

if __name__ == '__main__':
    main()
