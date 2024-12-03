import 'package:course_work_fkm/classes/equation.dart';

bool isVar (String char){
  return char.toLowerCase() == char;
}

bool isConst (String char){
  return char.toUpperCase() == char;
}

void getVarsAndConstsFromList(
    List<Equation> equations, List<String> variables, List<String> constants) {
  variables.clear();
  constants.clear();
  for (Equation equation in equations) {
    String value = equation.left + equation.right;

    // Проходим по каждому символу в строке
    for (int i = 0; i < value.length; i++) {
      String char = value[i];

      // Проверяем, является ли символ буквой
      if (RegExp(r'[a-zA-Z]').hasMatch(char)) {
        if (char == char.toLowerCase()) {
          // Если строчный символ и его нет в _variables, добавляем
          if (!variables.contains(char)) {
            variables.add(char);
            variables.sort();
          }
        } else if (char == char.toUpperCase()) {
          // Если заглавный символ и его нет в _constants, добавляем
          if (!constants.contains(char)) {
            constants.add(char);
            constants.sort();
          }
        }
      }
    }
  }
}
