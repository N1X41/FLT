import 'package:course_work_fkm/classes/node.dart';
import 'package:course_work_fkm/functions/for_graph.dart';
import 'package:course_work_fkm/functions/for_nodes.dart';
import 'package:course_work_fkm/functions/vars_and_consts.dart';
import 'package:course_work_fkm/widgets/const_box.dart';
import 'package:course_work_fkm/widgets/var_box.dart';
import 'package:flutter/material.dart';
import 'package:graphview/GraphView.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(
          title: 'Поиск разрешимости системы строковых уравнений'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final List<GlobalKey<FormState>> _formKeys = [GlobalKey<FormState>()];
  final List<TextEditingController> _controllers = [TextEditingController()];
  final List<String> _variables = [];
  final List<String> _constants = [];

  bool _showOnlySolution = false;

  final Graph _graph = Graph();

  // Регулярное выражение для проверки уравнения
  final RegExp _equationRegExp = RegExp(r'^[a-zA-Z]+\s*=\s*[a-zA-Z]+$');

  String? _validateEquation(String? value) {
    if (value == null || value.isEmpty) {
      return 'Введите уравнение';
    } else if (!_equationRegExp.hasMatch(value)) {
      if (!value.contains('=')) {
        return 'Некорректно составлено уравнение';
      } else {
        return 'Недопустимые символы';
      }
    }
    return null; // Уравнение корректно
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      // Отступы от краев экрана
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        // Прокрутка экрана для виджета графа
        child: SingleChildScrollView(
          scrollDirection: Axis.vertical,
          child: Column(
            children: [
              // Виджет системы уравнений
              SizedBox(
                height: 200,
                child: Column(
                  children: [
                    Expanded(
                      // Виджет списка уравнений
                      child: ListView.builder(
                        itemCount: _formKeys.length,
                        itemBuilder: (context, index) => Form(
                          key: _formKeys[index],
                          child: Row(
                            children: [
                              Expanded(
                                child: TextFormField(
                                  controller: _controllers[index],
                                  decoration: const InputDecoration(
                                    labelText: 'Уравнение',
                                    hintText: 'Ax = Bz',
                                    errorStyle: TextStyle(color: Colors.red),
                                  ),
                                  validator: _validateEquation,
                                ),
                              ),
                              // Кнопка удаления уравнения из системы
                              IconButton(
                                onPressed: () {
                                  setState(() {
                                    _formKeys.removeAt(index);
                                    _controllers.removeAt(index);
                                  });
                                },
                                icon: const Icon(Icons.delete),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(
                      height: 20,
                    ),
                    // Кнопка добавления уравнения в систему
                    TextButton(
                        onPressed: () {
                          setState(() {
                            _formKeys.add(GlobalKey<FormState>());
                            _controllers.add(TextEditingController());
                            if (_graph.nodes.isNotEmpty) {
                              _graph.nodes[0].key!.value.equations
                                  .add(createEquation('='));
                            } else {
                              _graph.addNode(Node.Id(MyNode(
                                  depth: 0, equations: [createEquation('=')])));
                            }
                          });
                        },
                        child: const Text('Добавить уравнение')),
                    const SizedBox(
                      height: 20,
                    ),
                    // Кнопка запуска поиска решений
                    TextButton(
                        onPressed: () {
                          setState(() {
                            if (_formKeys.every((formKey) =>
                                formKey.currentState?.validate() ?? false)) {
                              clearGraph(_graph);
                              _graph.addNode(Node.Id(
                                  MyNode(depth: 0, equations: [
                                for (TextEditingController text in _controllers)
                                  createEquation(text.text)
                              ])));
                              getVarsAndConstsFromList(
                                  _graph.nodes[0].key!.value.equations,
                                  _variables,
                                  _constants);
                              solve(_graph, 0);
                            }
                          });
                        },
                        child: const Text('Найти решения')),
                  ],
                ),
              ),
              // Разделитель экрана
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 40),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(children: [
                      const Text('Переменные: '),
                      for (String variable in _variables) ...[
                        const SizedBox(
                          width: 5,
                        ),
                        VarBox(variable: variable)
                      ],
                    ]),
                    const SizedBox(
                      height: 10,
                    ),
                    Row(children: [
                      const Text('Константы: '),
                      for (String constant in _constants) ...[
                        const SizedBox(
                          width: 5,
                        ),
                        ConstBox(constant: constant)
                      ],
                    ]),
                    const Divider(),
                  ],
                ),
              ),
              if (_graph.nodes.isNotEmpty) ...[
                Center(
                  child: Text(
                    'Дерево развёртки',
                    style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.lerp(
                            FontWeight.w600, FontWeight.w400, 0.5)),
                  ),
                ),
                const SizedBox(
                  height: 10,
                ),
                // Чекбокс для отображения только решения
                CheckboxListTile(
                  title: Text("Отображать только решение"),
                  value: _showOnlySolution,
                  onChanged: (bool? value) {
                    setState(() {
                      _showOnlySolution = value ?? false; // Обновляем состояние
                    });
                  },
                ),
                // Виджет графа
                if (_graph.nodes[0].key!.value.equations.length != 0 &&
                    !(_graph.nodes[0].key!.value.equations[0].left == '' &&
                        _graph.nodes[0].key!.value.equations[0].right == '' &&
                        _graph.nodes[0].key!.value.equations.length == 1))
                  (_showOnlySolution &&
                          !_graph.nodes[0].key!.value.isInSolution)
                      ? const Text('Нет решений')
                      : SingleChildScrollView(
                          scrollDirection: Axis.horizontal,
                          child: GraphView(
                            graph: _showOnlySolution
                                ? getOnlySolution(_graph)!
                                : _graph,
                            algorithm: BuchheimWalkerAlgorithm(
                                BuchheimWalkerConfiguration(),
                                TreeEdgeRenderer(
                                    BuchheimWalkerConfiguration())),
                            builder: (Node node) {
                              // Виджет внешнего вида графа
                              return Column(
                                children: [
                                  if (node.key!.value.rule != null)
                                    Text(
                                        node.key!.value.rule.variable +
                                            ' => ' +
                                            node.key!.value.rule.rule,
                                        style: const TextStyle(
                                            color: Colors.black, fontSize: 24)),
                                  Container(
                                    decoration: BoxDecoration(
                                      borderRadius: const BorderRadius.all(
                                          Radius.circular(10)),
                                      border: Border.all(
                                        color: node.key!.value.isInSolution
                                            ? Colors.green
                                            : Colors.red,
                                        width: 2,
                                      ),
                                      color: Colors.transparent,
                                    ),
                                    padding: const EdgeInsets.all(8),
                                    child: Text(node.key!.value.getNodeText(),
                                        style: const TextStyle(
                                            color: Colors.black, fontSize: 24)),
                                  ),
                                  errorWidget(node.key!.value.error_code)
                                ],
                              );
                            },
                          ),
                        )
              ],
              const SizedBox(
                height: 20,
              )
            ],
          ),
        ),
      ),
    );
  }
}

Widget errorWidget(int error_code){
  switch(error_code){
    case 1:
      return Column(
        children: [
          const SizedBox(height: 10,),
          Icon(
            Icons.do_not_disturb_alt,
            size: 40,
          )
        ]
      );
    case 2:
      return Column(
        children: [
          const SizedBox(height: 10,),
          Icon(
            Icons.autorenew,
            size: 40,
          )
        ]
      );
    case 3:
      return Column(
        children: [
          const SizedBox(height: 10,),
          Icon(
            Icons.remove_circle_outline,
            size: 40,
          )
        ]
      );
    default:
      return SizedBox.shrink();
  }
}
