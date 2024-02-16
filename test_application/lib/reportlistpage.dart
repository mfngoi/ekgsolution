import 'package:flutter/material.dart';
import 'package:flutter_application/reportpage.dart';

class ReportListPage extends StatefulWidget {
  const ReportListPage({super.key});

  @override
  State<ReportListPage> createState() => _ReportListPageState();
}

class _ReportListPageState extends State<ReportListPage> {
  Widget TopWindow() {
    return Container(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Text("Most Recent Report"),
              ],
            ),
            ClipRRect(
              borderRadius: BorderRadius.circular(7.0),
              child: Container(
                height: 200,
                color: Colors.purple,
              ),
            ),
          ],
        ),
      ),
    );
  }

  void navigateToReportPage() {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => ReportPage()));
  }

  Widget ReportRow() {
    return GestureDetector(
      onTap: () {
        navigateToReportPage();
      },
      child: Container(
          margin: const EdgeInsets.only(bottom: 5.0),
          color: Color.fromARGB(255, 223, 173, 231),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: <Widget>[
              Icon(Icons.settings),
              Text("Your Report"),
              Icon(
                Icons.arrow_forward_ios,
                size: 15,
              ),
            ],
          )),
    );
  }

  Widget ReportList() {
    return Container(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Text("Past Reports"),
              ],
            ),
            ClipRRect(
              borderRadius: BorderRadius.circular(7.0),
              child: Container(
                height: 200,
                child: ListView(
                  children: <Widget>[
                    ReportRow(),
                    ReportRow(),
                    ReportRow(),
                    ReportRow(),
                    ReportRow(),
                  ],
                ),
              ),
            ),
          ],
        ),
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
          "Personal Reports",
          style: TextStyle(
              color: Colors.black, fontWeight: FontWeight.bold, fontSize: 25.0),
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            SizedBox(height: 20),
            TopWindow(),
            Container(
              height: 20,
              color: Colors.purple,
            ),
            ReportList(),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: "",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.addchart),
            label: "",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: "",
          ),
        ],
      ),
    );
  }
}
