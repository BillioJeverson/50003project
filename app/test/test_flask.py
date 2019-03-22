import unittest
from app import app
from app.forms import LoginForm


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    # 1 Ensure that Flask was set up correctly
    def test_app_working(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # 2 Ensure that app redirects ticket if not logged in
    def test_anon_ticket(self):
        tester = app.test_client(self)
        response = tester.get('/ticket', content_type='html/text')
        self.assertEqual(response.status_code, 302)

    # 3 Ensure that app redirects index if not logged in
    def test_anon_index(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertEqual(response.status_code, 302)

    # 4 Ensure that app redirects home if not logged in
    def test_anon_home(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 302)

    # 5 Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login')
        self.assertIn(b'<title>Login Page</title>', response.data)

    # 6 Ensure app can login with correct credentials
    def test_wrong_username_login(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'<title>Home Page</title>', response.data)

    # 7 Ensure app redirects back to login page with wrong username
    def test_wrong_password_login(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="wrongadmin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'<title>Login Page</title>', response.data)

    # 8 Ensure app redirects back to login page with wrong password
    def test_correct_login(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="admin", password="wrongadmin"),
            follow_redirects=True
        )
        self.assertIn(b'<title>Login Page</title>', response.data)

    # 9 Ensure app can register new user
    def test_register_user(self):
        tester = app.test_client()
        response = tester.post(
            '/register',
            data=dict(email="testing@testing.com", username="testing", password="testing",password2="testing"),
            follow_redirects=True
        )
        self.assertIn(b'<title>Login Page</title>', response.data)

    # 10 Ensure app does not register already registered user
    def test_existing_user(self):
        tester = app.test_client()
        response = tester.post(
            '/register',
            data=dict(email="admin@example.com", username="admin", password="admin", password2="admin"),
            follow_redirects=True
        )
        self.assertIn(b'[Please use a different email address.]', response.data)

    # 11 Ensure register does not work if username is empty
    def test_empty_register1(self):
        tester = app.test_client()
        response = tester.post(
            '/register',
            data=dict(email="something@example.com", username="", password="admin", password2="admin"),
            follow_redirects=True
        )
        self.assertIn(b'[This field is required.]', response.data)

    # 12 Ensure app does not work if password is empty
    def test_empty_register2(self):
        tester = app.test_client()
        response = tester.post(
            '/register',
            data=dict(email="something@example.com", username="usertest", password="", password2="admin"),
            follow_redirects=True
        )
        self.assertIn(b'[This field is required.]', response.data)

    # 13 Ensure app does not work if password2 is empty
    def test_empty_register3(self):
        tester = app.test_client()
        response = tester.post(
            '/register',
            data=dict(email="something@example.com", username="usertest", password="admin", password2=""),
            follow_redirects=True
        )
        self.assertIn(b'[This field is required.]', response.data)

    # 14 Ensure app does not work if email is empty
    def test_empty_register4(self):
        tester = app.test_client()
        response = tester.post(
            '/register',
            data=dict(email="", username="usertest", password="admin", password2="admin"),
            follow_redirects=True
        )
        self.assertIn(b'[This field is required.]', response.data)

    # 15 Ensure email is valid when registering
    def test_invalid_email(self):
        tester = app.test_client()
        response = tester.post(
            '/register',
            data=dict(email="itssomething", username="usertest", password="admin", password2="admin"),
            follow_redirects=True
        )
        self.assertIn(b'[Invalid email address.]', response.data)

    #
    # # Ensure that logout page requires user login
    # def test_logout_route_requires_login(self):
    #     tester = app.test_client()
    #     response = tester.get('/logout', follow_redirects=True)
    #     self.assertIn(b'You need to login first.', response.data)

    # Ensure login behaves correctly with incorrect credentials
    # def test_incorrect_login(self):
    #     tester = app.test_client()
    #     response = tester.post(
    #         '/login',
    #         data=dict(username="wrong", password="wrong"),
    #         follow_redirects=True
    #     )
    #     self.assertIn(b'Invalid Credentials. Please try again.', response.data)
    #
    # # Ensure logout behaves correctly
    # def test_logout(self):
    #     tester = app.test_client()
    #     tester.post(
    #         '/login',
    #         data=dict(username="admin", password="admin"),
    #         follow_redirects=True
    #     )
    #     response = tester.get('/logout', follow_redirects=True)
    #     self.assertIn(b'You were logged out', response.data)
    #
    # # Ensure that main page requires user login
    # def test_main_route_requires_login(self):
    #     tester = app.test_client()
    #     response = tester.get('/', follow_redirects=True)
    #     self.assertIn(b'You need to login first.', response.data)
    #
    #
    # # Ensure that posts show up on the main page
    # def test_posts_show_up_on_main_page(self):
    #     tester = app.test_client()
    #     response = tester.post(
    #         '/login',
    #         data=dict(username="admin", password="admin"),
    #         follow_redirects=True
    #     )
    #     self.assertIn(b'Hello from the shell', response.data)
    #

if __name__ == '__main__':
    unittest.main()
