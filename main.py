import datetime
from docxtpl import DocxTemplate

# получение даты
months_list = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь',
               'декабрь']

now = datetime.datetime.now()
year = now.year
day = now.day
number_month = now.month
month = months_list[now.month - 1]  # заполняется месяц в котором сдается отчет
months = months_list[now.month - 2]  # заполняется месяц за который сдается отчет
# --- # --- # --- # --- #

# answer = input("Хочешь дополнить БД (ДА - д)/(НЕТ - н):   ").lower()
# if answer[0] == "д" or answer[0] == 'l':
#     print("OK")
#     # TODO заполнение данных в БД
# else:
#     print("NO")

COEFFICIENT = 0.2345
COEFFICIENT_ENERGY = 0.123

# Запись данных в word файл
answer_total = 0
answer_released = 0
answer_energy = 0

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
        answer_energy = float(input(f"тыс.квт/ч. за {months} {year}г.:   "))
        break
    except ValueError:
        print("Ошибка ввода")
        continue


def total_spend_released(meters, coefficient):
    """Получает из м3 т.у.т."""
    tmp = str(meters * coefficient).split(".")
    return int(tmp[0]), round(float(f"0.{tmp[1]}"), 3)


def total_spend_energy(kwt, coefficient):
    """Получение из квт/ч т.у.т."""
    tmp = str(kwt * coefficient / 1000).split(".")
    return int(tmp[0]), round(float(f"0.{tmp[1]}"), 3)


total_spent, fraction_spent = total_spend_released(answer_total,
                                                   coefficient=COEFFICIENT)
released_population, fraction_released = total_spend_released(answer_released,
                                                              coefficient=COEFFICIENT)
total_energy, fraction_energy = total_spend_energy(answer_energy,
                                                   coefficient=COEFFICIENT_ENERGY)

print(total_spent, fraction_spent, sep='\n')
print(released_population, fraction_released, sep='\n')
print(total_energy, fraction_energy, sep='\n')

# TODO записыва тыс.квт/ч. в колонку нужно как-то правильно

# Запись данных в word.doc
doc = DocxTemplate("starting.docx")
context = {
    'month': month,
    'months': months,
    'year': year,
    'day': day,
}
doc.render(context)
doc.save(f"№{number_month - 1} январь - {months} {year}.docx")

# ---  # --- # --- # --- #
