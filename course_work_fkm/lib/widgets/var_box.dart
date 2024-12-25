import 'package:flutter/material.dart';

class VarBox extends StatelessWidget {
  const VarBox({super.key, required this.variable});

  final String variable;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 32.0,
      height: 32.0,
      decoration: BoxDecoration(
        color: Colors.transparent,
        shape: BoxShape.circle,
        border: Border.all(
          color: Colors.blue,
          width: 2,
        ),
      ),
      child: Center(
        child: Text(
          variable,
          style: const TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}
