import 'package:course_work_fkm/classes/equation.dart';
import 'package:course_work_fkm/classes/rule.dart';
import 'package:course_work_fkm/functions/vars_and_consts.dart';

/// Создает объект класса Equation из строки UI
Equation createEquation(String equation) {
  return Equation(
      left: equation.replaceAll(' ', '').split('=')[0],
      right: equation.replaceAll(' ', '').split('=')[1]);
}

/// Проведение подстановок в системе уравнений
(List<Equation>, bool, Rule?) makeSubstitution(List<Equation> equations){
  List<Equation> newEquations = [];

  // Если уравнений нет/одно - вернуть список
  if (equations.length <= 1) return (equations, false, null);

  // Проверка на наличие нулевых подстановок (x = ABA|_)
  for (int i = 0; i < equations.length; i++){
    if (equations[i].right.length == 1 && isVar(equations[i].right[0]) && equations[i].left != equations[i].right) {
      for (int j = 0; j < equations.length; j++) {
        if (j != i) {
          Equation newEquation = Equation(
            left: equations[j].left.replaceAll(equations[i].right[0], equations[i].left),
            right: equations[j].right.replaceAll(equations[i].right[0], equations[i].left)
          );
          newEquation.simplify();
          newEquations.add(newEquation);
        } 
        // else if (equations[i].left != '') {
        //     newEquations.add(equations[i]);
        // }
      }
      return (newEquations, true, Rule(variable: equations[i].right[0], rule: equations[i].left));
    }
    else if (equations[i].left.length == 1 && isVar(equations[i].left[0]) && equations[i].left != equations[i].right) {
      for (int j = 0; j < equations.length; j++) {
        if (j != i) {
          Equation newEquation = Equation(
            left: equations[j].left.replaceAll(equations[i].left[0], equations[i].right),
            right: equations[j].right.replaceAll(equations[i].left[0], equations[i].right),
          );
          newEquation.simplify();
          newEquations.add(newEquation);
        } 
        // else if (equations[i].right != '') {
        //     newEquations.add(equations[i]);
        // }
      }
      return (newEquations, true, Rule(variable: equations[i].left[0], rule: equations[i].right));
    }
  }
  
  // Подстановка с максимальным сокращением длины
  // Map<Equation, int> substitution = _lengthReduction(equations);

  // Подстановка с максимальным сокращением после упрощения
  Map<Rule, int> substitution = _lengthReductionBySimplify(equations);
  
  
  // Ищем самую выгодную подстановку и проводим ее (для метрики упрощения длины)
  // if (substitution.isNotEmpty) {
  //   Equation maxBenefit = substitution.entries.reduce((a, b) => a.value > b.value ? a : b).key;

  //   for (Equation eq in equations)
  //     if (eq != maxBenefit){
  //       Equation newEquation = Equation(
  //         left: eq.left.replaceAll(
  //           maxBenefit.left.length >= maxBenefit.right.length ? maxBenefit.left : maxBenefit.right,
  //           maxBenefit.left.length < maxBenefit.right.length ? maxBenefit.left : maxBenefit.right
  //         ),
  //         right: eq.right.replaceAll(
  //           maxBenefit.left.length >= maxBenefit.right.length ? maxBenefit.left : maxBenefit.right,
  //           maxBenefit.left.length < maxBenefit.right.length ? maxBenefit.left : maxBenefit.right
  //         )
  //       );
  //       newEquation.simplify();
  //       newEquations.add(newEquation);
  //     } else {
  //       eq.simplify();
  //       newEquations.add(eq);
  //     }
  //   return (newEquations, true, Rule(variable: maxBenefit.left, rule: maxBenefit.right));
  // } else {
  //   return (equations, false, null);
  // }

  // Ищем самую выгодную подстановку и проводим ее (для метрики сокращения)
  if (substitution.isNotEmpty) {
    Rule maxBenefit = substitution.entries.reduce((a, b) => a.value > b.value ? a : b).key;

    for (Equation eq in equations)
      if (eq != maxBenefit){
        Equation newEquation = Equation(
          left: eq.left.replaceAll(
            maxBenefit.variable,
            maxBenefit.rule
          ),
          right: eq.right.replaceAll(
            maxBenefit.variable,
            maxBenefit.rule
          )
        );
        newEquation.simplify();
        newEquations.add(newEquation);
      } else {
        eq.simplify();
        newEquations.add(eq);
      }
    return (newEquations, true, maxBenefit);
  } else {
    return (equations, false, null);
  }
}

