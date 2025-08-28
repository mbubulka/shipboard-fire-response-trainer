// DCA Feedback Integration for Website
// Integrates feedback collection into the existing training interface

class DCAFeedbackManager {
    constructor() {
        this.currentSession = null;
        this.currentActionId = null;
        this.feedbackEnabled = true;
        // Connect to Google Sheets Web App
        this.apiBaseUrl = 'https://script.google.com/macros/s/AKfycbzMUER_b0xgAiEaHQMizgN8ll_0DvZbbn_dqDOf6xI3b9HXQbnNH8Fg8vga5tImxAMz/exec';
        this.feedbackQueue = [];
        
        console.log('🔥 DCA Feedback Manager initialized - Connected to feedback system');
        this.startFeedbackSession({ id: 'init_' + Date.now() });
    }

    // Start a new feedback session
    async startFeedbackSession(scenarioData) {
        try {
            // Use form-based submission to avoid CORS preflight
            const formData = new FormData();
            formData.append('session_id', 'session_' + Date.now());
            formData.append('scenario_id', scenarioData.id || 'web_scenario_' + Date.now());
            formData.append('difficulty_rating', '0');
            formData.append('ai_helpfulness', '0');
            formData.append('scenario_realism', '0');
            formData.append('action', 'start_session');

            const response = await fetch(this.apiBaseUrl, {
                method: 'POST',
                mode: 'no-cors', // This prevents CORS errors
                body: formData
            });

            const data = await response.json();
            
            if (data.success) {
                this.currentSession = 'session_' + Date.now();
                console.log(`📊 Feedback session started: ${this.currentSession}`);
                this.showFeedbackNotification('Feedback collection enabled for this assessment');
                return this.currentSession;
            } else {
                console.warn('Failed to start feedback session:', data.error);
                return null;
            }
        } catch (error) {
            console.error('Error starting feedback session:', error);
            return null;
        }
    }

    // Log an assessment action for RL system
    async logAssessmentAction(actionData) {
        if (!this.currentSession) {
            console.warn('No active RL feedback session');
            return null;
        }

        try {
            // Store action data for episode tracking
            this.episodeData.actions.push(actionData.userAction || 0);
            this.episodeData.q_values.push(actionData.q_values || [0.5, 0.3, 0.2, 0.8, 0.4, 0.6, 0.7, 0.1]);
            this.episodeData.rewards.push(actionData.reward || 0);
            this.episodeData.states.push(actionData.state || Array(20).fill(0.5));

            const response = await fetch(`${this.apiBaseUrl}/session/action`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.currentSession,
                    action: actionData.userAction || 0,
                    q_values: actionData.q_values || [0.5, 0.3, 0.2, 0.8, 0.4, 0.6, 0.7, 0.1],
                    reward: actionData.reward || 0,
                    state: actionData.state || Array(20).fill(0.5),
                    user_agreement: actionData.user_agreement,
                    alternative_action: actionData.ai_recommendation,
                    feedback_text: actionData.feedback_text || ''
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.currentActionId = `action_${this.episodeData.actions.length}`;
                console.log(`📝 RL Action logged: ${this.currentActionId}`);
                
                // Show feedback prompt if AI recommendation differs from user action
                if (actionData.ai_recommendation !== actionData.userAction) {
                    this.promptForFeedback(actionData);
                }
                
                return this.currentActionId;
            } else {
                console.warn('Failed to log RL action:', data.error);
                return null;
            }
        } catch (error) {
            console.error('Error logging action:', error);
            return null;
        }
    }

