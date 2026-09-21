import 'dart:math' as math;
import 'dart:ui';
import 'package:flame/components.dart';
import '../isometric_coordinates.dart';

class Snowflake {
  double x;
  double y;
  double speedY;
  double speedX;
  double radius;
  double opacity;

  Snowflake({
    required this.x,
    required this.y,
    required this.speedY,
    required this.speedX,
    required this.radius,
    required this.opacity,
  });
}

class SleetDrop {
  double x;
  double y;
  double speedY;
  double speedX;
  double length;

  SleetDrop({
    required this.x,
    required this.y,
    required this.speedY,
    required this.speedX,
    required this.length,
  });
}

class FogBand {
  double x;
  double y;
  double width;
  double height;
  double speedX;
  double phase;

  FogBand({
    required this.x,
    required this.y,
    required this.width,
    required this.height,
    required this.speedX,
    required this.phase,
  });
}

/// Atmospheric psychological thriller winter weather: wind-driven snow, freezing sleet, and drifting cold fog.
class WeatherEffectsLayer extends Component with HasGameRef {
  final List<Snowflake> _snowflakes = [];
  final List<SleetDrop> _sleet = [];
  final List<FogBand> _fogBands = [];
  final math.Random _random = math.Random(1989);

  double _globalTime = 0.0;

  WeatherEffectsLayer() {
    priority = IsometricCoordinates.zOrderWeather;
  }

  @override
  Future<void> onLoad() async {
    // 1. Initialize Snowflakes
    for (var i = 0; i < 90; i++) {
      _snowflakes.add(
        Snowflake(
          x: (_random.nextDouble() - 0.5) * 1800,
          y: (_random.nextDouble() - 0.5) * 1400,
          speedY: 28.0 + _random.nextDouble() * 38.0,
          speedX: -18.0 - _random.nextDouble() * 18.0,
          radius: 1.2 + _random.nextDouble() * 2.2,
          opacity: 0.35 + _random.nextDouble() * 0.45,
        ),
      );
    }

    // 2. Initialize Freezing Sleet streaks
    for (var i = 0; i < 25; i++) {
      _sleet.add(
        SleetDrop(
          x: (_random.nextDouble() - 0.5) * 1800,
          y: (_random.nextDouble() - 0.5) * 1400,
          speedY: 140.0 + _random.nextDouble() * 80.0,
          speedX: -60.0 - _random.nextDouble() * 40.0,
          length: 6.0 + _random.nextDouble() * 6.0,
        ),
      );
    }

    // 3. Initialize Drifting Fog Mist bands
    for (var i = 0; i < 5; i++) {
      _fogBands.add(
        FogBand(
          x: (_random.nextDouble() - 0.5) * 1200,
          y: -400.0 + i * 200.0,
          width: 500.0 + _random.nextDouble() * 300.0,
          height: 180.0 + _random.nextDouble() * 100.0,
          speedX: -12.0 - _random.nextDouble() * 14.0,
          phase: _random.nextDouble() * math.pi * 2,
        ),
      );
    }
  }

  @override
  void update(double dt) {
    super.update(dt);
    _globalTime += dt;

    // Update Snow
    for (final flake in _snowflakes) {
      flake.y += flake.speedY * dt;
      flake.x += flake.speedX * dt;

      if (flake.y > 700) {
        flake.y = -700;
        flake.x = (_random.nextDouble() - 0.5) * 1800;
      }
      if (flake.x < -900) {
        flake.x = 900;
      }
    }

    // Update Sleet
    for (final drop in _sleet) {
      drop.y += drop.speedY * dt;
      drop.x += drop.speedX * dt;

      if (drop.y > 700) {
        drop.y = -700;
        drop.x = (_random.nextDouble() - 0.5) * 1800;
      }
      if (drop.x < -900) {
        drop.x = 900;
      }
    }

    // Update Fog Bands
    for (final fog in _fogBands) {
      fog.x += fog.speedX * dt;
      if (fog.x < -1100) {
        fog.x = 1100;
      }
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    // 1. Drifting Cold Fog bands (low alpha, eerie atmosphere)
    for (final fog in _fogBands) {
      final pulse = 0.12 + 0.06 * math.sin(_globalTime * 0.8 + fog.phase);
      final fogPaint = Paint()
        ..color = Color.fromRGBO(203, 213, 225, pulse)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 28.0);

      canvas.drawOval(
        Rect.fromCenter(
          center: Offset(fog.x, fog.y),
          width: fog.width,
          height: fog.height,
        ),
        fogPaint,
      );
    }

    // 2. Freezing Sleet streaks
    final sleetPaint = Paint()
      ..color = const Color(0x55E2E8F0)
      ..strokeWidth = 1.0;

    for (final drop in _sleet) {
      canvas.drawLine(
        Offset(drop.x, drop.y),
        Offset(drop.x + (drop.speedX * 0.03), drop.y + drop.length),
        sleetPaint,
      );
    }

    // 3. Snowflakes
    for (final flake in _snowflakes) {
      final paint = Paint()
        ..color = Color.fromRGBO(241, 245, 249, flake.opacity)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 0.8);

      canvas.drawCircle(Offset(flake.x, flake.y), flake.radius, paint);
    }
  }
}
