# Подключение модулей
import pygame
# Змейка будет появляться в случайном месте, понадобится генератор целых чисел
from random import randrange

# Константы
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = (300,300)
# змейка и яблоко будут квадратными, OBJECT_SIZE это их размер:
OBJECT_SIZE = 10

# Переменные и инициализация
# чтобы воспользоваться библиотекой pygame, её необходимо инициализировать
pygame.init()

# Create display
# https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
screen = pygame.display.set_mode(WINDOW_SIZE)

# Функция randrange создает список с числами в интервале от 0 до WINDOW_WIDTH с шагом в OBJECT_SIZE, а потом из него выбирает случайное значение
x = randrange(0, WINDOW_WIDTH, OBJECT_SIZE)
y = randrange(0, WINDOW_HEIGHT, OBJECT_SIZE)

# координаты головы змейки будем хранить с помощью списка
body_snake = [(x, y)]
# счетчик длины змейки
length_snake = 1

dx, dy = 0, 0

#переменная для скорости (так же она будет отвечать за количество выполнений цикла в одну секунду)
fps = 7

apple = randrange(0, WINDOW_WIDTH, OBJECT_SIZE), randrange(0, WINDOW_HEIGHT, OBJECT_SIZE)

# Словарь движения
# движемся по оси у, либо по оси х. Направление задается знаком перед единицей, если она положительна, то мы двигаемся по направлению оси, если отрицательна - то против
traffic_dict = {"W": (0, -1), "S": (0,1), "A": (-1,0), "D": (1,0)}

# при каждом выполнении цикла экран будет обновляться и, при след. выполнении, мы будем видеть все, что нарисовали
# Так как у нас программа отрисовки находится внутри цикла while, то при каждом новом выполнении цикла у нас будет рисоваться новая картинка, которая будет накладываться на предыдущую
while True:
# Показ экрана и закраска его в черный цвет
    screen.fill(pygame.Color('black'))
    
# Отрисовка змейки
# Сейчас в змейке всего одна пара координат,но тк змейка будет есть яблоки, количество координат будет увеличиваться. Поэтому нам нужно воспользоваться циклом.
    for i, j in body_snake:
        # из координат i, j рисуется прямоугольник со сторонами SIZE, SIZE (квадрат) и заливается зеленым цветом
        # https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect
        pygame.draw.rect(screen, pygame.Color('green'), (i, j, OBJECT_SIZE, OBJECT_SIZE))
        
# Отрисовка яблока
# чтобы получить все значения списка, можно пройти его поэлементно и вывести каждый, а можно использовать *
# используя * нужно быть уверенным, что количество значений, которые мы хотим получить, и количество элементов в списке должны быть одинаковыми. Так как у нас там всегда находится только два значения, мы можем не писать поэлементное извлечение, а воспользоваться *
    pygame.draw.rect(screen, pygame.Color('red'), (*apple, OBJECT_SIZE, OBJECT_SIZE))
    
# Изменение координат змейки
# будем находить новые координаты путем прибавления направления, умноженного на размер клетки    
    x += dx * OBJECT_SIZE
    y += dy * OBJECT_SIZE  
    
    #добавления элемента в список. добавляем новые координаты
    body_snake.append((x, y))  
    
# Так как мы добавляем новые координаты, а наша змейка не увеличилась в размере, то нам нужно изменить количество координат
# сокращенная операция среза. минус означает, что отсчитываем длину не сначала списка, а с конца. двоеточие в конце значит, что доходим до конца списка
    body_snake = body_snake[-length_snake:] 
    
    # Поедание яблока
    if body_snake[-1] == apple:
        apple = randrange(0, WINDOW_WIDTH, OBJECT_SIZE), randrange(0, WINDOW_HEIGHT, OBJECT_SIZE)
        length_snake += 1
        
        fps += 1 #Мы будем отслеживать координаты головы змейки (в момент добавления координат в список координаты головы поменяются на добавляемые, а они в свою очередь будут последними в списке и для того, чтобы их "вызвать", используем команду snake[-1]), и если они совпадут с яблоком (1), то мы снова сгенерируем яблоко (2), увеличим длину змейки (3) и скорость (4)
        
# Модуль для индетифицирования нажатой клавиши
# https://www.pygame.org/docs/ref/key.html
    key = pygame.key.get_pressed()
    
    # Условия движения
    if key[pygame.K_w] and (dx, dy) != traffic_dict["S"]:
        dx, dy = traffic_dict["W"]
    if key[pygame.K_s] and (dx, dy) != traffic_dict["W"]:
        dx, dy = traffic_dict["S"]
    if key[pygame.K_a] and (dx, dy) != traffic_dict["D"]:
        dx, dy = traffic_dict["A"]
    if key[pygame.K_d] and (dx, dy) != traffic_dict["A"]:
        dx, dy = traffic_dict["D"]
        
    # Вызод за границы экрана
    if x <0 or x > WINDOW_WIDTH or y < 0 or y > WINDOW_HEIGHT:
        break
        
# Поедание змейкой самой себя  
# в нашем списке body_snake хранятся списки координат головы и тела змейки. 
# len() считает кол-во координат внутри списка body_snake. 
# set() сделает тоже самое, но исключит при этом одинаковые координаты (это будут голова и часть тела змейки в случае ее поедания самой себя). 
    if len(body_snake) != len(set(body_snake)):        
        break 
        
    # Условие закрытия программы
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            
    # Обновление экрана    
    # всё, что мы будем показывать, появится только после выполнения этого метода
    pygame.display.flip()
    
    # Управление частотой кадров
    clock = pygame.time.Clock()
    
    # Количество раз выполнения цикла в секунду
    clock.tick(2*fps)


