import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:test_application/main.dart';
import 'package:test_application/reportlistpage.dart';

class WeeklyReportPage extends StatefulWidget {
  const WeeklyReportPage({super.key});

  @override
  State<WeeklyReportPage> createState() => _WeeklyReportPageState();
}

class _WeeklyReportPageState extends State<WeeklyReportPage> {
  late User user;
  late Future<List<QueryDocumentSnapshot>> weeklyReports;

  void navigateToReportListPage(String weekId) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => ReportListPage(weekId: weekId)));
  }

  @override
  void initState() {
    super.initState();

    user = auth.currentUser!;
    weeklyReports = QueryWeeklyReports();
  }

  Future<List<QueryDocumentSnapshot>> QueryWeeklyReports() async {
    final db = await FirebaseFirestore.instance; // Connect to database

    List<QueryDocumentSnapshot> weeklyReportsList = [];

    // Ask the database for reports
    await db
        .collection("users_test")
        .doc(user.uid)
        .collection("weekly_reports")
        .get()
        .then(
      (querySnapshot) {
        for (var docSnapshot in querySnapshot.docs) {
          weeklyReportsList.add(docSnapshot);
          // print(docSnapshot.data());
        }
      },
      onError: (e) => print("Error completing: $e"),
    );

    weeklySort(weeklyReportsList);

    return weeklyReportsList;
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

        int a_num = int.parse(a.id.substring(4));
        int b_num = int.parse(b.id.substring(4));

        if (a_num < b_num) {
          min_idx = j;
        }
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

  Widget FutureTopWindow() {
    return FutureBuilder(
        future: weeklyReports,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            // render the report list on screen
            List reportList = snapshot.data as List;

            if (reportList.length == 0) {
              return Text("No reports available yet");
            } else {
              QueryDocumentSnapshot doc = reportList[0];
              Map data = doc.data() as Map;
              int warnings = data["warnings"];
              String weekId = reportList[0].id;

              return TopWindow(weekId, warnings);
            }
          } else {
            return Text("An error occurred. Could not get warnings");
          }
        });
  }

  Widget TopWindow(String weekId, int warnings) {
    return Container(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Text("Most Recent Report: " + weekId,
                    style:
                        TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ],
            ),
            SizedBox(height: 10),
            ClipRRect(
              borderRadius: BorderRadius.circular(7.0),
              child: Container(
                height: 200,
                color: const Color.fromRGBO(121, 134, 203, 1),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: <Widget>[
                    Column(
                      children: <Widget>[
                        SizedBox(height: 20),
                        Row(
                          children: <Widget>[
                            Text(
                              warnings.toString(),
                              style:
                                  TextStyle(fontSize: 40, color: Colors.white),
                            )
                          ],
                        ),
                        Row(
                          children: <Widget>[
                            Text(
                              "warnings",
                              style:
                                  TextStyle(fontSize: 20, color: Colors.white),
                            )
                          ],
                        ),
                        Row(
                          children: <Widget>[
                            ElevatedButton(
                              style: ButtonStyle(
                                backgroundColor:
                                    MaterialStateProperty.all(Colors.white),
                              ),
                              onPressed: () {
                                navigateToReportListPage(weekId);
                              },
                              child: Text("View more",
                                  style: TextStyle(
                                      color: const Color.fromRGBO(
                                          57, 73, 171, 1))),
                            ),
                          ],
                        ),
                      ],
                    ),
                    Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        Icon(
                          Icons.circle_outlined,
                          size: 150,
                          color: Colors.white,
                        )
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

  Widget FutureReportList() {
    return FutureBuilder(
        future: weeklyReports,
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
                Text("Past Reports",
                    style:
                        TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ],
            ),
            ClipRRect(
              borderRadius: BorderRadius.circular(7.0),
              child: Container(
                height: 200,
                child: ListView(
                  children: generateReportRows(reportList),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  List<Widget> generateReportRows(List reportList) {
    List<Widget> reportRows = [];
    for (int i = 1; i < reportList.length; i++) {
      reportRows.add(ReportRow(reportList[i].id));
    }
    return reportRows;
  }

  Widget ReportRow(String reportName) {
    return GestureDetector(
      onTap: () {
        // Navigate to the ReportListPage upon tapping a report row
        navigateToReportListPage(reportName);
      },
      child: Container(
          height: 35,
          margin: const EdgeInsets.only(bottom: 5.0),
          color: const Color.fromRGBO(159, 168, 218, 1),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.start,
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.only(left: 4.0),
                child: Icon(Icons.folder),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 10.0),
                child: Text(reportName),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 230, right: 4.0),
                child: Icon(
                  Icons.arrow_forward_ios,
                  size: 15,
                ),
              ),
            ],
          )),
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
            Icons.file_copy,
            color: const Color.fromRGBO(57, 73, 171, 1),
          ),
        ),
        title: Text(
          "Personal Reports",
          style: TextStyle(
              color: const Color.fromRGBO(57, 73, 171, 1),
              fontWeight: FontWeight.bold,
              fontSize: 24.0),
        ),
      ),
      body: Center(
        child: Column(
          children: <Widget>[
            SizedBox(height: 40),
            FutureTopWindow(),
            SizedBox(height: 40),
            FutureReportList(),
          ],
        ),
      ),
    );
  }
}
