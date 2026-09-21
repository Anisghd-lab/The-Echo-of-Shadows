import 'dart:math' as math;

/// Point of Interest in the Village World ready for narrative interactions.
class PointOfInterest {
  final String id;
  final String nameEn;
  final String nameFr;
  final double worldX;
  final double worldY;
  final double triggerRadius;
  final String? defaultInteractionPrompt;

  const PointOfInterest({
    required this.id,
    required this.nameEn,
    required this.nameFr,
    required this.worldX,
    required this.worldY,
    this.triggerRadius = 1.6,
    this.defaultInteractionPrompt,
  });

  bool isNear(double playerX, double playerY) {
    final dx = playerX - worldX;
    final dy = playerY - worldY;
    return (dx * dx + dy * dy) <= (triggerRadius * triggerRadius);
  }

  double distanceTo(double playerX, double playerY) {
    final dx = playerX - worldX;
    final dy = playerY - worldY;
    return math.sqrt(dx * dx + dy * dy);
  }
}

/// Canonical POI registry for Phase 3
class VillagePOIRegistry {
  static const String villageEntrance = 'VILLAGE_ENTRANCE';
  static const String villageSquare = 'VILLAGE_SQUARE';
  static const String oldWell = 'OLD_WELL';
  static const String abandonedChurch = 'ABANDONED_CHURCH';
  static const String familyHouse = 'FAMILY_HOUSE';
  static const String abandonedHouse01 = 'ABANDONED_HOUSE_01';
  static const String abandonedHouse02 = 'ABANDONED_HOUSE_02';

  static final List<PointOfInterest> allPOIs = [
    const PointOfInterest(
      id: villageEntrance,
      nameEn: 'Village Entrance (Bridge)',
      nameFr: 'Entrée du village (Pont)',
      worldX: 0.0,
      worldY: 0.0,
      triggerRadius: 1.8,
      defaultInteractionPrompt: 'Inspect the snowy bridge',
    ),
    const PointOfInterest(
      id: villageSquare,
      nameEn: 'Central Square',
      nameFr: 'Place centrale',
      worldX: 0.0,
      worldY: 5.5,
      triggerRadius: 2.2,
      defaultInteractionPrompt: 'Examine central plaza',
    ),
    const PointOfInterest(
      id: oldWell,
      nameEn: 'Ancient Stone Well',
      nameFr: 'Puits en pierre',
      worldX: 0.0,
      worldY: 6.0,
      triggerRadius: 1.5,
      defaultInteractionPrompt: 'Look into the frozen well',
    ),
    const PointOfInterest(
      id: abandonedChurch,
      nameEn: 'St. Jude Abandoned Church',
      nameFr: 'Église abandonnée St-Jude',
      worldX: 6.5,
      worldY: 5.0,
      triggerRadius: 2.4,
      defaultInteractionPrompt: 'Examine church doors',
    ),
    const PointOfInterest(
      id: familyHouse,
      nameEn: 'Alex Family House',
      nameFr: 'Maison familiale',
      worldX: 0.0,
      worldY: 10.5,
      triggerRadius: 2.0,
      defaultInteractionPrompt: 'Enter family house',
    ),
    const PointOfInterest(
      id: abandonedHouse01,
      nameEn: 'Dilapidated Cottage',
      nameFr: 'Cottage délabré',
      worldX: -5.5,
      worldY: 4.5,
      triggerRadius: 1.8,
      defaultInteractionPrompt: 'Inspect wooden porch',
    ),
    const PointOfInterest(
      id: abandonedHouse02,
      nameEn: 'Forester Shack',
      nameFr: 'Cabane du garde',
      worldX: -5.5,
      worldY: 8.5,
      triggerRadius: 1.8,
      defaultInteractionPrompt: 'Examine shuttered window',
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
