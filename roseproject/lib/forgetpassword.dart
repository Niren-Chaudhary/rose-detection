import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class ForgotPasswordScreen extends StatefulWidget {
  const ForgotPasswordScreen({super.key});

  @override
  ForgotPasswordScreenState createState() => ForgotPasswordScreenState();
}

class ForgotPasswordScreenState extends State<ForgotPasswordScreen> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _newPasswordController = TextEditingController();
  final TextEditingController _confirmPasswordController =
      TextEditingController();
  final TextEditingController _otpController = TextEditingController();
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  // Method to verify the OTP and reset the password
  Future<void> resetPassword(String email, String otp, String newPassword,
      String confirmPassword) async {
    try {
      final response = await http.post(
        Uri.parse('http://192.168.1.95sx:8000/api/password-reset/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'email': email,
          'otp': otp,
          'new_password': newPassword,
          'confirm_password': confirmPassword,
        }),
      );

      final responseData = json.decode(response.body);
      if (response.statusCode == 200) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Password reset successful!')),
          );
          Navigator.pushReplacementNamed(context, '/login');
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
                content:
                    Text(responseData['error'] ?? 'Failed to reset password')),
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
        title: const Text('Forgot Password'),
        automaticallyImplyLeading: false,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              const Text('Reset your password'),
              const SizedBox(height: 20),

              TextFormField(
                controller: _otpController,
                decoration: const InputDecoration(hintText: 'OTP'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter the OTP sent to your email';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              TextFormField(
                controller: _newPasswordController,
                obscureText: true,
                decoration: const InputDecoration(hintText: 'New Password'),
                validator: (value) {
                  if (value == null || value.length < 6) {
                    return 'Password must be at least 6 characters long';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              TextFormField(
                controller: _confirmPasswordController,
                obscureText: true,
                decoration: const InputDecoration(hintText: 'Confirm Password'),
                validator: (value) {
                  if (value != _newPasswordController.text) {
                    return 'Passwords do not match';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState?.validate() ?? false) {
                    resetPassword(
                      _emailController.text,
                      _otpController.text,
                      _newPasswordController.text,
                      _confirmPasswordController.text,
                    );
                  }
                },
                child: const Text('Reset Password'),
              ),
              const SizedBox(height: 20),
              // Place the Generate OTP text and GestureDetector after the Reset Password button
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    'You must generate OTP for Reset Password',
                    style: TextStyle(fontSize: 14),
                  ),
                  const SizedBox(width: 8), // Space between text and button
                  GestureDetector(
                    onTap: () {
                      // Navigate to the OTP generation screen
                      Navigator.pushNamed(context, '/generateOtp');
                    },
                    child: const Text(
                      'Generate OTP',
                      style: TextStyle(
                        color: Colors.blue,
                        fontSize: 14, // Smaller font size
                        decoration: TextDecoration.underline, // Underline
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
