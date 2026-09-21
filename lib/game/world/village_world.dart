import 'package:flame/components.dart';
import '../player/alex_component.dart';
import '../player/player_animation_controller.dart';
import '../player/player_controller.dart';
import 'collision_box.dart';
import 'isometric_coordinates.dart';
import 'layers/building_layer.dart';
import 'layers/characters_layer.dart';
import 'layers/ground_layer.dart';
import 'layers/prop_layer.dart';
import 'layers/road_layer.dart';
import 'layers/weather_effects_layer.dart';
import 'navigation_grid.dart';
import 'point_of_interest.dart';
import 'village_map.dart';

/// The root Flame World component for the reconstructed Village scene based on Map village .png.
class VillageWorld extends World with HasGameRef {
  final CollisionManager collisionManager = CollisionManager();
  final VillageMap villageMap;
  late final NavigationGrid navigationGrid;
  late final PlayerController playerController;
  late final PlayerAnimationController playerAnimationController;
  late final AlexComponent alex;

  // Calibrated world boundaries enclosing the complete village blueprint
  double get minWorldX => villageMap.bounds.minWorldX * IsometricCoordinates.worldScale;
  double get maxWorldX => villageMap.bounds.maxWorldX * IsometricCoordinates.worldScale;
  double get minWorldY => villageMap.bounds.minWorldY * IsometricCoordinates.worldScale;
  double get maxWorldY => villageMap.bounds.maxWorldY * IsometricCoordinates.worldScale;

  final double? initialPlayerX;
  final double? initialPlayerY;
  final String? initialOrientation;

  // Active Point of Interest
  PointOfInterest? activePOI;

  VillageWorld({
    VillageMap? map,
    this.initialPlayerX,
    this.initialPlayerY,
    this.initialOrientation,
  }) : villageMap = map ?? VillageMap.canonical();

  @override
  Future<void> onLoad() async {
    navigationGrid = NavigationGrid(
      map: villageMap,
      collisionManager: collisionManager,
    );

    // 1. Initialize Player Controllers at canonical entrance bridge
    final spawnX = initialPlayerX ?? (villageMap.playerSpawn.worldX * IsometricCoordinates.worldScale);
    final spawnY = initialPlayerY ?? (villageMap.playerSpawn.worldY * IsometricCoordinates.worldScale);
    final spawnOrient = initialOrientation ?? villageMap.playerSpawn.orientation;

    playerController = PlayerController(
      worldX: spawnX,
      worldY: spawnY,
      orientation: spawnOrient,
      collisionManager: collisionManager,
    );

    playerAnimationController = PlayerAnimationController();
    await playerAnimationController.load(gameRef);

    alex = AlexComponent(
      controller: playerController,
      animationController: playerAnimationController,
    );

    // 2. Add Perimeter World Boundary Collisions
    _addPerimeterCollisions();

    // 3. Mount Layers in strict isometric order
    // Ground (Multi-zone: River, Bridge, Cobblestones, Plaza, Snow, Yards)
    add(GroundLayer(gridRadius: (24 * IsometricCoordinates.worldScale).ceil()));

    // Roads & Pathways
    add(RoadLayer());

    // Buildings (Reconstructed from Map village .png)
    add(BuildingLayer(
      collisionManager: collisionManager,
      villageMap: villageMap,
    ));

    // Props (Well, Statue, Market Stalls, Crane, Cemetery Gate, Street Lamps, Trees)
    add(PropLayer(
      collisionManager: collisionManager,
      villageMap: villageMap,
    ));

    // Characters (Alex with calibrated human scale and dynamic Z-ordering)
    add(CharactersLayer(alex: alex));

    // Atmospheric Weather (Wind-driven snow, freezing sleet, fog mist)
    add(WeatherEffectsLayer());
  }

  @override
  void update(double dt) {
    super.update(dt);
    // Check nearest Point of Interest
    activePOI = VillagePOIRegistry.findActivePOI(
      playerController.worldX,
      playerController.worldY,
    );
  }

  void _addPerimeterCollisions() {
    final hw = 0.5 * IsometricCoordinates.worldScale;
    // West mountain cliff boundary
    collisionManager.addObstacle(
      IsometricCollisionBox(
        id: 'boundary_west',
        worldX: minWorldX - hw,
        worldY: (minWorldY + maxWorldY) / 2,
        halfWidth: hw,
        halfHeight: (maxWorldY - minWorldY) / 2,
        label: 'boundary',
      ),
    );
    // East mountain cliff boundary
    collisionManager.addObstacle(
      IsometricCollisionBox(
        id: 'boundary_east',
        worldX: maxWorldX + hw,
        worldY: (minWorldY + maxWorldY) / 2,
        halfWidth: hw,
        halfHeight: (maxWorldY - minWorldY) / 2,
        label: 'boundary',
      ),
    );
    // South frozen river boundary
    collisionManager.addObstacle(
      IsometricCollisionBox(
        id: 'boundary_south',
        worldX: (minWorldX + maxWorldX) / 2,
        worldY: maxWorldY + hw,
        halfWidth: (maxWorldX - minWorldX) / 2,
        halfHeight: hw,
        label: 'boundary',
      ),
    );
    // North mountain boundary
    collisionManager.addObstacle(
      IsometricCollisionBox(
        id: 'boundary_north',
        worldX: (minWorldX + maxWorldX) / 2,
        worldY: minWorldY - hw,
        halfWidth: (maxWorldX - minWorldX) / 2,
        halfHeight: hw,
        label: 'boundary',
      ),
    );
  }
}
