from django.test import TestCase
from playground.models import storyHistory
from django.contrib.auth.models import User  # If you're using the default User model


#python manage.py test playground.tests.StoryHistoryModelTestCase
# This is for console


class StoryHistoryModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.story_instance = storyHistory.objects.create(
            user_id=self.user,
            name="Test Story",
            friend_name="Test Friend",
            story_topic="Test Topic",
            generated_story="Test Generated Story"
        )

    def test_story_instance_creation(self):
        self.assertTrue(isinstance(self.story_instance, storyHistory))
        self.assertEqual(self.story_instance.name, "Test Story")
