import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gigachad_runner/main.dart';

void main() {
  testWidgets('GigaChad Runner app loads', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const GigaChadRunnerApp());

    // Verify that the app loads without errors
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}
