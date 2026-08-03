from dataclasses import dataclass
@dataclass
class Credentials:
    password: str
    email: str | None = None
    phone: str | None = None
    
    @property
    def json(self):
        return {
            "email": self.email,
            "password": self.password,
            "phone": self.phone
        }