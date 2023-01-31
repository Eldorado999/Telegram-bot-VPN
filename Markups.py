from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_exit = InlineKeyboardButton(text='🚪Выйти', callback_data='exit')

# Кнопка после /start #1
button_what_is_vpn = InlineKeyboardButton(text='Что такое VPN?', callback_data='what_is_vpn')
markup_what_is_vpn = InlineKeyboardMarkup(row_width=1)
markup_what_is_vpn.insert(button_what_is_vpn)

# Кнопка после /start #2
button_why_vpn = InlineKeyboardButton(text='Зачем нужен VPN?', callback_data='why_vpn')
markup_why_vpn = InlineKeyboardMarkup(row_width=1)
markup_why_vpn.insert(button_why_vpn)

# Кнопка после /start #3
button_why_own_vpn = InlineKeyboardButton(text='Какие есть варианты VPN?', callback_data='why_own_vpn')
markup_why_own_vpn = InlineKeyboardMarkup(row_width=1)
markup_why_own_vpn.insert(button_why_own_vpn)

# Кнопка после /start #4
button_price = InlineKeyboardButton(text='Узнать расценки', callback_data='price')
markup_price = InlineKeyboardMarkup(row_width=1)
markup_price.insert(button_price)

# Кнопки после /buynew
button_amster = InlineKeyboardButton(text='🇳🇱Амстердам', callback_data='amster')
button_moscow = InlineKeyboardButton(text='🇷🇺Москва', callback_data='moscow')
markup_city = InlineKeyboardMarkup(row_width=1)
markup_city.add(button_amster, button_moscow, button_exit)


# Выбор срока подписки
def period_button(menu_type):
    button_1day = InlineKeyboardButton(text='1 день', callback_data='1_day' + menu_type)
    button_1week = InlineKeyboardButton(text='1 неделя', callback_data='1_week' + menu_type)
    button_1month = InlineKeyboardButton(text='1 месяц', callback_data='1_month' + menu_type)
    button_6month = InlineKeyboardButton(text='6 месяцев', callback_data='6_month' + menu_type)
    button_1year = InlineKeyboardButton(text='1 год', callback_data='1_year' + menu_type)
    if menu_type == 'New':
        button_back_to_ = InlineKeyboardButton(text='⏪Назад', callback_data='back_city')
    elif menu_type == 'Extend':
        button_back_to_ = InlineKeyboardButton(text='⏪Назад', callback_data='back_extend')
    else:
        button_back_to_ = InlineKeyboardButton(text='Ничего не делать', callback_data='Nothing')
    markup_period = InlineKeyboardMarkup(row_width=1)
    markup_period.add(button_1day, button_1week, button_1month, button_6month, button_1year, button_back_to_, button_exit)
    return markup_period


# Выбор способа оплаты
button_qiwi = InlineKeyboardButton(text='🥝Оплата через Qiwi в руб.', callback_data='qiwi')
button_usdt = InlineKeyboardButton(text='🪙Оплата trc-20 в USDT', callback_data='usdt')
button_back_to_period_new = InlineKeyboardButton(text='⏪Назад', callback_data='back_period_new')
markup_payment_new = InlineKeyboardMarkup(row_width=1)
markup_payment_new.add(button_qiwi, button_usdt, button_back_to_period_new, button_exit)
button_back_to_period_ext = InlineKeyboardButton(text='⏪Назад', callback_data='back_period_ext')
markup_payment_ext = InlineKeyboardMarkup(row_width=1)
markup_payment_ext.add(button_qiwi, button_usdt, button_back_to_period_ext, button_exit)


# Ссылка на оплату QIWI и кнопка проверки
def pay_link_button(_url, bill_id):
    button_pay_link = InlineKeyboardButton(text='Ссылка на оплату', url=_url)
    button_payment_status = InlineKeyboardButton(text='🔄Проверить оплату', callback_data='qiwi_check_' + bill_id)
    markup_pay_link = InlineKeyboardMarkup(row_width=1)
    return markup_pay_link.add(button_pay_link, button_payment_status)


# Кнопка для ввода hash транзакции и проверки оплаты USDT
def read_hash_usdt(bill_id):
    button_read_hash = InlineKeyboardButton(text='Ввести hash', callback_data='read_hash_' + bill_id)
    markup_read_hash = InlineKeyboardMarkup(row_width=1)
    return markup_read_hash.insert(button_read_hash)


# Кнопка для повторного ввода hash транзакции и проверки оплаты USDT
def check_usdt_status(bill_id, _hash):
    button_check_status_usdt = InlineKeyboardButton(text='🔄Проверить подтверждение транзакции',
                                                    callback_data='usdt_status_' + bill_id)
    button_read_hash_again = InlineKeyboardButton(text='Ввести другой hash', callback_data='read_hash_' + bill_id)
    markup_check_status_usdt = InlineKeyboardMarkup(row_width=1)
    return markup_check_status_usdt.add(button_check_status_usdt, button_read_hash_again)


# Создание кнопок для продления подписки
def extend_buttons(amster_list, moscow_list):
    markup_extend = InlineKeyboardMarkup(row_width=1)
    if len(amster_list) == 0:
        pass
    else:
        for i in amster_list:
            button_amster_vpn = InlineKeyboardButton(text=f'🇳🇱Амстердам, до: {i[1]}', callback_data='amster_' + str(i[0]))
            markup_extend.add(button_amster_vpn)
    if len(moscow_list) == 0:
        pass
    else:
        for i in moscow_list:
            button_moscow_vpn = InlineKeyboardButton(text=f'🇷🇺Москва, до: {i[1]}', callback_data='moscow_' + str(i[0]))
            markup_extend.add(button_moscow_vpn)
    return markup_extend.add(button_exit)
