import 'package:flutter/material.dart';
import 'package:test_application/loginpage.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:test_application/masterpage.dart';

class SignUpPage extends StatefulWidget {
  const SignUpPage({super.key});

  @override
  State<SignUpPage> createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  final _emailController = TextEditingController();
  final _passwordController1 = TextEditingController();
  final _passwordController2 = TextEditingController();

  bool obscureValue1 = true;
  bool obscureValue2 = true;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController1.dispose();
    _passwordController2.dispose();
    super.dispose();
  }

  void navigateToMasterPage() {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => MasterPage()));
  }

  void navigateToLoginPage() {
    Navigator.pop(context);
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

  Widget CustomPasswordField1(String hintValue) {
    return Container(
      height: 35.0,
      width: 350.0,
      child: TextField(
        controller: _passwordController1,
        obscureText: obscureValue1,
        decoration: InputDecoration(
          contentPadding: EdgeInsets.all(8.0),
          suffixIcon: IconButton(
            icon: Icon(
              obscureValue1 ? Icons.visibility_off : Icons.visibility,
              color: Colors.purple,
            ),
            onPressed: () {
              setState(() {
                obscureValue1 = !obscureValue1;
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

  Widget CustomPasswordField2(String hintValue) {
    return Container(
      height: 35.0,
      width: 350.0,
      child: TextField(
        controller: _passwordController2,
        obscureText: obscureValue2,
        decoration: InputDecoration(
          contentPadding: EdgeInsets.all(8.0),
          suffixIcon: IconButton(
            icon: Icon(
              obscureValue2 ? Icons.visibility_off : Icons.visibility,
              color: Colors.purple,
            ),
            onPressed: () {
              setState(() {
                obscureValue2 = !obscureValue2;
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

  void SignUp() async {
    print("Clicked Button");
    // Create a user account for firebase authentication
    String email_text = _emailController.text;
    String password_text = _passwordController2.text;
    UserCredential credential = await FirebaseAuth.instance.createUserWithEmailAndPassword(
      email: email_text,
      password: password_text,
    );
    print("Created Account");

    // Create user information in database
    // final weekReport = <String, dynamic>{
    //   "warnings": 0,
    // };
    // final report = <String, dynamic>{
    //   "signals": [200, 300, 400, 500, 600, 700, 800, 500, 400, 300, 400]
    // };
    final user = <String, dynamic>{
      "email": _emailController.text,
      "sex": "?",
      "age": 0,
      "height": 0,
      "weight": 0,
      "race": "?",
    };

    final db = await FirebaseFirestore.instance; // Connect to database

    await db
        .collection("users_test")
        .doc(credential.user?.uid)
        .set(user); // Add user info to database

    // // Code to determine what week the report should be stored in
    // DateTime date = DateTime.now();

    // int weekOfYear = date.weekday == DateTime.sunday
    //     ? date.difference(DateTime(date.year, 1, 1)).inDays ~/ 7 + 1
    //     : date.difference(DateTime(date.year, 1, 1)).inDays ~/ 7;

    // String weekDocId = weekOfYear.toString() + "_" + date.year.toString();

    // await db
    //     .collection("users_test")
    //     .doc(credential.user?.uid)
    //     .collection("weekly_reports") // create colletion for weeks
    //     .doc(weekDocId)
    //     .set(weekReport); // Add warnings field

    // await db
    //     .collection("users_test")
    //     .doc(credential.user?.uid)
    //     .collection("weekly_reports")
    //     .doc(weekDocId)
    //     .collection("reports")  // create collection for reports in each week
    //     .doc(date.toString())
    //     .set(report);  // Add dummy ekg report into db
    // print("Created User Data");

    navigateToMasterPage();
  }

  Widget SignUpButton() {
    return Container(
      height: 35.0,
      width: 350.0,
      child: ElevatedButton(
        onPressed: SignUp,
        style: ButtonStyle(
          backgroundColor: MaterialStateProperty.all(
              Colors.black), // Background color of the button
          foregroundColor: MaterialStateProperty.all(
              Colors.white), // Text color of the buttonof the button
        ),
        child: Text('Sign Up'),
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
            color: Colors.purple,
          ),
        ),
        title: Text(
          "Σureka",
          style: TextStyle(
              color: Colors.black, fontWeight: FontWeight.bold, fontSize: 25.0),
        ),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text(
                "Hi! Welcome",
                style: TextStyle(
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                  fontSize: 40,
                ),
              ),
              Text(
                "Please register below",
                style: TextStyle(
                  color: Colors.purple,
                  fontSize: 30,
                ),
              ),
              SizedBox(height: 50),
              CustomTextField("Email or Phone Number"),
              SizedBox(height: 20),
              CustomTextField("Full Name"),
              SizedBox(height: 20),
              CustomPasswordField1("Password"),
              Text(
                "Password must be at least 6 characters and contain numbers and letters",
                style: TextStyle(
                  color: Colors.purple,
                  fontSize: 10,
                ),
              ),
              SizedBox(height: 20),
              CustomPasswordField2("Confirm Password"),
              SizedBox(height: 20),
              SignUpButton(),
              SizedBox(height: 10),
              Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    Text(
                      "Have an account?",
                      style: TextStyle(color: Colors.purple),
                    ),
                    TextButton(
                        onPressed: navigateToLoginPage,
                        child: Text(
                          "Log In",
                          style: TextStyle(
                              decoration: TextDecoration.underline,
                              fontWeight: FontWeight.bold,
                              color: Colors.purple),
                        )),
                  ]),
              SizedBox(height: 150),
              Text("We need permission for the service you use. Learn more."),
            ],
          ),
        ),
      ),
    );
  }
}
