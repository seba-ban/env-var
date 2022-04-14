from unittest import TestCase

from env_var import env
from env_var._transformers.numeric import num_transformer_factory

from .helpers import VAR_NAME, check_validators, set_var


class TestNumeric(TestCase):
    def test_int(self):
        valid_values = (
            ("10", 10),
            ("1231", 1231),
            ("412", 412),
            ("-121231", -121231),
            ("0", 0),
        )
        invalid_values = ("10.", "10.5", "asd")
        check_validators(self, env(VAR_NAME).as_int(), valid_values, invalid_values)

        valid_values = (
            ("10", 10),
            ("1231", 1231),
        )
        invalid_values = ("9", "0")
        check_validators(
            self, env(VAR_NAME).as_int(min=10), valid_values, invalid_values
        )

        valid_values = (
            ("10", 10),
            ("-10", -10),
        )
        invalid_values = ("19", "11")
        check_validators(
            self, env(VAR_NAME).as_int(max=10), valid_values, invalid_values
        )

        valid_values = (
            ("5", 5),
            ("8", 8),
            ("10", 10),
        )
        invalid_values = ("19", "-11", "0")
        check_validators(
            self, env(VAR_NAME).as_int(min=5, max=10), valid_values, invalid_values
        )

        valid_values = (
            ("a", 10),
            ("A", 10),
            ("f", 15),
            ("10", 16),
        )
        invalid_values = ("af", "-11", "0")
        check_validators(
            self,
            env(VAR_NAME).as_int(min=10, max=16, base=16),
            valid_values,
            invalid_values,
        )

    def test_int_base(self):
        set_var("100")
        for i in range(2, 37):
            self.assertEqual(env(VAR_NAME).as_int(base=i).required(), i**2)

    def test_int_positive(self):
        valid_values = (("10", 10), ("0", 0))
        invalid_values = ("-1", "-1000")
        check_validators(
            self, env(VAR_NAME).as_int_positive(), valid_values, invalid_values
        )

        valid_values = (("a", 10), ("0", 0))
        invalid_values = ("-af", "-11")
        check_validators(
            self, env(VAR_NAME).as_int_positive(base=16), valid_values, invalid_values
        )

    def test_int_negative(self):
        valid_values = (("-10", -10), ("-11305", -11305))
        invalid_values = ("1", "1000", "0", "-1.")
        check_validators(
            self, env(VAR_NAME).as_int_negative(), valid_values, invalid_values
        )

        valid_values = (("-a", -10),)
        invalid_values = ("af", "11", "0")
        check_validators(
            self, env(VAR_NAME).as_int_negative(base=16), valid_values, invalid_values
        )

    def test_as_float(self):
        valid_values = (("-10", -10.0), ("-11305", -11305.0), ("0", 0.0), ("13.", 13.0))
        invalid_values = "not_a_float"
        check_validators(self, env(VAR_NAME).as_float(), valid_values, invalid_values)

        valid_values = (("10.5", 10.5), ("11305", 11305.0))
        invalid_values = "9.2"
        check_validators(
            self, env(VAR_NAME).as_float(min=10), valid_values, invalid_values
        )

        valid_values = (("9.23", 9.23), ("-10321.421", -10321.421))
        invalid_values = ("10.5", "100.12314")
        check_validators(
            self, env(VAR_NAME).as_float(max=10), valid_values, invalid_values
        )

        valid_values = (("9.23", 9.23), ("5.", 5.0), ("10", 10.0))
        invalid_values = ("10.5", "100.12314", "4.12")
        check_validators(
            self, env(VAR_NAME).as_float(min=5, max=10), valid_values, invalid_values
        )

    def test_as_float_positive(self):
        valid_values = (("9.23", 9.23), ("0", 0.0), ("10", 10.0))
        invalid_values = ("-10.5", "-100.12314", "-4.12")
        check_validators(
            self, env(VAR_NAME).as_float_positive(), valid_values, invalid_values
        )

    def test_as_float_negative(self):
        valid_values = (("-9.23", -9.23), ("-10", -10.0))
        invalid_values = ("0", "10.5", "0.0000000001")
        check_validators(
            self, env(VAR_NAME).as_float_negative(), valid_values, invalid_values
        )

    def test_as_port_number(self):
        valid_values = tuple((str(i), i) for i in range(1, 65535))
        invalid_values = tuple(str(i) for i in range(-100, 1)) + tuple(
            str(i) for i in range(65536, 70000)
        )
        check_validators(
            self, env(VAR_NAME).as_port_number(), valid_values, invalid_values
        )

    def test_if_raises(self):
        set_var("8")
        with self.assertRaises(ValueError):
            env(VAR_NAME).as_int(min=10, max=5)

        with self.assertRaises(ValueError):
            num_transformer_factory(float, base=10)

    def test_accept_one(self):
        set_var("8")
        self.assertEqual(env(VAR_NAME).as_int(min=8, max=8).required(), 8)
