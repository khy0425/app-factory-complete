import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:runstart/main.dart';

void main() {
  testWidgets('런스타트 app loads', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const RunStartApp());

    // Verify that the app loads without errors
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}
