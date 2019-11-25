"""

This module provides implementations of the finite-state machines
(regular grammars) used by the filter programs.

"""

def dialogue_state_machine(state, line_no, word):
    if state == 'default':
        if word == '“':
            return 'dialogue'
        elif word == '”':
            raise ValueError("Missing open quote, line {}".format(line_no))
        elif word == '"':
            raise ValueError("Found straight quote, line {}".format(line_no))
        elif word == '(':
            return 'parenthetical'
        elif word == ')':
            raise ValueError("Missing open paren, line {}".format(line_no))
        else:
            return state
    elif state == 'dialogue':
        if word == '”':
            return 'default'
        elif word == '“':
            raise ValueError("Nested close quote, line {}".format(line_no))
        elif word == '¶':
            raise ValueError("Found paragraph break inside quotes, line {}".format(line_no))
        elif word == '"':
            raise ValueError("Found straight quote, line {}".format(line_no))
        elif word == '(':
            return 'parenthetical-dialogue'
        elif word == ')':
            raise ValueError("Missing open paren, line {}".format(line_no))
        else:
            return state
    elif state == 'parenthetical':
        if word in ('“', '”', '"'):
            raise ValueError("Found quote in parentheses, line {}".format(line_no))
        elif word == '¶':
            raise ValueError("Found paragraph break inside parentheses, line {}".format(line_no))
        elif word == ')':
            return 'default'
        else:
            return state
    elif state == 'parenthetical-dialogue':
        if word in ('“', '”', '"'):
            raise ValueError("Found quote in parentheses, line {}".format(line_no))
        elif word == '¶':
            raise ValueError("Found paragraph break inside parentheses, line {}".format(line_no))
        elif word == ')':
            return 'dialogue'
        else:
            return state
    else:
        raise NotImplementedError


def null_state_machine(state, line_no, word):
    return state


STATE_MACHINES = {
    'dialogue': dialogue_state_machine,
    'none': null_state_machine,
}