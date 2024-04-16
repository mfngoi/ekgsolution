import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:test_application/main.dart';

class ReportPage extends StatefulWidget {
  final String weekId;
  final String reportId;
  const ReportPage({super.key, required this.weekId, required this.reportId});
  @override
  State<ReportPage> createState() => _ReportPageState();
}

class _ReportPageState extends State<ReportPage> {
  late User user;
  late Future<Map> report;
  late Future<String> prediction;

  @override
  void initState() {
    super.initState();

    user = auth.currentUser!;
    report = QueryReport();
    prediction = QueryPrediction();
  }

  Future<Map> QueryReport() async {
    final db = await FirebaseFirestore.instance; // Connect to database
    // Ask the database for reports
    Map report = await db
        .collection("users_test")
        .doc(user.uid)
        .collection("weekly_reports")
        .doc(widget.weekId)
        .collection("reports")
        .doc(widget.reportId)
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

  Future<String> QueryPrediction() async {
    final db = await FirebaseFirestore.instance; // Connect to database
    String prediction = "";
    // Ask the database for reports
    await db
        .collection("users_test")
        .doc(user.uid)
        .collection("weekly_reports")
        .doc(widget.weekId)
        .collection("reports")
        .doc(widget.reportId)
        .get()
        .then(
      (DocumentSnapshot doc) {
        final data = doc.data()
            as Map<String, dynamic>; // Gives you the document as a Map
        prediction = data["condition"];
      },
      onError: (e) => print("Error getting document: $e"),
    );
    return prediction;
  }

  Widget BackButton(BuildContext context) {
    return IconButton(
      icon: Icon(Icons.arrow_back, color: Color.fromRGBO(57, 73, 171, 1)),
      onPressed: () {
        Navigator.of(context).pop();
      },
    );
  }

  Widget FutureTopWindow() {
    return FutureBuilder(
        future: report,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            Map report = snapshot.data as Map;
            List avg_heartbeat = report["avg_heartbeat"] as List;
            return TopWindow(avg_heartbeat);
          } else {
            return Text("Error occured. Unable to get average heartbeats");
          }
        });
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
                color: const Color.fromRGBO(197, 202, 233, 1),
                child: LineChart(
                  LineChartData(
                    lineBarsData: [
                      LineChartBarData(
                        spots: createPoints(avg_heartbeat),
                      ),
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

  List<FlSpot> createPoints(List avg_heartbeat) {
    List<FlSpot> points = [];
    for (int i = 0; i < avg_heartbeat.length; i++) {
      points.add(new FlSpot(i.toDouble(), avg_heartbeat[i].toDouble()));
    }
    return points;
  }

  Widget DisplayWarning(String prediction) {
    if (prediction == "Placebo") {
      return Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Text("No Warnings"),
          ],
        ),
      );
    } else {
      return Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Text(
                "Warning! Detected ECG irregularies suggest potential substance consumption beyond safe levels."),
          ],
        ),
      );
    }
  }

  Widget FutureWarning() {
    return FutureBuilder(
        future: prediction,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            String prediction = snapshot.data as String;
            return DisplayWarning(prediction);
          } else {
            return Text("Error occured. Unable to get warnings");
          }
        });
  }

  Widget FutureBottomWindow() {
    return FutureBuilder(
        future: report,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            Map report = snapshot.data as Map;

            return BottomWindow(report);
          } else {
            return Text("Error occured. Unable to get reports");
          }
        });
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
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    Text("Your Average P Wave: " +
                        (25 * report["pr_interval"]).toString() +
                        " milliseconds"),
                    Text("Your Average Corrected QT Interval: " +
                        (25 * report["qt_interval"]).toString() +
                        " milliseconds"),
                    Text("Demographic paragraph")
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
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            SizedBox(height: 70),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 30.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: <Widget>[BackButton(context)],
              ),
            ),
            SizedBox(height: 40),
            FutureTopWindow(),
            SizedBox(height: 20),
            FutureWarning(),
            SizedBox(height: 20),
            FutureBottomWindow(),
          ],
        ),
      ),
    );
  }
}
