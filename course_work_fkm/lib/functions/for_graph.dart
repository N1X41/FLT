import 'package:course_work_fkm/classes/equation.dart';
import 'package:course_work_fkm/classes/node.dart';
import 'package:course_work_fkm/classes/rule.dart';
import 'package:course_work_fkm/functions/vars_and_consts.dart';
import 'package:graphview/GraphView.dart';

/// Возврат графа решения
Graph? getOnlySolution(Graph graph) {
  if (graph.nodes[0].key!.value.isInSolution) {
    final Graph newGraph = Graph();
    int index = 0;
    while (index < graph.nodes.length - 1) {
      if (graph.nodes[index].key!.value.isInSolution) {
        newGraph.addNode(
            Node.Id(graph.nodes[index].key!.value.copy(isInSolution: true)));
        newGraph.nodes[newGraph.nodes.length - 1].key!.value.rule =
            graph.nodes[index].key!.value.rule;
        for (int child in graph.nodes[index].key!.value.children)
          if (graph.nodes[child].key!.value.isInSolution) {
            if (newGraph.nodes.length > 1)
              newGraph.addEdge(
                  newGraph.getNodeUsingId(
                      newGraph.nodes[newGraph.nodes.length - 2].key!.value),
                  newGraph.getNodeUsingId(
                      newGraph.nodes[newGraph.nodes.length - 1].key!.value));
            index = child;
          }
      }
    }
    newGraph.addNode(
        Node.Id(graph.nodes[index].key!.value.copy(isInSolution: true)));
    newGraph.nodes[newGraph.nodes.length - 1].key!.value.rule =
        graph.nodes[index].key!.value.rule;
    if (newGraph.nodes.length > 1)
      newGraph.addEdge(
          newGraph.getNodeUsingId(
              newGraph.nodes[newGraph.nodes.length - 2].key!.value),
          newGraph.getNodeUsingId(
              newGraph.nodes[newGraph.nodes.length - 1].key!.value));
    return newGraph;
  }
  return null;
}

/// Очистка графа
void clearGraph(Graph graph) {
  graph.nodes.clear();
  graph.edges.clear();
}

/// Решение графа
void solve(Graph graph, int index) {
  List<String> variables = [];
  List<String> constants = [];

  // Тестовое уловие
  if (graph.nodes[index].key!.value.depth > 5) return;

  // Если система решена - выходим
  if (graph.nodes[0].key!.value.isInSolution) return;

  // Если нашли решение - отмечаем успешную ветку и выходим
  if (isSolved(graph.nodes[index].key!.value.equations)) {
    makeIsInSolution(graph, index);
    return;
  }

  // Если неразрешима - заркываем ветку и выходим
  if (isFalseEquation(graph.nodes[index].key!.value.equations)) return;

  // Если уже есть идентичное решение - закрываем ветку
  if (isAlreadyExist(graph, index)) return;

  // Получаем актальный список переменных и констант
  getVarsAndConstsFromList(
      graph.nodes[index].key!.value.equations, variables, constants);

  for (Rule rule in getAllRules(
      graph.nodes[0].key!.value.equations, variables, constants)) {
    if (!graph.nodes[0].key!.value.isInSolution) {
      createNodeByRule(graph, index, rule);
      solve(graph, graph.nodes.length - 1);
    }
  }
}

/// Отметка разрешенной ветки
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

/// Проверка на наличие идентичного узла
bool isAlreadyExist(Graph graph, int index) {
  if (index == 0) return false;
  for (int i = 0; i < graph.nodes.length; i++) {
    bool result = true;
    if (i != index) {
      if (graph.nodes[index].key!.value.equations.length ==
          graph.nodes[i].key!.value.equations.length) {
        for (int j = 0; j < graph.nodes[index].key!.value.equations.length; j++)
          if (result &&
              graph.nodes[index].key!.value.equations[j] !=
                  graph.nodes[i].key!.value.equations[j]) result = false;
      } else
        result = false;
    } else
      result = false;
    if (result) return true;
  }
  return false;
}

/// Выбор правила для преобразования
List<Rule> getAllRules(
    List<Equation> equations, List<String> variables, List<String> constants) {
  List<Rule> rules = [];
  // Для каждой переменной создаем список по уровню ликвидности
  for (String vr in variables) {
    // Добавляем пустой переход
    rules.add(Rule(variable: vr, rule: ''));
    for (String constant in constants) {
      // Создаем два листа - префиксные/суффиксные переходы, и "необоснованные"
      List<Rule> effective = [];
      List<Rule> nonEffective = [];
      // Проверка наличия переменной - константы на префиксах/суффиксах
      if (isPrefix(equations, vr, constant) ||
          isSuffix(equations, vr, constant)) {
        if (isPrefix(equations, vr, constant))
          effective.add(Rule(variable: vr, rule: constant + vr));
        if (isSuffix(equations, vr, constant))
          effective.add(Rule(variable: vr, rule: vr + constant));
      } else {
        nonEffective.add(Rule(variable: vr, rule: constant + vr));
        nonEffective.add(Rule(variable: vr, rule: vr + constant));
      }
      rules.addAll(effective);
      rules.addAll(nonEffective);
    }
  }
  return rules;
}

/// Проверка на префикс
bool isPrefix(List<Equation> equations, String variable, String constant) {
  for (Equation equation in equations) {
    if ((variable == equation.left[0] && constant == equation.right[0]) ||
        (variable == equation.right[0] && constant == equation.left[0]))
      return true;
  }
  return false;
}

/// Проверка на суффикс
bool isSuffix(List<Equation> equations, String variable, String constant) {
  for (Equation equation in equations) {
    if ((variable == equation.left[equation.left.length - 1] &&
            constant == equation.right[equation.right.length - 1]) ||
        (variable == equation.right[equation.right.length - 1] &&
            constant == equation.left[equation.left.length - 1])) return true;
  }
  return false;
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

    // Сокращаем уравнение слева и справа (убираем константы до длины строки в 1 символ)
    equation.simplify();

    // Разбиваем уравнение
    List<Equation> equations = equation.divide();

    // Проверяем, что нет идентичного уравнения
    for (Equation equat in equations) {
      if (newNode.equations.every((eq) => eq != equat) &&
          equat.left + equat.right != '') newNode.equations.add(equat);
    }
  }

  newNode.equations.sort(
    (a, b) {
      return (a.left + a.right).compareTo(b.left + b.right);
    },
  );

  newNode.parent = index;
  newNode.rule = rule;
  newNode.depth++;

  graph.nodes[index].key!.value.children.add(graph.nodes.length);

  graph.addNode(Node.Id(newNode));
  graph.addEdge(graph.getNodeUsingId(graph.nodes[index].key!.value),
      graph.getNodeUsingId(graph.nodes[graph.nodes.length - 1].key!.value));
}
