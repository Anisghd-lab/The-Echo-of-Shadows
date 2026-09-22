import 'dart:math' as math;
import '../world/collision_box.dart';
import '../world/isometric_coordinates.dart';
import 'player_orientation_controller.dart';

enum PlayerMovementState {
  idle,
  walk,
  run,
  interact,
  talk,
}

/// Logical controller governing Alex's movement, speed, state transitions,
/// in-place 360° rotation, and collision checking.
class PlayerController {
  double worldX;
  double worldY;
  final PlayerOrientationController orientationController;
  PlayerMovementState state = PlayerMovementState.idle;

  // Speeds in continuous world units per second, scaled with IsometricCoordinates.worldScale
  // to ensure constant physical pixel speed across any tile dimension.
  static double get walkSpeed => 2.4 * IsometricCoordinates.worldScale;
  static double get runSpeed => 4.8 * IsometricCoordinates.worldScale;
  static double get playerCollisionRadius => 0.28 * IsometricCoordinates.worldScale; // ~35px in screen space

  // Joystick thresholds:
  // - below 0.10: deadzone (remain completely still)
  // - between 0.10 and 0.30: turn-on-the-spot without displacement
  // - between 0.30 and 0.70: walk
  // - above 0.70: run
  static const double deadzoneThreshold = 0.10;
  static const double walkThreshold = 0.30;
  static const double runThreshold = 0.70;

  final CollisionManager collisionManager;

  PlayerController({
    required this.worldX,
    required this.worldY,
    String orientation = PlayerOrientationController.southEast,
    required this.collisionManager,
  }) : orientationController = PlayerOrientationController(initialOrientation: orientation);

  /// Current 2-letter canonical orientation code ('SE', 'SW', 'NE', 'NW').
  String get orientation => orientationController.orientation;

  set orientation(String newOrient) {
    orientationController.setOrientation(newOrient);
  }

  /// Rotates Alex 90° clockwise without changing world position.
  /// SE -> SW -> NW -> NE -> SE
  String rotateClockwise() {
    state = PlayerMovementState.idle;
    return orientationController.rotateClockwise();
  }

  /// Rotates Alex 90° counter-clockwise without changing world position.
  /// SE -> NE -> NW -> SW -> SE
  String rotateCounterClockwise() {
    state = PlayerMovementState.idle;
    return orientationController.rotateCounterClockwise();
  }

  /// Checks if Alex is facing towards a target world point (targetX, targetY).
  bool isFacingTarget(double targetX, double targetY, {double maxAngleDegrees = 75.0}) {
    return orientationController.isFacingTarget(
      alexX: worldX,
      alexY: worldY,
      targetX: targetX,
      targetY: targetY,
      maxAngleDegrees: maxAngleDegrees,
    );
  }

  /// Updates Alex's position and orientation based on input vector and elapsed delta time.
  /// Supports in-place turning when input magnitude is low or when [turnOnly] is true.
  void update({
    required double inputX,
    required double inputY,
    required double dt,
    bool turnOnly = false,
  }) {
    final magnitude = math.sqrt(inputX * inputX + inputY * inputY);

    // 1. Deadzone or in Talk state: remain still
    if (state == PlayerMovementState.talk) {
      return;
    }

    if (magnitude < deadzoneThreshold) {
      if (state != PlayerMovementState.interact) {
        state = PlayerMovementState.idle;
      }
      return;
    }

    // Normalize input vector
    final normX = inputX / magnitude;
    final normY = inputY / magnitude;

    // 2. In-place rotation zone: rotate orientation without moving
    if (turnOnly || magnitude < walkThreshold) {
      orientationController.updateFromVector(normX, normY);
      if (state != PlayerMovementState.interact) {
        state = PlayerMovementState.idle;
      }
      // Position strictly remains unchanged
      return;
    }

    // 3. Movement zone (walk or run)
    orientationController.updateFromVector(normX, normY);

    final isRunning = magnitude >= runThreshold;
    state = isRunning ? PlayerMovementState.run : PlayerMovementState.walk;
    final currentSpeed = isRunning ? runSpeed : walkSpeed;

    // Compute intended displacement in isometric world coordinates from screen input:
    // Guarantees strictly uniform, isotropic velocity across all 8 cardinal and isometric directions.
    final screenSpeed = currentSpeed * IsometricCoordinates.halfTileWidth;
    final worldDisp = IsometricCoordinates.screenToWorld(
      normX * screenSpeed * dt,
      normY * screenSpeed * dt,
    );

    final targetX = worldX + worldDisp.x;
    final targetY = worldY + worldDisp.y;

    // Resolve collision via sliding
    final resolved = collisionManager.resolveMovement(
      currentX: worldX,
      currentY: worldY,
      targetX: targetX,
      targetY: targetY,
      radius: playerCollisionRadius,
    );

    worldX = resolved.x;
    worldY = resolved.y;
  }

  void teleport(double newX, double newY, {String? newOrientation}) {
    worldX = newX;
    worldY = newY;
    if (newOrientation != null) {
      orientation = newOrientation;
    }
  }

  /// Automatically orients Alex to face towards a world coordinate (e.g. an NPC or POI).
  void faceTarget(double targetX, double targetY) {
    orientation = PlayerOrientationController.calculateFacingOrientation(
      fromX: worldX,
      fromY: worldY,
      toX: targetX,
      toY: targetY,
    );
  }
}
