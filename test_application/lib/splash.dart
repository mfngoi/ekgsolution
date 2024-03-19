import 'dart:async';
import 'package:flutter/material.dart';
import 'package:test_application/loginpage.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:test_application/main.dart';
import 'package:test_application/masterpage.dart';

class Splash extends StatefulWidget {
  const Splash({super.key});

  @override
  State<Splash> createState() => _SplashState();
}

class _SplashState extends State<Splash> {
  @override
  void initState() {
    super.initState();

    // if (FirebaseAuth.instance.currentUser != null) {
    //   print("================= PING =====================");
    //   print(FirebaseAuth.instance.currentUser?.uid);
    // }

    // Delay
    Timer(Duration(milliseconds: 3000), navigateToApp);
  }

  void navigateToApp() {
    auth.authStateChanges().listen((User? user) {
      if (user == null) {
        navigateToLoginPage();
      } else {
        navigateToHomePage();
      }
    });
  }

  void navigateToLoginPage() {
    Navigator.push(
        context, MaterialPageRoute(builder: (context) => LoginInPage()));
  }

  void navigateToHomePage() {
    Navigator.push(
        context,
        MaterialPageRoute(
            builder: (context) => MasterPage()));
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
