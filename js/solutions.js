/**
 * Solutions Page - N-Expert.ai
 * Interactive 3D flip cards and demo modal with webhook/widget support
 */

// ==========================================================================
// AGENT CONFIGURATION
// ==========================================================================
// For each agent, set EITHER webhookUrl OR chatWidgetUrl (not both).
// - webhookUrl:     Your n8n webhook URL (POST). The custom chat UI sends
//                   { message, sessionId, agentId } and expects { response }.
// - chatWidgetUrl:  Your n8n chat widget URL. An iframe is embedded inside
//                   the modal, and n8n handles the full conversation.
// If both are empty, the demo shows a placeholder message.
// ==========================================================================

const AGENT_CONFIG = {
    business: {
        webhookUrl: '',
        chatWidgetUrl: '',
    },
    customer: {
        webhookUrl: '',
        chatWidgetUrl: '',
    },
    sales: {
        webhookUrl: '',
        chatWidgetUrl: '',
    },
    finance: {
        webhookUrl: '',
        chatWidgetUrl: '',
    },
    legal: {
        webhookUrl: '',
        chatWidgetUrl: '',
    }
};

// ==========================================================================
// Session Management
// ==========================================================================

let currentSessionId = null;
let currentAgentId = null;
let conversationStarted = false;

function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substring(2, 9);
}

// ==========================================================================
// Card Flip Functionality
// ==========================================================================

document.addEventListener('DOMContentLoaded', function() {
    initializeFlipCards();
    initializeDemoModal();
});

/**
 * Initialize flip card interactions
 * Cards flip on click, except when clicking the demo button
 */
function initializeFlipCards() {
    var cards = document.querySelectorAll('.bot-card');

    cards.forEach(function(card) {
        card.addEventListener('click', function(e) {
            // Don't flip if clicking the demo button
            if (e.target.closest('.bot-demo-btn')) {
                return;
            }
            this.classList.toggle('flipped');
        });

        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.classList.toggle('flipped');
            }
        });
    });
}

// ==========================================================================
// Demo Modal Functionality
// ==========================================================================

function initializeDemoModal() {
    var modal = document.getElementById('demo-modal');
    var modalClose = document.getElementById('demo-modal-close');
    var demoInput = document.getElementById('demo-input');
    var sendButton = document.getElementById('demo-send');

    if (!modal) return;

    // Open modal from "Try Demo" buttons
    var demoButtons = document.querySelectorAll('.bot-demo-btn');
    demoButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            openDemoModal(this);
        });
    });

    // Close button triggers confirmation
    if (modalClose) {
        modalClose.addEventListener('click', function(e) {
            e.stopPropagation();
            requestCloseModal();
        });
    }

    // Clicking outside does NOT close — intentionally omitted

    // Escape key triggers confirmation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            var confirmOverlay = document.getElementById('confirm-exit-overlay');
            if (confirmOverlay && confirmOverlay.classList.contains('active')) {
                // If confirmation is showing, cancel it
                cancelExitConfirmation();
            } else {
                requestCloseModal();
            }
        }
    });

    // Send message functionality
    if (sendButton && demoInput) {
        sendButton.addEventListener('click', sendDemoMessage);

        demoInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendDemoMessage();
            }
        });
    }

    // Confirmation dialog buttons
    var confirmExitBtn = document.getElementById('confirm-exit-yes');
    var cancelExitBtn = document.getElementById('confirm-exit-no');

    if (confirmExitBtn) {
        confirmExitBtn.addEventListener('click', confirmExitModal);
    }
    if (cancelExitBtn) {
        cancelExitBtn.addEventListener('click', cancelExitConfirmation);
    }
}

// ==========================================================================
// Open Demo Modal
// ==========================================================================

