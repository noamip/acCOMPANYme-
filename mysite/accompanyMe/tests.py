from django.test import TestCase

from .models import User


class ExpensesTestCase(TestCase):
    def test_expense(self):
        self.assertEqual(User.objects.count(), 0)

        e = User(
            name="noami",
            email="noamijofen@gmail.com",
            phone_number="0548485512"
        )
        e.save()

        self.assertEqual(User.objects.count(), 1)




