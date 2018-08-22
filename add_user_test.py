import unittest

class AddUserTest(unittest.TestCase):
    def runTest(self):
        userid = "123456" # Alice Tan
        attributes = {"gender" : "female", "age" : 25}
        cs = CloudServerMock()
        addUser = AddUserUseCase()
        addUser.run(userid, attributes)
        self.assertIn(userid, cs.getProxyKeyStore())
        self.assertEqual("273c1ff060399a9059558ff7e8d75876e36836d6", cs.getProxyKey(userid))

class AddUserUseCase():
    def __init__(self):
        pass

    def run(self, userid, attributes):
        pass

class CloudServerMock():

    def getProxyKeyStore(self):
        return {'123456': '273c1ff060399a9059558ff7e8d75876e36836d6'}

    def getProxyKey(self, userid):
        return '273c1ff060399a9059558ff7e8d75876e36836d6'

if __name__ == '__main__':
    unittest.main()
