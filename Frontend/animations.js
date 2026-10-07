// ════════════════════════════════════════════
// 1. PARTICLE BACKGROUND
// ════════════════════════════════════════════

function initParticles(canvasId) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  function resize() {
    canvas.width  = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  const PARTICLE_COUNT = 55;
  const particles = [];

  class Particle {
    constructor() { this.reset(); }

    reset() {
      this.x     = Math.random() * canvas.width;
      this.y     = Math.random() * canvas.height;
      this.r     = Math.random() * 1.6 + 0.4;
      this.alpha = Math.random() * 0.5 + 0.1;
      this.vx    = (Math.random() - 0.5) * 0.35;
      this.vy    = (Math.random() - 0.5) * 0.35;
      this.life  = 0;
      this.maxLife = Math.random() * 300 + 200;

      // Color — gold or blue tint
      const colors = [
        `rgba(232,184,75,`,
        `rgba(245,208,122,`,
        `rgba(59,130,246,`,
        `rgba(34,211,238,`
      ];
      this.color = colors[Math.floor(Math.random() * colors.length)];
    }

    update() {
      this.x    += this.vx;
      this.y    += this.vy;
      this.life += 1;

      // Fade in and out
      const half = this.maxLife / 2;
      if (this.life < half) {
        this.alpha = (this.life / half) * 0.55;
      } else {
        this.alpha = ((this.maxLife - this.life) / half) * 0.55;
      }

      if (this.life >= this.maxLife) this.reset();
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = this.color + this.alpha + ')';
      ctx.fill();
    }
  }

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const p = new Particle();
    p.life = Math.random() * p.maxLife; // stagger start
    particles.push(p);
  }

  // Draw connecting lines between nearby particles
  function drawLines() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx   = particles[i].x - particles[j].x;
        const dy   = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 100) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(232,184,75,${0.06 * (1 - dist / 100)})`;
          ctx.lineWidth   = 0.5;
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawLines();
    particles.forEach(p => { p.update(); p.draw(); });
    requestAnimationFrame(animate);
  }

  animate();
}

// Start particles on hero and chat background
document.addEventListener('DOMContentLoaded', () => {
  initParticles('hero-canvas');
  initParticles('chat-canvas');
});


// ════════════════════════════════════════════
// 2. TYPEWRITER EFFECT
// ════════════════════════════════════════════

function typeWriter(elementId, lines, speed = 52) {
  const el = document.getElementById(elementId);
  if (!el) return;

  el.innerHTML = '';
  let lineIndex = 0;
  let charIndex = 0;
  let currentSpan = null;

  function nextChar() {
    if (lineIndex >= lines.length) {
      // Add blinking cursor at end
      const cursor = document.createElement('span');
      cursor.className = 'type-cursor';
      cursor.textContent = '|';
      el.appendChild(cursor);
      return;
    }

    if (charIndex === 0) {
      // Start a new line span
      if (lineIndex > 0) el.appendChild(document.createElement('br'));
      currentSpan = document.createElement('span');
      el.appendChild(currentSpan);
    }

    currentSpan.textContent += lines[lineIndex][charIndex];
    charIndex++;

    if (charIndex >= lines[lineIndex].length) {
      lineIndex++;
      charIndex = 0;
      setTimeout(nextChar, speed * 4); // pause between lines
    } else {
      setTimeout(nextChar, speed);
    }
  }

  // Small delay before starting
  setTimeout(nextChar, 600);
}

// ════════════════════════════════════════════
// 3. BUTTON SHINE HOVER EFFECT
// ════════════════════════════════════════════

function initButtonShine() {
  document.querySelectorAll('.btn-primary, .auth-btn, .new-chat-btn').forEach(btn => {
    btn.classList.add('shine-btn');

    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x    = ((e.clientX - rect.left) / rect.width)  * 100;
      const y    = ((e.clientY - rect.top)  / rect.height) * 100;
      btn.style.setProperty('--shine-x', x + '%');
      btn.style.setProperty('--shine-y', y + '%');
    });
  });
}

document.addEventListener('DOMContentLoaded', initButtonShine);

// Re-run for dynamically added buttons
const btnObserver = new MutationObserver(() => initButtonShine());
btnObserver.observe(document.body, { childList: true, subtree: true });


// ════════════════════════════════════════════
// 4. SCROLL REVEAL (enhanced)
// ════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
  const observer = new IntersectionObserver(entries => {
    entries.forEach((e, i) => {
      if (e.isIntersecting) {
        setTimeout(() => e.target.classList.add('visible'), i * 80);
      }
    });
  }, { threshold: 0.10 });

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
});


// ════════════════════════════════════════════
// 5. CHAT MESSAGE RIPPLE on send button
// ════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
  const sendBtn = document.getElementById('send');
  if (!sendBtn) return;

  sendBtn.addEventListener('click', function(e) {
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    const rect = this.getBoundingClientRect();
    ripple.style.left = (e.clientX - rect.left) + 'px';
    ripple.style.top  = (e.clientY - rect.top)  + 'px';
    this.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
});