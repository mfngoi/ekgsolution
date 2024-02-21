import 'package:flutter/material.dart';

class NewsPage extends StatefulWidget {
  // Reconsider news page parameters
  final Map<String, dynamic> newsData;
  const NewsPage({super.key, required this.newsData});

  @override
  State<NewsPage> createState() => _NewsPageState();
}

class _NewsPageState extends State<NewsPage> {
  Widget NewsTitle() {
    return Container(
      height: 120,
      width: double.infinity,
      decoration: BoxDecoration(
        image: DecorationImage(
          image: NetworkImage(widget.newsData["image"]!),
          fit: BoxFit.cover,
        ),
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(25.0),
          topRight: Radius.circular(25.0),
        ),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: <Widget>[
          Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: <Widget>[
              BackButton(),
            ],
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.start,
            children: <Widget>[
              Padding(
                padding: EdgeInsets.only(left: 20.0, bottom: 10.0),
                child: Text(
                  widget.newsData["article_title"]!,
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 35.0,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget BackButton() {
    return ElevatedButton(
      onPressed: () {
        Navigator.pop(context);
      },
      child: Icon(Icons.close),
      style: ButtonStyle(
        shape: MaterialStateProperty.all(CircleBorder()),
        backgroundColor: MaterialStateProperty.all<Color>(Colors.transparent),
        foregroundColor: MaterialStateProperty.all<Color>(Colors.white),
      ),
    );
  }

  Widget NewsContent() {
    return Expanded(
      child: Container(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: ListView(
          padding: EdgeInsets.only(top: 10),
          children: <Widget>[
            Text(
              widget.newsData["article_content"]!,
              textAlign: TextAlign.left,
              style: TextStyle(
                color: Colors.black,
                fontSize: 18,
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
            SizedBox(height: 90.0),
            NewsTitle(),
            NewsContent(),
          ],
        ),
      ),
    );
  }
}
