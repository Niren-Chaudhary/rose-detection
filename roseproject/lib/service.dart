import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:typed_data';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:logger/logger.dart';

class ServicePage extends StatefulWidget {
  const ServicePage({super.key});

  @override
  State<ServicePage> createState() => _ServicePageState();
}

class _ServicePageState extends State<ServicePage> {
  Uint8List? _selectedImageBytes;
  String? _serviceResult;
  bool _isLoading = false;
  bool _isRose = false;
  final String baseUrl = 'http://127.0.0.1:8000/api/classify/';
  final Logger _logger = Logger();

  String _expandedSection = ''; // Track which section is expanded

  @override
  void initState() {
    super.initState();
    _checkAuthentication();
  }

  Future<void> _checkAuthentication() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    if (token == null) {
      if (mounted) {
        WidgetsBinding.instance.addPostFrameCallback((_) {
          Navigator.pushReplacementNamed(context, '/login');
        });
      }
    }
  }

  Future<void> _uploadImage() async {
    final picker = ImagePicker();
    final XFile? pickedFile =
        await picker.pickImage(source: ImageSource.gallery);

    if (pickedFile == null) {
      setState(() {
        _serviceResult = 'No image selected.';
        _isRose = false;
      });
      return;
    }

    final imageBytes = await pickedFile.readAsBytes();
    setState(() {
      _selectedImageBytes = imageBytes;
      _isLoading = true;
      _serviceResult = null;
    });

    try {
      final formData = FormData.fromMap({
        'image': MultipartFile.fromBytes(imageBytes, filename: pickedFile.name),
      });

      final dio = Dio();
      final response = await dio.post(baseUrl, data: formData);

      if (response.statusCode == 200) {
        final data = response.data;
        _logger.d('Response data: $data');

        setState(() {
          _isRose = data['is_rose'] ?? false;
          _serviceResult = _isRose
              ? 'The image is a rose. Disease: ${data['disease_status']}'
              : 'The image is not a rose.';
        });
      } else {
        setState(() {
          _serviceResult = 'Error: ${response.data ?? 'Unknown error.'}';
          _isRose = false;
        });
      }
    } catch (e) {
      setState(() {
        _serviceResult = 'Error uploading image: ${e.toString()}';
        _isRose = false;
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _logout(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
    if (mounted) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        Navigator.pushReplacementNamed(context, '/login');
      });
    }
  }

  void _toggleSection(String section) {
    setState(() {
      _expandedSection = (_expandedSection == section) ? '' : section;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Service Detection'),
        automaticallyImplyLeading: false,
        actions: [
          PopupMenuButton<String>(onSelected: (String value) {
            if (value == 'logout') {
              _logout(context);
            }
          }, itemBuilder: (BuildContext context) {
            return [
              const PopupMenuItem<String>(
                value: 'logout',
                child: Text('Logout'),
              ),
            ];
          }),
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
              onPressed: _isLoading ? null : _uploadImage,
              child: const Text('Browse Files'),
            ),
            const SizedBox(height: 20),
            if (_isLoading) const CircularProgressIndicator(),
            if (_selectedImageBytes != null && !_isLoading) ...[
              const SizedBox(height: 10),
              Image.memory(_selectedImageBytes!, height: 150),
              const SizedBox(height: 10),
              Text(
                _serviceResult ?? 'No result yet',
                style:
                    const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 20),
              if (_isRose) ...[
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton(
                      onPressed: () => _toggleSection('Black Spot'),
                      child: const Text('Black Spot'),
                    ),
                    ElevatedButton(
                      onPressed: () => _toggleSection('Downy Mildew'),
                      child: const Text('Downy Mildew'),
                    ),
                    ElevatedButton(
                      onPressed: () => _toggleSection('Fresh Leaf'),
                      child: const Text('Fresh Leaf'),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                if (_expandedSection == 'Black Spot')
                  const Text(
                      'BLACK SPOT \n 1. Prune Infected Areas:\n \t Remove and dispose of infected leaves, stems, and flowers. This helps prevent the spread of the disease and improves airflow around the plant.\n 2. Fungicide Application:\n \t Use fungicides like Chlorothalonil, Mancozeb, or Tebuconazole to control the disease.\n 3. Improve Air Circulation:\n \t Ensure proper spacing between plants and prune away any excess growth to allow better airflow. This reduces humidity around the plant, which can help prevent fungal growth.\n 4. Watering Practices:\n \t Avoid overhead watering, as water droplets can spread the spores. Water at the base of the plant to keep the leaves dry, especially during the evening or night, when the disease thrives in moisture.\n 5. Mulching and Soil Care:\n \t Apply a layer of mulch around the base of the plant to keep the soil healthy and prevent spores from splashing onto the plant. Use compost or well-rotted manure to enrich the soil and improve overall plant health.'),
                if (_expandedSection == 'Downy Mildew')
                  const Text(
                      'DOWNY MILDEW \n 1. Fungicide Treatment:\n \t Use fungicides that are effective against downy mildew, such as Mancozeb, Copper-based sprays, or Chlorothalonil.\n 2. Pruning Infected Areas:\n \t Remove and dispose of infected leaves and stems to prevent the spread of the disease.'),
                if (_expandedSection == 'Fresh Leaf')
                  const Text(
                      ' FRESH LEAF \n 1.Hydration:\n \t Place the stem in water or wrap it in a damp paper towel to maintain moisture and prevent wilting.\n 2.Cool Environment:\n \t Keep the leaf in a cool, shaded area, away from direct sunlight or heat, to slow down dehydration.\n 3.Seal & Store:\n \t If you need to store it, place the leaf in an airtight container or a zip-lock bag in the refrigerator to preserve its freshness'),
              ],
            ],
          ],
        ),
      ),
    );
  }
}
