import 'local_save_repository.dart';
import 'save_model.dart';
import 'save_repository.dart';

typedef SaveStateListener = void Function(SaveModel? save);

/// Central orchestrator for all save operations in L'Écho des Ombres.
/// 
/// Follows the architecture:
/// SaveManager -> SaveRepository -> LocalSaveRepository -> Stockage local
/// 
/// Guarantees:
/// - 0% Firebase / 0% Server / 0% Cloud
/// - 100% Local offline persistence
class SaveManager {
  final SaveRepository _repository;
  SaveModel? _currentSave;
  final List<SaveStateListener> _listeners = [];

  SaveManager({SaveRepository? repository})
      : _repository = repository ?? LocalSaveRepository();

  /// Currently loaded game state.
  SaveModel? get currentSave => _currentSave;

  /// Whether an active game session is loaded in memory.
  bool get hasActiveSession => _currentSave != null;

  /// Registers a listener to receive save state updates.
  void addListener(SaveStateListener listener) {
    _listeners.add(listener);
  }

  /// Unregisters a save state listener.
  void removeListener(SaveStateListener listener) {
    _listeners.remove(listener);
  }

  void _notifyListeners() {
    for (final listener in _listeners) {
      listener(_currentSave);
    }
  }

  /// Initializes the save manager and checks if a default save exists.
  Future<bool> initialize({String defaultSlot = 'save_default'}) async {
    return await _repository.hasSave(saveId: defaultSlot);
  }

  /// Starts a brand new game session.
  Future<SaveModel> createNewGame({String saveId = 'save_default'}) async {
    final newSave = SaveModel.newGame(saveId: saveId);
    _currentSave = newSave;
    await _repository.save(newSave);
    _notifyListeners();
    return newSave;
  }

  /// Persists the current in-memory game state to local storage.
  Future<bool> saveGame() async {
    if (_currentSave == null) return false;
    try {
      final updated = _currentSave!.copyWith(
        updatedAt: DateTime.now().toIso8601String(),
      );
      _currentSave = updated;
      await _repository.save(updated);
      _notifyListeners();
      return true;
    } catch (_) {
      return false;
    }
  }

  /// Triggers an automatic checkpoint save (e.g. on entering family house, discovering evidence).
  Future<bool> autoSave() async {
    return await saveGame();
  }

  /// Loads an existing save from local storage into memory.
  Future<SaveModel?> loadGame({String saveId = 'save_default'}) async {
    final loaded = await _repository.load(saveId: saveId);
    if (loaded != null) {
      _currentSave = loaded;
      _notifyListeners();
    }
    return loaded;
  }

  /// Checks if a save exists in the specified slot.
  Future<bool> hasSavedGame({String saveId = 'save_default'}) async {
    return await _repository.hasSave(saveId: saveId);
  }

  /// Deletes a save slot from local storage.
  Future<void> deleteGame({String saveId = 'save_default'}) async {
    await _repository.deleteSave(saveId: saveId);
    if (_currentSave?.saveId == saveId) {
      _currentSave = null;
      _notifyListeners();
    }
  }

  // ===========================================================================
  // In-Game State Mutations (Local Game Loop Updates)
  // ===========================================================================

  /// Updates Alex's current isometric map, position, and orientation.
  void updatePosition({
    required String map,
    required double x,
    required double y,
    required String orientation,
  }) {
    if (_currentSave == null) return;
    _currentSave = _currentSave!.copyWith(
      currentMap: map,
      position: PlayerPositionModel(x: x, y: y, orientation: orientation),
    );
    _notifyListeners();
  }

  /// Sets a narrative flag (e.g. 'received_ethan_message', 'found_old_key').
  void setFlag(String flagName, bool value) {
    if (_currentSave == null) return;
    final updatedFlags = Map<String, bool>.from(_currentSave!.flags);
    updatedFlags[flagName] = value;
    _currentSave = _currentSave!.copyWith(flags: updatedFlags);
    _notifyListeners();
  }

  /// Reads a narrative flag safely.
  bool getFlag(String flagName, {bool defaultValue = false}) {
    return _currentSave?.flags[flagName] ?? defaultValue;
  }

  /// Adds an item to Alex's inventory.
  void addInventoryItem(InventoryItemModel item) {
    if (_currentSave == null) return;
    final updatedInventory = List<InventoryItemModel>.from(_currentSave!.inventory);
    if (!updatedInventory.any((i) => i.id == item.id)) {
      updatedInventory.add(item);
      _currentSave = _currentSave!.copyWith(inventory: updatedInventory);
      _notifyListeners();
    }
  }

