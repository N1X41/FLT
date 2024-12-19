import 'package:course_work_fkm/classes/equation.dart';
import 'package:course_work_fkm/classes/rule.dart';

class MyNode {
  /// Список уравнений
  List<Equation> equations;

  /// Индекс родительского узла
  int? parent;

  /// Правило переписывания
  Rule? rule;

  /// Список индексов дочерних узлов
  List<int> children;

  /// Является ли узел частью ветки решения
  bool isInSolution;

  /// Глубина развертки
  int depth;

  /// Причина закрытия ветки
  /// 0 - Узел не конечный
  /// 1 - Логическая ошибка
  /// 2 - Повторение узла
  /// 3 - Превышение глубины погружения
  int error_code;

  // Конструктор класса Node
  MyNode({
    required this.equations,
    required this.depth,
    int? parent,
    Rule? rule,
    List<int>? children,
    this.error_code = 0,
    this.isInSolution = false,
  }) : children = children ?? [];

  String getNodeText() {
    String text = '';

    for (Equation equation in equations) {
      if (equation.left != '') {
        text = '$text\n${equation.left} = ${equation.right}';
      }
    }

    return text != '' ? text.substring(1) : '';
  }

  // Метод для создания копии узла
  MyNode copy({bool? isInSolution}) {
    return MyNode(
      equations: equations,
      parent: parent,
      rule: rule,
      depth: depth,
      isInSolution: isInSolution ?? false,
      error_code: 0,
    );
  }
}
