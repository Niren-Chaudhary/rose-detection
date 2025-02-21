import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class GenerateOtp extends StatefulWidget {
  const GenerateOtp({super.key});

  @override
  GenerateOtpState createState() => GenerateOtpState();
}

class GenerateOtpState extends State<GenerateOtp> {
  final TextEditingController _emailController = TextEditingController();
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  // Method to request OTP
  Future<void> requestOtp(String email) async {
    try {
      final response = await http.post(
        Uri.parse('http://192.168.1.95:8000/api/send-otp/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'email': email}),
      );

      final responseData = json.decode(response.body);

      if (mounted) {
        if (response.statusCode == 200) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('OTP sent to your email!')),
          );

          // Navigate back to the previous screen after OTP is successfully sent
          Navigator.pop(context);
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(responseData['error'] ?? 'Failed to send OTP'),
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Generate OTP Page'),
        automaticallyImplyLeading: false,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              const Text('Enter your email to receive OTP'),
              const SizedBox(height: 20),
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(hintText: 'Email'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter your email';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState?.validate() ?? false) {
                    // Request OTP and handle navigation after success
                    requestOtp(_emailController.text);
                  }
                },
                child: const Text('Send OTP'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
