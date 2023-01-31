import sqlite3
import datetime


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE User_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, username, join_date):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' (User_id, Username, Join_date) VALUES (?, ?, ?)",
                                       (user_id, username, join_date,))

    def user_money(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT Money_paid FROM 'users' WHERE User_id = ?", (user_id,)).fetchone()
            return int(result[0])

    def set_money(self, user_id, money):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET Money_paid = ? WHERE User_id = ?", (money, user_id,))

    def last_city(self, user_id, last_city):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET last_city = ? WHERE User_id = ?", (last_city, user_id,))

    def last_pay_period(self, user_id, last_pay_period):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET last_pay_period = ? WHERE User_id = ?",
                                       (last_pay_period, user_id,))

    def last_type(self, user_id, last_type):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET last_type = ? WHERE User_id = ?",
                                       (last_type, user_id,))

    def extend_num(self, user_id, extend_num):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET Extend_num = ? WHERE User_id = ?",
                                       (extend_num, user_id,))

    def get_last_city(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT last_city FROM 'users' WHERE User_id = ?", (user_id,)).fetchone()[0]

    def get_last_pay_period(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT last_pay_period FROM 'users' WHERE User_id = ?", (user_id,)).fetchone()[0]

    def get_last_type(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT last_type FROM 'users' WHERE User_id = ?", (user_id,)).fetchone()[0]

    def get_extend_num(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT Extend_num FROM 'users' WHERE User_id = ?", (user_id,)).fetchone()[0]

    def give_vpn_amster(self, user_id, valid_untill):
        with self.connection:
            number = self.cursor.execute("SELECT Number FROM 'vpn_list_amster' WHERE In_use = ?", ('No',)).fetchone()
            self.cursor.execute("UPDATE 'vpn_list_amster' SET In_use = ?, User_id = ?, Valid_untill = ? WHERE "
                                "Number = ?", ('Yes', user_id, valid_untill, number[0],))
            return number[0]

    def give_vpn_moscow(self, user_id, valid_untill):
        with self.connection:
            number = self.cursor.execute("SELECT Number FROM 'vpn_list_moscow' WHERE In_use = ?", ('No',)).fetchone()
            self.cursor.execute("UPDATE 'vpn_list_moscow' SET In_use = ?, User_id = ?, Valid_untill = ? WHERE "
                                "Number = ?", ('Yes', user_id, valid_untill, number[0],))
            return number[0]

    def get_date_amster(self, number):
        with self.connection:
            return self.cursor.execute("SELECT Valid_untill FROM 'vpn_list_amster' WHERE Number = ?", (number,)).fetchone()[0]

    def get_date_moscow(self, number):
        with self.connection:
            return self.cursor.execute("SELECT Valid_untill FROM 'vpn_list_moscow' WHERE Number = ?", (number,)).fetchone()[0]

    def extend_vpn_amster(self, number, new_date):
        with self.connection:
            return self.cursor.execute("UPDATE 'vpn_list_amster' SET Valid_untill = ? WHERE Number = ?",
                                       (new_date, number,))

    def extend_vpn_moscow(self, number, new_date):
        with self.connection:
            return self.cursor.execute("UPDATE 'vpn_list_moscow' SET Valid_untill = ? WHERE Number = ?",
                                       (new_date, number,))

    def check_active_vpn_amster(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT Number, Valid_untill FROM 'vpn_list_amster' WHERE (User_id, In_use) "
                                       "= (?, ?)", (user_id, 'Yes',)).fetchall()

    def check_active_vpn_moscow(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT Number, Valid_untill FROM 'vpn_list_moscow' WHERE (User_id, In_use) "
                                       "= (?, ?)", (user_id, 'Yes',)).fetchall()

    def add_bill_qiwi(self, user_id, money, bill_id, comment, duration, city, bill_type, extend_num=None):
        with self.connection:
            now_date = datetime.datetime.now().strftime('%d.%m.%Y')
            return self.cursor.execute(f"INSERT INTO 'qiwi_payment' (User_id, Money, Bill_id, Comment, Duration, City, "
                                       f"Bill_type, Extend_num, Date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                       (user_id, money, bill_id, comment, duration, city, bill_type, extend_num, now_date,))

    def get_bill_qiwi(self, bill_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'qiwi_payment' WHERE Bill_id = ?", (bill_id,)).fetchone()
            if result is None:
                return False
            return result

    def qiwi_bill_paid(self, bill_id):
        with self.connection:
            return self.cursor.execute("UPDATE 'qiwi_payment' SET Status = ? WHERE Bill_id = ?", ('Paid', bill_id,))

    def add_bill_usdt(self, user_id, money, bill_id, duration, city, bill_type, extend_num=None):
        with self.connection:
            now_date = datetime.datetime.now().strftime('%d.%m.%Y')
            return self.cursor.execute(f"INSERT INTO 'usdt_payment' (User_id, Money, Bill_id, Duration, City, "
                                       f"Bill_type, Extend_num, Date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                       (user_id, money, bill_id, duration, city, bill_type, extend_num, now_date,))

    def get_bill_usdt(self, bill_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'usdt_payment' WHERE Bill_id = ?", (bill_id,)).fetchone()
            if result is None:
                return False
            return result

    def add_hash_to_bill_usdt(self, _hash, bill_id):
        with self.connection:
            return self.cursor.execute("UPDATE 'usdt_payment' SET Hash = ? WHERE Bill_id = ?", (_hash, bill_id,))

    def check_hash_usdt(self, _hash):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'usdt_payment' WHERE (Hash, Hash_used) = (?, ?)",
                                         (_hash, 'Yes')).fetchone()
            if result is None:
                return True
            else:
                return False

    def usdt_bill_paid(self, bill_id, _hash):
        with self.connection:
            return self.cursor.execute("UPDATE 'usdt_payment' SET (Status, Hash, Hash_used) = (?, ?, ?) WHERE "
                                       "Bill_id = ?", ('Paid', _hash, 'Yes', bill_id,))

    def active_vpn_amster(self):
        with self.connection:
            return self.cursor.execute("SELECT Number, User_id, Valid_untill FROM 'vpn_list_amster' "
                                       "WHERE In_use = ?", ('Yes',)).fetchall()

    def active_vpn_moscow(self):
        with self.connection:
            return self.cursor.execute("SELECT Number, User_id, Valid_untill FROM 'vpn_list_moscow' "
                                       "WHERE In_use = ?", ('Yes',)).fetchall()

    def delete_qiwi_np_bills(self, date):
        with self.connection:
            self.cursor.execute("DELETE FROM 'qiwi_payment' WHERE (Date, Status) = (?, ?)", (date, 'Not paid'))
            return True

    def delete_usdt_np_bills(self, date):
        with self.connection:
            self.cursor.execute("DELETE FROM 'usdt_payment' WHERE (Date, Status) = (?, ?)", (date, 'Not paid'))
            return True

    def turn_off_amster(self, number):
        with self.connection:
            self.cursor.execute("UPDATE 'vpn_list_amster' SET In_use = ? WHERE Number = ?", ('Expired', number,))
            return True

    def turn_off_moscow(self, number):
        with self.connection:
            self.cursor.execute("UPDATE 'vpn_list_moscow' SET In_use = ? WHERE Number = ?", ('Expired', number,))
            return True
