import 'dart:math' as math;
import 'package:flame/components.dart';

/// Camera Contexts defined in Phase 11.
enum CameraContext {
  world,      // Wide village overview (Master Blueprint Map / Global view)
  cinematic,  // Dynamic cinematic camera pan/zoom towards target
  player,     // Standard gameplay camera following Alex
  interior,   // Focused camera on building interiors (Family House / Bunker)
}

/// Advanced multi-context Isometric Camera Controller.
/// Governs the intro sequence (World Overview -> Cinematic Zoom -> Alex -> Gameplay Camera),
/// smooth player tracking, bounded clamping, interior cutaway transitions, and zero-void protection.
class IsometricCameraController {
  final CameraComponent camera;
  final Vector2 minBounds;
  final Vector2 maxBounds;

  CameraContext _currentContext = CameraContext.world;
  CameraContext get currentContext => _currentContext;

  double zoomLevel = 1.15;
  static const double minZoom = 0.55;
  static const double maxZoom = 1.8;
  static const double followSpeed = 5.5;

  // Intro sequence state
  double _introTimer = 0.0;
  static const double worldOverviewDuration = 2.0;
  static const double cinematicZoomDuration = 2.5;
  bool _introComplete = false;
  bool get isIntroComplete => _introComplete;

  // Target coordinates for custom framing
  Vector2? customFocusTarget;
  double? targetZoom;

  IsometricCameraController({
    required this.camera,
    required this.minBounds,
    required this.maxBounds,
    this.zoomLevel = 1.15,
  }) {
    // Start with wide world view
    zoomLevel = 0.65;
    camera.viewfinder.zoom = zoomLevel;
  }

  /// Sets camera context with smooth transition.
  void setContext(CameraContext context, {Vector2? focusPoint, double? customZoom}) {
    _currentContext = context;
    customFocusTarget = focusPoint;
    if (customZoom != null) {
      targetZoom = customZoom;
    } else {
      switch (context) {
        case CameraContext.world:
          targetZoom = 0.65;
          break;
        case CameraContext.cinematic:
          targetZoom = 1.25;
          break;
        case CameraContext.player:
          targetZoom = 1.15;
          break;
        case CameraContext.interior:
          targetZoom = 1.45;
          break;
      }
    }
  }

  /// Updates camera position and zoom according to active CameraContext.
  void update({
    required Vector2 targetPosition,
    required Vector2 viewportSize,
    required double dt,
  }) {
    // Handle opening cinematic intro sequence
    if (!_introComplete) {
      _introTimer += dt;
      if (_introTimer < worldOverviewDuration) {
        // Phase 1: WORLD MAP overview
        _currentContext = CameraContext.world;
        targetZoom = 0.65;
        customFocusTarget = (minBounds + maxBounds) / 2.0;
      } else if (_introTimer < worldOverviewDuration + cinematicZoomDuration) {
        // Phase 2: CINEMATIC ZOOM towards Alex
        _currentContext = CameraContext.cinematic;
        final progress = (_introTimer - worldOverviewDuration) / cinematicZoomDuration;
        targetZoom = 0.65 + (1.15 - 0.65) * _easeInOutCubic(progress);
        final worldCenter = (minBounds + maxBounds) / 2.0;
        customFocusTarget = worldCenter + (targetPosition - worldCenter) * _easeInOutCubic(progress);
      } else {
        // Phase 3: Transition to normal PLAYER CAMERA
        _introComplete = true;
        _currentContext = CameraContext.player;
        targetZoom = 1.15;
        customFocusTarget = null;
      }
    }

    // Smoothly interpolate zoom towards targetZoom
    if (targetZoom != null) {
      final zoomLerp = (4.0 * dt).clamp(0.0, 1.0);
      zoomLevel = zoomLevel + (targetZoom! - zoomLevel) * zoomLerp;
    }

    // Determine target position depending on context
    Vector2 desiredTarget;
    if (_currentContext == CameraContext.player) {
      desiredTarget = targetPosition;
    } else if (customFocusTarget != null) {
      desiredTarget = customFocusTarget!;
    } else {
      desiredTarget = targetPosition;
    }

    final currentPos = camera.viewfinder.position;

    // Smooth lerp towards desired target
    final smoothX = currentPos.x + (desiredTarget.x - currentPos.x) * (followSpeed * dt).clamp(0.0, 1.0);
    final smoothY = currentPos.y + (desiredTarget.y - currentPos.y) * (followSpeed * dt).clamp(0.0, 1.0);

    // Compute visible half-extents at current zoom
    final effectiveHalfWidth = (viewportSize.x / 2.0) / zoomLevel;
    final effectiveHalfHeight = (viewportSize.y / 2.0) / zoomLevel;

    // Calculate clamped bounds to prevent void reveal
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

  double _easeInOutCubic(double t) {
    return t < 0.5 ? 4 * t * t * t : 1 - math.pow(-2 * t + 2, 3) / 2;
  }

  void setZoom(double newZoom) {
    zoomLevel = newZoom.clamp(minZoom, maxZoom);
    targetZoom = zoomLevel;
    camera.viewfinder.zoom = zoomLevel;
  }

  void zoomIn([double step = 0.15]) => setZoom(zoomLevel + step);
  void zoomOut([double step = 0.15]) => setZoom(zoomLevel - step);
}
