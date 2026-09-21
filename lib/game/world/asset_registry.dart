import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

enum AssetType {
  character,
  characterAnimation,
  building,
  prop,
  tile,
  interior,
  item,
  map,
  unknown
}

class AssetEntry {
  final String assetId;
  final String path;
  final AssetType type;
  final String category;
  final int width;
  final int height;
  final double pivotX;
  final double pivotY;
  final double scale;
  final String orientation;
  final bool hasCollision;
  final double collisionWidth;
  final double collisionHeight;
  final bool isInteractable;

  const AssetEntry({
    required this.assetId,
    required this.path,
    required this.type,
    required this.category,
    required this.width,
    required this.height,
    this.pivotX = 0.5,
    this.pivotY = 0.5,
    this.scale = 1.0,
    this.orientation = 'NONE',
    this.hasCollision = false,
    this.collisionWidth = 0.0,
    this.collisionHeight = 0.0,
    this.isInteractable = false,
  });

  factory AssetEntry.fromJson(Map<String, dynamic> json) {
    final typeStr = json['type'] as String? ?? '';
    final assetType = _parseType(typeStr);
    final col = json['collision'] as Map<String, dynamic>? ?? {};

    return AssetEntry(
      assetId: json['assetId'] as String,
      path: json['path'] as String,
      type: assetType,
      category: json['category'] as String? ?? 'misc',
      width: (json['width'] as num?)?.toInt() ?? 0,
      height: (json['height'] as num?)?.toInt() ?? 0,
      pivotX: (json['pivot']?['x'] as num?)?.toDouble() ?? 0.5,
      pivotY: (json['pivot']?['y'] as num?)?.toDouble() ?? 0.5,
      scale: (json['scale'] as num?)?.toDouble() ?? 1.0,
      orientation: json['isometricOrientation'] as String? ?? 'NONE',
      hasCollision: (col['type'] as String? ?? 'none') != 'none',
      collisionWidth: (col['width'] as num?)?.toDouble() ?? 0.0,
      collisionHeight: (col['height'] as num?)?.toDouble() ?? 0.0,
      isInteractable: json['interactable'] as bool? ?? false,
    );
  }

  static AssetType _parseType(String type) {
    switch (type) {
      case 'character':
        return AssetType.character;
      case 'character_animation':
        return AssetType.characterAnimation;
      case 'building':
        return AssetType.building;
      case 'prop':
        return AssetType.prop;
      case 'tile':
        return AssetType.tile;
      case 'interior':
        return AssetType.interior;
      case 'item':
        return AssetType.item;
      case 'map':
        return AssetType.map;
      default:
        return AssetType.unknown;
    }
  }
}

/// Data-Driven Asset Registry holding references to all canonical game graphics.
class GameAssetRegistry {
  static final GameAssetRegistry _instance = GameAssetRegistry._internal();
  factory GameAssetRegistry() => _instance;
  GameAssetRegistry._internal();

  final Map<String, AssetEntry> _entries = {};
  bool _initialized = false;

  bool get isInitialized => _initialized;
  int get totalAssets => _entries.length;

  // ===========================================================================
  // Canonical Static Asset IDs for Phase 2 Gameplay
  // ===========================================================================
  
  // Alex Character & Animations
  static const String alexIdleSE = 'alex_animation_idle03';
  static const String alexIdleSW = 'alex_animation_idle04';
  static const String alexIdleNE = 'alex_animation_idle06';
  static const String alexIdleNW = 'alex_animation_idle07';
  static const String alexWalkStrip = 'alex_marche01';
  static const String alexRunStrip = 'alex_course01';
  static const String alexInteraction = 'alex_interaction01';
  static const String alexPortrait = 'alex_animation_idle02';

  // Village Buildings & Exterior
  static const String villageChurch = 'village_abandonne_environment_sprite_sheet05';
  static const String villageHouse01 = 'village_abandonne_environment_sprite_sheet01';
  static const String villageHouse02 = 'village_abandonne_environment_sprite_sheet02';
  static const String villageHouse03 = 'village_abandonne_environment_sprite_sheet03';
  static const String villageHouse04 = 'village_abandonne_environment_sprite_sheet04';
  static const String villageIronGate = 'village_abandonne_environment_sprite_sheet15';
  static const String villageStoneSlab = 'village_abandonne_environment_sprite_sheet25';
  static const String villageWell = 'village_abandonne_route_decor_exterieur01';
  static const String villageBridge = 'village_abandonne_route_decor_exterieur05';
  static const String villageMasterMap = 'map_village';

  // Family House Exterior & Interior
  static const String familyHouseExterior = 'maison_familiale_exterieure01';
  static const String alexBedroomCutaway = 'chambre_d_alex01';
  static const String ethanDesk = 'bureau_d_ethan_01';
  static const String woodenWardrobe = 'armoire_en_bois01';
  static const String woodenBed = 'lit_en_bois01';

  // Key Items & Evidence
  static const String itemOldKey = 'cle_ancienne01';
  static const String itemEthanCassette = 'cassette_audio_d_ethan00';
  static const String itemAlexPhone = 'telephone_d_alex00';
  static const String itemInvestigationBoard = 'tableau_d_enquete_01';
  static const String itemEthanNotebook = 'carnet_d_ethan01';

