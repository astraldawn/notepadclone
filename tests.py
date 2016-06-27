import os
import server
import unittest
import tempfile


class ServerTestCase(unittest.TestCase):
    def setUp(self):
        """Create a new test client, init a new DB"""
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        with server.app.app_context():
            server.init_db()

    def tearDown(self):
        """Deletes the DB after the test completes"""
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()
