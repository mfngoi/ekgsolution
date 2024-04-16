import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:test_application/loginpage.dart';
import 'package:test_application/main.dart';

const List<String> ethnic = <String>[
  'OTHER',
  'WHITE',
  'ASIAN',
  'AFRICAN AMERICAN'
];

class AboutMePage extends StatefulWidget {
  const AboutMePage({super.key});

  @override
  State<AboutMePage> createState() => _AboutMePageState();
}

class _AboutMePageState extends State<AboutMePage> {
  late User user;
  late Future<Map> user_info;

  bool _editMode = false;
  String ethnicityValue = ethnic.first;

  final _sexController = TextEditingController();
  final _ageController = TextEditingController();
  final _heightController = TextEditingController();
  final _weightController = TextEditingController();

  @override
  void initState() {
    super.initState();
    print("Entered ProfilePage");

    user = auth.currentUser!;
    user_info = QueryUserInfo();
  }

  @override
  void dispose() {
    _sexController.dispose();
    _ageController.dispose();
    _heightController.dispose();
    _weightController.dispose();
    super.dispose();
  }

  Future<Map> QueryUserInfo() async {
    // Query for user data
    final db = await FirebaseFirestore.instance; // Connect to database

    Map user_info = await db.collection("users_test").doc(user.uid).get().then(
      (DocumentSnapshot doc) {
        final data = doc.data() as Map<String, dynamic>;
        // print(data);
        return data;
      },
      onError: (e) => print("Error completing: $e"),
    );

    return user_info;
  }

  Widget BackButton(BuildContext context) {
    return IconButton(
      icon: Icon(Icons.arrow_back, color: Color.fromRGBO(57, 73, 171, 1)),
      onPressed: () {
        Navigator.of(context).pop();
      },
    );
  }

  Widget EditButton(BuildContext context) {
    return IconButton(
      icon: Icon(Icons.edit, color: Color.fromRGBO(57, 73, 171, 1)),
      onPressed: () {
        setState(() {
          _editMode = !_editMode;
        });
      },
    );
  }

