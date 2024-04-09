import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:test_application/main.dart';
import 'package:test_application/reportpage.dart';

class ReportListPage extends StatefulWidget {
  final String week_id;
  const ReportListPage({super.key, required this.week_id});
  @override
  State<ReportListPage> createState() => _ReportListPageState();
}

class _ReportListPageState extends State<ReportListPage> {
  late Future<List<QueryDocumentSnapshot>> reports;
  late User user;

  @override
  void initState() {
    super.initState();
    print("Entered ReportListPage: " + widget.week_id);

    user = auth.currentUser!;
    reports = QueryReports();
  }

  Future<List<QueryDocumentSnapshot>> QueryReports() async {
    List<QueryDocumentSnapshot> reports = [];
    final db = await FirebaseFirestore.instance; // Connect to db

    // Query all documents in reports collection in specific user
    await db
        .collection("users_test")
        .doc(user.uid)
        .collection("weekly_reports")
        .doc(widget.week_id)
        .collection("reports")
        .get()
        .then(
      (querySnapshot) {
        for (var docSnapshot in querySnapshot.docs) {
          reports.add(docSnapshot);
          print(docSnapshot.id);
          // print(docSnapshot.data());
        }
      },
      onError: (e) => print("Error completing: $e"),
    );

    // Sort report from most recent to least recent
    reports
        .sort((a, b) => DateTime.parse(b.id).compareTo(DateTime.parse(a.id)));

    return reports;
  }

  void navigateToReportPage(String report_id) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) =>
            ReportPage(week_id: widget.week_id, report_id: report_id)));
  }

  Widget BackButton() {
    return ElevatedButton(
      onPressed: () {
        Navigator.pop(context);
      },
      child: Text("Back"),
    );
  }

  Widget ReportListSection() {
    return FutureBuilder(
      future: reports,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          List<QueryDocumentSnapshot> reports =
              snapshot.data as List<QueryDocumentSnapshot>;
          // print(reports);

          List<Widget> reportChildren = [];
          for (int i = 0; i < reports.length; i++) {
            reportChildren.add(ReportRow(reports[i].id));
          }

          return ReportList(reportChildren);
        } else {
          return Text("Unable to get reports from database...");
        }
      },
    );
  }

  Widget ReportRow(String report_id) {
    return GestureDetector(
      onTap: () {
        navigateToReportPage(report_id);
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
                  padding: EdgeInsets.zero,
                  children: reportRows,
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
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            SizedBox(height: 70),
            BackButton(),
            ReportListSection()
          ],
        ),
      ),
    );
  }
}
