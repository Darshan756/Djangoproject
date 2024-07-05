from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserRegisterForm

class TestUserRegisterForm(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_password2(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': '',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_invalid_email(self):
        form_data = {
            'username': 'testuser',
            'email': 'invalidemail',  # Invalid email format
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_short_password(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'short',  # Short password
            'password2': 'short',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_passwords_dont_match(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'mismatchedpassword',  # Passwords don't match
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


from django.test import TestCase
from django.contrib.auth.models import User
from user.models import Profile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create a test image file
        self.test_image_path = 'media/profile_pics/hotel-1068x801.jpg'
        self.test_image = SimpleUploadedFile(name='hotel-1068x801.jpg', content=open(self.test_image_path, 'rb').read(),
                                             content_type='image/jpeg')

        # Delete any existing profile for the user before creating a new one
        Profile.objects.filter(user=self.user).delete()

        self.profile = Profile.objects.create(user=self.user, image=self.test_image, country_name='Test Country')

    def test_profile_str_method(self):
        self.assertEqual(str(self.profile), 'testuser Profile')

    def test_profile_image_upload(self):
        # Debugging: Print the actual image path
        print(f"Uploaded image path: {self.profile.image.path}")

        # Ensure the image was uploaded to the correct path
        expected_dir = os.path.join('media', 'profile_pics')
        actual_dir = os.path.dirname(self.profile.image.path)
        self.assertTrue(expected_dir in actual_dir)
        self.assertTrue(os.path.basename(self.profile.image.path).startswith('hotel-1068x801'))

    def test_profile_image_resize(self):
        # Open the image and check its dimensions
        img = Image.open(self.profile.image.path)
        self.assertLessEqual(img.height, 300)
        self.assertLessEqual(img.width, 300)

    def tearDown(self):
        # Clean up by deleting the user and profile objects
        self.user.delete()
        # Remove the test image if it was created
        if os.path.exists(self.profile.image.path):
            os.remove(self.profile.image.path)
