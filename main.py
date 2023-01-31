import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import Qiwi_payment
import Usdt_payment
import asyncio
import aioschedule
import datetime
from db import Database
import Config
import Messages
import Markups
import Methods


logging.basicConfig(level=logging.INFO)
bot = Bot(token=Config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database('Create_VPN_bot.db')


class Form(StatesGroup):
    hash = State()


async def give_vpn_amster(user_id, date):
    num = db.give_vpn_amster(user_id, date)
    picture = open(Methods.get_pic_path_amster(num), 'rb')
    await bot.send_message(user_id, Methods.get_text_from_file_amster(num))
    await bot.send_photo(user_id, picture)
    await bot.send_message(Config.ADMIN_ID, f'Выдаю пользователю {user_id} VPN amster #{num}')


async def give_vpn_moscow(user_id, date):
    num = db.give_vpn_moscow(user_id, date)
    picture = open(Methods.get_pic_path_moscow(num), 'rb')
    await bot.send_message(user_id, Methods.get_text_from_file_moscow(num))
    await bot.send_photo(user_id, picture)
    await bot.send_message(Config.ADMIN_ID, f'Выдаю пользователю {user_id} VPN moscow #{num}')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            join_date = datetime.datetime.now().strftime("%d.%m.%Y")
            db.add_user(message.from_user.id, message.from_user.username, join_date)
            await bot.send_message(Config.ADMIN_ID, f'Новый пользователь:'
                                                    f'\n{message.from_user.id, message.from_user.username}')
        await bot.send_message(message.from_user.id, Messages.start_msg, reply_markup=Markups.markup_what_is_vpn)


@dp.message_handler(commands=['help'])
async def help_menu(message: types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.from_user.id, Messages.help_msg)


@dp.message_handler(commands=['price'])
async def price(message: types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.from_user.id, Messages.price_msg)


@dp.message_handler(commands=['instructions'])
async def help_menu(message: types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.from_user.id, Messages.instructions)


@dp.message_handler(commands=['myvpn'])
async def check_active_vpn(message: types.Message):
    if message.chat.type == 'private':
        amster_list = db.check_active_vpn_amster(message.from_user.id)
        moscow_list = db.check_active_vpn_moscow(message.from_user.id)
        await bot.send_message(message.from_user.id, Methods.active_vpn_msg(amster_list, moscow_list))


@dp.message_handler(commands=['buynew'])
async def buy_new_vpn(message: types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.from_user.id, Messages.buy_new_msg, reply_markup=Markups.markup_city)


@dp.message_handler(commands=['extend'])
async def extend_vpn(message: types.Message):
    if message.chat.type == 'private':
        amster_list = db.check_active_vpn_amster(message.from_user.id)
        moscow_list = db.check_active_vpn_moscow(message.from_user.id)
        if len(amster_list) == len(moscow_list) == 0:
            await bot.send_message(message.from_user.id, 'У Вас нет активных VPN для продления'
                                                         '\nВоспользуйтесь командой /buynew')
        else:
            await bot.send_message(message.from_user.id, 'Выберите VPN, который хотите продлить',
                                   reply_markup=Markups.extend_buttons(amster_list, moscow_list))


@dp.message_handler()
async def answer_on_all(message: types.Message):
    if 'кря' in str(message.text).lower():
        await bot.send_message(message.from_user.id, 'Не надо тут крякать')
    else:
        await bot.send_message(message.from_user.id, 'Простите, я Вас не понимаю. Пожалуйста, пользуйтесь командами '
                                                     'из меню или /help')


@dp.callback_query_handler(text='what_is_vpn')
async def what_is_vpn(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, Messages.what_is_vpn, reply_markup=Markups.markup_why_vpn)


@dp.callback_query_handler(text='why_vpn')
async def why_vpn(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, Messages.why_vpn, reply_markup=Markups.markup_why_own_vpn)


@dp.callback_query_handler(text='why_own_vpn')
async def why_own_vpn(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, Messages.why_own_vpn, reply_markup=Markups.markup_price)


@dp.callback_query_handler(text='price')
async def price_command(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, Messages.price_msg)


@dp.callback_query_handler(text='exit')
async def exit_menu(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)


@dp.callback_query_handler(text='amster')
async def choose_pay_amster(callback: types.CallbackQuery):
    db.last_city(callback.from_user.id, 'amster')
    db.last_type(callback.from_user.id, 'New')
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, Messages.choose_period, reply_markup=Markups.period_button('New'))


