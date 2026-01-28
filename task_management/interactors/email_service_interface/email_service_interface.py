from abc import ABC, abstractmethod


class EmailServiceInterface(ABC):

    @abstractmethod
    def send_password_reset_email(self, email: str, reset_link: str) -> bool:
        pass
