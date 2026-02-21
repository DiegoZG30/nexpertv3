// ========== FLOATING PARTICLES (Hero) ==========
const particlesContainer = document.getElementById('particles');
if (particlesContainer) {
    const particleCount = window.innerWidth <= 768 ? 6 : 20;
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 6 + 's';
        particle.style.animationDuration = (Math.random() * 4 + 4) + 's';
        particlesContainer.appendChild(particle);
    }
}

// ========== FLOATING STARS (Space Background) ==========
const spaceBg = document.querySelector('.space-background-container');
if (spaceBg) {
    const starCount = window.innerWidth <= 768 ? 15 : 40;
    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.className = 'floating-star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        const size = Math.random() * 3 + 1;
        star.style.width = size + 'px';
        star.style.height = size + 'px';
        star.style.animationDelay = Math.random() * 8 + 's';
        star.style.animationDuration = (Math.random() * 6 + 5) + 's';
        if (Math.random() > 0.7) star.classList.add('star-blue');
        spaceBg.appendChild(star);
    }
}
