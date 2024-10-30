import 'package:course_work_fkm/classes/equation.dart';

Equation createEquation(String equation) {
  return Equation(
      left: equation.replaceAll(' ', '').split('=')[0],
      right: equation.replaceAll(' ', '').split('=')[1]);
}
