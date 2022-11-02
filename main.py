import datetime
from docxtpl import DocxTemplate
from models import *

# Создание БД если таковая отсуствует
with database:
    database.create_tables([Report])  # создание таблицы
print('loaded...'.upper())
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
print(months)
# --- # --- # --- # --- #


start_populating_database = True  # Запуск предворительного заполнения БД (в бесконечном цикле while)


class Reports:
    def __init__(self):
        self.coefficient = 0.2345
        self.coefficient_energy = 0.123
        self.year = now.year
        self.day = now.day
        self.months = months_list[now.month - 2]

    def questions_report(self):
        """Вопросы для предварительного заполнения БД"""
        answer_year = input("Год:   ")
        answer_month = input("Месяц:   ")
        answer_spend = input("Израсходовано всего в т.у.т.:   ")
        answer_population = input("Отпущено населению в т.у.т:   ")
        answer_kilowatt = input("тыс.квт/ч.:   ")
        answer_consumption = input("Суммарное потребление тэр:   ")
        return [answer_year, answer_month, answer_spend, answer_population, answer_kilowatt, answer_consumption]

    def db_previously(self):
        """Предварительное заполнение БД"""
        answer_previously = input("\n" + r"Предварительно заполнить БД - ДА(д) \ НЕТ(н):   ").lower()
        if answer_previously[0] == "д" or answer_previously[0] == "l":
            tmp = self.questions_report()
            save_to_db = input("\n" + r"Сохранить эти данные в БД - ДА(д) \ НЕТ(н):   ").lower()
            if save_to_db[0] == "д" or save_to_db[0] == 'l':
                Report(
                    year=tmp[0], month=f"январь - {tmp[1]}", total_spend=tmp[2], released_population=tmp[3],
                    thousand_kilowatt_hours=tmp[4], total_consumption=tmp[5], fraction_spend=0, fraction_rel_pop=0,
                    integer_standard_fuel_ton=0, fraction_standard_fuel_ton=0
                ).save()
        else:
            global start_populating_database
            start_populating_database = False
            return start_populating_database

    def getting_latest_record(self):
        """Получение последней записи из БД"""
        tmp = Report.select().order_by(Report.id.desc()).get_or_none()
        tmp_list = [tmp.year, tmp.month, tmp.total_spend, tmp.fraction_spend, tmp.released_population,
                    tmp.fraction_rel_pop, tmp.thousand_kilowatt_hours,
                    tmp.integer_standard_fuel_ton,
                    tmp.fraction_standard_fuel_ton, tmp.total_consumption]
        return tmp_list

    def getting_corresponding_period(self):
        """Получение данных за соответствующий период"""
        tmp = Report.select().where((Report.year == f"{self.year - 1}") & (Report.month == f"январь - {self.months}"))
        if tmp:
            t_list = []
            for i in tmp:
                t_list.extend([i.total_spend, i.released_population, i.thousand_kilowatt_hours, i.total_consumption])
            print(t_list[0], t_list[1], t_list[2], t_list[3])
            return t_list
        else:
            print(f"Данные за период январь - {self.months} {self.year - 1}г. в БД отсутствуют!")

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
        tmp = str(kwt * 1000 * self.coefficient_energy / 1000).split(".")
        return int(tmp[0]), float(f"0.{tmp[1]}")

    def addition_past_current_data(self, ans_total, rel_total, energy_total):
        """Сложение прошлых и текущих данных"""

        # TODO добавить проверку если заполняется за январь

        latest_record = self.getting_latest_record()
        total_spend = self.total_spend_released(ans_total)
        total = total_spend[0] + latest_record[2]  # израсходовано всего (прошлый  + текущи месяц)
        released_spend = self.total_spend_released(rel_total)
        released = released_spend[0] + latest_record[4]  # отпущено населению (прошлый + текущий месяц)
        spend_energy = self.total_spend_energy(energy_total)
        energy = energy_total + latest_record[6]  # тыс.квт/ч. (прошлый + текущий месяц)
        print(total, released, energy, spend_energy)

    def docx_save(self, m, ms, get_s, get_p, get_k, get_c):
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
            "get_s": get_s,
            "get_p": get_p,
            "get_k": get_k,
            "get_c": get_c,
        }
        doc.render(context)
        doc.save(f"№ {number_month - 1} январь - {months} {self.year}.docx")


if __name__ == "__main__":
    temp = Reports()
    # Запуск предворительного заполнения БД в бесконечном цикле while
    # while start_populating_database:
    #     temp.db_previously()
    # g_c_p = temp.getting_corresponding_period()  # получение данных за соответствующий период прошлого года
    # temp.docx_save(m=month, ms=months, get_s=g_c_p[0], get_p=g_c_p[1], get_k=g_c_p[2], get_c=g_c_p[3])
    answer_total = 0  # Израсходовано всего
    answer_released = 0  # Отпущено населению
    answer_energy = 0  # тыс.квт/ч.

    while True:
        try:
            answer_total = float(input(f"Израсходовано всего м3 за {months} {year}г.:   "))
            break
        except ValueError:
            print("Ошибка ввода")
            continue

    while True:
        try:
            answer_released = float(input(f"Отпущено населению м3 за {months} {year}г.:   "))
            break
        except ValueError:
            print("Ошибка ввода")
            continue

    while True:
        try:
            answer_energy = int(input(f"тыс.квт/ч. за {months} {year}г.:   "))
            break
        except ValueError:
            print("Ошибка ввода")
            continue

    temp.addition_past_current_data(ans_total=answer_total, rel_total=answer_released, energy_total=answer_energy)
# --- # --- # --- # --- #
