// UI Controller, Section Routers, Search Engine & Modals with Node.js & Free Music APIs

document.addEventListener("DOMContentLoaded", async () => {
  // Elements
  const dynamicAmbientBg = document.getElementById("dynamic-ambient-bg");
  const visualizerCanvas = document.getElementById("visualizer-canvas");
  const songsGrid = document.getElementById("songs-grid");
  const sectionTitle = document.getElementById("current-section-title");
  const sectionSubtitle = document.getElementById("current-section-subtitle");
  const searchInput = document.getElementById("search-input");
  const clearSearchBtn = document.getElementById("clear-search-btn");
  const categoryTabs = document.querySelectorAll(".nav-tab");
  const adminDashboardBtn = document.getElementById("admin-dashboard-btn");
  const adminDashboardModal = document.getElementById("admin-dashboard-modal");
  const adminTotalUsers = document.getElementById("admin-total-users");
  const adminTotalSongs = document.getElementById("admin-total-songs");
  const adminCatBreakdown = document.getElementById("admin-cat-breakdown");
  const adminUsersTableBody = document.getElementById("admin-users-table-body");
  const adminModalUploadBtn = document.getElementById("admin-modal-upload-btn");

  // Player bar elements
  const currentCover = document.getElementById("player-cover");
  const currentTitle = document.getElementById("player-title");
  const currentArtist = document.getElementById("player-artist");
  const currentMovieActor = document.getElementById("player-movie-actor");
  const playPauseBtn = document.getElementById("play-pause-btn");
  const prevBtn = document.getElementById("prev-btn");
  const nextBtn = document.getElementById("next-btn");
  const shuffleBtn = document.getElementById("shuffle-btn");
  const repeatBtn = document.getElementById("repeat-btn");
  const progressBar = document.getElementById("progress-bar");
  const progressContainer = document.getElementById("progress-container");
  const currentTimeEl = document.getElementById("current-time");
  const durationTimeEl = document.getElementById("duration-time");
  const volumeSlider = document.getElementById("volume-slider");
  const muteBtn = document.getElementById("mute-btn");
  const downloadBtn = document.getElementById("download-btn");
  const favoritePlayerBtn = document.getElementById("favorite-player-btn");

  // Auth & Admin elements
  const userRoleText = document.getElementById("user-role-text");
  const authModal = document.getElementById("auth-modal");
  const authBtn = document.getElementById("auth-btn");
  const authForm = document.getElementById("auth-form");
  const authTitle = document.getElementById("auth-title");
  const authToggleLink = document.getElementById("auth-toggle-link");
  const authSubmitBtn = document.getElementById("auth-submit-btn");
  const adminUploadBtn = document.getElementById("admin-upload-btn");
  const uploadModal = document.getElementById("upload-modal");
  const uploadForm = document.getElementById("upload-form");
  const editModal = document.getElementById("edit-modal");
  const editForm = document.getElementById("edit-form");
  const editSongId = document.getElementById("edit-song-id");
  const editSongTitle = document.getElementById("edit-song-title");
  const editSongArtist = document.getElementById("edit-song-artist");
  const editSongMovie = document.getElementById("edit-song-movie");
  const editSongActor = document.getElementById("edit-song-actor");
  const editSongCategory = document.getElementById("edit-song-category");
  const editSongDuration = document.getElementById("edit-song-duration");
  const editSongCover = document.getElementById("edit-song-cover");
  const editCoverFile = document.getElementById("edit-cover-file");
  const editSongUrl = document.getElementById("edit-song-url");
  const editAudioFile = document.getElementById("edit-audio-file");
  const guestLimitModal = document.getElementById("guest-limit-modal");
  const toastContainer = document.getElementById("toast-container");

  // State
  let currentCategory = "all";
  let currentSource = "all"; // 'all' | 'curated' | 'online'
  let isRegisterMode = false;
  let cachedSongsList = [];

  // Initialize visualizer
  const visualizer = new AudioVisualizer(window.musicPlayer.audio);
  window.musicPlayer.setVisualizer(visualizer);

  // Sync profile if token exists
  if (window.musicAPI.isLoggedIn()) {
    await window.musicAPI.getMe();
  }

  // Toast Notification
  function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <span class="toast-icon">${type === "success" ? "✓" : type === "error" ? "✕" : "ℹ"}</span>
      <span class="toast-text">${message}</span>
    `;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.classList.add("toast-fade-out");
      setTimeout(() => toast.remove(), 400);
    }, 3500);
  }

  window.addEventListener("toastMessage", (e) => {
    showToast(e.detail.message, e.detail.type);
  });

  // Time formatter
  function formatTime(seconds) {
    if (isNaN(seconds) || seconds < 0) return "0:00";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  }

  // Fetch & Render Category Songs from Local DB and Free Music API
  async function loadAndRender(cat, filterQuery = "") {
    currentCategory = cat;
    let songs = [];

    const isSearch = filterQuery && filterQuery.trim() !== "";
    const query = isSearch ? filterQuery.trim() : "";

    // Show/hide clear search button
    if (clearSearchBtn) {
      clearSearchBtn.style.display = isSearch ? "block" : "none";
    }

    if (cat === "favorites") {
      // Favorites comes from local database filtered by user's favorites array
      const allLocal = await window.musicAPI.getSongs("all", query);
      const user = window.musicAPI.getCachedUser() || {};
      const favIds = user.favorites || [];
      songs = allLocal.filter(s => favIds.includes(s._id || s.id));
      sectionTitle.textContent = "Liked Songs";
      sectionSubtitle.textContent = `Songs saved to your personal library (${songs.length} tracks)`;
    } else if (cat === "playlist-emraan") {
      // YouTube Playlist 1: Emraan Hashmi Romantic Hits
      songs = await window.musicAPI.getSongs("all", query, "emraan");
      sectionTitle.textContent = "🌹 Emraan Hashmi Romantic Hits";
      sectionSubtitle.textContent = `Curated from YouTube Playlist (Jannat, Murder 2, Zeher, Tum Mile, Gangster) • ${songs.length} tracks`;
    } else if (cat === "playlist-tseries") {
      // YouTube Playlist 2: Ultimate Bollywood Moody Mix
      songs = await window.musicAPI.getSongs("all", query, "tseries");
      sectionTitle.textContent = "🎧 Ultimate Bollywood Moody Mix";
      sectionSubtitle.textContent = `Curated from T-Series YouTube Playlist (Arijit Singh, Jubin Nautiyal, Animal, Shershaah) • ${songs.length} tracks`;
    } else if (isSearch) {
      // Universal deep search: combines local catalog + live Free Music API
      let localMatches = [];
      let onlineMatches = [];

      if (currentSource === "all" || currentSource === "curated") {
        localMatches = await window.musicAPI.getSongs("all", query);
      }
      if (currentSource === "all" || currentSource === "online") {
        onlineMatches = await window.musicAPI.searchFreeMusicOnline(query);
      }

      // Merge and remove duplicates by title + artist
      const seen = new Set();
      songs = [...localMatches, ...onlineMatches].filter(s => {
        const key = `${s.title.toLowerCase().trim()}_${s.artist.toLowerCase().trim()}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });

      sectionTitle.textContent = `Search Results for "${query}"`;
      sectionSubtitle.textContent = `Found ${songs.length} track(s) matching your query across catalog & free APIs`;
    } else {
      // Normal section browsing (Hollywood, Bollywood, Tollywood, Bhojpuri)
      // Loads only genuine full-length curated songs (no 30s clips injected!)
      if (currentSource === "online") {
        songs = await window.musicAPI.getFreeMusicTrending(cat);
      } else {
        songs = await window.musicAPI.getSongs(cat);
      }

      const displayNames = {
        all: "All Music Collection",
        hollywood: "Hollywood Hits & Global Beats",
        bollywood: "Bollywood Melodies & Desi Hits",
        tollywood: "Tollywood Anthems & Southern Grooves",
        bhojpuri: "Bhojpuri Dhamaal & High Energy Hits"
      };
      sectionTitle.textContent = displayNames[cat] || "Music Collection";
      sectionSubtitle.textContent = cat === "all" ? `Top tracks across Hollywood, Bollywood, Tollywood & Bhojpuri • ${songs.length} tracks` : `Top hits in ${cat.toUpperCase()} • ${songs.length} tracks`;
    }

    cachedSongsList = songs;

    // Load initial song to player queue if not currently playing
    if (songs.length > 0 && !window.musicPlayer.getCurrentSong()) {
      window.musicPlayer.setQueue(songs, 0);
    }

    renderGrid(songs);
  }

  // Render HTML Cards into Grid
  function renderGrid(songs) {
    songsGrid.innerHTML = "";

    if (!songs || songs.length === 0) {
      songsGrid.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">🎵</div>
          <h3>No Tracks Found</h3>
          <p>${currentCategory === "favorites" ? "You haven't bookmarked any songs yet. Click the heart icon on any track!" : "No songs match this category or search filter. Try another keyword or switch source to '🌟 All Tracks'."}</p>
        </div>
      `;
      return;
    }

    const currentSong = window.musicPlayer.getCurrentSong();
    const isAdmin = window.musicAPI.isAdmin();
    const user = window.musicAPI.getCachedUser() || {};
    const userFavorites = user.favorites || [];

    songs.forEach(song => {
      const songId = song._id || song.id;
      const isCurrent = currentSong && (currentSong._id === songId || currentSong.id === songId);
      const isFav = userFavorites.includes(songId);
      const isOnline = !!song.isOnlineTrack;
      const isPlaylist = !!song.isPlaylistTrack || !!song.playlistSource;

      // Handle cover path
      let coverSrc = song.cover;
      if (song.cover && song.cover.startsWith("/")) {
        const isSeparateLiveServer = window.location.hostname === "localhost" && window.location.port !== "5000" && window.location.port !== "";
        const host = isSeparateLiveServer ? "http://localhost:5000" : "";
        coverSrc = `${host}${song.cover}`;
      }

      const card = document.createElement("div");
      card.className = `song-card ${isCurrent ? "active-playing" : ""}`;
      card.innerHTML = `
        <div class="card-cover-wrap">
          <img src="${coverSrc}" alt="${song.title}" class="card-cover" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=300'">
          <button class="card-play-btn" data-id="${songId}" title="Play Track">
            ${isCurrent && window.musicPlayer.isPlaying ? "❚❚" : "▶"}
          </button>
          <span class="card-badge ${song.category}">${song.category}</span>
          ${isPlaylist ? '<span class="card-badge playlist" style="left: 12px; right: auto; background: rgba(239, 68, 68, 0.85);" title="' + (song.playlistSource || 'YouTube Playlist') + '">▶ YT Mix</span>' : isOnline ? '<span class="card-badge online" style="left: 12px; right: auto; background: rgba(59, 130, 246, 0.85);">Free API</span>' : ""}
        </div>
        <div class="card-info">
          <div class="card-title-row">
            <h4 class="card-title" title="${song.title}">${song.title}</h4>
            <button class="card-fav-btn ${isFav ? "favorited" : ""}" data-id="${songId}" title="${isFav ? 'Remove Favorite' : 'Add to Favorites'}">
              ${isFav ? "♥" : "♡"}
            </button>
          </div>
          <p class="card-artist">🎤 ${song.artist}</p>
          <p class="card-meta">🎬 <span>${song.movie || "Single"}</span> • ⭐ <span>${song.actor || "Artist"}</span></p>
          <div class="card-actions">
            <button class="card-action-btn download-action-btn" data-id="${songId}" title="Download Track as MP3">
              📥 Download
            </button>
            ${isAdmin && !isOnline ? `
              <button class="card-action-btn edit-action-btn" data-id="${songId}" title="Edit Song Details">
                ✏️ Edit
              </button>
              <button class="card-action-btn delete-action-btn" data-id="${songId}" title="Delete Song as Admin">
                🗑 Delete
              </button>
            ` : ""}
          </div>
        </div>
      `;

      // Play button click
      card.querySelector(".card-play-btn").addEventListener("click", (e) => {
        e.stopPropagation();
        if (isCurrent) {
          window.musicPlayer.togglePlay();
        } else {
          window.musicPlayer.playSongById(songId, songs);
        }
      });

      // Favorite button click
      card.querySelector(".card-fav-btn").addEventListener("click", async (e) => {
        e.stopPropagation();
        if (window.musicAPI.isGuest()) {
          showToast("Please login to save favorite tracks!", "error");
          openAuthModal();
          return;
        }

        const res = await window.musicAPI.toggleFavorite(songId, song);
        if (res.success) {
          showToast(res.isFavorite ? "Added to your Liked Songs!" : "Removed from Liked Songs", "info");
          updateAuthUI();
          loadAndRender(currentCategory, searchInput.value);
        } else {
          showToast(res.message, "error");
        }
      });

      // Download button click
      card.querySelector(".download-action-btn").addEventListener("click", (e) => {
        e.stopPropagation();
        window.musicPlayer.downloadSong(song);
      });

      // Admin Edit click (for catalog songs)
      const editBtn = card.querySelector(".edit-action-btn");
      if (editBtn) {
        editBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          openEditModal(song);
        });
      }

      // Admin Delete click (for local catalog songs)
      const delBtn = card.querySelector(".delete-action-btn");
      if (delBtn) {
        delBtn.addEventListener("click", async (e) => {
          e.stopPropagation();
          if (confirm(`Admin Action: Permanently delete "${song.title}" from catalog?`)) {
            const res = await window.musicAPI.deleteSong(songId);
            if (res.success) {
              showToast(res.message, "success");
              loadAndRender(currentCategory, searchInput.value);
            } else {
              showToast(res.message, "error");
            }
          }
        });
      }

      // Card container click
      card.addEventListener("click", () => {
        window.musicPlayer.playSongById(songId, songs);
      });

      songsGrid.appendChild(card);
    });
  }

  // Category Tabs switching
  categoryTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      categoryTabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      const category = tab.getAttribute("data-category");
      searchInput.value = "";
      if (clearSearchBtn) clearSearchBtn.style.display = "none";
      loadAndRender(category);
    });
  });

  // Search input debouncing
  let searchTimeout = null;
  searchInput.addEventListener("input", (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      const q = e.target.value;
      loadAndRender(currentCategory, q);
    }, 280);
  });

  // Clear search button
  if (clearSearchBtn) {
    clearSearchBtn.addEventListener("click", () => {
      searchInput.value = "";
      clearSearchBtn.style.display = "none";
      loadAndRender(currentCategory, "");
      searchInput.focus();
    });
  }

  // Auth UI Status
  function updateAuthUI() {
    const isGuest = window.musicAPI.isGuest();
    const isAdmin = window.musicAPI.isAdmin();
    const user = window.musicAPI.getCachedUser();

    if (isGuest) {
      const plays = window.musicAPI.getGuestPlays();
      const remaining = Math.max(0, 3 - plays);
      userRoleText.innerHTML = `👤 Guest (${remaining} Free Play${remaining === 1 ? "" : "s"} left)`;
      authBtn.textContent = "Login / Register";
      if (adminUploadBtn) adminUploadBtn.style.display = "none";
      if (adminDashboardBtn) adminDashboardBtn.style.display = "none";
    } else {
      userRoleText.innerHTML = `${isAdmin ? "🛡️ [Admin]" : "👤"} ${user ? (user.name || user.username) : "User"}`;
      authBtn.textContent = "Logout";
      if (adminUploadBtn) adminUploadBtn.style.display = isAdmin ? "inline-flex" : "none";
      if (adminDashboardBtn) adminDashboardBtn.style.display = isAdmin ? "inline-flex" : "none";
    }

    updatePlayerFavState();
  }

  // Admin Dashboard click
  if (adminDashboardBtn) {
    adminDashboardBtn.addEventListener("click", async () => {
      adminDashboardModal.classList.add("active");
      const statsRes = await window.musicAPI.getAdminStats();
      const usersRes = await window.musicAPI.getAdminUsers();

      if (statsRes && statsRes.stats) {
        adminTotalUsers.textContent = statsRes.stats.totalUsers;
        adminTotalSongs.textContent = statsRes.stats.totalSongs;
        const catMap = statsRes.stats.categories.map(c => `${c.category.toUpperCase()}: ${c.count}`).join(" • ");
        adminCatBreakdown.textContent = catMap || "None";
      }

      if (usersRes && usersRes.users) {
        adminUsersTableBody.innerHTML = usersRes.users.map(u => `
          <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
            <td style="padding: 8px 14px; color: var(--text-muted);">${u.id}</td>
            <td style="padding: 8px 14px; font-weight: 600;">${u.username}</td>
            <td style="padding: 8px 14px;">${u.name || "-"}</td>
            <td style="padding: 8px 14px;"><span style="background: ${u.role === 'admin' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(16, 185, 129, 0.2)'}; color: ${u.role === 'admin' ? '#f87171' : '#34d399'}; padding: 2px 8px; border-radius: 6px; font-size: 0.8rem;">${u.role}</span></td>
            <td style="padding: 8px 14px; color: var(--text-muted); font-size: 0.8rem;">${new Date(u.created_at || Date.now()).toLocaleDateString()}</td>
          </tr>
        `).join("");
      }
    });
  }

  if (adminModalUploadBtn) {
    adminModalUploadBtn.addEventListener("click", () => {
      adminDashboardModal.classList.remove("active");
      uploadModal.classList.add("active");
    });
  }

  function updatePlayerFavState() {
    const current = window.musicPlayer.getCurrentSong();
    if (!current) return;
    const currentId = current._id || current.id;
    const user = window.musicAPI.getCachedUser() || {};
    const favs = user.favorites || [];
    const isFav = favs.includes(currentId);
    favoritePlayerBtn.innerHTML = isFav ? "♥" : "♡";
    favoritePlayerBtn.classList.toggle("favorited", isFav);
  }

  // Modals
  function openAuthModal() {
    authModal.classList.add("active");
  }
  function closeModals() {
    document.querySelectorAll(".modal-overlay").forEach(m => m.classList.remove("active"));
  }

  document.querySelectorAll(".modal-close-btn").forEach(btn => {
    btn.addEventListener("click", closeModals);
  });

  authBtn.addEventListener("click", () => {
    if (window.musicAPI.isLoggedIn()) {
      window.musicAPI.logout();
      showToast("Logged out successfully. Switched to Guest mode.", "info");
      updateAuthUI();
      loadAndRender(currentCategory);
    } else {
      openAuthModal();
    }
  });

  authToggleLink.addEventListener("click", (e) => {
    e.preventDefault();
    isRegisterMode = !isRegisterMode;
    authTitle.textContent = isRegisterMode ? "Create Your Account" : "Welcome Back";
    authSubmitBtn.textContent = isRegisterMode ? "Register & Stream" : "Login";
    authToggleLink.textContent = isRegisterMode ? "Already have an account? Login here" : "Don't have an account? Sign up";
    document.getElementById("auth-name-group").style.display = isRegisterMode ? "block" : "none";
    document.getElementById("auth-role-group").style.display = isRegisterMode ? "block" : "none";
  });

  authForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("auth-username").value;
    const password = document.getElementById("auth-password").value;
    const name = document.getElementById("auth-name") ? document.getElementById("auth-name").value : "";
    const role = document.getElementById("auth-role-select") ? document.getElementById("auth-role-select").value : "user";

    if (isRegisterMode) {
      const res = await window.musicAPI.register(username, password, name, role);
      if (res.success) {
        showToast(res.message, "success");
        closeModals();
        updateAuthUI();
        loadAndRender(currentCategory);
      } else {
        showToast(res.message, "error");
      }
    } else {
      const res = await window.musicAPI.login(username, password);
      if (res.success) {
        showToast(res.message, "success");
        closeModals();
        updateAuthUI();
        loadAndRender(currentCategory);
      } else {
        showToast(res.message, "error");
      }
    }
  });

  // Admin Upload Modal
  adminUploadBtn.addEventListener("click", () => {
    uploadModal.classList.add("active");
  });

  uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("song-title-input").value;
    const artist = document.getElementById("song-artist-input").value;
    const movie = document.getElementById("song-movie-input").value;
    const actor = document.getElementById("song-actor-input").value;
    const category = document.getElementById("song-category-input").value;
    const audioUrl = document.getElementById("song-url-input").value;
    const coverUrl = document.getElementById("song-cover-input").value;
    const audioFileInput = document.getElementById("song-file-input");
    const coverFileInput = document.getElementById("cover-file-input");

    const formData = new FormData();
    formData.append("title", title);
    formData.append("artist", artist);
    formData.append("movie", movie);
    formData.append("actor", actor);
    formData.append("category", category);
    if (audioUrl) formData.append("audioUrl", audioUrl);
    if (coverUrl) formData.append("coverUrl", coverUrl);

    if (audioFileInput.files && audioFileInput.files[0]) {
      formData.append("audioFile", audioFileInput.files[0]);
    }
    if (coverFileInput && coverFileInput.files && coverFileInput.files[0]) {
      formData.append("coverFile", coverFileInput.files[0]);
    }

    showToast("Uploading song and publishing to catalog...", "info");
    const res = await window.musicAPI.uploadSong(formData);
    if (res.success) {
      showToast(res.message, "success");
      uploadForm.reset();
      closeModals();
      loadAndRender(category);
    } else {
      showToast(res.message, "error");
    }
  });

  // Admin Edit Song Modal Helpers
  function openEditModal(song) {
    if (!editModal) return;
    const songId = song._id || song.id;
    editSongId.value = songId;
    editSongTitle.value = song.title || "";
    editSongArtist.value = song.artist || "";
    editSongMovie.value = song.movie || "";
    editSongActor.value = song.actor || "";
    editSongCategory.value = song.category || "bollywood";
    editSongDuration.value = song.duration || "";
    editSongCover.value = song.cover || "";
    editSongUrl.value = song.url || "";
    if (editCoverFile) editCoverFile.value = "";
    if (editAudioFile) editAudioFile.value = "";
    editModal.classList.add("active");
  }

  if (editForm) {
    editForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const songId = editSongId.value;
      if (!songId) return;

      const formData = new FormData();
      formData.append("title", editSongTitle.value.trim());
      formData.append("artist", editSongArtist.value.trim());
      formData.append("movie", editSongMovie.value.trim());
      formData.append("actor", editSongActor.value.trim());
      formData.append("category", editSongCategory.value);
      formData.append("duration", editSongDuration.value.trim());
      formData.append("coverUrl", editSongCover.value.trim());
      formData.append("audioUrl", editSongUrl.value.trim());

      if (editCoverFile && editCoverFile.files && editCoverFile.files[0]) {
        formData.append("coverFile", editCoverFile.files[0]);
      }
      if (editAudioFile && editAudioFile.files && editAudioFile.files[0]) {
        formData.append("audioFile", editAudioFile.files[0]);
      }

      showToast("Saving updates to MongoDB...", "info");
      const res = await window.musicAPI.updateSong(songId, formData);
      if (res.success) {
        showToast(res.message, "success");
        closeModals();
        loadAndRender(currentCategory, searchInput.value);
      } else {
        showToast(res.message, "error");
      }
    });
  }

  // Player Bar Controls
  playPauseBtn.addEventListener("click", () => {
    window.musicPlayer.togglePlay();
  });

  prevBtn.addEventListener("click", () => {
    window.musicPlayer.prev();
  });

  nextBtn.addEventListener("click", () => {
    window.musicPlayer.next();
  });

  shuffleBtn.addEventListener("click", () => {
    const isShuffle = window.musicPlayer.toggleShuffle();
    shuffleBtn.classList.toggle("active-control", isShuffle);
    showToast(isShuffle ? "Shuffle Mode Enabled" : "Shuffle Mode Disabled", "info");
  });

  repeatBtn.addEventListener("click", () => {
    const mode = window.musicPlayer.toggleRepeat();
    repeatBtn.classList.toggle("active-control", mode !== "off");
    showToast(`Repeat Mode: ${mode.toUpperCase()}`, "info");
  });

  downloadBtn.addEventListener("click", () => {
    window.musicPlayer.downloadSong();
  });

  favoritePlayerBtn.addEventListener("click", async () => {
    const current = window.musicPlayer.getCurrentSong();
    if (!current) return;
    const currentId = current._id || current.id;
    if (window.musicAPI.isGuest()) {
      showToast("Please login to save favorite tracks!", "error");
      openAuthModal();
      return;
    }
    const res = await window.musicAPI.toggleFavorite(currentId, current);
    if (res.success) {
      updatePlayerFavState();
      loadAndRender(currentCategory, searchInput.value);
      showToast(res.isFavorite ? "Added to your Liked Songs!" : "Removed from Liked Songs", "info");
    }
  });

  progressContainer.addEventListener("click", (e) => {
    const rect = progressContainer.getBoundingClientRect();
    const percent = ((e.clientX - rect.left) / rect.width) * 100;
    window.musicPlayer.seek(percent);
  });

  volumeSlider.addEventListener("input", (e) => {
    window.musicPlayer.setVolume(e.target.value / 100);
    muteBtn.textContent = e.target.value == 0 ? "🔇" : "🔊";
  });

  muteBtn.addEventListener("click", () => {
    const isMuted = window.musicPlayer.toggleMute();
    muteBtn.textContent = isMuted ? "🔇" : "🔊";
  });

  // Custom Events from MusicPlayer
  window.addEventListener("currentSongChange", (e) => {
    const song = e.detail.song;
    let coverSrc = song.cover;
    if (song.cover && song.cover.startsWith("/")) {
      const isSeparateLiveServer = window.location.hostname === "localhost" && window.location.port !== "5000" && window.location.port !== "";
      const host = isSeparateLiveServer ? "http://localhost:5000" : "";
      coverSrc = `${host}${song.cover}`;
    }

    currentCover.src = coverSrc;
    currentTitle.textContent = song.title;
    currentArtist.textContent = song.artist;
    currentMovieActor.textContent = `${song.movie || ""} • ${song.actor || ""}`;
    updatePlayerFavState();
    renderGrid(cachedSongsList);
  });

  window.addEventListener("playerStateChange", (e) => {
    const isPlaying = e.detail.isPlaying;
    playPauseBtn.innerHTML = isPlaying ? "❚❚" : "▶";
    renderGrid(cachedSongsList);
  });

  window.addEventListener("playerTimeUpdate", (e) => {
    const { current, duration, progress } = e.detail;
    progressBar.style.width = `${progress}%`;
    currentTimeEl.textContent = formatTime(current);
    durationTimeEl.textContent = formatTime(duration);
  });

  function triggerGuestLimitModal(msg) {
    if (msg) document.getElementById("guest-limit-desc").textContent = msg;
    guestLimitModal.classList.add("active");
  }

  window.addEventListener("guestLimitReached", () => {
    triggerGuestLimitModal("You've enjoyed your 3 free guest songs! Login or create a free account to continue unlimited listening, Liked songs, and MP3 downloads.");
  });

  window.addEventListener("guestLimitExceeded", (e) => {
    triggerGuestLimitModal(e.detail && e.detail.reason);
  });

  document.getElementById("guest-login-redirect-btn").addEventListener("click", () => {
    closeModals();
    openAuthModal();
  });

  window.addEventListener("guestPlayWarning", (e) => {
    const { remaining } = e.detail;
    updateAuthUI();
    if (remaining > 0) {
      showToast(`Guest Preview: ${remaining} song(s) remaining before login is required.`, "info");
    }
  });

  window.addEventListener("playerError", (e) => {
    showToast(e.detail.message, "error");
  });

  // Initial load: 5 sections (All, Hollywood, Bollywood, Tollywood, Bhojpuri)
  updateAuthUI();
  await loadAndRender("all");
});
