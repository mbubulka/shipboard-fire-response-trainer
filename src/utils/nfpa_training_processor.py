#!/usr/bin/env python3
"""
NFPA 1001 Training Data Processor
Extracts and processes NFPA 1001 firefighter qualification standards
for integration into CVN Fire Response Training System
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any

class NFPATrainingProcessor:
    """Process NFPA 1001 data for fire response training"""
    
    def __init__(self, data_dir: str = "d:/projects/website-files/training-data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # NFPA 1001 Key Competency Areas (publicly available structure)
        self.competency_areas = {
            "general_requirements": {
                "description": "General knowledge and skills for firefighters",
                "topics": [
                    "Fire behavior and combustion",
                    "Building construction",
                    "Fire department organization",
                    "Safety procedures and protocols",
                    "Communications and terminology"
                ]
            },
            "fire_suppression": {
                "description": "Fire suppression operations and techniques",
                "topics": [
                    "Hose line operations",
                    "Water supply systems", 
                    "Foam operations",
                    "Ventilation techniques",
                    "Search and rescue operations"
                ]
            },
            "rescue_operations": {
                "description": "Emergency rescue and extrication",
                "topics": [
                    "Vehicle extrication",
                    "Confined space rescue",
                    "Water rescue operations", 
                    "Emergency medical care",
                    "Technical rescue systems"
                ]
            },
            "hazmat_operations": {
                "description": "Hazardous materials response",
                "topics": [
                    "Chemical identification",
                    "Containment procedures",
                    "Decontamination processes",
                    "Personal protective equipment",
                    "Emergency response planning"
                ]
            },
            "marine_firefighting": {
                "description": "Shipboard and marine fire response (CVN specific)",
                "topics": [
                    "Ship systems and layout",
                    "Naval fire suppression systems",
                    "Compartment firefighting",
                    "Damage control procedures",
                    "Aviation fuel fire response"
                ]
            }
        }
    
    def create_training_scenarios(self) -> List[Dict[str, Any]]:
        """Generate NFPA 1001 compliant training scenarios"""
        
        scenarios = []
        
        # Fire Suppression Scenarios
        scenarios.extend([
            {
                "id": "nfpa_fs_001",
                "title": "STRUCTURAL FIRE ATTACK - NFPA 1001 Compliant",
                "category": "fire_suppression",
                "nfpa_reference": "NFPA 1001 - Fire Suppression Operations",
                "description": "Two-story residential structure fire with occupants trapped on second floor. Heavy smoke showing from first floor windows.",
                "learning_objectives": [
                    "Demonstrate proper hose line selection and deployment",
                    "Execute coordinated ventilation operations", 
                    "Perform primary search operations",
                    "Apply NFPA water flow calculations"
                ],
                "scenario_details": {
                    "location": "Two-story single family residence",
                    "conditions": "Heavy smoke, limited visibility, potential flashover conditions",
                    "resources": "Engine company, truck company, rescue squad",
                    "weather": "Clear, 15 mph winds from southwest"
                },
                "assessment_criteria": [
                    "Proper size-up and initial actions",
                    "Appropriate hose line selection (1.75\" vs 2.5\")",
                    "Coordinated ventilation timing",
                    "Search pattern execution",
                    "Water application technique"
                ]
            },
            {
                "id": "nfpa_hm_001", 
                "title": "HAZMAT INCIDENT - CHEMICAL LEAK",
                "category": "hazmat_operations",
                "nfpa_reference": "NFPA 1001 - Hazardous Materials Operations",
                "description": "Unknown chemical leak at industrial facility. Multiple workers reporting respiratory distress.",
                "learning_objectives": [
                    "Demonstrate proper approach and isolation procedures",
                    "Identify hazardous materials using ERG",
                    "Select appropriate PPE levels",
                    "Execute decontamination procedures"
                ],
                "scenario_details": {
                    "location": "Chemical processing plant",
                    "conditions": "Unknown vapor cloud, multiple casualties",
                    "resources": "Hazmat team, EMS units, law enforcement",
                    "weather": "Light winds, potential for vapor spread"
                },
                "assessment_criteria": [
                    "Initial isolation distance establishment",
                    "Proper ERG usage and chemical identification",
                    "PPE selection rationale",
                    "Decontamination setup and execution"
                ]
            }
        ])
        
        # CVN-Specific Marine Firefighting Scenarios
        scenarios.extend([
            {
                "id": "nfpa_marine_001",
                "title": "AIRCRAFT HANGAR FIRE - CVN OPERATIONS",
                "category": "marine_firefighting", 
                "nfpa_reference": "NFPA 1001 + Naval Fire Fighting Standards",
                "description": "Class B fire involving JP-5 aviation fuel in aircraft hangar bay. Aircraft and personnel at risk.",
                "learning_objectives": [
                    "Apply marine firefighting principles per NFPA 1001",
                    "Demonstrate AFFF system operation",
                    "Execute shipboard evacuation procedures",
                    "Coordinate with damage control teams"
                ],
                "scenario_details": {
                    "location": "CVN Aircraft Hangar Bay",
                    "conditions": "JP-5 fuel fire, heavy smoke, confined space",
                    "resources": "Ship's fire party, damage control teams, flight deck crew",
                    "special_considerations": "Sea state, aircraft movement limitations"
                },
                "assessment_criteria": [
                    "Proper foam application technique",
                    "Coordination with ship systems",
                    "Personnel accountability procedures", 
                    "Damage assessment and reporting"
                ]
            }
        ])
        
        return scenarios
    
    def create_knowledge_base(self) -> Dict[str, Any]:
        """Create NFPA 1001 knowledge base for AI training"""
        
        knowledge_base = {
            "standards_reference": "NFPA 1001 - Standard for Fire Fighter Professional Qualifications",
            "version": "2019 Edition",
            "scope": "Professional qualifications for firefighters",
            "competency_areas": self.competency_areas,
            "key_principles": {
                "fire_behavior": [
                    "Fire triangle: heat, fuel, oxygen",
                    "Stages of fire development",
                    "Flashover and backdraft conditions",
                    "Thermal layering in compartments"
                ],
                "safety_principles": [
                    "Risk assessment and management",
                    "Personal protective equipment requirements",
                    "Accountability systems",
                    "Incident command structure"
                ],
                "tactical_operations": [
                    "Size-up procedures",
                    "Attack line selection and deployment",
                    "Ventilation coordination",
                    "Search and rescue priorities"
                ]
            },
            "assessment_methods": [
                "Written examinations",
                "Practical skill demonstrations",
                "Scenario-based evaluations",
                "Competency verification"
            ]
        }
        
        return knowledge_base
    
    def generate_training_prompts(self) -> List[Dict[str, str]]:
        """Generate AI training prompts based on NFPA 1001"""
        
        prompts = [
            {
                "category": "fire_behavior",
                "prompt": "You are a fire training instructor teaching NFPA 1001 fire behavior principles. Explain the fire development process and key warning signs firefighters must recognize.",
                "context": "NFPA 1001 emphasizes understanding fire behavior for firefighter safety and effective suppression operations."
            },
            {
                "category": "tactics",
                "prompt": "As a fire tactics instructor following NFPA 1001 standards, describe the proper size-up process and initial tactical priorities for a structure fire.",
                "context": "NFPA 1001 requires firefighters to demonstrate systematic approach to fire ground operations."
            },
            {
                "category": "safety",
                "prompt": "You are teaching NFPA 1001 safety procedures. Explain the risk management process and when firefighters should transition from offensive to defensive operations.",
                "context": "NFPA 1001 prioritizes firefighter safety through proper risk assessment and decision-making."
            },
            {
                "category": "marine_ops",
                "prompt": "As a naval fire instructor combining NFPA 1001 principles with shipboard operations, explain the unique considerations for firefighting aboard naval vessels.",
                "context": "Naval firefighting applies NFPA 1001 fundamentals adapted for marine environment and ship systems."
            }
        ]
        
        return prompts
    
    def save_training_data(self):
        """Save all training data to files"""
        
        # Save scenarios
        scenarios = self.create_training_scenarios()
        with open(self.data_dir / "nfpa_1001_scenarios.json", 'w') as f:
            json.dump(scenarios, f, indent=2)
        
        # Save knowledge base
        knowledge_base = self.create_knowledge_base()
        with open(self.data_dir / "nfpa_1001_knowledge_base.json", 'w') as f:
            json.dump(knowledge_base, f, indent=2)
        
        # Save training prompts
        prompts = self.generate_training_prompts()
        with open(self.data_dir / "nfpa_1001_prompts.json", 'w') as f:
            json.dump(prompts, f, indent=2)
        
        print("✅ NFPA 1001 training data generated successfully!")
        print(f"📁 Files saved to: {self.data_dir}")
        print(f"📊 Generated {len(scenarios)} training scenarios")
        print(f"📚 Created knowledge base with {len(self.competency_areas)} competency areas")
        print(f"🤖 Prepared {len(prompts)} AI training prompts")

def main():
    """Main processing function"""
    processor = NFPATrainingProcessor()
    processor.save_training_data()
    
    print("\n🎯 Next Steps:")
    print("1. Copy generated JSON files to your website-files directory")
    print("2. Update your training system to use NFPA 1001 scenarios")
    print("3. Enhance AI prompts with NFPA standards knowledge")
    print("4. Test new scenarios in your live training system")

if __name__ == "__main__":
    main()
