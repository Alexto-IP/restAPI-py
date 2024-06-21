import sqlite3


class SQLigther:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.is_processing = False

    def get_all_items_id(self):
        """Получаем id всех продуктов"""
        with self.connection:
            return self.cursor.execute('SELECT `item_id` FROM `warehouse`').fetchall()

    def get_item_name(self, item_id):
        """Получаем название продукта по id"""
        with self.connection:
            return self.cursor.execute('SELECT `item_name` FROM `warehouse` WHERE `item_id` = ?', (item_id,)).fetchone()[0]

    def get_item_type(self, item_id):
        """Получаем категорию продукта по id"""
        with self.connection:
            return self.cursor.execute('SELECT `item_type` FROM `warehouse` WHERE `item_id` = ?', (item_id,)).fetchone()[0]

    def get_item_price(self, item_id):
        """Получаем цену продукта по id"""
        with self.connection:
            return self.cursor.execute('SELECT `item_price` FROM `warehouse` WHERE `item_id` = ?', (item_id,)).fetchone()[0]

    def get_item_count(self, item_id):
        """Получаем количество продукта по id"""
        with self.connection:
            return self.cursor.execute('SELECT `item_count` FROM `warehouse` WHERE `item_id` = ?', (item_id,)).fetchone()[0]

    def get_items_id_by_type(self, item_type):
        """Получаем id продуктов одной категории"""
        with self.connection:
            return self.cursor.execute('SELECT `item_id` FROM `warehouse` WHERE `item_type` = ?', (item_type,)).fetchall()

    def delete_item(self, item_id):
        """Удаляем продукт по id"""
        with self.connection:
            self.cursor.execute('DELETE FROM `warehouse` WHERE `item_id` = ?', (item_id,))

    def add_item(self, item_id, item_name, item_type, item_count, item_price):
        """Добавление продукта"""
        with self.connection:
            self.cursor.execute('INSERT INTO `warehouse` (`item_id`, `item_name`, `item_type`, `item_count`, `item_price`) '
                                'VALUES(?,?,?,?,?)', (item_id, item_name, item_type, item_count, item_price,))

    def update_item_info(self, item_id, item_name, item_type, item_count, item_price):
        """Обновление информации о продукте"""
        with self.connection:
            self.cursor.execute('UPDATE `warehouse` SET `item_name` = ?, item_type = ?, item_count = ?, item_price = ? '
                                'WHERE `item_id` = ?', (item_name, item_type, item_count, item_price, item_id,))
