import 'package:flutter/material.dart';
import 'package:test_application/main.dart';
import 'package:test_application/signuppage.dart';
import 'package:test_application/navigationpage.dart';
import 'package:firebase_auth/firebase_auth.dart';

class LoginInPage extends StatefulWidget {
  const LoginInPage({super.key});

  @override
  State<LoginInPage> createState() => _LoginInPageState();
}

class _LoginInPageState extends State<LoginInPage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  bool obscureValue = true;
  bool rememberValue = true;

  @override
  void initState() {
    super.initState();
    auth.authStateChanges().listen((User? user) {
      if (user != null) {
        navigateToNavigationPage();
      }
    });
  }

  void navigateToSignUpPage() {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => const SignUpPage()));
  }

  void navigateToNavigationPage() {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => NavigationPage()));
  }

  Widget CustomTextField(String hintValue) {
    return Container(
      height: 35.0,
      width: 350.0,
      child: TextField(
        controller: _emailController,
        decoration: InputDecoration(
          contentPadding: EdgeInsets.all(8.0),
          hintText: hintValue,
          filled: true,
          fillColor: Colors.white, // Background color of the text field
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(
                50.0), // Adjust the value to control the roundness
            borderSide: BorderSide(
              color: Colors.purple, // Border color
              width: 4,
            ),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(50.0),
            borderSide: BorderSide(
              color: Colors.purple, // Border color when focused
              width: 4,
            ),
          ),
        ),
      ),
    );
  }

  Widget CustomPasswordField(String hintValue) {
    return Container(
      height: 35.0,
      width: 350.0,
      child: TextField(
        controller: _passwordController,
        obscureText: obscureValue,
        decoration: InputDecoration(
          contentPadding: EdgeInsets.all(8.0),
          suffixIcon: IconButton(
            icon: Icon(
              obscureValue ? Icons.visibility_off : Icons.visibility,
              color: Colors.purple,
            ),
            onPressed: () {
              setState(() {
                obscureValue = !obscureValue;
              });
            },
          ),
          hintText: hintValue,
          filled: true,
          fillColor: Colors.white, // Background color of the text field
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(
                50.0), // Adjust the value to control the roundness
            borderSide: BorderSide(
              color: Colors.purple, // Border color
              width: 4,
            ),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(50.0),
            borderSide: BorderSide(
              color: Colors.purple, // Border color when focused
              width: 4,
            ),
          ),
        ),
      ),
    );
  }

  Widget LoginButton() {
    return Container(
      height: 35.0,
      width: 350.0,
      child: ElevatedButton(
        onPressed: () {
          FirebaseAuth.instance
              .signInWithEmailAndPassword(
            email: _emailController.text,
            password: _passwordController.text,
          )
              .then((_) {
            navigateToNavigationPage();
          });
        },
        style: ButtonStyle(
          backgroundColor: MaterialStateProperty.all(
              Colors.black), // Background color of the button
          foregroundColor: MaterialStateProperty.all(
              Colors.white), // Text color of the buttonof the button
        ),
        child: Text('Log In'),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      appBar: AppBar(
        centerTitle: false,
        leading: Padding(
          padding: const EdgeInsets.only(left: 40.0),
          child: Icon(
            Icons.file_copy,
          ),
        ),
        title: Text(
          "Σureka",
          style: TextStyle(
              color: Colors.black, fontWeight: FontWeight.bold, fontSize: 25.0),
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            SizedBox(height: 50),
            Text(
              "Welcome Back!",
              style: TextStyle(
                color: Colors.black,
                fontWeight: FontWeight.bold,
                fontSize: 40,
              ),
            ),
            Text(
              "Please enter your login information",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 30,
              ),
            ),
            SizedBox(height: 80),
            CustomTextField("Username, Email, or Phone Number"),
            SizedBox(height: 10),
            CustomPasswordField("Password"),
            SizedBox(height: 10),
            Container(
              width: 350.0,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: <Widget>[
                      SizedBox(
                          width: 30,
                          child: Checkbox(
                            value: rememberValue,
                            onChanged: (bool? remValue) {
                              setState(() {
                                rememberValue = remValue!;
                              });
                            },
                          )),
                      Text(
                        "Remember me",
                        style: TextStyle(
                          fontSize: 15,
                        ),
                      ),
                    ],
                  ),
                  Text(
                    "Forgot Password?",
                    style: TextStyle(
                      fontSize: 15,
                    ),
                  ),
                ],
              ),
            ),
            SizedBox(height: 50),
            LoginButton(),
            SizedBox(height: 230),
            Row(mainAxisAlignment: MainAxisAlignment.center, children: <Widget>[
              Text(
                "Don't have an account?",
              ),
              TextButton(
                  onPressed: navigateToSignUpPage,
                  child: Text(
                    "Sign Up",
                    style: TextStyle(
                      decoration: TextDecoration.underline,
                      fontWeight: FontWeight.bold,
                    ),
                  )),
            ]),
          ],
        ),
      ),
    );
  }
}
