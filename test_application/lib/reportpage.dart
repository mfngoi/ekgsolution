import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:test_application/main.dart';

class ReportPage extends StatefulWidget {
  final String week_id;
  final String report_id;
  const ReportPage({super.key, required this.week_id, required this.report_id});

  @override
  State<ReportPage> createState() => _ReportPageState();
}

class _ReportPageState extends State<ReportPage> {
  late Future<Map> report;
  late User user;

  @override
  void initState() {
    super.initState();
    print("Entered ReportPage: ");

    user = auth.currentUser!;
    report = QueryReport();
  }

  Future<Map> QueryReport() async {
    final db = await FirebaseFirestore.instance; // Connect to db

    Map report = await db
        .collection("users_test")
        .doc(user.uid)
        .collection("weekly_reports")
        .doc(widget.week_id)
        .collection("reports")
        .doc(widget.report_id)
        .get()
        .then(
      (DocumentSnapshot doc) {
        final data = doc.data()
            as Map<String, dynamic>; // Gives you the document as a Map
        return data;
      },
      onError: (e) => print("Error getting document: $e"),
    );

    return report;
  }

  Widget BackButton() {
    return ElevatedButton(
      onPressed: () {
        Navigator.pop(context);
      },
      child: Text("Back"),
    );
  }

  Widget TopWindowSection() {
    return FutureBuilder(
      future: report,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          Map report = snapshot.data as Map;
          List avg_heartbeat = report["avg_heartbeat"] as List;
          // print(avg_heartbeat);

          return TopWindow(avg_heartbeat);
        } else {
          return Text("Unable to get avg heartbeat from database...");
        }
      },
    );
  }

  Widget TopWindow(List avg_heartbeat) {
    return Container(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(7.0),
              child: Container(
                height: 200,
                color: const Color.fromARGB(255, 223, 173, 231),
                child: LineChart(
                  LineChartData(
                    lineBarsData: [
                      LineChartBarData(
                        spots: generatePoints(avg_heartbeat),
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

  Widget BottomWindowSection() {
    return FutureBuilder(
      future: report,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          Map report = snapshot.data as Map;

          return BottomWindow(report);
        } else {
          return Text("Unable to get recent report from database...");
        }
      },
    );
  }

  Widget BottomWindow(Map report) {
    return Container(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(7.0),
              child: Container(
                height: 200,
                width: double.infinity,
                color: const Color.fromARGB(255, 223, 173, 231),
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: <Widget>[
                      Text("Condition: " + report["condition"]),
                      Text("PR Interval: " + report["pr_interval"].toString()),
                      Text("QT Interval: " + report["qt_interval"].toString()),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  List<FlSpot> generatePoints(List values) {
    List<FlSpot> points = [];

    for (int i = 0; i < values.length; i++) {
      points.add(new FlSpot(i.toDouble(), values[i].toDouble()));
    }
    return points;
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
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 30.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: <Widget>[
                  Text("AVG Heartbeat"),
                ],
              ),
            ),
            TopWindowSection(),
            SizedBox(height: 20),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 30.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: <Widget>[
                  Text("Additional Information"),
                ],
              ),
            ),
            BottomWindowSection(),
          ],
        ),
      ),
    );
  }
}
