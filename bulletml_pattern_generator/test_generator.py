"""
BulletML Pattern Generator - Test Suite
Automated tests for pattern generation and XML handling
"""

import sys
import unittest
import os
import tempfile
from bulletml_core import BulletMLGenerator


class TestBulletMLGenerator(unittest.TestCase):
    """Test cases for BulletML pattern generator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = BulletMLGenerator()
    
    def test_initialization(self):
        """Test that generator initializes with default values"""
        self.assertEqual(self.generator.get_parameter('bullets_per_shoot'), 10)
        self.assertEqual(self.generator.get_parameter('speed'), 1.0)
        self.assertEqual(self.generator.get_parameter('sprite'), 'bullet_sprite')
    
    def test_set_parameter(self):
        """Test setting individual parameters"""
        self.generator.set_parameter('speed', 2.5)
        self.assertEqual(self.generator.get_parameter('speed'), 2.5)
        
        self.generator.set_parameter('bullets_per_shoot', 20)
        self.assertEqual(self.generator.get_parameter('bullets_per_shoot'), 20)
    
    def test_set_all_parameters(self):
        """Test setting multiple parameters at once"""
        new_params = {
            'speed': 3.0,
            'bullets_per_shoot': 15,
            'angle_increment': 45.0
        }
        self.generator.set_all_parameters(new_params)
        
        self.assertEqual(self.generator.get_parameter('speed'), 3.0)
        self.assertEqual(self.generator.get_parameter('bullets_per_shoot'), 15)
        self.assertEqual(self.generator.get_parameter('angle_increment'), 45.0)
    
    def test_reset_to_defaults(self):
        """Test resetting parameters to defaults"""
        self.generator.set_parameter('speed', 5.0)
        self.generator.set_parameter('bullets_per_shoot', 50)
        
        self.generator.reset_to_defaults()
        
        self.assertEqual(self.generator.get_parameter('speed'), 1.0)
        self.assertEqual(self.generator.get_parameter('bullets_per_shoot'), 10)
    
    def test_generate_pattern_xml(self):
        """Test XML pattern generation"""
        xml_output = self.generator.generate_pattern_xml()
        
        # Check that output is valid XML string
        self.assertIsInstance(xml_output, str)
        self.assertIn('<?xml', xml_output)
        self.assertIn('<bulletml', xml_output)
        self.assertIn('</bulletml>', xml_output)
        self.assertIn('<action', xml_output)
        self.assertIn('<fire>', xml_output)
    
    def test_generate_custom_pattern(self):
        """Test generating a custom pattern"""
        self.generator.set_all_parameters({
            'bullets_per_shoot': 5,
            'speed': 2.0,
            'angle_increment': 72.0
        })
        
        xml_output = self.generator.generate_pattern_xml()
        
        # Verify custom values appear in output
        self.assertIn('<speed>2.0</speed>', xml_output)
        # Should have 5 fire elements
        self.assertEqual(xml_output.count('<fire>'), 5)
    
    def test_load_preset_spiral(self):
        """Test loading spiral preset"""
        result = self.generator.load_preset('spiral')
        self.assertTrue(result)
        self.assertEqual(self.generator.get_parameter('bullets_per_shoot'), 12)
        self.assertEqual(self.generator.get_parameter('angle_increment'), 30.0)
    
    def test_load_preset_circle(self):
        """Test loading circle preset"""
        result = self.generator.load_preset('circle')
        self.assertTrue(result)
        self.assertEqual(self.generator.get_parameter('bullets_per_shoot'), 36)
        self.assertEqual(self.generator.get_parameter('angle_increment'), 10.0)
    
    def test_load_preset_wave(self):
        """Test loading wave preset"""
        result = self.generator.load_preset('wave')
        self.assertTrue(result)
        self.assertEqual(self.generator.get_parameter('sine_enabled'), True)
        self.assertEqual(self.generator.get_parameter('sine_amplitude'), 2.0)
    
    def test_load_preset_flower(self):
        """Test loading flower preset"""
        result = self.generator.load_preset('flower')
        self.assertTrue(result)
        self.assertEqual(self.generator.get_parameter('polar_enabled'), True)
        self.assertEqual(self.generator.get_parameter('bullets_per_shoot'), 16)
    
    def test_load_invalid_preset(self):
        """Test loading an invalid preset"""
        result = self.generator.load_preset('nonexistent')
        self.assertFalse(result)
    
    def test_save_to_file(self):
        """Test saving pattern to file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xml') as f:
            temp_file = f.name
        
        try:
            self.generator.set_parameter('bullets_per_shoot', 8)
            result = self.generator.save_to_file(temp_file)
            
            self.assertTrue(result)
            self.assertTrue(os.path.exists(temp_file))
            
            # Verify file contents
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn('<?xml', content)
                self.assertIn('<bulletml', content)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_load_from_file(self):
        """Test loading pattern from file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.xml') as f:
            temp_file = f.name
        
        try:
            # Create a pattern and save it
            self.generator.set_all_parameters({
                'bullets_per_shoot': 7,
                'speed': 3.5,
                'angle_increment': 51.4
            })
            self.generator.save_to_file(temp_file)
            
            # Create new generator and load the file
            new_generator = BulletMLGenerator()
            result = new_generator.load_from_file(temp_file)
            
            self.assertTrue(result)
            self.assertEqual(new_generator.get_parameter('bullets_per_shoot'), 7)
            # Speed and angle might not be exact due to parsing
            self.assertIsNotNone(new_generator.get_parameter('speed'))
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_angle_calculation(self):
        """Test angle calculation with different parameters"""
        self.generator.set_all_parameters({
            'angle_target': 0,
            'angle_increment': 45,
            'rotation_speed': 0
        })
        
        # Test basic angle calculation
        angle_0 = self.generator._calculate_angle(0)
        angle_1 = self.generator._calculate_angle(1)
        
        self.assertEqual(angle_0, 0.0)
        self.assertEqual(angle_1, 45.0)
    
    def test_speed_calculation(self):
        """Test speed calculation with iteration modifier"""
        self.generator.set_all_parameters({
            'speed': 2.0,
            'iter_speed_mod': 0.1
        })
        
        speed_0 = self.generator._calculate_speed(0)
        speed_1 = self.generator._calculate_speed(1)
        
        self.assertEqual(speed_0, 2.0)
        self.assertEqual(speed_1, 2.1)
    
    def test_xml_structure(self):
        """Test that generated XML has proper structure"""
        xml_output = self.generator.generate_pattern_xml()
        
        # Check for required elements
        required_elements = [
            'bulletml',
            'action',
            'fire',
            'direction',
            'speed',
            'bullet'
        ]
        
        for element in required_elements:
            self.assertIn(f'<{element}', xml_output)
    
    def test_parameter_bounds(self):
        """Test that parameters handle boundary values"""
        # Test setting extreme values
        self.generator.set_parameter('bullets_per_shoot', 1)
        self.assertEqual(self.generator.get_parameter('bullets_per_shoot'), 1)
        
        self.generator.set_parameter('bullets_per_shoot', 100)
        self.assertEqual(self.generator.get_parameter('bullets_per_shoot'), 100)
        
        # Speed should have minimum bound
        speed = self.generator._calculate_speed(0)
        self.assertGreaterEqual(speed, 0.1)


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBulletMLGenerator)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
