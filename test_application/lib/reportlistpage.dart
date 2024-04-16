import 'package:flutter/material.dart';
import 'package:test_application/reportpage.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:test_application/main.dart';

class ReportListPage extends StatefulWidget {
  final String weekId;
  const ReportListPage({super.key, required this.weekId});

  @override
  State<ReportListPage> createState() => _ReportListPageState();
}

class _ReportListPageState extends State<ReportListPage> {
  late Future<List> reportList; // Variable to hold the list of reports
  late User user;

  // Tells the page what to do when it first opens
  @override
  void initState() {
    super.initState();
    user = auth.currentUser!;
    reportList =
        QueryReportList(); // Asking the db for a list of the user's reports
  }

  Future<List> QueryReportList() async {
    final db = await FirebaseFirestore.instance; // Connect to database
    List reportList = [];

    // Ask the database for reports
    await db
        .collection("users_test")
        .doc(user.uid)
        .collection("weekly_reports")
        .doc(widget.weekId)
        .collection("reports")
        .get()
        .then(
      (querySnapshot) {
        for (var docSnapshot in querySnapshot.docs) {
          reportList.add(docSnapshot.id);
          // print(docSnapshot.data());
        }
      },
      onError: (e) => print("Error completing: $e"),
    );

    // Sorting...
    reportList.sort((b, a) => a.compareTo(b));

    return reportList;
  }

  void navigateToReportPage(String weekId, String reportId) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => ReportPage(weekId: weekId, reportId: reportId)));
  }

  Widget ReportRow(String reportName) {
    return GestureDetector(
      onTap: () {
        navigateToReportPage(widget.weekId, reportName);
      },
      child: Container(
          height: 35,
          margin: const EdgeInsets.only(bottom: 5.0),
          color: Color.fromARGB(255, 159, 168, 218),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.only(left: 4.0),
                child: Icon(Icons.file_copy),
              ),
              Text(reportName),
              Padding(
                padding: const EdgeInsets.only(right: 4.0),
                child: Icon(
                  Icons.arrow_forward_ios,
                  size: 15,
                ),
              ),
            ],
          )),
    );
  }

  List<Widget> generateReportRows(List reportList) {
    List<Widget> reportRows = [];
    for (int i = 0; i < reportList.length; i++) {
      reportRows.add(ReportRow(reportList[i]));
    }
    return reportRows;
  }

  Widget ReportList(List reportList) {
    return Container(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Text("Current Week's Reports",
                    style:
                        TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ],
            ),
            SizedBox(height: 20),
            ClipRRect(
              child: Container(
                height: 700,
                child: ListView(
                  padding: EdgeInsets.zero,
                  children: generateReportRows(reportList),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget FutureReportList() {
    return FutureBuilder(
        future: reportList,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            // render the report list on screen
            List reportList = snapshot.data as List;
            return ReportList(reportList);
          } else {
            return Text("An error occurred. Could not get report list");
          }
        });
  }

  Widget BackButton(BuildContext context) {
    return IconButton(
      icon: Icon(Icons.arrow_back, color: Color.fromRGBO(57, 73, 171, 1)),
      onPressed: () {
        Navigator.of(context).pop();
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            SizedBox(height: 70),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 30.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  BackButton(context),
                ],
              ),
            ),
            FutureReportList(),
          ],
        ),
      ),
    );
  }
}
