// Enhanced DCA Knowledge Base with Integrated Training Standards
// Combines NFPA, USCG, and Navy training materials
// Updated with comprehensive multi-source scenarios

const enhancedDCAKnowledgeBase = {
    // Comprehensive training sources
    trainingSources: {
        "nfpa_1500": "NFPA 1500 - Fire Department Occupational Safety and Health Program (2021)",
        "nfpa_1521": "NFPA 1521 - Fire Department Safety Officer Professional Qualifications (2020)", 
        "nfpa_1670": "NFPA 1670 - Operations and Training for Technical Search and Rescue (2017)",
        "uscg_cg022": "USCG CG-022 - Firefighting and Personal Safety Manual",
        "navy_rvss": "Navy RVSS - Recruit Visual Signals School 11th Edition (2021)"
    },

    // Enhanced scenarios with multi-source integration
    integratedScenarios: [
        {
            id: "unified_safety_001",
            title: "CVN SAFETY OFFICER RESPONSE - MAJOR FIRE",
            category: "safety_management",
            sources: ["nfpa_1500", "nfpa_1521", "navy_rvss"],
            description: "Major fire event requiring safety officer coordination, risk assessment, and personnel accountability using naval communication protocols.",
            learningObjectives: [
                "Apply NFPA 1500 safety program principles",
                "Execute NFPA 1521 safety officer procedures", 
                "Implement Navy RVSS communication protocols",
                "Coordinate multi-agency safety response"
            ],
            scenarioDetails: {
                location: "CVN engineering spaces and adjacent compartments",
                conditions: "Major fire, structural compromise, multiple casualties",
                resources: "Ship safety officer, repair parties, medical team, bridge",
                safetyPriorities: "Personnel accountability, exposure assessment, evacuation coordination"
            },
            assessmentCriteria: [
                "NFPA 1500 safety program implementation",
                "NFPA 1521 safety officer decision-making", 
                "Navy communication protocol adherence",
                "Risk assessment accuracy",
                "Personnel accountability maintenance"
            ]
        },
        {
            id: "unified_rescue_001",
            title: "CONFINED SPACE RESCUE - FIRE CASUALTY", 
            category: "technical_rescue",
            sources: ["nfpa_1670", "uscg_cg022", "navy_rvss"],
            description: "Firefighter down in confined engineering space requiring technical rescue with Coast Guard coordination procedures.",
            learningObjectives: [
                "Apply NFPA 1670 technical rescue operations",
                "Implement USCG rescue coordination procedures",
                "Execute Navy confined space protocols", 
                "Coordinate inter-service rescue operations"
            ],
            scenarioDetails: {
                location: "CVN machinery space - confined area",
                conditions: "Firefighter unconscious, toxic atmosphere, structural hazards",
                resources: "Technical rescue team, ship medical, USCG helicopter",
                rescuePriorities: "Immediate life safety, atmospheric monitoring, extraction planning"
            },
            assessmentCriteria: [
                "NFPA 1670 rescue operation procedures",
                "USCG coordination protocol execution",
                "Navy confined space safety compliance",
                "Inter-service communication effectiveness",
                "Medical treatment coordination"
            ]
        },
        {
            id: "unified_marine_001", 
            title: "MULTI-PLATFORM MARINE FIRE RESPONSE",
            category: "marine_operations",
            sources: ["uscg_cg022", "navy_rvss", "nfpa_1500"],
            description: "Fire aboard CVN requiring USCG assistance and multi-platform coordination using standardized marine firefighting procedures.",
            learningObjectives: [
                "Apply USCG marine firefighting procedures",
                "Execute Navy inter-ship communication protocols",
                "Implement NFPA safety standards at sea", 
                "Coordinate multi-platform emergency response"
            ],
            scenarioDetails: {
                location: "CVN flight deck and hangar bay",
                conditions: "Aircraft fire, aviation fuel involvement, sea state 4",
                resources: "CVN fire teams, USCG cutter, helicopter support",
                marineFactors: "Weather conditions, platform coordination, resource sharing"
            },
            assessmentCriteria: [
                "USCG firefighting procedure application",
                "Navy visual signal protocol execution",
                "NFPA safety standard adherence", 
                "Multi-platform coordination effectiveness",
                "Resource allocation optimization"
            ]
        }
    ],

    // Enhanced knowledge areas
    comprehensiveKnowledge: {
        nfpaStandards: {
            nfpa1500: {
                focus: "Occupational safety and health programs",
                keyAreas: [
                    "Risk management procedures",
                    "Personnel safety protocols",
                    "Training program requirements", 
                    "Equipment safety standards",
                    "Medical and fitness requirements"
                ]
            },
            nfpa1521: {
                focus: "Safety officer professional qualifications",
                keyAreas: [
                    "Incident safety officer duties",
                    "Risk assessment procedures",
                    "Safety communication protocols",
                    "Personnel accountability systems",
                    "Post-incident safety analysis"
                ]
            },
            nfpa1670: {
                focus: "Technical search and rescue operations", 
                keyAreas: [
                    "Confined space rescue",
                    "Structural collapse rescue",
                    "Water rescue operations",
                    "Rope rescue techniques",
                    "Medical considerations"
                ]
            }
        },
        militaryStandards: {
            navyRVSS: {
                focus: "Naval visual communications",
                keyAreas: [
                    "Visual signal procedures",
                    "Emergency communication protocols",
                    "Bridge-to-bridge communications",
                    "Damage control signals",
                    "Flight operations coordination"
                ]
            },
            uscgProcedures: {
                focus: "Coast Guard firefighting and safety",
                keyAreas: [
                    "Marine firefighting techniques",
                    "Shipboard safety procedures", 
                    "Inter-agency coordination",
                    "Search and rescue operations",
                    "Maritime emergency response"
                ]
            }
        }
    },

    // Enhanced AI prompts for comprehensive training
    enhancedPrompts: [
        {
            category: "integrated_safety",
            prompt: "You are a CVN Safety Officer trained in NFPA 1500/1521 standards and Navy protocols. A major fire has occurred in the engineering spaces. Explain your safety assessment process and coordination with repair parties using proper Navy terminology.",
            context: "Combines NFPA safety officer standards with Navy operational procedures for comprehensive emergency response."
        },
        {
            category: "technical_rescue", 
            prompt: "As a technical rescue specialist following NFPA 1670 and USCG procedures, describe the rescue plan for a firefighter down in a confined machinery space aboard a naval vessel.",
            context: "Integrates NFPA technical rescue standards with maritime rescue procedures for naval-specific scenarios."
        },
        {
            category: "marine_coordination",
            prompt: "You are coordinating a multi-platform marine fire response using USCG CG-022 procedures and Navy RVSS communication protocols. Explain the coordination process between CVN and USCG assets.",
            context: "Combines Coast Guard maritime firefighting with Navy visual signals for inter-service operations."
        },
        {
            category: "cvn_operations",
            prompt: "As a CVN DCA integrating all training standards (NFPA, USCG, Navy), describe your comprehensive response to a flight deck aviation fuel fire with multiple agencies involved.",
            context: "Unified approach combining civilian fire standards, military procedures, and inter-service coordination."
        }
    ],

    // Method to get random enhanced scenario
    getRandomScenario: function() {
        const scenarios = this.integratedScenarios;
        return scenarios[Math.floor(Math.random() * scenarios.length)];
    },

    // Method to get scenario by category
    getScenarioByCategory: function(category) {
        return this.integratedScenarios.filter(scenario => 
            scenario.category === category
        );
    },

    // Method to get scenarios by source
    getScenariosBySource: function(source) {
        return this.integratedScenarios.filter(scenario =>
            scenario.sources.includes(source)
        );
    }
};

// Export for use in training systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = enhancedDCAKnowledgeBase;
}

console.log("✅ Enhanced DCA Knowledge Base loaded with comprehensive training standards");
console.log(`📚 Integrated ${Object.keys(enhancedDCAKnowledgeBase.trainingSources).length} authoritative sources`);
console.log(`🎯 ${enhancedDCAKnowledgeBase.integratedScenarios.length} comprehensive training scenarios available`);
