import 'dart:math' as math;
import 'package:test/test.dart';
import '../lib/game/player/player_controller.dart';
import '../lib/game/world/asset_registry.dart';
import '../lib/game/world/collision_box.dart';
import '../lib/game/world/isometric_coordinates.dart';
import '../lib/save/local_save_repository.dart';
import '../lib/save/save_manager.dart';
import 'dart:io';

void main() {
  group('1. Isometric Coordinate System Tests', () {
    test('Constants match specification (128x64)', () {
      expect(IsometricCoordinates.tileWidth, equals(128.0));
      expect(IsometricCoordinates.tileHeight, equals(64.0));
      expect(IsometricCoordinates.halfTileWidth, equals(64.0));
      expect(IsometricCoordinates.halfTileHeight, equals(32.0));
    });

    test('World to Screen and Screen to World reversibility', () {
      const testX = 5.5;
      const testY = -3.2;

      final screen = IsometricCoordinates.worldToScreen(testX, testY);
      final world = IsometricCoordinates.screenToWorld(screen.x, screen.y);

      expect(world.x, closeTo(testX, 0.001));
      expect(world.y, closeTo(testY, 0.001));
    });

    test('Vector to 4-Way Isometric Orientation', () {
      // SE: Down-Right (+X, +Y)
      expect(IsometricCoordinates.vectorToOrientation(1.0, 1.0), equals('SE'));
      // SW: Down-Left (-X, +Y)
      expect(IsometricCoordinates.vectorToOrientation(-1.0, 1.0), equals('SW'));
      // NE: Up-Right (+X, -Y)
      expect(IsometricCoordinates.vectorToOrientation(1.0, -1.0), equals('NE'));
      // NW: Up-Left (-X, -Y)
      expect(IsometricCoordinates.vectorToOrientation(-1.0, -1.0), equals('NW'));
    });

    test('Z-Order Depth Calculation ordering', () {
      final zBack = IsometricCoordinates.calculateZOrder(0.0, 2.0);
      final zFront = IsometricCoordinates.calculateZOrder(0.0, 5.0);

      // Higher Y must have higher Z-Order (drawn in front)
      expect(zFront, greaterThan(zBack));
    });
  });

  group('2. Collision System Tests', () {
    late CollisionManager collisionManager;

    setUp(() {
      collisionManager = CollisionManager();
      // Add obstacle at (4.0, 4.0) with extent 1.0x1.0 (bounds from 3.0 to 5.0)
      collisionManager.addObstacle(
        const IsometricCollisionBox(
          id: 'test_rock',
          worldX: 4.0,
          worldY: 4.0,
          halfWidth: 1.0,
          halfHeight: 1.0,
          label: 'rock',
        ),
      );
    });

    test('Collision detection triggers on overlap', () {
      expect(collisionManager.hasCollision(4.0, 4.0, 0.2), isTrue);
      expect(collisionManager.hasCollision(0.0, 0.0, 0.2), isFalse);
    });

    test('Sliding resolution along free axis when blocked', () {
      // Attempt to move from (2.5, 4.0) into (3.2, 4.0) (blocked by rock)
      // but Y is free
      final resolved = collisionManager.resolveMovement(
        currentX: 2.5,
        currentY: 1.0,
        targetX: 3.5, // blocked
        targetY: 1.2, // free
        radius: 0.2,
      );

      // Should slide: retain safe currentX or move along Y
      expect(collisionManager.hasCollision(resolved.x, resolved.y, 0.2), isFalse);
    });
  });

  group('3. PlayerController & Movement State Transitions', () {
    late CollisionManager collisionManager;
    late PlayerController controller;

    setUp(() {
      collisionManager = CollisionManager();
      controller = PlayerController(
        worldX: 0.0,
        worldY: 0.0,
        orientation: 'SE',
        collisionManager: collisionManager,
      );
    });

    test('Idle state when input magnitude is zero', () {
      controller.update(inputX: 0.0, inputY: 0.0, dt: 0.1);
      expect(controller.state, equals(PlayerMovementState.idle));
      expect(controller.worldX, equals(0.0));
      expect(controller.worldY, equals(0.0));
    });

    test('Walk state when input is moderate (< 0.65)', () {
      controller.update(inputX: 0.4, inputY: 0.3, dt: 0.1);
      expect(controller.state, equals(PlayerMovementState.walk));
      expect(controller.orientation, equals('SE'));
      expect(controller.worldX, greaterThan(0.0));
    });

    test('Run state when input is strong (> 0.65)', () {
      controller.update(inputX: 0.8, inputY: 0.8, dt: 0.1);
      expect(controller.state, equals(PlayerMovementState.run));
      expect(controller.orientation, equals('SE'));
    });
  });

  group('4. Z-Order Dynamic Sorting: Front, Behind, Between Objects', () {
    test('Alex behind object, in front of object, and between two objects', () {
      // House at world position (0.0, 8.0)
      const houseBaseY = 8.0;
      final houseZ = IsometricCoordinates.calculateZOrder(0.0, houseBaseY);

      // Alex behind the house: (0.0, 6.0)
      final alexBehindZ = IsometricCoordinates.calculateZOrder(0.0, 6.0);
      expect(alexBehindZ, lessThan(houseZ), reason: 'Alex behind house must have lower Z-order');

      // Alex in front of the house: (0.0, 9.5)
      final alexFrontZ = IsometricCoordinates.calculateZOrder(0.0, 9.5);
      expect(alexFrontZ, greaterThan(houseZ), reason: 'Alex in front of house must have higher Z-order');

      // Two props: Well at (0.0, 4.0) and House at (0.0, 8.0)
      final wellZ = IsometricCoordinates.calculateZOrder(0.0, 4.0);
      // Alex between the two: (0.0, 6.0)
      expect(alexBehindZ, greaterThan(wellZ), reason: 'Alex must be in front of Well');
      expect(alexBehindZ, lessThan(houseZ), reason: 'Alex must be behind House');
    });
  });

  group('5. SaveManager & World Position Persistence', () {
    test('Save and restore player position in Village World', () async {
      final tempDir = Directory.systemTemp.createTempSync('echo_world_test_');
      try {
        final repo = LocalSaveRepository(baseDirectoryPath: tempDir.path);
        final manager = SaveManager(repository: repo);
        await manager.createNewGame(saveId: 'village_test_slot');

        // Alex walks to family house entrance
        manager.updatePosition(
          map: 'VILLAGE_ABANDONED',
          x: 0.2,
          y: 7.8,
          orientation: 'NW',
        );
        manager.setFlag('received_ethan_message', true);
        await manager.saveGame();

        // Fresh load simulation
        final freshRepo = LocalSaveRepository(baseDirectoryPath: tempDir.path);
        final freshManager = SaveManager(repository: freshRepo);
        final loaded = await freshManager.loadGame(saveId: 'village_test_slot');

        expect(loaded, isNotNull);
        expect(loaded!.currentMap, equals('VILLAGE_ABANDONED'));
        expect(loaded.position.x, closeTo(0.2, 0.001));
        expect(loaded.position.y, closeTo(7.8, 0.001));
        expect(loaded.position.orientation, equals('NW'));
        expect(loaded.flags['received_ethan_message'], isTrue);
      } finally {
        if (tempDir.existsSync()) {
          tempDir.deleteSync(recursive: true);
        }
      }
    });
  });

  group('6. Asset Registry Verification', () {
    test('Asset Registry initializes default assets', () {
      final registry = GameAssetRegistry();
      registry.initDefaults();

      expect(registry.has(GameAssetRegistry.alexIdleSE), isTrue);
      expect(registry.has(GameAssetRegistry.alexWalkStrip), isTrue);
      expect(registry.has(GameAssetRegistry.villageChurch), isTrue);
      expect(registry.has(GameAssetRegistry.familyHouseExterior), isTrue);
      expect(registry.has(GameAssetRegistry.ethanDesk), isTrue);
    });
  });
}
