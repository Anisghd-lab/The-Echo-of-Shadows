import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;
import 'isometric_coordinates.dart';

/// Representation of a terrain/environmental zone in the village blueprint.
class MapZone {
  final String id;
  final String nameFr;
  final String nameEn;
  final String type;
  final bool navigable;
  final Map<String, dynamic> bounds;

  const MapZone({
    required this.id,
    required this.nameFr,
    required this.nameEn,
    required this.type,
    this.navigable = true,
    this.bounds = const {},
  });

  factory MapZone.fromJson(Map<String, dynamic> json) {
    return MapZone(
      id: json['id'] as String,
      nameFr: json['name_fr'] as String? ?? '',
      nameEn: json['name_en'] as String? ?? '',
      type: json['type'] as String? ?? 'ground',
      navigable: json['navigable'] as bool? ?? true,
      bounds: (json['bounds'] as Map<String, dynamic>?) ?? {},
    );
  }
}

/// Representation of a building reconstructed from Map village .png.
class MapBuilding {
  final String id;
  final String nameFr;
  final String nameEn;
  final String assetId;
  final String blueprintFeature;
  final double worldX;
  final double worldY;
  final double displayWidth;
  final double displayHeight;
  final double collisionHalfWidth;
  final double collisionHalfHeight;
  final double collisionOffsetY;
  final String poiId;
  final int narrativeAct;

  const MapBuilding({
    required this.id,
    required this.nameFr,
    required this.nameEn,
    required this.assetId,
    required this.blueprintFeature,
    required this.worldX,
    required this.worldY,
    required this.displayWidth,
    required this.displayHeight,
    required this.collisionHalfWidth,
    required this.collisionHalfHeight,
    this.collisionOffsetY = 0.0,
    required this.poiId,
    this.narrativeAct = 1,
  });

  factory MapBuilding.fromJson(Map<String, dynamic> json) {
    final col = (json['collision'] as Map<String, dynamic>?) ?? {};
    return MapBuilding(
      id: json['id'] as String,
      nameFr: json['name_fr'] as String? ?? '',
      nameEn: json['name_en'] as String? ?? '',
      assetId: json['asset_id'] as String,
      blueprintFeature: json['blueprint_feature'] as String? ?? '',
      worldX: (json['world_x'] as num).toDouble(),
      worldY: (json['world_y'] as num).toDouble(),
      displayWidth: (json['display_width'] as num).toDouble(),
      displayHeight: (json['display_height'] as num).toDouble(),
      collisionHalfWidth: (col['half_width'] as num?)?.toDouble() ?? 1.2,
      collisionHalfHeight: (col['half_height'] as num?)?.toDouble() ?? 1.0,
      collisionOffsetY: (col['offset_y'] as num?)?.toDouble() ?? 0.0,
      poiId: json['poi_id'] as String? ?? '',
      narrativeAct: (json['narrative_act'] as num?)?.toInt() ?? 1,
    );
  }
}

/// Representation of an environmental prop placed in the village world.
class MapProp {
  final String id;
  final String nameFr;
  final String nameEn;
  final String assetId;
  final double worldX;
  final double worldY;
  final double displayWidth;
  final double displayHeight;
  final double collisionHalfWidth;
  final double collisionHalfHeight;
  final bool hasCollision;
  final String poiId;

  const MapProp({
    required this.id,
    required this.nameFr,
    required this.nameEn,
    required this.assetId,
    required this.worldX,
    required this.worldY,
    required this.displayWidth,
    required this.displayHeight,
    this.collisionHalfWidth = 0.5,
    this.collisionHalfHeight = 0.5,
    this.hasCollision = true,
    this.poiId = '',
  });

  factory MapProp.fromJson(Map<String, dynamic> json) {
    final col = (json['collision'] as Map<String, dynamic>?) ?? {};
    return MapProp(
      id: json['id'] as String,
      nameFr: json['name_fr'] as String? ?? '',
      nameEn: json['name_en'] as String? ?? '',
      assetId: json['asset_id'] as String,
      worldX: (json['world_x'] as num).toDouble(),
      worldY: (json['world_y'] as num).toDouble(),
      displayWidth: (json['display_width'] as num).toDouble(),
      displayHeight: (json['display_height'] as num).toDouble(),
      collisionHalfWidth: (col['half_width'] as num?)?.toDouble() ?? 0.5,
      collisionHalfHeight: (col['half_height'] as num?)?.toDouble() ?? 0.5,
      hasCollision: col.isNotEmpty,
      poiId: json['poi_id'] as String? ?? '',
    );
  }
}

/// A street lantern post illuminating the roads and plaza.
class MapStreetLamp {
  final String id;
  final double worldX;
  final double worldY;