    // Submit user feedback
    async submitFeedback(feedbackData) {
        if (!this.currentSession) {
            console.warn('No active feedback session');
            return false;
        }

        try {
            const response = await fetch(this.apiBaseUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.currentSession,
                    scenario_id: feedbackData.scenario_id || 'scenario_' + Date.now(),
                    difficulty_rating: feedbackData.difficulty_rating || 0,
                    ai_helpfulness: feedbackData.ai_helpfulness || 0,
                    scenario_realism: feedbackData.scenario_realism || 0,
                    confidence_level: feedbackData.confidence_level || 0,
                    training_level: feedbackData.training_level || 'user',
                    what_worked_well: feedbackData.what_worked_well || '',
                    what_was_confusing: feedbackData.what_was_confusing || '',
                    suggested_improvements: feedbackData.suggested_improvements || '',
                    additional_comments: feedbackData.additional_comments || ''
                })
            });

            const data = await response.json();
            
            if (data.success) {
                console.log(`✅ RL Feedback submitted: ${data.feedback_id}`);
                this.showFeedbackThankYou();
                if (data.retraining_triggered) {
                    this.showFeedbackNotification('Your feedback will help retrain the AI model!');
                }
                return true;
            } else {
                console.warn('Failed to submit RL feedback:', data.error);
                return false;
            }
        } catch (error) {
            console.error('Error submitting feedback:', error);
            return false;
        }
    }

    // Calculate success rate based on episode performance
    calculateSuccessRate() {
        if (this.episodeData.rewards.length === 0) return 0.5;
        
        const totalReward = this.episodeData.rewards.reduce((a, b) => a + b, 0);
        const maxPossibleReward = this.episodeData.rewards.length * 5; // Assuming max reward per step is 5
        
        return Math.min(1.0, Math.max(0.0, (totalReward + maxPossibleReward * 0.5) / (maxPossibleReward * 1.5)));
    }

    // Complete the RL feedback session
    async completeFeedbackSession(completionData) {
        if (!this.currentSession) {
            console.warn('No active RL feedback session to complete');
            return false;
        }

        try {
            // Submit final episode feedback
            const episodeFeedback = {
                difficulty_rating: completionData.difficulty_rating || 3,
                ai_helpfulness: completionData.ai_helpfulness || 3,
                scenario_realism: completionData.scenario_realism || 4,
                confidence_level: completionData.confidence_level || 3,
                what_worked_well: completionData.what_worked_well || 'AI provided logical recommendations',
                what_was_confusing: completionData.what_was_confusing || '',
                suggested_improvements: completionData.suggested_improvements || '',
                additional_comments: completionData.additional_comments || ''
            };

            const success = await this.submitFeedback(episodeFeedback);
            
            if (success) {
                console.log(`🎯 RL Feedback session completed: ${this.currentSession}`);
                this.showSessionCompletionFeedback(completionData);
                
                // Reset session data
                this.currentSession = null;
                this.currentActionId = null;
                this.episodeData = { actions: [], q_values: [], rewards: [], states: [] };
                
                return true;
            } else {
                console.warn('Failed to complete RL session');
                return false;
            }
        } catch (error) {
            console.error('Error completing session:', error);
            return false;
        }
    }

    // Test function to manually show feedback modal (for testing purposes)
    showTestFeedbackModal() {
        const testActionData = {
            aiRecommendation: 'Deploy foam system',
            userAction: 'Use water spray',
            qValue: 0.85,
            reward: 0.7,
            context: {
                scenario: 'Engine room fire',
                time_pressure: 'high'
            }
        };
        
        this.promptForFeedback(testActionData);
        console.log('🧪 Test feedback modal displayed');
    }

    // Show feedback prompt when AI recommendation differs from user action
    // Show feedback prompt when AI recommendation differs from user action
    promptForFeedback(actionData) {
        const feedbackModal = this.createFeedbackModal(actionData);
        document.body.appendChild(feedbackModal);
        
        // Show immediately and animate in
        feedbackModal.style.display = 'flex';
        feedbackModal.style.alignItems = 'center';
        feedbackModal.style.justifyContent = 'center';
        
        // Add animation
        const content = feedbackModal.querySelector('.feedback-content');
        content.style.transform = 'scale(0.7)';
        content.style.opacity = '0';
        content.style.transition = 'all 0.3s ease';
        
        setTimeout(() => {
            content.style.transform = 'scale(1)';
            content.style.opacity = '1';
        }, 10);
        
        console.log('💬 Feedback modal displayed for action comparison');
    }

    // Create feedback modal
    createFeedbackModal(actionData) {
        const modal = document.createElement('div');
        modal.className = 'dca-feedback-modal';
        modal.style.cssText = `
            display: none;
            position: fixed;
            z-index: 10000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.7);
            backdrop-filter: blur(2px);
        `;

        modal.innerHTML = `
            <div class="feedback-content" style="
                background-color: #fefefe;
                margin: 10% auto;
                padding: 20px;
                border: none;
                border-radius: 10px;
                width: 80%;
                max-width: 500px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            ">
                <div class="feedback-header" style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 15px;
                ">
                    <h3 style="margin: 0; color: #d32f2f;">🔥 Training Feedback</h3>
                    <span class="close-feedback" style="
                        color: #aaa;
                        font-size: 28px;
                        font-weight: bold;
                        cursor: pointer;
                    ">&times;</span>
                </div>
                
                <div class="feedback-body">
                    <p style="margin-bottom: 15px;">
                        <strong>AI Recommended:</strong> Action ${actionData.aiRecommendation}<br>
                        <strong>You Selected:</strong> Action ${actionData.userAction}<br>
                        ${actionData.qValue ? `<strong>AI Confidence:</strong> ${(actionData.qValue * 100).toFixed(1)}%<br>` : ''}
                        ${actionData.reward !== undefined ? `<strong>Expected Outcome:</strong> ${actionData.reward > 0 ? 'Positive' : actionData.reward < 0 ? 'Negative' : 'Neutral'}<br>` : ''}
                    </p>
                    
                    <p>How would you rate the AI's recommendation?</p>
                    
                    <div class="rating-section" style="margin: 15px 0;">
                        <div class="star-rating" style="font-size: 24px; text-align: center;">
                            <span class="star" data-rating="1">⭐</span>
                            <span class="star" data-rating="2">⭐</span>
                            <span class="star" data-rating="3">⭐</span>
                            <span class="star" data-rating="4">⭐</span>
                            <span class="star" data-rating="5">⭐</span>
                        </div>
                        <div style="text-align: center; margin-top: 5px; font-size: 12px; color: #666;">
                            1 = Poor, 3 = Average, 5 = Excellent
                        </div>
                    </div>
                    
                    <textarea 
                        id="feedback-text" 
                        placeholder="Optional: Tell us why you chose differently or any other feedback..."
                        style="
                            width: 100%;
                            height: 80px;
                            margin: 15px 0;
                            padding: 10px;
                            border: 1px solid #ddd;
                            border-radius: 5px;
                            resize: vertical;
                            font-family: inherit;
                        "
                    ></textarea>
                    
                    <div class="feedback-buttons" style="
                        display: flex;
                        justify-content: space-between;
                        margin-top: 20px;
                    ">
                        <button class="btn-skip" style="
                            background: #6c757d;
                            color: white;
                            border: none;
                            padding: 10px 20px;
                            border-radius: 5px;
                            cursor: pointer;
                        ">Skip</button>
                        
                        <button class="btn-submit" style="
                            background: #d32f2f;
                            color: white;
                            border: none;
                            padding: 10px 20px;
                            border-radius: 5px;
                            cursor: pointer;
                        ">Submit Feedback</button>
                    </div>
                </div>
            </div>
        `;

        // Add event listeners
        const closeBtn = modal.querySelector('.close-feedback');
        const skipBtn = modal.querySelector('.btn-skip');
        const submitBtn = modal.querySelector('.btn-submit');
        const stars = modal.querySelectorAll('.star');
        let selectedRating = 0;

        // Star rating functionality
        stars.forEach(star => {
            star.addEventListener('click', () => {
                selectedRating = parseInt(star.dataset.rating);
                this.updateStarDisplay(stars, selectedRating);
            });
            
            star.addEventListener('mouseover', () => {
                const hoverRating = parseInt(star.dataset.rating);
                this.updateStarDisplay(stars, hoverRating);
            });
        });

        // Close modal functionality
        const closeModal = () => {
            modal.remove();
        };

        closeBtn.addEventListener('click', closeModal);
        skipBtn.addEventListener('click', closeModal);
        
        // Submit feedback
        submitBtn.addEventListener('click', () => {
            const feedbackText = modal.querySelector('#feedback-text').value;
            
            if (selectedRating === 0) {
                alert('Please provide a rating before submitting.');
                return;
            }
            
            this.submitFeedback({
                action_id: actionData.actionId || this.currentSession.actions.length - 1,
                rating: selectedRating,
                feedback_text: feedbackText,
                action_type: 'recommendation_rating',
                action_data: {
                    ai_recommendation: actionData.aiRecommendation,
                    user_action: actionData.userAction,
                    context: actionData.context || {}
                }
            });
            
            closeModal();
        });

        // Click outside to close
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });

        return modal;
    }

    // Update star display
    updateStarDisplay(stars, rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.style.color = '#ffc107';
                star.style.textShadow = '0 0 3px rgba(255, 193, 7, 0.5)';
            } else {
                star.style.color = '#dee2e6';
                star.style.textShadow = 'none';
            }
        });
    }

    // Show feedback notification
    showFeedbackNotification(message) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #c3e6cb;
            z-index: 9999;
            max-width: 300px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        `;
        notification.innerHTML = `
            <strong>📊 Feedback System</strong><br>
            ${message}
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 4000);
    }

    // Show thank you message
    showFeedbackThankYou() {
        const thankYou = document.createElement('div');
        thankYou.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #d1ecf1;
            color: #0c5460;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #bee5eb;
            z-index: 9999;
            max-width: 300px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        `;
        thankYou.innerHTML = `
            <strong>✅ Thank You!</strong><br>
            Your feedback will help improve the AI training system.
        `;

        document.body.appendChild(thankYou);

        setTimeout(() => {
            thankYou.remove();
        }, 3000);
    }

    // Show session completion feedback
    showSessionCompletionFeedback(completionData) {
        const completion = document.createElement('div');
        completion.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #f1b0b7;
            z-index: 9999;
            max-width: 350px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        `;
        completion.innerHTML = `
            <strong>🎯 Assessment Complete</strong><br>
            Score: ${completionData.finalScore || 'N/A'}<br>
            Data collected for model improvement
        `;

        document.body.appendChild(completion);

        setTimeout(() => {
            completion.remove();
        }, 5000);
    }

    // Show episode completion feedback modal
    showEpisodeFeedbackModal(episodeData) {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
        `;

        const successRate = this.calculateSuccessRate();
        const totalActions = this.currentSession.actions.length;

        modal.innerHTML = `
            <div style="
                background: white;
                padding: 30px;
                border-radius: 15px;
                width: 90%;
                max-width: 600px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            ">
                <div class="episode-header" style="
                    text-align: center;
                    margin-bottom: 25px;
                    border-bottom: 2px solid #d32f2f;
                    padding-bottom: 20px;
                ">
                    <h2 style="margin: 0; color: #d32f2f;">🎯 Training Episode Complete</h2>
                </div>
                
                <div class="episode-stats" style="
                    display: grid;
                    grid-template-columns: 1fr 1fr 1fr;
                    gap: 20px;
                    margin-bottom: 25px;
                    text-align: center;
                ">
                    <div style="padding: 15px; background: #f8f9fa; border-radius: 8px;">
                        <div style="font-size: 24px; font-weight: bold; color: #d32f2f;">${totalActions}</div>
                        <div style="font-size: 12px; color: #666;">Actions Taken</div>
                    </div>
                    <div style="padding: 15px; background: #f8f9fa; border-radius: 8px;">
                        <div style="font-size: 24px; font-weight: bold; color: #28a745;">${(successRate * 100).toFixed(1)}%</div>
                        <div style="font-size: 12px; color: #666;">Success Rate</div>
                    </div>
                    <div style="padding: 15px; background: #f8f9fa; border-radius: 8px;">
                        <div style="font-size: 24px; font-weight: bold; color: #007bff;">${episodeData.scenario || 'Standard'}</div>
                        <div style="font-size: 12px; color: #666;">Scenario Type</div>
                    </div>
                </div>
                
                <div class="episode-feedback">
                    <h4 style="margin-bottom: 15px;">How did this training episode go overall?</h4>
                    
                    <div class="episode-rating" style="margin: 20px 0;">
                        <div class="episode-stars" style="font-size: 32px; text-align: center;">
                            <span class="episode-star" data-rating="1">⭐</span>
                            <span class="episode-star" data-rating="2">⭐</span>
                            <span class="episode-star" data-rating="3">⭐</span>
                            <span class="episode-star" data-rating="4">⭐</span>
                            <span class="episode-star" data-rating="5">⭐</span>
                        </div>
                        <div style="text-align: center; margin-top: 10px; font-size: 14px; color: #666;">
                            1 = Poor Training Value, 5 = Excellent Training Value
                        </div>
                    </div>
                    
                    <textarea 
                        id="episode-feedback-text" 
                        placeholder="What worked well? What could be improved? Any suggestions for the AI system?"
                        style="
                            width: 100%;
                            height: 100px;
                            margin: 20px 0;
                            padding: 15px;
                            border: 2px solid #ddd;
                            border-radius: 8px;
                            resize: vertical;
                            font-family: inherit;
                            font-size: 14px;
                        "
                    ></textarea>
                    
                    <div class="episode-buttons" style="
                        display: flex;
                        justify-content: space-between;
                        margin-top: 25px;
                    ">
                        <button class="btn-episode-skip" style="
                            background: #6c757d;
                            color: white;
                            border: none;
                            padding: 12px 25px;
                            border-radius: 8px;
                            cursor: pointer;
                            font-size: 14px;
                        ">Skip Feedback</button>
                        
                        <button class="btn-episode-submit" style="
                            background: #d32f2f;
                            color: white;
                            border: none;
                            padding: 12px 25px;
                            border-radius: 8px;
                            cursor: pointer;
                            font-size: 14px;
                        ">Complete Training</button>
                    </div>
                </div>
            </div>
        `;

        // Add event listeners
        const episodeStars = modal.querySelectorAll('.episode-star');
        const skipBtn = modal.querySelector('.btn-episode-skip');
        const submitBtn = modal.querySelector('.btn-episode-submit');
        let selectedEpisodeRating = 0;

        // Episode star rating functionality
        episodeStars.forEach(star => {
            star.addEventListener('click', () => {
                selectedEpisodeRating = parseInt(star.dataset.rating);
                this.updateStarDisplay(episodeStars, selectedEpisodeRating);
            });
            
            star.addEventListener('mouseover', () => {
                const hoverRating = parseInt(star.dataset.rating);
                this.updateStarDisplay(episodeStars, hoverRating);
            });
        });

        // Close modal functionality
        const closeModal = () => {
            modal.remove();
        };

        skipBtn.addEventListener('click', () => {
            this.completeFeedbackSession();
            closeModal();
        });
        
        // Submit episode feedback
        submitBtn.addEventListener('click', () => {
            const feedbackText = modal.querySelector('#episode-feedback-text').value;
            
            if (selectedEpisodeRating === 0) {
                alert('Please provide a rating before submitting.');
                return;
            }
            
            // Submit episode-level feedback
            this.submitFeedback({
                episode_rating: selectedEpisodeRating,
                feedback_text: feedbackText,
                action_type: 'episode_completion',
                action_data: {
                    total_actions: totalActions,
                    success_rate: successRate,
                    scenario: episodeData.scenario,
                    duration: episodeData.duration,
                    episode_stats: {
                        actions: this.currentSession.actions.length,
                        q_values: this.currentSession.q_values,
                        rewards: this.currentSession.rewards
                    }
                }
            });
            
            this.completeFeedbackSession();
            closeModal();
        });

        // Click outside to close
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.completeFeedbackSession();
                closeModal();
            }
        });

        document.body.appendChild(modal);
        return modal;
    }

    // Get user ID (you can customize this based on your authentication system)
    getUserId() {
        // Try to get from session storage, localStorage, or generate anonymous ID
        let userId = sessionStorage.getItem('dca_user_id') || 
                    localStorage.getItem('dca_user_id');
        
        if (!userId) {
            userId = 'anon_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('dca_user_id', userId);
        }
        
        return userId;
    }

    // Get system status
    async getSystemStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/status`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error checking feedback system status:', error);
            return null;
        }
    }
}

// Global instance
window.dcaFeedbackManager = new DCAFeedbackManager();

// Integration helper functions for existing code
window.startDCAFeedbackSession = (scenarioData) => {
    return window.dcaFeedbackManager.startFeedbackSession(scenarioData);
};

window.logDCAAction = (actionData) => {
    return window.dcaFeedbackManager.logAssessmentAction(actionData);
};

window.completeDCAEpisode = (episodeData) => {
    return window.dcaFeedbackManager.showEpisodeFeedbackModal(episodeData);
};

window.getDCAFeedbackStatus = () => {
    return window.dcaFeedbackManager.getSystemStatus();
};

window.showTestFeedback = () => {
    return window.dcaFeedbackManager.showTestFeedbackModal();
};

window.completeDCAFeedbackSession = (completionData) => {
    return window.dcaFeedbackManager.completeFeedbackSession(completionData);
};

console.log('🔥 DCA Feedback integration loaded - Ready for data collection!');
