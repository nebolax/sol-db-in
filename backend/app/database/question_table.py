#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from backend.app.flask_app import FlaskApp
from .editable import Editable
from .question import Question
from .formatting_settings import FormattingSettings
from typing import List, Set, Dict, Any


# List of column questions
QuestionTable_T = List[Question]


class QuestionTable(Editable, FlaskApp().db.Model):
    __tablename__ = 'question_tables'
    _block_sorting = FlaskApp().db.Column('block_sorting', FlaskApp().db.Integer)

    def __init__(self, block_sorting: int):
        super(Editable).__init__()
        self.block_sorting = block_sorting

    @property
    def block_sorting(self) -> int:
        return self._block_sorting

    @block_sorting.setter
    @Editable.on_edit
    def block_sorting(self, new_value: int) -> None:
        self._block_sorting = new_value

    @staticmethod
    def get_by_ids(ids: Set[int]) -> List['QuestionTable']:
        return QuestionTable.query.filter(QuestionTable.id.in_(ids)).all()

    def get_questions(self, with_answers=False, leader_id: int = None, project_id: int = None) -> List[Dict[str, Any]]:
        formats = FormattingSettings.get_from_question_table(self.id)
        ids = [item.id for item in formats]
        formats_dict = {item.id: item for item in formats}

        results: List[Question] = Question.get_by_ids(ids)
        results_indexed = [(result, formats_dict[result.formatting_settings].row_question_id) for result in results]
        results_indexed.sort(key=lambda x: x[1])
        return [result[0].to_json(with_answers, leader_id, project_id) for result in results_indexed]

