import 'dart:math' as math;
import '../world/isometric_coordinates.dart';

/// The 8 canonical character directions (Cardinal + Isometric).
enum CharacterDirection {
  north,
  northEast,
  east,
  southEast,
  south,
  southWest,
  west,
  northWest,
}

/// Character movement / state machine states.
enum CharacterAnimation {
  idle,
  walk,
  run,
  talk,
}

/// The canonical orientations representing cardinal and isometric angles.
enum CanonicalOrientation {
  north,     // N (-Y in screen space, 0° / back)
  south,     // S (+Y in screen space, 180° / front)
  east,      // E (+X in screen space, 90° / right)
  west,      // W (-X in screen space, 270° / left)
  southEast, // SE (+X, +Y in screen space, ~45°)
  southWest, // SW (-X, +Y in screen space, ~135°)
  northWest, // NW (-X, -Y in screen space, ~225°)
  northEast, // NE (+X, -Y in screen space, ~315°)
}

/// Controller governing Alex's 360° orientation, in-place rotation transitions,
/// and directional interaction targeting across 8 real directions.
class PlayerOrientationController {
  // Strict Cardinal Directions
  static const String north = 'N';
  static const String south = 'S';
  static const String east = 'E';
  static const String west = 'W';

  // Isometric Quadrants
  static const String southEast = 'SE';
  static const String southWest = 'SW';
  static const String northWest = 'NW';
  static const String northEast = 'NE';

  // Clockwise 8-way cycle: N (0) -> NE (1) -> E (2) -> SE (3) -> S (4) -> SW (5) -> W (6) -> NW (7)
  static const List<String> eightWayCycle = [
    north,
    northEast,
    east,
    southEast,
    south,
    southWest,
    west,
    northWest,
  ];

  // Clockwise cardinal cycle: N (0) -> E (1) -> S (2) -> W (3)
  static const List<String> cardinalCycle = [
    north,
    east,
    south,
    west,
  ];

  // Clockwise isometric cycle: SE (0) -> SW (1) -> NW (2) -> NE (3)
  static const List<String> canonicalCycle = [
    southEast,
    southWest,
    northWest,
    northEast,
  ];

  String _currentOrientation;

  PlayerOrientationController({String initialOrientation = southEast})
      : _currentOrientation = _sanitize(initialOrientation);

  /// Current 1 or 2-letter orientation code ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW').
  String get orientation => _currentOrientation;

  /// Current canonical orientation enum.
  CanonicalOrientation get canonicalOrientation {
    switch (_currentOrientation) {
      case north:
        return CanonicalOrientation.north;
      case northEast:
        return CanonicalOrientation.northEast;
      case east:
        return CanonicalOrientation.east;
      case southEast:
        return CanonicalOrientation.southEast;
      case south:
        return CanonicalOrientation.south;
      case southWest:
        return CanonicalOrientation.southWest;
      case west:
        return CanonicalOrientation.west;
      case northWest:
        return CanonicalOrientation.northWest;
      default:
        return CanonicalOrientation.southEast;
    }
  }

  /// Current CharacterDirection enum.
  CharacterDirection get characterDirection {
    switch (_currentOrientation) {
      case north:
        return CharacterDirection.north;
      case northEast:
        return CharacterDirection.northEast;
      case east:
        return CharacterDirection.east;
      case southEast:
        return CharacterDirection.southEast;
      case south:
        return CharacterDirection.south;
      case southWest:
        return CharacterDirection.southWest;
      case west:
        return CharacterDirection.west;
      case northWest:
        return CharacterDirection.northWest;
      default:
        return CharacterDirection.southEast;
    }
  }

