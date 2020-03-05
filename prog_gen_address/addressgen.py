#!/usr/bin/python
 # -*- coding: utf-8 -*-

import re
import json
import random


def info_only(obj: object):
    """ Декоратор для условного выполнения функции. 

    Если при вызове декорированной функции значение хотя бы одного из аргументов
    было равно переданному декоратору объекту, то функция не вызывается, а вместо
    нее в консоль выводится строка вида «Вызов функции x с параметрами a, b, c». 

    """
    def real_decorator(func):
        def wrapper(*args, **kwargs):
            all_args = list(args)
            all_args.extend(kwargs.values())
            if obj in all_args:
                print(
                    f'Вызов функции {func.__name__} с параметрами: ',
                    end=' ')
                for arg in args:
                    print(arg, end=', ')
                for kwarg in kwargs:
                    print(f'{kwarg}={kwargs[kwarg]}', end=', ')
                    print()
            else:
                return func(*args, **kwargs)

        return wrapper

    return real_decorator


def validate(to_validate: str, raise_error: bool=True) -> bool:
    """ 
    Проверяет строку to_validate на корректность.

    возвращает True, если строка соответствует шаблону accepted_pattern,
    иначе возвращает False

    если именованный аргумент raise_error = True, то если строка переданная
    в качестве первого аргумента не соответствует шаблону accepted_pattern,
    вызывается исключение ValueError

    Именованные аргументы:
    raise_error -- вызвать исключение в случае, если строка некорректна (по умолчанию True)

    """
    error_msg = f'Проверьте корректность данных: {to_validate}'
    acceptable = (
            to_validate and
            isinstance(to_validate, str) and
            re.match(accepted_pattern, to_validate) #Этот метод ищет по заданному шаблону в начале строки
    )
    if acceptable:
        return True
    elif raise_error:
        raise ValueError(error_msg)
    else:
        print(error_msg)
        return False

@info_only('тест')

def address_gen(
        country: str='',
        city: str='',
        streets: list=[],
        file: str='',
        json_string: str='') -> 'generator object':
    """ Возвращает генератор строк, содержащих в себе случайный адрес.

    при вызове функции передаются название города city, страны country и список улиц streets.
    эти данные проверяются на корректность. В случае, если данные некорректны, вызывается исключение ValueError.
    данные также могут быть переданы в виде json-строки json_string или строки file, содержащей путь
    к файлу, в котором лежит json-строка. 

    для работы функции должны быть переданы аргументы
    (county, city, streets) или (file) или (json_string)

    объект генератора может принимать с помощью метода send новые данные для генерации в виде последовательности, 
    содержащей в себе название страны, название города и список улиц, которые необходимо добавить.
    данные проверяются на корректность. В случае, если данные корректны, они дополняют список данных для генерации
    генератора, иначев стандартный поток вывода выводится сообщение об ошибке, исключение не вызывается.

    Именованные аргументы:
    country -- название страны (по умолчанию '')
    city -- название города (по умолчанию '')
    streets -- список улиц (по умолчанию [])
    file -- путь к json-файлу, содержащему в себе строку следующего формата:
        {"country": "%название страны%", "city", "%название города%", "streets": ["%улица 1%",...,"%улица N%"]}
        (по умолчанию '')
    json_string -- json-строка вышеупомянутого формата (по умолчанию '')

    """

    cities = []
    data = None
    if json_string:
        data = json.loads(json_string) #десериализует- считывает файл и возврощает объект Python.
    elif file:
        with open(file) as f:
            data = json.load(f)#десериализует- считывает строку и возврощает объект Python.
    if data:
        country = data['country']
        city = data['city']
        streets = data['streets']

    for toponym in (country, city, *streets):
        validate(toponym)
        
    cities.append(f'{country}, г. {city}, ')
    address_pattern = '{}{}, д. {}{}{}'
    while True:
        city = random.choice(cities) #случайный элемент непустой последовательности.
        street = random.choice(streets)
        house = random.randint(1, 100)
        apartment = f', кв. {random.randint(1, 500)}' if random.random() > 0.5 else '' #random.randint(A, B)-случайное целое число N, A ≤ N ≤ B.
        building = f'/{random.randint(1, 60)}' if random.random() > 0.8 else '' #random.random() - случайное число от 0 до 1.
        msg = yield address_pattern.format(city, street, house, building, apartment)
        if msg:
            if validate(msg[0], raise_error=False) and validate(msg[1], raise_error=False):
                cities.append(f'{msg[0]}, г. {msg[1]}, ')
            for street in msg[2]:
                if validate(street, raise_error=False):
                    streets.append(street)

# Паттерн допустимых названий стран/городов/улиц
accepted_pattern = r"^[A-Za-zА-Яа-я0-9.\-№'\" ]+$"

if __name__ == '__main__':
    
    # file = "/home/address.json"
    # g = address_gen(file=file)
    # print(next(g))
    g = address_gen('Россия', 'Санкт-Петербург', streets=['ул. Обручевых', 'Площадь Мужества'])
    print(next(g))
    print(next(g))
    g.send(("Россия","Мocква", ["Ленина","Сталина"]))  
    print(next(g))
    print(next(g))
    print(next(g))
    
   