  Widget FutureFields() {
    return FutureBuilder(
      future: user_info,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          Map user_info = snapshot.data as Map;
          return UserInfoFields(user_info);
        } else {
          return Text("Unable to get user information from database...");
        }
      },
    );
  }

  Widget UserInfoFields(Map user_info) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        Padding(
          padding: EdgeInsets.symmetric(horizontal: 30.0),
          child: Container(
            width: double.infinity,
            decoration: BoxDecoration(
              border: Border(
                bottom: BorderSide(
                  color: Colors.black,
                  width: 2.0,
                ),
              ),
            ),
            child: Center(
              child: Text(
                user_info['email'],
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 16.0,
                ),
              ),
            ),
          ),
        ),
        SizedBox(height: 30),
        RowFields(user_info, "Age", 'age'),
        SizedBox(height: 10),
        RowFields(user_info, "Sex", 'sex'),
        SizedBox(height: 10),
        RowFields(user_info, "Height", 'height'),
        SizedBox(height: 10),
        RowFields(user_info, "Weight", 'weight'),
        SizedBox(height: 10),
        RowFields(user_info, "Race", 'race'),
        SizedBox(height: 10),
      ],
    );
  }

  Widget RowFields(Map user_info, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 50.0),
      child: Container(
        height: 50.0,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            Container(
              width: 100.0,
              child: Text(
                label + ": ",
                style: TextStyle(fontSize: 16),
              ),
            ),
            SizedBox(width: 50),
            !_editMode ? displayInfo(user_info, value) : editInfo(value),
          ],
        ),
      ),
    );
  }

  Widget displayInfo(Map user_info, String value) {
    return Container(
      child: user_info[value] == "" ||
              user_info[value] == 0 ||
              user_info[value] == "?"
          ? Text("empty")
          : Text(user_info[value]),
    );
  }

  Widget editInfo(String value) {
    if (value == 'age') {
      return AgeTextField("Age");
    }
    if (value == 'height') {
      return HeightTextField("Height (m)");
    }
    if (value == 'weight') {
      return WeightTextField("Weight (kg)");
    }
    if (value == 'race') {
      return EthnicityField("Something");
    }
    if (value == 'sex') {
      return SexTextField("M / F");
    }
    return Text("Error...");
  }

  Widget SexTextField(String hintValue) {
    return Container(
      height: 35.0,
      width: 150.0,
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
              color: const Color.fromRGBO(121, 134, 203, 1), // Border color
              width: 4,
            ),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(50.0),
            borderSide: BorderSide(
              color: const Color.fromRGBO(
                  121, 134, 203, 1), // Border color when focused
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
      width: 150.0,
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
              color: const Color.fromRGBO(121, 134, 203, 1), // Border color
              width: 4,
            ),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(50.0),
            borderSide: BorderSide(
              color: const Color.fromRGBO(
                  121, 134, 203, 1), // Border color when focused
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
      width: 150.0,
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
              color: const Color.fromRGBO(121, 134, 203, 1), // Border color
              width: 4,
            ),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(50.0),
            borderSide: BorderSide(
              color: const Color.fromRGBO(
                  121, 134, 203, 1), // Border color when focused
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
      width: 150.0,
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
              color: const Color.fromRGBO(121, 134, 203, 1), // Border color
              width: 4,
            ),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(50.0),
            borderSide: BorderSide(
              color: const Color.fromRGBO(
                  121, 134, 203, 1), // Border color when focused
              width: 4,
            ),
          ),
        ),
      ),
    );
  }

  Widget EthnicityField(String hintValue) {
    return DropdownMenu<String>(
      width: 150.0,
      initialSelection: ethnic.first,
      onSelected: (String? value) {
        // This is called when the user selects an item.
        setState(() {
          ethnicityValue = value!;
        });
      },
      dropdownMenuEntries:
          ethnic.map<DropdownMenuEntry<String>>((String value) {
        return DropdownMenuEntry<String>(value: value, label: value);
      }).toList(),
    );
  }

  Widget SubmitButton() {
    return ElevatedButton(onPressed: SubmitData, child: Text('Submit'));
  }

  void SubmitData() async {
    Map<String, dynamic> newData = {};

    if (_ageController.text != "") {
      newData.addAll({"age": _ageController.text});
    }
    if (_sexController.text != "") {
      newData.addAll({"sex": _sexController.text});
    }
    if (_heightController.text != "") {
      newData.addAll({"height": _heightController.text});
    }
    if (_weightController.text != "") {
      newData.addAll({"weight": _weightController.text});
    }
    if (ethnicityValue != "OTHER") {
      newData.addAll({"race": ethnicityValue});
    }

    final db = await FirebaseFirestore.instance; // Connect to database

    final docRef = await db
        .collection("users_test")
        .doc(user.uid); // Get container of user data
    await docRef.update(newData); // Update user data
  }

  Widget LogOutButton() {
    return ElevatedButton(
        onPressed: signOut,
        child: Text(
          "Sign Out",
        ));
  }

  void signOut() async {
    await auth.signOut();
    Navigator.of(context).pushAndRemoveUntil(
        MaterialPageRoute(builder: (context) => LoginInPage()),
        (route) => false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: BackButton(context),
        actions: <Widget>[
          Padding(
            padding: EdgeInsets.only(right: 30),
            child: EditButton(context),
          ),
        ],
      ),
      body: Center(
        child: ListView(
          children: <Widget>[
            FutureFields(),
            SizedBox(height: 40),
            Center(
              child: SizedBox(
                width: 200, // Constrain the width of the button
                child: SubmitButton(),
              ),
            ),
            SizedBox(height: 10), // Spacing between buttons
            Center(
              child: SizedBox(
                width: 200, // Constrain the width of the button
                child: LogOutButton(),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
