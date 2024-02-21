import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:carousel_slider/carousel_slider.dart';
import 'package:test_application/reportlistpage.dart';
import 'package:test_application/newspage.dart';
import 'package:http/http.dart' as http;

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late Future<Map> newsInfo;

  @override
  void initState() {
    super.initState();
    newsInfo = getNewsInfo();
  }

  Future<Map> getNewsInfo() async {
    try {
      String urlLink = "http://10.0.2.2:5000/newsinfo";
      // Define destination link
      Uri link = Uri.parse(urlLink);

      // Send the request and get a response back
      final server_response = await http.get(link);

      final Map<String, dynamic> newsInfo = jsonDecode(server_response.body);

      print(newsInfo);

      return newsInfo;
    } catch (e) {
      print('error caught: $e');
    }

    return {};
  }

  Future<String> triggerDevice() async {
    http.post(Uri.parse(
        'https://api.particle.io/v1/devices/e00fce684219e0e249d5bc42/readECG?access_token=40c9617030f65832904eb99528de3da5e7ebfe66'));
    return "Sent Request";
  }

  void navigateToReportPage() {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => const ReportListPage()));
  }

  void navigateToNewsPage(Map<String, dynamic> newsData) {
    Navigator.of(context).push(
        MaterialPageRoute(builder: (context) => NewsPage(newsData: newsData)));
  }

  // List<Widget> CreateImageSlides(List<String> imgList) {
  //   List<Widget> imageSlides = [];
  //   for (int i = 0; i < imgList.length; i++) {
  //     Widget imageCard = CustomGestureDetector(imgList, i);
  //     imageSlides.add(imageCard);
  //   }

  //   return imageSlides;
  // }

  Widget CustomGestureDetector(Map<String, dynamic> newsData) {
    // FUTURE -> should accept title and content as well
    return GestureDetector(
      onTap: () {
        navigateToNewsPage(
            newsData); // FUTURE -> should accept title and content
      },
      child: Container(
        child: Container(
          margin: EdgeInsets.all(5.0),
          child: ClipRRect(
            borderRadius: BorderRadius.all(Radius.circular(5.0)),
            child: Stack(
              fit: StackFit.expand,
              children: <Widget>[
                Image.network(newsData["image"]!,
                    fit: BoxFit.cover, width: 1000.0),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget DianoseNow() {
    return Container(
      width: 300,
      child: ElevatedButton(
        style: ButtonStyle(
          shape: MaterialStateProperty.all<RoundedRectangleBorder>(
            RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(
                  10.0), // Adjust the value to control the roundness
            ),
          ),
          padding: MaterialStateProperty.all<EdgeInsetsGeometry>(
              EdgeInsets.all(16.0)),
          backgroundColor: MaterialStateProperty.all<Color>(Colors.purple),
          foregroundColor: MaterialStateProperty.all<Color>(Colors.white),
        ),
        onPressed: triggerDevice,
        child: Text(
          "Diagnoze Now",
          textAlign: TextAlign.center,
        ),
      ),
    );
  }

  Widget CheckReport() {
    return Container(
      width: 300,
      child: ElevatedButton(
        style: ButtonStyle(
          shape: MaterialStateProperty.all<RoundedRectangleBorder>(
            RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(
                  10.0), // Adjust the value to control the roundness
            ),
          ),
          padding: MaterialStateProperty.all<EdgeInsetsGeometry>(
              EdgeInsets.all(16.0)),
          backgroundColor: MaterialStateProperty.all<Color>(Colors.purple),
          foregroundColor: MaterialStateProperty.all<Color>(Colors.white),
        ),
        onPressed: navigateToReportPage,
        child: Text(
          "Check Report",
          textAlign: TextAlign.center,
        ),
      ),
    );
  }

  // Modify NewsCarousel to accept "items"
  Widget NewsCarousel(List<Widget> newsCards) {
    // FUTURE
    return Container(
      child: CarouselSlider(
        options: CarouselOptions(
          height: 370,
          autoPlay: true,
          aspectRatio: 2.0,
          enlargeCenterPage: true,
        ),
        items: newsCards,
      ),
    );
  }

  Widget NewsSection() {
    return FutureBuilder(
      future: newsInfo,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          Map newsInfo = snapshot.data as Map;

          final List news = newsInfo.keys.toList();
          List<Widget> newsCards = [];
          for (int i = 0; i < news.length; i++) {
            newsCards.add(CustomGestureDetector(newsInfo[news[i]]));
          }

          return NewsCarousel(newsCards);
        } else {
          return Text("Unable to get news from server...");
        }
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            SizedBox(height: 60),
            Text(
              "Σureka",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 80,
              ),
            ),
            SizedBox(height: 70),
            DianoseNow(),
            SizedBox(height: 20),
            CheckReport(),
            SizedBox(height: 70),
            NewsSection(),
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
