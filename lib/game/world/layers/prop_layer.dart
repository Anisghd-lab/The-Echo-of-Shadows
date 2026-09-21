import 'dart:ui';
import 'package:flame/components.dart';
import '../asset_registry.dart';
import '../collision_box.dart';
import '../isometric_coordinates.dart';

class PropItem {
  final String id;
  final String assetId;
  final double worldX;
  final double worldY;
  final double displayWidth;
  final double displayHeight;
  final double collisionWidth;
  final double collisionHeight;
  final bool hasCollision;

  const PropItem({
    required this.id,
    required this.assetId,
    required this.worldX,
    required this.worldY,
    required this.displayWidth,
    required this.displayHeight,
    this.collisionWidth = 0.6,
    this.collisionHeight = 0.6,
    this.hasCollision = true,
  });
}

class PropSpriteComponent extends PositionComponent with HasGameRef {
  final PropItem prop;
  Sprite? _sprite;

  PropSpriteComponent(this.prop) {
    anchor = Anchor.bottomCenter;
    size = Vector2(prop.displayWidth, prop.displayHeight);

    final screenPos = IsometricCoordinates.worldToScreen(prop.worldX, prop.worldY);
    position = Vector2(screenPos.x, screenPos.y);

    // Z-Order: dynamic priority based on base ground contact point
    priority = IsometricCoordinates.calculateZOrder(
      prop.worldX,
      prop.worldY,
      layerBase: IsometricCoordinates.zOrderProps,
    );
  }

  @override
  Future<void> onLoad() async {
    final registry = GameAssetRegistry();
    final path = registry.getPath(prop.assetId);
    if (path.isNotEmpty) {
      try {
        final image = await gameRef.images.load(path);
        _sprite = Sprite(image);
      } catch (_) {}
    }
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    if (_sprite != null) {
      _sprite!.render(canvas, position: Vector2.zero(), size: size);
    } else {
      final paint = Paint()..color = const Color(0xFFD97706);
      canvas.drawRect(Rect.fromLTWH(0, 0, size.x, size.y), paint);
    }
  }
}

/// Layer 4: Interactive and environmental props (well, gate, lamp posts, fences).
class PropLayer extends Component with HasGameRef {
  final CollisionManager collisionManager;

  // Props positioned to test passing between objects and front/behind depth sorting
  final List<PropItem> props = const [
    // Village Well in the center
    PropItem(
      id: 'village_well',
      assetId: GameAssetRegistry.villageWell,
      worldX: 0.0,
      worldY: 4.0,
      displayWidth: 90,
      displayHeight: 100,
      collisionWidth: 0.8,
      collisionHeight: 0.8,
      hasCollision: true,
    ),

    // Iron Gate flanking the path to the right
    PropItem(
      id: 'iron_gate_right',
      assetId: GameAssetRegistry.villageIronGate,
      worldX: 2.2,
      worldY: 4.0,
      displayWidth: 110,
      displayHeight: 70,
      collisionWidth: 0.9,
      collisionHeight: 0.4,
      hasCollision: true,
    ),

    // Left fence/gate marker
    PropItem(
      id: 'iron_gate_left',
      assetId: GameAssetRegistry.villageIronGate,
      worldX: -2.2,
      worldY: 4.0,
      displayWidth: 110,
      displayHeight: 70,
      collisionWidth: 0.9,
      collisionHeight: 0.4,
      hasCollision: true,
    ),
  ];

  PropLayer({required this.collisionManager});

  @override
  Future<void> onLoad() async {
    for (final p in props) {
      add(PropSpriteComponent(p));

      if (p.hasCollision) {
        collisionManager.addObstacle(
          IsometricCollisionBox(
            id: 'col_${p.id}',
            worldX: p.worldX,
            worldY: p.worldY,
            halfWidth: p.collisionWidth / 2,
            halfHeight: p.collisionHeight / 2,
            label: p.id,
          ),
        );
      }
    }
  }
}
