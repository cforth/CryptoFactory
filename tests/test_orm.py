import unittest
from CryptoFactory.ORM import *


class User(Model):
    # 定义类的属性到列的映射：
    id = IntegerField('id', primary_key=True)
    username = StringField('username')
    email = StringField('email')
    password = StringField('password')


class CryptoUser(Model):
    # 定义类的属性到列的映射：
    id = IntegerField('id', primary_key=True)
    username = StringField('username')
    email = StringField('email')
    password = StringField('password')


class TestORM(unittest.TestCase):
    def test_new_table(self):
        # 新建数据库和数据表
        if not User.has_table():
            User.new_table()
        self.assertTrue(User.has_table())
        User.delete_table()
        self.assertFalse(User.has_table())

    def test_operate(self):
        if not User.has_table():
            User.new_table()
        self.assertFalse(User.has_item("username", 'xiaoming'))

        u = User(id=1, username='xiaoming', email='xiaoming@gmail.com', password='hello')
        if not User.has_item("id", u.id):
            u.save()
        self.assertTrue(User.has_item("username", 'xiaoming'))

        u_list = [User(id=2, username='xxx', email='xxx@gmail.com', password='world'),
                  User(id=3, username='yyy', email='yyy@gmail.com', password='sdgfdg'),
                  User(id=4, username='xxx', email='xxx2@gmail.com', password='world2')]
        User.insert_batch(u_list)

        find_result = User.find_all("username", "xxx")
        self.assertEqual(len(find_result), 2)

        remove_result = User.remove_all('username', "xxx")
        find_result = User.find_all("username", "xxx")
        self.assertEqual(remove_result, 2)
        self.assertFalse(find_result)

        User.delete_table()
        self.assertFalse(User.has_table())
        os.remove("User.db")


if __name__ == '__main__':
    unittest.main()
