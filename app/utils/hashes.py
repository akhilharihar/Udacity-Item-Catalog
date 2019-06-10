from hashids import Hashids
from abc import ABC, abstractmethod
from flask import abort


class Hashes():
    """
    Obfuscate integers using hashids.
    params:
    salt: A random string to make the obfuscated output unique.
    min-length: the minimum length of the obfuscated string to be generated
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
    Abstract Class to easily obfuscate database integer primary keys and
    vice versa.

    Methods:
    encode(int): the integer to be obfuscated. returns type:str
    decode(str): the string to be de-obfuscated. returns type:int

    Example:

    class Test(AbstractHashID):
        salt='random_string'
        min_length=5
    """

    @property
    @abstractmethod
    def salt(self):
        """
        Random string to make obfuscated data unique.

        eg: return 'liwordofs'
        """
        pass

    @property
    @abstractmethod
    def min_length(self):
        """
        Single digit integer.
        """
        pass

    @classmethod
    def hash(cls):
        """
        set class hashes with secret and min length.
        """
        return Hashes(str(cls.salt), int(cls.min_length))

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

        if not len(unhashed_tuple):
            abort(404)

        return unhashed_tuple[0]
