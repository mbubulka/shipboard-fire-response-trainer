// DCA Evaluation API for Netlify Functions
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

// Simple in-memory DCA response evaluator for web deployment
class WebDCAEvaluator {
    constructor() {
        this.scenarioWeights = {
            "Initial Response": { speed: 0.3, protocol: 0.5, safety: 0.2 },
            "Investigation Phase": { speed: 0.2, protocol: 0.4, safety: 0.4 },
            "Fire Attack": { speed: 0.4, protocol: 0.3, safety: 0.3 },
            "Containment": { speed: 0.2, protocol: 0.3, safety: 0.5 },
            "Overhaul": { speed: 0.1, protocol: 0.4, safety: 0.5 }
        };
    }

    evaluateResponse(scenario, responseData, context) {
        // Calculate time score (faster is better, but not too fast)
        const timeScore = this.calculateTimeScore(responseData.response_time_ms);
        
        // Protocol score based on correctness
        const protocolScore = responseData.correct ? 1.0 : 0.0;
        
        // Safety score based on scenario type
        const safetyScore = this.calculateSafetyScore(scenario, responseData);
        
        // Get scenario weights
        const weights = this.scenarioWeights[scenario] || { speed: 0.3, protocol: 0.4, safety: 0.3 };
        
        // Calculate weighted total score
        const totalScore = (
            weights.speed * timeScore +
            weights.protocol * protocolScore +
            weights.safety * safetyScore
        );
        
        // Calculate confidence based on score distribution
        const scores = [timeScore, protocolScore, safetyScore];
        const confidence = 1.0 - (Math.max(...scores) - Math.min(...scores)) / 2;
        
        // Generate feedback
        const feedback = this.generateFeedback(scenario, totalScore, timeScore, protocolScore, safetyScore);
        
        return {
            score: Math.round(totalScore * 100) / 100,
            confidence: Math.round(confidence * 100) / 100,
            feedback: feedback,
            details: {
                time_score: Math.round(timeScore * 100) / 100,
                protocol_score: Math.round(protocolScore * 100) / 100,
                safety_score: Math.round(safetyScore * 100) / 100
            }
        };
    }

    calculateTimeScore(responseTimeMs) {
        // Optimal response time is between 3-8 seconds
        const responseTimeSec = responseTimeMs / 1000;
        if (responseTimeSec < 2) return 0.6; // Too fast, might be guessing
        if (responseTimeSec <= 5) return 1.0; // Optimal
        if (responseTimeSec <= 10) return 0.8; // Good
        if (responseTimeSec <= 20) return 0.6; // Acceptable
        return 0.3; // Too slow
    }

    calculateSafetyScore(scenario, responseData) {
        // Basic safety scoring based on scenario type
        const baseScore = responseData.correct ? 0.9 : 0.3;
        
        // Adjust based on scenario
        if (scenario.includes("Safety") || scenario.includes("Emergency")) {
            return baseScore * 1.1; // Safety scenarios are more critical
        }
        
        return baseScore;
    }

    generateFeedback(scenario, totalScore, timeScore, protocolScore, safetyScore) {
        let feedback = [];
        
        if (totalScore >= 0.8) {
            feedback.push("Excellent response! You demonstrated strong decision-making skills.");
        } else if (totalScore >= 0.6) {
            feedback.push("Good response with room for improvement.");
        } else {
            feedback.push("Consider reviewing the procedures for this scenario.");
        }
        
        if (timeScore < 0.5) {
            if (timeScore < 0.4) {
                feedback.push("Take more time to consider your options.");
            } else {
                feedback.push("Response time could be optimized.");
            }
        }
        
        if (protocolScore < 0.5) {
            feedback.push("Review the standard operating procedures for this situation.");
        }
        
        if (safetyScore < 0.7) {
            feedback.push("Consider the safety implications of your decision.");
        }
        
        return feedback.join(" ");
    }
}

exports.handler = async (event, context) => {
    // Set CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    };

    // Handle preflight requests
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: ''
        };
    }

    // Only allow POST requests
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        // Parse the incoming request
        const data = JSON.parse(event.body);
        
        // Validate required fields
        if (!data.scenario || !data.question || !data.selected_response) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ 
                    error: 'Missing required fields: scenario, question, selected_response' 
                })
            };
        }

        // Create evaluator and process response
        const evaluator = new WebDCAEvaluator();
        
        // Simulate response data structure
        const responseData = {
            response_time_ms: data.response_time_ms || 5000,
            correct: data.is_correct || false
        };

        const evaluation = evaluator.evaluateResponse(
            data.scenario,
            responseData,
            data.context || {}
        );

        // Return the evaluation
        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                success: true,
                evaluation: evaluation,
                timestamp: new Date().toISOString()
            })
        };

    } catch (error) {
        console.error('Error processing DCA evaluation:', error);
        
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ 
                success: false,
                error: 'Internal server error',
                message: error.message 
            })
        };
    }
};
