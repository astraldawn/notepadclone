import os
import server
import unittest
import tempfile


class ServerTestCase(unittest.TestCase):
    """A more complex test suite - https://github.com/pallets/flask/tree/master/examples/minitwit/"""
    def setUp(self):
        """Create a new test client, init a new DB"""
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()

        """Disable error catching during request handling, better error reports
        when performing test requests against the application"""
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        with server.app.app_context():
            server.init_db()

    def tearDown(self):
        """Deletes the DB after the test completes"""
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])

    def test_empty_db(self):
        """Assert that an empty database is empty"""
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def login(self, username, password):
        """Need to follow redirects (behaviour of login page)"""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Need to follow redirects (behaviour of logout page)"""
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        """Valid credentials should work, invalid credentials should not"""
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        """Check that posting a message works"""
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data


if __name__ == '__main__':
    unittest.main()
