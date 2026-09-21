import 'dart:math' as math;
import '../world/collision_box.dart';
import '../world/isometric_coordinates.dart';

enum PlayerMovementState {
  idle,
  walk,
  run,
}

/// Logical controller governing Alex's movement, speed, state transitions, and collision checking.
class PlayerController {
  double worldX;
  double worldY;
  String orientation;
  PlayerMovementState state = PlayerMovementState.idle;

  // Speeds in continuous world units per second
  static const double walkSpeed = 2.4;
  static const double runSpeed = 4.8;
  static const double playerCollisionRadius = 0.28; // ~35px in screen space

  final CollisionManager collisionManager;

  PlayerController({
    required this.worldX,
    required this.worldY,
    this.orientation = 'SE',
    required this.collisionManager,
  });

  /// Updates Alex's position and state based on input vector and elapsed delta time.
  void update({
    required double inputX,
    required double inputY,
    required double dt,
  }) {
    final magnitude = math.sqrt(inputX * inputX + inputY * inputY);

    if (magnitude < 0.08) {
      state = PlayerMovementState.idle;
      return;
    }

    // Determine target state based on joystick tilt / pressure
    final isRunning = magnitude > 0.65;
    state = isRunning ? PlayerMovementState.run : PlayerMovementState.walk;
    final currentSpeed = isRunning ? runSpeed : walkSpeed;

    // Normalize input vector
    final normX = inputX / magnitude;
    final normY = inputY / magnitude;

    // Update 4-way orientation
    orientation = IsometricCoordinates.vectorToOrientation(normX, normY);

    // Compute intended displacement in isometric world coordinates
    // When pressing down-right (screen +X, +Y), world increases X
    // When pressing down-left (screen -X, +Y), world increases Y
    final worldDx = (normX + normY) * currentSpeed * dt * 0.707;
    final worldDy = (-normX + normY) * currentSpeed * dt * 0.707;

    final targetX = worldX + worldDx;
    final targetY = worldY + worldDy;

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
}
