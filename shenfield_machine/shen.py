class Shenfield:
    def __init__(self, tape, tape_size=20):
        self.tape = tape
        self.tape.extend([0 for _ in range(tape_size)])
        self.current_step = 1

    def inc(self, index):
        self.tape[index] += 1
        self.current_step += 1

    def dec(self, index_1, index_2):
        if self.tape[index_1] <= 0:
            self.current_step += 1
            return

        self.tape[index_1] -= 1
        self.current_step = index_2

    def run(self, prog):
        print(f'\nStart tape: {self.tape}')
        while self.current_step <= len(prog):
            command, *args = prog[self.current_step - 1]
            getattr(self, command)(*args)

        print(f'Finish tape: {self.tape}\n')


if __name__ == '__main__':
    # Example 1
    # f_1(x, y) = x + y
    prog_1 = [
        ('inc', 0),
        ('dec', 1, 1),
        ('dec', 2, 1),
        ('dec', 0, 5),
    ]
    machine_1 = Shenfield([0, 18, 3])  # Инициализация ленты машины
    machine_1.run(prog_1)  # Запуск машины

    # Example 2
    machine_1 = Shenfield([0, 16, 7])
    machine_1.run(prog_1)

    # Example 3
    # f_2(x, y) = x '-' y (верхняя разность)
    prog_2 = [
        ('inc', 0),
        ('dec', 1, 1),
        ('dec', 0, 4),
        ('dec', 2, 3),
    ]
    machine_2 = Shenfield([0, 16, 7])
    machine_2.run(prog_2)

    # Example 4
    machine_2 = Shenfield([0, 7, 16])
    machine_2.run(prog_2)

    # Example 3
    # copy(x, y, buffer) макрос copy
    # Пример x=1, y=0, buffer=2
    prog_3 = [
        ('inc', 0),
        ('inc', 2),
        ('dec', 1, 1),
        ('dec', 0, 5),
        ('inc', 1),
        ('dec', 2, 5),
        ('dec', 1, 8),
        ('dec', 1, 10),
    ]
    machine_3 = Shenfield([0, 16])
    machine_3.run(prog_3)