function openDemoModal(button) {
    var modal = document.getElementById('demo-modal');
    var modalIcon = document.getElementById('demo-modal-icon');
    var modalTitle = document.getElementById('demo-modal-title');
    var modalChat = document.getElementById('demo-modal-chat');
    var chatWidget = document.getElementById('demo-chat-widget');
    var chatArea = document.getElementById('demo-chat-area');
    var inputArea = document.getElementById('demo-input-area');
    var demoInput = document.getElementById('demo-input');
    var sendButton = document.getElementById('demo-send');

    var name = button.dataset.name;
    var icon = button.dataset.icon;
    var color = button.dataset.color;
    var agentId = button.dataset.bot;

    currentAgentId = agentId;
    currentSessionId = generateSessionId();
    conversationStarted = false;

    // Set modal header
    modalIcon.style.background = color;
    modalIcon.innerHTML = '<i class="fas ' + icon + '"></i>';
    modalTitle.textContent = name + ' Demo';

    var config = AGENT_CONFIG[agentId] || {};

    // Determine mode: chatWidget, webhook, or placeholder
    if (config.chatWidgetUrl) {
        // --- IFRAME MODE ---
        chatArea.style.display = 'none';
        inputArea.style.display = 'none';
        chatWidget.style.display = 'flex';
        chatWidget.innerHTML = '<iframe src="' + escapeAttr(config.chatWidgetUrl) + '" style="width:100%;height:100%;border:none;border-radius:0 0 16px 16px;" allow="microphone"></iframe>';
        conversationStarted = true;

    } else {
        // --- CUSTOM CHAT MODE (webhook or placeholder) ---
        chatWidget.style.display = 'none';
        chatWidget.innerHTML = '';
        chatArea.style.display = 'flex';
        inputArea.style.display = 'flex';

        var hasWebhook = !!config.webhookUrl;

        // Welcome messages per agent
        var welcomeMessages = {
            'business': 'Hello! I\'m your Business Expert Agent. I can help with client intake, business assessments, scheduling, and general inquiries. How can I assist you today?',
            'customer': 'Hi there! I\'m the Customer Service Expert. I manage inquiries, tickets, escalations, and satisfaction tracking. What do you need help with?',
            'sales': 'Welcome! I\'m the Sales & Marketing Expert. I can qualify leads, automate follow-ups, and optimize your pipeline. How can I help?',
            'finance': 'Hello! I\'m the Finance & Admin Expert. I handle invoicing, expense tracking, financial reports, and compliance. What would you like to know?',
            'legal': 'Greetings! I\'m the Legal Expert Agent, powered by JurisMind\u2122. I assist with contract review, compliance, and legal research. How can I help you?'
        };

        var welcomeMessage = welcomeMessages[agentId] || 'Hello! I\'m the ' + name + '. How can I help you today?';

        modalChat.innerHTML = '<div class="chat-message bot-message"><p>' + welcomeMessage + '</p></div>';

        // Always enable the input so the user can interact
        demoInput.disabled = false;
        sendButton.disabled = false;
        demoInput.placeholder = 'Type a message...';
    }

    // Show modal
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Focus input
    setTimeout(function() {
        if (demoInput && chatArea.style.display !== 'none') {
            demoInput.focus();
        }
    }, 300);
}

// ==========================================================================
// Close Modal with Confirmation
// ==========================================================================

function requestCloseModal() {
    if (conversationStarted) {
        showExitConfirmation();
    } else {
        forceCloseModal();
    }
}

function showExitConfirmation() {
    var overlay = document.getElementById('confirm-exit-overlay');
    if (overlay) {
        overlay.classList.add('active');
    }
}

