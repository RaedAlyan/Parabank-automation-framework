"""
Generates fake user data for testing purposes using the Faker library.

@author: Raed Eleyan
@date: 04/15/2025
@contact: raedeleyan1@gmail.com
"""
from faker import Faker

fake: Faker = Faker()

def generate_first_name() -> str:
    """Generates a random first name."""
    return fake.first_name()


def generate_last_name() -> str:
    """Generates a random last name."""
    return fake.last_name()


def generate_address() -> str:
    """Generates a random address."""
    return fake.address()


def generate_city() -> str:
    """Generates a random city."""
    return fake.city()


def generate_state() -> str:
    """Generates a random state."""
    return fake.state()


def generate_zipcode() -> str:
    """Generates a random zipcode."""
    return fake.zipcode()


def generate_phone_number() -> str:
    """Generates a random phone number."""
    return fake.phone_number()


def generate_ssn() -> str:
    """Generates a random SSN."""
    return fake.ssn()


def generate_username() -> str:
    """Generates a random username."""
    return fake.user_name()


def generate_password() -> str:
    """Generates a random password."""
    return fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
