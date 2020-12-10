from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly-test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UsersViewTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add a sample user"""

        User.query.delete()

        user = User(first_name="TestUser", last_name="TestLast", image_url='')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users_page(self):
        """ Test that users are shown on /users route """

        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)
            self.assertIn('id="users-list"', html)

    def test_user_add(self):
        """ Test that a new user is successfully added to data base
            on /users/new route with POST method
        """

        with app.test_client() as client:
            d = {"first_name": "Lucas", "last_name": "Paga", "image_url": ""}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Lucas", html)
            self.assertIn('id="users-list"', html)

    def test_user_edit(self):
        """ Test that user edit to their info appears on user info page after redirect """

        with app.test_client() as client:
            d = {"first_name": "Jonathan",
                 "last_name": "Pagac",
                 "image_url": ""}
            resp = client.post(f"/users/{self.user_id}/edit",
                               data=d,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Jonathan", html)
            self.assertIn("Pagac", html)
            self.assertIn('id="user-info"', html)

    def test_user_delete(self):
        """ Test that user info does not appear on users page after redirect """

        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete",
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("TestUser", html)
