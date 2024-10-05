from abc import ABC, abstractmethod
from .models import Review, Menu
from user.models import CustomUser

class AbstractFactory(ABC):
    @abstractmethod
    def create_instance(self, *args, **kwargs):
        pass

class UserFactory(AbstractFactory):
    def create_instance(self, username, name, age, weight, height):
        return CustomUser.objects.create_user(username=username, name=name, age=age, weight=weight, height=height)

class ReviewFactory(AbstractFactory):
    def create_instance(self, user, menu, text, favorito, calificacion):
        return Review.objects.create(user=user, menu=menu, text=text, favorito=favorito, calificacion=calificacion)