/// Проверка на наличие переменных в строке
bool _hasVars(String part){
  for (String char in part.split('')){
    if (isVar(char)) return true;
  }
  return false;
}

/// Количество вхождений подстроки
int _containsCount(String part, String substring){
  return (part.length - part.replaceAll(substring, '').length) ~/ substring.length;
}

// Поиск сокращений длины
Map<Equation, int> _lengthReduction(List<Equation> equations) {
  Map<Equation, int> substitution = {};
  for (int i = 0; i < equations.length; i++) {
    if (equations[i].left != equations[i].right) {
      if (equations[i].left.length > equations[i].right.length && _hasVars(equations[i].left)) {
        for (int j = 0; j < equations.length; j++) {
          if (equations[j].toString().contains(equations[i].left) && j != i) {
            if (!substitution.containsKey(equations[i])){
              substitution.addAll({equations[i]: _containsCount(equations[j].toString(), equations[i].left)});
            } else {
              substitution[equations[i]] = _containsCount(equations[j].toString(), equations[i].left) + substitution[equations[i]]!;
            }
          }
        }
      } else if (_hasVars(equations[i].right)) {
        for (int j = 0; j < equations.length; j++) {
          if (equations[j].toString().contains(equations[i].right) && j != i) {
            if (!substitution.containsKey(equations[i])) {
              substitution.addAll({equations[i]: _containsCount(equations[j].toString(), equations[i].right)});
            } else {
              substitution[equations[i]] = _containsCount(equations[j].toString(), equations[i].right) + substitution[equations[i]]!;
            }
          }
        }
      }
    }
  }
  return substitution;
}

// Поиск сокращений после упрощения
Map<Rule, int> _lengthReductionBySimplify(List<Equation> equations) {
  Map<Rule, int> substitution = {};
  for (int i = 0; i < equations.length; i++) {
    if (equations[i].left != equations[i].right) {
      if (_hasVars(equations[i].left) && equations[i].left != equations[i].right) {
        for (int j = 0; j < equations.length; j++) {
          if (equations[j].toString().contains(equations[i].left) && j != i) {
            if (!substitution.containsKey(equations[i])){
              Equation newEquation = Equation(
                  left: equations[j].left.replaceAll(equations[i].left, equations[i].right),
                  right: equations[j].right.replaceAll(equations[i].left, equations[i].right)
                );
              newEquation.simplify();
              substitution.addAll({Rule(variable: equations[i].left, rule: equations[i].right): 
                equations[j].toString().length - newEquation.toString().length});
            } else {
              Equation newEquation = Equation(
                  left: equations[j].left.replaceAll(equations[i].left, equations[i].right),
                  right: equations[j].right.replaceAll(equations[i].left, equations[i].right)
                );
              newEquation.simplify();
              substitution[Rule(variable: equations[i].left, rule: equations[i].right)] = substitution[equations[i]]!
               + equations[j].toString().length - newEquation.toString().length;
            }
          }
        }
      } 
      if (_hasVars(equations[i].right) && equations[i].left != equations[i].right) {
        for (int j = 0; j < equations.length; j++) {
          if (equations[j].toString().contains(equations[i].right) && j != i) {
            if (!substitution.containsKey(equations[i])) {
              Equation newEquation = Equation(
                left: equations[j].left.replaceAll(equations[i].right, equations[i].left),
                right: equations[j].right.replaceAll(equations[i].right, equations[i].left)
              );
              newEquation.simplify();
              substitution.addAll({Rule(variable: equations[i].right, rule: equations[i].left): 
                equations[j].toString().length - newEquation.toString().length});
            } else {
              Equation newEquation = Equation(
                left: equations[j].left.replaceAll(equations[i].right, equations[i].left),
                right: equations[j].right.replaceAll(equations[i].right, equations[i].left)
              );
              newEquation.simplify();
              substitution[Rule(variable: equations[i].right, rule: equations[i].left)] = substitution[equations[i]]!
                + equations[j].toString().length - newEquation.toString().length;
            }
          }
        }
      }
    }
  }
  return substitution;
}