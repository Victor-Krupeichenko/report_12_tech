import datetime
from docxtpl import DocxTemplate
from models import *
from decimal import Decimal, ROUND_HALF_UP
import shutil
import os

# Вывод текста по середине консоли
lines = ["Заполнение отчета 12-ТЭК", "ГП 'Лоевское ПМС'", "Version 1.0(beta)"]

width = shutil.get_terminal_size().columns
position = (width - max(map(len, lines))) // 2
for line in lines:  # center
    print(line.center(width))

print("Разработано:\nКрупейченко В.Г.\n07.11.2022г.")

# Создание БД если таковая отсуствует
with database:
    database.create_tables([Report])  # создание таблицы
print('\ndatabase loaded...'.upper())

months_list = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь',
               'декабрь']

rename_month = []

# Изменение окончаний у месяцев
for mon in months_list:
    rename_month.append(mon.replace("ь", "я"))
    if mon[-1] == "т":
        rename_month.append(mon + "а")
        rename_month.remove(mon)
    elif mon[-1] == "й":
        rename_month.append(mon[:-1] + "я")
        rename_month.remove(mon)

# получение текущей даты
now = datetime.datetime.now()
year = now.year
day = now.day
number_month = now.month
month = rename_month[now.month - 1]  # заполняется месяц в котором сдается отчет
months = months_list[now.month - 2]  # заполняется месяц за который сдается отчет


