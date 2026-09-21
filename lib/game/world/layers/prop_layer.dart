import 'dart:ui';
import 'package:flame/components.dart';
import '../asset_registry.dart';
import '../collision_box.dart';
import '../isometric_coordinates.dart';
import '../village_map.dart';

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
    this.collisionWidth = 0.5,
    this.collisionHeight = 0.5,
    this.hasCollision = true,
  });

  factory PropItem.fromMapProp(MapProp p) {
    return PropItem(
      id: p.id,
      assetId: p.assetId,
      worldX: p.worldX,
      worldY: p.worldY,
      displayWidth: p.displayWidth,
      displayHeight: p.displayHeight,
      collisionWidth: p.collisionHalfWidth * 2.0,
      collisionHeight: p.collisionHalfHeight * 2.0,
      hasCollision: p.hasCollision,
    );
  }
}

class PropSpriteComponent extends PositionComponent with HasGameRef {
  final PropItem prop;
  Sprite? _sprite;

  PropSpriteComponent(this.prop) {
    anchor = Anchor.bottomCenter;
    size = Vector2(prop.displayWidth, prop.displayHeight);

    final scale = IsometricCoordinates.worldScale;
    final wx = prop.worldX * scale;
    final wy = prop.worldY * scale;

    final screenPos = IsometricCoordinates.worldToScreen(wx, wy);
    position = Vector2(screenPos.x, screenPos.y);

    // Dynamic Z-Order based on base ground contact point
    priority = IsometricCoordinates.calculateZOrder(
      wx,
      wy,
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
    }
  }
}

/// Layer 4: Environmental props composed for realistic spatial storytelling.
class PropLayer extends Component with HasGameRef {
  final CollisionManager collisionManager;
  final VillageMap? villageMap;

  PropLayer({
    required this.collisionManager,
    this.villageMap,
  });

  List<PropItem> get props {
    final vMap = villageMap ?? VillageMap.canonical();
    final list = <PropItem>[];

    // 1. Props from VillageMap
    for (final p in vMap.props) {
      list.add(PropItem.fromMapProp(p));
    }

    // 2. Street Lamps from VillageMap
    for (final l in vMap.streetLamps) {
      list.add(
        PropItem(
          id: l.id,
          assetId: GameAssetRegistry.villageStreetLamp,
          worldX: l.worldX,
          worldY: l.worldY,
          displayWidth: 38,
          displayHeight: 96,
          collisionWidth: 0.3,
          collisionHeight: 0.3,
          hasCollision: true,
        ),
      );
    }

    // 3. Environmental Pine & Dead Trees from Map blueprint
    list.addAll(const [
      PropItem(
        id: 'pine_church_01',
        assetId: GameAssetRegistry.villagePineTree,
        worldX: 5.0,
        worldY: -8.5,
        displayWidth: 85,
        displayHeight: 145,
        collisionWidth: 0.4,
        collisionHeight: 0.4,
        hasCollision: true,
      ),
      PropItem(
        id: 'pine_church_02',
        assetId: GameAssetRegistry.villagePineTree,
        worldX: 2.0,
        worldY: -9.0,
        displayWidth: 95,
        displayHeight: 160,
        collisionWidth: 0.4,
        collisionHeight: 0.4,
        hasCollision: true,
      ),
      PropItem(
        id: 'dead_tree_plaza',
        assetId: GameAssetRegistry.villageDeadTree,
        worldX: 0.8,
        worldY: 3.5,
        displayWidth: 80,
        displayHeight: 135,
        collisionWidth: 0.4,
        collisionHeight: 0.4,
        hasCollision: true,
      ),
      PropItem(
        id: 'pine_farm_01',
        assetId: GameAssetRegistry.villagePineTree,
        worldX: -7.0,
        worldY: -4.5,
        displayWidth: 90,
        displayHeight: 150,
        collisionWidth: 0.4,
        collisionHeight: 0.4,
        hasCollision: true,
      ),
      PropItem(
        id: 'pine_watermill_01',
        assetId: GameAssetRegistry.villagePineTree,
        worldX: -3.5,
        worldY: 7.0,
        displayWidth: 85,
        displayHeight: 140,
        collisionWidth: 0.4,
        collisionHeight: 0.4,
        hasCollision: true,
      ),
      PropItem(
        id: 'pine_sawmill_01',
        assetId: GameAssetRegistry.villagePineTree,
        worldX: 10.0,
        worldY: 0.5,
        displayWidth: 85,
        displayHeight: 140,
        collisionWidth: 0.4,
        collisionHeight: 0.4,
        hasCollision: true,
      ),
    ]);

    return list;
  }

  @override
  Future<void> onLoad() async {
    final scale = IsometricCoordinates.worldScale;
    for (final p in props) {
      add(PropSpriteComponent(p));

      if (p.hasCollision) {
        collisionManager.addObstacle(
          IsometricCollisionBox(
            id: 'prop_${p.id}',
            worldX: p.worldX * scale,
            worldY: p.worldY * scale,
            halfWidth: (p.collisionWidth / 2) * scale,
            halfHeight: (p.collisionHeight / 2) * scale,
            label: p.id,
          ),
        );
      }
    }
  }
}
