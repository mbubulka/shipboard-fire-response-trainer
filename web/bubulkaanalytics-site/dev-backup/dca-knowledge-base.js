/**
 * DCA (Damage Control Assistant) Knowledge Base
 * Comprehensive training data for AI system
 */

const DCA_KNOWLEDGE_BASE = {
    
    // Core DCA Responsibilities
    primary_duties: {
        "fire_response": {
            description: "Lead damage control efforts during fire emergencies",
            responsibilities: [
                "Assess fire conditions and determine appropriate response",
                "Coordinate with FEDFIRE and ship's fire party",
                "Ensure proper ventilation and smoke removal",
                "Monitor structural integrity during firefighting",
                "Communicate with bridge and engineering spaces"
            ]
        },
        "crew_safety": {
            description: "Ensure safety of all personnel during emergencies",
            responsibilities: [
                "Account for all personnel in affected areas",
                "Coordinate evacuation procedures when necessary",
                "Ensure proper use of firefighting equipment",
                "Monitor crew for heat exhaustion and smoke inhalation",
                "Coordinate with medical personnel as needed"
            ]
        },
        "damage_assessment": {
            description: "Evaluate and report damage to ship systems",
            responsibilities: [
                "Assess fire damage to ship structure and systems",
                "Report damage status to commanding officer",
                "Coordinate repair efforts with ship's force",
                "Monitor for secondary hazards",
                "Document damage for future reference"
            ]
        }
    },

    // Fire Response Procedures
    fire_procedures: {
        "initial_response": [
            "Sound fire alarm and notify bridge",
            "Assess fire type and location", 
            "Secure ventilation to affected space",
            "Establish communications with FEDFIRE",
            "Deploy appropriate firefighting agents"
        ],
        "jp5_fuel_fires": [
            "Use AFFF (Aqueous Film Forming Foam)",
            "Secure fuel supply if possible",
            "Cool surrounding bulkheads",
            "Monitor for vapor accumulation",
            "Prepare for reflash potential"
        ],
        "electrical_fires": [
            "Secure electrical power to affected circuits",
            "Use CO2 or PKP extinguishing agents",
            "Ensure electrical isolation before water use",
            "Coordinate with ship's electricians",
            "Monitor for system restoration requirements"
        ],
        "class_k_fires": [
            "Use wet chemical suppression systems",
            "Secure galley equipment power",
            "Cool surrounding areas",
            "Ensure adequate ventilation",
            "Coordinate with culinary specialists"
        ]
    },

    // Communication Protocols
    communication: {
        "reporting_hierarchy": [
            "Bridge (Officer of the Deck)",
            "Engineering Officer of the Watch",
            "Command Duty Officer",
            "Commanding Officer",
            "Shore-based emergency services if required"
        ],
        "required_reports": [
            "Fire location and type",
            "Personnel accountability",
            "Firefighting efforts underway",
            "Damage assessment",
            "Additional resource requirements"
        ]
    },

    // Equipment and Systems
    equipment: {
        "firefighting_agents": {
            "AFFF": "Aqueous Film Forming Foam - Class B fires",
            "PKP": "Purple K Powder - Electrical/chemical fires", 
            "CO2": "Carbon Dioxide - Electrical fires, confined spaces",
            "Water": "Class A fires, cooling",
            "Wet_Chemical": "Class K fires (cooking oils/fats)"
        },
        "detection_systems": [
            "Smoke detectors",
            "Heat detectors", 
            "Fire alarm panels",
            "FEDFIRE communication systems",
            "Damage control communication circuits"
        ]
    },

    // Common Scenarios and Responses
    scenario_responses: {
        "engine_room_fire": {
            "immediate_actions": [
                "Sound fire alarm",
                "Secure ventilation",
                "Notify EOOW",
                "Deploy FEDFIRE team",
                "Assess fire type and size"
            ],
            "considerations": [
                "Fuel systems proximity",
                "High temperature environment",
                "Machinery protection",
                "Electrical hazards",
                "Confined space challenges"
            ]
        },
        "berthing_fire": {
            "immediate_actions": [
                "Account for all personnel",
                "Secure electrical power",
                "Establish evacuation route",
                "Deploy appropriate agents",
                "Monitor for smoke spread"
            ],
            "considerations": [
                "Personnel safety priority",
                "Smoke toxicity",
                "Escape route maintenance",
                "Personal property protection",
                "Ventilation control"
            ]
        }
    }
};

// Multiple Choice Questions Database
const DCA_QUESTIONS = {
    "fire_response_basics": [
        {
            id: "fr_001",
            scenario: "Engine room JP-5 fuel fire reported by EOOW",
            question: "What is your FIRST action as DCA upon receiving this report?",
            options: [
                "Deploy FEDFIRE team immediately",
                "Sound general alarm and notify bridge", 
                "Secure ventilation to engine room",
                "Proceed to engine room to assess situation"
            ],
            correct: 1,
            explanation: "Bridge notification and general alarm are required first to ensure proper command awareness and crew response.",
            nstm_reference: "NSTM 555-24.3.1"
        },
        {
            id: "fr_002", 
            scenario: "Electrical fire in berthing compartment with personnel trapped",
            question: "Which firefighting agent should NOT be used initially?",
            options: [
                "CO2 extinguisher",
                "PKP (Purple K Powder)",
                "Water or AFFF",
                "Halon (if available)"
            ],
            correct: 2,
            explanation: "Water conducts electricity and poses electrocution risk until power is secured to the affected circuits.",
            nstm_reference: "NSTM 555-24.4.2"
        }
    ],
    "crew_safety": [
        {
            id: "cs_001",
            scenario: "Heavy smoke conditions in mess decks during galley fire",
            question: "What is the DCA's primary concern for crew safety?",
            options: [
                "Immediate fire suppression",
                "Personnel accountability and evacuation",
                "Ventilation restoration", 
                "Equipment protection"
            ],
            correct: 1,
            explanation: "Personnel safety and accountability is always the first priority in any emergency situation.",
            nstm_reference: "NSTM 555-24.2.1"
        }
    ],
    "damage_assessment": [
        {
            id: "da_001",
            scenario: "Fire extinguished in main engine room, visible damage to electrical panels",
            question: "What should the DCA prioritize in damage assessment?",
            options: [
                "Cosmetic damage documentation",
                "Safety hazards and system operability",
                "Cost estimation for repairs",
                "Insurance claim preparation"
            ],
            correct: 1,
            explanation: "Safety hazards and critical system operability must be assessed first to ensure continued safe operation.",
            nstm_reference: "NSTM 555-24.6.1"
        }
    ]
};

// Scoring and Assessment Logic
const DCA_ASSESSMENT = {
    scoring: {
        "excellent": { min: 90, feedback: "Outstanding DCA knowledge demonstrated" },
        "good": { min: 80, feedback: "Solid understanding of DCA responsibilities" },
        "satisfactory": { min: 70, feedback: "Adequate knowledge, continue studying" },
        "needs_improvement": { min: 60, feedback: "Additional training required" },
        "unsatisfactory": { min: 0, feedback: "Comprehensive retraining needed" }
    },
    
    knowledge_areas: [
        "Fire Response Procedures",
        "Crew Safety Management", 
        "Damage Assessment",
        "Communication Protocols",
        "Equipment Operation",
        "NSTM Compliance"
    ]
};

export { DCA_KNOWLEDGE_BASE, DCA_QUESTIONS, DCA_ASSESSMENT };
