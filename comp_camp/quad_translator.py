import re
from uuid import uuid4
from abc import abstractmethod
from typing import List, Dict, Optional


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

    def get_temp_boolean_name(self):
        return f'temp_boolean_{uuid4().hex}'


class QuadCode:
    def __init__(self, opcodes: Optional[str] = None, value_id: Optional[str] = None):
        self.opcodes = opcodes
        self.value_id = value_id

    def finalize(self):
        if not self.opcodes:
            return

        finalized_opcodes_list: List[str] = list()
        label_name_to_opcode_line: Dict[str, int] = dict()

        opcodes_with_no_empty_lines = re.sub('(\n\s*)+', '\n', f'{self.opcodes}\nHALT')
        opcodes_with_fixed_labels = re.sub(':\n*', ':', opcodes_with_no_empty_lines)

        for opcode in opcodes_with_fixed_labels.splitlines():
            if not opcode.strip():
                continue

            if ':' in opcode:
                label_name, opcode = opcode.split(':')
                label_name_to_opcode_line[label_name] = len(finalized_opcodes_list)

            finalized_opcodes_list.append(opcode.strip())

        for i in range(len(finalized_opcodes_list)):
            for label_name, opcode_line in label_name_to_opcode_line.items():
                finalized_opcodes_list[i] = finalized_opcodes_list[i].replace(label_name, str(opcode_line))

        self.opcodes = '\n'.join(finalized_opcodes_list)
        self.opcodes += '\n# EOF, generated by Ariel Tubul\'s compiler'


class QuadTranslatable:
    @abstractmethod
    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        ...