  /// Angle in radians corresponding to orientation in screen coordinates.
  double get screenAngleRadians {
    switch (_currentOrientation) {
      case east:
        return 0.0;
      case southEast:
        return math.pi / 4;       // 45°
      case south:
        return math.pi / 2;       // 90°
      case southWest:
        return 3 * math.pi / 4;   // 135°
      case west:
        return math.pi;           // 180°
      case northWest:
        return -3 * math.pi / 4;  // 225° / -135°
      case north:
        return -math.pi / 2;      // -90°
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
  /// SE -> SW -> NW -> NE -> SE (if isometric) or N -> E -> S -> W -> N (if cardinal).
  String rotateClockwise() {
    if (canonicalCycle.contains(_currentOrientation)) {
      final idx = canonicalCycle.indexOf(_currentOrientation);
      final nextIdx = (idx + 1) % canonicalCycle.length;
      _currentOrientation = canonicalCycle[nextIdx];
      return _currentOrientation;
    } else if (cardinalCycle.contains(_currentOrientation)) {
      final idx = cardinalCycle.indexOf(_currentOrientation);
      final nextIdx = (idx + 1) % cardinalCycle.length;
      _currentOrientation = cardinalCycle[nextIdx];
      return _currentOrientation;
    } else {
      final idx = eightWayCycle.indexOf(_currentOrientation);
      final nextIdx = (idx + 1) % eightWayCycle.length;
      _currentOrientation = eightWayCycle[nextIdx];
      return _currentOrientation;
    }
  }

  /// Performs a 90° counter-clockwise rotation on the spot:
  /// SE -> NE -> NW -> SW -> SE (if isometric) or N -> W -> S -> E -> N (if cardinal).
  String rotateCounterClockwise() {
    if (canonicalCycle.contains(_currentOrientation)) {
      final idx = canonicalCycle.indexOf(_currentOrientation);
      final prevIdx = (idx - 1 + canonicalCycle.length) % canonicalCycle.length;
      _currentOrientation = canonicalCycle[prevIdx];
      return _currentOrientation;
    } else if (cardinalCycle.contains(_currentOrientation)) {
      final idx = cardinalCycle.indexOf(_currentOrientation);
      final prevIdx = (idx - 1 + cardinalCycle.length) % cardinalCycle.length;
      _currentOrientation = cardinalCycle[prevIdx];
      return _currentOrientation;
    } else {
      final idx = eightWayCycle.indexOf(_currentOrientation);
      final prevIdx = (idx - 1 + eightWayCycle.length) % eightWayCycle.length;
      _currentOrientation = eightWayCycle[prevIdx];
      return _currentOrientation;
    }
  }

  /// Performs a 45° step clockwise rotation through all 8 directions.
  String rotateClockwise8Way() {
    final idx = eightWayCycle.indexOf(_currentOrientation);
    final nextIdx = (idx + 1) % eightWayCycle.length;
    _currentOrientation = eightWayCycle[nextIdx];
    return _currentOrientation;
  }

  /// Performs a 45° step counter-clockwise rotation through all 8 directions.
  String rotateCounterClockwise8Way() {
    final idx = eightWayCycle.indexOf(_currentOrientation);
    final prevIdx = (idx - 1 + eightWayCycle.length) % eightWayCycle.length;
    _currentOrientation = eightWayCycle[prevIdx];
    return _currentOrientation;
  }

  /// Updates orientation based on a 2D screen direction vector (e.g. from joystick/keys).
  /// Divides the 360° circle into 8 distinct 45° octants (±22.5°):
  /// - E, SE, S, SW, W, NW, N, NE
  void updateFromVector(double dx, double dy) {
    if (dx == 0 && dy == 0) return;
    _currentOrientation = IsometricCoordinates.vectorToOrientation8Way(dx, dy);
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

  /// Helper to calculate the 8-way orientation facing from one world point to another.
  static String calculateFacingOrientation({
    required double fromX,
    required double fromY,
    required double toX,
    required double toY,
  }) {
    final dx = (toX - toY) - (fromX - fromY);
    final dy = ((toX + toY) - (fromX + fromY)) * 0.5;
    return IsometricCoordinates.vectorToOrientation8Way(dx, dy);
  }

  static String _sanitize(String orient) {
    final up = orient.toUpperCase();
    if (eightWayCycle.contains(up)) return up;
    if (up == 'NORTH') return north;
    if (up == 'NORTHEAST') return northEast;
    if (up == 'EAST') return east;
    if (up == 'SOUTHEAST') return southEast;
    if (up == 'SOUTH') return south;
    if (up == 'SOUTHWEST') return southWest;
    if (up == 'WEST') return west;
    if (up == 'NORTHWEST') return northWest;
    return southEast;
  }
}
