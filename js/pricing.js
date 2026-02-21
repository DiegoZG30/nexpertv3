// ========================================
// PRICING PAGE JAVASCRIPT
// ========================================

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initFAQ();
});

// ========================================
// FAQ Accordion Functionality
// ========================================

function initFAQ() {
    const faqQuestions = document.querySelectorAll('.faq-question');

    if (faqQuestions.length === 0) return;

    faqQuestions.forEach(question => {
        question.addEventListener('click', function() {
            const item = this.parentElement;
            const isActive = item.classList.contains('active');

            // Close all FAQ items in the same column
            const column = item.closest('.faq-column');
            if (column) {
                column.querySelectorAll('.faq-item').forEach(faq => {
                    faq.classList.remove('active');
                });
            }

            // Toggle current item if it wasn't active
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
}

// ========================================
// Pricing Card Button Actions
// ========================================

// Get Started buttons
const getStartedButtons = document.querySelectorAll('.pricing-card .btn-primary');
getStartedButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Get the plan name from the card
        const card = this.closest('.pricing-card');
        const planName = card.querySelector('h3').textContent;

        // For now, redirect to contact page with plan parameter
        // In production, this would integrate with your payment/signup system
        window.location.href = `contact.html?plan=${encodeURIComponent(planName)}`;
    });
});

// Contact Sales button (Enterprise)
const contactSalesButtons = document.querySelectorAll('.pricing-card .btn-outline');
contactSalesButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Redirect to contact page with enterprise flag
        window.location.href = 'contact.html?plan=Enterprise';
    });
});

// CTA Banner Button
const ctaButton = document.querySelector('.cta-banner .btn-primary');
if (ctaButton) {
    ctaButton.addEventListener('click', function() {
        window.location.href = 'contact.html?type=consultation';
    });
}
