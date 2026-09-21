import 'dart:convert';

/// Representation of player coordinates and orientation in the isometric world.
class PlayerPositionModel {
  final double x;
  final double y;
  final String orientation; // 'SE', 'SW', 'NE', 'NW'

  const PlayerPositionModel({
    required this.x,
    required this.y,
    required this.orientation,
  });

  factory PlayerPositionModel.initial() {
    return const PlayerPositionModel(
      x: 0.0,
      y: 0.0,
      orientation: 'SE',
    );
  }

  PlayerPositionModel copyWith({
    double? x,
    double? y,
    String? orientation,
  }) {
    return PlayerPositionModel(
      x: x ?? this.x,
      y: y ?? this.y,
      orientation: orientation ?? this.orientation,
    );
  }

  Map<String, dynamic> toJson() => {
        'x': x,
        'y': y,
        'orientation': orientation,
      };

  factory PlayerPositionModel.fromJson(Map<String, dynamic> json) {
    return PlayerPositionModel(
      x: (json['x'] as num?)?.toDouble() ?? 0.0,
      y: (json['y'] as num?)?.toDouble() ?? 0.0,
      orientation: json['orientation'] as String? ?? 'SE',
    );
  }
}

/// Inventory item stored in local save.
class InventoryItemModel {
  final String id;
  final String nameId; // Localization ID (e.g., 'ITEM_OLD_KEY')
  final String type; // 'key', 'tape', 'document', 'tool'
  final bool usable;
  final bool isEvidence;
  final String? evidenceId;

  const InventoryItemModel({
    required this.id,
    required this.nameId,
    required this.type,
    this.usable = true,
    this.isEvidence = false,
    this.evidenceId,
  });

  Map<String, dynamic> toJson() => {
        'id': id,
        'nameId': nameId,
        'type': type,
        'usable': usable,
        'isEvidence': isEvidence,
        'evidenceId': evidenceId,
      };

  factory InventoryItemModel.fromJson(Map<String, dynamic> json) {
    return InventoryItemModel(
      id: json['id'] as String,
      nameId: json['nameId'] as String,
      type: json['type'] as String? ?? 'item',
      usable: json['usable'] as bool? ?? true,
      isEvidence: json['isEvidence'] as bool? ?? false,
      evidenceId: json['evidenceId'] as String?,
    );
  }
}

/// Evidence item recorded in Alex's journal.
class EvidenceItemModel {
  final String id; // e.g. 'EVIDENCE_2014_01'
  final String titleId;
  final String descriptionId;
  final String category; // '2014', 'ethan', 'bunker', 'village'
  final String discoveredAt;
  final String? assetRef;

  const EvidenceItemModel({
    required this.id,
    required this.titleId,
    required this.descriptionId,
    required this.category,
    required this.discoveredAt,
    this.assetRef,
  });

  Map<String, dynamic> toJson() => {
        'id': id,
        'titleId': titleId,
        'descriptionId': descriptionId,
        'category': category,
        'discoveredAt': discoveredAt,
        'assetRef': assetRef,
      };

  factory EvidenceItemModel.fromJson(Map<String, dynamic> json) {
    return EvidenceItemModel(
      id: json['id'] as String,
      titleId: json['titleId'] as String,
      descriptionId: json['descriptionId'] as String,
      category: json['category'] as String? ?? 'general',
      discoveredAt: json['discoveredAt'] as String? ?? DateTime.now().toIso8601String(),
      assetRef: json['assetRef'] as String?,
    );
  }
}

/// Complete game state save model.
/// Contains all canonical variables, flags, positions, and inventory.
class SaveModel {
  static const int currentVersion = 1;

  final int version;
  final String saveId;
  final String currentMap; // 'VILLAGE_ABANDONED', 'FAMILY_HOUSE', 'ALEX_BEDROOM', etc.
  final PlayerPositionModel position;
  final String chapter; // 'ACT_I_THE_RETURN', 'ACT_II_FAMILY_HOUSE'
  final List<InventoryItemModel> inventory;
  final List<EvidenceItemModel> evidence;

  // Interpersonal Trust variables
  final int trustEmma;
  final int trustJames;
  final int trustDavid;
  final int trustSarah;
  final int trustMichael;
  final int trustEthan;

  // Investigation statistics
  final int cluesDiscovered;
  final int evidence2014;
  final int memoriesReconstructed;
  final int liesDiscovered;

