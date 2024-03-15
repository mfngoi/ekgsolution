import 'package:flutter/material.dart';
import 'package:test_application/main.dart';
import 'package:test_application/reportpage.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:fl_chart/fl_chart.dart';

class ReportListPage extends StatefulWidget {
  const ReportListPage({super.key});

  @override
  State<ReportListPage> createState() => _ReportListPageState();
}

class _ReportListPageState extends State<ReportListPage> {
  late Future<List> reports; // List of reports user has collected
  late Future<List> avg_heartbeat;
  late User user;

  @override
  void initState() {
    super.initState();
    user = auth.currentUser!;
    reports = QueryReports();
    avg_heartbeat = QueryAvgHeartBeat();
  }

  Future<List> QueryReports() async {
    List reports = [];
    final db = await FirebaseFirestore.instance; // Connect to db

    // Query all documents in reports collection in specific user
    await db
        .collection("users_test")
        .doc(user.uid)
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

  Future<List> QueryAvgHeartBeat() async {
    List reports = [];
    final db = await FirebaseFirestore.instance; // Connect to db

    // Query all documents in reports collection in specific user
    await db
        .collection("users_test")
        .doc(user.uid)
        .collection("reports")
        .get()
        .then(
      (querySnapshot) {
        for (var docSnapshot in querySnapshot.docs) {
          reports.add(docSnapshot.id);
        }
      },
      onError: (e) => print("Error completing: $e"),
    );

    // Sort report from most recent to least recent
    reports.sort((a, b) => DateTime.parse(b).compareTo(DateTime.parse(a)));

    // Query avg heartbeat signal from recent report id
    String recent_report = reports[0];
    List recent_avg_heartbeat = [];
    await db
        .collection("users_test")
        .doc(user.uid)
        .collection("reports")
        .doc(recent_report)
        .get()
        .then(
      (DocumentSnapshot doc) {
        final data = doc.data()
            as Map<String, dynamic>; // Gives you the document as a Map
        // print(data);
        // print(data["avg_heartbeat"]);
        for (int i=0; i< data["avg_heartbeat"].length; i++) {
          recent_avg_heartbeat.add(data["avg_heartbeat"][i]);
        }
      },
      onError: (e) => print("Error getting document: $e"),
    );
    // print(recent_avg_heartbeat);
    return recent_avg_heartbeat;
  }

  List<FlSpot> generatePoints(List values) {
    List<FlSpot> points = [];

    for (int i = 0; i < values.length; i++) {
      points.add(new FlSpot(i.toDouble(), values[i].toDouble()));
    }
    return points;
  }

  Widget TopWindow(List recent_avg_hearbeat) {
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
                color: const Color.fromARGB(255, 223, 173, 231),
                child: LineChart(
                  LineChartData(
                    lineBarsData: [
                      LineChartBarData(
                        spots: generatePoints(recent_avg_hearbeat),
                      ),
                    ],
                    // read about it in the LineChartData section
                  ),
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
      future: avg_heartbeat,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          List avg_heartbeat = snapshot.data as List;
          // print(avg_heartbeat);

          return TopWindow(avg_heartbeat);
        } else {
          return Text("Unable to get recent report from database...");
        }
      },
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
