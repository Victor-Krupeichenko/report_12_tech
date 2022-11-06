from peewee import *

database = SqliteDatabase('12_tek_database.db')  # с какой имено будет взаимадействовать наше приложение


class BaseModel(Model):
    class Meta:
        database = database  # с какой бд будет взаимодействовать
        order_by = 'id'  # по какому полю проводить сортировку


class Report(BaseModel):
    year = CharField()  # год
    month = CharField()  # месяц
    total_spend = IntegerField()  # израсходовано всего (т.у.т. -целые)
    released_population = IntegerField()  # отпущено населению(т.у.т. - целые)
    thousand_kilowatt_hours = IntegerField()  # тыс.квт/ч.
    total_consumption = IntegerField()  # израсходовано всего (total_spend + integer_standard_fuel_ton)

    class Meta:
        table_name = 'reports_12_tek'
