from pet import Animal


class Turtle(Animal):

    def get_age_in_human_years(self) -> int:
        if self._age <= 0:
            return 0
        return 15 + (self._age - 1) * 2

    def express(self) -> None:
        print(r"""
  _____     ____
 /      \  |  o |
|        |/ ___\|
|_________/
|_|_| |_|_|
""")


class Parrot(Animal):

    def get_age_in_human_years(self) -> int:
        return self._age * 5

    def express(self) -> None:
        print(f'{self._name}: "Hello!"')
        print(r"""
   \
   (o>
\\_//)
 \_/_)
  _|_
""")