  /// Pre-populates typed entries so game boots instantly without waiting for JSON parse.
  void initDefaults() {
    if (_initialized) return;

    final defaultList = [
      // Alex Idle
      const AssetEntry(
        assetId: alexIdleSE,
        path: 'assets/images/characters/alex/idle/Alex-—-Animation-Idle03.png',
        type: AssetType.characterAnimation,
        category: 'alex',
        width: 139,
        height: 296,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'SE',
        hasCollision: true,
        collisionWidth: 28,
        collisionHeight: 16,
      ),
      const AssetEntry(
        assetId: alexIdleSW,
        path: 'assets/images/characters/alex/idle/Alex-—-Animation-Idle04.png',
        type: AssetType.characterAnimation,
        category: 'alex',
        width: 135,
        height: 286,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'SW',
        hasCollision: true,
        collisionWidth: 28,
        collisionHeight: 16,
      ),
      const AssetEntry(
        assetId: alexIdleNE,
        path: 'assets/images/characters/alex/idle/Alex-—-Animation-Idle06.png',
        type: AssetType.characterAnimation,
        category: 'alex',
        width: 134,
        height: 295,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'NE',
        hasCollision: true,
        collisionWidth: 28,
        collisionHeight: 16,
      ),
      const AssetEntry(
        assetId: alexIdleNW,
        path: 'assets/images/characters/alex/idle/Alex-—-Animation-Idle07.png',
        type: AssetType.characterAnimation,
        category: 'alex',
        width: 128,
        height: 287,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'NW',
        hasCollision: true,
        collisionWidth: 28,
        collisionHeight: 16,
      ),

      // Alex Walk & Run
      const AssetEntry(
        assetId: alexWalkStrip,
        path: 'assets/images/characters/alex/walk/Alex-—-Marche01.png',
        type: AssetType.characterAnimation,
        category: 'alex',
        width: 392,
        height: 182,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'SE',
      ),
      const AssetEntry(
        assetId: alexRunStrip,
        path: 'assets/images/characters/alex/run/Alex-—-Course01.png',
        type: AssetType.characterAnimation,
        category: 'alex',
        width: 126,
        height: 169,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'SE',
      ),

      // Village Environment
      const AssetEntry(
        assetId: villageChurch,
        path: 'assets/images/environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet05.png',
        type: AssetType.building,
        category: 'village',
        width: 304,
        height: 401,
        pivotX: 0.5,
        pivotY: 0.90,
        hasCollision: true,
        collisionWidth: 220,
        collisionHeight: 140,
      ),
      const AssetEntry(
        assetId: villageHouse01,
        path: 'assets/images/environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet01.png',
        type: AssetType.building,
        category: 'village',
        width: 334,
        height: 313,
        pivotX: 0.5,
        pivotY: 0.88,
        hasCollision: true,
        collisionWidth: 240,
        collisionHeight: 120,
      ),
      const AssetEntry(
        assetId: villageIronGate,
        path: 'assets/images/environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet15.png',
        type: AssetType.prop,
        category: 'village',
        width: 229,
        height: 148,
        pivotX: 0.5,
        pivotY: 0.85,
        hasCollision: true,
        collisionWidth: 160,
        collisionHeight: 40,
      ),
      const AssetEntry(
        assetId: villageStoneSlab,
        path: 'assets/images/environments/village/buildings/Village-abandonné-—-Environment-Sprite-Sheet25.png',
        type: AssetType.tile,
        category: 'village',
        width: 149,
        height: 101,
        pivotX: 0.5,
        pivotY: 0.5,
      ),
      const AssetEntry(
        assetId: villageWell,
        path: 'assets/images/environments/village/decor/Village-abandonné-—-Route-&-décor-extérieur01.png',
        type: AssetType.prop,
        category: 'village',
        width: 155,
        height: 173,
        pivotX: 0.5,
        pivotY: 0.85,
        hasCollision: true,
        collisionWidth: 80,
        collisionHeight: 60,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: familyHouseExterior,
        path: 'assets/images/environments/family_house/exterior/Maison-familiale-extérieure01.png',
        type: AssetType.building,
        category: 'family_house',
        width: 366,
        height: 341,
        pivotX: 0.5,
        pivotY: 0.88,
        hasCollision: true,
        collisionWidth: 260,
        collisionHeight: 140,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: ethanDesk,
        path: 'assets/images/props/furniture/desk/Bureau-d’Ethan-01.png',
        type: AssetType.prop,
        category: 'family_house',
        width: 326,
        height: 329,
        pivotX: 0.5,
        pivotY: 0.85,
        hasCollision: true,
        collisionWidth: 180,
        collisionHeight: 100,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: villageMasterMap,
        path: 'assets/images/environments/village/map_tiles/Map village .png',
        type: AssetType.map,
        category: 'village',
        width: 1536,
        height: 1024,
        pivotX: 0.5,
        pivotY: 0.5,
      ),
    ];

    for (final entry in defaultList) {
      _entries[entry.assetId] = entry;
    }
    _initialized = true;
  }

  /// Loads the full asset_registry.json data file.
  Future<void> loadFullRegistry() async {
    initDefaults();
    try {
      final jsonStr = await rootBundle.loadString('assets/data/asset_registry.json');
      final data = jsonDecode(jsonStr) as Map<String, dynamic>;
      final assetsMap = data['assets'] as Map<String, dynamic>? ?? {};

      for (final entry in assetsMap.entries) {
        final val = entry.value as Map<String, dynamic>;
        final assetEntry = AssetEntry.fromJson(val);
        _entries[assetEntry.assetId] = assetEntry;
      }
    } catch (_) {
      // Fallback to built-in default entries
    }
  }

  AssetEntry? get(String assetId) {
    if (!_initialized) initDefaults();
    return _entries[assetId];
  }

  String getPath(String assetId) {
    return get(assetId)?.path ?? '';
  }

  bool has(String assetId) {
    if (!_initialized) initDefaults();
    return _entries.containsKey(assetId);
  }
}
