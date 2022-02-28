import os
import tkinter as tk
from PIL import ImageTk, Image


class Parametrs:
    '''
        Параметры игры
    '''
    click_step = 0
    game_ower_flag = False
    winner = None

    def __init__(self):
        self.WIDTH_WINDOW = 450
        self.H_label = 50
        self.HEIGHT_WINDOW = 450
        self.W_N, self.H_M = 3, 3
        self.bd = 5
        self.H_BOX = self.HEIGHT_WINDOW // self.H_M - self.bd * (self.H_M - 2) * 2
        self.W_BOX = self.WIDTH_WINDOW // self.W_N - self.bd * (self.W_N - 2) * 2
        self.first_person = "X"
        self.second_person = "O"


def test_picture(path, W_BOX, H_BOX):
    '''

    :param path: Путь к картинке
    :param W_BOX: Ширина картинки
    :param H_BOX: Высота картинки
    :return: Обьект image
    '''
    if os.path.exists(path):
        image = Image.open(path)
        image = image.resize((W_BOX, H_BOX), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        return image
    raise Exception("Картинок нет")


class Cell(Parametrs):
    img_path_cross = os.path.normpath("img/cross.jpg")
    img_path_zero = os.path.normpath("img/zero.jpg")
    img_path_before = os.path.normpath("img/before.png")

    def __init__(self, x, y, btn):
        super(Cell, self).__init__()
        self.__image_cross = test_picture(Cell.img_path_cross, self.W_BOX, self.H_BOX)
        self.__image_zero = test_picture(Cell.img_path_zero, self.W_BOX, self.H_BOX)
        self.__image_before = test_picture(Cell.img_path_before, self.W_BOX, self.H_BOX)
        self.__image_before = self.__image_before
        self.__image_now = self.__image_before
        self.active = False
        self.person_active = None
        self.position_x = self.set_x(x)
        self.position_y = self.set_y(y)
        self.btn = btn
        self.btn["image"] = self.image()


    def click(self, event):
        '''
            Обрабатывает событие на клик
        '''
        if not Parametrs.game_ower_flag:
            self.new_click()
            if not self.active:
                self.__image_now = self.__image_cross if self.person_active == self.first_person else self.__image_zero
                self.active = True
                self.btn["image"] = self.__image_now
                # print(f"Нажал {self.person_active} на клетку {self.position_x, self.position_y}")
                return True
            print(f"Уже нажата {self.person_active}")
        print("\t\t\t\t\t\t\tИгра закончена")
        return False

    def new_click(self):
        '''
            Чередование 0/X
        :return:
        '''
        if not self.active:
            if Parametrs.click_step % 2 == 0:
                self.person_active = self.first_person
            else:
                self.person_active = self.second_person
            Parametrs.click_step += 1

    def set_x(self, x):
        '''
            Проверка входного параметра x
        :param x:
        :return:
        '''
        if self.W_N > x >= 0:
            return x
        return None

    def set_y(self, y):
        '''
            Проверка входного параметра y
        :param x:
        :return:
        '''
        if self.H_M > y >= 0:
            return y
        return None

    def image(self):
        '''
            Возвращает фоновую картинку, которая в данный момент
        :return:
        '''
        return self.__image_now

    def __str__(self):
        return f"Кнопка активна x,y = {self.position_x}{self.position_y}" if self.active else f"Кнопка не активна x,y = {self.position_x}{self.position_y}"


class Game(Parametrs):

    def __init__(self):
        super(Game, self).__init__()
        self.game_table = None
        self.root = tk.Tk()

    def create_game(self):
        '''
            Полотно для дальнейшей работы
        :return:
        '''
        self.root.title("X/0")
        self.root.geometry(f"{self.WIDTH_WINDOW}x{self.HEIGHT_WINDOW}")
        self.root.resizable(width=False, height=False)

    def create_table(self):
        '''
            Создается обьект self.game_table, в котором хранятся кнопки
        :return:
        '''
        self.root.bind("<Button-1>", self.game_ower)
        self.game_table = [[x for x in range(self.W_N)] for y in range(self.H_M)]
        for y in range(self.H_M):
            for x in range(self.W_N):
                self.game_table[y][x] = Cell(x=x, y=y,
                                             btn=tk.Button(master=self.root,
                                                           text="Нажми на меня!",
                                                           width=self.W_BOX,
                                                           height=self.H_BOX,
                                                           border=self.bd,
                                                           ))
                self.game_table[y][x].btn.bind("<Button-1>", self.game_table[y][x].click)
                self.game_table[y][x].btn.grid(row=x, column=y, ipadx=0, ipady=0, padx=0, pady=0)
        # lab1 = tk.Label()
        # lab1.pack()

    def start(self):
        '''
            Запуск игры
        :return:
        '''
        print("=" * 70)
        print("\t\t\t\t\t\t\tИгра началась!")
        print("=" * 70)
        self.create_game()
        self.create_table()
        self.root.mainloop()

    def game_ower(self, event):
        '''
            Проверка на завершение игры
        :param event:
        :return:
        '''
        table = [[None for x in range(self.W_N)] for y in range(self.H_M)]
        for x in range(self.W_N):
            for y in range(self.H_M):
                if self.game_table[y][x].active:
                    table[y][x] = 1 if self.game_table[y][x].person_active == self.first_person else 0

        for i in range(0, self.W_N):
            for j in range(0, self.H_M):
                if table[j][i] is not None:
                    if i >= 1 and i < self.W_N - 1:
                        if table[j][i - 1] == table[j][i] == table[j][i + 1]:
                            self.func_winner(i, j)
                    if j >= 1 and j < self.H_M - 1:
                        if table[j - 1][i] == table[j][i] == table[j + 1][i]:
                            self.func_winner(i, j)
                    if (i >= 1 and i < self.W_N - 1) and (j >= 1 and j < self.H_M - 1):
                        if table[j - 1][i - 1] == table[j][i] == table[j + 1][i + 1] or table[j + 1][i - 1] == table[j][
                            i] == table[j - 1][i + 1]:
                            self.func_winner(i, j)

        if not self.game_ower_flag and all(all(x.active for x in line) for line in self.game_table):
            print("Ничья!")

    def func_winner(self, i, j):
        '''
            Функция для печати победителя
        '''
        if not self.game_ower_flag:
            print("!" * 70)
            print(f"\t\t\t\t\t\t\tПобедил {self.game_table[j][i].person_active}")
            print("!" * 70)
            Parametrs.winner = self.game_table[j][i].person_active
            Parametrs.game_ower_flag = True


Game().start()
