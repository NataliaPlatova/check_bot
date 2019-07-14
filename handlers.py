from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging

import db_users as db
from db_users import Users
from create_user import add_new_user

def start(bot, update, user_data):
    update.message.reply_text('Введите преподавателя', reply_markup=ReplyKeyboardRemove())#предлагаю Введите преподавателя убрать и сделать кнопку выберите преподавателя, нажимая будет выпадать список
    return 'teachers_group'


def find_teachers_group(bot, update, user_data):
    teachers_name = update.message.text
    print(teachers_name)
    with open('teacher1.txt', 'r', encoding='ptcp154') as t1_file:
        # TODO: Здесь будет проверка, есть ли такой преподаватель и список его учеников из бд
        user_data['teacher1'] = list(t1_file.read().split('\n'))
    my_keyboard = ReplyKeyboardMarkup([
        ['/list'],
        ['/edit_group'],
        ['/questions']
        #['/back']
    ])
    update.message.reply_text('Выберите действие', reply_markup=my_keyboard)
    return 'actions'


def edit_group(bot, update, user_data):
    students_list = ''
    for student in user_data['teacher1']:
        students_list += f'{student}\n'
    my_keyboard = ReplyKeyboardMarkup([
        ['/add'],
        ['/delete']
        # ['/back']
    ])
    update.message.reply_text(students_list, reply_markup=my_keyboard)
    return 'edit'


def ask_user_name(bot, update):
    update.message.reply_text('Введите нового пользователя', reply_markup=ReplyKeyboardRemove())


#  def add_new_user(bot, update, user_data):
#    """Запись информации о пользователе в текстовый файл"""
#    new_user = update.message.text
#    user_data['teacher1'].append(new_user)  # Добавляем нового ученика в user_data
#    with open('teacher1.txt', 'a', encoding='ptcp154') as t1_file:
#        # TODO: Здесь мы будем добавлять нового ученика не в текстовый документ, а в бд
#        t1_file.write(f'\n{new_user}')


def delete_user(bot, update, user_data):  # создаю функцию удаления юзера
    del_user = update.message.text
    try:
        user_data['teacher1'].remove(del_user)
    except ValueError:
        update.message.reply_text('Нет такого студента')
    except TypeError:
        update.message.reply_text('')
    except KeyError:
        update.message.reply_text('Введите имя преподавателя')


def see_students_list(bot, update, user_data):  # Просмотр всех учеников
    students_list_keyboard = []
    for student in user_data['teacher1']:
        student_button = list[student]
        students_list_keyboard.append(student_button)
    update.message.reply_text('Список студентов:', students_list_keyboard)
    return 'student'


def see_students_tasks(bot, update, user_data):
    students_name = update.message.text()
    tasks_keyboard = [
        ['/done_tasks'],
        ['/undone_tasks'],
        ['/questions']
    ]
    update.message.reply_text('', tasks_keyboard)
    return 'tasks'


def get_fallback(bot, update, user_data):
    update.message.reply_text('Пожалуйста, переформулируйте ответ')

def clean_temporary_user_data(bot, update,user_data):
    pass

def save_users(user='Sergey', git_url='www.github.com', gmt=2):
    repeat_user = Users.query.filter(Users.user == user).order_by(Users.gmt, git_url).first()
    print(repeat_user)

def save_data_users(bot, update, user_data):#функция добавления данных в бд
    user=user_data['student_user']
    repeat_user = Users.query.filter(Users.user == user).first()
    if not repeat_user:   
        new_user = Users(user=user, git_url=user_data['git'], gmt=user_data['gmt'])
        db.db_session.add(new_user)
        db.db_session.commit()
        return 'saved'
    else:
        return 'allready exist'
    

def dialog_start(bot, update, user_data):#начало диалога
    update.message.reply_text('Введите имя студента', reply_markup=ReplyKeyboardRemove())
    return 'user'


def dialog_user(bot, update, user_data):
    user_data['student_user']=update.message.text
    user=user_data['student_user']
    repeat_user = Users.query.filter(Users.user == user).first()
    if repeat_user:
        print('aaa')
        update.message.reply_text(f'Пользователь с именем {user} уже существует')
        return ConversationHandler.END
    update.message.reply_text('Введите ссылку на github')
    return 'github'

def dialog_git(bot, update, user_data):
    user_data['git']=update.message.text
    update.message.reply_text('Введите ваш часовой пояс')
    return 'gmt'

def dialog_gmt(bot, update, user_data):
    user_data['gmt']=int(update.message.text)
    result=save_data_users(bot, update, user_data)
    update.message.reply_text(result)
    return ConversationHandler.END