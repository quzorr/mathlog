def fsm_check_word(fsm: dict, input_str: str) -> bool:
    current_state = fsm['start']

    for symbol in input_str:
        if symbol in fsm['transitions'][current_state]:
            current_state = fsm['transitions'][current_state][symbol]
        else:
            return False

    return current_state in fsm['finals']


def is_determined(fsm: dict) -> bool:
    for state in fsm['states']:
        for symbol in fsm['alphabet']:
            if fsm['transitions'][state].get(symbol, None) is None:
                return False

    return True


def is_correct(fsm: dict) -> bool:
    pass


def determine(fsm: dict) -> dict:
    pass


if __name__ == '__main__':
    # Пример FSM_1 (букв "a" четное число)
    fsm_1 = {
        'alphabet': ['a', 'b'],
        'states': ['q0', 'q1'],
        'transitions': {
            'q0': {'a': 'q1', 'b': 'q0'},
            'q1': {'a': 'q0', 'b': 'q1'},
        },
        'start': 'q0',
        'finals': ['q0']
    }
    print(f'FSM_1 is determined?: {is_determined(fsm_1)}')

    input_string_1 = "aab"
    result = fsm_check_word(fsm_1, input_string_1)
    print(f"Input string '{input_string_1}' for FSM_1 is : {result}")

    # Пример FSM_2 (букв "b" не больше трех)
    fsm_2 = {
        'alphabet': ['a', 'b'],
        'states': ['q0', 'q1', 'q2', 'q3', 'q4'],
        'transitions': {
            'q0': {'a': 'q0', 'b': 'q1'},
            'q1': {'a': 'q1', 'b': 'q2'},
            'q2': {'a': 'q2', 'b': 'q3'},
            'q3': {'a': 'q3', 'b': 'q4'},
            'q4': {'a': 'q4', 'b': 'q4'},
        },
        'start': 'q0',
        'finals': ['q0', 'q1', 'q2', 'q3']
    }
    print(f'FSM_2 is determined?: {is_determined(fsm_2)}')

    input_string_2 = "abbbbbbaaaaa"
    result = fsm_check_word(fsm_2, input_string_2)
    print(f"Input string '{input_string_2}' for FSM_2 is : {result}")
