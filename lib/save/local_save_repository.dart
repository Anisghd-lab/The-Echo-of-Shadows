import 'dart:convert';
import 'dart:io';
import 'save_model.dart';
import 'save_repository.dart';

/// Concrete implementation of [SaveRepository] targeting local storage on the device.
/// 
/// Guarantees:
/// - 100% offline & local (0% Firebase, 0% server, 0% cloud)
/// - Atomic write operations via temporary files (.tmp) to prevent corruption upon unexpected shutdown
/// - Automatic recovery from backup files (.bak) in case of file corruption
class LocalSaveRepository implements SaveRepository {
  final String _baseDirectoryPath;

  LocalSaveRepository({String? baseDirectoryPath})
      : _baseDirectoryPath = baseDirectoryPath ?? _defaultLocalSaveDir();

  /// Default directory for local saves on the filesystem.
  static String _defaultLocalSaveDir() {
    // In local standalone Dart/Flutter environment:
    final home = Platform.environment['HOME'] ?? '.';
    return '$home/.echo_of_shadows/saves';
  }

  /// Resolves the file path for a given save slot.
  File _getSaveFile(String saveId) {
    final dir = Directory(_baseDirectoryPath);
    if (!dir.existsSync()) {
      dir.createSync(recursive: true);
    }
    return File('${dir.path}/$saveId.json');
  }

  /// Resolves the backup file path for a given save slot.
  File _getBackupFile(String saveId) {
    return File('${_baseDirectoryPath}/$saveId.json.bak');
  }

  @override
  Future<void> save(SaveModel model) async {
    final file = _getSaveFile(model.saveId);
    final backupFile = _getBackupFile(model.saveId);
    final tempFile = File('${file.path}.tmp');

    try {
      final jsonString = const JsonEncoder.withIndent('  ').convert(model.toJson());

      // 1. Write to temporary file first (atomic safety)
      await tempFile.writeAsString(jsonString, flush: true);

      // 2. If existing primary save exists, keep it as backup
      if (await file.exists()) {
        if (await backupFile.exists()) {
          await backupFile.delete();
        }
        await file.rename(backupFile.path);
      }

      // 3. Move temp file to primary file
      await tempFile.rename(file.path);
    } catch (e) {
      // Clean up temp file on failure
      if (await tempFile.exists()) {
        await tempFile.delete();
      }
      rethrow;
    }
  }

  @override
  Future<SaveModel?> load({String saveId = 'save_default'}) async {
    final file = _getSaveFile(saveId);
    final backupFile = _getBackupFile(saveId);

    // Try loading primary save file
    if (await file.exists()) {
      try {
        final content = await file.readAsString();
        final jsonMap = jsonDecode(content) as Map<String, dynamic>;
        return SaveModel.fromJson(jsonMap);
      } catch (e) {
        // Primary file corrupted, attempt backup recovery
        if (await backupFile.exists()) {
          try {
            final backupContent = await backupFile.readAsString();
            final jsonMap = jsonDecode(backupContent) as Map<String, dynamic>;
            final recovered = SaveModel.fromJson(jsonMap);
            // Restore primary from backup
            await backupFile.copy(file.path);
            return recovered;
          } catch (_) {
            return null;
          }
        }
        return null;
      }
    }

    // If primary not found, check if backup exists
    if (await backupFile.exists()) {
      try {
        final backupContent = await backupFile.readAsString();
        final jsonMap = jsonDecode(backupContent) as Map<String, dynamic>;
        return SaveModel.fromJson(jsonMap);
      } catch (_) {
        return null;
      }
    }

    return null;
  }

  @override
  Future<bool> hasSave({String saveId = 'save_default'}) async {
    final file = _getSaveFile(saveId);
    if (await file.exists()) {
      return true;
    }
    final backupFile = _getBackupFile(saveId);
    return await backupFile.exists();
  }

  @override
  Future<void> deleteSave({String saveId = 'save_default'}) async {
    final file = _getSaveFile(saveId);
    final backupFile = _getBackupFile(saveId);
    if (await file.exists()) {
      await file.delete();
    }
    if (await backupFile.exists()) {
      await backupFile.delete();
    }
  }

  @override
  Future<List<String>> listSaveSlots() async {
    final dir = Directory(_baseDirectoryPath);
    if (!await dir.exists()) {
      return [];
    }

    final slots = <String>[];
    await for (final entity in dir.list()) {
      if (entity is File && entity.path.endsWith('.json') && !entity.path.endsWith('.tmp')) {
        final basename = entity.uri.pathSegments.last;
        final slotId = basename.substring(0, basename.length - 5);
        slots.add(slotId);
      }
    }
    return slots;
  }
}
