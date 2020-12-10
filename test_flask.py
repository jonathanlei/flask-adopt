from unittest import TestCase

from app import app
from models import db, User, Post

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
        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestUser", last_name="TestLast", image_url='')
        db.session.add(user)
        db.session.flush()
        #print()
        post = Post(title="TestTitle", content="TestContent", user_id=user.id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id
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
    
    def test_user_info_page(self):
        """ Test that individual user information
        and their posts are showing"""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser TestLast', html)
            self.assertIn('id="user-info"', html)
            self.assertIn("TestTitle", html)

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
    

class PostsViewTestCase(TestCase):
    """Tests for views for posts."""

    def setUp(self):
        """Add a sample user"""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="TestUser", last_name="TestLast", image_url='')
        db.session.add(user)
        db.session.flush()
        #print()
        post = Post(title="TestTitle", content="TestContent", user_id=user.id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id
        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_post_info_page(self):
        """ Test that title, content and author appears on the post info page"""

        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('id="post-info"', html)
            self.assertIn("TestTitle", html)
            self.assertIn("TestContent", html)
            self.assertIn("By TestUser TestLast", html)
    
    def test_post_add(self):
        """ Test that a new post is successfully added to data base
            on /users/user_id/posts/new route with POST method
        """

        with app.test_client() as client:
            d = {"title": "Chicken",
                 "content": "Little",
                 "user_id": self.user_id}
            resp = client.post(f"/users/{self.user_id}/posts/new",
                               data=d,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('id="user-info"', html)
            self.assertIn('Chicken', html)
            # test empty submission, and redirect back to form
            d = {"title": "",
                 "content": "Little",
                 "user_id": self.user_id}
            resp = client.post(f"/users/{self.user_id}/posts/new",
                               data=d,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Please fill out all fields", html)
            self.assertIn('id="new-post"', html)

    def test_post_edit(self):
        """ Test that edited post title and contents appears on post info page"""

        with app.test_client() as client:
            d = {"title": "Chicken",
                 "content": "Little",
                 "user_id": self.user_id}
            resp = client.post(f"/posts/{self.post_id}/edit",
                               data=d,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Chicken", html)
            self.assertIn("Little", html)
            self.assertIn("By TestUser TestLast", html)
            self.assertIn('id="post-info"', html)
            # test empty submission, and redirect back to form
            d = {"title": "",
                 "content": "Little",
                 "user_id": self.user_id}
            resp = client.post(f"/posts/{self.post_id}/edit",
                               data=d,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Please fill out all fields", html)
            self.assertIn('id="edit-post"', html)
    
    def test_post_delete(self):
        """ Test that post title does not appear on user info page after redirect"""

        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete",
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('id="user-info"', html)
            self.assertNotIn("TestTitle", html)



