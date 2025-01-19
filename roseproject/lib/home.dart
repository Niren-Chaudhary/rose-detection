import 'package:flutter/material.dart';
import 'package:animate_do/animate_do.dart';

void main() => runApp(
      const MaterialApp(
        debugShowCheckedModeBanner: false,
        home: HomePage(),
      ),
    );

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return  Scaffold(
      body: Container(
        width: double.infinity,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            colors: [
              Colors.green.shade900,
              Colors.green.shade700,
              Colors.green.shade400,
            ],
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            const SizedBox(height: 80),
            Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  FadeInDown(
                    duration: const Duration(milliseconds: 1000),
                    child: const Text(
                      "WELCOME TO PLANTPAL",
                      style: TextStyle(
                        color: Color.fromARGB(255, 245, 241, 4),
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  const SizedBox(height: 10),
                  FadeInDown(
                    duration: const Duration(milliseconds: 1300),
                    child: const Text(
                      "Your ultimate plant care application",
                      style: TextStyle(color: Colors.white, fontSize: 30),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: Container(
                decoration: const BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(60),
                    topRight: Radius.circular(60),
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.greenAccent,
                      blurRadius: 50,
                      spreadRadius: 10,
                      offset: Offset(0, 10),
                    ),
                  ],
                ),
                child:Stack(
                  children: [
                   const Positioned(
                      top: 50,
                      left: 30,
                      child: Icon(
                        Icons.local_florist,
                        size: 100,
                        color:  Color.fromARGB(255, 247, 10, 10),
                      ),
                    ),
                    Positioned(
                      bottom: 80,
                      right: 30,
                      child: Icon(
                        Icons.grass,
                        size: 100,
                        color: Colors.green.shade100,
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(30),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                          FadeInUp(
                            duration: const Duration(milliseconds: 1500),
                            child: MaterialButton(
                              onPressed: () {
                                Navigator.pushNamed(context, '/services');
                              },
                              height: 50,
                              color: Colors.green[900],
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(50),
                              ),
                              child: const Center(
                                child: Text(
                                  "Services",
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 18,
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
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
}
