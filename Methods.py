from pathlib import Path
from pycbrf.toolbox import ExchangeRates
import datetime
import Config


d1 = datetime.timedelta(days=1)
d3 = datetime.timedelta(days=3)
d7 = datetime.timedelta(days=7)
m1 = datetime.timedelta(days=31)
m6 = datetime.timedelta(days=183)
y1 = datetime.timedelta(days=366)


def get_text_from_file_amster(number):
    path = Path(Path.cwd(), "Amsterdam", f"{str(number)}.txt")
    with open(path) as file:
        return file.read()


def get_pic_path_amster(number):
    return str(Path(Path.cwd(), "Amsterdam", f"{str(number)}.png"))


def get_text_from_file_moscow(number):
    path = Path(Path.cwd(), "Moscow", f"{str(number)}.txt")
    with open(path) as file:
        return file.read()


def get_pic_path_moscow(number):
    return str(Path(Path.cwd(), "Moscow", f"{str(number)}.png"))


# Rub в USD
def get_usd_cb(price):
    rates = ExchangeRates(datetime.datetime.now())
    return float('{:.2f}'.format(price / float(rates['USD'].value)))


# USD в RUB
def get_rub_cb(price):
    rates = ExchangeRates(datetime.datetime.now())
    return float('{:.2f}'.format(price * float(rates['USD'].value)))


def get_price_period(period):
    if period == '1_day':
        return Config.PRICE_DAY
    if period == '1_week':
        return Config.PRICE_WEEK
    if period == '1_month':
        return Config.PRICE_MONTH
    if period == '6_month':
        return Config.PRICE_6_MONTH
    if period == '1_year':
        return Config.PRICE_YEAR


def get_datetime(duration, date):
    if duration == '1_day':
        return (date + d1).strftime('%d.%m.%Y')
    if duration == '1_week':
        return (date + d7).strftime('%d.%m.%Y')
    if duration == '1_month':
        return (date + m1).strftime('%d.%m.%Y')
    if duration == '6_month':
        return (date + m6).strftime('%d.%m.%Y')
    if duration == '1_year':
        return (date + y1).strftime('%d.%m.%Y')


def active_vpn_msg(amster_list, moscow_list):
    result = ''
    numer = 1
    if len(amster_list) == 0:
        result = result + 'У Вас нет активных VPN в Амстердаме\nВоспользуйтесь командой /buynew'
    else:
        for i in amster_list:
            result = result + f'\nVPN #{numer}. Амстердам. Доступ до: {i[1]}'
            numer += 1
        result = result + '\nДля продления подписки воспользуйтесь командой /extend'
    if len(moscow_list) == 0:
        result = result + '\n\nУ Вас нет активных VPN в Москве\nВоспользуйтесь командой /buynew'
    else:
        for i in moscow_list:
            result = result + f'\n\nVPN #{numer}. Москва. Доступ до: {i[1]}'
            numer += 1
        result = result + '\nДля продления подписки воспользуйтесь командой /extend'
    return result


def days_after_3(date):
    return (date + d3).strftime('%d.%m.%Y')


def days_before_3(date):
    return (date - d3).strftime('%d.%m.%Y')
