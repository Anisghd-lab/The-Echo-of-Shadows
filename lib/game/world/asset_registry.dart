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

/// Official Data-Driven Asset Registry holding references to all canonical game graphics from new assets.
class GameAssetRegistry {
  static final GameAssetRegistry _instance = GameAssetRegistry._internal();
  factory GameAssetRegistry() => _instance;
  GameAssetRegistry._internal();

  final Map<String, AssetEntry> _entries = {};
  bool _initialized = false;

  bool get isInitialized => _initialized;
  int get totalAssets => _entries.length;

  // ===========================================================================
  // Official Canonical Asset IDs (New Assets Library)
  // ===========================================================================

  // Alex Character (Cardinal & 360° Rotations)
  static const String alexNorth = 'alex_personnage_principal01';
  static const String alexNorthEast = 'alex_personnage_principal03';
  static const String alexEast = 'alex_personnage_principal05';
  static const String alexSouthEast = 'alex_personnage_principal07';
  static const String alexSouth = 'alex_personnage_principal09';
  static const String alexSouthWest = 'alex_personnage_principal11';
  static const String alexWest = 'alex_personnage_principal13';
  static const String alexNorthWest = 'alex_personnage_principal15';

  // Legacy Aliases for seamless compatibility
  static const String alexIdleSE = 'alex_personnage_principal07';
  static const String alexIdleSW = 'alex_personnage_principal11';
  static const String alexIdleNE = 'alex_personnage_principal03';
  static const String alexIdleNW = 'alex_personnage_principal15';
  static const String alexWalkStrip = 'alex_personnage_principal07';
  static const String alexWalkSE = 'alex_personnage_principal07';
  static const String alexWalkSW = 'alex_personnage_principal11';
  static const String alexWalkNE = 'alex_personnage_principal03';
  static const String alexWalkNW = 'alex_personnage_principal15';
  static const String alexRunStrip = 'alex_personnage_principal07';
  static const String alexRunSE = 'alex_personnage_principal07';
  static const String alexRunSW = 'alex_personnage_principal11';
  static const String alexRunNE = 'alex_personnage_principal03';
  static const String alexRunNW = 'alex_personnage_principal15';
  static const String alexInteraction = 'alex_personnage_principal09';
  static const String alexInteractSE = 'alex_personnage_principal07';
  static const String alexInteractSW = 'alex_personnage_principal11';
  static const String alexInteractNE = 'alex_personnage_principal03';
  static const String alexInteractNW = 'alex_personnage_principal15';
  static const String alexPortrait = 'alex_personnage_principal09';

  // NPCs
  static const String npcEmma = 'emma01';
  static const String npcEthan = 'ethan_frere_dalex01';
  static const String npcJames = 'officer_james01';
  static const String npcMichael = 'old_michael01';

  // Village Buildings & Exterior
  static const String villageChurch = 'village_environment_104';
  static const String villageHouse01 = 'village_environment_101';
  static const String villageHouse02 = 'village_environment_105';
  static const String villageHouse03 = 'village_environment_106';
  static const String villageHouse04 = 'village_environment_102';
  static const String villageWatermill = 'village_environment_103';
  static const String villageWindmill = 'village_environment_102';
  static const String villageBridge = 'village_environment_108';
  static const String villageWell = 'village_environment_111';
  static const String villageStreetLamp = 'village_environment_110';
  static const String villageIronGate = 'village_environment_113';
  static const String villageMarketStall01 = 'village_environment_116';
  static const String villageMarketStall02 = 'village_environment_121';
  static const String villageCrane = 'village_environment_129';
  static const String villageBoat = 'village_environment_152';
  static const String villageMasterMap = 'map_du_village';

  // Family House
  static const String familyHouseExterior = 'maison_familliale02';
  static const String familyHouseInterior = 'maison_familliale03';
  static const String alexBedroomCutaway = 'maison_familliale04';
  static const String familyKitchen = 'maison_familliale05';
  static const String familyHallway = 'maison_familliale06';

  // Bunker
  static const String bunkerExterior = 'interiors_bunker02';
  static const String bunkerInterior = 'interiors_bunker03';
  static const String bunkerControlRoom = 'interiors_bunker04';

