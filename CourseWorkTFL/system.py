class System:
    def __init__(self, system):
        self.system = system

    def make_string_system(self):
        return sorted([sorted((eq[0].make_string(), eq[1].make_string())) for eq in self.system])

    def print_system(self):
        result = ""
        for eq in [(eq[0].make_string(), eq[1].make_string()) for eq in self.system]:
            for left in eq[0]:
                result += left
            result += " = "
            for right in eq[1]:
                result += right
            result += '\n'
        return result
