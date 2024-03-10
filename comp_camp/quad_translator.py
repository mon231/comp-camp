from uuid import uuid4
from abc import abstractmethod
from typing import Dict, Optional


class QuadTranslator:
    def __init__(self):
        self.__id_to_type: Dict[str, str]

    def declare_new_variable(self, variable_id: str, variable_type: str):
        if variable_id in self.__id_to_type:
            raise NameError(f'variable named {variable_id} was already declared')

        self.__id_to_type[variable_id] = variable_type

    def get_variable_type(self, variable_id: str) -> str:
        if variable_id not in self.__id_to_type:
            raise NameError(f'variable named {variable_id} was not declared')

        return self.__id_to_type[variable_id]

    def get_temp_variable_name(self, variable_type: str):
        variable_name = f'temp_variable_{uuid4().hex}'
        self.__id_to_type[variable_name] = variable_type

    def get_temp_label_name(self):
        return f'temp_label_{uuid4().hex}'


class QuadCode:
    def __init__(self, opcodes: Optional[str] = None, value_id: Optional[str] = None):
        self.opcodes = opcodes
        self.value_id = value_id


class QuadTranslatable:
    @abstractmethod
    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        ...
