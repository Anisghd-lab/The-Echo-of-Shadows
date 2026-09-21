import 'package:flame/components.dart';
import '../../player/alex_component.dart';

/// Layer 5: Characters layer dynamically sorted by ground contact point.
class CharactersLayer extends Component {
  final AlexComponent alex;

  CharactersLayer({required this.alex});

  @override
  Future<void> onLoad() async {
    add(alex);
  }
}