@dp.callback_query_handler(text='moscow')
async def choose_pay_moscow(callback: types.CallbackQuery):
    db.last_city(callback.from_user.id, 'moscow')
    db.last_type(callback.from_user.id, 'New')
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, Messages.choose_period, reply_markup=Markups.period_button('New'))


@dp.callback_query_handler(text='back_city')
async def back_to_city(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, Messages.buy_new_msg, reply_markup=Markups.markup_city)


@dp.callback_query_handler(text='back_extend')
async def back_to_extend(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    amster_list = db.check_active_vpn_amster(callback.from_user.id)
    moscow_list = db.check_active_vpn_moscow(callback.from_user.id)
    await bot.send_message(callback.from_user.id, 'Выберите VPN, который хотите продлить',
                           reply_markup=Markups.extend_buttons(amster_list, moscow_list))


@dp.callback_query_handler(text_contains='1_day')
async def choose_pay_1d(callback: types.CallbackQuery):
    db.last_pay_period(callback.from_user.id, '1_day')
    menu_type = str(callback.data[5:])
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    if menu_type == 'New':
        await bot.send_message(callback.from_user.id, Messages.choose_payment, reply_markup=Markups.markup_payment_new)
    elif menu_type == 'Extend':
        await bot.send_message(callback.from_user.id, Messages.choose_payment, reply_markup=Markups.markup_payment_ext)


@dp.callback_query_handler(text_contains='1_week')
async def choose_pay_1w(callback: types.CallbackQuery):
    db.last_pay_period(callback.from_user.id, '1_week')
    menu_type = str(callback.data[6:])
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    if menu_type == 'New':
        await bot.send_message(callback.from_user.id, Messages.choose_payment, reply_markup=Markups.markup_payment_new)
    elif menu_type == 'Extend':
        await bot.send_message(callback.from_user.id, Messages.choose_payment, reply_markup=Markups.markup_payment_ext)


@dp.callback_query_handler(text_contains='1_month')
async def choose_pay_1m(callback: types.CallbackQuery):
    db.last_pay_period(callback.from_user.id, '1_month')
    menu_type = str(callback.data[7:])
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    if menu_type == 'New':
        await bot.send_message(callback.from_user.id, Messages.choose_payment, reply_markup=Markups.markup_payment_new)
    elif menu_type == 'Extend':
        await bot.send_message(callback.from_user.id, Messages.choose_payment, reply_markup=Markups.markup_payment_ext)


@dp.callback_query_handler(text_contains='6_month')
async def choose_pay_6m(callback: types.CallbackQuery):
    db.last_pay_period(callback.from_user.id, '6_month')
    menu_type = str(callback.data[7:])
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    if menu_type == 'New':
        await bot.send_message(callback.from_user.id, Messages.choose_payment, reply_markup=Markups.markup_payment_new)
    elif menu_type == 'Extend':
        await bot.send_message(callback.from_user.id, Messages.choose_payment, reply_markup=Markups.markup_payment_ext)


@dp.callback_query_handler(text_contains='1_year')
async def choose_pay_1y(callback: types.CallbackQuery):
    db.last_pay_period(callback.from_user.id, '1_year')
    menu_type = str(callback.data[6:])
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    if menu_type == 'New':
        await bot.send_message(callback.from_user.id, Messages.choose_payment, reply_markup=Markups.markup_payment_new)
    elif menu_type == 'Extend':
        await bot.send_message(callback.from_user.id, Messages.choose_payment, reply_markup=Markups.markup_payment_ext)


@dp.callback_query_handler(text='back_period_new')
async def back_to_period(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, Messages.choose_period, reply_markup=Markups.period_button('New'))


@dp.callback_query_handler(text='back_period_ext')
async def back_to_period(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, Messages.choose_period, reply_markup=Markups.period_button('Extend'))


@dp.callback_query_handler(text='qiwi')
async def qiwi_create_bill(callback: types.CallbackQuery):
    period = db.get_last_pay_period(callback.from_user.id)
    city = db.get_last_city(callback.from_user.id)
    bill_type = db.get_last_type(callback.from_user.id)
    summ = Methods.get_price_period(period)
    bill_list = Qiwi_payment.create_payment(callback.from_user.id, summ)
    if bill_type == 'New':
        db.add_bill_qiwi(bill_list[0], bill_list[1], bill_list[2], bill_list[3], period, city, bill_type)
        await bot.send_message(Config.ADMIN_ID, f'Создан новый счёт QIWI:\n'
                                                f'{bill_list[0]}, {bill_list[1]}, {bill_list[2]}, {bill_list[3]}, '
                                                f'{period}, {city}, {bill_type}')
    elif bill_type == 'Extend':
        extend_num = db.get_extend_num(callback.from_user.id)
        db.add_bill_qiwi(bill_list[0], bill_list[1], bill_list[2], bill_list[3], period, city, bill_type, extend_num)
        await bot.send_message(Config.ADMIN_ID, f'Создан новый счёт QIWI:\n'
                                                f'{bill_list[0]}, {bill_list[1]}, {bill_list[2]}, {bill_list[3]}, '
                                                f'{period}, {city}, {bill_type}, {extend_num}')
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, f'Вам нужно отправить {bill_list[1]} руб. на наш счет QIWI',
                           reply_markup=Markups.pay_link_button(bill_list[4], bill_list[2]))


