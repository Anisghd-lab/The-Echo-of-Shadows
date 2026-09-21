import 'dart:math' as math;
import 'isometric_coordinates.dart';

/// Point of Interest in the Village World ready for narrative interactions.
class PointOfInterest {
  final String id;
  final String nameEn;
  final String nameFr;
  final double worldX;
  final double worldY;
  final double triggerRadius;
  final String? defaultInteractionPrompt;
  final int narrativeAct;
  final String storyFlag;

  const PointOfInterest({
    required this.id,
    required this.nameEn,
    required this.nameFr,
    required this.worldX,
    required this.worldY,
    this.triggerRadius = 1.8,
    this.defaultInteractionPrompt,
    this.narrativeAct = 1,
    this.storyFlag = '',
  });

  bool isNear(double playerX, double playerY) {
    final scale = IsometricCoordinates.worldScale;
    final dx = playerX - (worldX * scale);
    final dy = playerY - (worldY * scale);
    final r = triggerRadius * scale;
    return (dx * dx + dy * dy) <= (r * r);
  }

  double distanceTo(double playerX, double playerY) {
    final scale = IsometricCoordinates.worldScale;
    final dx = playerX - (worldX * scale);
    final dy = playerY - (worldY * scale);
    return math.sqrt(dx * dx + dy * dy);
  }
}

/// Canonical POI registry reconstructed from Map village .png.
class VillagePOIRegistry {
  // Legacy aliases for backward compatibility
  static const String villageEntrance = 'POI_BRIDGE';
  static const String villageSquare = 'POI_PLAZA_MONUMENT';
  static const String oldWell = 'POI_ANCIENT_WELL';
  static const String abandonedChurch = 'POI_CHURCH';
  static const String familyHouse = 'POI_FAMILY_HOUSE';
  static const String abandonedHouse01 = 'POI_COTTAGE_WEST';
  static const String abandonedHouse02 = 'POI_COTTAGE_SOUTH';

  // Canonical Map POI IDs
  static const String poiBridge = 'POI_BRIDGE';
  static const String poiPlaza = 'POI_PLAZA_MONUMENT';
  static const String poiWell = 'POI_ANCIENT_WELL';
  static const String poiShrine = 'POI_PLAZA_SHRINE';
  static const String poiFamilyHouse = 'POI_FAMILY_HOUSE';
  static const String poiChurch = 'POI_CHURCH';
  static const String poiCemetery = 'POI_CEMETERY';
  static const String poiMarketplace = 'POI_MARKETPLACE';
  static const String poiSawmill = 'POI_SAWMILL';
  static const String poiWatermill = 'POI_WATERMILL';
  static const String poiWindmill = 'POI_WINDMILL';
  static const String poiFarm = 'POI_FARM';
  static const String poiMineEntrance = 'POI_MINE_ENTRANCE';
  static const String poiBoatDock = 'POI_BOAT_DOCK';
  static const String poiCargoDock = 'POI_CARGO_DOCK';
  static const String poiRiversideCottage = 'POI_RIVERSIDE_COTTAGE';
  static const String poiCottageWest = 'POI_COTTAGE_WEST';
  static const String poiCottageSouth = 'POI_COTTAGE_SOUTH';
  static const String poiCottageFarWest = 'POI_COTTAGE_FAR_WEST';
  static const String poiCraftsman = 'POI_CRAFTSMAN_HOUSE';