  // Narrative & Interactive Props
  static const String itemAlexPhone = 'telephone_prpos01';
  static const String itemEthanCassette = 'narrative_props_furniture01';
  static const String itemAudioRecorder = 'narrative_props_furniture03';
  static const String itemOldKey = 'narrative_props_furniture04';
  static const String itemEthanNotebook = 'narrative_props_furniture05';
  static const String itemPhotographs = 'narrative_props_furniture06';
  static const String itemInvestigationDocuments = 'narrative_props_furniture07';
  static const String itemInvestigationBoard = 'narrative_props_furniture08';
  static const String itemCountdownDevice = 'narrative_props_furniture09';
  static const String ethanDesk = 'narrative_props_furniture05';
  static const String woodenWardrobe = 'narrative_props_furniture08';
  static const String woodenBed = 'maison_familliale07';

  // Nature & Ground Tiles
  static const String villagePineTree = 'nature_gameplay_structures02';
  static const String villageDeadTree = 'nature_gameplay_structures06';
  static const String villageStoneSlab = 'nature_gameplay_structures04';
  static const String villageStoneSlabVar = 'nature_gameplay_structures07';
  static const String villageSnowSlab = 'nature_gameplay_structures08';
  static const String villageIceSlab = 'nature_gameplay_structures10';
  static const String villageCliff = 'nature_gameplay_structures09';

