// Core Audio Player Engine with Backend API & Guest Limitations

class MusicPlayer {
  constructor() {
    this.audio = new Audio();
    this.audio.crossOrigin = "anonymous";
    this.queue = [];
    this.currentIndex = -1;
    this.isPlaying = false;
    this.isShuffle = false;
    this.repeatMode = "off"; // 'off' | 'all' | 'one'
    this.visualizer = null;
    this.playedSongsInSession = new Set();

    this.initAudioListeners();
  }

  setVisualizer(visualizer) {
    this.visualizer = visualizer;
  }

  initAudioListeners() {
    this.audio.addEventListener("play", () => {
      this.isPlaying = true;
      if (this.visualizer) this.visualizer.onPlay();
      window.dispatchEvent(new CustomEvent("playerStateChange", { detail: { isPlaying: true } }));
    });

    this.audio.addEventListener("pause", () => {
      this.isPlaying = false;
      if (this.visualizer) this.visualizer.onPauseOrStop();
      window.dispatchEvent(new CustomEvent("playerStateChange", { detail: { isPlaying: false } }));
    });

    this.audio.addEventListener("timeupdate", () => {
      const current = this.audio.currentTime || 0;
      const duration = this.audio.duration || 0;
      window.dispatchEvent(new CustomEvent("playerTimeUpdate", {
        detail: {
          current,
          duration,
          progress: duration > 0 ? (current / duration) * 100 : 0
        }
      }));
    });

    this.audio.addEventListener("ended", () => {
      if (this.repeatMode === "one") {
        this.audio.currentTime = 0;
        this.audio.play();
      } else if (this.repeatMode === "all" || this.currentIndex < this.queue.length - 1) {
        this.next();
      } else {
        this.isPlaying = false;
        if (this.visualizer) this.visualizer.onPauseOrStop();
        window.dispatchEvent(new CustomEvent("playerStateChange", { detail: { isPlaying: false } }));
      }
    });

    this.audio.addEventListener("error", (e) => {
      console.warn("Audio loading error:", e);
      window.dispatchEvent(new CustomEvent("playerError", {
        detail: { message: "Failed to stream audio file. Check network or source URL." }
      }));
    });
  }

  setQueue(songs, startIndex = 0) {
    this.queue = [...songs];
    this.currentIndex = startIndex;
    if (this.queue.length > 0) {
      this.loadSong(this.queue[this.currentIndex]);
    }
  }

  loadSong(song) {
    if (!song) return;

    // Resolve URL (relative /uploads or external stream)
    let finalUrl = song.url;
    const isLiveServer = window.location.port !== "5000";
    const host = isLiveServer ? "http://localhost:5000" : "";

    if (song.isLocalFile && song.url.startsWith("/")) {
      finalUrl = `${host}${song.url}`;
    } else if (song.url.startsWith("http") && !song.url.includes("localhost:5000")) {
      // Proxy external audio through local server to ensure CORS & range request support
      finalUrl = `${host}/api/songs/stream?url=${encodeURIComponent(song.url)}`;
    }

    this.audio.src = finalUrl;
    this.audio.load();
    window.dispatchEvent(new CustomEvent("currentSongChange", { detail: { song } }));
  }

  playSongById(songId, allSongs = null) {
    if (allSongs) {
      this.queue = [...allSongs];
    }
    const idx = this.queue.findIndex(s => (s._id === songId || s.id === songId));
    if (idx !== -1) {
      this.currentIndex = idx;
      this.loadSong(this.queue[this.currentIndex]);
      this.play();
    }
  }

  play() {
    const current = this.getCurrentSong();
    if (!current) return;

    // Track played songs for session and enforce guest limit (2-4 songs limit)
    if (window.musicAPI.isGuest()) {
      const authCheck = window.musicAPI.canPlaySong();
      if (!authCheck.allowed) {
        this.pause();
        window.dispatchEvent(new CustomEvent("guestLimitReached"));
        return;
      }
      const songId = current._id || current.id;
      if (!this.playedSongsInSession.has(songId)) {
        this.playedSongsInSession.add(songId);
        window.musicAPI.incrementGuestPlay();
      }
    }

    this.audio.play().catch(err => {
      console.warn("Autoplay was prevented by browser policy:", err);
    });
  }

  pause() {
    this.audio.pause();
  }

  togglePlay() {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.play();
    }
  }

  next() {
    if (this.queue.length === 0) return;

    if (this.isShuffle) {
      let randIdx;
      do {
        randIdx = Math.floor(Math.random() * this.queue.length);
      } while (randIdx === this.currentIndex && this.queue.length > 1);
      this.currentIndex = randIdx;
    } else {
      this.currentIndex = (this.currentIndex + 1) % this.queue.length;
    }

    this.loadSong(this.queue[this.currentIndex]);
    this.play();
  }

  prev() {
    if (this.queue.length === 0) return;

    if (this.audio.currentTime > 3) {
      this.audio.currentTime = 0;
      return;
    }

    this.currentIndex = (this.currentIndex - 1 + this.queue.length) % this.queue.length;
    this.loadSong(this.queue[this.currentIndex]);
    this.play();
  }

  seek(percent) {
    if (this.audio.duration) {
      this.audio.currentTime = (percent / 100) * this.audio.duration;
    }
  }

  setVolume(val) {
    this.audio.volume = Math.max(0, Math.min(1, val));
  }

  toggleMute() {
    this.audio.muted = !this.audio.muted;
    return this.audio.muted;
  }

  toggleShuffle() {
    this.isShuffle = !this.isShuffle;
    return this.isShuffle;
  }

  toggleRepeat() {
    const modes = ["off", "all", "one"];
    const nextIdx = (modes.indexOf(this.repeatMode) + 1) % modes.length;
    this.repeatMode = modes[nextIdx];
    return this.repeatMode;
  }

  getCurrentSong() {
    return this.queue[this.currentIndex] || null;
  }

  async downloadSong(song = null) {
    const targetSong = song || this.getCurrentSong();
    if (!targetSong) return;

    try {
      window.dispatchEvent(new CustomEvent("toastMessage", {
        detail: { message: `Downloading "${targetSong.title}"...`, type: "info" }
      }));

      const downloadUrl = window.musicAPI.getDownloadUrl(targetSong);
      const safeTitle = `${targetSong.title} - ${targetSong.artist}`.replace(/[^a-zA-Z0-9 _-]/g, "");
      const fileName = `${safeTitle}.mp3`;

      // Trigger direct anchor download
      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = fileName;
      link.target = "_blank";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      window.dispatchEvent(new CustomEvent("toastMessage", {
        detail: { message: `Download started: ${fileName}`, type: "success" }
      }));
    } catch (err) {
      window.dispatchEvent(new CustomEvent("toastMessage", {
        detail: { message: `Error downloading track: ${err.message}`, type: "error" }
      }));
    }
  }
}

window.musicPlayer = new MusicPlayer();
