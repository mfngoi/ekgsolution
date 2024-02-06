import 'package:flutter/material.dart';

final List<Map> newsList = [
  {
    "title": "News 1",
    "content":
        "Fire is a dynamic chemical reaction that releases heat and light as a result of the combustion of combustible materials. It has been a symbol of energy, transformation, and destruction throughout human history. Fire's mesmerizing dance embodies both the creative and destructive forces of nature, offering warmth and illumination while capable of consuming everything in its path."
  },
  {
    "title": "News 2",
    "content":
        "Earth, our home planet, is a complex and interconnected system of land, water, and atmosphere. It sustains life through a delicate balance of ecosystems and natural processes. From towering mountains to vast oceans, Earth's diverse landscapes provide habitats for countless species. Human activities profoundly impact the Earth, influencing its climate, biodiversity, and overall health. The importance of environmental stewardship has become increasingly evident as societies strive to achieve sustainability and protect the planet for future generations."
  },
  {
    "title": "News 3",
    "content":
        "Air, a mixture of gases primarily composed of nitrogen and oxygen, envelops the Earth, creating the atmosphere crucial for sustaining life. Beyond its role in respiration, air influences weather patterns and climatic conditions. The movement of air masses, driven by atmospheric pressure differentials, results in winds and plays a pivotal role in shaping the Earth's climate. Air pollution, caused by human activities, poses challenges to both environmental and public health, emphasizing the importance of responsible resource management and pollution control."
  },
  {
    "title": "News 4",
    "content":
        "Water, covering about 71% of the Earth's surface, is essential for all forms of life. It exists in various forms, from oceans and rivers to ice caps and clouds, facilitating the planet's diverse ecosystems. Water's unique properties, such as its ability to dissolve substances and moderate temperature, make it indispensable for biochemical processes and climate regulation. However, issues like water scarcity, pollution, and climate change threaten this precious resource, highlighting the need for sustainable water management practices worldwide."
  },
  {
    "title": "News 5",
    "content":
        "Plasma, often referred to as the fourth state of matter, exists at extremely high temperatures, causing atoms to ionize and creating a charged gas composed of ions and electrons. Commonly found in stars, lightning, and certain human-made technologies like plasma TVs, plasma exhibits unique electromagnetic properties. Its role extends from powering the sun's fusion reactions to enabling advanced technologies on Earth, emphasizing its importance in both astrophysics and technological innovation."
  },
  {
    "title": "News 6",
    "content":
        "\t Force, in physics, is a vector quantity representing the interaction that causes an object's acceleration or deformation. Governed by Newton's laws, forces can be gravitational, electromagnetic, or arising from contact between objects. Forces are fundamental in understanding the motion of celestial bodies, the functioning of machines, and the dynamics of everyday life. From the pull of gravity to the tension in a stretched spring, forces shape the physical world, and their comprehension is essential for advancing scientific knowledge and technological applications."
  },
];

class NewsPage extends StatefulWidget {
  final int index;
  final String imageLink;
  const NewsPage({super.key, required this.index, required this.imageLink});

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
          image: NetworkImage(widget.imageLink),
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
                  newsList[widget.index]["title"],
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
              newsList[widget.index]["content"],
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
