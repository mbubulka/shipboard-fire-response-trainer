"""
DCA Scenario States and Decision Consequences
"""
from typing import Dict, List, Optional
import json


class FireState:
    def __init__(self, location: str, intensity: str, spread_risk: float):
        self.location = location
        self.intensity = intensity  # light, moderate, severe
        self.spread_risk = spread_risk  # 0.0 to 1.0
        self.contained = False
        self.affected_compartments = [location]
        self.smoke_spread: List[str] = []
        self.class_: str = "unknown"  # A, B, C, D, K
        self.phase: str = "detection"  # detection, investigation, attack, containment, overhaul
        self.materials: List[str] = []

    def update_based_on_action(self, action: str) -> Dict:
        """Update fire state based on action taken"""
        consequences = {
            "state_changes": [],
            "new_risks": [],
            "effectiveness": 0.0
        }

        # Class A Fire Responses
        if self.class_ == "A":
            if "water" in action.lower():
                consequences["effectiveness"] = 0.9
                consequences["state_changes"].append(
                    "Water effectively cooling and extinguishing Class A materials"
                )
            elif "PKP" in action:
                consequences["effectiveness"] = 0.6
                consequences["state_changes"].append(
                    "PKP provides some control but water needed for deep-seated fire"
                )

        # Class B Fire Responses
        elif self.class_ == "B":
            if "AFFF" in action:
                consequences["effectiveness"] = 0.9
                consequences["state_changes"].append(
                    "AFFF effectively smothering liquid fuel fire"
                )
            elif "water" in action.lower():
                consequences["effectiveness"] = 0.2
                consequences["state_changes"].append(
                    "Water spreading fuel fire!"
                )
                consequences["new_risks"].append("Fire spread risk increased")

        # Class C Fire Responses
        elif self.class_ == "C":
            if "power" in action.lower():
                consequences["effectiveness"] = 0.8
                consequences["state_changes"].append(
                    "Power secured, electrical hazard reduced"
                )
            elif "water" in action.lower():
                consequences["effectiveness"] = 0.1
                consequences["state_changes"].append(
                    "Water creating electrical hazards!"
                )
                consequences["new_risks"].append("Electrocution risk")

        # Class D Fire Responses
        elif self.class_ == "D":
            if "Met-L-X" in action:
                consequences["effectiveness"] = 0.9
                consequences["state_changes"].append(
                    "Met-L-X effectively controlling metal fire"
                )
            elif "water" in action.lower():
                consequences["effectiveness"] = 0.0
                consequences["state_changes"].append(
                    "Water reacting violently with metal fire!"
                )
                consequences["new_risks"].extend([
                    "Explosion risk",
                    "Chemical reaction"
                ])

        # Class K Fire Responses
        elif self.class_ == "K":
            if "Class K" in action or "Ansul" in action:
                consequences["effectiveness"] = 0.9
                consequences["state_changes"].append(
                    "Special agent effectively smothering cooking fire"
                )
            elif "water" in action.lower():
                consequences["effectiveness"] = 0.1
                consequences["state_changes"].append(
                    "Water spreading burning oil!"
                )
                consequences["new_risks"].append("Oil fire spread")
        
        # Update phase based on effectiveness
        if consequences["effectiveness"] >= 0.7:
            next_phase = self._get_next_phase()
            if next_phase:
                self.phase = next_phase
                consequences["state_changes"].append(
                    f"Fire response effective - progressing to {next_phase} phase"
                )
        if consequences["effectiveness"] < 0.6 and not self.contained:
            self._handle_fire_spread()
            
        return consequences

    def _handle_fire_spread(self):
        """Handle fire spread to adjacent compartments"""
        if self.spread_risk > 0.7:
            # High risk of spread
            if "engine room" in self.location.lower():
                self.affected_compartments.append("Adjacent Machinery Space")
                self.smoke_spread.extend([
                    "Forward Passageway",
                    "Ventilation System"
                ])
            elif "electrical" in self.location.lower():
                self.affected_compartments.append("Adjacent Panel")
                self.smoke_spread.append("Overhead Cable Run")


class DCAScenarioState:
    def __init__(self, 
                 scenario_id: str,
                 description: str, 
                 initial_state: Dict,
                 options: List[str]):
        self.scenario_id = scenario_id
        self.description = description
        self.fire_state = FireState(
            initial_state["location"],
            initial_state["intensity"],
            initial_state["spread_risk"]
        )
        # Set fire class and phase
        self.fire_state.class_ = initial_state.get("class", "unknown")
        self.fire_state.phase = initial_state.get("phase", "detection")
        self.fire_state.materials = initial_state.get("materials", [])
        
        self.options = options
        self.selected_action: Optional[str] = None
        self.consequences: Optional[Dict] = None


