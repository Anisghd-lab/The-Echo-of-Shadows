import 'dart:ui';
import 'package:flame/components.dart';
import '../world/isometric_coordinates.dart';
import 'player_animation_controller.dart';
import 'player_controller.dart';

/// Flame visual component rendering Alex in the isometric game world.
/// Automatically updates dynamic Z-order and screen position.
class AlexComponent extends PositionComponent with HasGameRef {
  final PlayerController controller;
  final PlayerAnimationController animationController;
  double _runningTime = 0.0;

  // Shadow paint for feet ground contact
  final Paint _shadowPaint = Paint()
    ..color = const Color(0x66000000)
    ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 4.0);

  AlexComponent({
    required this.controller,
    required this.animationController,
  }) {
    // Initial size of Alex on screen (scaled down to fit isometric tile perspective)
    size = Vector2(72, 144);
    anchor = Anchor.bottomCenter;
  }

  @override
  void update(double dt) {
    super.update(dt);
    _runningTime += dt;
    animationController.update(dt);

    // 1. Sync screen position from isometric world coordinates
    final screenPos = IsometricCoordinates.worldToScreen(
      controller.worldX,
      controller.worldY,
    );
    position = Vector2(screenPos.x, screenPos.y);

    // 2. Dynamic Z-Ordering: depth depends on world ground position
    priority = IsometricCoordinates.calculateZOrder(
      controller.worldX,
      controller.worldY,
    );
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    // 1. Render contact ground shadow
    canvas.drawOval(
      Rect.fromCenter(
        center: Offset(size.x / 2, size.y - 4),
        width: size.x * 0.55,
        height: 14.0,
      ),
      _shadowPaint,
    );

    // 2. Render active Alex sprite
    final sprite = animationController.getCurrentSprite(
      state: controller.state,
      orientation: controller.orientation,
      runningTime: _runningTime,
    );

    if (sprite != null) {
      sprite.render(
        canvas,
        position: Vector2.zero(),
        size: size,
      );
    } else {
      // Fallback debug silhouette
      final debugPaint = Paint()..color = const Color(0xFF3B82F6);
      canvas.drawRRect(
        RRect.fromRectAndRadius(
          Rect.fromLTWH(size.x * 0.2, 10, size.x * 0.6, size.y - 14),
          const Radius.circular(8),
        ),
        debugPaint,
      );
    }
  }
}
