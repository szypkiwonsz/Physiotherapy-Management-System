from django.test import TestCase

from applications.users.forms import LoginForm, OfficeSignUpForm, PatientSignUpForm, NewSetPasswordForm, \
    UsersUpdateForm, \
    OfficeUpdateForm, PatientUpdateForm, ProfileUpdateForm, OfficeDayUpdateForm
from applications.users.models import User


class TestLoginForm(TestCase):
    def setUp(self):
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )

    def test_login_form_valid(self):
        form = LoginForm(data={
            'username': 'patient@gmail.com',
            'password': 'patientpassword'
        })
        self.assertTrue(form.is_valid())

    def test_login_form_no_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)


class TestOfficeSignUpForm(TestCase):
    def test_office_signup_form_valid(self):
        form = OfficeSignUpForm(data={
            'name': 'Fizjo-Med',
            'address': 'random',
            'city': 'random',
            'phone_number': '000000000',
            'website': 'www.fizjo-med.eu',
            'email': 'przykladowy_gabinet@gmail.com',
            'confirm_email': 'przykladowy_gabinet@gmail.com',
            'password1': 'szypkiwonsz',
            'password2': 'szypkiwonsz'
        })
        self.assertTrue(form.is_valid())

    def test_office_signup_form_no_data(self):
        form = OfficeSignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 8)

    def test_office_signup_form_wrong_phone_number(self):
        form = OfficeSignUpForm(data={
            'name': 'Fizjo-Med',
            'address': 'random',
            'city': 'random',
            'phone_number': '00000000',
            'website': 'www.fizjo-med.eu',
            'email': 'przykladowy_gabinet@gmail.com',
            'confirm_email': 'przykladowy_gabinet@gmail.com',
            'password1': 'szypkiwonsz',
            'password2': 'szypkiwonsz'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_office_signup_form_wrong_confirm_email(self):
        form = OfficeSignUpForm(data={
            'name': 'Fizjo-Med',
            'address': 'random',
            'city': 'random',
            'phone_number': '000000000',
            'website': 'www.fizjo-med.eu',
            'email': 'przykladowy_gabinet@gmail.com',
            'confirm_email': 'error@gmail.com',
            'password1': 'szypkiwonsz',
            'password2': 'szypkiwonsz'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_office_signup_form_wrong_second_password(self):
        form = OfficeSignUpForm(data={
            'name': 'Fizjo-Med',
            'address': 'random',
            'city': 'random',
            'phone_number': '000000000',
            'website': 'www.fizjo-med.eu',
            'email': 'przykladowy_gabinet@gmail.com',
            'confirm_email': 'przykladowy_gabinet@gmail.com',
            'password1': 'szypkiwonsz',
            'password2': 'error'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestPatientSignUpForm(TestCase):
    def test_patient_signup_form_valid(self):
        form = PatientSignUpForm(data={
            'phone_number': '000000000',
            'email': 'przykladowy_pacjent@gmail.com',
            'confirm_email': 'przykladowy_pacjent@gmail.com',
            'password1': 'szypkiwonsz',
            'password2': 'szypkiwonsz'
        })
        self.assertTrue(form.is_valid())

    def test_patient_signup_form_no_data(self):
        form = PatientSignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_patient_signup_form_wrong_number(self):
        form = PatientSignUpForm(data={
            'phone_number': '00000000',
            'email': 'przykladowy_pacjent@gmail.com',
            'confirm_email': 'przykladowy_pacjent@gmail.com',
            'password1': 'szypkiwonsz',
            'password2': 'szypkiwonsz'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_patient_signup_form_wrong_confirm_email(self):
        form = PatientSignUpForm(data={
            'phone_number': '000000000',
            'email': 'przykladowy_pacjent@gmail.com',
            'confirm_email': 'error@gmail.com',
            'password1': 'szypkiwonsz',
            'password2': 'szypkiwonsz'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_patient_signup_form_wrong_second_password(self):
        form = PatientSignUpForm(data={
            'phone_number': '000000000',
            'email': 'przykladowy_pacjent@gmail.com',
            'confirm_email': 'przykladowy_pacjent@gmail.com',
            'password1': 'szypkiwonsz',
            'password2': 'error'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestNewSetPasswordForm(TestCase):
    def setUp(self):
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )

    def test_new_password_form_valid(self):
        form = NewSetPasswordForm(user=self.patient1, data={
            'new_password1': 'szypkiwonsz',
            'new_password2': 'szypkiwonsz'
        })
        self.assertTrue(form.is_valid())

    def test_new_password_form_no_data(self):
        form = NewSetPasswordForm(user=self.patient1, data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_new_password_form_wrong_second_password(self):
        form = NewSetPasswordForm(user=self.patient1, data={
            'new_password1': 'szypkiwonsz',
            'new_password2': 'error'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestUsersUpdateForm(TestCase):
    def test_user_update_form_valid(self):
        form = UsersUpdateForm(data={
            'email': 'new_email@gmail.com'
        })
        self.assertTrue(form.is_valid())

    def test_user_update_form_no_data(self):
        form = UsersUpdateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_user_update_form_email_taken(self):
        self.patient1 = User.objects.create_user(
            'patient', 'patient@gmail.com', 'patientpassword', is_patient=True
        )
        form = UsersUpdateForm(data={
            'email': 'patient@gmail.com'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestOfficeUpdateForm(TestCase):
    def test_office_update_form_valid(self):
        form = OfficeUpdateForm(data={
            'name': 'fizjo-med',
            'address': 'random',
            'city': 'random',
            'phone_number': '000000000',
            'website': 'www.fizjo-med.eu'
        })
        self.assertTrue(form.is_valid())

    def test_office_update_form_no_data(self):
        form = OfficeUpdateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_office_update_form_wrong_phone_number(self):
        form = OfficeUpdateForm(data={
            'name': 'fizjo-med',
            'address': 'random',
            'city': 'random',
            'phone_number': '00000000',
            'website': 'www.fizjo-med.eu'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestPatientUpdateForm(TestCase):
    def test_patient_update_form_valid(self):
        form = PatientUpdateForm(data={
            'phone_number': '000000000'
        })
        self.assertTrue(form.is_valid())

    def test_patient_update_form_no_data(self):
        form = PatientUpdateForm(data={})
        # Phone number is not required.
        self.assertTrue(form.is_valid())

    def test_patient_update_form_wrong_phone_number(self):
        form = PatientUpdateForm(data={
            'phone_number': '00000000'
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestProfileUpdateForm(TestCase):
    # def test_profile_update_form_valid(self):
    #     pass

    def test_profile_update_form_no_data(self):
        form = ProfileUpdateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestOfficeDayUpdateForm(TestCase):
    def test_patient_update_form_valid(self):
        form = OfficeDayUpdateForm(data={
            'day': 0,
            'earliest_appointment_time': '10:00',
            'latest_appointment_time': '20:00'
        })
        self.assertTrue(form.is_valid())

    def test_patient_update_form_no_data(self):
        form = OfficeDayUpdateForm(data={})
        self.assertFalse(form.is_valid())