  const MapStreetLamp({
    required this.id,
    required this.worldX,
    required this.worldY,
  });

  factory MapStreetLamp.fromJson(Map<String, dynamic> json) {
    return MapStreetLamp(
      id: json['id'] as String,
      worldX: (json['world_x'] as num).toDouble(),
      worldY: (json['world_y'] as num).toDouble(),
    );
  }
}

/// Point of Interest in the data-driven map.
class MapPOI {
  final String id;
  final String nameFr;
  final String nameEn;
  final double worldX;
  final double worldY;
  final double triggerRadius;
  final String promptFr;
  final String promptEn;
  final int narrativeAct;
  final String storyFlag;

  const MapPOI({
    required this.id,
    required this.nameFr,
    required this.nameEn,
    required this.worldX,
    required this.worldY,
    this.triggerRadius = 1.8,
    required this.promptFr,
    required this.promptEn,
    this.narrativeAct = 1,
    this.storyFlag = '',
  });

  factory MapPOI.fromJson(Map<String, dynamic> json) {
    return MapPOI(
      id: json['id'] as String,
      nameFr: json['name_fr'] as String? ?? '',
      nameEn: json['name_en'] as String? ?? '',
      worldX: (json['world_x'] as num).toDouble(),
      worldY: (json['world_y'] as num).toDouble(),
      triggerRadius: (json['trigger_radius'] as num?)?.toDouble() ?? 1.8,
      promptFr: json['interaction_prompt_fr'] as String? ?? '',
      promptEn: json['interaction_prompt_en'] as String? ?? '',
      narrativeAct: (json['narrative_act'] as num?)?.toInt() ?? 1,
      storyFlag: json['story_flag'] as String? ?? '',
    );
  }
}

/// NPC definition from the village blueprint.
class MapNPC {
  final String id;
  final String name;
  final String role;
  final bool isPlayable;
  final double initialWorldX;
  final double initialWorldY;
  final String initialOrientation;
  final double speedWalk;
  final double speedRun;
  final List<int> activeActs;
  final double patrolRadius;
  final bool isEchoApparition;
  final String dialogueKey;
  final String narrativeCondition;

  const MapNPC({
    required this.id,
    required this.name,
    required this.role,
    this.isPlayable = false,
    required this.initialWorldX,
    required this.initialWorldY,
    this.initialOrientation = 'SE',
    this.speedWalk = 2.4,
    this.speedRun = 4.8,
    this.activeActs = const [1],
    this.patrolRadius = 1.0,
    this.isEchoApparition = false,
    this.dialogueKey = '',
    this.narrativeCondition = '',
  });

  factory MapNPC.fromJson(Map<String, dynamic> json) {
    final acts = (json['active_acts'] as List<dynamic>?)?.map((e) => (e as num).toInt()).toList() ?? [1];
    return MapNPC(
      id: json['id'] as String,
      name: json['name'] as String? ?? '',
      role: json['role'] as String? ?? '',
      isPlayable: json['is_playable'] as bool? ?? false,
      initialWorldX: (json['initial_world_x'] as num).toDouble(),
      initialWorldY: (json['initial_world_y'] as num).toDouble(),
      initialOrientation: json['initial_orientation'] as String? ?? 'SE',
      speedWalk: (json['speed_walk'] as num?)?.toDouble() ?? 2.4,
      speedRun: (json['speed_run'] as num?)?.toDouble() ?? 4.8,
      activeActs: acts,
      patrolRadius: (json['patrol_radius'] as num?)?.toDouble() ?? 1.0,
      isEchoApparition: json['is_echo_apparition'] as bool? ?? false,
      dialogueKey: json['dialogue_key'] as String? ?? '',
      narrativeCondition: json['narrative_condition'] as String? ?? '',
    );
  }
}

/// Initial player spawn configuration.
class PlayerSpawnPoint {
  final double worldX;
  final double worldY;
  final String orientation;
  final String locationNameFr;
  final String locationNameEn;

  const PlayerSpawnPoint({
    required this.worldX,
    required this.worldY,
    this.orientation = 'NW',
    required this.locationNameFr,
    required this.locationNameEn,
  });

  factory PlayerSpawnPoint.fromJson(Map<String, dynamic> json) {
    return PlayerSpawnPoint(
      worldX: (json['world_x'] as num).toDouble(),
      worldY: (json['world_y'] as num).toDouble(),
      orientation: json['orientation'] as String? ?? 'NW',
      locationNameFr: json['location_name_fr'] as String? ?? '',
      locationNameEn: json['location_name_en'] as String? ?? '',
    );
  }
}

