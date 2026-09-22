import 'save_model.dart';

/// Abstract contract for save persistence.
/// Pure local architecture: does not depend on any cloud, Firebase or external network service.
abstract class SaveRepository {
  /// Persists a game state.
  Future<void> save(SaveModel model);

  /// Loads a game state for a specific saveId. Returns null if none exists.
  Future<SaveModel?> load({String saveId = 'save_default'});

  /// Checks if a save exists for a specific saveId.
  Future<bool> hasSave({String saveId = 'save_default'});

  /// Deletes a save for a specific saveId.
  Future<void> deleteSave({String saveId = 'save_default'});

  /// Lists all available local save slot IDs.
  Future<List<String>> listSaveSlots();
}
