from fsm.graph_vis.graph_visualization import visualize_fsm
from fsm.run.fsm_check import fsm_accepts, is_determined
from fsm.tests.fsms import fsm_1, fsm_2

if __name__ == '__main__':
    # Пример FSM_1 (четное число букв "a")
    # Визуализация
    visualize_fsm(fsm_1, file_name='fsm_1')

    # Проверка на детерминированность
    print(f'FSM_1 is_determined?: {is_determined(fsm_1)}')

    # Проверка строки с помощью автомата
    input_string_1 = "aaab"
    result = fsm_accepts(fsm_1, input_string_1)
    print(f"Input string '{input_string_1}' for FSM_1 is : {result}")

    # Пример FSM_2 (букв "b" не больше трех)
    # Визуализация
    visualize_fsm(fsm_2, file_name='fsm_2')

    # Проверка на детерминированность
    print(f'FSM_2 is_determined?: {is_determined(fsm_2)}')

    # Проверка строки с помощью автомата
    input_string_2 = "abbbbbbaaaaa"
    result = fsm_accepts(fsm_2, input_string_2)
    print(f"Input string '{input_string_2}' for FSM_2 is : {result}")
