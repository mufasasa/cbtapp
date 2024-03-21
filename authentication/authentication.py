from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from authentication.models import TimedAuthToken


class TimedAuthTokenAuthentication(TokenAuthentication):
    model = TimedAuthToken
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)

        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if token.is_expired:
            raise exceptions.AuthenticationFailed('session timed out, for your security please log in again')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        # Since the token was used to authenticate, we can calculate a new
        # expiration date, and update the last used date.
        token.calculate_new_expiration()
        token.save(update_fields=['expires', 'last_used'])

        return token.user, token
