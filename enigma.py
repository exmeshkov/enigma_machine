class Enigma:
    __rotors_dictionary = {
        1: ('AELTPHQXRU', 'BKNW', 'CMOY', 'DFG', 'IV', 'JZ', 'S'),
        2: ('FIXVYOMW', 'CDKLHUP', 'ESZ', 'BJ', 'GR', 'NT', 'A', 'Q'),
        3: ('ABDHPEJT', 'CFLVMZOYQIRWUKXSG', 'N')
    }
    __reflector_dictionary = {
        1: [('AY'), ('BR'), ('CU'), ('DH'), ('EQ'), ('FS'), ('GL'), ('IP'), ('JX'), ('KN'), ('MO'), ('TZ'), ('VW')]
    }
    __alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    __shift_rots = {1: 17, 2: 5, 3: 22}

    def __init__(self, text, reflector, rot1, shift1, rot2, shift2, rot3, shift3, pairs=''):
        self.text = ''
        for i in text.upper():
            if i in self.__alphabet:
                self.text += i
        self.reflector = reflector
        self.rots = [rot1, rot2, rot3]
        self.shifts = [shift1, shift2, shift3]
        self.pairs = pairs.upper()
        self.position_before_shift2 = False
        self.shift2_status = False

    def __rotor(self, symbol, n, reverse=False):
        if reverse:
            flag = -1
        else:
            flag = 1
        for j in self.__rotors_dictionary[n]:
            if symbol in j:
                return j[(j.index(symbol) + flag) % len(j)]

    def __caesar(self, symbol, rot, flag):
        if rot == 1:
            shift = self.shifts[0] - self.shifts[1]
        elif rot == 2:
            shift = self.shifts[1] - self.shifts[2]
        elif rot == 3:
            shift = self.shifts[2]
        else:
            shift = self.shifts[0]
        return self.__alphabet[(self.__alphabet.index(symbol) + shift * flag) % len(self.__alphabet)]

    def __reflector(self, symbol, n):
        if n == 0:
            return symbol
        for j in self.__reflector_dictionary[n]:
            if symbol in j:
                if j.index(symbol) == 0:
                    return j[1]
                else:
                    return j[0]

    def __shift_rotor(self):
        self.shifts[2] = (self.shifts[2] + 1) % 26
        if self.position_before_shift2:
            self.shifts[1] = (self.shifts[1] + 1) % 26
            self.position_before_shift2 = False
        if self.shifts[2] == self.__shift_rots[self.rots[2]]:
            self.shifts[1] = (self.shifts[1] + 1) % 26
            self.shift2_status = False
        if self.shifts[1] == self.__shift_rots[self.rots[1]] and not self.shift2_status:
            self.shifts[0] = (self.shifts[0] + 1) % 26
            self.shift2_status = True
        elif self.shifts[1] == self.__shift_rots[self.rots[1]] - 1:
            self.position_before_shift2 = True

    def encrypt(self):
        encrypted_text = ''
        for symbol in self.text:
            self.__shift_rotor()

            for rot in (3, 2, 1):
                symbol = self.__rotor(self.__caesar(symbol, rot, 1), self.rots[rot - 1])

            symbol = self.__caesar(self.__reflector(self.__caesar(symbol, 0, -1), self.reflector), 0, 1)

            for rot in (1, 2, 3):
                symbol = self.__caesar(self.__rotor(symbol, self.rots[rot - 1], reverse=True), rot, -1)

            encrypted_text += symbol
        return encrypted_text


def enigma(text, ref, rot1, shift1, rot2, shift2, rot3, shift3):
    e = Enigma(text, ref, rot1, shift1, rot2, shift2, rot3, shift3)
    return e.encrypt()


