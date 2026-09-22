import 'dart:ui';
import 'package:flame/components.dart';
import '../player/alex_component.dart';
import '../player/player_orientation_controller.dart';
import '../world/isometric_coordinates.dart';

/// Generic Flame visual component representing an NPC in the isometric game world.
/// Features:
/// - Full 360° directional spritesheet rendering from authentic assets.
/// - Dynamic Z-order sorting by ground contact point.
/// - Invariant foot anchor and contact shadow.
/// - Proximity detection with Alex.
/// - Dynamic orientation targeting (faces Alex during interaction).
/// - Floating interaction indicator when in range and facing.
class NpcComponent extends PositionComponent with HasGameRef {
  final String id;
  final String name;
  final String role;
  double worldX;
  double worldY;
  String orientation;
  final double interactionRadius;
  final String assetFolder;
  final String assetPrefix;
  final int frameCount;

  final Map<String, Sprite> _directionalSprites = {};
  bool _loaded = false;

  // Shadow paint for feet ground contact
  final Paint _shadowPaint = Paint()
    ..color = const Color(0x66000000)
    ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 4.0);

  // Interaction prompt paint
  final Paint _promptBgPaint = Paint()
    ..color = const Color(0xCC1E293B)
    ..style = PaintingStyle.fill;
  final Paint _promptBorderPaint = Paint()
    ..color = const Color(0xFF60A5FA)
    ..style = PaintingStyle.stroke
    ..strokeWidth = 1.5;

  NpcComponent({
    required this.id,
    required this.name,
    required this.role,
    required this.worldX,
    required this.worldY,
    this.orientation = PlayerOrientationController.southEast,
    this.interactionRadius = 1.8,
    required this.assetFolder,
    required this.assetPrefix,
    this.frameCount = 18,
  }) {
    // Proportional character size matching Alex scale (28x56)
    size = Vector2(28, 56);
    anchor = Anchor.bottomCenter;

    final screenPos = IsometricCoordinates.worldToScreen(worldX, worldY);
    position.setValues(screenPos.x, screenPos.y);
    priority = IsometricCoordinates.calculateZOrder(worldX, worldY);
  }

  @override
  Future<void> onLoad() async {
    await super.onLoad();

    // Map 8-way directions to corresponding asset frames:
    // Frame 01: North (Back)
    // Frame 03: North-East
    // Frame 05: East (Profile Right)
    // Frame 07: South-East
    // Frame 09: South (Front)
    // Frame 11: South-West
    // Frame 13: West (Profile Left)
    // Frame 15: North-West
    final Map<String, int> dirFrameMap;
    if (frameCount == 12) {
      dirFrameMap = {
        PlayerOrientationController.north: 1,
        PlayerOrientationController.northEast: 2,
        PlayerOrientationController.east: 4,
        PlayerOrientationController.southEast: 5,
        PlayerOrientationController.south: 7,
        PlayerOrientationController.southWest: 8,
        PlayerOrientationController.west: 10,
        PlayerOrientationController.northWest: 11,
      };
    } else {
      dirFrameMap = {
        PlayerOrientationController.north: 1,
        PlayerOrientationController.northEast: 3,
        PlayerOrientationController.east: 5,
        PlayerOrientationController.southEast: 7,
        PlayerOrientationController.south: 9,
        PlayerOrientationController.southWest: 11,
        PlayerOrientationController.west: 13,
        PlayerOrientationController.northWest: 15,
      };
    }

    for (final entry in dirFrameMap.entries) {
      final frameNum = entry.value.toString().padLeft(2, '0');
      final path = '$assetFolder/$assetPrefix$frameNum.png';
      try {
        final img = await gameRef.images.load(path);
        _directionalSprites[entry.key] = Sprite(img);
      } catch (_) {}
    }

    _loaded = true;
  }

  /// Automatically orients the NPC to face towards a world coordinate (e.g. Alex).
  void faceTarget(double targetX, double targetY) {
    orientation = PlayerOrientationController.calculateFacingOrientation(
      fromX: worldX,
      fromY: worldY,
      toX: targetX,
      toY: targetY,
    );
  }

  /// Sets world position and updates screen coordinates + Z-order.
  void setWorldPosition(double wx, double wy) {
    worldX = wx;
    worldY = wy;
    final screenPos = IsometricCoordinates.worldToScreen(wx, wy);
    position.setValues(screenPos.x, screenPos.y);
    priority = IsometricCoordinates.calculateZOrder(wx, wy);
  }

  /// Checks Euclidean distance to Alex in world units.
  double distanceToAlex(AlexComponent alex) {
    final dx = alex.worldX - worldX;
    final dy = alex.worldY - worldY;
    return (dx * dx + dy * dy);
  }

  /// Returns true if Alex is within interaction radius.
  bool isPlayerInRange(AlexComponent alex) {
    final r2 = interactionRadius * interactionRadius;
    return distanceToAlex(alex) <= r2;
  }

  @override
  void update(double dt) {
    super.update(dt);
    // Dynamic Z-Order based on world position
    priority = IsometricCoordinates.calculateZOrder(worldX, worldY);
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);

    // 1. Invariant ground shadow
    canvas.drawOval(
      Rect.fromCenter(
        center: Offset(size.x / 2, size.y - 2),
        width: size.x * 0.75,
        height: 6.0,
      ),
      _shadowPaint,
    );

    // 2. Active directional sprite
    final sprite = _directionalSprites[orientation] ??
        _directionalSprites[PlayerOrientationController.southEast] ??
        _directionalSprites.values.firstOrNull;

    if (sprite != null) {
      sprite.render(
        canvas,
        position: Vector2.zero(),
        size: size,
      );
    } else {
      // Fallback silhouette
      final debugPaint = Paint()..color = const Color(0xFF10B981);
      canvas.drawRRect(
        RRect.fromRectAndRadius(
          Rect.fromLTWH(size.x * 0.2, 10, size.x * 0.6, size.y - 14),
          const Radius.circular(8),
        ),
        debugPaint,
      );
    }
  }

  /// Renders interaction prompt bubble when close and facing.
  void renderInteractionPrompt(Canvas canvas) {
    final rect = Rect.fromCenter(
      center: Offset(size.x / 2, -14),
      width: 44,
      height: 18,
    );
    final rrect = RRect.fromRectAndRadius(rect, const Radius.circular(6));
    canvas.drawRRect(rrect, _promptBgPaint);
    canvas.drawRRect(rrect, _promptBorderPaint);
  }
}
