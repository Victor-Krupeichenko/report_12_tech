from peewee import *

database = SqliteDatabase('database.db')  # с какой имено будет взаимадействовать наше приложение


class BaseModel(Model):
    class Meta:
        database = database  # с какой бд будет взаимодействовать
        order_by = 'id'  # по какому полю проводить сортировку


class Report(BaseModel):
    year = CharField()  # год
    month = CharField()  # месяц
    total_spend = IntegerField()  # израсходовано всего (т.у.т. -целые)
    fraction_spend = FloatField()  # израсходовано всего (т.у.т. -дробная часть)
    released_population = IntegerField()  # отпущено населению(т.у.т. - целые)
    fraction_rel_pop = FloatField()  # отпущено населению(т.у.т. - дробная часть)
    thousand_kilowatt_hours = IntegerField()  # тыс.квт/ч.
    integer_standard_fuel_ton = IntegerField()  # тыс.квт/ч. в т.у.т (целые)
    fraction_standard_fuel_ton = FloatField()  # тыс.квт/ч. в т.у.т (дробные)
    total_consumption = IntegerField()  # суммарное потребление тэр

    class Meta:
        table_name = 'reports_12_tek'
