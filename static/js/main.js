// =====================================================
// MAIN JAVASCRIPT - Interactivity & Animations
// =====================================================

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeNavigation();
    initializeCounters();
    initializeSmoothScroll();
    initializeMobileMenu();
    initializeScrollAnimations();
    initializeFormValidation();
    initializeServiceCardAnimations();
    initializeServiceCardExpand();
    initializeHeroMockups();
});

// =====================================================
// THEME TOGGLE
// =====================================================

function initializeTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeToggleCircle = document.getElementById('theme-toggle-circle');
    const savedTheme = localStorage.getItem('theme') || 'dark';
    
    // Apply saved theme
    applyTheme(savedTheme);
    
    // Add click listener
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.body.classList.contains('light-mode') ? 'light' : 'dark';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
}

function applyTheme(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    const themeToggleCircle = document.getElementById('theme-toggle-circle');
    
    if (theme === 'light') {
        document.body.classList.add('light-mode');
        if (themeToggle) {
            themeToggle.classList.remove('bg-gray-400');
            themeToggle.classList.add('bg-primary-500');
        }
        if (themeToggleCircle) {
            themeToggleCircle.classList.add('translate-x-6');
            themeToggleCircle.innerHTML = '<i class="fas fa-sun text-yellow-400 text-xs flex items-center justify-center absolute inset-0"></i>';
        }
    } else {
        document.body.classList.remove('light-mode');
        if (themeToggle) {
            themeToggle.classList.remove('bg-primary-500');
            themeToggle.classList.add('bg-gray-400');
        }
        if (themeToggleCircle) {
            themeToggleCircle.classList.remove('translate-x-6');
            themeToggleCircle.innerHTML = '<i class="fas fa-moon text-dark-900 text-xs flex items-center justify-center absolute inset-0"></i>';
        }
    }
}

// =====================================================
// SERVICE CARD ANIMATIONS
// =====================================================

function initializeServiceCardAnimations() {
    const cards = document.querySelectorAll('.card-3d');
    
    cards.forEach(card => {
        const icon = card.querySelector('i');
        
        card.addEventListener('mouseenter', function() {
            if (icon) {
                icon.classList.add('rotate-icon');
            }
        });
        
        card.addEventListener('mouseleave', function() {
            if (icon) {
                icon.classList.remove('rotate-icon');
            }
        });
    });
}

// =====================================================
// SERVICE CARD EXPAND/COLLAPSE
// =====================================================

function initializeServiceCardExpand() {
    const container = document.getElementById('servicesContainer');
    const cards = document.querySelectorAll('.service-card');
    
    console.log('Initializing service card expand. Found cards:', cards.length);
    
    if (!container) {
        console.log('Container not found');
        return;
    }
    
    cards.forEach((card, index) => {
        console.log('Attaching click handler to card', index);
        const closeBtn = card.querySelector('.service-close-btn');
        
        // Make entire card clickable
        card.style.cursor = 'pointer';
        
        // Toggle expand/collapse on click
        card.addEventListener('click', function(e) {
            // Don't handle here if clicking the close button (it has its own handler)
            if (e.target.closest('.service-close-btn')) {
                console.log('Close button clicked');
                return;
            }

            // If card is already expanded, collapse it on click
            if (card.classList.contains('expanded')) {
                console.log('Card clicked while expanded — collapsing');
                collapseCard(card);
                return;
            }

            console.log('Card clicked, expanding');
            expandCard(card);
        });
        
        // Close button click
        if (closeBtn) {
            closeBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                console.log('Close button listener triggered');
                collapseCard(card);
            });
        }
    });
    
    // Escape key to close
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const expandedCard = document.querySelector('.service-card.expanded');
            if (expandedCard) {
                collapseCard(expandedCard);
            }
        }
    });
}

// =====================================================
// HERO MOCKUP ROTATOR (auto-rotate panels)
// =====================================================
function initializeHeroMockups() {
    const rotator = document.querySelector('.mockup-rotator');
    if (!rotator) return;
    const panels = rotator.querySelectorAll('.mockup-panel');
    if (!panels.length) return;
    let idx = 0;
    panels.forEach((p, i) => p.classList.remove('active'));
    panels[0].classList.add('active');

    setInterval(() => {
        panels[idx].classList.remove('active');
        idx = (idx + 1) % panels.length;
        panels[idx].classList.add('active');
    }, 4200);
}