class DCAAssessmentManager:
    def __init__(self):
        """Initialize the assessment manager with predefined scenarios"""
        # Initialize base scenarios
        self.scenarios = []
        self.current_index = 0
        self.response_history: List[Dict] = []
        self.current_fire_class = None  # Track current fire progression
        
        # Class A Fire - Berthing Space Progression
        self.add_scenario(
            "CLASS_A_DETECTION",
            "[After Hours - 0215] Smoke detector activation in Forward Berthing, Frame 64. "
            "Duty section reports light smoke visible under door with multiple racks occupied. "
            "Fire Marshal en route from quarterdeck.",
            {
                "location": "Forward Berthing",
                "intensity": "light",
                "spread_risk": 0.3,
                "class": "A",
                "phase": "detection",
                "materials": ["unknown"],
                "time_of_day": "after_hours"
            },
            [
                "Sound General Quarters",
                "Send investigator",
                "Activate sprinkler system",
                "Break out fire hoses"
            ]
        )

        self.add_scenario(
            "CLASS_A_INVESTIGATION",
            "[After Hours - 0217] Investigation team at scene reports mattress fire in Rack 15, "
            "upper level. Moderate smoke banking down from overhead, approximately 4 feet. "
            "Two sailors with minor smoke exposure being evaluated.",
            {
                "location": "Forward Berthing",
                "intensity": "moderate",
                "spread_risk": 0.5,
                "class": "A",
                "phase": "investigation",
                "materials": ["bedding", "furniture"],
                "time_of_day": "after_hours"
            },
            [
                "Set fire boundaries",
                "Deploy attack team",
                "Start ventilation",
                "Alert medical"
            ]
        )

        self.add_scenario(
            "CLASS_A_ATTACK",
            "[After Hours - 0220] Attack team reports mattress and adjacent rack fully involved. "
            "Heavy black smoke to deck, high heat conditions. Adjacent racks beginning to smolder. "
            "Limited visibility, multiple SCBA teams needed. All hands in vicinity evacuated.",
            {
                "location": "Forward Berthing",
                "intensity": "severe",
                "spread_risk": 0.7,
                "class": "A",
                "phase": "attack",
                "materials": ["bedding", "furniture", "paint"]
            },
            [
                "Attack with straight stream",
                "Attack with fog pattern",
                "Back out and regroup",
                "Switch to PKP"
            ]
        )

        self.add_scenario(
            "CLASS_A_CONTAINMENT",
            "Fire knocked down but deep-seated burning in mattress. Smoke clearing.",
            {
                "location": "Forward Berthing",
                "intensity": "moderate",
                "spread_risk": 0.4,
                "class": "A",
                "phase": "containment",
                "materials": ["bedding"]
            },
            [
                "Continue water application",
                "Remove mattress",
                "Check for extension",
                "Begin ventilation"
            ]
        )

        self.add_scenario(
            "CLASS_A_OVERHAUL",
            "Main fire out. Hot spots remain in bedding and nearby materials.",
            {
                "location": "Forward Berthing",
                "intensity": "light",
                "spread_risk": 0.2,
                "class": "A",
                "phase": "overhaul",
                "materials": ["bedding", "furniture"]
            },
            [
                "Pull apart and wet down",
                "Set reflash watch",
                "Begin dewatering",
                "Secure from GQ"
            ]
        )

        # Class B Fire - Engine Room Progression
        self.add_scenario(
            "CLASS_B_DETECTION",
            "[Working Hours - 1345] Machinery Room 1 reports unusual fuel oil smell "
            "near Main Engine #2. Engineering watch investigating source. Normal "
            "operations in progress with full watch team on station.",
            {
                "location": "Main Engine Room",
                "intensity": "light",
                "spread_risk": 0.4,
                "class": "B",
                "phase": "detection",
                "materials": ["unknown"],
                "time_of_day": "working_hours"
            },
            [
                "Sound GQ",
                "Send investigator",
                "Secure fuel transfer",
                "Activate AFFF system"
            ]
        )

        self.add_scenario(
            "CLASS_B_INVESTIGATION",
            "[Working Hours - 1347] Investigation confirms high-pressure fuel oil "
            "spray from ME#2 supply line with atomized mist near hot surfaces. "
            "Multiple fuel oil pressure gauges showing abnormal readings.",
            {
                "location": "Main Engine Room",
                "intensity": "moderate",
                "spread_risk": 0.6,
                "class": "B",
                "phase": "investigation",
                "materials": ["fuel oil"],
                "time_of_day": "working_hours"
            },
            [
                "Secure affected engine",
                "Deploy AFFF team",
                "Set fire boundaries",
                "Start ventilation"
            ]
        )

        self.add_scenario(
            "CLASS_B_ATTACK",
            "[Working Hours - 1349] Fuel spray ignites on exhaust manifold, creating "
            "intense Class B fire. Heavy black smoke banking down. High-pressure "
            "fuel spray continuing to atomize. Two engineering casualties reported.",
            {
                "location": "Main Engine Room",
                "intensity": "severe",
                "spread_risk": 0.8,
                "class": "B",
                "phase": "attack",
                "materials": ["fuel oil", "lubricating oil"],
                "time_of_day": "working_hours"
            },
            [
                "Activate installed AFFF",
                "Deploy AFFF hose team",
                "Use installed CO2",
                "Deploy PKP team"
            ]
        )

        self.add_scenario(
            "CLASS_B_CONTAINMENT",
            "[Working Hours - 1355] Primary fire knocked down by AFFF. Residual fuel "
            "burning in bilge near Frame 110. Ventilation restored. Medical treating "
            "two engineers for minor burns and smoke inhalation.",
            {
                "location": "Main Engine Room",
                "intensity": "moderate",
                "spread_risk": 0.5,
                "class": "B",
                "phase": "containment",
                "materials": ["fuel oil"],
                "time_of_day": "working_hours"
            },
            [
                "Apply AFFF to bilge",
                "Start dewatering",
                "Check for hotspots",
                "Begin cleanup"
            ]
        )

        self.add_scenario(
            "CLASS_B_OVERHAUL",
            "[Working Hours - 1410] Main fire extinguished. Oil-soaked lagging still "
            "smoking near fuel manifold. AFFF blanket maintained. Engineering Officer "
            "assessing damage to ME#2 fuel system.",
            {
                "location": "Main Engine Room",
                "intensity": "light",
                "spread_risk": 0.3,
                "class": "B",
                "phase": "overhaul",
                "materials": ["fuel oil", "lagging"]
            },
            [
                "Remove soaked lagging",
                "Continue ventilation",
                "Monitor temperatures",
                "Set reflash watch"
            ]
        )

        # Class C Fire - Electrical Space Progression
        self.add_scenario(
            "CLASS_C_DETECTION",
            "[Working Hours - 0945] IC Switchboard 2A abnormal.\n"
            "Electrical PO reports burning smell and unusual sounds.\n"
            "Critical radar systems on affected circuit.",
            {
                "location": "IC Room",
                "intensity": "light",
                "spread_risk": 0.3,
                "class": "C",
                "phase": "detection",
                "materials": ["unknown"],
                "time_of_day": "working_hours"
            },
            [
                "Sound GQ",
                "Send electrician to investigate",
                "Prepare to shift power",
                "Ready PKP extinguishers"
            ]
        )

        self.add_scenario(
            "CLASS_C_INVESTIGATION",
            "[Working Hours - 0947] Investigation reveals arcing and smoke from "
            "circuit breaker panel B4. Multiple breakers tripping. Temperature "
            "reading on panel surface is 425°F. Acrid smell intensifying.",
            {
                "location": "IC Room",
                "intensity": "moderate",
                "spread_risk": 0.5,
                "class": "C",
                "phase": "investigation",
                "materials": ["electrical equipment"],
                "time_of_day": "working_hours"
            },
            [
                "Secure power to switchboard",
                "Deploy PKP team",
                "Set fire boundaries",
                "Begin smoke removal"
            ]
        )

        self.add_scenario(
            "CLASS_C_ATTACK",
            "[Working Hours - 0949] Electrical fire in switchboard.\n"
            "Intense arcing. Heavy smoke with electrical component odor.\n"
            "Adjacent cables smoldering. Radar systems lost power.",
            {
                "location": "IC Room",
                "intensity": "severe",
                "spread_risk": 0.7,
                "class": "C",
                "phase": "attack",
                "materials": ["electrical equipment", "cables"],
                "time_of_day": "working_hours"
            },
            [
                "Deploy CO2 extinguisher",
                "Use PKP extinguisher",
                "Deploy backup power",
                "Use water fog (last resort)"
            ]
        )

        self.add_scenario(
            "CLASS_C_CONTAINMENT",
            "[Working Hours - 0955] Main electrical fire controlled. Spot fires in "
            "overhead cable runs being addressed. Electrical safety checks in "
            "progress. Emergency power maintaining critical systems.",
            {
                "location": "IC Room",
                "intensity": "moderate",
                "spread_risk": 0.4,
                "class": "C",
                "phase": "containment",
                "materials": ["electrical equipment"],
                "time_of_day": "working_hours"
            },
            [
                "Continue PKP application",
                "Check adjacent spaces",
                "Monitor circuit readings",
                "Maintain boundaries"
            ]
        )

        self.add_scenario(
            "CLASS_C_OVERHAUL",
            "[Working Hours - 1010] Fire extinguished. Damaged switchboard de-energized. "
            "Thermal imaging shows residual hotspots in cable trays. Electricians "
            "preparing damage assessment. Critical loads on alternate power.",
            {
                "location": "IC Room",
                "intensity": "light",
                "spread_risk": 0.2,
                "class": "C",
                "phase": "overhaul",
                "materials": ["electrical equipment"],
                "time_of_day": "working_hours"
            },
            [
                "Monitor with thermal imaging",
                "Begin damage assessment",
                "Clear smoke from space",
                "Plan power restoration"
            ]
        )

        # Class D Fire - Metal Fire Progression
        self.add_scenario(
            "CLASS_D_DETECTION",
            "[Working Hours - 1530] Machine Shop reports sparks and unusual flame "
            "color from grinding operation on magnesium component. Shop supervisor "
            "clearing space. Standard fire extinguisher nearby.",
            {
                "location": "Machine Shop",
                "intensity": "light",
                "spread_risk": 0.3,
                "class": "D",
                "phase": "detection",
                "materials": ["magnesium"],
                "time_of_day": "working_hours"
            },
            [
                "Sound GQ",
                "Clear the space",
                "Get Met-L-X extinguisher",
                "Use standard extinguisher"
            ]
        )

        self.add_scenario(
            "CLASS_D_INVESTIGATION",
            "[Working Hours - 1532] Investigation confirms Class D metal fire in "
            "magnesium shavings. Fire is bright white with intense heat. Standard "
            "extinguisher discharged with negative effects. Area evacuated.",
            {
                "location": "Machine Shop",
                "intensity": "moderate",
                "spread_risk": 0.5,
                "class": "D",
                "phase": "investigation",
                "materials": ["magnesium"],
                "time_of_day": "working_hours"
            },
            [
                "Apply Met-L-X agent",
                "Use dry sand",
                "Set boundaries",
                "Cool adjacent metal"
            ]
        )

        self.add_scenario(
            "CLASS_D_ATTACK",
            "[Working Hours - 1534] Metal fire intensifying with temperatures exceeding "
            "2000°F. Workbench surface beginning to melt. Intense white flames and "
            "UV radiation. Adjacent flammables threatened.",
            {
                "location": "Machine Shop",
                "intensity": "severe",
                "spread_risk": 0.7,
                "class": "D",
                "phase": "attack",
                "materials": ["magnesium", "metal equipment"],
                "time_of_day": "working_hours"
            },
            [
                "Apply Met-L-X extensively",
                "Use dry sand barrier",
                "Cool surroundings",
                "Deploy water fog"
            ]
        )

        self.add_scenario(
            "CLASS_D_CONTAINMENT",
            "[Working Hours - 1540] Primary metal fire contained with Met-L-X. "
            "Residual material still reacting. Workbench heavily damaged. "
            "Maintaining safe perimeter due to extreme heat.",
            {
                "location": "Machine Shop",
                "intensity": "moderate",
                "spread_risk": 0.4,
                "class": "D",
                "phase": "containment",
                "materials": ["magnesium"],
                "time_of_day": "working_hours"
            },
            [
                "Continue Met-L-X coverage",
                "Monitor temperature",
                "Check structural integrity",
                "Maintain boundaries"
            ]
        )

        self.add_scenario(
            "CLASS_D_OVERHAUL",
            "[Working Hours - 1555] Metal fire fully extinguished. Cooling in progress. "
            "Damage assessment team evaluating structural integrity of space. "
            "DCA reviewing grinding operations procedures.",
            {
                "location": "Machine Shop",
                "intensity": "light",
                "spread_risk": 0.2,
                "class": "D",
                "phase": "overhaul",
                "materials": ["magnesium"],
                "time_of_day": "working_hours"
            },
            [
                "Monitor with thermal imaging",
                "Clean up Met-L-X powder",
                "Document damage",
                "Review safety procedures"
            ]
        )

        # Class K Fire - Galley Fire Progression
        self.add_scenario(
            "CLASS_K_DETECTION",
            "[Working Hours - 1145] Galley watch reports smoke from deep fat fryer. "
            "Oil temperature rising above normal range. Lunch meal preparation in "
            "progress with full galley crew.",
            {
                "location": "Galley",
                "intensity": "light",
                "spread_risk": 0.3,
                "class": "K",
                "phase": "detection",
                "materials": ["cooking oil"],
                "time_of_day": "working_hours"
            },
            [
                "Sound GQ",
                "Secure power to fryer",
                "Activate Ansul system",
                "Use Class K extinguisher"
            ]
        )

        self.add_scenario(
            "CLASS_K_INVESTIGATION",
            "[Working Hours - 1147] Oil temperature critical, light smoke visible "
            "from fryer unit. Thermostat failure confirmed. Grease beginning to "
            "overflow. Galley personnel evacuated.",
            {
                "location": "Galley",
                "intensity": "moderate",
                "spread_risk": 0.5,
                "class": "K",
                "phase": "investigation",
                "materials": ["cooking oil", "grease"],
                "time_of_day": "working_hours"
            },
            [
                "Activate hood suppression",
                "Use Class K extinguisher",
                "Set boundaries",
                "Secure ventilation"
            ]
        )

        self.add_scenario(
            "CLASS_K_ATTACK",
            "[Working Hours - 1148] Deep fat fryer fully involved. Fire extending "
            "into ventilation hood. Heavy smoke with high heat. Grease fire "
            "spreading across cooking surface.",
            {
                "location": "Galley",
                "intensity": "severe",
                "spread_risk": 0.7,
                "class": "K",
                "phase": "attack",
                "materials": ["cooking oil", "grease"],
                "time_of_day": "working_hours"
            },
            [
                "Activate fixed suppression",
                "Deploy multiple K extinguishers",
                "Use PKP backup",
                "Apply water"
            ]
        )

        self.add_scenario(
            "CLASS_K_CONTAINMENT",
            "[Working Hours - 1152] Main fire knocked down by Ansul system. "
            "Residual grease fires in hood system. Ventilation secured. "
            "No injuries reported.",
            {
                "location": "Galley",
                "intensity": "moderate",
                "spread_risk": 0.4,
                "class": "K",
                "phase": "containment",
                "materials": ["cooking oil", "grease"],
                "time_of_day": "working_hours"
            },
            [
                "Apply additional K agent",
                "Check hood system",
                "Monitor temperatures",
                "Maintain boundaries"
            ]
        )

        self.add_scenario(
            "CLASS_K_OVERHAUL",
            "[Working Hours - 1205] Fire fully extinguished. Hood system being "
            "inspected. Ansul system needs recharge. Health inspector notified. "
            "Galley secured pending cleanup.",
            {
                "location": "Galley",
                "intensity": "light",
                "spread_risk": 0.2,
                "class": "K",
                "phase": "overhaul",
                "materials": ["cooking oil", "grease"],
                "time_of_day": "working_hours"
            },
            [
                "Clean suppression agent",
                "Inspect hood system",
                "Document damage",
                "Plan galley restoration"
            ]
        )

        print("Initialized scenarios with progressive phases for all fire classes")
        
    def submit_decision(self, selected_option: int) -> Dict:
        """Submit a decision and get consequences"""
        scenario = self.get_current_scenario()
        if not scenario:
            return {}

        # Record the action taken
        action = scenario.options[selected_option]
        scenario.selected_action = action

        # Calculate consequences
        consequences = scenario.fire_state.update_based_on_action(action)
        scenario.consequences = consequences

        # Store in history
        response_data = {
            'scenario_id': scenario.scenario_id,
            'description': scenario.description,
            'action_taken': action,
            'consequences': consequences,
            'fire_state': {
                'location': scenario.fire_state.location,
                'intensity': scenario.fire_state.intensity,
                'class': scenario.fire_state.class_,
                'phase': scenario.fire_state.phase,
                'contained': scenario.fire_state.contained,
                'affected_compartments': scenario.fire_state.affected_compartments,
                'smoke_spread': scenario.fire_state.smoke_spread
            }
        }
        self.response_history.append(response_data)

        # Check if we should stay on same fire class or move to next
        current_phase = scenario.fire_state.phase
        if not current_phase:
            current_phase = "detection"
            
        next_phase = self._get_next_phase(current_phase)
        
        # Find next scenario in progression
        if next_phase:
            current_class = scenario.fire_state.class_ or "unknown"
            self.current_index = self._find_next_phase_scenario(
                current_class,
                next_phase
            )
        else:
            # Move to next fire class
            self.current_index = self._find_next_fire_class()

        return consequences
    
    def _get_next_phase(self, current_phase: str) -> Optional[str]:
        """Get the next phase in fire progression"""
        phases = [
            "detection", "investigation", "attack", 
            "containment", "overhaul"
        ]
        try:
            current_idx = phases.index(current_phase)
            if current_idx < len(phases) - 1:
                return phases[current_idx + 1]
        except ValueError:
            pass
        return None
    
    def _find_next_phase_scenario(self, fire_class: str, phase: str) -> int:
        """Find the next scenario matching the fire class and phase"""
        for idx, scenario in enumerate(self.scenarios):
            if (scenario.fire_state.class_ == fire_class and 
                    scenario.fire_state.phase == phase):
                return idx
        return self.current_index + 1
    
    def _find_next_fire_class(self) -> int:
        """Find the first scenario of the next fire class"""
        current = self.get_current_scenario()
        if not current:
            return 0
            
        current_class = current.fire_state.class_
        for idx, scenario in enumerate(self.scenarios):
            if (scenario.fire_state.class_ != current_class and 
                scenario.fire_state.phase == "detection"):
                return idx
        return len(self.scenarios)  # End of all scenarios

    def add_scenario(
            self,
            scenario_id: str,
            description: str,
            initial_state: Dict,
            options: List[str]
    ):
        """Helper method to add a new scenario"""
        scenario = DCAScenarioState(
            scenario_id, description, initial_state, options
        )
        self.scenarios.append(scenario)
        print(f"Added scenario: {scenario_id}")

    def get_current_scenario(self) -> Optional[DCAScenarioState]:
        """Get the current scenario if available"""
        print("\nGetting current scenario:")
        print(f"Current index: {self.current_index}")
        print(f"Total scenarios: {len(self.scenarios)}")
        if 0 <= self.current_index < len(self.scenarios):
            scenario = self.scenarios[self.current_index]
            print(f"Found scenario: {scenario.scenario_id}")
            return scenario
        print("No current scenario available")
        return None

    def submit_decision(self, selected_option: int) -> Dict:
        """Submit a decision and get consequences"""
        scenario = self.get_current_scenario()
        if not scenario:
            return {}

        # Record the action taken
        action = scenario.options[selected_option]
        scenario.selected_action = action

        # Calculate consequences
        consequences = scenario.fire_state.update_based_on_action(action)
        scenario.consequences = consequences

        # Store in history
        response_data = {
            'scenario_id': scenario.scenario_id,
            'description': scenario.description,
            'action_taken': action,
            'consequences': consequences,
            'fire_state': {
                'location': scenario.fire_state.location,
                'intensity': scenario.fire_state.intensity,
                'contained': scenario.fire_state.contained,
                'affected_compartments': scenario.fire_state.affected_compartments,
                'smoke_spread': scenario.fire_state.smoke_spread
            }
        }
        self.response_history.append(response_data)

        # Move to next scenario
        self.current_index += 1

        return consequences

    def get_final_results(self) -> Dict:
        """Get final assessment results"""
        overall_effectiveness = sum(
            r['consequences']['effectiveness'] 
            for r in self.response_history
        ) / len(self.response_history)

        total_affected_spaces = sum(
            len(r['fire_state']['affected_compartments']) 
            for r in self.response_history
        )

        containment_success = sum(
            1 for r in self.response_history 
            if r['fire_state']['contained']
        )

        return {
            'scenarios_completed': len(self.response_history),
            'overall_effectiveness': overall_effectiveness,
            'containment_rate': (
                containment_success / len(self.response_history)
            ),
            'total_affected_spaces': total_affected_spaces,
            'response_history': self.response_history
        }

    def save_session(self, filepath: str):
        """Save the current session data to a JSON file"""
        session_data = {
            'response_history': self.response_history,
            'scenarios_completed': self.current_index,
            'results': self.get_final_results()
        }
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)

    @classmethod
    def load_session(cls, filepath: str) -> 'DCAAssessmentManager':
        """Load a session from a JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        manager = cls()
        manager.response_history = data['response_history']
        manager.current_index = data['scenarios_completed']
        return manager