function cancelExitConfirmation() {
    var overlay = document.getElementById('confirm-exit-overlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
    // Re-focus input
    var demoInput = document.getElementById('demo-input');
    if (demoInput && !demoInput.disabled) {
        demoInput.focus();
    }
}

function confirmExitModal() {
    var overlay = document.getElementById('confirm-exit-overlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
    forceCloseModal();
}

function forceCloseModal() {
    var modal = document.getElementById('demo-modal');
    var chatWidget = document.getElementById('demo-chat-widget');

    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Clean up iframe to stop any ongoing connections
    if (chatWidget) {
        chatWidget.innerHTML = '';
        chatWidget.style.display = 'none';
    }

    currentSessionId = null;
    currentAgentId = null;
    conversationStarted = false;
}

// ==========================================================================
// Send Message (Webhook Mode)
// ==========================================================================

function sendDemoMessage() {
    var demoInput = document.getElementById('demo-input');
    var sendButton = document.getElementById('demo-send');
    var modalChat = document.getElementById('demo-modal-chat');

    if (!demoInput || !demoInput.value.trim()) return;

    var userMessage = demoInput.value.trim();
    var config = AGENT_CONFIG[currentAgentId] || {};
    var hasWebhook = !!config.webhookUrl;

    conversationStarted = true;

    // Add user message to chat
    var userDiv = document.createElement('div');
    userDiv.className = 'chat-message user-message';
    userDiv.innerHTML = '<p>' + escapeHtml(userMessage) + '</p>';
    modalChat.appendChild(userDiv);

    // Clear input and disable while processing
    demoInput.value = '';
    demoInput.disabled = true;
    sendButton.disabled = true;

    // Show typing indicator
    var typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot-message';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
    modalChat.appendChild(typingDiv);
    modalChat.scrollTop = modalChat.scrollHeight;

    if (hasWebhook) {
        // --- LIVE MODE: send to n8n webhook ---
        fetch(config.webhookUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: userMessage,
                sessionId: currentSessionId,
                agentId: currentAgentId
            })
        })
        .then(function(response) {
            if (!response.ok) throw new Error('HTTP ' + response.status);
            return response.json();
        })
        .then(function(data) {
            removeTypingIndicator();

            // Extract response text — supports multiple response formats from n8n
            var responseText = data.response
                || data.output
                || data.text
                || data.message
                || (Array.isArray(data) && data[0] && (data[0].response || data[0].output || data[0].text))
                || 'I received your message but could not generate a response.';

            addBotMessage(formatBotResponse(responseText));
        })
        .catch(function(error) {
            removeTypingIndicator();
            addBotMessage('<span style="color:var(--accent-red);">Connection error. Please verify the webhook URL is active and try again.</span>');
            console.error('Webhook error:', error);
        })
        .finally(function() {
            demoInput.disabled = false;
            sendButton.disabled = false;
            demoInput.focus();
        });

    } else {
        // --- DEMO MODE: simulated responses ---
        var demoResponses = {
            'business': [
                'Great question! As your Business Expert Agent, I can help you assess your business needs and recommend the right AI solution. Would you like to start with a quick assessment?',
                'I can help schedule a consultation with our team, automate your client intake process, or answer questions about our services. What interests you most?',
                'Based on what you\'ve shared, I\'d recommend starting with our Professional tier. It includes custom agent development and workflow automation. Want me to walk you through the details?'
            ],
            'customer': [
                'I understand your concern. Let me look into that for you. Our Customer Service system can route tickets, track resolution times, and escalate critical issues automatically.',
                'I\'ve noted your request. In a live environment, I would create a support ticket and route it to the appropriate team member based on priority and expertise.',
                'Is there anything else I can help with? I can also provide updates on existing tickets or connect you with a specialist.'
            ],
            'sales': [
                'Thanks for your interest! I can help qualify leads, automate follow-up sequences, and provide pipeline analytics. What\'s your current sales process like?',
                'Based on our data, businesses using AI-driven sales automation see a 35% increase in conversion rates. Would you like to see how this would work for your specific industry?',
                'I can set up an automated follow-up sequence for you. Typically, we recommend a 5-touch sequence over 14 days. Shall I outline the approach?'
            ],
            'finance': [
                'I can help streamline your financial operations. Do you need assistance with invoicing, expense tracking, or financial reporting?',
                'Our Finance Agent integrates with QuickBooks and other accounting platforms. In a live setup, I would automatically categorize expenses and flag anomalies.',
                'I\'ve prepared a summary of your request. In production, this would generate a detailed financial report with actionable insights.'
            ],
            'legal': [
                'I\'m powered by JurisMind\u2122 RAG technology. I can assist with contract review, compliance monitoring, and legal research. What do you need help with?',
                'I\'ve analyzed your query. In a live environment, I would cross-reference relevant legal databases and provide citations along with my analysis.',
                'Important note: While I provide AI-assisted legal guidance, all recommendations should be reviewed by a qualified attorney. Would you like me to draft a summary for your legal team?'
            ]
        };

        var responses = demoResponses[currentAgentId] || [
            'Thank you for your message. This is a demo of how our AI agents interact.',
            'In a live environment, I would process your request using our n8n-powered workflow and provide a real-time response.',
            'Would you like to learn more about connecting this agent to your business workflows?'
        ];

        // Pick a response based on conversation length
        var messageCount = modalChat.querySelectorAll('.user-message').length;
        var responseIndex = Math.min(messageCount - 1, responses.length - 1);
        var botResponse = responses[responseIndex];

        setTimeout(function() {
            removeTypingIndicator();
            addBotMessage(botResponse);
            demoInput.disabled = false;
            sendButton.disabled = false;
            demoInput.focus();
        }, 1200 + Math.random() * 800);
    }
}

// Helper: remove typing indicator
function removeTypingIndicator() {
    var typing = document.getElementById('typing-indicator');
    if (typing) typing.remove();
}

// Helper: add a bot message to the chat
function addBotMessage(html) {
    var modalChat = document.getElementById('demo-modal-chat');
    var botDiv = document.createElement('div');
    botDiv.className = 'chat-message bot-message';
    botDiv.innerHTML = '<p>' + html + '</p>';
    modalChat.appendChild(botDiv);
    modalChat.scrollTop = modalChat.scrollHeight;
}

// ==========================================================================
// Utility Functions
// ==========================================================================

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Escape attribute value
 */
function escapeAttr(text) {
    return text.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/**
 * Format bot response — convert basic markdown-like formatting
 */
function formatBotResponse(text) {
    // Escape HTML first
    var safe = escapeHtml(text);
    // Convert **bold**
    safe = safe.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Convert line breaks
    safe = safe.replace(/\n/g, '<br>');
    return safe;
}

// ==========================================================================
// Focus Trap for Accessibility
// ==========================================================================

function trapFocus(element) {
    var focusableElements = element.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    var firstFocusable = focusableElements[0];
    var lastFocusable = focusableElements[focusableElements.length - 1];

    element.addEventListener('keydown', function(e) {
        if (e.key !== 'Tab') return;

        if (e.shiftKey) {
            if (document.activeElement === firstFocusable) {
                e.preventDefault();
                lastFocusable.focus();
            }
        } else {
            if (document.activeElement === lastFocusable) {
                e.preventDefault();
                firstFocusable.focus();
            }
        }
    });
}

var demoModal = document.getElementById('demo-modal');
if (demoModal) {
    trapFocus(demoModal);
}
