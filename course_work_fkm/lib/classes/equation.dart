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
  bool operator ==(Object other) {
    // Проверяем, является ли other экземпляром Equation
    if (other is! Equation) return false;

    // Сравниваем left и right
    return left == other.left && right == other.right;
  }

  /// Уравнение решено
  bool isSolved() {
    return left == right;
  }

  /// Уравнение неразрешимо
  bool isFalse() {
    return ((left.length != right.length && left.length * right.length == 0) ||
        (left[0].toLowerCase() != left[0] &&
            right[0].toLowerCase() != right[0] &&
            left[0] != right[0]) ||
        (left[left.length - 1].toLowerCase() != left[left.length - 1] &&
            right[right.length - 1].toLowerCase() != right[right.length - 1] &&
            left[left.length - 1] != right[right.length - 1]));
  }

  Equation copy() {
    return Equation(left: left, right: right);
  }

  /// Сокращение констант
  void simplify() {
    // Убираем одинаковые символы с начала
    while (left.isNotEmpty && right.isNotEmpty && 
           left[0] == right[0] && 
           left[0].toUpperCase() == left[0]) {
      left = left.substring(1);
      right = right.substring(1);
    }

    // Убираем одинаковые символы с конца
    while (left.isNotEmpty && right.isNotEmpty && 
           left[left.length - 1] == right[right.length - 1] && 
           left[left.length - 1].toUpperCase() == left[left.length - 1]) {
      left = left.substring(0, left.length - 1);
      right = right.substring(0, right.length - 1);
    }
  }
}
