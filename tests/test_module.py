import unittest
# from application import app


class BasicTestCase(unittest.TestCase):

    def test_logout(self):
        pass

    #     self.app = app.test_client()
    #     ans =self.app.get('/logout')
    #     self.assertEqual(ans.status_code, 200)

    # def test_home(self):
    #     self.app = app.test_client()
    #     ans =self.app.get('/home')
    #     self.assertEqual(ans.status_code, 302)

    # def test_login(self):
    #     self.app = app.test_client()
    #     ans =self.app.get('/login')
    #     self.assertEqual(ans.status_code, 200)

    # def test_register(self):
    #     self.app = app.test_client()
    #     ans =self.app.get('/register')
    #     self.assertEqual(ans.status_code, 200)

    # def test_dashboard(self):
    #     self.app = app.test_client()
    #     ans =self.app.get('/dashboard')
    #     self.assertEqual(ans.status_code, 200)

    # def test_friends(self):
    #     self.app= app.test_client()
    #     ans=self.app.get('/friends')
    #     self.assertEqual(ans.status_code, 200)

    # def test_calories(self):
    #     self.app= app.test_client()
    #     ans=self.app.get('/calories')
    #     self.assertEqual(ans.status_code, 302)
    pass


if __name__ == '__main__':
    unittest.main()
