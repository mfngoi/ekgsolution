import 'package:flutter/material.dart';
import 'package:test_application/aboutmepage.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  @override
  void initState() {
    super.initState();
    print("Entered SettingsPage");
  }

  void navigateToProfilePage() {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => AboutMePage()));
  }

  Widget SettingsRow(String pageName, Icon icon) {
    return GestureDetector(
      onTap: () {
        if (pageName == "About Me") {
          navigateToProfilePage();
        }
      },
      child: Container(
        width: 350,
        height: 70,
        // decoration: BoxDecoration(
        // border: Border(
        //   bottom: BorderSide(
        //     color: const Color.fromRGBO(121, 134, 203, 1),
        //     width: 1.0,
        //   ),
        // ),
        // ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: <Widget>[
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Row(
                  children: <Widget>[
                    icon,
                    SizedBox(width: 10),
                    Text(pageName,
                        style: TextStyle(
                            fontSize: 16, fontWeight: FontWeight.bold)),
                  ],
                ),
              ],
            ),
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.arrow_forward_ios),
              ],
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: false,
        leading: Padding(
          padding: const EdgeInsets.only(left: 40.0),
          child: Icon(
            Icons.settings,
            color: const Color.fromRGBO(57, 73, 171, 1),
          ),
        ),
        title: Text(
          "Settings",
          style: TextStyle(
              color: const Color.fromRGBO(57, 73, 171, 1),
              fontWeight: FontWeight.bold,
              fontSize: 24.0),
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            SizedBox(height: 30),
            SettingsRow("About Me", Icon(Icons.person)),
            SettingsRow("Messages", Icon(Icons.chat_bubble)),
            SettingsRow("Account and Privacy", Icon(Icons.lock)),
            SettingsRow("About Σureka", Icon(Icons.report)),
          ],
        ),
      ),
    );
  }
}
