#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from . import db
from backend.constants import MAX_TOPONYM_SIZE
from typing import List, Dict, Any


class Toponym(db.Model):
    __tablename__ = 'toponyms'
    id = db.Column('id', db.Integer, primary_key=True, unique=True)
    name = db.Column('name', db.Text(MAX_TOPONYM_SIZE))
    parent_id = db.Column('parent_id', db.ForeignKey('toponyms.id'), nullable=True, default=None)

    @staticmethod
    def get_by_name(name: str) -> 'Toponym':
        return Toponym.query.filter_by(name=name).first()

    def __init__(self, name: str, parent_name: str) -> None:
        parent = Toponym.get_by_name(parent_name)
        if parent is not  None:
            self.name = name
            self.parent_id = parent.id

    def to_json(self) -> Dict[str, Any]:
        return self.__dict__

    def get_ancestors(self) -> List['Toponym']:
        result = [self]
        current = self.parent_id

        # not sure about correctness of this check: int NULL value might be 0 - IDK
        while current is not None:
            node = Toponym.query.filter_by(id=current)
            result.append(node)
            current = node.parent_id
        return result

    @staticmethod
    def search_by_name(name_substring: str) -> List['Toponym']:
        return Toponym.query.filter(Toponym.name.like(f"%{name_substring}%")).all()
