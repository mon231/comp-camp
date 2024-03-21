from dataclasses import dataclass
from typing import List, Dict, Union, Tuple
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
        total_declared_variable_names = []

        for declaration in self.declarations:
            declaration.translate(quad_translator)
            total_declared_variable_names += declaration.variable_ids

        if len(set(total_declared_variable_names)) != len(total_declared_variable_names):
            raise SyntaxError('Invalid re-declaration of variable')

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
            opcodes += f'{last_quad_code.opcodes}\n'

        return QuadCode(opcodes=opcodes, value_id=last_quad_code.value_id)

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
class NumericExpression(QuadTranslatable):
    def __init__(self, value: Union['NumericTerm', 'NumericOperationADD', 'NumericOperationSUB']):
        self.value = value

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        return self.value.translate(quad_translator)

class NumericTerm(QuadTranslatable):
    def __init__(self, value: Union['NumericFactor', 'NumericOperationMUL', 'NumericOperationDIV']):
        self.value = value

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        return self.value.translate(quad_translator)

class NumericFactor(QuadTranslatable):
    def __init__(self, value: int | float | str):
        for possible_number_type in (int, float):
            try:
                value = possible_number_type(value)
                break
            except: pass

        self.value = value

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        return QuadCode(value_id=self.value)

class NumericBinaryOperation(QuadTranslatable):
    def __init__(self, left_expression: NumericExpression, right_expression: NumericExpression):
        self.left_expression = left_expression
        self.right_expression = right_expression

    def assign_type_adjusted_expressions(self, quad_translator: QuadTranslator) -> str:
        left_expression_evaluation = self.left_expression.translate(quad_translator)
        right_expression_evaluation = self.right_expression.translate(quad_translator)

        if quad_translator.get_variable_type(left_expression_evaluation.value_id) == quad_translator.get_variable_type(right_expression_evaluation.value_id):
            return quad_translator.get_variable_type(left_expression_evaluation.value_id)

        if quad_translator.get_variable_type(left_expression_evaluation.value_id) != 'float':
            self.left_expression = NumericOperationCast(self.left_expression, 'float')

        if quad_translator.get_variable_type(right_expression_evaluation.value_id) != 'float':
            self.right_expression = NumericOperationCast(self.right_expression, 'float')

        return 'float'

class NumericOperationADD(NumericBinaryOperation):
    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        adjusted_type = self.assign_type_adjusted_expressions(quad_translator)
        value_name = quad_translator.get_temp_variable_name(adjusted_type)

        left_boolean_evaluation = self.left_expression.translate(quad_translator)
        right_boolean_evaluation = self.right_expression.translate(quad_translator)

        add_opcode = 'IADD' if (adjusted_type == 'int') else 'RADD'
        opcodes = f'''
        {right_boolean_evaluation.opcodes}
        {left_boolean_evaluation.opcodes}

        {add_opcode} {value_name} {left_boolean_evaluation.value_id} {right_boolean_evaluation.value_id}
        '''

        return QuadCode(opcodes=opcodes, value_id=value_name)

class NumericOperationSUB(NumericBinaryOperation):
    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        adjusted_type = self.assign_type_adjusted_expressions(quad_translator)
        value_name = quad_translator.get_temp_variable_name(adjusted_type)

        left_boolean_evaluation = self.left_expression.translate(quad_translator)
        right_boolean_evaluation = self.right_expression.translate(quad_translator)

        add_opcode = 'ISUB' if (adjusted_type == 'int') else 'RSUB'
        opcodes = f'''
        {right_boolean_evaluation.opcodes}
        {left_boolean_evaluation.opcodes}

        {add_opcode} {value_name} {left_boolean_evaluation.value_id} {right_boolean_evaluation.value_id}
        '''

        return QuadCode(opcodes=opcodes, value_id=value_name)

class NumericOperationMUL(NumericBinaryOperation):
    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        adjusted_type = self.assign_type_adjusted_expressions(quad_translator)
        value_name = quad_translator.get_temp_variable_name(adjusted_type)

        left_boolean_evaluation = self.left_expression.translate(quad_translator)
        right_boolean_evaluation = self.right_expression.translate(quad_translator)

        add_opcode = 'IMLT' if (adjusted_type == 'int') else 'RMLT'
        opcodes = f'''
        {right_boolean_evaluation.opcodes}
        {left_boolean_evaluation.opcodes}

        {add_opcode} {value_name} {left_boolean_evaluation.value_id} {right_boolean_evaluation.value_id}
        '''

        return QuadCode(opcodes=opcodes, value_id=value_name)

class NumericOperationDIV(NumericBinaryOperation):
    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        adjusted_type = self.assign_type_adjusted_expressions(quad_translator)
        value_name = quad_translator.get_temp_variable_name(adjusted_type)

        left_boolean_evaluation = self.left_expression.translate(quad_translator)
        right_boolean_evaluation = self.right_expression.translate(quad_translator)

        add_opcode = 'IDIV' if (adjusted_type == 'int') else 'RDIV'
        opcodes = f'''
        {right_boolean_evaluation.opcodes}
        {left_boolean_evaluation.opcodes}

        {add_opcode} {value_name} {left_boolean_evaluation.value_id} {right_boolean_evaluation.value_id}
        '''

        return QuadCode(opcodes=opcodes, value_id=value_name)