/// World bounds.
class MapBounds {
  final double minWorldX;
  final double maxWorldX;
  final double minWorldY;
  final double maxWorldY;

  const MapBounds({
    required this.minWorldX,
    required this.maxWorldX,
    required this.minWorldY,
    required this.maxWorldY,
  });

  factory MapBounds.fromJson(Map<String, dynamic> json) {
    return MapBounds(
      minWorldX: (json['min_world_x'] as num).toDouble(),
      maxWorldX: (json['max_world_x'] as num).toDouble(),
      minWorldY: (json['min_world_y'] as num).toDouble(),
      maxWorldY: (json['max_world_y'] as num).toDouble(),
    );
  }
}

/// Canonical Village Map blueprint loader and model.
class VillageMap {
  final String mapId;
  final String titleFr;
  final String titleEn;
  final String referenceBlueprint;
  final PlayerSpawnPoint playerSpawn;
  final MapBounds bounds;
  final List<MapZone> zones;
  final List<MapBuilding> buildings;
  final List<MapProp> props;
  final List<MapStreetLamp> streetLamps;
  final List<MapPOI> pois;
  final List<MapNPC> npcs;

  const VillageMap({
    required this.mapId,
    required this.titleFr,
    required this.titleEn,
    required this.referenceBlueprint,
    required this.playerSpawn,
    required this.bounds,
    required this.zones,
    required this.buildings,
    required this.props,
    required this.streetLamps,
    required this.pois,
    required this.npcs,
  });

  factory VillageMap.fromJson(Map<String, dynamic> json) {
    final coordSys = (json['coordinate_system'] as Map<String, dynamic>?) ?? {};
    final bData = (coordSys['bounds'] as Map<String, dynamic>?) ?? {};
    final spawnData = (json['player_spawn'] as Map<String, dynamic>?) ?? {};

    return VillageMap(
      mapId: json['map_id'] as String? ?? 'village_abandonne',
      titleFr: json['title_fr'] as String? ?? '',
      titleEn: json['title_en'] as String? ?? '',
      referenceBlueprint: json['reference_blueprint'] as String? ?? '',
      playerSpawn: PlayerSpawnPoint.fromJson(spawnData),
      bounds: MapBounds.fromJson(bData),
      zones: ((json['zones'] as List<dynamic>?) ?? [])
          .map((z) => MapZone.fromJson(z as Map<String, dynamic>))
          .toList(),
      buildings: ((json['buildings'] as List<dynamic>?) ?? [])
          .map((b) => MapBuilding.fromJson(b as Map<String, dynamic>))
          .toList(),
      props: ((json['props'] as List<dynamic>?) ?? [])
          .map((p) => MapProp.fromJson(p as Map<String, dynamic>))
          .toList(),
      streetLamps: ((json['street_lamps'] as List<dynamic>?) ?? [])
          .map((l) => MapStreetLamp.fromJson(l as Map<String, dynamic>))
          .toList(),
      pois: ((json['pois'] as List<dynamic>?) ?? [])
          .map((p) => MapPOI.fromJson(p as Map<String, dynamic>))
          .toList(),
      npcs: ((json['npcs'] as List<dynamic>?) ?? [])
          .map((n) => MapNPC.fromJson(n as Map<String, dynamic>))
          .toList(),
    );
  }

