from graphviz import Digraph


def visualize_fsm(fsm: dict, file_name: str):
    fsm_graph = Digraph(filename=file_name, format='pdf')

    # Создаем все состояния, если оно финишное, то добавляем двойной круг
    for state in fsm['states']:
        if state in fsm['finals']:
            fsm_graph.node(state, state, shape='doublecircle')
        else:
            fsm_graph.node(state, state)

    # Добавляем начальное состояние со стрелочкой
    fsm_graph.node('', '', shape='plaintext')
    fsm_graph.edge('', fsm['start'])

    # Добавляем переходы
    for state, transitions in fsm['transitions'].items():
        for input_char, next_state in transitions.items():
            fsm_graph.edge(state, next_state, label=input_char)

    fsm_graph.view()


if __name__ == '__main__':
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

    # Визуализация
    visualize_fsm(fsm_1, file_name='fsm_1')
