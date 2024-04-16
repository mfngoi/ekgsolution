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
    Timer(Duration(milliseconds: 3000), navigateToHomePage);
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
            ClipRect(
              child: Align(
                alignment: Alignment.center,
                widthFactor: 0.8,
                child: Image.asset("assets/app_icon.png"),
              ),
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
