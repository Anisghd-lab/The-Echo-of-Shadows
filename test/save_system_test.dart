import 'dart:io';
import '../lib/save/local_save_repository.dart';
import '../lib/save/save_manager.dart';
import '../lib/save/save_model.dart';

void main() async {
  print('--- Running Save System Verification ---');

  final tempDir = Directory.systemTemp.createTempSync('echo_save_test_');
  print('Using temporary directory for local save: ${tempDir.path}');

  try {
    final repository = LocalSaveRepository(baseDirectoryPath: tempDir.path);
    final manager = SaveManager(repository: repository);

    // 1. Initial State Check
    assert(!manager.hasActiveSession, 'No active session should exist initially');
    assert(!await manager.hasSavedGame(), 'No saved game should exist in slot');

    // 2. Create New Game
    final newSave = await manager.createNewGame(saveId: 'slot_test_01');
    assert(manager.hasActiveSession, 'Active session should be created');
    assert(newSave.currentMap == 'VILLAGE_ABANDONED', 'Initial map must be VILLAGE_ABANDONED');
    assert(newSave.chapter == 'ACT_I_THE_RETURN', 'Initial chapter must be ACT_I_THE_RETURN');
    assert(newSave.trustEmma == 50, 'Emma trust must be default 50');
    assert(!manager.getFlag('received_ethan_message'), 'Flag received_ethan_message must be false');

    // 3. Narrative Updates & Gameplay Loop Simulation
    manager.setFlag('received_ethan_message', true);
    manager.updatePosition(
      map: 'FAMILY_HOUSE',
      x: 320.5,
      y: 180.2,
      orientation: 'NW',
    );
    manager.addInventoryItem(const InventoryItemModel(
      id: 'old_key',
      nameId: 'ITEM_OLD_KEY',
      type: 'key',
      usable: true,
      isEvidence: true,
      evidenceId: 'EVIDENCE_KEY_01',
    ));
    manager.discoverEvidence(EvidenceItemModel(
      id: 'EVIDENCE_CASSETTE_01',
      titleId: 'EVIDENCE_TITLE_CASSETTE',
      descriptionId: 'EVIDENCE_DESC_CASSETTE',
      category: '2014',
      discoveredAt: DateTime.now().toIso8601String(),
    ));
    manager.updateTrust('emma', 10);
    manager.updateSuspicion(15);
    manager.updateTruthProgress(25);
    manager.recordCriticalChoice('CHOICE_01_PHONE', 'READ_MESSAGE_IMMEDIATELY');

    // 4. Save to Disk
    final saveSuccess = await manager.saveGame();
    assert(saveSuccess, 'Game save must succeed');
    assert(await manager.hasSavedGame(saveId: 'slot_test_01'), 'Save file must exist on disk');

    // 5. Load into completely separate SaveManager instance (Cold boot test)
    final freshRepo = LocalSaveRepository(baseDirectoryPath: tempDir.path);
    final freshManager = SaveManager(repository: freshRepo);
    final loadedSave = await freshManager.loadGame(saveId: 'slot_test_01');

    assert(loadedSave != null, 'Loaded save must not be null');
    assert(loadedSave!.currentMap == 'FAMILY_HOUSE', 'Map should be restored to FAMILY_HOUSE');
    assert(loadedSave.position.x == 320.5, 'Position X should be restored to 320.5');
    assert(loadedSave.position.orientation == 'NW', 'Orientation should be NW');
    assert(loadedSave.flags['received_ethan_message'] == true, 'Flag must be true');
    assert(loadedSave.trustEmma == 60, 'Emma trust should be 60 (50 + 10)');
    assert(loadedSave.suspicionLevel == 15, 'Suspicion level should be 15');
    assert(loadedSave.truthProgress == 25, 'Truth progress should be 25');
    assert(loadedSave.inventory.any((i) => i.id == 'old_key'), 'Inventory must contain old_key');
    assert(loadedSave.evidence.any((e) => e.id == 'EVIDENCE_CASSETTE_01'), 'Evidence must be present');
    assert(loadedSave.cluesDiscovered == 1, 'Clues discovered must be 1');
    assert(loadedSave.evidence2014 == 1, 'Evidence 2014 counter must be 1');
    assert(loadedSave.criticalChoices['CHOICE_01_PHONE'] == 'READ_MESSAGE_IMMEDIATELY', 'Choice preserved');

    // 6. Delete Save
    await freshManager.deleteGame(saveId: 'slot_test_01');
    assert(!await freshManager.hasSavedGame(saveId: 'slot_test_01'), 'Save slot should be empty after deletion');

    print('✅ ALL SAVE SYSTEM TESTS PASSED SUCCESSFULLY!');
  } finally {
    if (tempDir.existsSync()) {
      tempDir.deleteSync(recursive: true);
    }
  }
}