  /// Removes an item from Alex's inventory.
  void removeInventoryItem(String itemId) {
    if (_currentSave == null) return;
    final updatedInventory = _currentSave!.inventory.where((i) => i.id != itemId).toList();
    _currentSave = _currentSave!.copyWith(inventory: updatedInventory);
    _notifyListeners();
  }

  /// Checks if Alex has a specific item.
  bool hasInventoryItem(String itemId) {
    return _currentSave?.inventory.any((i) => i.id == itemId) ?? false;
  }

  /// Records a newly discovered piece of evidence in Alex's journal.
  void discoverEvidence(EvidenceItemModel evidence) {
    if (_currentSave == null) return;
    final updatedEvidence = List<EvidenceItemModel>.from(_currentSave!.evidence);
    if (!updatedEvidence.any((e) => e.id == evidence.id)) {
      updatedEvidence.add(evidence);
      final newCluesCount = _currentSave!.cluesDiscovered + 1;
      final new2014Count = evidence.category == '2014'
          ? _currentSave!.evidence2014 + 1
          : _currentSave!.evidence2014;

      _currentSave = _currentSave!.copyWith(
        evidence: updatedEvidence,
        cluesDiscovered: newCluesCount,
        evidence2014: new2014Count,
      );
      _notifyListeners();
    }
  }

  /// Checks if a piece of evidence has already been uncovered.
  bool hasEvidence(String evidenceId) {
    return _currentSave?.evidence.any((e) => e.id == evidenceId) ?? false;
  }

  /// Modifies interpersonal trust score for a specific character.
  void updateTrust(String character, int delta) {
    if (_currentSave == null) return;
    int clampTrust(int val) => val.clamp(0, 100);

    switch (character.toLowerCase()) {
      case 'emma':
        _currentSave = _currentSave!.copyWith(trustEmma: clampTrust(_currentSave!.trustEmma + delta));
        break;
      case 'james':
        _currentSave = _currentSave!.copyWith(trustJames: clampTrust(_currentSave!.trustJames + delta));
        break;
      case 'david':
        _currentSave = _currentSave!.copyWith(trustDavid: clampTrust(_currentSave!.trustDavid + delta));
        break;
      case 'sarah':
        _currentSave = _currentSave!.copyWith(trustSarah: clampTrust(_currentSave!.trustSarah + delta));
        break;
      case 'michael':
        _currentSave = _currentSave!.copyWith(trustMichael: clampTrust(_currentSave!.trustMichael + delta));
        break;
      case 'ethan':
        _currentSave = _currentSave!.copyWith(trustEthan: clampTrust(_currentSave!.trustEthan + delta));
        break;
    }
    _notifyListeners();
  }

  /// Adjusts global suspicion level.
  void updateSuspicion(int delta) {
    if (_currentSave == null) return;
    final newVal = (_currentSave!.suspicionLevel + delta).clamp(0, 100);
    _currentSave = _currentSave!.copyWith(suspicionLevel: newVal);
    _notifyListeners();
  }

  /// Advances truth progression.
  void updateTruthProgress(int delta) {
    if (_currentSave == null) return;
    final newVal = (_currentSave!.truthProgress + delta).clamp(0, 100);
    _currentSave = _currentSave!.copyWith(truthProgress: newVal);
    _notifyListeners();
  }

  /// Advances lie progression.
  void updateLieProgress(int delta) {
    if (_currentSave == null) return;
    final newVal = (_currentSave!.lieProgress + delta).clamp(0, 100);
    _currentSave = _currentSave!.copyWith(lieProgress: newVal);
    _notifyListeners();
  }

  /// Records a critical choice made in dialogue or investigation.
  void recordCriticalChoice(String choiceId, String optionId) {
    if (_currentSave == null) return;
    final updatedChoices = Map<String, String>.from(_currentSave!.criticalChoices);
    updatedChoices[choiceId] = optionId;
    _currentSave = _currentSave!.copyWith(criticalChoices: updatedChoices);
    _notifyListeners();
  }

  /// Advances the story chapter.
  void setChapter(String chapter) {
    if (_currentSave == null) return;
    _currentSave = _currentSave!.copyWith(chapter: chapter);
    _notifyListeners();
  }

  /// Grants or revokes bunker access.
  void setBunkerAccess(bool allowed) {
    if (_currentSave == null) return;
    _currentSave = _currentSave!.copyWith(bunkerAccess: allowed);
    _notifyListeners();
  }

  /// Adds elapsed play time in seconds.
  void addPlayTime(int seconds) {
    if (_currentSave == null) return;
    _currentSave = _currentSave!.copyWith(
      playTimeSeconds: _currentSave!.playTimeSeconds + seconds,
    );
  }
}
