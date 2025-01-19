import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'dart:io';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key}); // Use super parameter

  @override
  CameraScreenState createState() => CameraScreenState();
}

class CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  late List<CameraDescription> _cameras;
  bool _isScanning = false;
  File? _capturedImage;

  @override
  void initState() {
    super.initState();
    initializeCamera();
  }

  Future<void> initializeCamera() async {
    try {
      _cameras = await availableCameras();
      _controller = CameraController(_cameras[0], ResolutionPreset.high);
      await _controller.initialize();
      setState(() {});
    } catch (e) {
      debugPrint("Error initializing camera: $e");
    }
  }

  Future<void> captureAndScan() async {
    if (!_controller.value.isInitialized) return;

    try {
      setState(() => _isScanning = true);

      // Capture the image
      final XFile imageFile = await _controller.takePicture();

      // Save the captured image
      _capturedImage = File(imageFile.path);

      // Simulate plant scanning (replace with actual AI model or API call)
      await Future.delayed(const Duration(seconds: 2)); // Simulated delay

      setState(() {
        _isScanning = false;
      });

      // Display scan result
      if (mounted) {
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text("Plant Scan Result"),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Display the captured image in dialog
                if (_capturedImage != null)
                  Image.file(
                    _capturedImage!,
                    width: 150,
                    height: 150,
                    fit: BoxFit.cover,
                  ),
                const SizedBox(height: 10),
                const Text(
                    "Plant detected: Example Plant"), // Replace with actual result
              ],
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text("OK"),
              ),
            ],
          ),
        );
      }
    } catch (e) {
      debugPrint("Error capturing image: $e");
      setState(() => _isScanning = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!_controller.value.isInitialized) {
      return const Center(child: CircularProgressIndicator());
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Plant Scanner')),
      body: Stack(
        children: [
          // Camera Preview
          CameraPreview(_controller),

          // Scanner Overlay
          Center(
            child: Container(
              width: 200, // 20:20 square scaled up for better visibility
              height: 200,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.green, width: 2),
                color: Colors.transparent,
              ),
            ),
          ),

          // Dimmed Background Outside Scanner
          Positioned.fill(
            child: IgnorePointer(
              child: Container(
                color: Colors.black
                    .withAlpha(128), // Updated withAlpha for transparency
                child: Center(
                  child: Container(
                    width: 200,
                    height: 200,
                    color: Colors.transparent, // Transparent square
                  ),
                ),
              ),
            ),
          ),

          // Loading Indicator
          if (_isScanning)
            Container(
              color: Colors.black
                  .withAlpha(128), // Updated withAlpha for transparency
              child: const Center(
                child: CircularProgressIndicator(color: Colors.white),
              ),
            ),

          // Capture Button
          Positioned(
            bottom: 20,
            left: 0,
            right: 0,
            child: Center(
              child: ElevatedButton(
                onPressed: _isScanning ? null : captureAndScan,
                child: const Text("Scan Plant"),
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
