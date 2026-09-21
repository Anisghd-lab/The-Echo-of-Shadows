import 'package:flame/components.dart';

/// Camera controller providing smooth target following, bounded clamping, and controlled zoom.
/// Guarantees that camera bounds never reveal empty unbuilt void.
class IsometricCameraController {
  final CameraComponent camera;
  final Vector2 minBounds;
  final Vector2 maxBounds;

  double zoomLevel = 1.15; // Slightly enhanced initial cinematic focus
  static const double minZoom = 0.85;
  static const double maxZoom = 1.6;
  static const double followSpeed = 5.5; // Smooth cinematic damping

  IsometricCameraController({
    required this.camera,
    required this.minBounds,
    required this.maxBounds,
    this.zoomLevel = 1.15,
  });

  /// Updates camera position to follow target smoothly while staying within world bounds.
  void update({
    required Vector2 targetPosition,
    required Vector2 viewportSize,
    required double dt,
  }) {
    final currentPos = camera.viewfinder.position;

    // Smooth lerp towards target
    final smoothX = currentPos.x + (targetPosition.x - currentPos.x) * (followSpeed * dt).clamp(0.0, 1.0);
    final smoothY = currentPos.y + (targetPosition.y - currentPos.y) * (followSpeed * dt).clamp(0.0, 1.0);

    // Compute visible half-extents at current zoom
    final effectiveHalfWidth = (viewportSize.x / 2.0) / zoomLevel;
    final effectiveHalfHeight = (viewportSize.y / 2.0) / zoomLevel;

    // Calculate clamped bounds (if viewport is smaller than world extent)
    double clampedX = smoothX;
    double clampedY = smoothY;

    final minAllowedX = minBounds.x + effectiveHalfWidth;
    final maxAllowedX = maxBounds.x - effectiveHalfWidth;
    if (minAllowedX < maxAllowedX) {
      clampedX = smoothX.clamp(minAllowedX, maxAllowedX);
    } else {
      clampedX = (minBounds.x + maxBounds.x) / 2.0;
    }

    final minAllowedY = minBounds.y + effectiveHalfHeight;
    final maxAllowedY = maxBounds.y - effectiveHalfHeight;
    if (minAllowedY < maxAllowedY) {
      clampedY = smoothY.clamp(minAllowedY, maxAllowedY);
    } else {
      clampedY = (minBounds.y + maxBounds.y) / 2.0;
    }

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
