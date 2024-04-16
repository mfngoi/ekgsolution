import 'package:flutter/material.dart';
import 'package:test_application/loginpage.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:test_application/navigationpage.dart';

class SignUpPage extends StatefulWidget {
  const SignUpPage({super.key});

  @override
  State<SignUpPage> createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController1 = TextEditingController();
  final _passwordController2 = TextEditingController();

  bool obscureValue1 = true;
  bool obscureValue2 = true;

  void navigateToNavigationPage() {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => NavigationPage()));
  }

  void navigateToLoginPage() {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => const LoginInPage()));
  }

  Widget NameTextField(String hintValue) {
    return Container(
      height: 35.0,
      width: 350.0,
      child: TextField(
        controller: _nameController,
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

  Widget EmailTextField(String hintValue) {
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
    // Create a user account for firebase authentication
    String name_text = _nameController.text;
    String email_text = _emailController.text;
    String password_text = _passwordController2.text;

    // Create an account
    UserCredential cred =
        await FirebaseAuth.instance.createUserWithEmailAndPassword(
      email: email_text,
      password: password_text,
    );

    final profileInfo = {
      "full_name": name_text,
      "email": email_text,
      "age": 0,
      "sex": "?",
      "height": 0,
      "weight": 0,
      "race": "?",
    };

    // Allocate space for user data in the database
    final db = await FirebaseFirestore.instance; // Connect to database
    await db
        .collection("users_test")
        .doc(cred.user?.uid)
        .set(profileInfo); // Creates a user folder in the database

    // final weekInfo = {
    //   "warnings": 0,
    // };
    // await db
    //     .collection("users_test")
    //     .doc(cred.user?.uid)
    //     .collection("weekly_reports")
    //     .doc("week11")                 // !!!!!!!!!!!!!!!!!!!!
    //     .set(weekInfo); // creates weekly report list in user

    // final reportInfo = {
    //   "signals": [1, 2, 3, 4, 5, 6],
    // };
    // await db
    //     .collection("users_test")
    //     .doc(cred.user?.uid)
    //     .collection("weekly_reports")
    //     .doc("week11")                 // !!!!!!!!!!!!!!!!!!!!
    //     .collection("reports")
    //     .doc(DateTime.now().toString())
    //     .set(reportInfo);

    // Navigate to homepage
    navigateToNavigationPage();
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

  Widget birthdayDropdown() {
    DateTime date = DateTime.now();

    List months = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December'
    ];

    String selectedDay = date.day.toString(); // Default today's date
    String selectedMonth = months[date.month - 1];
    String selectedYear = date.year.toString();

    List<DropdownMenuItem<String>> dayItems =
        List<String>.generate(31, (index) => '${index + 1}')
            .map((String value) {
      return DropdownMenuItem<String>(
        value: value,
        child: Text(value),
      );
    }).toList();

    List<DropdownMenuItem<String>> monthItems = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December'
    ].map((String value) {
      return DropdownMenuItem<String>(
        value: value,
        child: Text(value),
      );
    }).toList();

    List<DropdownMenuItem<String>> yearItems =
        List<String>.generate(100, (index) => '${DateTime.now().year - index}')
            .map((String value) {
      return DropdownMenuItem<String>(
        value: value,
        child: Text(value),
      );
    }).toList();

    return Container(
      width: 350,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: <Widget>[
          DropdownButton<String>(
            value: selectedDay,
            onChanged: (newValue) {
              setState(() {
                selectedDay = newValue!;
              });
            },
            items: dayItems,
          ),
          DropdownButton<String>(
            value: selectedMonth,
            onChanged: (newValue) {
              setState(() {
                selectedMonth = newValue!;
              });
            },
            items: monthItems,
          ),
          DropdownButton<String>(
            value: selectedYear,
            onChanged: (newValue) {
              setState(() {
                selectedYear = newValue!;
              });
            },
            items: yearItems,
          ),
        ],
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
              NameTextField("Full Name"),
              SizedBox(height: 20),
              EmailTextField("Email or Phone Number"),
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
              birthdayDropdown(),
              SizedBox(height: 40),
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
                        onPressed: () {
                          Navigator.pop(context);
                        },
                        child: Text(
                          "Log In",
                          style: TextStyle(
                              decoration: TextDecoration.underline,
                              fontWeight: FontWeight.bold,
                              color: Colors.purple),
                        )),
                  ]),
              SizedBox(height: 100),
              Text("We need permission for the service you use. Learn more."),
            ],
          ),
        ),
      ),
    );
  }
}
