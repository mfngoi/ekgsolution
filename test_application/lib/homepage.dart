import 'package:flutter/material.dart';
import 'package:carousel_slider/carousel_slider.dart';
import 'package:test_application/reportlistpage.dart';
import 'package:test_application/newspage.dart';

final List<String> imgList = [
  'https://images.unsplash.com/photo-1520342868574-5fa3804e551c?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=6ff92caffcdd63681a35134a6770ed3b&auto=format&fit=crop&w=1951&q=80',
  'https://images.unsplash.com/photo-1522205408450-add114ad53fe?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=368f45b0888aeb0b7b08e3a1084d3ede&auto=format&fit=crop&w=1950&q=80',
  'https://images.unsplash.com/photo-1519125323398-675f0ddb6308?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=94a1e718d89ca60a6337a6008341ca50&auto=format&fit=crop&w=1950&q=80',
  'https://images.unsplash.com/photo-1523205771623-e0faa4d2813d?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=89719a0d55dd05e2deae4120227e6efc&auto=format&fit=crop&w=1953&q=80',
  'https://images.unsplash.com/photo-1508704019882-f9cf40e475b4?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=8c6e5e3aba713b17aa1fe71ab4f0ae5b&auto=format&fit=crop&w=1352&q=80',
  'https://images.unsplash.com/photo-1519985176271-adb1088fa94c?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=a0c8d632e977f94e5d312d9893258f59&auto=format&fit=crop&w=1355&q=80'
];

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  void navigateToReportPage() {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => const ReportListPage()));
  }

  void navigateToNewsPage(int newsIndex) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) =>
            NewsPage(index: newsIndex, imageLink: imgList[newsIndex])));
  }

  List<Widget> CreateImageSlides(List<String> imgList) {
    List<Widget> imageSlides = [];
    for (int i = 0; i < imgList.length; i++) {
      Widget imageCard = CustomGestureDetector(imgList, i);
      imageSlides.add(imageCard);
    }

    return imageSlides;
  }

  Widget CustomGestureDetector(List<String> imgList, int index) {
    return GestureDetector(
      onTap: () {
        navigateToNewsPage(index);
      },
      child: Container(
        child: Container(
          margin: EdgeInsets.all(5.0),
          child: ClipRRect(
            borderRadius: BorderRadius.all(Radius.circular(5.0)),
            child: Stack(
              fit: StackFit.expand,
              children: <Widget>[
                Image.network(imgList[index], fit: BoxFit.cover, width: 1000.0),
                // Positioned(
                //   bottom: 0.0,
                //   left: 0.0,
                //   right: 0.0,
                //   child: Container(
                //     decoration: BoxDecoration(
                //       gradient: LinearGradient(
                //         colors: [
                //           Color.fromARGB(200, 0, 0, 0),
                //           Color.fromARGB(0, 0, 0, 0)
                //         ],
                //         begin: Alignment.bottomCenter,
                //         end: Alignment.topCenter,
                //       ),
                //     ),
                //     padding: EdgeInsets.symmetric(
                //         vertical: 10.0, horizontal: 20.0),
                //     child: Text(
                //       'No. ${imgList.indexOf(item)} image',
                //       style: TextStyle(
                //         color: Colors.white,
                //         fontSize: 20.0,
                //         fontWeight: FontWeight.bold,
                //       ),
                //     ),
                //   ),
                // ),
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
        onPressed: null,
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

  Widget NewsCarousel() {
    return Container(
      child: CarouselSlider(
        options: CarouselOptions(
          height: 370,
          autoPlay: true,
          aspectRatio: 2.0,
          enlargeCenterPage: true,
        ),
        items: CreateImageSlides(imgList),
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
            NewsCarousel(),
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