  void initDefaults() {
    if (_initialized) return;

    final defaultList = [
      // Alex Orientations
      const AssetEntry(
        assetId: alexNorth,
        path: 'assets/images/characters/alex/Alex-—-Personnage-principal01.png',
        type: AssetType.character,
        category: 'alex',
        width: 77,
        height: 202,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'N',
      ),
      const AssetEntry(
        assetId: alexEast,
        path: 'assets/images/characters/alex/Alex-—-Personnage-principal05.png',
        type: AssetType.character,
        category: 'alex',
        width: 65,
        height: 203,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'E',
      ),
      const AssetEntry(
        assetId: alexSouth,
        path: 'assets/images/characters/alex/Alex-—-Personnage-principal09.png',
        type: AssetType.character,
        category: 'alex',
        width: 79,
        height: 201,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'S',
      ),
      const AssetEntry(
        assetId: alexWest,
        path: 'assets/images/characters/alex/Alex-—-Personnage-principal13.png',
        type: AssetType.character,
        category: 'alex',
        width: 67,
        height: 202,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'W',
      ),
      const AssetEntry(
        assetId: alexSouthEast,
        path: 'assets/images/characters/alex/Alex-—-Personnage-principal07.png',
        type: AssetType.character,
        category: 'alex',
        width: 66,
        height: 202,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'SE',
      ),
      const AssetEntry(
        assetId: alexSouthWest,
        path: 'assets/images/characters/alex/Alex-—-Personnage-principal11.png',
        type: AssetType.character,
        category: 'alex',
        width: 66,
        height: 203,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'SW',
      ),
      const AssetEntry(
        assetId: alexNorthWest,
        path: 'assets/images/characters/alex/Alex-—-Personnage-principal15.png',
        type: AssetType.character,
        category: 'alex',
        width: 67,
        height: 201,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'NW',
      ),
      const AssetEntry(
        assetId: alexNorthEast,
        path: 'assets/images/characters/alex/Alex-—-Personnage-principal03.png',
        type: AssetType.character,
        category: 'alex',
        width: 69,
        height: 201,
        pivotX: 0.5,
        pivotY: 0.95,
        orientation: 'NE',
      ),

      // NPCs
      const AssetEntry(
        assetId: npcEmma,
        path: 'assets/images/characters/emma/Emma01.png',
        type: AssetType.character,
        category: 'emma',
        width: 79,
        height: 200,
        pivotX: 0.5,
        pivotY: 0.95,
      ),
      const AssetEntry(
        assetId: npcEthan,
        path: 'assets/images/characters/ethan/Ethan-—-Frère-d’Alex01.png',
        type: AssetType.character,
        category: 'ethan',
        width: 77,
        height: 193,
        pivotX: 0.5,
        pivotY: 0.95,
      ),
      const AssetEntry(
        assetId: npcJames,
        path: 'assets/images/characters/officer_james/Officer-James01.png',
        type: AssetType.character,
        category: 'james',
        width: 82,
        height: 196,
        pivotX: 0.5,
        pivotY: 0.95,
      ),
      const AssetEntry(
        assetId: npcMichael,
        path: 'assets/images/characters/old_michael/Old-Michael01.png',
        type: AssetType.character,
        category: 'michael',
        width: 78,
        height: 188,
        pivotX: 0.5,
        pivotY: 0.95,
      ),

      // Village Buildings & Key Environment
      const AssetEntry(
        assetId: villageChurch,
        path: 'assets/images/environments/village/VILLAGE-ENVIRONMENT-104.png',
        type: AssetType.building,
        category: 'village',
        width: 265,
        height: 319,
        pivotX: 0.5,
        pivotY: 0.9,
        hasCollision: true,
        collisionWidth: 200,
        collisionHeight: 180,
      ),
      const AssetEntry(
        assetId: villageHouse01,
        path: 'assets/images/environments/village/VILLAGE-ENVIRONMENT-101.png',
        type: AssetType.building,
        category: 'village',
        width: 275,
        height: 289,
        pivotX: 0.5,
        pivotY: 0.9,
        hasCollision: true,
      ),
      const AssetEntry(
        assetId: villageHouse02,
        path: 'assets/images/environments/village/VILLAGE-ENVIRONMENT-105.png',
        type: AssetType.building,
        category: 'village',
        width: 345,
        height: 304,
        pivotX: 0.5,
        pivotY: 0.9,
        hasCollision: true,
      ),
      const AssetEntry(
        assetId: villageWatermill,
        path: 'assets/images/environments/village/VILLAGE-ENVIRONMENT-103.png',
        type: AssetType.building,
        category: 'village',
        width: 348,
        height: 298,
        pivotX: 0.5,
        pivotY: 0.9,
        hasCollision: true,
      ),
      const AssetEntry(
        assetId: villageWindmill,
        path: 'assets/images/environments/village/VILLAGE-ENVIRONMENT-102.png',
        type: AssetType.building,
        category: 'village',
        width: 289,
        height: 299,
        pivotX: 0.5,
        pivotY: 0.9,
        hasCollision: true,
      ),
      const AssetEntry(
        assetId: villageBridge,
        path: 'assets/images/environments/village/VILLAGE-ENVIRONMENT-108.png',
        type: AssetType.prop,
        category: 'village',
        width: 208,
        height: 149,
      ),
      const AssetEntry(
        assetId: villageWell,
        path: 'assets/images/environments/village/VILLAGE-ENVIRONMENT-111.png',
        type: AssetType.prop,
        category: 'village',
        width: 227,
        height: 186,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: villageStreetLamp,
        path: 'assets/images/environments/village/VILLAGE-ENVIRONMENT-110.png',
        type: AssetType.prop,
        category: 'village',
        width: 89,
        height: 113,
      ),
      const AssetEntry(
        assetId: villageMasterMap,
        path: 'assets/images/environments/village/map du village.png',
        type: AssetType.map,
        category: 'village',
        width: 1536,
        height: 1024,
      ),

      // Family House
      const AssetEntry(
        assetId: familyHouseExterior,
        path: 'assets/images/environments/family_house/MAISON-FAMILLIALE02.png',
        type: AssetType.building,
        category: 'family_house',
        width: 359,
        height: 337,
        hasCollision: true,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: familyHouseInterior,
        path: 'assets/images/environments/family_house/MAISON-FAMILLIALE03.png',
        type: AssetType.interior,
        category: 'family_house',
        width: 282,
        height: 246,
      ),
      const AssetEntry(
        assetId: alexBedroomCutaway,
        path: 'assets/images/environments/family_house/MAISON-FAMILLIALE04.png',
        type: AssetType.interior,
        category: 'family_house',
        width: 295,
        height: 242,
      ),

      // Bunker
      const AssetEntry(
        assetId: bunkerExterior,
        path: 'assets/images/environments/bunker/INTERIORS-BUNKER02.png',
        type: AssetType.building,
        category: 'bunker',
        width: 351,
        height: 224,
        hasCollision: true,
      ),
      const AssetEntry(
        assetId: bunkerInterior,
        path: 'assets/images/environments/bunker/INTERIORS-BUNKER03.png',
        type: AssetType.interior,
        category: 'bunker',
        width: 376,
        height: 223,
      ),

      // Interactive & Narrative Items
      const AssetEntry(
        assetId: itemAlexPhone,
        path: 'assets/images/props/interactive/TELEPHONE-PRPOS01.png',
        type: AssetType.item,
        category: 'props',
        width: 289,
        height: 393,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: itemEthanCassette,
        path: 'assets/images/props/narrative/NARRATIVE-PROPS-FURNITURE01.png',
        type: AssetType.item,
        category: 'props',
        width: 103,
        height: 154,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: itemAudioRecorder,
        path: 'assets/images/props/narrative/NARRATIVE-PROPS-FURNITURE03.png',
        type: AssetType.item,
        category: 'props',
        width: 123,
        height: 97,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: itemOldKey,
        path: 'assets/images/props/narrative/NARRATIVE-PROPS-FURNITURE04.png',
        type: AssetType.item,
        category: 'props',
        width: 107,
        height: 115,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: itemEthanNotebook,
        path: 'assets/images/props/narrative/NARRATIVE-PROPS-FURNITURE05.png',
        type: AssetType.item,
        category: 'props',
        width: 120,
        height: 116,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: itemPhotographs,
        path: 'assets/images/props/narrative/NARRATIVE-PROPS-FURNITURE06.png',
        type: AssetType.item,
        category: 'props',
        width: 110,
        height: 121,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: itemInvestigationDocuments,
        path: 'assets/images/props/narrative/NARRATIVE-PROPS-FURNITURE07.png',
        type: AssetType.item,
        category: 'props',
        width: 94,
        height: 143,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: itemInvestigationBoard,
        path: 'assets/images/props/narrative/NARRATIVE-PROPS-FURNITURE08.png',
        type: AssetType.prop,
        category: 'props',
        width: 120,
        height: 151,
        isInteractable: true,
      ),
      const AssetEntry(
        assetId: itemCountdownDevice,
        path: 'assets/images/props/narrative/NARRATIVE-PROPS-FURNITURE09.png',
        type: AssetType.item,
        category: 'props',
        width: 140,
        height: 149,
        isInteractable: true,
      ),

      // Nature
      const AssetEntry(
        assetId: villagePineTree,
        path: 'assets/images/nature/NATURE-GAMEPLAY-STRUCTURES02.png',
        type: AssetType.prop,
        category: 'nature',
        width: 106,
        height: 180,
      ),
      const AssetEntry(
        assetId: villageDeadTree,
        path: 'assets/images/nature/NATURE-GAMEPLAY-STRUCTURES06.png',
        type: AssetType.prop,
        category: 'nature',
        width: 96,
        height: 176,
      ),
      const AssetEntry(
        assetId: villageStoneSlab,
        path: 'assets/images/nature/NATURE-GAMEPLAY-STRUCTURES04.png',
        type: AssetType.tile,
        category: 'nature',
        width: 103,
        height: 95,
      ),
      const AssetEntry(
        assetId: villageStoneSlabVar,
        path: 'assets/images/nature/NATURE-GAMEPLAY-STRUCTURES07.png',
        type: AssetType.tile,
        category: 'nature',
        width: 92,
        height: 79,
      ),
      const AssetEntry(
        assetId: villageSnowSlab,
        path: 'assets/images/nature/NATURE-GAMEPLAY-STRUCTURES08.png',
        type: AssetType.tile,
        category: 'nature',
        width: 66,
        height: 65,
      ),
      const AssetEntry(
        assetId: villageIceSlab,
        path: 'assets/images/nature/NATURE-GAMEPLAY-STRUCTURES10.png',
        type: AssetType.tile,
        category: 'nature',
        width: 93,
        height: 102,
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
