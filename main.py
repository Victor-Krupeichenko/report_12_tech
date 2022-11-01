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
        tmp_list = [tmp.year, tmp.month, tmp.total_spend, tmp.released_population, tmp.thousand_kilowatt_hours,
                    tmp.total_consumption, tmp.fraction_spend, tmp.fraction_rel_pop, tmp.integer_standard_fuel_ton,
                    tmp.fraction_standard_fuel_ton]
        return tmp_list

    def getting_corresponding_period(self):
        """Получение данных за соответствующий период"""
        tmp = Report.select().where((Report.year == f"{self.year + 1}") & (Report.month == f"январь - {self.months}"))
        if tmp:
            t_list = []
            for i in tmp:
                t_list.extend([i.total_spend, i.released_population, i.thousand_kilowatt_hours, i.total_consumption])
            print(t_list[0], t_list[1], t_list[2], t_list[3])
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

    def docx_save(self, m, ms):
        """
        Запись данных в word.docx
        :return: новый заполненый документ word
        """
        doc = DocxTemplate("starting.docx")
        # TODO получить данные за соответствующий период
        # TODO добавить остольные параметры в context
        tmp = self.getting_latest_record()
        context = {
            "month": m,
            "months": ms,
            "year": self.year,
            "day": self.day,
            "t": tmp[4]
        }
        doc.render(context)
        doc.save(f"№ {number_month - 1} январь - {months} {self.year}.docx")


if __name__ == "__main__":
    temp = Reports()
    # Запуск предворительного заполнения БД в бесконечном цикле while
    # while start_populating_database:
    #     temp.db_previously()
    temp.getting_corresponding_period()
# --- # --- # --- # --- #
