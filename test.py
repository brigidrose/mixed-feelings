import server
import unittest

class MyAppIntegrationTestCase(unittest.TestCase):

    def test_index(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn('<h1>Jumbotron</h1>', result.data)

    def test_login_form(self):
        client = server.app.test_client()
        result = client.get('/login')
        self.assertIn('<h1>Login</h1>', result.data)

    def test_registration_form(self):
        client = server.app.test_client()
        result = client.get('/register')
        self.assertIn('<h1>Register</h1>', result.data)
    
    def test_about(self):
        client = server.app.test_client()
        result = client.get('/about')
        self.assertIn('<div id="about-text">', result.data)

        #this one is failing. Check the route. That is probably the issue.
    def test_user_page(self):
        client = server.app.test_client()
        result = client.get('/user/<user_id>')
        self.assertIn('<h4>{{result.keywords}}</h4>', result.data)





if __name__ == '__main__':
    unittest.main()