function expandCard(card) {
    const allCards = document.querySelectorAll('.service-card');
    
    // Remove any previously expanded card
    allCards.forEach(c => {
        if (c !== card && c.classList.contains('expanded')) {
            collapseCard(c);
        }
    });
    
    // Expand current card
    card.classList.add('expanded');
    
    // Dim other cards (keep in same grid, but faded)
    allCards.forEach(c => {
        if (c !== card) {
            c.classList.add('hidden');
        }
    });
    
    // Scroll to expanded card smoothly
    setTimeout(() => {
        card.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

function collapseCard(card) {
    const allCards = document.querySelectorAll('.service-card');
    
    // Collapse card
    card.classList.remove('expanded');
    
    // Show all cards again
    allCards.forEach(c => {
        c.classList.remove('hidden');
    });
}

// =====================================================
// NAVIGATION
// =====================================================

function initializeNavigation() {
    const navbar = document.getElementById('navbar');
    if (!navbar) {
        console.log('Navbar not found');
        return;
    }
    
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add shadow on scroll
        if (scrollTop > 50) {
            navbar.classList.add('shadow-lg', 'shadow-primary-500/10');
        } else {
            navbar.classList.remove('shadow-lg', 'shadow-primary-500/10');
        }
        
        lastScrollTop = scrollTop;
    });
}

// =====================================================
// MOBILE MENU
// =====================================================

function initializeMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
        
        // Close menu when link is clicked
        const links = mobileMenu.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.add('hidden');
            });
        });
    }
}

// =====================================================
// SMOOTH SCROLL
// =====================================================

function initializeSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// =====================================================
// ANIMATED COUNTERS
// =====================================================

function initializeCounters() {
    const counters = document.querySelectorAll('.counter');
    let hasStarted = false;

    function startCounting() {
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = 2000; // 2 seconds
            const increment = target / (duration / 16);
            let current = 0;

            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    counter.textContent = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };

            updateCounter();
        });
    }

    // Start counting when counters come into view
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !hasStarted) {
                hasStarted = true;
                startCounting();
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

// =====================================================
// SCROLL ANIMATIONS
// =====================================================

function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-slide-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all sections
    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });

    // Observe cards
    document.querySelectorAll('[class*="card"]').forEach(card => {
        observer.observe(card);
    });
}

// =====================================================
// FORM VALIDATION
// =====================================================

function initializeFormValidation() {
    const form = document.getElementById('contact-form');
    
    if (form) {
        const inputs = form.querySelectorAll('input[required], textarea[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('error')) {
                    validateField(this);
                }
            });
        });
    }
}

function validateField(field) {
    let isValid = true;
    const errorClass = 'border-red-500 bg-red-500/10';
    
    if (field.type === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        isValid = emailRegex.test(field.value);
    } else if (field.type === 'tel') {
        const phoneRegex = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/;
        isValid = field.value.length === 0 || phoneRegex.test(field.value.replace(/\D/g, ''));
    } else if (field.hasAttribute('required') && field.value.trim() === '') {
        isValid = false;
    }
    
    if (!isValid) {
        field.classList.add(errorClass);
    } else {
        field.classList.remove(errorClass);
    }
    
    return isValid;
}

// =====================================================
// FORM SUBMISSION
// =====================================================

function submitContactForm(formData) {
    return fetch('/api/submit-lead', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    }).then(response => response.json());
}

// =====================================================
// UTILITY FUNCTIONS
// =====================================================

// Debounce function for performance
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Throttle function
function throttle(func, delay) {
    let lastCall = 0;
    return function(...args) {
        const now = Date.now();
        if (now - lastCall >= delay) {
            func.apply(this, args);
            lastCall = now;
        }
    };
}

// Get scroll position
function getScrollPosition() {
    return {
        x: window.pageXOffset,
        y: window.pageYOffset
    };
}

// Check if element is in viewport
function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Add loading animation
function showLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.remove('hidden');
    }
}

function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.add('hidden');
    }
}

// =====================================================
// PERFORMANCE OPTIMIZATIONS
// =====================================================

// Lazy load images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// =====================================================
// LIGHT THEME TOGGLE (Optional)
// =====================================================

function toggleTheme() {
    const html = document.documentElement;
    if (html.getAttribute('data-theme') === 'light') {
        html.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        html.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    }
}

// Load saved theme
function loadSavedTheme() {
    const saved = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
}

// =====================================================
// ACCESSIBILITY
// =====================================================

// Keyboard navigation for dropdown menus
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const mobileMenu = document.getElementById('mobile-menu');
        if (mobileMenu) {
            mobileMenu.classList.add('hidden');
        }
    }
});

// Skip to main content link
const skipLink = document.createElement('a');
skipLink.href = '#main';
skipLink.textContent = 'Skip to main content';
skipLink.className = 'sr-only focus:not-sr-only';
document.body.prepend(skipLink);

// =====================================================
// ANALYTICS (Add your tracking code here)
// =====================================================

// Track page view
function trackPageView() {
    if (typeof gtag !== 'undefined') {
        gtag('config', 'GA_MEASUREMENT_ID', {
            'page_path': window.location.pathname,
            'page_title': document.title
        });
    }
}

// Track events
function trackEvent(eventName, eventParams) {
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, eventParams);
    }
}

// =====================================================
// INITIALIZATION ON PAGE LOAD
// =====================================================

window.addEventListener('load', () => {
    hideLoader();
    loadSavedTheme();
    trackPageView();
});

// Log initialization
console.log('%cCodilight', 'font-size: 20px; font-weight: bold; color: #3b82f6;');
console.log('%cPremium Software Development & Web Development Company', 'font-size: 14px; color: #10b981;');
console.log('%cWebsite loaded successfully!', 'font-size: 12px; color: #888;');
