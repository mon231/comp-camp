from dataclasses import dataclass
from typing import List, Dict, Union
from .quad_translator import QuadTranslator, QuadTranslatable, QuadCode


# START declarations #
class Declaration(QuadTranslatable):
    def __init__(self, variable_ids: List[str], variable_type: str):
        self.variable_ids = variable_ids
        self.variable_type = variable_type

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        for id in self.variable_ids:
            quad_translator.declare_new_variable(id, self.variable_type)

        return QuadCode()

class Declarations(QuadTranslatable):
    def __init__(self, declarations: List[Declaration] = []):
        self.declarations = declarations

    def add_declaration(self, declaration: Declaration):
        self.declarations.append(declaration)

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        for declaration in self.declarations:
            declaration.translate(quad_translator)

        return QuadCode()
# END   declarations #

# START base statements #
class Statement(QuadTranslatable):
    pass

class StatementList(Statement):
    def __init__(self, statements: List[Statement] = []):
        self.statements = statements

    def add_statement(self, statement: Statement):
        self.statements.append(statement)

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        opcodes = ''
        if not self.statements: return QuadCode()

        for statement in self.statements:
            last_quad_code = statement.translate(quad_translator)
            opcodes += last_quad_code.opcodes + '\n'

        return QuadCode(opcodes, last_quad_code.value_id)

class StatementBlock(Statement):
    def __init__(self, statements: StatementList):
        self.statements = statements

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        return self.statements.translate(quad_translator)
# END   base statements #

# START cases #
@dataclass
class DefaultCase:
    statements: StatementList

@dataclass
class ConditionalCase:
    number: int
    statements: StatementList

@dataclass
class ConditionalCases:
    cases: List[ConditionalCase]

    def add_case(self, case: ConditionalCase):
        self.cases.append(case)
# END   cases #

# START expressions #
# TODO
class Expression(QuadTranslatable):
    pass

class BooleanExpression(QuadTranslatable):
    def __init__(self, value: Union['BooleanTerm', 'BooleanOperationOR']):
        self.value = value

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        return self.value.translate(quad_translator)

class BooleanTerm(QuadTranslatable):
    def __init__(self, value: Union['BooleanFactor', 'BooleanOperationAND']):
        self.value = value

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        return self.value.translate(quad_translator)

class BooleanFactor(QuadTranslatable):
    pass

class BooleanOperationOR(QuadTranslatable):
    def __init__(self, boolean_expression: BooleanExpression, boolean_term: BooleanTerm):
        self.boolean_term = boolean_term
        self.boolean_expression = boolean_expression

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        boolean_value_name = quad_translator.get_temp_boolean_name()
        right_boolean_evaluation = self.boolean_term.translate(quad_translator)
        left_boolean_evaluation = self.boolean_expression.translate(quad_translator)

        opcodes = f'''
        {right_boolean_evaluation.opcodes}
        {left_boolean_evaluation.opcodes}

        IADD {boolean_value_name} {left_boolean_evaluation.value_id} {right_boolean_evaluation.value_id}
        '''

        return QuadCode(opcodes=opcodes, value_id=boolean_value_name)

class BooleanOperationAND(QuadTranslatable):
    def __init__(self, boolean_term: BooleanTerm, boolean_factor: BooleanFactor):
        self.boolean_term = boolean_term
        self.boolean_factor = boolean_factor

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        boolean_value_name = quad_translator.get_temp_boolean_name()
        label_do_not_change_value = quad_translator.get_temp_label_name()
        right_boolean_evaluation = self.boolean_term.translate(quad_translator)
        left_boolean_evaluation = self.boolean_factor.translate(quad_translator)

        opcodes = f'''
        {right_boolean_evaluation.opcodes}
        {left_boolean_evaluation.opcodes}

        INQL {boolean_value_name} {left_boolean_evaluation} 0
        JMPZ {label_do_not_change_value} {boolean_value_name}

        INQL {boolean_value_name} {right_boolean_evaluation} 0
        {label_do_not_change_value};
        '''

        return QuadCode(opcodes=opcodes, value_id=boolean_value_name)
# END   expressions #

# START statements #
class InputStatement(Statement):
    def __init__(self, id: str):
        self.id = id

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        match quad_translator.get_variable_type(self.id):
            case 'int':
                return QuadCode(opcodes=f'IINP {self.id}')

            case 'float':
                return QuadCode(opcodes=f'RINP {self.id}')

class OutputStatement(Statement):
    def __init__(self, id: str):
        self.id = id

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        match quad_translator.get_variable_type(self.id):
            case 'int':
                return QuadCode(opcodes=f'IPRT {self.id}')

            case 'float':
                return QuadCode(opcodes=f'RPRT {self.id}')

class BreakStatement(Statement):
    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        raise NotImplementedError('Due to time constraints, the break statement is not implemented')

