from abc import ABC, abstractmethod


class Pet(ABC):

    @abstractmethod
    def express(self) -> None:
        ...

    @abstractmethod
    def get_name(self) -> str:
        ...

    @abstractmethod
    def get_age(self) -> int:
        ...

    @abstractmethod
    def get_age_in_human_years(self) -> int:
        ...


class Animal(Pet, ABC):

    def __init__(self, name: str, age: int) -> None:
        self._name = name
        self._age = age

    def happy_birthday(self) -> None:
        self._age += 1

    @abstractmethod
    def express(self) -> None:
        ...

    @abstractmethod
    def get_age_in_human_years(self) -> int:
        ...

    def get_name(self) -> str:
        return self._name

    def get_age(self) -> int:
        return self._age