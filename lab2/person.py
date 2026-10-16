from pet import Pet


class Person:

    def __init__(self, name: str, pet: Pet | None = None) -> None:
        self._name = name
        self._pet = pet

    def set_pet(self, pet: Pet) -> None:
        self._pet = pet

    def get_pet_info(self) -> None:
        print("-" * 20)

        if self._pet is None:
            print(f"{self._name} has no pet yet")
            print("-" * 20)
            return

        pet = self._pet
        print(f"Pet for {self._name} is named {pet.get_name()}")
        print(
            f"Age: {pet.get_age()} year(s), "
            f"about {pet.get_age_in_human_years()} human years"
        )
        print("And it expresses itself like this:")
        pet.express()
        print("-" * 20)