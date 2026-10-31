// Dynamic Audio Reactive Background & Visualizer using Web Audio API

class AudioVisualizer {
  constructor(audioElement) {
    this.audio = audioElement;
    this.audioContext = null;
    this.analyser = null;
    this.source = null;
    this.dataArray = null;
    this.bufferLength = 0;
    this.animationFrameId = null;
    this.canvas = document.getElementById("visualizer-canvas");
    this.ctx = this.canvas ? this.canvas.getContext("2d") : null;
    this.ambientBg = document.getElementById("dynamic-ambient-bg");
    this.isInitialized = false;
    this.isPlaying = false;

    // Smoothed frequency metrics
    this.bassEnergy = 0;
    this.midEnergy = 0;
    this.trebleEnergy = 0;
    this.hueShift = 240; // Initial purple-indigo hue

    // Particle system
    this.particles = [];
    this.numParticles = 50;

    this.resizeCanvas();
    window.addEventListener("resize", () => this.resizeCanvas());
    this.initParticles();
  }

  resizeCanvas() {
    if (!this.canvas) return;
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  initParticles() {
    this.particles = [];
    for (let i = 0; i < this.numParticles; i++) {
      this.particles.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        radius: Math.random() * 3 + 1,
        baseSpeedX: (Math.random() - 0.5) * 0.8,
        baseSpeedY: (Math.random() - 0.5) * 0.8,
        alpha: Math.random() * 0.5 + 0.2
      });
    }
  }

  setupAudioContext() {
    if (this.isInitialized) return;

    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.audioContext = new AudioCtx();
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = 256;
      this.analyser.smoothingTimeConstant = 0.82;

      this.source = this.audioContext.createMediaElementSource(this.audio);
      this.source.connect(this.analyser);
      this.analyser.connect(this.audioContext.destination);

      this.bufferLength = this.analyser.frequencyBinCount;
      this.dataArray = new Uint8Array(this.bufferLength);
      this.isInitialized = true;
    } catch (e) {
      console.warn("Web Audio API initialized with fallback:", e);
    }
  }

  onPlay() {
    this.setupAudioContext();
    if (this.audioContext && this.audioContext.state === "suspended") {
      this.audioContext.resume();
    }
    this.isPlaying = true;
    if (this.ambientBg) {
      this.ambientBg.classList.add("reactive-active");
    }
    this.animate();
  }

  onPauseOrStop() {
    this.isPlaying = false;
    // Smooth reset to clean starting background
    if (this.ambientBg) {
      this.ambientBg.classList.remove("reactive-active");
      this.ambientBg.style.setProperty("--bass-glow", "0px");
      this.ambientBg.style.setProperty("--reactive-scale", "1");
      this.ambientBg.style.background = "";
      this.ambientBg.style.filter = "blur(60px)";
    }
  }

  animate() {
    if (!this.canvas || !this.ctx) return;

    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    if (this.isPlaying && this.analyser) {
      this.analyser.getByteFrequencyData(this.dataArray);

      let bassSum = 0;
      let midSum = 0;
      let trebleSum = 0;

      const bassEnd = Math.floor(this.bufferLength * 0.15);
      const midEnd = Math.floor(this.bufferLength * 0.55);

      for (let i = 0; i < this.bufferLength; i++) {
        const val = this.dataArray[i];
        if (i < bassEnd) bassSum += val;
        else if (i < midEnd) midSum += val;
        else trebleSum += val;
      }

      const rawBass = bassSum / (bassEnd || 1);
      const rawMid = midSum / ((midEnd - bassEnd) || 1);
      const rawTreble = trebleSum / ((this.bufferLength - midEnd) || 1);

      this.bassEnergy += (rawBass - this.bassEnergy) * 0.15;
      this.midEnergy += (rawMid - this.midEnergy) * 0.15;
      this.trebleEnergy += (rawTreble - this.trebleEnergy) * 0.15;

      this.hueShift = (this.hueShift + 0.35 + (this.trebleEnergy / 255) * 1.5) % 360;

      const color1 = `hsl(${this.hueShift}, 85%, ${Math.min(65, 30 + (this.bassEnergy / 255) * 35)}%)`;
      const color2 = `hsl(${(this.hueShift + 65) % 360}, 90%, ${Math.min(60, 25 + (this.midEnergy / 255) * 35)}%)`;
      const color3 = `hsl(${(this.hueShift + 140) % 360}, 80%, ${Math.min(50, 20 + (this.trebleEnergy / 255) * 30)}%)`;

      if (this.ambientBg) {
        const bassNorm = this.bassEnergy / 255;
        const scale = 1 + bassNorm * 0.08;
        const blur = 60 + bassNorm * 80;

        this.ambientBg.style.background = `
          radial-gradient(circle at 20% 30%, ${color1} 0%, transparent 55%),
          radial-gradient(circle at 80% 70%, ${color2} 0%, transparent 60%),
          radial-gradient(circle at 50% 50%, ${color3} 0%, transparent 70%),
          #0b0d17
        `;
        this.ambientBg.style.setProperty("--reactive-scale", scale.toFixed(3));
        this.ambientBg.style.filter = `blur(${blur}px) contrast(1.2)`;
      }

      this.drawWaveforms(color1, color2);
      this.drawParticles(this.bassEnergy / 255);

      this.animationFrameId = requestAnimationFrame(() => this.animate());
    } else {
      this.drawIdleCanvas();
    }
  }

  drawWaveforms(c1, c2) {
    const width = this.canvas.width;
    const height = this.canvas.height;
    const sliceWidth = width / this.bufferLength;

    this.ctx.lineWidth = 2.5;
    this.ctx.beginPath();

    let x = 0;
    for (let i = 0; i < this.bufferLength; i++) {
      const v = this.dataArray[i] / 255.0;
      const y = height * 0.85 - (v * height * 0.28);

      if (i === 0) {
        this.ctx.moveTo(x, y);
      } else {
        this.ctx.lineTo(x, y);
      }
      x += sliceWidth;
    }

    const grad = this.ctx.createLinearGradient(0, height * 0.5, width, height);
    grad.addColorStop(0, c1);
    grad.addColorStop(1, c2);

    this.ctx.strokeStyle = grad;
    this.ctx.stroke();

    this.ctx.lineTo(width, height);
    this.ctx.lineTo(0, height);
    this.ctx.closePath();
    this.ctx.fillStyle = "rgba(255, 255, 255, 0.03)";
    this.ctx.fill();
  }

  drawParticles(boost) {
    const w = this.canvas.width;
    const h = this.canvas.height;

    for (let p of this.particles) {
      p.x += p.baseSpeedX * (1 + boost * 3);
      p.y += p.baseSpeedY * (1 + boost * 3);

      if (p.x < 0) p.x = w;
      if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h;
      if (p.y > h) p.y = 0;

      const dynamicRadius = p.radius + boost * 3;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, dynamicRadius, 0, Math.PI * 2);
      this.ctx.fillStyle = `rgba(255, 255, 255, ${p.alpha * (0.4 + boost * 0.6)})`;
      this.ctx.shadowBlur = 10 * boost;
      this.ctx.shadowColor = `hsl(${this.hueShift}, 100%, 70%)`;
      this.ctx.fill();
      this.ctx.shadowBlur = 0;
    }
  }

  drawIdleCanvas() {
    const w = this.canvas.width;
    const h = this.canvas.height;
    this.ctx.clearRect(0, 0, w, h);

    for (let p of this.particles) {
      p.x += p.baseSpeedX * 0.3;
      p.y += p.baseSpeedY * 0.3;

      if (p.x < 0) p.x = w;
      if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h;
      if (p.y > h) p.y = 0;

      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.radius * 0.7, 0, Math.PI * 2);
      this.ctx.fillStyle = "rgba(255, 255, 255, 0.08)";
      this.ctx.fill();
    }
  }
}

window.AudioVisualizer = AudioVisualizer;
