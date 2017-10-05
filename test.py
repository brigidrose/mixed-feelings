import server
import unittest

class MyAppIntegrationTestCase(unittest.TestCase):

    def test_index(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn(' <title> Mixed Feelings </title>', result.data)

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
        result = client.get('/user')
        self.assertIn('Saved Feels', result.data)

    def test_feelings_form(self):
        client = server.app.test_client()
        result = client.get('/feelings')
        self.assertIn('<h1>How are you feeling?</h1>', result.data)

    def test_map(self):
        client = server.app.test_client()
        result = client.get('/global_feelings')
        self.assertIn('<div id="feelings-heatmap"></div>', result.data)










if __name__ == '__main__':
    unittest.main()