@dp.callback_query_handler(text_contains='qiwi_check_')
async def qiwi_check_status(callback: types.CallbackQuery):
    bill_id = str(callback.data[11:])
    info = db.get_bill_qiwi(bill_id)
    if info != False:
        if Qiwi_payment.check_payment(bill_id):
            city = info[5]
            user_money = db.user_money(callback.from_user.id)
            money = int(info[1])
            db.set_money(callback.from_user.id, user_money + money)
            db.qiwi_bill_paid(bill_id)
            duration = info[4]
            if info[6] == 'New':
                now_date = datetime.datetime.now()
                until_date = Methods.get_datetime(duration, now_date)
                await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                            text='Счёт оплачен, бот создал Вам личный VPN\nДля помощи в установке '
                                                 'воспользуйтесь командой /instructions', reply_markup=None)
                if city == 'amster':
                    await give_vpn_amster(callback.from_user.id, until_date)
                if city == 'moscow':
                    await give_vpn_moscow(callback.from_user.id, until_date)
            elif info[6] == 'Extend':
                if city == 'amster':
                    last_date = datetime.datetime.strptime(db.get_date_amster(info[7]), '%d.%m.%Y')
                    until_date = Methods.get_datetime(duration, last_date)
                    db.extend_vpn_amster(info[7], until_date)
                    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                                text=f'Счёт оплачен, VPN активен до {until_date}', reply_markup=None)
                if city == 'moscow':
                    last_date = datetime.datetime.strptime(db.get_date_moscow(info[7]), '%d.%m.%Y')
                    until_date = Methods.get_datetime(duration, last_date)
                    db.extend_vpn_moscow(info[7], until_date)
                    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                                text=f'Счёт оплачен, VPN активен до {until_date}', reply_markup=None)
            await bot.send_message(Config.ADMIN_ID, f'Счёт QIWI оплачен:\n{info}')
        else:
            await bot.answer_callback_query(callback_query_id=callback.id, show_alert=False,
                                            text='Счёт не оплачен')
    else:
        await bot.send_message(callback.from_user.id, 'Счет не найден')


@dp.callback_query_handler(text='usdt')
async def usdt_create_bill(callback: types.CallbackQuery):
    period = db.get_last_pay_period(callback.from_user.id)
    city = db.get_last_city(callback.from_user.id)
    bill_type = db.get_last_type(callback.from_user.id)
    summ = Methods.get_usd_cb(Methods.get_price_period(period))
    bill_id = Usdt_payment.create_payment(callback.from_user.id)
    if bill_type == 'New':
        db.add_bill_usdt(callback.from_user.id, summ, bill_id, period, city, bill_type)
        await bot.send_message(Config.ADMIN_ID, f'Создан новый счёт USDT:\n'
                                                f'{callback.from_user.id}, {summ}, {bill_id}, {period}, {city}, '
                                                f'{bill_type}')
    elif bill_type == 'Extend':
        extend_num = db.get_extend_num(callback.from_user.id)
        db.add_bill_usdt(callback.from_user.id, summ, bill_id, period, city, bill_type, extend_num)
        await bot.send_message(Config.ADMIN_ID, f'Создан новый счёт USDT:\n'
                                                f'{callback.from_user.id}, {summ}, {bill_id}, {period}, {city}, '
                                                f'{bill_type}')
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, f'Вам нужно отправить ровно {summ} USDT на наш счет в сети trc-20 '
                                                  f'(TRON):')
    await bot.send_message(callback.from_user.id, f'{Config.USDT_ADRESS}')
    await bot.send_message(callback.from_user.id, 'Пожалуйста, убедитесь что отправляете точно указанную сумму по правильному '
                                                  'адресу!'
                                                  '\nПосле того, как перевод будет выполнен, скопируйте hash транзакции, '
                                                  'нажмите кнопку "Ввести hash", и пришлите его в ответ боту',
                           reply_markup=Markups.read_hash_usdt(bill_id))


