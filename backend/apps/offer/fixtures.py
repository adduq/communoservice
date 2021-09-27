from .models import Offer
from django.contrib.auth.models import User
import decimal


class OfferFixtures:

    # @staticmethod
    # def any_valid_user():
    #     username = "Gandalf"
    #     firstname = "Gandalf"
    #     lastname = "LeBlanc"
    #     email = "gandalf@globetrotter.net"
    #     password = "qwerty1234"

    #     user = User.objects.create(username=username,
    #                                first_name=firstname,
    #                                last_name=lastname,
    #                                email=email,
    #                                password=password)

    #     return user

    @staticmethod
    def any_type_service():
        return "Gardiennage"

    @staticmethod
    def any_description():
        return "Beaucoup d'expérience avec les ados indisciplinés."

    @staticmethod
    def any_hourly_rate():
        rate = decimal.Decimal(12.5)
        return rate

    @staticmethod
    def negative_hourly_rate():
        rate = decimal.Decimal('12.5').copy_negate()
        return rate

    @staticmethod
    def over_max_digits_hourly_rate():
        rate = decimal.Decimal('12345.12')
        return rate

    @staticmethod
    def over_max_decimals_hourly_rate():
        rate = decimal.Decimal('10.1234')
        return rate

    @staticmethod
    def any_max_distance():
        return 2

    @staticmethod
    def negative_max_distance():
        return -2

    @staticmethod
    def wrong_type_max_distance():
        return 2.5

    # @staticmethod
    # def any_valid_offer():
    #     offer = Offer.objects.create(OfferFixtures.any_valid_user(),
    #                                  OfferFixtures.any_type_service(),
    #                                  OfferFixtures.any_description(),
    #                                  OfferFixtures.any_hourly_rate(),
    #                                  OfferFixtures.any_max_distance())
    #     return offer
