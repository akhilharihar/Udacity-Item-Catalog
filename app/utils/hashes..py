from hashids import Hashids
from abc import ABC, abstractmethod
from flask import abort


class Hashes():
    """
    Obfuscate integers using hashids.
    params:
    salt: A random string to make the obfusated output unique.
    min-length: the minimum length of the obfucted string to be generated
    from an integer.
    """
    def __init__(self, salt, min_length):
        self.length = min_length
        self.__hash = Hashids(salt=salt, min_length=self.length)

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, value):
        if value < 1 or not isinstance(value, int):
            raise ValueError('Min length argument should be an integer \
                greater than 1.')
        else:
            self.__length = value

    def encode(self, value):
        """
        Build hash from a int value.
        """
        return self.__hash.encode(value)

    def decode(self, value):
        """
        Restores encoded hash values to tuple.
        """
        return self.__hash.decode(value)


class AbstractHashID(ABC):
    """
    Abstract Class to easily obfustate database integer primary keys and
    vice versa.

    Refer :class: Hashes for more info on how this abstract class is
    implemented.
    """

    @staticmethod
    def hash_provider(secret, length):
        """
        Return Hashid instance. There's no need to call this method as this is
        directly called by the below hash method.
        """

        return Hashes(salt=secret, min_length=length)

    @classmethod
    @abstractmethod
    def hash(cls):
        """
        Abstract class method. Should return the above hash_provider method.

        eg: return cls.hash_provider('Z8e9ZBebzy', 5)
        """
        pass

    @classmethod
    def encode(cls, value):
        """Return obfustated string from an integer."""
        try:
            unhashed_int = int(value)
        except TypeError:
            abort(404)

        return cls.hash().encode(unhashed_int)

    @classmethod
    def decode(cls, value):
        """Returns the first integer from the deobfuscated integer tuple."""

        unhashed_tuple = cls.hash().decode(value)

        if len(unhashed_tuple):
            abort(404)

        return unhashed_tuple[0]
