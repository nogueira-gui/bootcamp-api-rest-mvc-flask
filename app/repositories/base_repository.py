from typing import List, TypeVar, Type, Optional
from app import db

T = TypeVar('T', bound=db.Model)

class BaseRepository:
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
    
    def create(self, **kwargs) -> T:
        instance = self.model_class(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance
    
    def get_by_id(self, id: int) -> Optional[T]:
        return self.model_class.query.get(id)
    
    def get_all(self) -> List[T]:
        return self.model_class.query.all()
    
    def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        db.session.commit()
        return instance
    
    def delete(self, instance: T) -> None:
        db.session.delete(instance)
        db.session.commit()
    
    def filter_by(self, **kwargs) -> List[T]:
        return self.model_class.query.filter_by(**kwargs).all()
    
    def first(self, **kwargs) -> Optional[T]:
        return self.model_class.query.filter_by(**kwargs).first() 