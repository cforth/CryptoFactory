#!/usr/bin/env python
# -*- coding: utf-8 -*-
from CryptoFactory.CFCrypto import *
import os
import filecmp
import unittest
import shutil


class TestCrypto(unittest.TestCase):
    def test_StringCrypto(self):
        my_cipher = StringCrypto('this is password')
        string = 'this is a secret!!! 这是一个秘密！！！'
        encrypt_str = my_cipher.encrypt(string)
        decrypt_str = my_cipher.decrypt(encrypt_str)
        self.assertEqual(string, decrypt_str)

    def test_FileCrypto(self):
        # 使用AES加密解密的演示
        my_aes = FileCrypto('this is very long password to test file crypto')
        my_aes.encrypt('./testdata/test.jpg', './testdata/test.jpg.aes')
        my_aes.decrypt('./testdata/test.jpg.aes', './testdata/aes_test.jpg')
        self.assertTrue(filecmp.cmp('./testdata/test.jpg', './testdata/aes_test.jpg'))
        os.remove('./testdata/aes_test.jpg')
        os.remove('./testdata/test.jpg.aes')
        my_aes.encrypt('./testdata/test.mp3', './testdata/test.mp3.aes')
        my_aes.decrypt('./testdata/test.mp3.aes', './testdata/aes_test.mp3')
        self.assertTrue(filecmp.cmp('./testdata/test.mp3', './testdata/aes_test.mp3'))
        os.remove('./testdata/aes_test.mp3')
        os.remove('./testdata/test.mp3.aes')

    def test_DirCrypto(self):
        my_cipher = DirFileCrypto('crypto dir')
        my_cipher.encrypt('./testdata/testdir/', './testdata/en_dir/')
        my_cipher.decrypt('./testdata/en_dir/slV4TcFOc0AvAKmyEq0-hA==/', './testdata/de_dir/')
        my_cipher.encrypt('./testdata/testdir/', './testdata/en_dir2/', False)  # 测试不加密文件和文件夹名称
        my_cipher.decrypt('./testdata/en_dir2/testdir/', './testdata/de_dir2/', False)
        self.assertTrue(filecmp.cmp('./testdata/de_dir/testdir/test.mp3', './testdata/testdir/test.mp3'))
        self.assertTrue(filecmp.cmp('./testdata/de_dir/testdir/test.jpg', './testdata/testdir/test.jpg'))
        self.assertTrue(filecmp.cmp('./testdata/de_dir/testdir/测试中文目录名/test.txt', './testdata/testdir/测试中文目录名/test.txt'))
        self.assertTrue(filecmp.cmp('./testdata/de_dir/testdir/测试中文目录名/test/test.jpg', './testdata/testdir/测试中文目录名/test/test.jpg'))
        self.assertTrue(filecmp.cmp('./testdata/de_dir/testdir/测试中文目录名/test/test.jpg', './testdata/de_dir2/testdir/测试中文目录名/test/test.jpg'))
        shutil.rmtree('./testdata/en_dir')
        shutil.rmtree('./testdata/en_dir2')
        shutil.rmtree('./testdata/de_dir')
        shutil.rmtree('./testdata/de_dir2')

    def test_RSACrypto(self):
        # 使用RSA加密解密的演示
        my_rsa = RSACrypto()
        # 如果首次加密，本地没有私钥文件和公钥文件，则需要生成
        my_rsa.set_password('helloRSA')
        my_rsa.set_public_key_path('./testdata/my_rsa.pub')
        my_rsa.set_private_key_path('./testdata/my_rsa')
        my_rsa.generate_key()
        # 使用RSA加密需要用到公钥文件
        my_rsa.set_public_key_path('./testdata/my_rsa.pub')
        my_rsa.encrypt('./testdata/test.jpg', './testdata/test.bin')
        # 使用RSA解密需要用到私钥密码和私钥文件
        my_rsa.set_password('helloRSA')
        my_rsa.set_private_key_path('./testdata/my_rsa')
        my_rsa.decrypt('./testdata/test.bin', './testdata/output.jpg')
        self.assertTrue(filecmp.cmp('./testdata/test.jpg', './testdata/output.jpg'))
        os.remove('./testdata/output.jpg')
        os.remove('./testdata/test.bin')
        os.remove('./testdata/my_rsa.pub')
        os.remove('./testdata/my_rsa')

    def test_DirNameCrypto(self):
        # 复制原测试文件夹
        a_dir_path = os.path.abspath('./testdata')
        b_dir_path = os.path.abspath('./testdata_copy/')
        shutil.copytree(a_dir_path, b_dir_path)
        my_cipher = DirNameCrypto('crypto dir', './dir_name.json')
        my_cipher.encrypt(a_dir_path)
        my_cipher.decrypt(a_dir_path)
        # 保存两个测试文件夹里的目录与文件名称
        a_dir_list = []
        b_dir_list = []
        a_index = len(a_dir_path)
        b_index = len(b_dir_path)
        for path, subdir, files in os.walk(a_dir_path, topdown=False):
            for d in subdir:
                a_dir_list.append(os.path.join(os.path.abspath(path)[a_index:], d))
            for f in files:
                a_dir_list.append(os.path.join(os.path.abspath(path)[a_index:], f))

        for path, subdir, files in os.walk(b_dir_path, topdown=False):
            for d in subdir:
                b_dir_list.append(os.path.join(os.path.abspath(path)[b_index:], d))
            for f in files:
                b_dir_list.append(os.path.join(os.path.abspath(path)[b_index:], f))

        a_dir_list.sort()
        b_dir_list.sort()
        self.assertEqual(a_dir_list, b_dir_list)
        os.remove('./dir_name.json')
        shutil.rmtree(b_dir_path)


if __name__ == '__main__':
    unittest.main()
