/**
 * DCA Feedback Integration System
 * Provides feedback collection and session management for web deployment
 */

class DCAFeedbackIntegration {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.sessionData = {
            id: this.sessionId,
            startTime: Date.now(),
            responses: [],
            feedbackEnabled: true
        };
        this.apiBase = window.location.origin;
    }

    generateSessionId() {
        return 'dca_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    async startDCAFeedbackSession(config) {
        this.sessionData = {
            ...this.sessionData,
            ...config,
            startTime: Date.now()
        };
        
        console.log('🎯 DCA Feedback Session Started:', this.sessionData.id);
        return this.sessionData.id;
    }

    async submitDCAResponse(questionData, selectedResponse, responseTimeMs) {
        const responseData = {
            sessionId: this.sessionData.id,
            timestamp: Date.now(),
            scenario: questionData.scenario,
            question: questionData.question,
            selectedResponse: selectedResponse,
            responseTimeMs: responseTimeMs,
            options: questionData.options,
            correctAnswer: questionData.correct
        };

        // Store locally
        this.sessionData.responses.push(responseData);

        try {
            // Send to API for evaluation
            const response = await fetch(`${this.apiBase}/api/dca-evaluate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    scenario: questionData.scenario || "General",
                    question: questionData.question,
                    selected_response: selectedResponse,
                    response_time_ms: responseTimeMs,
                    is_correct: selectedResponse === questionData.correct,
                    context: {
                        session_id: this.sessionData.id,
                        question_index: this.sessionData.responses.length - 1
                    }
                })
            });

            if (response.ok) {
                const evaluation = await response.json();
                console.log('✅ DCA Response Evaluated:', evaluation);
                return evaluation.evaluation;
            } else {
                console.warn('⚠️ API evaluation failed, using fallback');
                return this.fallbackEvaluation(responseData);
            }
        } catch (error) {
            console.warn('⚠️ Network error, using fallback evaluation:', error);
            return this.fallbackEvaluation(responseData);
        }
    }

    fallbackEvaluation(responseData) {
        const isCorrect = responseData.selectedResponse === responseData.correctAnswer;
        const timeScore = this.calculateTimeScore(responseData.responseTimeMs);
        
        return {
            score: isCorrect ? 0.85 : 0.35,
            confidence: 0.75,
            feedback: isCorrect ? 
                "Good decision! Your response aligns with standard procedures." :
                "Consider reviewing the standard response for this scenario.",
            details: {
                time_score: timeScore,
                protocol_score: isCorrect ? 1.0 : 0.0,
                safety_score: 0.8
            }
        };
    }

    calculateTimeScore(responseTimeMs) {
        const responseTimeSec = responseTimeMs / 1000;
        if (responseTimeSec < 2) return 0.6;
        if (responseTimeSec <= 5) return 1.0;
        if (responseTimeSec <= 10) return 0.8;
        return 0.6;
    }

    async submitSessionFeedback(feedbackData) {
        const sessionSummary = {
            session_id: this.sessionData.id,
            total_responses: this.sessionData.responses.length,
            session_duration: Date.now() - this.sessionData.startTime,
            ...feedbackData
        };

        try {
            const response = await fetch(`${this.apiBase}/api/feedback`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(sessionSummary)
            });

            if (response.ok) {
                console.log('✅ Session feedback submitted successfully');
                return await response.json();
            }
        } catch (error) {
            console.warn('⚠️ Failed to submit session feedback:', error);
        }

        // Store locally as fallback
        localStorage.setItem(`dca_feedback_${this.sessionData.id}`, JSON.stringify(sessionSummary));
        return { success: true, stored_locally: true };
    }

    getSessionSummary() {
        const correctResponses = this.sessionData.responses.filter(r => 
            r.selectedResponse === r.correctAnswer
        ).length;

        return {
            sessionId: this.sessionData.id,
            totalQuestions: this.sessionData.responses.length,
            correctAnswers: correctResponses,
            accuracy: this.sessionData.responses.length > 0 ? 
                correctResponses / this.sessionData.responses.length : 0,
            averageResponseTime: this.sessionData.responses.length > 0 ?
                this.sessionData.responses.reduce((sum, r) => sum + r.responseTimeMs, 0) / this.sessionData.responses.length : 0,
            sessionDuration: Date.now() - this.sessionData.startTime
        };
    }
}

// Initialize global feedback system
window.dcaFeedback = new DCAFeedbackIntegration();

// Export functions for compatibility
window.startDCAFeedbackSession = (config) => window.dcaFeedback.startDCAFeedbackSession(config);
window.submitDCAResponse = (question, response, time) => window.dcaFeedback.submitDCAResponse(question, response, time);
window.submitSessionFeedback = (feedback) => window.dcaFeedback.submitSessionFeedback(feedback);
window.getDCASessionSummary = () => window.dcaFeedback.getSessionSummary();

console.log('🔥 DCA Feedback Integration Loaded');
