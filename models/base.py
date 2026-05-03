from abc import ABC, abstractmethod

class Base(ABC):
    """Clase base abstracta para todas las entidades del sistema"""
    _contador = 0
    PREFIJO = ""

    @classmethod
    def generar_id(cls):
        cls._contador += 1
        return f"{cls.PREFIJO}-{cls._contador:04d}"

    @abstractmethod
    def mostrar(self):
        """Método abstracto para mostrar información de la entidad"""
        pass
    
    @abstractmethod
    def to_dict(self):
        """Convertir entidad a diccionario para JSON"""
        pass
    
    @staticmethod
    @abstractmethod
    def from_dict(data):
        """Crear entidad desde diccionario JSON"""
        pass