class AssignmentStatement(Statement):
    def __init__(self, id: str, expression: Expression):
        self.id = id
        self.expression = expression

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        expression_evaluation_code = self.expression.translate(quad_translator)

        if expression_evaluation_code.value_id is None:
            raise TypeError('Invalid value-less expression')

        evaluated_expression_type = quad_translator.get_variable_type(expression_evaluation_code.value_id)
        assignment_opcodes = AssignmentStatement.__get_assignment_opcodes(
            expression_evaluation_code.value_id,
            evaluated_expression_type,
            self.id,
            quad_translator.get_variable_type(self.id)
        )

        return QuadCode(opcodes=f'{expression_evaluation_code.opcodes}\n{assignment_opcodes}')

    @staticmethod
    def __get_assignment_opcodes(
        src_variable_name: str,
        src_variable_type: str,
        dst_variable_name: str,
        dst_variable_type: str):

        if src_variable_type == 'int' and dst_variable_type == 'int':
            return f'IASN {dst_variable_name} {src_variable_name}'
        elif src_variable_type == 'float' and dst_variable_type == 'float':
            return f'RASN {dst_variable_name} {src_variable_name}'
        elif src_variable_type == 'int' and dst_variable_type == 'float':
            return f'ITOR {dst_variable_name} {src_variable_name}'
        else:
            raise TypeError('Invalid assignment of float expression into int variable')

class IFStatement(Statement):
    def __init__(self, condition: BooleanExpression, case_true: Statement, case_false: Statement):
        self.condition = condition
        self.case_true = case_true
        self.case_false = case_false

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        case_true_label_name = quad_translator.get_temp_label_name()
        case_false_label_name = quad_translator.get_temp_label_name()
        post_case_false_label_name = quad_translator.get_temp_label_name()
        condition_evaluation_code = self.condition.translate(quad_translator)

        opcodes = f'''
        {condition_evaluation_code.opcodes}
        JUMPZ {case_false_label_name} {condition_evaluation_code.value_id}

        {case_true_label_name}: {self.case_true.translate(quad_translator).opcodes}
        JUMP {post_case_false_label_name}

        {case_false_label_name}: {self.case_false.translate(quad_translator).opcodes}
        {post_case_false_label_name}:'''

        return QuadCode(opcodes=opcodes)

class WhileStatement(Statement):
    def __init__(self, condition: BooleanExpression, statement: Statement):
        self.condition = condition
        self.statement = statement

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        post_statement_label_name = quad_translator.get_temp_label_name()
        check_condition_label_name = quad_translator.get_temp_label_name()
        condition_evaluation_code = self.condition.translate(quad_translator)

        opcodes = f'''
        {check_condition_label_name}: {condition_evaluation_code.opcodes}
        JMPZ {post_statement_label_name} {condition_evaluation_code.value_id}

        {self.statement.translate(quad_translator).opcodes}

        JUMP {check_condition_label_name}
        {post_statement_label_name}:'''

        return QuadCode(opcodes=opcodes)

class SwitchStatement(Statement):
    def __init__(self, expression: Expression, conditional_cases: ConditionalCases, default_case: DefaultCase):
        self.expression = expression
        self.default_case = default_case
        self.conditional_cases = conditional_cases

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        boolean_name = quad_translator.get_temp_boolean_name()
        expression_code = self.expression.translate(quad_translator)
        post_last_case_label_name = quad_translator.get_temp_label_name()

        if not expression_code.value_id or quad_translator.get_variable_type(expression_code.value_id) == 'int':
            raise SyntaxError('expression for switch statement must be integer')

        label_to_conditional_case: Dict[str, ConditionalCase] = {
            quad_translator.get_temp_label_name(): conditional_case
            for conditional_case in self.conditional_cases
        }

        conditional_case_number_to_label: Dict[int, str] = {
            conditional_case.number: label_name
            for label_name, conditional_case in label_to_conditional_case.items()
        }

        if len(conditional_case_number_to_label) != len(label_to_conditional_case):
            raise SyntaxError('Invalid duplicate cases')

        # TODO: use RELop equals
        compare_and_jump_case_opcodes = [
            f'''
            INQL {boolean_name} {expression_code.value_id} {case_number}
            JMPZ {case_label} {boolean_name}
            '''
            for case_number, case_label in conditional_case_number_to_label.items()
        ]

        default_case_opcodes = f'''
        {self.default_case.statements.translate(quad_translator).opcodes}
        JUMP {post_last_case_label_name}
        '''

        opcodes = f'''
        {compare_and_jump_case_opcodes}
        {default_case_opcodes}
        {'\n'.join(
            f'{label_name}: {conditional_case.statements.translate(quad_translator).opcodes}'
            for label_name, conditional_case
            in label_to_conditional_case.items()
        )}
        {post_last_case_label_name}:'''

        return QuadCode(opcodes=opcodes)
# END   statements #

# START AST #
class Program:
    def __init__(self, declarations: List[Declaration], statement_block: StatementBlock):
        self.declarations = declarations
        self.statement_block = statement_block

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        for declaration in self.declarations:
            declaration.translate(quad_translator)

        return self.statement_block.translate(quad_translator)
# END   AST #