class NumericOperationCast(QuadTranslatable):
    def __init__(self, numeric_expression: NumericExpression, target_type: str):
        self.target_type = target_type
        self.numeric_expression = numeric_expression

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        expression_evaluation_code = self.numeric_expression.translate(quad_translator)

        if quad_translator.get_variable_type(expression_evaluation_code.value_id) == self.target_type:
            return expression_evaluation_code

        cast_opcode = 'ITOR' if self.target_type == 'float' else 'RTOI'
        casted_expression_variable = quad_translator.get_temp_variable_name(self.target_type)

        opcodes = f'''
        {expression_evaluation_code.opcodes}
        {cast_opcode} {casted_expression_variable} {expression_evaluation_code.value_id}
        '''

        return QuadCode(opcodes=opcodes, value_id=casted_expression_variable)

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
    def __init__(self, value: Union['BooleanOperationNOT', 'BooleanRelationOperation']):
        self.value = value

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        return self.value.translate(quad_translator)

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

class BooleanOperationNOT(QuadTranslatable):
    def __init__(self, boolean_expression: BooleanExpression):
        self.boolean_expression = boolean_expression

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        boolean_value_name = quad_translator.get_temp_boolean_name()
        boolean_evaluation = self.boolean_expression.translate(quad_translator)

        opcodes = f'''
        {boolean_evaluation.opcodes}
        IEQL {boolean_value_name} {boolean_evaluation.value_id} 0
        '''

        return QuadCode(opcodes=opcodes, value_id=boolean_value_name)

class BooleanRelationOperation(NumericBinaryOperation):
    def __init__(self, left_expression: NumericExpression, right_expression: NumericExpression, relation_operation: str):
        super().__init__(left_expression, right_expression)
        self.relation_operation = relation_operation

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        self.assign_type_adjusted_expressions(quad_translator)
        evaluated_relop_variable = quad_translator.get_temp_boolean_name()

        left_expression_evaluation = self.left_expression.translate(quad_translator)
        right_expression_evaluation = self.right_expression.translate(quad_translator)

        expressions_type = quad_translator.get_variable_type(left_expression_evaluation.value_id)

        TYPE_TO_OPCODE_PREFIX = {
            'int': 'I',
            'float': 'R'
        }

        RELOP_TO_TYPELESS_OPCODE = {
            '<': 'LSS',
            '>': 'GRT',
            '==': 'EQL',
            '!=': 'NQL'
        }

        relop_opcode = TYPE_TO_OPCODE_PREFIX[expressions_type] + RELOP_TO_TYPELESS_OPCODE[self.relation_operation]

        opcodes = f'''
        {left_expression_evaluation.opcodes}
        {right_expression_evaluation.opcodes}
        {relop_opcode} {evaluated_relop_variable} {left_expression_evaluation.value_id} {right_expression_evaluation.value_id}
        '''

        return QuadCode(opcodes=opcodes, value_id=evaluated_relop_variable)
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
    def __init__(self, expression: NumericExpression):
        self.expression = expression

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        expression_evaluation_code = self.expression.translate(quad_translator)

        match quad_translator.get_variable_type(expression_evaluation_code.value_id):
            case 'int':
                return QuadCode(opcodes=f'{expression_evaluation_code.opcodes}\nIPRT {expression_evaluation_code.value_id}')

            case 'float':
                return QuadCode(opcodes=f'{expression_evaluation_code.opcodes}\nRPRT {expression_evaluation_code.value_id}')

class BreakStatement(Statement):
    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        raise NotImplementedError('Due to time constraints, the break statement is not implemented')

class AssignmentStatement(Statement):
    def __init__(self, id: str, expression: NumericExpression):
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

        return QuadCode(opcodes=f'{expression_evaluation_code.opcodes}\n{assignment_opcodes}', value_id=self.id)

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
    def __init__(self, expression: NumericExpression, conditional_cases: ConditionalCases, default_case: DefaultCase):
        self.expression = expression
        self.default_case = default_case
        self.conditional_cases = conditional_cases

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        boolean_name = quad_translator.get_temp_boolean_name()
        expression_evaluation_code = self.expression.translate(quad_translator)
        post_last_case_label_name = quad_translator.get_temp_label_name()

        if not expression_evaluation_code.value_id or quad_translator.get_variable_type(expression_evaluation_code.value_id) != 'int':
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

        compare_and_jump_case_opcodes = [
            f'''
            INQL {boolean_name} {expression_evaluation_code.value_id} {case_number}
            JMPZ {case_label} {boolean_name}
            '''
            for case_number, case_label in conditional_case_number_to_label.items()
        ]

        case_statements = '\n'.join(
            f'{label_name}: {conditional_case.statements.translate(quad_translator).opcodes}'
            for label_name, conditional_case
            in label_to_conditional_case.items()
        )

        opcodes = f'''
        {compare_and_jump_case_opcodes}

        {self.default_case.statements.translate(quad_translator).opcodes}
        JUMP {post_last_case_label_name}

        {case_statements}
        {post_last_case_label_name}:'''

        return QuadCode(opcodes=opcodes)
# END   statements #

# START AST #
class Program:
    def __init__(self, declarations: Declarations, statement_block: StatementBlock):
        self.declarations = declarations
        self.statement_block = statement_block

    def translate(self, quad_translator: QuadTranslator) -> QuadCode:
        for declaration in self.declarations.declarations:
            declaration.translate(quad_translator)

        return self.statement_block.translate(quad_translator)
# END   AST #
