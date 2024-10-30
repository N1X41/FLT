import 'package:course_work_fkm/classes/equation.dart';
import 'package:course_work_fkm/classes/node.dart';
import 'package:course_work_fkm/classes/rule.dart';
import 'package:course_work_fkm/functions/vars_and_consts.dart';
import 'package:graphview/GraphView.dart';

void clearGraph(Graph graph) {
  graph.nodes.clear();
  graph.edges.clear();
}

solve(Graph graph, int index) {
  List<String> variables = [];
  List<String> constants = [];
  Rule rule = Rule(variable: '', rule: '');

  // Тестовое уловие
  if (index > 10) return;

  // Если система решена - выходим
  if (graph.nodes[0].key!.value.isInSolution) return;

  // Если нашли решение - отмечаем успешную ветку и выходим
  if (isSolved(graph.nodes[index].key!.value.equations)) {
    makeIsInSolution(graph, index);
    return;
  }

  // Если неразрешима - заркываем ветку и выходим
  if (isFalseEquation(graph.nodes[index].key!.value.equations)) return;

  // Получаем актальный список переменных и констант
  getVarsAndConstsFromList(
      graph.nodes[0].key!.value.equations, variables, constants);

  // Получаем правило из преф/суфф, иначе первую из списка
  rule = chooseVarForRule(
          graph.nodes[0].key!.value.equations, variables, constants) ??
      Rule(variable: variables[0], rule: variables[0] + constants[0]);

  // Создаем узел с переходом в Е и запускаем его решение
  createNodeByRule(graph, index, Rule(variable: rule.variable, rule: ''));
  solve(graph, graph.nodes.length - 1);

  // Создаем узел на основе правила преобразования и запускаем его решение
  createNodeByRule(graph, index, rule);
  solve(graph, graph.nodes.length - 1);
}

void makeIsInSolution(Graph graph, int index) {
  graph.nodes[index].key!.value.isInSolution = true;
  if (graph.nodes[index].key!.value.parent != null) {
    makeIsInSolution(graph, graph.nodes[index].key!.value.parent);
  }
}

/// Проверка разрешимости системы
bool isSolved(List<Equation> equations) {
  for (Equation equation in equations) {
    if (!equation.isSolved()) return false;
  }
  return true;
}

/// Проверка ложности
bool isFalseEquation(List<Equation> equations) {
  for (Equation equation in equations) {
    if (equation.isFalse()) return true;
  }
  return false;
}

/// Выбор правила для преобразования
Rule? chooseVarForRule(
    List<Equation> equations, List<String> variables, List<String> constants) {
  for (Equation equation in equations) {
    // Проверка наличия переменной - константы на префиксах
    if ((variables.contains(equation.left[0]) &&
            constants.contains(equation.right[0])) ||
        (variables.contains(equation.right[0]) &&
            constants.contains(equation.left[0]))) {
      if (variables.contains(equation.left[0])) {
        return Rule(
            variable: equation.left[0],
            rule: equation.right[0] + equation.left[0]);
      } else {
        return Rule(
            variable: equation.right[0],
            rule: equation.left[0] + equation.right[0]);
      }
      // Проверка наличия переменной - константы на суффиксах
    } else if ((variables.contains(equation.left[equation.left.length - 1]) &&
            constants.contains(equation.right[equation.right.length - 1])) ||
        (variables.contains(equation.right[equation.right.length - 1]) &&
            constants.contains(equation.left[equation.left.length - 1]))) {
      if (variables.contains(equation.left[equation.left.length - 1])) {
        return Rule(
            variable: equation.left[equation.left.length - 1],
            rule: equation.right[equation.right.length - 1] +
                equation.left[equation.left.length - 1]);
      } else {
        return Rule(
            variable: equation.right[equation.right.length - 1],
            rule: equation.left[equation.left.length - 1] +
                equation.right[equation.right.length - 1]);
      }
    }
  }
  return null;
}

/// Создание нового узла
void createNodeByRule(Graph graph, int index, Rule rule) {
  MyNode newNode = graph.nodes[index].key!.value.copy();

  newNode.equations = [];
  for (int i = 0; i < graph.nodes[index].key!.value.equations.length; i++) {
    Equation equation = Equation(
        left: graph.nodes[index].key!.value.equations[i].left
            .replaceAll(rule.variable, rule.rule),
        right: graph.nodes[index].key!.value.equations[i].right
            .replaceAll(rule.variable, rule.rule));
    newNode.equations.add(equation);
  }

  newNode.parent = index;
  newNode.rule = rule;

  graph.nodes[index].key!.value.children.add(graph.nodes.length);

  graph.addNode(Node.Id(newNode));
  graph.addEdge(graph.getNodeUsingId(graph.nodes[index].key!.value),
      graph.getNodeUsingId(graph.nodes[graph.nodes.length - 1].key!.value));
}
