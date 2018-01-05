''' custom validator for accounts app - ensures use of special characters in a
    password field '''
import re


from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class SpecialCharactersValidator:
    ''' custom validator on password to ensure use of special characters '''
    pattern = "[$&+,:;=?@#|'<>.^*()%!-]"

    def validate(self, password, user=None):
        ''' validate password contains special chars '''
        special_chars = re.compile(self.pattern)
        has_special = special_chars.search(password)
        if has_special is None:
            raise ValidationError(
                '''The password must contain at least one of these special
                characters {} '''.format(self.pattern),
                code='password_no_special')
        return password

    def get_help_text(self):
        ''' set the help text for the validator '''
        return _(
            '''Your password must contain at least one of these special
               characters {} '''.format(self.pattern))
