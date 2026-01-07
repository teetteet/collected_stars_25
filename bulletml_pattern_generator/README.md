# BulletML Pattern Generator

A comprehensive Python-based tool for creating and managing BulletML patterns with an interactive GUI.

## Features

- **Interactive GUI** with sliders and keyboard inputs for all parameters
- **Real-time XML preview** of generated BulletML patterns
- **Load/Save functionality** for BulletML XML files
- **Preset patterns** (Spiral, Circle, Wave, Flower)
- **Full keyboard shortcut support** for efficient workflow
- **Comprehensive parameter control** including:
  - Bullets per shoot, sprite selection
  - Position displacement (X/Y)
  - Speed and acceleration
  - Angle targeting and increments
  - Sine wave behaviors
  - Polar coordinates
  - Rotation speed
  - Iteration-based modifications
  - Timing controls

## Installation

### Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)

### Setup

1. Clone or download this repository
2. Navigate to the `bulletml_pattern_generator` directory
3. Install dependencies (if needed):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

Or run directly:

```bash
python -m bulletml_pattern_generator.main
```

### GUI Controls

The interface is divided into two main panels:

- **Left Panel**: Parameter controls with sliders and inputs
- **Right Panel**: Real-time XML preview of the generated pattern

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save pattern to file |
| `Ctrl+O` | Load pattern from file |
| `Ctrl+R` | Reset to default values |
| `Ctrl+U` | Update XML preview |
| `Ctrl+1` | Load Spiral preset |
| `Ctrl+2` | Load Circle preset |
| `Ctrl+3` | Load Wave preset |
| `Ctrl+4` | Load Flower preset |

### Parameters

#### Basic Parameters
- **Bullets Per Shoot**: Number of bullets fired in each shoot (1-100)
- **Repeat Count**: Number of times the pattern repeats (1-50)
- **Wait Time**: Delay between repeats in seconds (0.0-2.0)

#### Position
- **Position X/Y**: Starting position offset (-200 to 200)

#### Movement
- **Speed**: Base bullet speed (0.1-10.0)
- **Acceleration**: Rate of speed change (-1.0 to 1.0)

#### Angle
- **Target Angle**: Base firing angle (0-360°)
- **Angle Increment**: Angle difference between bullets (0-360°)
- **Rotation Speed**: Rotation applied per bullet (-20 to 20)

#### Sine Wave (Optional)
- **Enable Sine Wave**: Toggle sine wave modulation
- **Amplitude**: Sine wave strength (0-50)
- **Frequency**: Oscillation rate (0-10)
- **Phase**: Starting phase offset (0-6.28)

#### Polar Coordinates (Optional)
- **Enable Polar**: Toggle polar coordinate transformation
- **Radius**: Distance from origin (0-200)
- **Angle Offset**: Polar angle offset (0-360°)

#### Iteration Modifications
- **Speed Modifier**: Per-bullet speed increment (-0.5 to 0.5)
- **Direction Modifier**: Per-bullet angle increment (-10 to 10)

## Preset Patterns

### Spiral
A rotating spiral pattern with 12 bullets expanding outward.

### Circle
A perfect 360-degree circular pattern with 36 evenly spaced bullets.

### Wave
An 8-bullet pattern with sine wave modulation for organic movement.

### Flower
A 16-petal flower pattern using polar coordinates.

## Example Patterns

Two example XML patterns are included in the `examples/` directory:

- `spiral_pattern.xml` - Rotating spiral effect
- `circle_pattern.xml` - Full 360-degree pattern

Load these files using `Ctrl+O` or the Load button to explore their parameters.

## Testing

Run the automated test suite:

```bash
python test_generator.py
```

Or using unittest:

```bash
python -m unittest test_generator.py
```

Tests verify:
- Default pattern generation
- Custom pattern creation
- XML loading and parsing
- File save/load functionality
- Parameter validation
- Preset loading

## Implementation Details

### Architecture

The generator is implemented in three main modules:

1. **bulletml_core.py** - Core pattern generation and XML handling
   - `BulletMLGenerator` class for pattern creation
   - XML generation and parsing
   - Parameter management
   - Preset configurations

2. **gui.py** - Tkinter-based GUI with parameter controls
   - Interactive sliders for all parameters
   - Real-time XML preview
   - File operations (load/save)
   - Preset buttons

3. **main.py** - Application entry point
   - Initializes and launches the GUI
   - Displays keyboard shortcuts

### BulletML Format

BulletML is an XML-based format for describing bullet patterns in shooting games. This generator creates patterns following the BulletML specification with support for:

- Absolute and relative directions
- Speed and acceleration
- Bullet actions and behaviors
- Repeated patterns
- Timing controls

## Contributing

Contributions are welcome! Areas for improvement:

- Additional preset patterns
- More advanced BulletML features (references, variables)
- Pattern visualization
- Export to different formats
- Undo/Redo functionality

## License

This project is open source and available under the MIT License.

## Credits

Created as part of the collected_stars_25 repository.

BulletML specification: http://www.asahi-net.or.jp/~cs8k-cyu/bulletml/

## References

- [BulletML Official Site](http://www.asahi-net.or.jp/~cs8k-cyu/bulletml/)
- [BulletML Specification](http://www.asahi-net.or.jp/~cs8k-cyu/bulletml/bulletml_ref_e.html)
- Related projects in the repository:
  - [dmanning23/BulletMLLib](https://github.com/dmanning23/BulletMLLib) - C# BulletML library
  - [thejustinwalsh/libbulletml](https://github.com/thejustinwalsh/libbulletml) - Modern C++ fork
  - [daishihmr/bulletml.js](https://github.com/daishihmr/bulletml.js) - JavaScript library
  - [SolAZDev/GodotBulletML](https://github.com/SolAZDev/GodotBulletML) - Godot implementation
