import 'package:flutter/material.dart';
import 'package:test_application/splash.dart';
import 'package:google_fonts/google_fonts.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        textTheme: GoogleFonts.comfortaaTextTheme(Theme.of(context).textTheme),
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color.fromRGBO(121, 134, 203, 1),
        ),
        useMaterial3: true,
      ),
      home: const Splash(),
    );
  }
}
