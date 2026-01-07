"""
BulletML Pattern Generator - Core Module
Handles pattern generation and XML creation/manipulation
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import math
from typing import Dict, Any, Optional


class BulletMLGenerator:
    """Core class for generating BulletML patterns"""
    
    def __init__(self):
        self.reset_to_defaults()
    
    def reset_to_defaults(self):
        """Reset all parameters to default values"""
        self.params = {
            'bullets_per_shoot': 10,
            'sprite': 'bullet_sprite',
            'pos_x': 0.0,
            'pos_y': 0.0,
            'speed': 1.0,
            'acceleration': 0.0,
            'angle_target': 0.0,
            'angle_increment': 36.0,
            'sine_enabled': False,
            'sine_amplitude': 0.0,
            'sine_frequency': 1.0,
            'sine_phase': 0.0,
            'polar_enabled': False,
            'polar_radius': 100.0,
            'polar_angle': 0.0,
            'rotation_speed': 0.0,
            'iter_speed_mod': 0.0,
            'iter_direction_mod': 0.0,
            'wait_time': 0.0,
            'repeat_count': 1
        }
    
    def set_parameter(self, param_name: str, value: Any):
        """Set a specific parameter value"""
        if param_name in self.params:
            self.params[param_name] = value
    
    def get_parameter(self, param_name: str) -> Any:
        """Get a specific parameter value"""
        return self.params.get(param_name)
    
    def get_all_parameters(self) -> Dict[str, Any]:
        """Get all current parameters"""
        return self.params.copy()
    
    def set_all_parameters(self, params: Dict[str, Any]):
        """Set multiple parameters at once"""
        for key, value in params.items():
            if key in self.params:
                self.params[key] = value
    
    def load_preset(self, preset_name: str):
        """Load a preset pattern configuration"""
        presets = {
            'spiral': {
                'bullets_per_shoot': 12,
                'angle_increment': 30.0,
                'rotation_speed': 5.0,
                'speed': 2.0,
                'repeat_count': 10,
                'wait_time': 0.05
            },
            'circle': {
                'bullets_per_shoot': 36,
                'angle_increment': 10.0,
                'rotation_speed': 0.0,
                'speed': 1.5,
                'repeat_count': 1,
                'wait_time': 0.0
            },
            'wave': {
                'bullets_per_shoot': 8,
                'angle_increment': 45.0,
                'sine_enabled': True,
                'sine_amplitude': 2.0,
                'sine_frequency': 0.5,
                'speed': 1.0,
                'repeat_count': 15,
                'wait_time': 0.1
            },
            'flower': {
                'bullets_per_shoot': 16,
                'angle_increment': 22.5,
                'polar_enabled': True,
                'polar_radius': 50.0,
                'rotation_speed': 3.0,
                'speed': 0.8,
                'repeat_count': 8,
                'wait_time': 0.08
            }
        }
        
        if preset_name.lower() in presets:
            self.reset_to_defaults()
            self.set_all_parameters(presets[preset_name.lower()])
            return True
        return False
    
    def generate_pattern_xml(self) -> str:
        """Generate BulletML XML from current parameters"""
        # Create root bulletml element
        root = ET.Element('bulletml', {
            'xmlns': 'http://www.asahi-net.or.jp/~cs8k-cyu/bulletml',
            'type': 'vertical'
        })
        
        # Add action definition
        action = ET.SubElement(root, 'action', {'label': 'top'})
        
        # Add repeat if needed
        if self.params['repeat_count'] > 1:
            repeat = ET.SubElement(action, 'repeat')
            times = ET.SubElement(repeat, 'times')
            times.text = str(self.params['repeat_count'])
            action_ref = ET.SubElement(repeat, 'action')
            fire_action = action_ref
        else:
            fire_action = action
        
        # Generate bullets
        for i in range(self.params['bullets_per_shoot']):
            self._add_bullet_fire(fire_action, i)
        
        # Add wait time
        if self.params['wait_time'] > 0:
            wait = ET.SubElement(fire_action, 'wait')
            wait.text = str(self.params['wait_time'])
        
        # Pretty print XML
        xml_str = ET.tostring(root, encoding='unicode')
        dom = minidom.parseString(xml_str)
        return dom.toprettyxml(indent='  ')
    
    def _add_bullet_fire(self, parent: ET.Element, index: int):
        """Add a single bullet fire element"""
        fire = ET.SubElement(parent, 'fire')
        
        # Direction
        direction = ET.SubElement(fire, 'direction', {'type': 'absolute'})
        angle = self._calculate_angle(index)
        direction.text = str(angle)
        
        # Speed
        speed = ET.SubElement(fire, 'speed')
        calculated_speed = self._calculate_speed(index)
        speed.text = str(calculated_speed)
        
        # Bullet definition
        bullet = ET.SubElement(fire, 'bullet')
        
        # Add acceleration if set
        if self.params['acceleration'] != 0:
            accel_action = ET.SubElement(bullet, 'action')
            change_speed = ET.SubElement(accel_action, 'changeSpeed')
            speed_elem = ET.SubElement(change_speed, 'speed')
            speed_elem.text = str(self.params['acceleration'])
            term = ET.SubElement(change_speed, 'term')
            term.text = '60'
    
    def _calculate_angle(self, index: int) -> float:
        """Calculate angle for bullet at given index"""
        base_angle = self.params['angle_target'] + (index * self.params['angle_increment'])
        
        # Apply rotation
        base_angle += self.params['rotation_speed'] * index
        
        # Apply sine wave if enabled
        if self.params['sine_enabled']:
            sine_offset = (self.params['sine_amplitude'] * 
                          math.sin((index * self.params['sine_frequency']) + 
                                  self.params['sine_phase']))
            base_angle += sine_offset
        
        # Apply polar coordinates if enabled
        if self.params['polar_enabled']:
            polar_angle = math.radians(self.params['polar_angle'])
            base_angle = math.degrees(math.atan2(
                self.params['polar_radius'] * math.sin(polar_angle + math.radians(base_angle)),
                self.params['polar_radius'] * math.cos(polar_angle + math.radians(base_angle))
            ))
        
        # Apply iteration-based direction modification
        base_angle += self.params['iter_direction_mod'] * index
        
        return base_angle % 360
    
    def _calculate_speed(self, index: int) -> float:
        """Calculate speed for bullet at given index"""
        speed = self.params['speed']
        
        # Apply iteration-based speed modification
        speed += self.params['iter_speed_mod'] * index
        
        return max(0.1, speed)  # Ensure minimum speed
    
    def save_to_file(self, filename: str) -> bool:
        """Save current pattern to XML file"""
        try:
            xml_content = self.generate_pattern_xml()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def load_from_file(self, filename: str) -> bool:
        """Load pattern from XML file and extract parameters"""
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            
            # Parse XML and extract parameters (basic implementation)
            # This is a simplified parser that tries to extract common patterns
            self.reset_to_defaults()
            
            # Find action
            action = root.find('.//{http://www.asahi-net.or.jp/~cs8k-cyu/bulletml}action[@label="top"]')
            if action is None:
                action = root.find('.//action[@label="top"]')
            
            if action is not None:
                # Check for repeat
                repeat_elem = action.find('.//{http://www.asahi-net.or.jp/~cs8k-cyu/bulletml}repeat')
                if repeat_elem is None:
                    repeat_elem = action.find('.//repeat')
                
                if repeat_elem is not None:
                    times_elem = repeat_elem.find('.//{http://www.asahi-net.or.jp/~cs8k-cyu/bulletml}times')
                    if times_elem is None:
                        times_elem = repeat_elem.find('.//times')
                    if times_elem is not None and times_elem.text:
                        self.params['repeat_count'] = int(times_elem.text)
                
                # Count fire elements to get bullets per shoot
                fires = action.findall('.//{http://www.asahi-net.or.jp/~cs8k-cyu/bulletml}fire')
                if not fires:
                    fires = action.findall('.//fire')
                
                if fires:
                    self.params['bullets_per_shoot'] = len(fires)
                    
                    # Get first fire element to extract base parameters
                    first_fire = fires[0]
                    
                    # Extract speed
                    speed_elem = first_fire.find('.//{http://www.asahi-net.or.jp/~cs8k-cyu/bulletml}speed')
                    if speed_elem is None:
                        speed_elem = first_fire.find('.//speed')
                    if speed_elem is not None and speed_elem.text:
                        try:
                            self.params['speed'] = float(speed_elem.text)
                        except ValueError:
                            pass
                    
                    # Extract direction
                    direction_elem = first_fire.find('.//{http://www.asahi-net.or.jp/~cs8k-cyu/bulletml}direction')
                    if direction_elem is None:
                        direction_elem = first_fire.find('.//direction')
                    if direction_elem is not None and direction_elem.text:
                        try:
                            self.params['angle_target'] = float(direction_elem.text)
                        except ValueError:
                            pass
                    
                    # Try to detect angle increment
                    if len(fires) > 1:
                        second_fire = fires[1]
                        second_dir = second_fire.find('.//{http://www.asahi-net.or.jp/~cs8k-cyu/bulletml}direction')
                        if second_dir is None:
                            second_dir = second_fire.find('.//direction')
                        if second_dir is not None and second_dir.text and direction_elem is not None and direction_elem.text:
                            try:
                                first_angle = float(direction_elem.text)
                                second_angle = float(second_dir.text)
                                self.params['angle_increment'] = abs(second_angle - first_angle)
                            except ValueError:
                                pass
                
                # Extract wait time
                wait_elem = action.find('.//{http://www.asahi-net.or.jp/~cs8k-cyu/bulletml}wait')
                if wait_elem is None:
                    wait_elem = action.find('.//wait')
                if wait_elem is not None and wait_elem.text:
                    try:
                        self.params['wait_time'] = float(wait_elem.text)
                    except ValueError:
                        pass
            
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def get_xml_preview(self) -> str:
        """Get formatted XML preview"""
        return self.generate_pattern_xml()
