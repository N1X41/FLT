import 'package:flutter/material.dart';

class ConstBox extends StatelessWidget {
  const ConstBox({super.key, required this.constant});

  final String constant;

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.transparent,
        borderRadius: const BorderRadius.all(Radius.circular(5)),
        border: Border.all(
          color: Colors.blue,
          width: 2,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(5.0),
        child: Text(
          constant,
          style: const TextStyle(fontSize: 18),
        ),
      ),
    );
  }
}
