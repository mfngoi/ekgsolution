import 'package:flutter/material.dart';
import 'package:test_application/main.dart';
import 'package:test_application/reportlistpage.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

class ReportWeekListPage extends StatefulWidget {
  const ReportWeekListPage({super.key});

  @override
  State<ReportWeekListPage> createState() => _ReportWeekListPageState();
}

class _ReportWeekListPageState extends State<ReportWeekListPage> {
  late Future<List<QueryDocumentSnapshot>>
      weekly_reports; // List of weekly reports user has collected
  late User user;

  @override
  void initState() {
    super.initState();
    print("Entered ReportWeekListPage");

    user = auth.currentUser!;
    weekly_reports = QueryWeeklyReports();
  }

  Future<List<QueryDocumentSnapshot>> QueryWeeklyReports() async {
    List<QueryDocumentSnapshot> weekly_reports = [];
    final db = await FirebaseFirestore.instance; // Connect to db

    // Query all documents in reports collection in specific user
    await db
        .collection("users_test")
        .doc(user.uid)
        .collection("weekly_reports")
        .get()
        .then(
      (querySnapshot) {
        for (var docSnapshot in querySnapshot.docs) {
          weekly_reports.add(docSnapshot);
          // print(docSnapshot.id);
          // print(docSnapshot.data());
        }
      },
      onError: (e) => print("Error completing: $e"),
    );

    // Sort weeks from most recent to least recent
    weeklySort(weekly_reports);

    return weekly_reports;
  }

  void weeklySort(List<QueryDocumentSnapshot> weekly_reports) {
    int i, j, min_idx;

    // One by one move boundary of unsorted subarray
    for (i = 0; i < weekly_reports.length; i++) {
      // Find the minimum element in
      // unsorted array
      min_idx = i;
      for (j = i + 1; j < weekly_reports.length; j++) {
        QueryDocumentSnapshot a = weekly_reports[min_idx];
        QueryDocumentSnapshot b = weekly_reports[j];

        int a_week = int.parse(a.id.split("_")[0]);
        int a_year = int.parse(a.id.split("_")[1]);
        int b_week = int.parse(b.id.split("_")[0]);
        int b_year = int.parse(b.id.split("_")[1]);

        if (a_year <= b_year && a_week < b_week) min_idx = j;
      }

      // Swap the found minimum element
      // with the first element
      if (min_idx != i) {
        QueryDocumentSnapshot temp = weekly_reports[min_idx];

        weekly_reports.removeAt(min_idx);
        weekly_reports.insert(min_idx, weekly_reports[i]);

        weekly_reports.removeAt(i);
        weekly_reports.insert(i, temp);
      }
    }
  }

  Widget RecentReportTitle() {
    return FutureBuilder(
      future: weekly_reports,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          List<QueryDocumentSnapshot> weekly_reports =
              snapshot.data as List<QueryDocumentSnapshot>;
          String recent_id = weekly_reports[0].id;

          return Text("Recent Report: " + recent_id);
        } else {
          return Text("Unable to get recent report title from database...");
        }
      },
    );
  }

  Widget TopWindow(QueryDocumentSnapshot recent_week) {
    Map recent_data = recent_week.data() as Map;
    int warnings = recent_data["warnings"] as int;

    return Container(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                RecentReportTitle(),
              ],
            ),
            ClipRRect(
              borderRadius: BorderRadius.circular(7.0),
              child: Container(
                height: 200,
                color: Colors.purple,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: <Widget>[
                    Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        Text(
                          warnings.toString(),
                          style: TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 40.0),
                        ),
                        Text(
                          "Warnings",
                          style: TextStyle(color: Colors.white, fontSize: 20.0),
                        ),
                        SizedBox(height: 20),
                        ElevatedButton(
                          onPressed: () {
                            navigateToReportListPage(recent_week.id);
                          },
                          child: Text("View More"),
                          style: ButtonStyle(
                            backgroundColor:
                                MaterialStateProperty.all(Colors.white),
                          ),
                        ),
                      ],
                    ),
                    Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        Icon(
                          Icons.circle_outlined,
                          size: 100,
                          color: Colors.white,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget TopWindowSection() {
    return FutureBuilder(
      future: weekly_reports,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          List<QueryDocumentSnapshot> weekly_reports =
              snapshot.data as List<QueryDocumentSnapshot>;
          QueryDocumentSnapshot recent_week = weekly_reports[0];

          return TopWindow(recent_week);
        } else {
          return Text("Unable to get warnings from database...");
        }
      },
    );
  }

  void navigateToReportListPage(String weekly_report_id) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => ReportListPage(week_id: weekly_report_id)));
  }

  Widget ReportRow(String weekly_report_id) {
    return GestureDetector(
      onTap: () {
        navigateToReportListPage(weekly_report_id);
      },
      child: Container(
          margin: const EdgeInsets.only(bottom: 5.0),
          color: Color.fromARGB(255, 223, 173, 231),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: <Widget>[
              Icon(Icons.settings),
              Text(weekly_report_id),
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
      future: weekly_reports,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          List<QueryDocumentSnapshot> weekly_reports =
              snapshot.data as List<QueryDocumentSnapshot>;
          // print(reports);

          List<Widget> reportChildren = [];
          for (int i = 1; i < weekly_reports.length; i++) {
            reportChildren.add(ReportRow(weekly_reports[i].id));
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
            TopWindowSection(),
            SizedBox(height: 20),
            ReportListSection(),
            SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}
