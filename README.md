# Запуск:
    1. Запустите файла main.py командной строке
    2. В качестве параметра укажите URL


# Проверенные страницы:
    www.gazeta.ru
        1. https://www.gazeta.ru/science/news/2019/10/24/n_13615910.shtml
        2. https://www.gazeta.ru/business/2019/10/23/12773468.shtml
        3. https://www.gazeta.ru/business/2019/10/23/12772910.shtml
        4. https://www.gazeta.ru/social/news/2019/10/23/n_13612538.shtml
        5. https://www.gazeta.ru/science/news/2019/10/23/n_13612442.shtml
        6. https://www.gazeta.ru/army/2019/10/21/12768350.shtml
        7. https://www.gazeta.ru/politics/news/2019/10/23/n_13610372.shtml
        8. https://www.gazeta.ru/social/2019/10/22/12770906.shtml
        9. https://www.gazeta.ru/politics/2019/10/22_a_12770912.shtml
        10. https://www.gazeta.ru/social/news/2019/10/24/n_13617218.shtml

    www.lenta.ru
        1. https://lenta.ru/news/2019/10/23/dreams/
        2. https://lenta.ru/news/2019/10/23/russia_africa/
        3. https://lenta.ru/news/2019/10/23/bravenewworld/
        4. https://lenta.ru/news/2019/10/23/juul/
        5. https://lenta.ru/news/2018/10/08/nobel/

# Описание алгоритма:
    1. Вытягивание всей страницы по заданному адресу и возвращение ее в виде
        строк
    2. "Вытаскивание по тэгам" необходимой информации и объединение ее в одну
        строку
    3. Обработка строки для записи и запись в файл в указанной директории

# Дальнейшие улучшения/развите программы:
    1. Добавлние тестов и исключений    
    2. Увеличение входных параметров
    3. Улучшениее алгоритма поска "нужной информации"
    4. "Универсализация", под большинство сайтов с помощью дополнительных
        библиотек
    5. Декомпозиция на модули и пакеты
    6. Добавление шаблонов для обработки страниц
    7. Усовршенствование до краулера