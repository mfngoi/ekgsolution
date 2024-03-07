import 'package:flutter/material.dart';
import 'package:test_application/reportpage.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class ReportListPage extends StatefulWidget {
  final String user_email;
  const ReportListPage({super.key, required this.user_email});

  @override
  State<ReportListPage> createState() => _ReportListPageState();
}

class _ReportListPageState extends State<ReportListPage> {
  late Future<List> reports;  // List of reports user has collected

  @override
  void initState() {
    super.initState();
    reports = QueryReports();
  }

  Future<List> QueryReports() async {
    List reports = [];
    final db = await FirebaseFirestore.instance;  // Connect to db

    // Query all documents in reports collection in specific user
    await db
        .collection("users")
        .doc(widget.user_email)
        .collection("reports")
        .get()
        .then(
      (querySnapshot) {
        for (var docSnapshot in querySnapshot.docs) {
          reports.add(docSnapshot.id);
          // print(docSnapshot.id);
          // print(docSnapshot.data());
        }
      },
      onError: (e) => print("Error completing: $e"),
    );

    // Sort report from most recent to least recent
    reports.sort((a, b) => DateTime.parse(b).compareTo(DateTime.parse(a)));

    return reports;
  }

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

  Widget ReportRow(String report_id) {
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
              Text(report_id),
              Icon(
                Icons.arrow_forward_ios,
                size: 15,
              ),
            ],
          )),
    );
  }

  Widget ReportList(List<Widget> reportRows) {
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
                  children: reportRows,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget ReportListSection() {
    return FutureBuilder(
      future: reports,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          List reports = snapshot.data as List;
          // print(reports);

          List<Widget> reportChildren = [];
          for (int i = 0; i < reports.length; i++) {
            reportChildren.add(ReportRow(reports[i]));
          }

          return ReportList(reportChildren);
        } else {
          return Text("Unable to get reports from database...");
        }
      },
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
        actions: <Widget>[
          ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: Text("Back")),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            SizedBox(height: 20),
            TopWindow(),
            SizedBox(height: 20),
            ReportListSection(),
            SizedBox(height: 20),
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