  // Narrative Progress & Metrics
  final Map<String, String> criticalChoices;
  final int suspicionLevel;
  final int truthProgress;
  final int lieProgress;
  final bool bunkerAccess;
  final String? potentialEnding;

  // Narrative Flags
  final Map<String, bool> flags;

  // Metadata
  final int? countdown;
  final int playTimeSeconds;
  final String createdAt;
  final String updatedAt;

  const SaveModel({
    this.version = currentVersion,
    required this.saveId,
    required this.currentMap,
    required this.position,
    required this.chapter,
    required this.inventory,
    required this.evidence,
    this.trustEmma = 50,
    this.trustJames = 50,
    this.trustDavid = 50,
    this.trustSarah = 50,
    this.trustMichael = 50,
    this.trustEthan = 50,
    this.cluesDiscovered = 0,
    this.evidence2014 = 0,
    this.memoriesReconstructed = 0,
    this.liesDiscovered = 0,
    required this.criticalChoices,
    this.suspicionLevel = 0,
    this.truthProgress = 0,
    this.lieProgress = 0,
    this.bunkerAccess = false,
    this.potentialEnding,
    required this.flags,
    this.countdown,
    this.playTimeSeconds = 0,
    required this.createdAt,
    required this.updatedAt,
  });

  /// Factory for a brand-new game start.
  factory SaveModel.newGame({String? saveId}) {
    final now = DateTime.now().toIso8601String();
    return SaveModel(
      version: currentVersion,
      saveId: saveId ?? 'save_default',
      currentMap: 'VILLAGE_ABANDONED',
      position: const PlayerPositionModel(x: 200.0, y: 350.0, orientation: 'SE'),
      chapter: 'ACT_I_THE_RETURN',
      inventory: const [],
      evidence: const [],
      trustEmma: 50,
      trustJames: 50,
      trustDavid: 50,
      trustSarah: 50,
      trustMichael: 50,
      trustEthan: 50,
      cluesDiscovered: 0,
      evidence2014: 0,
      memoriesReconstructed: 0,
      liesDiscovered: 0,
      criticalChoices: {},
      suspicionLevel: 0,
      truthProgress: 0,
      lieProgress: 0,
      bunkerAccess: false,
      potentialEnding: null,
      flags: {
        'received_ethan_message': false,
        'found_old_key': false,
        'found_cassette': false,
        'met_emma': false,
        'met_james': false,
        'met_michael': false,
        'discovered_2014_document': false,
        'reconstructed_memory_01': false,
        'found_bunker': false,
        'opened_bunker': false,
        'met_ethan': false,
        'countdown_started': false,
        'final_confrontation': false,
      },
      countdown: null,
      playTimeSeconds: 0,
      createdAt: now,
      updatedAt: now,
    );
  }

  SaveModel copyWith({
    int? version,
    String? saveId,
    String? currentMap,
    PlayerPositionModel? position,
    String? chapter,
    List<InventoryItemModel>? inventory,
    List<EvidenceItemModel>? evidence,
    int? trustEmma,
    int? trustJames,
    int? trustDavid,
    int? trustSarah,
    int? trustMichael,
    int? trustEthan,
    int? cluesDiscovered,
    int? evidence2014,
    int? memoriesReconstructed,
    int? liesDiscovered,
    Map<String, String>? criticalChoices,
    int? suspicionLevel,
    int? truthProgress,
    int? lieProgress,
    bool? bunkerAccess,
    String? potentialEnding,
    Map<String, bool>? flags,
    int? countdown,
    int? playTimeSeconds,
    String? createdAt,
    String? updatedAt,
  }) {
    return SaveModel(
      version: version ?? this.version,
      saveId: saveId ?? this.saveId,
      currentMap: currentMap ?? this.currentMap,
      position: position ?? this.position,
      chapter: chapter ?? this.chapter,
      inventory: inventory ?? this.inventory,
      evidence: evidence ?? this.evidence,
      trustEmma: trustEmma ?? this.trustEmma,
      trustJames: trustJames ?? this.trustJames,
      trustDavid: trustDavid ?? this.trustDavid,
      trustSarah: trustSarah ?? this.trustSarah,
      trustMichael: trustMichael ?? this.trustMichael,
      trustEthan: trustEthan ?? this.trustEthan,
      cluesDiscovered: cluesDiscovered ?? this.cluesDiscovered,
      evidence2014: evidence2014 ?? this.evidence2014,
      memoriesReconstructed: memoriesReconstructed ?? this.memoriesReconstructed,
      liesDiscovered: liesDiscovered ?? this.liesDiscovered,
      criticalChoices: criticalChoices ?? this.criticalChoices,
      suspicionLevel: suspicionLevel ?? this.suspicionLevel,
      truthProgress: truthProgress ?? this.truthProgress,
      lieProgress: lieProgress ?? this.lieProgress,
      bunkerAccess: bunkerAccess ?? this.bunkerAccess,
      potentialEnding: potentialEnding ?? this.potentialEnding,
      flags: flags ?? this.flags,
      countdown: countdown ?? this.countdown,
      playTimeSeconds: playTimeSeconds ?? this.playTimeSeconds,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? DateTime.now().toIso8601String(),
    );
  }

