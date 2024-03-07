import 'dart:async';
import 'package:flutter/material.dart';
import 'package:test_application/loginpage.dart';

class Splash extends StatefulWidget {
  const Splash({super.key});

  @override
  State<Splash> createState() => _SplashState();
}

class _SplashState extends State<Splash> {
  @override
  void initState() {
    super.initState();
    // Delay
    Timer(Duration(milliseconds: 2500), navigateToHomePage);
  }

  void navigateToHomePage() {
    Navigator.pushReplacement(
        context, MaterialPageRoute(builder: (context) => LoginInPage()));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Container(
              color: Colors.purple,
              height: 50,
              width: 50,
            ),
            Text(
              "Σureka",
              style: TextStyle(
                color: Colors.black,
                fontWeight: FontWeight.bold,
                fontSize: 30.0,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