  /// Canonical hardcoded fallback representing the validated Map village .png reconstruction.
  /// Guarantees that unit tests and offline Flutter execution run with zero I/O dependencies.
  static VillageMap canonical() {
    return const VillageMap(
      mapId: 'village_abandonne',
      titleFr: 'Le Village Abandonné',
      titleEn: 'The Abandoned Village',
      referenceBlueprint: 'new assets/map du village.png',
      playerSpawn: PlayerSpawnPoint(
        worldX: 7.0,
        worldY: 8.0,
        orientation: 'NW',
        locationNameFr: 'Pont d\'entrée du village',
        locationNameEn: 'Village Entrance Bridge',
      ),
      bounds: MapBounds(
        minWorldX: -11.0,
        maxWorldX: 11.0,
        minWorldY: -12.0,
        maxWorldY: 12.0,
      ),
      zones: [
        MapZone(id: 'ZONE_FROZEN_RIVER', nameFr: 'Rivière gelée', nameEn: 'Frozen River', type: 'water_ice', navigable: false),
        MapZone(id: 'ZONE_BRIDGE_APPROACH', nameFr: 'Pont de bois', nameEn: 'Wooden Bridge', type: 'wooden_bridge'),
        MapZone(id: 'ZONE_MAIN_AVENUE', nameFr: 'Avenue principale', nameEn: 'Main South Avenue', type: 'cobblestone_road'),
        MapZone(id: 'ZONE_CENTRAL_PLAZA', nameFr: 'Place centrale', nameEn: 'Central Monument Plaza', type: 'paved_circular_plaza'),
        MapZone(id: 'ZONE_CHURCH_HILL', nameFr: 'Colline de l\'Église', nameEn: 'St. Jude Church Hill', type: 'stone_path'),
        MapZone(id: 'ZONE_CEMETERY', nameFr: 'Cimetière', nameEn: 'Parish Cemetery', type: 'hallowed_ground'),
        MapZone(id: 'ZONE_MARKETPLACE', nameFr: 'Place du Marché', nameEn: 'Marketplace', type: 'cobblestone_market'),
        MapZone(id: 'ZONE_SAWMILL', nameFr: 'Scierie', nameEn: 'Sawmill', type: 'timber_yard'),
        MapZone(id: 'ZONE_FARM_FIELD', nameFr: 'Champs de la ferme', nameEn: 'Farm Crops', type: 'frozen_farmland'),
        MapZone(id: 'ZONE_WINDMILL_RIDGE', nameFr: 'Crête du Moulin', nameEn: 'Windmill Ridge', type: 'rocky_ridge'),
        MapZone(id: 'ZONE_WATERMILL', nameFr: 'Rive du Moulin à eau', nameEn: 'Watermill Shore', type: 'rocky_shore'),
        MapZone(id: 'ZONE_MINE_PASS', nameFr: 'Défilé de la Mine', nameEn: 'Mine Mountain Pass', type: 'mountain_pass'),
      ],
      buildings: [
        MapBuilding(
          id: 'BUILDING_CHURCH',
          nameFr: 'Église abandonnée St-Jude',
          nameEn: 'St. Jude Abandoned Church',
          assetId: 'village_environment_104',
          blueprintFeature: 'CHURCH_ST_JUDE',
          worldX: 3.5,
          worldY: -7.5,
          displayWidth: 280,
          displayHeight: 370,
          collisionHalfWidth: 1.6,
          collisionHalfHeight: 1.4,
          collisionOffsetY: -0.2,
          poiId: 'POI_CHURCH',
          narrativeAct: 2,
        ),
        MapBuilding(
          id: 'BUILDING_FAMILY_HOUSE',
          nameFr: 'Maison familiale des Miller',
          nameEn: 'Miller Family House',
          assetId: 'maison_familiale_exterieure01',
          blueprintFeature: 'COTTAGE_NORTH',
          worldX: -1.5,
          worldY: -5.0,
          displayWidth: 320,
          displayHeight: 298,
          collisionHalfWidth: 1.6,
          collisionHalfHeight: 1.2,
          collisionOffsetY: -0.2,
          poiId: 'POI_FAMILY_HOUSE',
          narrativeAct: 1,
        ),
        MapBuilding(
          id: 'BUILDING_WATERMILL',
          nameFr: 'Vieux Moulin à eau',
          nameEn: 'Old Watermill',
          assetId: 'village_environment_101',
          blueprintFeature: 'WATERMILL',
          worldX: -2.5,
          worldY: 8.5,
          displayWidth: 260,
          displayHeight: 244,
          collisionHalfWidth: 1.4,
          collisionHalfHeight: 1.2,
          poiId: 'POI_WATERMILL',
          narrativeAct: 3,
        ),
        MapBuilding(
          id: 'BUILDING_WINDMILL',
          nameFr: 'Moulin à vent de la crête ouest',
          nameEn: 'West Ridge Windmill',
          assetId: 'village_environment_102',
          blueprintFeature: 'WINDMILL',
          worldX: -8.5,
          worldY: -2.0,
          displayWidth: 240,
          displayHeight: 270,
          collisionHalfWidth: 1.2,
          collisionHalfHeight: 1.2,
          poiId: 'POI_WINDMILL',
          narrativeAct: 2,
        ),
        MapBuilding(
          id: 'BUILDING_COTTAGE_WEST',
          nameFr: 'Maison du forgeron',
          nameEn: 'Blacksmith House',
          assetId: 'village_environment_101',
          blueprintFeature: 'COTTAGE_WEST',
          worldX: -4.0,
          worldY: -0.5,
          displayWidth: 220,
          displayHeight: 205,
          collisionHalfWidth: 1.2,
          collisionHalfHeight: 1.1,
          poiId: 'POI_COTTAGE_WEST',
          narrativeAct: 2,
        ),
        MapBuilding(
          id: 'BUILDING_COTTAGE_SOUTH',
          nameFr: 'Maisonnette du pêcheur',
          nameEn: 'Fisherman Cottage',
          assetId: 'village_environment_106',
          blueprintFeature: 'COTTAGE_SOUTH',
          worldX: -2.2,
          worldY: 1.8,
          displayWidth: 230,
          displayHeight: 180,
          collisionHalfWidth: 1.2,
          collisionHalfHeight: 1.1,
          poiId: 'POI_COTTAGE_SOUTH',
          narrativeAct: 1,
        ),
        MapBuilding(
          id: 'BUILDING_COTTAGE_FAR_WEST',
          nameFr: 'Chalet forestier de l\'ouest',
          nameEn: 'Forester Cottage',
          assetId: 'village_environment_101',
          blueprintFeature: 'COTTAGE_FAR_WEST',
          worldX: -5.5,
          worldY: 2.0,
          displayWidth: 210,
          displayHeight: 188,
          collisionHalfWidth: 1.1,
          collisionHalfHeight: 1.0,
          poiId: 'POI_COTTAGE_FAR_WEST',
          narrativeAct: 2,
        ),
        MapBuilding(
          id: 'BUILDING_RIVERSIDE_COTTAGE',
          nameFr: 'Poste de garde de la rivière',
          nameEn: 'Riverside Guardhouse',
          assetId: 'village_environment_101',
          blueprintFeature: 'RIVERSIDE_COTTAGE',
          worldX: 5.5,
          worldY: 3.0,
          displayWidth: 215,
          displayHeight: 190,
          collisionHalfWidth: 1.2,
          collisionHalfHeight: 1.1,
          poiId: 'POI_RIVERSIDE_COTTAGE',
          narrativeAct: 1,
        ),
        MapBuilding(
          id: 'BUILDING_EAST_WORKSHOP',
          nameFr: 'Atelier de l\'artisan',
          nameEn: 'Craftsman Workshop',
          assetId: 'village_environment_105',
          blueprintFeature: 'EAST_COTTAGES',
          worldX: 6.0,
          worldY: -1.5,
          displayWidth: 200,
          displayHeight: 180,
          collisionHalfWidth: 1.1,
          collisionHalfHeight: 1.0,
          poiId: 'POI_CRAFTSMAN_HOUSE',
          narrativeAct: 2,
        ),
        MapBuilding(
          id: 'BUILDING_SAWMILL',
          nameFr: 'Scierie et hangar',
          nameEn: 'Sawmill & Shed',
          assetId: 'village_environment_105',
          blueprintFeature: 'SAWMILL_LUMBER',
          worldX: 8.5,
          worldY: -1.0,
          displayWidth: 210,
          displayHeight: 195,
          collisionHalfWidth: 1.3,
          collisionHalfHeight: 1.2,
          poiId: 'POI_SAWMILL',
          narrativeAct: 2,
        ),
        MapBuilding(
          id: 'BUILDING_MINE_ARCHWAY',
          nameFr: 'Entrée de la mine de roche',
          nameEn: 'Rock Mine Entrance',
          assetId: 'village_environment_108',
          blueprintFeature: 'MINE_ENTRANCE',
          worldX: -7.5,
          worldY: -7.5,
          displayWidth: 170,
          displayHeight: 190,
          collisionHalfWidth: 1.2,
          collisionHalfHeight: 1.0,
          poiId: 'POI_MINE_ENTRANCE',
          narrativeAct: 3,
        ),
      ],
      props: [
        MapProp(
          id: 'PROP_STATUE_MONUMENT',
          nameFr: 'Statue du Fondateur',
          nameEn: 'Founder Statue',
          assetId: 'village_abandonne_route_decor_exterieur07',
          worldX: 0.0,
          worldY: 0.0,
          displayWidth: 90,
          displayHeight: 140,
          collisionHalfWidth: 0.6,
          collisionHalfHeight: 0.6,
          poiId: 'POI_PLAZA_MONUMENT',
        ),
        MapProp(
          id: 'PROP_ANCIENT_WELL',
          nameFr: 'Puits en pierre',
          nameEn: 'Stone Well',
          assetId: 'village_abandonne_route_decor_exterieur01',
          worldX: 1.2,
          worldY: 2.4,
          displayWidth: 100,
          displayHeight: 112,
          collisionHalfWidth: 0.7,
          collisionHalfHeight: 0.7,
          poiId: 'POI_ANCIENT_WELL',
        ),
        MapProp(
          id: 'PROP_PLAZA_SHRINE',
          nameFr: 'Oratoire en bois',
          nameEn: 'Wooden Shrine',
          assetId: 'village_environment_106',
          worldX: -1.2,
          worldY: -1.8,
          displayWidth: 80,
          displayHeight: 95,
          collisionHalfWidth: 0.5,
          collisionHalfHeight: 0.5,
          poiId: 'POI_PLAZA_SHRINE',
        ),
        MapProp(
          id: 'PROP_MARKET_STALL_01',
          nameFr: 'Étal de marché 01',
          nameEn: 'Market Stall 01',
          assetId: 'village_environment_116',
          worldX: 4.5,
          worldY: -0.5,
          displayWidth: 130,
          displayHeight: 115,
          collisionHalfWidth: 0.9,
          collisionHalfHeight: 0.6,
          poiId: 'POI_MARKETPLACE',
        ),
        MapProp(
          id: 'PROP_MARKET_STALL_02',
          nameFr: 'Étal de marché 02',
          nameEn: 'Market Stall 02',
          assetId: 'village_environment_121',
          worldX: 5.2,
          worldY: 0.4,
          displayWidth: 115,
          displayHeight: 105,
          collisionHalfWidth: 0.8,
          collisionHalfHeight: 0.5,
          poiId: 'POI_MARKETPLACE',
        ),
        MapProp(
          id: 'PROP_SAWMILL_CRANE',
          nameFr: 'Grue de la scierie',
          nameEn: 'Sawmill Crane',
          assetId: 'village_environment_129',
          worldX: 9.5,
          worldY: -1.8,
          displayWidth: 88,
          displayHeight: 139,
          collisionHalfWidth: 0.6,
          collisionHalfHeight: 0.6,
          poiId: 'POI_SAWMILL',
        ),
        MapProp(
          id: 'PROP_SAWMILL_LOGS',
          nameFr: 'Piles de grumes',
          nameEn: 'Timber Logs',
          assetId: 'village_environment_142',
          worldX: 8.0,
          worldY: 0.2,
          displayWidth: 103,
          displayHeight: 93,
          collisionHalfWidth: 0.8,
          collisionHalfHeight: 0.5,
          poiId: 'POI_SAWMILL',
        ),
        MapProp(
          id: 'PROP_CEMETERY_GATE',
          nameFr: 'Grille du cimetière',
          nameEn: 'Cemetery Gate',
          assetId: 'village_environment_113',
          worldX: 1.8,
          worldY: -3.2,
          displayWidth: 130,
          displayHeight: 85,
          collisionHalfWidth: 0.3,
          collisionHalfHeight: 0.8,
          poiId: 'POI_CEMETERY',
        ),
        MapProp(
          id: 'PROP_BOAT_ROWBOAT',
          nameFr: 'Barque amarrée',
          nameEn: 'Moored Rowboat',
          assetId: 'village_abandonne_route_decor_exterieur18',
          worldX: 2.0,
          worldY: 8.5,
          displayWidth: 90,
          displayHeight: 60,
          collisionHalfWidth: 0.6,
          collisionHalfHeight: 0.4,
          poiId: 'POI_BOAT_DOCK',
        ),
        MapProp(
          id: 'PROP_DOCK_CRANE',
          nameFr: 'Grue de quai',
          nameEn: 'Dock Hoist',
          assetId: 'village_environment_137',
          worldX: 6.0,
          worldY: 6.0,
          displayWidth: 80,
          displayHeight: 135,
          collisionHalfWidth: 0.5,
          collisionHalfHeight: 0.5,
          poiId: 'POI_CARGO_DOCK',
        ),
      ],
      streetLamps: [
        MapStreetLamp(id: 'LAMP_BRIDGE_TOP_L', worldX: 4.2, worldY: 4.8),
        MapStreetLamp(id: 'LAMP_BRIDGE_TOP_R', worldX: 4.8, worldY: 4.2),
        MapStreetLamp(id: 'LAMP_BRIDGE_BOT_L', worldX: 7.2, worldY: 7.8),
        MapStreetLamp(id: 'LAMP_BRIDGE_BOT_R', worldX: 7.8, worldY: 7.2),
        MapStreetLamp(id: 'LAMP_PLAZA_NW', worldX: -1.5, worldY: -0.8),
        MapStreetLamp(id: 'LAMP_PLAZA_NE', worldX: 0.8, worldY: -1.5),
        MapStreetLamp(id: 'LAMP_PLAZA_SW', worldX: -0.8, worldY: 1.5),
        MapStreetLamp(id: 'LAMP_PLAZA_SE', worldX: 1.5, worldY: 0.8),
        MapStreetLamp(id: 'LAMP_WELL', worldX: 1.8, worldY: 2.2),
        MapStreetLamp(id: 'LAMP_CHURCH_STEPS', worldX: 2.5, worldY: -4.2),
        MapStreetLamp(id: 'LAMP_MARKET_ENTRY', worldX: 3.8, worldY: -0.4),
        MapStreetLamp(id: 'LAMP_WEST_FORK', worldX: -1.8, worldY: 0.6),
        MapStreetLamp(id: 'LAMP_RIVERSIDE_HOUSE', worldX: 5.0, worldY: 2.6),
        MapStreetLamp(id: 'LAMP_FARM_ENTRY', worldX: -4.2, worldY: -2.2),
      ],
      pois: [
        MapPOI(
          id: 'POI_BRIDGE',
          nameFr: 'Pont de bois enneigé (Entrée du village)',
          nameEn: 'Snowy Wooden Bridge (Village Entrance)',
          worldX: 6.5,
          worldY: 6.5,
          triggerRadius: 2.0,
          promptFr: '[E] Traverser le pont de la rivière gelée',
          promptEn: '[E] Cross the frozen river bridge',
          narrativeAct: 1,
          storyFlag: 'BRIDGE_CROSSED',
        ),
        MapPOI(
          id: 'POI_PLAZA_MONUMENT',
          nameFr: 'Monument aux Fondateurs (Place centrale)',
          nameEn: 'Founders Monument (Central Square)',
          worldX: 0.0,
          worldY: 0.0,
          triggerRadius: 2.2,
          promptFr: '[E] Examiner la statue de pierre gravée',
          promptEn: '[E] Examine the engraved stone statue',
          narrativeAct: 1,
          storyFlag: 'PLAZA_DISCOVERED',
        ),
        MapPOI(
          id: 'POI_ANCIENT_WELL',
          nameFr: 'Puits en pierre gelé',
          nameEn: 'Ancient Stone Well',
          worldX: 1.2,
          worldY: 2.4,
          triggerRadius: 1.6,
          promptFr: '[E] Regarder dans le puits gelé et obscur',
          promptEn: '[E] Look into the dark frozen well',
          narrativeAct: 1,
          storyFlag: 'WELL_INSPECTED',
        ),
        MapPOI(
          id: 'POI_FAMILY_HOUSE',
          nameFr: 'Maison familiale des Miller',
          nameEn: 'Miller Family House',
          worldX: -1.5,
          worldY: -5.0,
          triggerRadius: 2.2,
          promptFr: '[E] Essayer la porte d\'entrée de la maison',
          promptEn: '[E] Try front door of family house',
          narrativeAct: 1,
          storyFlag: 'FAMILY_HOUSE_REACHED',
        ),
        MapPOI(
          id: 'POI_CHURCH',
          nameFr: 'Église abandonnée St-Jude',
          nameEn: 'St. Jude Abandoned Church',
          worldX: 3.5,
          worldY: -7.5,
          triggerRadius: 2.5,
          promptFr: '[E] Examiner les lourdes portes de chêne',
          promptEn: '[E] Examine heavy oak church doors',
          narrativeAct: 2,
          storyFlag: 'CHURCH_REACHED',
        ),
        MapPOI(
          id: 'POI_CEMETERY',
          nameFr: 'Cimetière paroissial & Sépultures',
          nameEn: 'Parish Cemetery & Graves',
          worldX: 1.2,
          worldY: -4.5,
          triggerRadius: 2.0,
          promptFr: '[E] Fouiller les tombes sous la neige',
          promptEn: '[E] Search snow-covered tombstones',
          narrativeAct: 2,
          storyFlag: 'CEMETERY_SEARCHED',
        ),
        MapPOI(
          id: 'POI_MARKETPLACE',
          nameFr: 'Place du marché abandonnée',
          nameEn: 'Abandoned Marketplace',
          worldX: 4.5,
          worldY: -0.5,
          triggerRadius: 2.0,
          promptFr: '[E] Fouiller les étals abandonnés',
          promptEn: '[E] Search abandoned vendor stalls',
          narrativeAct: 2,
          storyFlag: 'MARKET_INSPECTED',
        ),
        MapPOI(
          id: 'POI_SAWMILL',
          nameFr: 'Scierie et grue de levage',
          nameEn: 'Timber Sawmill & Hoist',
          worldX: 8.5,
          worldY: -1.0,
          triggerRadius: 2.2,
          promptFr: '[E] Examiner les grumes et le registre de coupe',
          promptEn: '[E] Inspect timber logs & sawmill logbook',
          narrativeAct: 2,
          storyFlag: 'SAWMILL_INSPECTED',
        ),
        MapPOI(
          id: 'POI_WATERMILL',
          nameFr: 'Vieux Moulin à eau de la falaise',
          nameEn: 'Old Cliffside Watermill',
          worldX: -2.5,
          worldY: 8.5,
          triggerRadius: 2.2,
          promptFr: '[E] Inspecter la roue gelée et la trappe basse',
          promptEn: '[E] Inspect frozen mill wheel & lower door',
          narrativeAct: 3,
          storyFlag: 'WATERMILL_INSPECTED',
        ),
        MapPOI(
          id: 'POI_WINDMILL',
          nameFr: 'Moulin à vent de la crête ouest',
          nameEn: 'West Ridge Windmill',
          worldX: -8.5,
          worldY: -2.0,
          triggerRadius: 2.2,
          promptFr: '[E] Examiner le mécanisme et le point de vue',
          promptEn: '[E] Examine locked mechanism & viewpoint',
          narrativeAct: 2,
          storyFlag: 'WINDMILL_INSPECTED',
        ),
        MapPOI(
          id: 'POI_FARM',
          nameFr: 'Champs gelés de la ferme',
          nameEn: 'Frozen Farm Crops',
          worldX: -5.5,
          worldY: -3.5,
          triggerRadius: 2.0,
          promptFr: '[E] Inspecter la remise à outils enneigée',
          promptEn: '[E] Inspect buried tool shed',
          narrativeAct: 2,
          storyFlag: 'FARM_INSPECTED',
        ),
        MapPOI(
          id: 'POI_MINE_ENTRANCE',
          nameFr: 'Porche de l\'ancienne mine (Passage nord)',
          nameEn: 'Old Rock Mine Archway (Forest Pass)',
          worldX: -7.5,
          worldY: -7.5,
          triggerRadius: 2.4,
          promptFr: '[E] Inspecter l\'entrée du tunnel obscur',
          promptEn: '[E] Inspect dark tunnel entrance',
          narrativeAct: 3,
          storyFlag: 'MINE_ENTRANCE_FOUND',
        ),
      ],
      npcs: [
        MapNPC(
          id: 'NPC_ALEX',
          name: 'Alex Miller',
          role: 'Protagonist',
          isPlayable: true,
          initialWorldX: 6.5,
          initialWorldY: 6.5,
          initialOrientation: 'NW',
        ),
        MapNPC(
          id: 'NPC_EMMA',
          name: 'Emma',
          role: 'Alex\'s Friend',
          initialWorldX: -1.0,
          initialWorldY: -2.5,
          initialOrientation: 'SE',
          dialogueKey: 'DLG_EMMA_ACT1',
          narrativeCondition: 'PLAZA_DISCOVERED',
        ),
        MapNPC(
          id: 'NPC_JAMES',
          name: 'James',
          role: 'Forester',
          initialWorldX: 7.0,
          initialWorldY: -0.5,
          initialOrientation: 'SW',
          dialogueKey: 'DLG_JAMES_ACT2',
          narrativeCondition: 'SAWMILL_INSPECTED',
        ),
        MapNPC(
          id: 'NPC_MICHAEL',
          name: 'Michael',
          role: 'Church Caretaker',
          initialWorldX: 2.5,
          initialWorldY: -4.5,
          initialOrientation: 'SE',
          dialogueKey: 'DLG_MICHAEL_ACT2',
          narrativeCondition: 'CHURCH_REACHED',
        ),
        MapNPC(
          id: 'NPC_DAVID',
          name: 'David',
          role: 'Merchant',
          initialWorldX: 4.0,
          initialWorldY: -0.2,
          initialOrientation: 'SW',
          dialogueKey: 'DLG_DAVID_ACT1',
          narrativeCondition: 'MARKET_INSPECTED',
        ),
        MapNPC(
          id: 'NPC_SARAH',
          name: 'Sarah',
          role: 'Resident',
          initialWorldX: -3.5,
          initialWorldY: 0.8,
          initialOrientation: 'NE',
          dialogueKey: 'DLG_SARAH_ACT2',
          narrativeCondition: 'WELL_INSPECTED',
        ),
        MapNPC(
          id: 'NPC_ETHAN',
          name: 'Ethan Miller',
          role: 'Missing Brother (Echo)',
          initialWorldX: 1.2,
          initialWorldY: 2.4,
          initialOrientation: 'NW',
          isEchoApparition: true,
          dialogueKey: 'DLG_ETHAN_ECHO_WELL',
          narrativeCondition: 'WELL_INSPECTED',
        ),
      ],
    );
  }

  /// Asynchronously loads map configuration from JSON asset bundle.
  static Future<VillageMap> loadFromAsset([String path = 'new assets/data/maps/village.json']) async {
    try {
      final jsonString = await rootBundle.loadString(path);
      final jsonMap = jsonDecode(jsonString) as Map<String, dynamic>;
      return VillageMap.fromJson(jsonMap);
    } catch (_) {
      return VillageMap.canonical();
    }
  }
}
