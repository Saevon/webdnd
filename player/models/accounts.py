import datetime
import hashlib

from django.db import models

from player.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from player.models.abstract import AbstractGameModel

class Account(AbstractGameModel):
    """
    A webdnd account.
    """

    username = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=False,
        unique=True)
    name = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=False)
    password_hash = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=False)
    password_salt = models.CharField(
        max_length=16,
        default=_create_salt,
        editable=False
        blank=False)
    email = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=True)
    active = models.SmallIntegerField(
        blank=False,
        null=False,
        default=0)
    signup_date = models.DateTimeField()

    def __unicode__(self):
        return u"%s" %(self.name)

    def _create_salt(self):
        """
        Creates a 16-byte password salt
        """
        return os.urandom(16)

    def auth_password(self, password):
        """
        Returns the success of this password
        """
        if self._hash_password(password, password_salt) == self.password_hash:
            self.session.new_session()
            return True
        return False

    def _hash_password(self, password, salt):
        """
        Hashes a password with salting
        Uses the SHA512 hash algorithm
        """
        return hashlib.sha512(password + salt).digest()

    def is_logged_in(self):
        """
        Returns whether the user is currently logged in
        """
        return self.session.is_active()

    def log_in(self, password):
        """
        Activates a logged in session for the User, and return success value
        """
        if self.auth_password(password):
            return True
        # Attempt fail .: disable any other sessions?
        return False

    def log_out(self):
        """
        logs the current user object
        """
        self.session.clear_session()

class AuthSession(AbstractGameModel):
    """
    An authenticated session
    """
    user = models.OneToOneField(
        Account,
        related_name='session',
        blank=False,
        null=False)
    expiry = models.DateTimeField(
        blank=True,
        null=True,
        default=None)
    added = models.DateTimeField(auto_now=True)

    def is_active(self):
        """
        Returns true when the session is active
        """
        now = datetime.utcnow()
        return self.expiry.date > now.date and self.expiry.time > now.time

    def add_time(self, minutes):
        """
        Extends the session by X minutes, returns a success value
        """
        # Only extend active sessions
        if self.is_active():
            self._set_expiry(self.expiry + datetime.timedelta(minutes=minutes))
            return True
        return False

    def new_session(self):
        """
        Generates a new session
        """
        self._set_expiry(datetime.utcnow())

    def clear_session(self):
        """
        Clears any current sessions
        """
        self.expiry = None
        self.save()

    def _set_expiry(self, time):
        """
        Updates the expiry datetime
        """
        self.expiry = time
        self.save()

class Preference(AbstractGameModel):
    """
    A Preference for a webdnd Account
    """

    preference = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=False)
    value = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=False)
    user = models.ForeignKey(
        Account,
        related_name='preferences',
        blank=False,
        null=False)