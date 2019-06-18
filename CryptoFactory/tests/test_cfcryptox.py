from CryptoFactory.CFCryptoX import *
import os
import filecmp
import unittest
import shutil


class TestCrypto(unittest.TestCase):
    def test_StringCrypto(self):
        original_string = 'this is a secret!!! 这是一个秘密！！！'
        my_cipher = StringCrypto('this is password')
        encrypt_str = my_cipher.encrypt(original_string)
        decrypt_str = my_cipher.decrypt(encrypt_str)
        self.assertEqual(original_string, decrypt_str)

    def test_ByteCrypto(self):
        my_cipher = ByteCrypto('this is very long password to test file crypto')
        with open('./testdata/test.png', 'rb') as f_from:
            encrypt_data = my_cipher.encrypt(f_from.read())
            with open('./testdata/test.png.aes', 'wb') as f_to:
                f_to.write(encrypt_data)

        with open('./testdata/test.png.aes', 'rb') as f_from:
            decrypt_data = my_cipher.decrypt(f_from.read())
            with open('./testdata/aes_test.png', 'wb') as f_to:
                f_to.write(decrypt_data)

        self.assertTrue(filecmp.cmp('./testdata/test.png', './testdata/aes_test.png'))
        os.remove('./testdata/aes_test.png')
        os.remove('./testdata/test.png.aes')

    def test_FileCrypto(self):
        my_cipher = FileCrypto('this is very long password to test file crypto')
        my_cipher.encrypt('./testdata/test.pdf', './testdata/test.pdf.aes')
        my_cipher.decrypt('./testdata/test.pdf.aes', './testdata/aes_test.pdf')
        self.assertTrue(filecmp.cmp('./testdata/test.pdf', './testdata/aes_test.pdf'))
        os.remove('./testdata/aes_test.pdf')
        os.remove('./testdata/test.pdf.aes')

    def test_BigFileCrypto(self):
        # 使用AES加密解密的演示
        password = 'this is very long password to test file crypto'
        my_cipher = FileCrypto(password)
        my_cipher.encrypt('./testdata/test.mp4', './testdata/test.mp4.aes')
        my_cipher.decrypt('./testdata/test.mp4.aes', './testdata/aes_test.mp4')
        self.assertTrue(filecmp.cmp('./testdata/test.mp4', './testdata/aes_test.mp4'))
        os.remove('./testdata/aes_test.mp4')
        # 测试错误的密码，验证头部标识不对后不会解密
        fail_cipher = FileCrypto("wrong password")
        fail_cipher.decrypt('./testdata/test.mp4.aes', './testdata/aes_test_wrong.mp4')
        os.remove('./testdata/test.mp4.aes')

    def test_DirCrypto(self):
        password = 'this is very long password to test file crypto'
        my_cipher = DirFileCrypto(password)
        my_cipher.encrypt('./testdata/testdir/', './testdata/')
        my_cipher.decrypt('./testdata/1186c9556ba1298a7e022d8493ac4601/', './testdata/testdecrytdir/')
        self.assertTrue(filecmp.cmp('./testdata/testdir/test.mp3', './testdata/testdecrytdir/testdir/test.mp3'))
        shutil.rmtree('./testdata/testdecrytdir')
        shutil.rmtree('./testdata/1186c9556ba1298a7e022d8493ac4601')
        os.remove('./testdata/1186c9556ba1298a7e022d8493ac4601.json')

    def test_ListCrypto(self):
        password = 'this is very long password to test file crypto'
        my_cipher = ListCrypto(password, "./list_test.json")
        my_cipher.encrypt(['./testdata/test.pdf', './testdata/testdir/', './testdata/test.png'], './testdata/testlist/')
        my_cipher.decrypt(['./testdata/testlist/1186c9556ba1298a7e022d8493ac4601/',
                           './testdata/testlist/51307180f8f2812085ee59422ca96cf0',
                           './testdata/testlist/ded5452dd4b0d7c2ba42e47d5d960fc9'],
                          './testdata/testdecrytlist/')
        self.assertTrue(filecmp.cmp('./testdata/testdir/test.mp3', './testdata/testdecrytlist/testdir/test.mp3'))
        shutil.rmtree('./testdata/testdecrytlist')
        shutil.rmtree('./testdata/testlist')
        os.remove('./list_test.json')


if __name__ == '__main__':
    unittest.main()
