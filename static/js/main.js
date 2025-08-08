// FinSurvive - Enhanced JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize scroll animations
    initScrollAnimations();
    
    // Initialize interactive effects
    initInteractiveEffects();
    
    // Initialize particle system
    initParticleSystem();
    
    // Initialize smooth scrolling
    initSmoothScrolling();
    
    // Initialize form enhancements
    initFormEnhancements();
    
    // Initialize flash message auto-dismiss
    initFlashMessages();
});

// Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);
    
    // Observe all scroll-animate elements
    document.querySelectorAll('.scroll-animate').forEach(el => {
        observer.observe(el);
    });
    
    // Observe cards for staggered animation
    document.querySelectorAll('.card').forEach((card, index) => {
        card.style.animationDelay = `${0.6 + index * 0.2}s`;
        observer.observe(card);
    });
}

// Interactive Effects
function initInteractiveEffects() {
    // Add hover effects to buttons
    document.querySelectorAll('.btn, .btn-outline').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px) scale(1.02)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Add ripple effect to cards
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', function(e) {
            const ripple = document.createElement('div');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.3)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            ripple.style.left = e.clientX - card.offsetLeft + 'px';
            ripple.style.top = e.clientY - card.offsetTop + 'px';
            ripple.style.width = ripple.style.height = '20px';
            
            card.style.position = 'relative';
            card.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Particle System
function initParticleSystem() {
    const particles = document.querySelectorAll('.particle');
    
    particles.forEach((particle, index) => {
        // Add random positioning
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 6 + 's';
        
        // Add mouse interaction
        document.addEventListener('mousemove', (e) => {
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            particle.style.transform = `translate(${x * 10}px, ${y * 10}px)`;
        });
    });
}

// Smooth Scrolling
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Form Enhancements
function initFormEnhancements() {
    // Add floating labels
    document.querySelectorAll('.auth-card input').forEach(input => {
        const label = input.previousElementSibling;
        if (label && label.tagName === 'LABEL') {
            input.addEventListener('focus', function() {
                label.style.transform = 'translateY(-20px) scale(0.8)';
                label.style.color = 'var(--accent)';
            });
            
            input.addEventListener('blur', function() {
                if (!this.value) {
                    label.style.transform = 'translateY(0) scale(1)';
                    label.style.color = 'var(--muted)';
                }
            });
        }
    });
    
    // Add loading states to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.textContent;
                submitBtn.innerHTML = '<span class="loading"></span> Processing...';
                submitBtn.disabled = true;
                
                // Re-enable after 3 seconds (fallback)
                setTimeout(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    });
}

// Flash Messages
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach((message, index) => {
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            message.style.animation = 'slideOutRight 0.5s ease-out';
            setTimeout(() => {
                message.remove();
            }, 500);
        }, 5000 + (index * 1000));
        
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.style.cssText = `
            position: absolute;
            top: 8px;
            right: 8px;
            background: none;
            border: none;
            color: white;
            font-size: 18px;
            cursor: pointer;
            opacity: 0.7;
            transition: opacity 0.3s ease;
        `;
        
        closeBtn.addEventListener('mouseenter', () => {
            closeBtn.style.opacity = '1';
        });
        
        closeBtn.addEventListener('mouseleave', () => {
            closeBtn.style.opacity = '0.7';
        });
        
        closeBtn.addEventListener('click', () => {
            message.style.animation = 'slideOutRight 0.5s ease-out';
            setTimeout(() => {
                message.remove();
            }, 500);
        });
        
        message.style.position = 'relative';
        message.appendChild(closeBtn);
    });
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .flash {
        position: relative;
        padding-right: 40px;
    }
    
    .loading {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
        margin-right: 8px;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

// Performance optimization
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimize scroll events
const optimizedScrollHandler = debounce(() => {
    // Handle scroll-based animations
}, 16);

window.addEventListener('scroll', optimizedScrollHandler);

// Add keyboard navigation
document.addEventListener('keydown', function(e) {
    // Escape key to close flash messages
    if (e.key === 'Escape') {
        document.querySelectorAll('.flash').forEach(message => {
            message.style.animation = 'slideOutRight 0.5s ease-out';
            setTimeout(() => {
                message.remove();
            }, 500);
        });
    }
});

// Add touch support for mobile
if ('ontouchstart' in window) {
    document.querySelectorAll('.card, .btn, .btn-outline').forEach(element => {
        element.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
        });
        
        element.addEventListener('touchend', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

console.log('🚀 FinSurvive enhanced with professional animations and interactions!');