from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        """
        Create and return a `User` with an username, username and password.
        """
        if not username:
            raise ValueError('Users Must Have an username address')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
