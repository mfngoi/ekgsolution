import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class ProfilePage extends StatefulWidget {
  final String user_email;
  const ProfilePage({super.key, required this.user_email});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  // sex, age, height, weight, ethnicity

  final _sexController = TextEditingController();
  final _ageController = TextEditingController();
  final _heightController = TextEditingController();
  final _weightController = TextEditingController();
  final _ethnicityController = TextEditingController();

  void SubmitData() async {

    final newData = <String, dynamic>{
      "sex": _sexController.text,
      "age": _ageController.text,
      "height": _heightController.text,
      "weight": _weightController.text,
      "race": _ethnicityController.text,
    };

    final db = await FirebaseFirestore.instance; // Connect to database

    final docRef = await db.collection("users").doc(widget.user_email); // Get container of user data
    await docRef.update(newData); // Update user data

  }

  Widget BackButton() {
    return ElevatedButton(onPressed: () {
        Navigator.pop(context);
      }, child: Text('Back'));
  }

  Widget SexTextField(String hintValue) {
    return Container(
      height: 35.0,
      width: 350.0,
      child: TextField(
        controller: _sexController,
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

  Widget AgeTextField(String hintValue) {
    return Container(
      height: 35.0,
      width: 350.0,
      child: TextField(
        controller: _ageController,
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

  Widget HeightTextField(String hintValue) {
    return Container(
      height: 35.0,
      width: 350.0,
      child: TextField(
        controller: _heightController,
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

  Widget WeightTextField(String hintValue) {
    return Container(
      height: 35.0,
      width: 350.0,
      child: TextField(
        controller: _weightController,
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

  Widget EthnicityTextField(String hintValue) {
    return Container(
      height: 35.0,
      width: 350.0,
      child: TextField(
        controller: _ethnicityController,
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

  Widget SubmitButton() {
    return ElevatedButton(onPressed: SubmitData, child: Text('Submit'));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            BackButton(),
            SexTextField('Sex (M/F) ... '),
            AgeTextField('Age ... '),
            HeightTextField('Height (cm) ...'),
            WeightTextField('Weight (kg) ...'),
            EthnicityTextField('Ethnicity ...'),
            SubmitButton(),
          ]
        ),
      ),
    );
  }
}