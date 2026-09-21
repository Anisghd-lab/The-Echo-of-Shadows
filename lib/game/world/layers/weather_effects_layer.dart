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

/// Layer 6: Atmospheric weather effects (gentle drifting snow, cold misty tint).
class WeatherEffectsLayer extends Component with HasGameRef {
  final List<Snowflake> _snowflakes = [];
  final math.Random _random = math.Random(42);
  static const int snowflakeCount = 65;

  WeatherEffectsLayer() {
    priority = IsometricCoordinates.zOrderWeather;
  }

  @override
  Future<void> onLoad() async {
    for (var i = 0; i < snowflakeCount; i++) {
      _snowflakes.add(
        Snowflake(
          x: (_random.nextDouble() - 0.5) * 1600,
          y: (_random.nextDouble() - 0.5) * 1200,
          speedY: 25.0 + _random.nextDouble() * 35.0,
          speedX: -15.0 - _random.nextDouble() * 20.0,
          radius: 1.2 + _random.nextDouble() * 2.2,
          opacity: 0.35 + _random.nextDouble() * 0.45,
        ),
      );
    }
  }

  @override
  void update(double dt) {
    super.update(dt);
    for (final flake in _snowflakes) {
      flake.y += flake.speedY * dt;
      flake.x += flake.speedX * dt;

      // Wrap around screen boundaries
      if (flake.y > 600) {
        flake.y = -600;
        flake.x = (_random.nextDouble() - 0.5) * 1600;
      }
      if (flake.x < -800) {
        flake.x = 800;
      }
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    for (final flake in _snowflakes) {
      final paint = Paint()
        ..color = Color.fromRGBO(240, 248, 255, flake.opacity)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 1.0);

      canvas.drawCircle(Offset(flake.x, flake.y), flake.radius, paint);
    }
  }
}
