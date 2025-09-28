class Person:
    def __init__(self, person_id: int, first_name: str, last_name: str, email: str):
        self._id = person_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email

    # Getters
    def get_id(self):
        return self._id

    def get_name(self):
        return f"{self._first_name} {self._last_name}"

    def get_email(self):
        return self._email

    # Setter with validation
    def set_email(self, email: str):
        if "@" not in email:
            raise ValueError("Invalid email address")
        self._email = email

    # Representations
    def __str__(self):
        return f"{self.get_name()} ({self._email})"

    def __repr__(self):
        return f"Person(id={self._id}, name='{self.get_name()}', email='{self._email}')"
