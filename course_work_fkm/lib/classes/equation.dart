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

  bool isSolved() {
    return left == right;
  }

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
}
