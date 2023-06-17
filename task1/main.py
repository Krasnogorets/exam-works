# Задание
# Реализовать консольное приложение заметки, с сохранением, чтением,
# добавлением, редактированием и удалением заметок. Заметка должна
# содержать идентификатор, заголовок, тело заметки и дату/время создания или
# последнего изменения заметки. Сохранение заметок необходимо сделать в
# формате json или csv формат (разделение полей рекомендуется делать через
# точку с запятой). Реализацию пользовательского интерфейса студент может
# делать как ему удобнее, можно делать как параметры запуска программы
# (команда, данные), можно делать как запрос команды с консоли и
# последующим вводом данных, как-то ещё, на усмотрение студента.

import json
import operator
import pprint
from time import gmtime, strftime
from datetime import datetime as dt

timecheck = strftime("%Y-%m-%d %H:%M:%S", gmtime())
id_notes = 0
id_list = []
data = {}
data['notes'] = []


def get_note_by_id(id):
    try:
        with open('data1.json') as json_file:
            data = json.load(json_file)
            flag = False
            for p in data['notes']:
                if p['id'] == id:
                    print('Id: ' + str(p['id']))
                    print('Notes name: ' + p['name'])
                    print('text: ' + p['text'])
                    print('Edited at date/time: ' + str(p['date_time']))
                    print()
                    flag = True
            if not flag:
                print('не ищите того , чего нет в заметках')
    except Exception as e:
        print(e)


def get_data():
    try:
        with open('data1.json') as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        print(e)


def get_id():
    try:
        with open('data1.json') as json_file:
            data = json.load(json_file)
            for p in data['notes']:
                id_list.append(p['id'])
        id_list.sort()
        id_notes = id_list[len(id_list) - 1] + 1
        id_list.clear()
        return id_notes
    except Exception as e:
        print("Note: file not found, skipped")
        id_notes = 1
        return id_notes


def write_json(new_data, filename='data1.json'):
    try:
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data['notes'].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    except Exception as e:
        with open(filename, 'a') as file:
            print("Note: file not found, created new one")
            file_data = {}
            file_data['notes'] = []
            file_data['notes'].append(new_data)
            json.dump(file_data, file, indent=4)


def input_data():
    notice_name = input("введите название заметки: ").lower()
    id_notes = get_id()
    if notice_name == "":
        notice_name = "Notice #" + " " + str(id_notes)
    notice_txt = input("введите текст заметки: ").lower()
    new_note = {
        'id': id_notes,
        'name': notice_name,
        'text': notice_txt,
        'date_time': timecheck
    }
    write_json(new_note)


def print_data(data):
    for p in data['notes']:
        print('Id: ' + str(p['id']))
        print('Notes name: ' + p['name'])
        print('text: ' + p['text'])
        print('Edited at date/time: ' + str(p['date_time']))
        print()


def read_data():
    get_choice = (int(input(
        """\n         Вы можете отобразить заметки с сортировкой по:
         1 - по id
         2 - по дате  """)))
    if get_choice == 1:
        try:
            with open('data1.json') as json_file:
                data = json.load(json_file)
                print_data(data)
        except Exception as e:
            print(e)
    else:
        try:
            with open('data1.json') as json_file:
                data = json.load(json_file)
                ordered = data['notes']
                ordered.sort(key=operator.itemgetter('date_time'))
                pprint.pprint(ordered)

        except Exception as e:
            print(e)


def find_data():
    get_choice = (int(input(
        """\n         Вы можете найти заметку по:
         1 - по id
         2 - по названию
         3 - по дате 
         4 - вернуться в главное меню  """)))
    with open('data1.json') as json_file:
        data = json.load(json_file)
    flag = False
    if get_choice == 1:
        find_feature = int(input('Введите id:  '))
        get_note_by_id(find_feature)
        flag = True

    elif get_choice == 2:
        find_feature = input('Введите слово, содержащееся в заметке:  ')
        for p in data['notes']:
            temp_list = p['name'].split(" ")
            id = p['id']
            if find_feature in temp_list:
                get_note_by_id(id)
        flag = True
    elif get_choice == 3:
        find_feature = input('Введите дату заметки формате YYYY/MM/DD:  ')
        try:
            date_1 = dt.strptime(find_feature, '%Y/%m/%d').date()
        except Exception as e:
            print("введен неверный формат даты")
        for p in data['notes']:
            temp_list = p['date_time'].split(" ")
            id = p['id']
            if str(date_1) == str(temp_list[0]):
                get_note_by_id(id)
        flag = True
    elif get_choice == 4:
        return
    if not flag:
        print("такой записи не найдено")


def replace_data():
    with open('data1.json') as json_file:
        data = json.load(json_file)
    find_data()
    get_id = int(input("введите id заметки для редактирования:  "))
    get_note_by_id(get_id)
    get_choice = (int(input(
        """\n         Вы можете изменить в  заметке:
         1 - название
         2 - текст  """)))
    if get_choice == 1:
        find_feature = input('Введите новое название заметки: ')
        for p in data['notes']:
            id = p['id']
            if get_id == id:
                p['name'] = find_feature
                p['date_time'] = timecheck
                write_lines(data['notes'])

    if get_choice == 2:
        find_feature = input('Введите новый текст заметки: ')
        for p in data['notes']:
            id = p['id']
            if get_id == id:
                p['text'] = find_feature
                p['date_time'] = timecheck
                write_lines(data['notes'])


def write_lines(data):
    try:
        with open('data1.json', 'w') as file:
            file_data = {}
            file_data['notes'] = data
            json.dump(file_data, file, indent=4)
    except Exception as e:
        print(e)


def remove_data():
    with open('data1.json') as json_file:
        data = json.load(json_file)
    get_id = int(input("введите id заметки для удаления : "))
    get_note_by_id(get_id)
    get_choice = int(input('Желаете полностью удалить эту строку? (1-да, 2-нет) '))
    if get_choice == 1:
        for i in data["notes"]:
            if i["id"] == get_id:
                data["notes"].remove(i)
        write_lines(data["notes"])
        return
    if get_choice == 2:
        return

while True:
    get_choice = (int(input(
        """\n введите 1 - для добавления заметки,
         2 - для вывода всех заметок, 
         3 - для поиска заметки, 
         4 - для изменения заметки
         5 - для удаления заметки         
         6 - для завершения работы  \n""")))
    match get_choice:
        case 1:
            input_data()
        case 2:
            read_data()
        case 3:
            find_data()
        case 4:
            replace_data()
        case 5:
            remove_data()
        case _:
            break
