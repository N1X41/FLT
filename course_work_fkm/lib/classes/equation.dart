import 'package:course_work_fkm/functions/vars_and_consts.dart';

class Equation {
  /// Уравнение слева
  String left;

  /// Уравнение справа
  String right;

  // Конструктор класса Equation
  Equation({
    required this.left,
    required this.right,
  });

  @override
  String toString() {
    return left + ' = ' + right;
  }

  @override
  bool operator ==(Object other) {
    // Проверяем, является ли other экземпляром Equation
    if (other is! Equation) return false;

    // Сравниваем left и right
    return ((left == other.left && right == other.right) || (left == other.right && right == other.left));
  }

  /// Уравнение решено
  bool isSolved() {
    return left == right;
  }

  /// Уравнение неразрешимо
  bool isFalse() {
    return (((left.length == 0) ^ (right.length == 0)) ||
      (left.length != right.length && left.length * right.length == 0) ||
        (isConst(left[0]) && isConst(right[0]) && left[0] != right[0]) ||
        (isConst(left[left.length - 1]) && isConst(right[right.length - 1]) &&
            left[left.length - 1] != right[right.length - 1]));
  }

  Equation copy() {
    return Equation(left: left, right: right);
  }

  /// Сокращение переменных и констант
  void simplify() {
    // Убираем одинаковые символы с начала
    while (left.length > 1 && right.length > 1 && left[0] == right[0]) {
      left = left.substring(1);
      right = right.substring(1);
    }

    // Убираем одинаковые символы с конца
    while (left.length > 1 && right.length > 1 && left[left.length - 1] == right[right.length - 1]) {
      left = left.substring(0, left.length - 1);
      right = right.substring(0, right.length - 1);
    }
  }

  /// Функция для получения списка объектов Equation путем разбиения исходного уравнения
  List<Equation> divide() {
    List<Equation> result = [];
    int minLength = left.length < right.length ? left.length : right.length;

    // Рекурсивное разбиение
    if (minLength > 1)
      for (int i = 1; i < minLength; i++) {
        String leftSub = left.substring(0, i);
        String rightSub = right.substring(0, i);
        // Проверяем, равны ли подстроки по набору символов
        if ((leftSub.split('')..sort()).toString() == (rightSub.split('')..sort()).toString() ||
          (leftSub.length == rightSub.length && 
          (leftSub.split('').where((char) => isVar(char)).toList()..sort()).toString() == 
          (rightSub.split('').where((char) => isVar(char)).toList()..sort()).toString())) {
          result.add(Equation(left: leftSub, right: rightSub));
          result.addAll(Equation(left: left.substring(i, left.length), right: right.substring(i, right.length)).divide());
          return result;
        }
      }
    
    return [this];
  }
}
