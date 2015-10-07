title: Декораторы в Python
date: 2015-08-19 00:47:00
Status: published
tags: python, programming, habr

Никакой волшебно новой информации здесь не будет, скорее это самому себе объяснение, что за зверь такой декораторы в python.

Т.к. в pyhton ф-ии являются объектами, то к ним можно применить шаблон проектирования [декоратор](https://ru.wikipedia.org/wiki/%D0%94%D0%B5%D0%BA%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80_%28%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F%29). Сам шаблон я на момент написания этих строк не разбирал, посему тут может быть не совсем корректная информация о том насколько правильно реализуется данный шаблон в случае ф-ий языка python.

Итак. Декоратор - это возможность расширения ф-нала имеющейся ф-ии(объекта). Получается что-то типа наследования, но без создания новой сущности. Для реализации декораторов необходимо написать сам декоратор, это ф-ия которая принимает в качестве параметра другую ф-ю(именно её адрес, а не её вызов) и оборачивает её како-либо логикой. Например:

    :::python
    def decorator(some_func):
        def wrapper():
            # делаем что-то перед вызовом оборачиваемой ф-ии
            print("before")
            # вызываем оборачиваемую ф-ю
            some_func()
            # делаем что-то после вызова обернутой ф-ии
            print("after")
        return wrapper
    
    def just_func():
        print("Я не изменюсь, но меня можно обернуть")
    
теперь обернем just_func

    :::python    
    decorator(just_func)()

    # before
    # Я не изменюсь, но меня можно обернуть
    # after

Можно подобному вызову ф-ии присовить имя:

    :::python
    just_func_wrapped = decorator(just_func)

И при вызове `just_func_wrapped` получим тоже самое:

    :::python
    just_func_wrapped()

    # before
    # Я не изменюсь, но меня можно обернуть
    # after

Мы почти добрались до сути. Собственно как это можно было записать при помощи синтаксиса декораторов:

    :::python
    @decorator
    def just_func():
        print("Я обернутая ф-я")

И вызвав `just_func` получим:
    
    :::python
    just_func()

    # before
    # Я обернутая ф-я
    # after

Т.е. синтаксис декоторов это синтаксический сахар заменяющий такую конструкцию:

    :::python
    def just_func():
        pass
    just_func = decorator(just_func)

    # равносильно такой записи
    @decorator
    def just_func():
        pass

## Передача аргументов внутрь обертки

Также можно, а точнее это и нужно, передавать агрументы внутрь ф-ии декоратора, оборачиваемой ф-ии.

    :::python
    def decorator(just_func):
        def wrapper(arg1, arg2):
            print("before")
            print("Я получил внутрь аргументы " + arg1 + " " + arg2)
            # вызываем ф-ию с аргументами
            just_func(arg1, arg2)
            print("after")
        return wrapper

    @decorator
    def just_func(str1, str2):
        print(str1 + " " + str2)

    just_func("Привет", "Мир")

    # before
    # Я получил внутрь аргументы Привет Мир
    # Привет Мир
    # after 

## Декор методов в классах

Всё то же самое за исключением, что метод отличается от ф-ии тем, что первым аргументом метода, всегда является ссылка на свой класс.

    :::python
    def decorator(class_method):
        def wrapper(self, some):
            print("Это обёртка для метода класса")
            print(1000 + some)
            return class_method(self, some)
        return wrapper

    class MyClass(object):
        def __init__(self):
            self.var = 2

        @decorator
        def my_method(self, some):
            print(self.var + some)

    m = MyClass()
    m.my_method(1)

    # 1003
    # Хотя по-идее мы могли бы ожидать 1 + 2, но благодаря обертке мы смогли
    # изменить функционал

## Передача \*args и \*\*kwargs декорируемой ф-ии

Ничего волшебного:

    :::python
    def decorator(just_func):
        def wrapper(*args, **kwargs):
            return just_func(*args, **kwargs)
        return wrapper

    @decorator
    def just_func(*args, **kwargs):
        print(args)
        print(kwargs)

    just_func()

    # ()
    # {}

## Передача аргументов декоратору

Логично возникает вопрос: "А как же передать аргументы в декоратор, если декоратор по определению должен принимать на вход только имя декорируемой ф-ии?".

Решение есть, но не лёгкое. Задекорируем декоратор (crazy).

    :::python
    # ф-ия создающая декоратор
    def decorator_for_decorator():
        # ф-я декоратор (т.е. изменяющая ф-ал оборачиваемой ф-ии)
        def decorator(func):
            # ф-ия обертка
            def wrapper():
                # some logic
                func()
            return wrapper
        return decorator

    new_decorator = decorator_for_decorator()
    # создаем декоратор и присваиваем его переменной

    def just_func():
        print("Я просто ф-я")

    # задекорируем ф-ю
    just_func = new_decorator(just_func)

    # и теперь можем вызвать задекорированную ф-ю
    just_func()

Или можно записать так:
    
    :::python
    def just_func():
        print("я декорируемая ф-я")

    just_func = decorator()(just_func)

    # и вызов задекорированной ф-ии
    just_func()

А теперь то же самое, но только при помощи `@`:

    :::python
    @decorator_for_decorator()
    def just_func():
        print("я декорируемая ф-я")

    just_func()

Т.к. декоратор теперь есть вызов ф-ии, то можем передать ему некие аргументы:

    :::python
    def deco_for_deco(deco_arg1, deco_arg2):
        print(deco_arg1 + deco_arg2)
        def decorator(just_func):
            def wrapper(func_arg1, func_arg2):
                # данная обертка теперь имеет доступ как к аргументам
                # декоратора, так и к аргументам декорируемой ф-ии
                return just_func(func_arg1, func_arg2)
            return wrapper
        return decorator

    @deco_for_deco("Привет", "Мир")
    def just_func(arg1, arg2):
        print("Меня задекорировали, и знаю только" +\
                "о своих аргументах %s и %s" % (arg1, arg2))

    # выведет: "ПриветМир"

    just_func("один", "два")

    # выведет: Меня задекорировали, и знаю только о своих аргументах один и два

Зная всё что здесь написано можно сделать декоратор для декораторов которому можно передавать любые аргументы:

    :::python
    def deco_for_deco(decorataion_decorator):
        def decorator_maker(*args, **kwargs):
            def decorator_wrapper(func):
                return decoration_decorator(func, *args, **kwargs)
            return decorator_wrapper
        return decorator_maker

Теперь посмотрим как воспользоваться этой адовой смесью:

    :::python
    @deco_for_deco
    def decorated_decorator(func, *args, **kwargs):
        def wrapper(func_arg1, func_arg2):
            print("Я знаю о %s и %s" % (args, kwargs))
            return func(func_arg1, func_arg2)
        return wrapper

Теперь декорируем нужные нам ф-ии передавая любые аргументы декоратору:

    :::python
    @decorated_decorator(42, 404, 1024)
    def just_func(arg1, arg2):
        print("Привет" + arg1 + arg2)

    just_func(" Жвачка и ", "Мир")

    # выведет:
    # Я знаю о (42, 404, 1024) и {}
    # Привет Жвачка и Мир

## Подводя итоги

В общем этот длиннопост переработанный изхабра, создавался когда я врубался в подсмотренный код в django, где в 4 строках скрыто целая тьма смысла и материала для изучения. Там создавался класс mixin в котором декорировался некий метод который обезапасивал доступ к сайту. Ацкая смесь без развернутых пояснений на англ. языке. Ну вот собственно с декораторами вроде разобрался.

Где еще применяется декорирование?

Декораторы могут быть использованы для расширения возможностей функций из сторонних библиотек (код которых мы не можем изменять), или для упрощения отладки (мы не хотим изменять код, который ещё не устоялся).
Так же полезно использовать декораторы для расширения различных функций одним и тем же кодом, без повторного его переписывания каждый раз, например:

    :::python
    def benchmark(func):
        """
        Декоратор, выводящий время, которое заняло
        выполнение декорируемой функции.
        """
        import time
        def wrapper(*args, **kwargs):
            t = time.clock()
            res = func(*args, **kwargs)
            print func.__name__, time.clock() - t
            return res
        return wrapper

    def logging(func):
        """
        Декоратор, логирующий работу кода.
        (хорошо, он просто выводит вызовы, но тут могло быть и логирование!)
        """
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            print func.__name__, args, kwargs
            return res
        return wrapper
     
     
    def counter(func):
        """
        Декоратор, считающий и выводящий количество вызовов
        декорируемой функции.
        """
        def wrapper(*args, **kwargs):
            wrapper.count += 1
            res = func(*args, **kwargs)
            print "{0} была вызвана: {1}x".format(func.__name__, wrapper.count)
            return res
        wrapper.count = 0
        return wrapper
     
     
    @benchmark
    @logging
    @counter
    def reverse_string(string):
        return str(reversed(string))
     
    print reverse_string("А роза упала на лапу Азора")
    print reverse_string("A man, a plan, a canoe, pasta, heros, rajahs, a coloratura, maps, snipe, percale, macaroni, a gag, a banana bag, a tan, a tag, a banana bag again (or a camel), a crepe, pins, Spam, a rut, a Rolo, cash, a jar, sore hats, a peon, a canal: Panama!")
     
    # выведет:
    # reverse_string ('А роза упала на лапу Азора',) {}
    # wrapper 0.0
    # reverse_string была вызвана: 1x
    # арозА упал ан алапу азор А
    # reverse_string ('A man, a plan, a canoe, pasta, heros, rajahs, a coloratura, maps, snipe, percale, macaroni, a gag, a banana bag, a tan, a tag, a banana bag again (or a camel), a crepe, pins, Spam, a rut, a Rolo, cash, a jar, sore hats, a peon, a canal: Panama!',) {}
    # wrapper 0.0
    # reverse_string была вызвана: 2x
    # !amanaP :lanac a ,noep a ,stah eros ,raj a ,hsac ,oloR a ,tur a ,mapS ,snip ,eperc a ,)lemac a ro( niaga gab ananab a ,gat a ,nat a ,gab ananab a ,gag a ,inoracam ,elacrep ,epins ,spam ,arutaroloc a ,shajar ,soreh ,atsap ,eonac a ,nalp a ,nam A

***

Скопипащенно *©[отсюда](http://habrahabr.ru/post/141411/)*