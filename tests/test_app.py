import unittest
from db import db
from models.models import UserModel
from passlib.hash import pbkdf2_sha256
from app import create_app
from config import TestConfig

app = create_app(config_class=TestConfig)
app.config.from_object(TestConfig)
client = app.test_client()


class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        ctx = app.app_context()
        ctx.push()
        with client:
            password_hash = pbkdf2_sha256.hash("password")
            test_user = UserModel(name="John Doe",
                                  email="johndoe@email.com",
                                  password=password_hash)

            db.session.add(test_user)
            # db.session.add(test_feedback)
            db.create_all()
            db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    #### HELPER METHODS ####
    def login(self, email, password):
        with app.test_client() as c:
            return c.post('/login', data=dict(
                email=email,
                password=password
            ), follow_redirects=True)

    def register(self, name, email, password, confirm_password):
        return client.post("/register", data=dict(
            name=name,
            email=email,
            password=password,
            confirm_password=confirm_password
        ), follow_redirects=True)

    def feedback(self, rating, q1, q2, q3, q4, comments, user):
        return client.post("/feedback", data=dict(rating=rating,
                                                  question1=q1,
                                                  question2=q2,
                                                  question3=q3,
                                                  question4=q4,
                                                  comments=comments,
                                                  user_id=user),
                           follow_redirects=True)
    # #### END HELPER METHODS ####

    # ***** Tests for the home route *****
    def test_home_route(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Farm Fresh Produce", response.data)
        self.assertNotIn(b"Sign Out", response.data)

    # ***** Tests for the register route *****
    def test_register_route(self):
        response = client.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Sign Up", response.data)

    def test_register_with_new_user(self):
        response = self.register("Jane Doe",
                                 "jd1900@email.com",
                                 "password",
                                 "password")
        self.assertTrue(b"The account for jd1900@email.com has been created", response.data)
        # Asserts that the redirect to the login page was successful
        self.assertTrue(b"Sign In", response.data)

    def test_register_with_existing_user(self):
        response = self.register("John Doe",
                                 "johndoe@email.com",
                                 "password",
                                 "password")
        self.assertTrue(b"An account with this email already exists", response.data)

    def test_register_with_invalid_email(self):
        response = self.register("Jane Doe",
                                 "Invalid Email!",
                                 "password",
                                 "password")
        self.assertTrue(b"Invalid email address", response.data)

    def test_register_with_incorrect_confirm_password(self):
        response = self.register("Jane Doe",
                                 "jd1900@email.com",
                                 "password",
                                 "different_password")
        self.assertTrue(b"Field must be equal to password", response.data)

    def test_register_with_empty_name_and_email(self):
        response = self.register("",
                                 "",
                                 "password",
                                 "password")
        self.assertTrue(b"This field is required.", response.data)

    # ***** Tests for the login route *****
    def test_login_route(self):
        response = client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"Sign In", response.data)

    def test_login_with_valid_credentials(self):
        response = self.login("johndoe@email.com",
                              "password")
        self.assertEqual(response.status_code, 200)
        # Asserts the redirect to the feedback page
        self.assertTrue(b"John Doe, your feedback is appreciated!", response.data)
        self.assertIn(b"Sign Out", response.data)
        # Asserts that the Sign Out link is present on other pages after logging in
        client.get("/")
        self.assertIn(b"Sign Out", response.data)

    def test_login_with_invalid_credentials(self):
        response = self.login("johndoe@email.com",
                              "password1")
        self.assertTrue(b"Please check your credentials", response.data)
        self.assertTrue(b"Sign In", response.data)

    def test_login_without_email_and_password(self):
        response = self.login("",
                              "")
        self.assertTrue(b"This field is required.", response.data)
        self.assertTrue(b"Sign In", response.data)

    # ***** Tests for the feedback route *****
    def test_feedback_route_without_logging_in(self):
        response = client.get("/feedback", follow_redirects=True)
        self.assertTrue(b"Please log in to access this page.", response.data)
        self.assertTrue(b"Sign In", response.data)

    def test_submit_feedback(self):
        u = UserModel(name="Test User",
                      email="TestUser@email.com",
                      password="password")
        db.session.add(u)
        db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = int(u.get_id())
            sess["_fresh"] = True

        response = client.get("/feedback")
        self.assertTrue(b"Test User, your feedback is appreciated!", response.data)
        feedback = self.feedback(5, True, True, False, False, "Test Comment", 1)
        self.assertTrue(b"Thanks for your feedback, Test User.", response.data)

    # ***** Tests for the success route *****
    def test_success_route_without_logging_in(self):
        response = client.get("/success", follow_redirects=True)
        self.assertTrue(b"Please log in to access this page.", response.data)
        self.assertTrue(b"Sign In", response.data)

    def test_provide_multiple_feedback_in_one_session(self):
        u = UserModel(name="Test User",
                      email="TestUser@email.com",
                      password="password")
        db.session.add(u)
        db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = int(u.get_id())
            sess["_fresh"] = True

        client.get("/feedback")
        self.feedback(5, True, True, False, False, "Test Comment", 1)
        client.get("/")
        response = client.get("/feedback")
        self.assertTrue(b"Thanks, Test User! We have recorded your recent feedback.", response.data)

    # ***** Tests for the logout route *****
    def test_logout(self):
        u = UserModel(name="Test User",
                      email="TestUser@email.com",
                      password="password")
        db.session.add(u)
        db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = int(u.get_id())
            sess["_fresh"] = True

        response = client.get("/logout", follow_redirects=True)
        self.assertTrue(b"Farm Fresh Produce", response.data)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()