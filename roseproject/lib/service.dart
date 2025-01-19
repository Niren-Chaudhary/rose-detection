import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:dio/dio.dart'; // For HTTP requests
import 'dart:developer' as developer; // For logging
import 'package:shared_preferences/shared_preferences.dart'; // For token storage

class ServicePage extends StatefulWidget {
  const ServicePage({super.key});

  @override
  State<ServicePage> createState() => _ServicePageState();
}

class _ServicePageState extends State<ServicePage> {
  File? _selectedImage;
  String? _serviceResult;

  @override
  void initState() {
    super.initState();
    _checkAuthentication(); // Check authentication on page load
  }

  // Check if the user is authenticated
  Future<void> _checkAuthentication() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    if (token == null) {
      // If no token is found, redirect to the login page
      if (mounted) {
        WidgetsBinding.instance.addPostFrameCallback((_) {
          Navigator.pushReplacementNamed(context, '/login');
        });
      }
    }
  }

  // Upload the selected image to the server
  Future<void> _uploadImage() async {
    final ImagePicker picker = ImagePicker();
    final XFile? pickedFile =
        await picker.pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        _selectedImage = File(pickedFile.path);
        _serviceResult =
            'This is a service result description'; // Simulated result
      });

      // Prepare and send the image to the backend
      try {
        final prefs = await SharedPreferences.getInstance();
        final token = prefs.getString('access_token'); // Retrieve the token

        if (token == null) {
          // If no token is found, redirect to the login page
          if (mounted) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              Navigator.pushReplacementNamed(context, '/login');
            });
          }
          return;
        }

        // Prepare the form data with the image
        FormData formData = FormData.fromMap({
          "image": await MultipartFile.fromFile(_selectedImage!.path,
              filename: _selectedImage!.path.split('/').last),
        });

        // Send the request to the backend with the token
        Dio dio = Dio();
        var response = await dio.post(
          'http://localhost:8000/upload/', // Replace with your server URL
          data: formData,
          options: Options(headers: {"Authorization": "Bearer $token"}),
        );

        if (response.statusCode == 200) {
          developer.log('Upload Successful');
        } else {
          developer.log('Upload Failed');
        }
      } catch (e) {
        developer.log('Error uploading image: $e');
      }
    }
  }

  // Logout and clear the token
  void _logout(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token'); // Remove the authentication token
    if (mounted) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        Navigator.pushReplacementNamed(
            context, '/login'); // Redirect to login page
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Service Detection'),
        automaticallyImplyLeading: false,
        actions: [
          PopupMenuButton<String>(
            onSelected: (String value) {
              if (value == 'logout') {
                _logout(context);
              }
            },
            itemBuilder: (BuildContext context) {
              return [
                const PopupMenuItem<String>(
                  value: 'logout',
                  child: Text('Logout'),
                ),
              ];
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            const Text(
              'Upload an Image',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _uploadImage,
              child: const Text('Browse Files'),
            ),
            const SizedBox(height: 20),
            if (_selectedImage != null) ...[
              Text(
                _selectedImage!.path.split('/').last,
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              kIsWeb
                  ? Image.network(_selectedImage!.path)
                  : Image.file(
                      _selectedImage!,
                      height: 150,
                    ),
              const SizedBox(height: 10),
              Text(
                _serviceResult ?? '',
                style:
                    const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
