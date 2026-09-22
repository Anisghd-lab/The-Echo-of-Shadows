import 'dart:ui';
import 'package:flame/components.dart';
import '../world/isometric_coordinates.dart';
import 'player_animation_controller.dart';
import 'player_controller.dart';

/// Specialized vector tracking and reactively binding to the active AlexComponent.
class _AlexPositionVector extends Vector2 {
  AlexComponent? activeComponent;

  _AlexPositionVector(super.x, super.y);

  @override
  set x(double value) {
    super.x = value;
    if (activeComponent != null && activeComponent!.controller.worldX != value) {
      activeComponent!.worldX = value;
    }
  }

  @override
  set y(double value) {
    super.y = value;
    if (activeComponent != null && activeComponent!.controller.worldY != value) {
      activeComponent!.worldY = value;
    }
  }
}

/// Static global configuration and coordinates for Alex character.
/// Allows direct coordinate assignment:
/// `Alex.position.x = 7.0;`
/// `Alex.position.y = 8.0;`
class Alex {
  static final _AlexPositionVector position = _AlexPositionVector(7.0, 8.0);

  static double get x => position.x;
  static set x(double val) => position.x = val;

  static double get y => position.y;
  static set y(double val) => position.y = val;
}

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
    // Calibrated human scale: 28px width, 56px height
    // Matches door heights (~50px), well rim (~30px), and church scale
    size = Vector2(28, 56);
    anchor = Anchor.bottomCenter;

    // Immediately sync screen position and priority from initial world coordinates
    final screenPos = IsometricCoordinates.worldToScreen(controller.worldX, controller.worldY);
    position.setValues(screenPos.x, screenPos.y);
    priority = IsometricCoordinates.calculateZOrder(controller.worldX, controller.worldY);
    Alex.position.activeComponent = this;
    Alex.position.x = controller.worldX;
    Alex.position.y = controller.worldY;
  }

  /// Direct world coordinate accessors
  double get worldX => controller.worldX;
  set worldX(double wx) {
    controller.worldX = wx;
    Alex.position.x = wx;
    final screenPos = IsometricCoordinates.worldToScreen(controller.worldX, controller.worldY);
    position.setValues(screenPos.x, screenPos.y);
    priority = IsometricCoordinates.calculateZOrder(controller.worldX, controller.worldY);
  }

  double get worldY => controller.worldY;
  set worldY(double wy) {
    controller.worldY = wy;
    Alex.position.y = wy;
    final screenPos = IsometricCoordinates.worldToScreen(controller.worldX, controller.worldY);
    position.setValues(screenPos.x, screenPos.y);
    priority = IsometricCoordinates.calculateZOrder(controller.worldX, controller.worldY);
  }

  /// Sets world position directly
  void setWorldPosition(double wx, double wy) {
    controller.worldX = wx;
    controller.worldY = wy;
    Alex.position.setValues(wx, wy);
    final screenPos = IsometricCoordinates.worldToScreen(wx, wy);
    position.setValues(screenPos.x, screenPos.y);
    priority = IsometricCoordinates.calculateZOrder(wx, wy);
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
    position.setValues(screenPos.x, screenPos.y);
    Alex.position.setValues(controller.worldX, controller.worldY);

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
        center: Offset(size.x / 2, size.y - 2),
        width: size.x * 0.75,
        height: 6.0,
      ),
      _shadowPaint,
    );

    // 2. Render active Alex sprite
    final renderInfo = animationController.getCurrentRenderInfo(
      state: controller.state,
      orientation: controller.orientation,
      runningTime: _runningTime,
    );

    if (renderInfo.sprite != null) {
      if (renderInfo.isFlipped) {
        canvas.save();
        canvas.translate(size.x, 0);
        canvas.scale(-1.0, 1.0);
        renderInfo.sprite!.render(
          canvas,
          position: Vector2.zero(),
          size: size,
        );
        canvas.restore();
      } else {
        renderInfo.sprite!.render(
          canvas,
          position: Vector2.zero(),
          size: size,
        );
      }
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