@dp.callback_query_handler(text_contains='read_hash_')
async def check_status(callback: types.CallbackQuery, state: FSMContext):
    bill_id = str(callback.data[10:])
    info = db.get_bill_usdt(bill_id)
    if info != False:
        await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id)
        await state.update_data(bill_id=bill_id)
        await Form.hash.set()
        await bot.send_message(callback.from_user.id, 'Отправьте мне hash транзакции, чтобы я мог проверить оплату.'
                                                      '\nПример как выглядит hash транзакции:'
                                                      '\n\n1465f7234e12f31943efe7a4bfc1bc9e8ab9d66c644d53fece35c423c65ec1cb')
    else:
        await bot.send_message(callback.from_user.id, 'Счет не найден')


@dp.message_handler(state=Form.hash)
async def process_hash(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hash'] = message.text
    await state.finish()
    db.add_hash_to_bill_usdt(data['hash'], data['bill_id'])
    await bot.send_message(message.from_user.id, f'Вы ввели hash:\n\n{data["hash"]}',
                           reply_markup=Markups.check_usdt_status(data['bill_id'], data['hash']))


@dp.callback_query_handler(text_contains='usdt_status_')
async def check_status_usdt(callback: types.CallbackQuery):
    bill_id = str(callback.data[12:])
    info = db.get_bill_usdt(bill_id)
    if info != False:
        money = info[1]
        _hash = info[3]
        answer = Usdt_payment.check_payment(money, _hash)
        if db.check_hash_usdt(_hash):
            if answer == 'transaction not found':
                await bot.answer_callback_query(callback_query_id=callback.id, show_alert=False,
                                                text='Транзакций по указанному вами hash не найдено.')
            elif answer == 'wrong coin':
                await bot.answer_callback_query(callback_query_id=callback.id, show_alert=False,
                                                text='Монета не USDT')
            elif answer == 'invalid recipient address':
                await bot.answer_callback_query(callback_query_id=callback.id, show_alert=False,
                                                text=f'Неправильный кошелёк получателя')
            elif answer == 'wrong value':
                await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id)
                await bot.send_message(callback.from_user.id, f'По указанной транзакции на кошелёк получателя '
                                                              f'поступило неправильное количество USDT. Необходимо '
                                                              f'отправить {money} USDT.\nПри незначительной ошибке, '
                                                              f'напишите аккаунту, указанному в описании бота')
            elif answer == 'transaction is not confirmed yet, pls wait':
                await bot.answer_callback_query(callback_query_id=callback.id, show_alert=False,
                                                text='Ждём достаточное кол-во подтверждений')
            elif answer == 'status: confirmed, transaction done':
                user_money = db.user_money(callback.from_user.id)
                money_paid = Methods.get_rub_cb(money)
                db.set_money(callback.from_user.id, user_money + money_paid)
                db.usdt_bill_paid(bill_id, _hash)
                duration = info[5]
                city = info[6]
                if info[7] == 'New':
                    now_date = datetime.datetime.now()
                    until_date = Methods.get_datetime(duration, now_date)
                    await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id)
                    await bot.send_message(callback.from_user.id,
                                           'Счёт оплачен, бот создал Вам личный VPN\nДля помощи в '
                                           'установке воспользуйтесь командой /instructions')
                    if city == 'amster':
                        await give_vpn_amster(callback.from_user.id, until_date)
                    if city == 'moscow':
                        await give_vpn_moscow(callback.from_user.id, until_date)
                elif info[7] == 'Extend':
                    if city == 'amster':
                        last_date = datetime.datetime.strptime(db.get_date_amster(info[8]), '%d.%m.%Y')
                        until_date = Methods.get_datetime(duration, last_date)
                        db.extend_vpn_amster(info[8], until_date)
                        await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id)
                        await bot.send_message(callback.message.message_id, f'Счёт оплачен, VPN активен до '
                                                                            f'{until_date}')
                    if city == 'moscow':
                        last_date = datetime.datetime.strptime(db.get_date_moscow(info[8]), '%d.%m.%Y')
                        until_date = Methods.get_datetime(duration, last_date)
                        db.extend_vpn_moscow(info[8], until_date)
                        await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id)
                        await bot.send_message(callback.message.message_id, f'Счёт оплачен, VPN активен до '
                                                                            f'{until_date}')
                await bot.send_message(Config.ADMIN_ID, f'Счёт USDT оплачен:\n{info}')
            else:
                await bot.send_message(callback.from_user.id,
                                       'Произошла ошибка, пожалуйста напишите аккаунту, указанному '
                                       'в описании бота')
        else:
            await bot.answer_callback_query(callback_query_id=callback.id, show_alert=False,
                                            text='Указанный hash уже был использован для создания VPN')
    else:
        await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id)
        await bot.send_message(callback.from_user.id, 'Счет не найден')


