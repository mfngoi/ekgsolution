import 'package:flutter/material.dart';

final List<String> warningList = [
  "warngin1",
  "warning2",
  "warning3",
  "warning4",
  "warning5",
  "warning6",
  "warning7",
];

final List<String> currentWarnings = [
  warningList[0], // "warngin1",
  warningList[2], // "warning3",
  warningList[4], // "warning5"
  warningList[5], // "warning6",
];

class ReportPage extends StatefulWidget {
  const ReportPage({super.key});
  @override
  State<ReportPage> createState() => _ReportPageState();
}

class _ReportPageState extends State<ReportPage> {
  Widget BackButton() {
    return ElevatedButton(
      onPressed: () {
        Navigator.pop(context);
      },
      child: Text("Back"),
    );
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
                Text("Report XX/XX/XX"),
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

  Widget Warnings() {
    List<Widget> warnings = [];

    for (int i = 0; i < currentWarnings.length; i++) {
      warnings.add(Text(currentWarnings[i]));
    }

    return Column(children: warnings);
  }

  Widget WarningList() {
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
                child: Warnings(),
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
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            BackButton(),
            TopWindow(),
            WarningList(),
          ],
        ),
      ),
    );
  }
}
