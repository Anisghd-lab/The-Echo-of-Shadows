import 'dart:math' as math;
import 'package:flutter/material.dart';

/// Touch input controller for Android mobile gameplay.
class TouchInputController extends ChangeNotifier {
  double _inputX = 0.0;
  double _inputY = 0.0;

  double get inputX => _inputX;
  double get inputY => _inputY;

  void setInput(double x, double y) {
    _inputX = x.clamp(-1.0, 1.0);
    _inputY = y.clamp(-1.0, 1.0);
    notifyListeners();
  }

  void reset() {
    _inputX = 0.0;
    _inputY = 0.0;
    notifyListeners();
  }
}

/// Floating or fixed Virtual Joystick Widget for Android mobile devices.
class VirtualJoystickWidget extends StatefulWidget {
  final TouchInputController controller;
  final double radius;

  const VirtualJoystickWidget({
    Key? key,
    required this.controller,
    this.radius = 65.0,
  }) : super(key: key);

  @override
  State<VirtualJoystickWidget> createState() => _VirtualJoystickWidgetState();
}

class _VirtualJoystickWidgetState extends State<VirtualJoystickWidget> {
  Offset _knobOffset = Offset.zero;

  void _updateKnob(Offset localPosition) {
    final center = Offset(widget.radius, widget.radius);
    final delta = localPosition - center;
    final distance = delta.distance;

    Offset clamped;
    if (distance > widget.radius) {
      clamped = Offset(
        (delta.dx / distance) * widget.radius,
        (delta.dy / distance) * widget.radius,
      );
    } else {
      clamped = delta;
    }

    setState(() {
      _knobOffset = clamped;
    });

    final normX = clamped.dx / widget.radius;
    final normY = clamped.dy / widget.radius;
    widget.controller.setInput(normX, normY);
  }

  void _resetKnob() {
    setState(() {
      _knobOffset = Offset.zero;
    });
    widget.controller.reset();
  }

  @override
  Widget build(BuildContext context) {
    final diameter = widget.radius * 2;

    return GestureDetector(
      onPanStart: (details) => _updateKnob(details.localPosition),
      onPanUpdate: (details) => _updateKnob(details.localPosition),
      onPanEnd: (_) => _resetKnob(),
      onPanCancel: () => _resetKnob(),
      child: Container(
        width: diameter,
        height: diameter,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: const Color(0x33000000),
          border: Border.all(color: const Color(0x6694A3B8), width: 2),
        ),
        child: Center(
          child: Transform.translate(
            offset: _knobOffset,
            child: Container(
              width: 50,
              height: 50,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: const RadialGradient(
                  colors: [Color(0xFF64748B), Color(0xFF334155)],
                ),
                boxShadow: const [
                  BoxShadow(
                    color: Color(0x66000000),
                    blurRadius: 8,
                    offset: Offset(0, 3),
                  ),
                ],
                border: Border.all(color: const Color(0xFFE2E8F0), width: 1.5),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
