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
        answer = input("\nХочешь дополнить БД (ДА - д)/(НЕТ - н):   ").lower()
        if answer[0] == "д" or answer[0] == "l":
            answer_year = input("Год:   ")
            answer_month = input("Месяц:   ")
            answer_spend = input("Израсходовано всего в т.у.т.:   ")
            answer_population = input("Отпущено населению в т.у.т:   ")
            answer_kilowatt = input("тыс.квт/ч.:   ")
            answer_consumption = input("Суммарное потребление тэр:   ")
            answer_db_save = input("\nСохранить эти данные в БД (ДА - д)/(НЕТ - н):   ").lower()
            if answer_db_save[0] == "д" or answer_db_save[0] == "l":
                Report(
                    total_spend=answer_spend, fraction_spend=0, released_population=answer_population,
                    fraction_rel_pop=0,
                    thousand_kilowatt_hours=answer_kilowatt,
                    integer_standard_fuel_ton=0, fraction_standard_fuel_ton=0, year=answer_year,
                    month=f"январь - {answer_month}", total_consumption=answer_consumption
                ).save()
            else:
                print("Отмена")
        else:
            global start_populating_database
            start_populating_database = False
            return start_populating_database

    def fill_report(self):
        """Заполнение отчета"""
        answer_fill_report = input("\nПриступаем к заполнению отчёта (ДА - д)/(НЕТ - н):   ").lower()
        answer_m3 = 0
        answer_m3_released = 0
        if answer_fill_report[0] == "д" or answer_fill_report[0] == "l":
            while True:
                try:
                    answer_m3 = float(input(f"Израсходовано всего м3 за {self.months} {self.year}г.:   "))
                    break
                except ValueError:
                    print("Ошибка ввода")
                    continue
            while True:
                try:
                    answer_m3_released = float(input(f"Отпущено населению м3 за {self.months} {self.year}г.:   "))
                    break
                except ValueError:
                    print("Ошибка ввода")
                    continue
            t_s, t_f = self.total_spend_released(answer_m3)
            r_p, r_f = self.total_spend_released(answer_m3_released)
            # TODO нужно как-то правильно добавить данные в БД
            # TODO прежде чем сохранить данные в БД необходимо слажить дробные части т.у.т. полученые из БД
        else:
            print("Тогда выходим")

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
        # TODO получить данные за соответствующий период
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


if __name__ == "__main__":
    temp = Reports()
    # Запуск предворительного заполнения БД в бесконечном цикле while
    while start_populating_database:
        temp.populating_database()
    # Запуск заполнения отчета
    temp.fill_report()
# --- # --- # --- # --- #
