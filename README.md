# L'Écho des Ombres (The Echo of Shadows)

> A 2.5D Isometric Psychological Thriller Game built with **Flutter & Flame**.

## Save Architecture

The persistence layer is **100% local, offline-first, with zero cloud/Firebase dependencies**:

```
SaveManager
    ↓
SaveRepository
    ↓
LocalSaveRepository
    ↓
Stockage local (Atomic .json + .bak recovery)
```

- `lib/save/save_model.dart`: Complete immutable narrative, position, inventory, evidence, trust, and flag state.
- `lib/save/save_repository.dart`: Abstract repository interface.
- `lib/save/local_save_repository.dart`: Concrete local disk storage with atomic write and backup recovery.
- `lib/save/save_manager.dart`: High-level game state orchestrator and notification dispatcher.
- `test/save_system_test.dart`: Automated test suite for persistence, recovery, and serialization.
