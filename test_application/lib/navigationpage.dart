import 'package:flutter/material.dart';
import 'package:test_application/homepage.dart';
import 'package:test_application/weeklyreportpage.dart';
import 'package:test_application/aichatpage.dart';
import 'package:test_application/settingspage.dart';
import 'package:test_application/my_flutter_app_icons.dart';

int selectedIndex = 0;

class NavigationPage extends StatefulWidget {
  const NavigationPage({super.key});

  @override
  State<NavigationPage> createState() => _NavigationPageState();
}

class _NavigationPageState extends State<NavigationPage> {
  static final List<Widget> pages = <Widget>[
    const HomePage(),
    const WeeklyReportPage(),
    const AIChatPage(),
    const SettingsPage(),
  ];

  void selectPage(int index) {
    setState(() {
      selectedIndex = index;
    });
  }

  Widget CheckReport() {
    return Container(
      width: 350,
      height: 60,
      child: ElevatedButton(
        style: ButtonStyle(
          shape: MaterialStateProperty.all<RoundedRectangleBorder>(
            RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(
                  10.0), // Adjust the value to control the roundness
            ),
          ),
          padding: MaterialStateProperty.all<EdgeInsetsGeometry>(
              EdgeInsets.all(16.0)),
          backgroundColor: MaterialStateProperty.all<Color>(
              const Color.fromRGBO(121, 134, 203, 1)),
          foregroundColor: MaterialStateProperty.all<Color>(Colors.white),
        ),
        onPressed: () {
          print("Clicked Check Report");
          selectPage(1);
        },
        child: Text(
          "Check Report",
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
          textAlign: TextAlign.center,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: selectedIndex != 0
          ? pages[selectedIndex]
          : Stack(
              children: <Widget>[
                pages[0],
                Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: <Widget>[
                      SizedBox(height: 320),
                      CheckReport(),
                    ],
                  ),
                ),
              ],
            ),
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: "Home",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.file_copy),
            label: "Reports",
          ),
          BottomNavigationBarItem(
            icon: Icon(MyFlutterApp.robot),
            label: "AI Chat",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.settings),
            label: "Settings",
          ),
        ],
        type: BottomNavigationBarType.fixed,
        selectedItemColor: const Color.fromRGBO(57, 73, 171, 1),
        unselectedItemColor: Colors.grey,
        currentIndex: selectedIndex,
        onTap: selectPage,
      ),
    );
  }
}