@dp.callback_query_handler(text_contains='amster_')
async def extend_amster(callback: types.CallbackQuery):
    extend_num = int(callback.data[7:])
    db.last_city(callback.from_user.id, 'amster')
    db.last_type(callback.from_user.id, 'Extend')
    db.extend_num(callback.from_user.id, extend_num)
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, Messages.choose_period, reply_markup=Markups.period_button('Extend'))


@dp.callback_query_handler(text_contains='moscow_')
async def extend_moscow(callback: types.CallbackQuery):
    extend_num = int(callback.data[7:])
    db.last_city(callback.from_user.id, 'moscow')
    db.last_type(callback.from_user.id, 'Extend')
    db.extend_num(callback.from_user.id, extend_num)
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, Messages.choose_period, reply_markup=Markups.period_button('Extend'))


async def warn_and_clear():
    try:
        now_date = datetime.datetime.now()
        date_minus_3d = Methods.days_before_3(now_date)
        db.delete_qiwi_np_bills(date_minus_3d)
        db.delete_usdt_np_bills(date_minus_3d)
        date_plus_3d = Methods.days_after_3(now_date)
        str_now_date = now_date.strftime('%d.%m.%Y')
        amster_list = list(db.active_vpn_amster())
        moscow_list = list(db.active_vpn_moscow())
        for i in amster_list:
            if i[2] == date_plus_3d:
                await bot.send_message(i[1], 'Оплата VPN Амстердам заканчивается через 3 дня.')
                await bot.send_message(Config.ADMIN_ID, f'Пользователь {i[1]} осталось 3 дня Амстердам {i[0]}')
            if i[2] == str_now_date:
                await bot.send_message(i[1], 'Оплата VPN Амстердам заканчивается сегодня, если Вы не продлите доступ, то '
                                       'Ваш туннель будет исключён с удаленного сервера.'
                                       '\nДля продления воспользуйтесь командой /extend')
                await bot.send_message(Config.ADMIN_ID, f'Пользователь {i[1]} последний день Амстердам{i[0]}')
        for i in moscow_list:
            if i[2] == date_plus_3d:
                await bot.send_message(i[1], 'Оплата VPN Москва заканчивается через 3 дня.')
                await bot.send_message(Config.ADMIN_ID, f'Пользователь {i[1]} осталось 3 дня Москва {i[0]}')
            if i[2] == str_now_date:
                await bot.send_message(i[1], 'Оплата VPN Москва заканчивается сегодня, если Вы не продлите доступ, то '
                                       'Ваш туннель будет исключён с удаленного сервера.'
                                       '\nДля продления воспользуйтесь командой /extend')
                await bot.send_message(Config.ADMIN_ID, f'Пользователь {i[1]} последний день Москва{i[0]}')
    except Exception as e:
        print(e)


async def tell_admin():
    str_now_date = datetime.datetime.now().strftime('%d.%m.%Y')
    amster_list = list(db.active_vpn_amster())
    moscow_list = list(db.active_vpn_moscow())
    for i in amster_list:
        if i[2] == str_now_date:
            db.turn_off_amster(i[0])
            await bot.send_message(Config.ADMIN_ID, f'{i} Не оплатил, меняю статус и удаляем Амстердам {i[0]}')
    for i in moscow_list:
        if i[2] == str_now_date:
            db.turn_off_moscow(i[0])
            await bot.send_message(Config.ADMIN_ID, f'{i} Не оплатил, меняю статус и удаляем Москва {i[0]}')


async def scheduler():
    aioschedule.every().day.at('18:00').do(warn_and_clear)
    aioschedule.every().day.at('22:00').do(tell_admin)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
