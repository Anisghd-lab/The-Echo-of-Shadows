import 'dart:math' as math;

/// Represents an independent ground-level collision obstacle in isometric world coordinates.
/// Decoupled from sprite visuals.
class IsometricCollisionBox {
  final String id;
  final double worldX;
  final double worldY;
  final double halfWidth;  // Extent along isometric X axis
  final double halfHeight; // Extent along isometric Y axis
  final String label;

  const IsometricCollisionBox({
    required this.id,
    required this.worldX,
    required this.worldY,
    required this.halfWidth,
    required this.halfHeight,
    this.label = 'obstacle',
  });

  /// Checks if a circular entity (like Alex with a collision radius) collides with this box.
  bool collidesWithCircle(double x, double y, double radius) {
    // Closest point on the AABB in world space
    final closestX = x.clamp(worldX - halfWidth, worldX + halfWidth);
    final closestY = y.clamp(worldY - halfHeight, worldY + halfHeight);

    final distX = x - closestX;
    final distY = y - closestY;
    final distSquared = distX * distX + distY * distY;

    return distSquared < (radius * radius);
  }

  /// Checks if a point is inside the collision area.
  bool contains(double x, double y) {
    return x >= (worldX - halfWidth) &&
        x <= (worldX + halfWidth) &&
        y >= (worldY - halfHeight) &&
        y <= (worldY + halfHeight);
  }
}

/// Central collision manager registering all static obstacles in the active world.
class CollisionManager {
  final List<IsometricCollisionBox> _obstacles = [];

  List<IsometricCollisionBox> get obstacles => List.unmodifiable(_obstacles);

  void addObstacle(IsometricCollisionBox obstacle) {
    _obstacles.add(obstacle);
  }

  void addAll(Iterable<IsometricCollisionBox> obstacles) {
    _obstacles.addAll(obstacles);
  }

  void clear() {
    _obstacles.clear();
  }

  /// Validates proposed player movement.
  /// If a collision occurs, attempts sliding along X and Y axes independently.
  math.Point<double> resolveMovement({
    required double currentX,
    required double currentY,
    required double targetX,
    required double targetY,
    required double radius,
  }) {
    // 1. Check full target position
    if (!hasCollision(targetX, targetY, radius)) {
      return math.Point(targetX, targetY);
    }

    // 2. Try sliding along X axis only
    if (!hasCollision(targetX, currentY, radius)) {
      return math.Point(targetX, currentY);
    }

    // 3. Try sliding along Y axis only
    if (!hasCollision(currentX, targetY, radius)) {
      return math.Point(currentX, targetY);
    }

    // 4. Blocked in all directions: remain at current position
    return math.Point(currentX, currentY);
  }

  /// Checks whether a circular entity at (x, y) collides with any registered obstacle.
  bool hasCollision(double x, double y, double radius) {
    for (final obstacle in _obstacles) {
      if (obstacle.collidesWithCircle(x, y, radius)) {
        return true;
      }
    }
    return false;
  }
}
