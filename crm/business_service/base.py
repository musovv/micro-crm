from abc import ABC, abstractmethod


class EntityBase(ABC):
    @abstractmethod
    def id(self):
        pass

    @abstractmethod
    def dict(self):
        pass
