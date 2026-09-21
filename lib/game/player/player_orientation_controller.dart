import 'dart:math' as math;
import '../world/isometric_coordinates.dart';

/// The 4 canonical isometric orientations representing 360° rotation.
enum CanonicalOrientation {
  southEast, // SE (+X, +Y in screen space, ~45°)
  southWest, // SW (-X, +Y in screen space, ~135°)
  northWest, // NW (-X, -Y in screen space, ~225°)
  northEast, // NE (+X, -Y in screen space, ~315°)
}

/// Controller governing Alex's 360° orientation, in-place rotation transitions,
/// and directional interaction targeting.
class PlayerOrientationController {
  static const String southEast = 'SE';
  static const String southWest = 'SW';
  static const String northWest = 'NW';
  static const String northEast = 'NE';

  // Clockwise order: SE (0) -> SW (1) -> NW (2) -> NE (3) -> SE (0)
  static const List<String> canonicalCycle = [
    southEast,
    southWest,
    northWest,
    northEast,
  ];

  String _currentOrientation;

  PlayerOrientationController({String initialOrientation = southEast})
      : _currentOrientation = _sanitize(initialOrientation);

  /// Current 2-letter orientation code ('SE', 'SW', 'NE', 'NW').
  String get orientation => _currentOrientation;

  /// Current canonical orientation enum.
  CanonicalOrientation get canonicalOrientation {
    switch (_currentOrientation) {
      case southEast:
        return CanonicalOrientation.southEast;
      case southWest:
        return CanonicalOrientation.southWest;
      case northWest:
        return CanonicalOrientation.northWest;
      case northEast:
        return CanonicalOrientation.northEast;
      default:
        return CanonicalOrientation.southEast;
    }
  }

  /// Angle in radians corresponding to orientation in screen coordinates.
  double get screenAngleRadians {
    switch (_currentOrientation) {
      case southEast:
        return math.pi / 4;       // 45°
      case southWest:
        return 3 * math.pi / 4;   // 135°
      case northWest:
        return -3 * math.pi / 4;  // 225° / -135°
      case northEast:
        return -math.pi / 4;      // 315° / -45°
      default:
        return math.pi / 4;
    }
  }

  /// Sets orientation directly.
  void setOrientation(String newOrientation) {
    _currentOrientation = _sanitize(newOrientation);
  }

  /// Performs a 90° clockwise rotation on the spot:
  /// SE -> SW -> NW -> NE -> SE
  String rotateClockwise() {
    final idx = canonicalCycle.indexOf(_currentOrientation);
    final nextIdx = (idx + 1) % canonicalCycle.length;
    _currentOrientation = canonicalCycle[nextIdx];
    return _currentOrientation;
  }

  /// Performs a 90° counter-clockwise rotation on the spot:
  /// SE -> NE -> NW -> SW -> SE
  String rotateCounterClockwise() {
    final idx = canonicalCycle.indexOf(_currentOrientation);
    final prevIdx = (idx - 1 + canonicalCycle.length) % canonicalCycle.length;
    _currentOrientation = canonicalCycle[prevIdx];
    return _currentOrientation;
  }

  /// Updates orientation based on a 2D screen direction vector (e.g. from joystick).
  /// Divides the 360° circle into 4 distinct 90° quadrants:
  /// - [0°, 90°):   SE
  /// - [90°, 180°]: SW
  /// - [-180°, -90°): NW
  /// - [-90°, 0°):  NE
  void updateFromVector(double dx, double dy) {
    if (dx == 0 && dy == 0) return;
    _currentOrientation = IsometricCoordinates.vectorToOrientation(dx, dy);
  }

  /// Calculates whether Alex is facing towards a target world coordinate (targetX, targetY)
  /// given Alex's current world position (alexX, alexY).
  ///
  /// Uses the angular difference between Alex's facing direction and the vector to the target.
  /// Returns true if within the specified angular cone (default 75°).
  bool isFacingTarget({
    required double alexX,
    required double alexY,
    required double targetX,
    required double targetY,
    double maxAngleDegrees = 75.0,
  }) {
    // Convert world displacement to screen displacement
    final dx = (targetX - targetY) - (alexX - alexY);
    final dy = ((targetX + targetY) - (alexX + alexY)) * 0.5;

    final targetAngle = math.atan2(dy, dx);
    final facingAngle = screenAngleRadians;

    // Smallest angular difference between [-PI, PI]
    var diff = (targetAngle - facingAngle).abs();
    while (diff > math.pi) {
      diff = (2 * math.pi - diff).abs();
    }

    final maxAngleRad = maxAngleDegrees * (math.pi / 180.0);
    return diff <= maxAngleRad;
  }

  static String _sanitize(String orient) {
    final up = orient.toUpperCase();
    if (canonicalCycle.contains(up)) return up;
    return southEast;
  }
}
