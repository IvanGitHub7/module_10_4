import threading
from time import sleep
import sys
import random
import queue

class Table: #Саздаем класс "Стол"
    def __init__(self, number): #Инициализируем создание объекта класса
        self.number = number #Присваиваем объекту атрибут "номер"
        self.guest = None #Присваиваем объекту атрибут "гость" (по умолчанию стол пустой)
    
class Guest(threading.Thread): #Создаем класс "Гость"
    def __init__(self, name): #Инициализируем создание объекта класса
        super().__init__() #Инициализируем родительский класс Thread
        self.name = name #Присваиваем объекту атрибут "имя"
        
    def run(self): #Создаём метод для имитации времени проведенного в кафе
        sleep(random.randint(3, 10)) #Имитируем время проведенное в кафе
       
class Cafe: #Создаем класс "Кафе"
    def __init__(self, *tables): #Инициализируем создание объекта класса
        self.queue = queue.Queue() #Присваиваем объекту класса атрибут "очередь"
        self.tables = tables #Присваиваем объекту класса атрибут "столы"
        
    def guest_arrival(self, *guests): #Создаем метод для имитации прибытия гостей
        for guest in guests: #Берем гостя из списка гостей
            for table in self.tables: #Пробегаемся по столам в атрибуте "столы"
                if table.guest is None: #если стол свободен
                    table.guest = guest #сажаем гостя за стол
                    guest.start() #запускаем поток, имитирующий нахождение гостя в кафе
                    print(f'{table.guest.name} сел за стол номер {table.number}') #Выводим сообщение о том, что гость сел за стол
                    break #завершаем итерацию цикла рассадки по данному гостю
            else: #Если свободных столов нет
                self.queue.put(guest) #Помещаем гостя в очередь
                print(f'{guest.name} в очереди') # Выводим сообщение о добавлении гостя в очередь
                # Переходим к рассадке следующего гостя (если список гостей не закончился)
            
    def discuss_guests(self): #Создаем метод имитирующий процесс обслуживания гостей
        while not self.queue.empty() or any(table.guest is not None for table in self.tables): #Пока очередь не пуста или пока хотя бы за одним из столов есть гость:
            for table in self.tables: #Пробегаемся по списку столов
                if table.guest and not table.guest.is_alive(): #Если за столом есть гость и гость поел
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)') #Выводим сообщение о том, что гость поел и ушёл
                    print(f'Стол номер {table.number} свободен') #Выводим сообщение о том, что стол освободился
                    table.guest = None #Убираем гостя из-за стола
                    
                    if not self.queue.empty(): #Если очередь не пуста:
                        guest = self.queue.get() #Берем гостя из очереди
                        table.guest = guest #Сажаем за освободившийся стол
                        guest.start() #Запускаем поток имитирующий нахождение гостя в кафе
                        print(f'{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}') #Выводим сообщение о том что гость вышел из очереди и сел за стол
                        
# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests() 
            