class Reports:
    def __init__(self):
        self.coefficient = 0.2345
        self.coefficient_energy = 0.123

    def questions_pre_filling_database(self):
        """Вопросы для предварительного заполнения БД"""
        answer_year = input("Год:   ")
        answer_month = input("Месяц:   ")
        answer_spend = input("Израсходовано всего в т.у.т.:   ")
        answer_population = input("Отпущено населению в т.у.т:   ")
        answer_kilowatt = input("тыс.квт/ч.:   ")
        answer_consumption = input("Суммарное потребление тэр:   ")
        return answer_year, answer_month, answer_spend, answer_population, answer_kilowatt, answer_consumption

    def db_previously(self):
        """Предварительное заполнение БД"""
        answer_previously = input("\n" + r"Предварительно заполнить БД - ДА(д) \ НЕТ(н):   ").lower()
        if answer_previously[0] == "д" or answer_previously[0] == "l":
            tmp = self.questions_pre_filling_database()
            save_to_db = input("\n" + r"Сохранить эти данные в БД - ДА(д) \ НЕТ(н):   ").lower()
            if save_to_db[0] == "д" or save_to_db[0] == 'l':
                Report(
                    year=tmp[0], month=f"январь - {tmp[1]}", total_spend=tmp[2], released_population=tmp[3],
                    thousand_kilowatt_hours=tmp[4], total_consumption=tmp[5]).save()
        else:
            global start_populating_database
            start_populating_database = False
            return start_populating_database

    def getting_latest_record(self):
        """Получение последней записи из БД"""
        tmp = Report.select().order_by(Report.id.desc()).get_or_none()
        tmp_list = [tmp.total_spend, tmp.released_population, tmp.thousand_kilowatt_hours, tmp.total_consumption,
                    tmp.month]
        return tmp_list

    def getting_corresponding_period(self):
        """Получение данных за соответствующий период"""
        tmp = Report.select().where((Report.year == f"{year - 1}") & (Report.month == f"январь - {months}"))
        if tmp:
            t_list = []
            for i in tmp:
                t_list.extend([i.total_spend, i.released_population, i.thousand_kilowatt_hours, i.total_consumption])
            return t_list
        else:
            return None

    def total_spend_released(self, meters):
        """Переводит м3 в т.у.т.
        :return: Возвращает значения т.у.т.
        (Converts m3 to t.c.f.
        Returns two values integer and fractional part in t.c.f.)
        """
        tmp = str(meters * self.coefficient)
        obj = Decimal(tmp)
        return obj.quantize(Decimal("1"), ROUND_HALF_UP)

    def total_spend_energy(self, kwt):
        """Переводит тыс.квт/ч. в т.у.т.
        :return: Возвращает  в т.у.т.
        """
        tmp = str(kwt * 1000 * self.coefficient_energy / 1000)
        obj = Decimal(tmp)
        return obj.quantize(Decimal("1"), ROUND_HALF_UP)

    def questions_for_report(self):
        """вопросы для отчета"""
        test_dict = {
            'question_total': 0, 'question_released': 0, 'question_energy': 0,
        }

        question = [
            f"Израсходовано всего м3 за {months} {year}г.:   ", f"Отпущено населению м3 за {months} {year}г.:   ",
            f"тыс.квт/ч. за {months} {year}г.:   "
        ]
        for j, key in enumerate(test_dict):
            while True:
                try:
                    test_dict[key] = float(input(question[j]))
                    break
                except ValueError:
                    print("ошибка ввода")
        return test_dict

    def addition_past_current_data(self, question_spend, question_released, question_energy):
        """Сложение данных за прошлый(если такой есть) и текущий месяц"""
        if not months == 'январь':
            latest_record = self.getting_latest_record()  # получение последней записи из БД
            total_spend = latest_record[0] + self.total_spend_released(
                question_spend)  # израсходовано всего
            total_released = latest_record[1] + self.total_spend_released(question_released)  # отпущено населению
            total_energy = latest_record[2] + int(question_energy)  # тыс.квт/ч.
            total_con = self.total_spend_energy(question_energy) + total_spend  # с начала года
            # Сохранение в БД
            Report(
                year=year, month=f"январь - {months}", total_spend=total_spend, released_population=total_released,
                thousand_kilowatt_hours=total_energy, total_consumption=total_con).save()
            return total_spend, total_released, total_energy, total_con
        else:
            total_spend = self.total_spend_released(question_spend)  # израсходовано всего
            total_released = self.total_spend_released(question_released)  # отпущено населению
            total_energy = int(question_energy)  # тыс.квт/ч.
            total_con = self.total_spend_energy(question_energy) + total_spend  # с начала года
            # Сохранение в БД
            Report(
                year=year, month=f"январь - {months}", total_spend=total_spend, released_population=total_released,
                thousand_kilowatt_hours=total_energy, total_consumption=total_con).save()
            return total_spend, total_released, total_energy, total_con

    def docx_save(self, m, period, y, d, ts, tr, te, tc, gts, gtr, gte, gtc, jo, ph, su):
        """
        Запись данных в word.docx
        :return: новый заполненый документ word
        """
        doc = DocxTemplate("starting.docx")
        homedir = os.path.expanduser('~')
        context = {
            "m": m,
            "ms": period,
            "ye": y,
            "day": d,
            "ts": ts,
            "tr": tr,
            "te": te,
            "tc": tc,
            "gts": gts,
            "gtr": gtr,
            "gte": gte,
            "gtc": gtc,
            "job": jo,
            "phone": ph,
            "surname": su,
        }
        doc.render(context)
        doc.save(homedir + f"\Desktop\\12-ТЭК № {number_month - 1} январь - {months} {year}.docx")


if __name__ == "__main__":
    temp = Reports()
    start_populating_database = True  # Запуск предворительного заполнения БД (в бесконечном цикле while)
    while start_populating_database:
        temp.db_previously()
    getting_data = temp.getting_corresponding_period()  # получение данных за соответствующий период прошлого года
    if getting_data is not None:
        print(f"Данные за период январь - {months} {year - 1}г. получены!\n")
    else:
        print(f"Данные за период январь - {months} {year - 1}г. отсутствуют!\n")

    print("Заполните данные (Если новых данных не поступало – то введите 0(ноль)):")
    questions = temp.questions_for_report()
    data = temp.addition_past_current_data(question_spend=questions["question_total"],
                                           question_released=questions["question_released"],
                                           question_energy=questions["question_energy"])
    job = input("Должность:   ").capitalize()
    if input("Номер телефона или Email 1/2:   ") == "1":
        phone = input("Номер:   ")
    else:
        phone = input("Email:   ")
    surname = input("Инициалы, Фамилия (Например - И.И. Иванов):   ")

    temp.docx_save(m=month, period=months, y=year, d=day, ts=data[0], tr=data[1], te=data[2], tc=data[3],
                   gts=getting_data[0], gtr=getting_data[1], gte=getting_data[2], gtc=getting_data[3], jo=job,
                   ph=phone, su=surname)
