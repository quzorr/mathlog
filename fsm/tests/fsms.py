# Пример FSM_1 (четное число букв "a")
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