  static final List<PointOfInterest> allPOIs = [
    // 1. South River Approach & Bridge
    const PointOfInterest(
      id: poiBridge,
      nameEn: 'Snowy Wooden Bridge (Village Entrance)',
      nameFr: 'Pont de bois enneigé (Entrée du village)',
      worldX: 6.5,
      worldY: 6.5,
      triggerRadius: 2.0,
      defaultInteractionPrompt: 'Inspect the snowy bridge',
      narrativeAct: 1,
      storyFlag: 'BRIDGE_CROSSED',
    ),
    const PointOfInterest(
      id: poiBoatDock,
      nameEn: 'Moored Rowboat Pier',
      nameFr: 'Embarcadère et barque amarrée',
      worldX: 2.0,
      worldY: 8.5,
      triggerRadius: 1.8,
      defaultInteractionPrompt: 'Examine the frozen rowboat',
      narrativeAct: 1,
      storyFlag: 'BOAT_INSPECTED',
    ),
    const PointOfInterest(
      id: poiCargoDock,
      nameEn: 'River Cargo Pier',
      nameFr: 'Quai de déchargement de la rivière',
      worldX: 6.0,
      worldY: 6.0,
      triggerRadius: 1.8,
      defaultInteractionPrompt: 'Search cargo crates',
      narrativeAct: 1,
      storyFlag: 'DOCK_CRATES_INSPECTED',
    ),
    const PointOfInterest(
      id: poiRiversideCottage,
      nameEn: 'River Guard Cottage',
      nameFr: 'Poste de garde de la rivière',
      worldX: 5.5,
      worldY: 3.0,
      triggerRadius: 2.0,
      defaultInteractionPrompt: 'Look through lit shuttered window',
      narrativeAct: 1,
      storyFlag: 'RIVERSIDE_HOUSE_CHECKED',
    ),

    // 2. Central Square & Well
    const PointOfInterest(
      id: poiPlaza,
      nameEn: 'Founders Monument (Central Square)',
      nameFr: 'Monument aux Fondateurs (Place centrale)',
      worldX: 0.0,
      worldY: 0.0,
      triggerRadius: 2.2,
      defaultInteractionPrompt: 'Examine central plaza monument',
      narrativeAct: 1,
      storyFlag: 'PLAZA_DISCOVERED',
    ),
    const PointOfInterest(
      id: poiWell,
      nameEn: 'Ancient Stone Well',
      nameFr: 'Puits en pierre gelé',
      worldX: 1.2,
      worldY: 2.4,
      triggerRadius: 1.6,
      defaultInteractionPrompt: 'Look into the dark frozen well',
      narrativeAct: 1,
      storyFlag: 'WELL_INSPECTED',
    ),
    const PointOfInterest(
      id: poiShrine,
      nameEn: 'Village Wooden Shrine',
      nameFr: 'Oratoire en bois de la place',
      worldX: -1.2,
      worldY: -1.8,
      triggerRadius: 1.5,
      defaultInteractionPrompt: 'Inspect wooden votive plaque',
      narrativeAct: 1,
      storyFlag: 'SHRINE_INSPECTED',
    ),

    // 3. North & Residential (Family House)
    const PointOfInterest(
      id: poiFamilyHouse,
      nameEn: 'Miller Family House (Childhood Home)',
      nameFr: 'Maison familiale des Miller (Demeure d\'enfance)',
      worldX: -1.5,
      worldY: -5.0,
      triggerRadius: 2.2,
      defaultInteractionPrompt: 'Try front door of family house',
      narrativeAct: 1,
      storyFlag: 'FAMILY_HOUSE_REACHED',
    ),

    // 4. Church Hill & Cemetery
    const PointOfInterest(
      id: poiChurch,
      nameEn: 'St. Jude Abandoned Church',
      nameFr: 'Église abandonnée St-Jude',
      worldX: 3.5,
      worldY: -7.5,
      triggerRadius: 2.5,
      defaultInteractionPrompt: 'Examine heavy oak church doors',
      narrativeAct: 2,
      storyFlag: 'CHURCH_REACHED',
    ),
    const PointOfInterest(
      id: poiCemetery,
      nameEn: 'Parish Cemetery & Graves',
      nameFr: 'Cimetière paroissial & Sépultures',
      worldX: 1.2,
      worldY: -4.5,
      triggerRadius: 2.0,
      defaultInteractionPrompt: 'Search snow-covered tombstones',
      narrativeAct: 2,
      storyFlag: 'CEMETERY_SEARCHED',
    ),

    // 5. Southeast Market & Sawmill
    const PointOfInterest(
      id: poiMarketplace,
      nameEn: 'Abandoned Marketplace',
      nameFr: 'Place du marché abandonnée',
      worldX: 4.5,
      worldY: -0.5,
      triggerRadius: 2.0,
      defaultInteractionPrompt: 'Search abandoned vendor stalls',
      narrativeAct: 2,
      storyFlag: 'MARKET_INSPECTED',
    ),
    const PointOfInterest(
      id: poiCraftsman,
      nameEn: 'Market Craftsman Workshop',
      nameFr: 'Atelier d\'artisan du marché',
      worldX: 6.0,
      worldY: -1.5,
      triggerRadius: 2.0,
      defaultInteractionPrompt: 'Knock on workshop shutter',
      narrativeAct: 2,
      storyFlag: 'WORKSHOP_CHECKED',
    ),
    const PointOfInterest(
      id: poiSawmill,
      nameEn: 'Timber Sawmill & Hoist',
      nameFr: 'Scierie et grue de levage',
      worldX: 8.5,
      worldY: -1.0,
      triggerRadius: 2.2,
      defaultInteractionPrompt: 'Inspect timber logs & sawmill logbook',
      narrativeAct: 2,
      storyFlag: 'SAWMILL_INSPECTED',
    ),

    // 6. West Residential & Farm
    const PointOfInterest(
      id: poiCottageSouth,
      nameEn: 'Fisherman Cottage',
      nameFr: 'Maisonnette du pêcheur',
      worldX: -2.2,
      worldY: 1.8,
      triggerRadius: 2.0,
      defaultInteractionPrompt: 'Examine nets hanging on porch',
      narrativeAct: 1,
      storyFlag: 'FISHERMAN_CHECKED',
    ),
    const PointOfInterest(
      id: poiCottageWest,
      nameEn: 'Blacksmith House',
      nameFr: 'Maison du forgeron',
      worldX: -4.0,
      worldY: -0.5,
      triggerRadius: 2.0,
      defaultInteractionPrompt: 'Check the cold forge entrance',
      narrativeAct: 2,
      storyFlag: 'FORGE_CHECKED',
    ),
    const PointOfInterest(
      id: poiCottageFarWest,
      nameEn: 'Forester Cottage',
      nameFr: 'Chalet forestier de l\'ouest',
      worldX: -5.5,
      worldY: 2.0,
      triggerRadius: 2.0,
      defaultInteractionPrompt: 'Inspect wooden door carvings',
      narrativeAct: 2,
      storyFlag: 'FORESTER_CHECKED',
    ),
    const PointOfInterest(
      id: poiFarm,
      nameEn: 'Frozen Farm Crops',
      nameFr: 'Champs gelés de la ferme',
      worldX: -5.5,
      worldY: -3.5,
      triggerRadius: 2.0,
      defaultInteractionPrompt: 'Inspect buried tool shed',
      narrativeAct: 2,
      storyFlag: 'FARM_INSPECTED',
    ),
    const PointOfInterest(
      id: poiWindmill,
      nameEn: 'West Ridge Windmill',
      nameFr: 'Moulin à vent de la crête ouest',
      worldX: -8.5,
      worldY: -2.0,
      triggerRadius: 2.2,
      defaultInteractionPrompt: 'Examine locked mechanism & viewpoint',
      narrativeAct: 2,
      storyFlag: 'WINDMILL_INSPECTED',
    ),

    // 7. Mountain Mine & Watermill
    const PointOfInterest(
      id: poiWatermill,
      nameEn: 'Old Cliffside Watermill',
      nameFr: 'Vieux Moulin à eau de la falaise',
      worldX: -2.5,
      worldY: 8.5,
      triggerRadius: 2.2,
      defaultInteractionPrompt: 'Inspect frozen mill wheel & lower door',
      narrativeAct: 3,
      storyFlag: 'WATERMILL_INSPECTED',
    ),
    const PointOfInterest(
      id: poiMineEntrance,
      nameEn: 'Old Rock Mine Archway (Forest Pass)',
      nameFr: 'Porche de l\'ancienne mine (Passage nord)',
      worldX: -7.5,
      worldY: -7.5,
      triggerRadius: 2.4,
      defaultInteractionPrompt: 'Inspect dark tunnel entrance',
      narrativeAct: 3,
      storyFlag: 'MINE_ENTRANCE_FOUND',
    ),
  ];

  /// Finds closest active POI near player if within radius.
  static PointOfInterest? findActivePOI(double playerX, double playerY) {
    PointOfInterest? closest;
    double minDistance = double.infinity;

    for (final poi in allPOIs) {
      if (poi.isNear(playerX, playerY)) {
        final dist = poi.distanceTo(playerX, playerY);
        if (dist < minDistance) {
          minDistance = dist;
          closest = poi;
        }
      }
    }
    return closest;
  }
}
