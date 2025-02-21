import 'package:flutter/material.dart';

//import 'package:roseproject/features/camera/camera_screen.dart';
import 'package:roseproject/forgetpassword.dart';
import 'package:roseproject/generate_otp.dart';
import 'package:roseproject/home.dart';
import 'package:roseproject/login.dart';
import 'package:roseproject/signup.dart'; // Import the CameraScreen
import 'package:roseproject/service.dart';

void main() {
  runApp(
    MaterialApp(
      debugShowCheckedModeBanner: false,
      initialRoute: '/login',
      routes: {
        '/home': (context) => const HomePage(),
        '/login': (context) => const LoginScreen(),
        '/signup': (context) => const SignUpPage(),
        '/service': (context) => const ServicePage(),
        // '/camera': (context) => const CameraScreen(),
        '/reset': (context) => const ForgotPasswordScreen(),
        '/generateOtp': (context) => const GenerateOtp(),
      },
    ),
  );
}