  Map<String, dynamic> toJson() => {
        'version': version,
        'saveId': saveId,
        'currentMap': currentMap,
        'position': position.toJson(),
        'chapter': chapter,
        'inventory': inventory.map((i) => i.toJson()).toList(),
        'evidence': evidence.map((e) => e.toJson()).toList(),
        'trustEmma': trustEmma,
        'trustJames': trustJames,
        'trustDavid': trustDavid,
        'trustSarah': trustSarah,
        'trustMichael': trustMichael,
        'trustEthan': trustEthan,
        'cluesDiscovered': cluesDiscovered,
        'evidence2014': evidence2014,
        'memoriesReconstructed': memoriesReconstructed,
        'liesDiscovered': liesDiscovered,
        'criticalChoices': criticalChoices,
        'suspicionLevel': suspicionLevel,
        'truthProgress': truthProgress,
        'lieProgress': lieProgress,
        'bunkerAccess': bunkerAccess,
        'potentialEnding': potentialEnding,
        'flags': flags,
        'countdown': countdown,
        'playTimeSeconds': playTimeSeconds,
        'createdAt': createdAt,
        'updatedAt': updatedAt,
      };

  factory SaveModel.fromJson(Map<String, dynamic> json) {
    return SaveModel(
      version: json['version'] as int? ?? currentVersion,
      saveId: json['saveId'] as String? ?? 'save_default',
      currentMap: json['currentMap'] as String? ?? 'VILLAGE_ABANDONED',
      position: json['position'] != null
          ? PlayerPositionModel.fromJson(json['position'] as Map<String, dynamic>)
          : PlayerPositionModel.initial(),
      chapter: json['chapter'] as String? ?? 'ACT_I_THE_RETURN',
      inventory: (json['inventory'] as List<dynamic>?)
              ?.map((item) => InventoryItemModel.fromJson(item as Map<String, dynamic>))
              .toList() ??
          [],
      evidence: (json['evidence'] as List<dynamic>?)
              ?.map((e) => EvidenceItemModel.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      trustEmma: json['trustEmma'] as int? ?? 50,
      trustJames: json['trustJames'] as int? ?? 50,
      trustDavid: json['trustDavid'] as int? ?? 50,
      trustSarah: json['trustSarah'] as int? ?? 50,
      trustMichael: json['trustMichael'] as int? ?? 50,
      trustEthan: json['trustEthan'] as int? ?? 50,
      cluesDiscovered: json['cluesDiscovered'] as int? ?? 0,
      evidence2014: json['evidence2014'] as int? ?? 0,
      memoriesReconstructed: json['memoriesReconstructed'] as int? ?? 0,
      liesDiscovered: json['liesDiscovered'] as int? ?? 0,
      criticalChoices: (json['criticalChoices'] as Map<String, dynamic>?)
              ?.map((k, v) => MapEntry(k, v.toString())) ??
          {},
      suspicionLevel: json['suspicionLevel'] as int? ?? 0,
      truthProgress: json['truthProgress'] as int? ?? 0,
      lieProgress: json['lieProgress'] as int? ?? 0,
      bunkerAccess: json['bunkerAccess'] as bool? ?? false,
      potentialEnding: json['potentialEnding'] as String?,
      flags: (json['flags'] as Map<String, dynamic>?)
              ?.map((k, v) => MapEntry(k, v as bool)) ??
          {},
      countdown: json['countdown'] as int?,
      playTimeSeconds: json['playTimeSeconds'] as int? ?? 0,
      createdAt: json['createdAt'] as String? ?? DateTime.now().toIso8601String(),
      updatedAt: json['updatedAt'] as String? ?? DateTime.now().toIso8601String(),
    );
  }

  String serialize() => jsonEncode(toJson());

  static SaveModel deserialize(String jsonStr) =>
      SaveModel.fromJson(jsonDecode(jsonStr) as Map<String, dynamic>);
}
