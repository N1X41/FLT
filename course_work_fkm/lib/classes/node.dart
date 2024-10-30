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

  // Конструктор класса Node
  MyNode({
    required this.equations,
    int? parent,
    Rule? rule,
    List<int>? children,
    this.isInSolution = false,
  }) : children = children ?? [];

  String getNodeText() {
    String text = '';

    for (Equation equation in equations) {
      if (equation.left != '') {
        text = '$text\n${equation.left} = ${equation.right}';
      }
    }

    return text.substring(1);
  }

  // Метод для создания копии узла
  MyNode copy() {
    return MyNode(
      equations: equations,
      parent: parent,
      rule: rule,
    );
  }
}