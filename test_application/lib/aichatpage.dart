import 'package:flutter/material.dart';
import 'package:test_application/my_flutter_app_icons.dart';

class AIChatPage extends StatefulWidget {
  const AIChatPage({super.key});

  @override
  State<AIChatPage> createState() => _AIChatPageState();
}

class _AIChatPageState extends State<AIChatPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: false,
        leading: Padding(
          padding: const EdgeInsets.only(left: 40.0),
          child: Icon(
            MyFlutterApp.robot,
            color: const Color.fromRGBO(57, 73, 171, 1),
          ),
        ),
        title: Text(
          "AI Chat Bot",
          style: TextStyle(
              color: const Color.fromRGBO(57, 73, 171, 1),
              fontWeight: FontWeight.bold,
              fontSize: 24.0),
        ),
      ),
      body: Center(
        child: Text("AI Chat Page under development",
            style: TextStyle(fontSize: 16.0)),
      ),
    );
  }
}
