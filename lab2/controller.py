#Tkinter - це стандартна бібліотека для створення графічних інтерфейсів у Python, імпортуємо її
from tkinter import *
#встановлюємо розміри пікселів
PIXEL_SIZE = 5
#встановлюємо розмір вікна
HEIGHT = 600
WIDTH = 1090
#створюємо клас, який буде містити необхідні алгоритми та дані для виводу прізвища
class RasterizationAlgorithms:
    #масив координат для кожної літери(складається з певної кількості відрізків)
    surname = {
        "H": [[(5, 10), (5, 40)], [(20, 10), (20, 40)], [(5, 25), (20, 25)]],
        "a": [[(30, 25), (33, 22)], [(34, 22), (40, 22)], [(41, 22), (44, 25)], [(44, 25), (44, 40)], [(44, 37), (41, 40)], [(40, 40), (34, 40)], [(33, 40), (30, 37)], [(30, 26), (30, 36)]],
        "r": [[(50, 25), (50, 40)], [(50, 26), (53, 23)], [(54, 23), (60, 23)], [(61, 23), (64, 26)]],
        "m": [[(70, 40), (70, 25)], [(70, 26), (73, 23)], [(74, 23), (77, 26)], [(77, 23), (80, 26)], [(80, 25), (80, 40)]],
        "a2": [[(90, 25), (93, 22)], [(94, 22), (100, 22)], [(101, 22), (104, 25)], [(104, 25), (104, 40)], [(104, 37), (101, 40)], [(100, 40), (94, 40)], [(93, 40), (90, 37)], [(90, 26), (90, 36)]],
        "t": [[(110, 10), (110, 40)], [(103, 22), (117, 22)]],
        "i": [[(125, 22), (125, 40)], [(124, 10), (126, 10)]],
        "u": [[(135, 22), (135, 40)], [(135, 37), (138, 40)], [(139, 40), (145, 40)], [(146, 40), (149, 37)], [(149, 40), (149, 22)]],
        "k": [[(155, 10), (155, 40)], [(155, 30), (165, 22)], [(155, 30), (165, 40)]]
    }
    #алгоримт ДДА
    def DDA(self, x1, y1, x2, y2):
        #обчислення різниці по координатах початкової та кінцевої точки
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        #обрахунок необхідної кількості кроків
        steps = dx if dx >= dy else dy
        #задання зміни кроку
        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps
        #встановлення початкових координат
        x, y = x1, y1
        #створення списку пікселів
        points = [[x, y], [x2, y2]]
        #цикл рисовки відрізка
        for i in range(steps - 1):
            x += dx
            y += dy
            points.append([round(x), round(y)])
        #відображення відрізка
        self.draw(points)
    #алгоритм Брезенхема для відрізка
    def Bresenham(self, x1, y1, x2, y2):
        #обчислення різниці по координатах початкової та кінцевої точки
        dx = x2 - x1
        dy = y2 - y1
        #визначення чи лінія має більшу зміну по у ніж по х
        is_steep = abs(dy) > abs(dx)
        #якщо так, то змінюємо координати х та у
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        #якщо початкові точки більші за кінцеві, то координати міняються місцями
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        #повторний обрахунок різниць координат
        dx = x2 - x1
        dy = y2 - y1
        #визначення чи змінювати координату у
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1
        #цикл рисовки відрізка
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx
        #відображення відрізка
        self.draw(points)
    #алгоритм Брезенхема для кола
    def circle_Bresenham(self, xc, yc, radius):
        #початкові налаштування
        x = 0
        y = radius
        delta = 1 - 2 * radius
        error = 0
        #список координат точок кола
        points = []
        #цикл рисовки кола
        while (y >= 0):
            #визначення 4ох симетричних точок
            points.append((xc + x, yc + y))
            points.append((xc + x, yc - y))
            points.append((xc - x, yc + y))
            points.append((xc - x, yc - y))
            error = 2 * (delta + y) - 1
            if (delta < 0) and (error <= 0):
                x += 1
                delta += 2 * x + 1
                continue
            error = 2 * (delta - x) - 1
            if delta > 0 and error > 0:
                y -= 1
                delta += 1 - 2 * y
                continue
            x += 1
            delta += 2 * (x - y)
            y -= 1
        #відображення відрізка
        self.draw(points)
    #алгоритм Ву
    def Wu(self, x1, y1, x2, y2):
        #список координат точок кола
        points = []
        #визначення чи лінія має більшу зміну по у ніж по х
        steep = abs(y2 - y1) > abs(x2 - x1)
        #якщо так, то змінюємо координати х та у
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        #якщо початкові точки більші за кінцеві, то координати міняються місцями
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        #обрахунок різниць координат
        dx = x2 - x1
        dy = y2 - y1
        gradient = dy / dx
        #визначення першої кінцевої точки
        xend = round(x1)
        yend = y1 + gradient * (xend - x1)
        xpxl1 = xend
        ypxl1 = int(yend)
        if steep:
            points.append([ypxl1, xpxl1])
        else:
            points.append([xpxl1, ypxl1])
        intery = yend + gradient
        #визначення другої кінцевої точки
        xend = round(x2)
        yend = y2 + gradient * (xend - x2)
        xpxl2 = xend
        ypxl2 = int(yend)
        if steep:
            points.append([ypxl2, xpxl2])
        else:
            points.append([xpxl2, ypxl2])
        #рисовка відрізку
        if steep:
            for i in range(xpxl1 + 1, xpxl2):
                points.append([int(intery), i])
                intery += gradient
        else:
            for i in range(xpxl1 + 1, xpxl2):
                points.append([i, int(intery)])
                intery += gradient
        #відображення відрізка
        self.draw(points)
    #метод рисовки пікселів
    def draw(self, coords):
        for point in coords:
            self.canvas.create_rectangle(PIXEL_SIZE * point[0], PIXEL_SIZE * point[1],
                                         PIXEL_SIZE * point[0] + PIXEL_SIZE, PIXEL_SIZE * point[1] + PIXEL_SIZE,
                                         fill="black", tag="surname")
    #метод очистки всіх нарисованих пікселів
    def clean(self):
        self.canvas.delete("surname")
    #метод для виклику функцій при натисканні на кнопки
    def callback(self, func_name):
        if func_name == "circle_Bresenham":
            return lambda func_name=func_name: getattr(self, func_name)(100, 75, 20)
        else:
            #рендеринг кожної літери з прізвища, використовуючи обраний алгоритм
            def func():
                for letter, lines in self.surname.items():
                    for line in lines:
                        getattr(self, func_name)(line[0][0], line[0][1], line[1][0], line[1][1])
            return func
    #ініціалізація вікна та розміщення в ньому кнопок
    def __init__(self):
        #створення головного вікна та його йменування
        window = Tk()
        window.title("Computer Graphics - Lab Work 1")
        #створення області для малювання та її розміщення в головному вікні
        self.canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="bisque")
        self.canvas.pack()
        #створення контейнера для роміщення та групування елементів всередині головного вікна
        frame = Frame(window)
        frame.pack()
        #розміщення кнопок
        dda_btn = Button(frame, text="DDA - surname", command=self.callback("DDA"), fg="black", bg="salmon1", font=("Courier New", 12))
        dda_btn.grid(row=1, column=1)
        bres_btn = Button(frame, text="Bresenham - surname", command=self.callback("Bresenham"), fg="black", bg="salmon1", font=("Courier New", 12))
        bres_btn.grid(row=1, column=2)
        circle_bres_btn = Button(frame, text="Bresenham - circle", command=self.callback("circle_Bresenham"), fg="black", bg="salmon1", font=("Courier New", 12))
        circle_bres_btn.grid(row=1, column=3)
        wu_btn = Button(frame, text="Wu - surname", command=self.callback("Wu"), fg="black", bg="salmon1", font=("Courier New", 12))
        wu_btn.grid(row=1, column=4)
        clear_btn = Button(frame, text="Clear screen", command=self.clean, fg="black", bg="salmon1", font=("Courier New", 12))
        clear_btn.grid(row=1, column=5)
        #цикл обробки подій, який чекає на події
        window.mainloop()
#перевірка чи даний файл буде запускатись безпосередньо
if __name__ == "__main__":
    RasterizationAlgorithms()

