import datetime
from docxtpl import DocxTemplate
from models import *

# Создание БД если таковая отсуствует
with database:
    database.create_tables([Report])  # создание таблицы
print('DONE')
# --- # --- # --- # --- #

# получение даты
months_list = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь',
               'декабрь']

now = datetime.datetime.now()
year = now.year
day = now.day
number_month = now.month
month = months_list[now.month - 1]  # заполняется месяц в котором сдается отчет
# TODO менять оканчание месяца
months = months_list[now.month - 2]  # заполняется месяц за который сдается отчет

# --- # --- # --- # --- #

answer_total = 0
answer_released = 0
answer_energy = 0

start_populating_database = True  # Запуск предворительного заполнения БД (в бесконечном цикле while)


class Reports:
    def __init__(self):
        self.coefficient = 0.2345
        self.coefficient_energy = 0.123
        self.year = now.year
        self.day = now.day
        self.months = months_list[now.month - 2]

    def populating_database(self):
        """
        Заполнение БД
        """
        answer = input("Хочешь дополнить БД (ДА - д)/(НЕТ - н):   ").lower()
        if answer[0] == "д" or answer[0] == "l":
            # TODO заполнение данных в БД
            Report.create(
                total_spend=32, fraction_spend=0.52, released_population=15, fraction_rel_pop=0.15,
                thousand_kilowatt_hours=777,
                integer_standard_fuel_ton=3, fraction_standard_fuel_ton=0.03, year=year, month=f"январь - {months}"
            )
            # TODO пробовать задавать вопросы в бесконечном цикле для заполнения БД
        else:
            print("NO")
            global start_populating_database
            start_populating_database = False
            return start_populating_database

    def total_spend_released(self, meters):
        """Переводит м3 в т.у.т.
        :param meters: m3
        :return: Возвращает два значения: целою и дробную часть в т.у.т.
        (Converts m3 to t.c.f.
        Returns two values integer and fractional part in t.c.f.)
        """
        tmp = str(meters * self.coefficient).split(".")
        return int(tmp[0]), float(f"0.{tmp[1]}")

    def total_spend_energy(self, kwt):
        """Переводит тыс.квт/ч. в т.у.т.
        :param kwt:
        :return: Возвращает два значения: целою и дробную часть в т.у.т.
        """
        tmp = str(kwt * self.coefficient_energy / 1000).split(".")
        return int(tmp[0]), float(f"0.{tmp[1]}")

    def docx_save(self, m, ms):
        """
        Запись данных в word.docx
        :return: новый заполненый документ word
        """
        doc = DocxTemplate("starting.docx")
        # TODO добавить остольные параметры в context
        context = {
            "month": m,
            "months": ms,
            "year": self.year,
            "day": self.day,
        }
        doc.render(context)
        doc.save(f"№{number_month - 1} январь - {months} {self.year}.docx")


# TODO записыва тыс.квт/ч. в колонку нужно как-то правильно

temp = Reports()

# Запуск предворительного заполнения БД в бесконечном цикле while
while start_populating_database:
    temp.populating_database()
# --- # --- # --- # --- #
