import 'package:flame/components.dart';

/// Camera controller providing smooth target following, bounded clamping, and controlled zoom.
class IsometricCameraController {
  final CameraComponent camera;
  final Vector2 minBounds;
  final Vector2 maxBounds;

  double zoomLevel = 1.0;
  static const double minZoom = 0.75;
  static const double maxZoom = 1.6;
  static const double followSpeed = 6.0; // Smooth damping factor

  IsometricCameraController({
    required this.camera,
    required this.minBounds,
    required this.maxBounds,
    this.zoomLevel = 1.0,
  });

  /// Updates camera position to follow target within bounds.
  void update({
    required Vector2 targetPosition,
    required Vector2 viewportSize,
    required double dt,
  }) {
    // Current camera position in world space
    final currentPos = camera.viewfinder.position;

    // Smooth lerp towards target
    final smoothX = currentPos.x + (targetPosition.x - currentPos.x) * (followSpeed * dt).clamp(0.0, 1.0);
    final smoothY = currentPos.y + (targetPosition.y - currentPos.y) * (followSpeed * dt).clamp(0.0, 1.0);

    // Compute visible half-extents at current zoom
    final effectiveHalfWidth = (viewportSize.x / 2.0) / zoomLevel;
    final effectiveHalfHeight = (viewportSize.y / 2.0) / zoomLevel;

    // Clamp camera position so the viewport edges never expose areas outside the bounds
    final clampedX = smoothX.clamp(
      minBounds.x + effectiveHalfWidth,
      maxBounds.x - effectiveHalfWidth,
    );
    final clampedY = smoothY.clamp(
      minBounds.y + effectiveHalfHeight,
      maxBounds.y - effectiveHalfHeight,
    );

    camera.viewfinder.position = Vector2(clampedX, clampedY);
    camera.viewfinder.zoom = zoomLevel;
  }

  void setZoom(double newZoom) {
    zoomLevel = newZoom.clamp(minZoom, maxZoom);
    camera.viewfinder.zoom = zoomLevel;
  }

  void zoomIn([double step = 0.15]) => setZoom(zoomLevel + step);
  void zoomOut([double step = 0.15]) => setZoom(zoomLevel - step);
}
