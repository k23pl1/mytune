// API Client for connecting Frontend to Node.js REST Backend & Free Music API

class MusicAPI {
  constructor() {
    const isLiveServer = window.location.port !== "5000";
    this.baseUrl = isLiveServer ? "http://localhost:5000/api" : "/api";
    this.tokenKey = "mytune_jwt_token_v1";
    this.cachedUserKey = "mytune_cached_user_v1";
    this.guestCountKey = "mytune_guest_song_count_v1";
    this.maxGuestPlays = 3;
  }

  getToken() {
    return localStorage.getItem(this.tokenKey);
  }

  setToken(token) {
    if (token) {
      localStorage.setItem(this.tokenKey, token);
    } else {
      localStorage.removeItem(this.tokenKey);
    }
  }

  getCachedUser() {
    try {
      return JSON.parse(localStorage.getItem(this.cachedUserKey));
    } catch {
      return null;
    }
  }

  setCachedUser(user) {
    if (user) {
      localStorage.setItem(this.cachedUserKey, JSON.stringify(user));
    } else {
      localStorage.removeItem(this.cachedUserKey);
    }
  }

  isLoggedIn() {
    return !!this.getToken();
  }

  isAdmin() {
    const user = this.getCachedUser();
    return user && user.role === "admin";
  }

  isGuest() {
    return !this.isLoggedIn();
  }

  getGuestPlays() {
    return parseInt(localStorage.getItem(this.guestCountKey) || "0", 10);
  }

  incrementGuestPlay() {
    const count = this.getGuestPlays() + 1;
    localStorage.setItem(this.guestCountKey, count.toString());
    return count;
  }

  canPlaySong() {
    if (this.isLoggedIn()) {
      return { allowed: true, remaining: Infinity };
    }
    const plays = this.getGuestPlays();
    const maxPlays = 3; // 2-4 song limit for guest preview
    if (plays >= maxPlays) {
      return { allowed: false, remaining: 0, reason: "limit_reached" };
    }
    return { allowed: true, remaining: maxPlays - plays };
  }

  async getAdminStats() {
    if (!this.isAdmin()) return null;
    try {
      const res = await fetch(`${this.baseUrl}/admin/stats`, {
        headers: { Authorization: `Bearer ${this.getToken()}` }
      });
      return await res.json();
    } catch {
      return null;
    }
  }

  async getAdminUsers() {
    if (!this.isAdmin()) return null;
    try {
      const res = await fetch(`${this.baseUrl}/admin/users`, {
        headers: { Authorization: `Bearer ${this.getToken()}` }
      });
      return await res.json();
    } catch {
      return null;
    }
  }

  // --- Auth Endpoints ---
  async login(username, password) {
    try {
      const res = await fetch(`${this.baseUrl}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (data.success) {
        this.setToken(data.token);
        this.setCachedUser(data.user);
      }
      return data;
    } catch (err) {
      return { success: false, message: "Could not connect to Node.js backend. Make sure 'npm start' is running." };
    }
  }

  async register(username, password, name = "", role = "user") {
    try {
      const res = await fetch(`${this.baseUrl}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password, name, role })
      });
      const data = await res.json();
      if (data.success) {
        this.setToken(data.token);
        this.setCachedUser(data.user);
      }
      return data;
    } catch (err) {
      return { success: false, message: "Could not connect to Node.js backend. Make sure 'npm start' is running." };
    }
  }

  async getMe() {
    if (!this.getToken()) return null;
    try {
      const res = await fetch(`${this.baseUrl}/auth/me`, {
        headers: { Authorization: `Bearer ${this.getToken()}` }
      });
      const data = await res.json();
      if (data.success) {
        this.setCachedUser(data.user);
        return data.user;
      }
      return null;
    } catch {
      return this.getCachedUser();
    }
  }

  logout() {
    this.setToken(null);
    this.setCachedUser(null);
  }

  async toggleFavorite(songId, songData = null) {
    if (this.isGuest()) {
      return { success: false, message: "Please login to save songs to favorites!" };
    }
    try {
      const res = await fetch(`${this.baseUrl}/favorites/toggle`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.getToken()}`
        },
        body: JSON.stringify({ songId, songData })
      });
      const data = await res.json();
      if (data.success) {
        const user = this.getCachedUser();
        if (user) {
          user.favorites = data.favorites;
          this.setCachedUser(user);
        }
      }
      return data;
    } catch (err) {
      return { success: false, message: "Network error saving favorite." };
    }
  }

  // --- Song Endpoints ---
  async getSongs(category = "all", search = "", playlist = "") {
    try {
      const params = new URLSearchParams();
      if (playlist) {
        params.append("playlist", playlist);
      } else if (category && category !== "all" && category !== "favorites") {
        params.append("category", category);
      }
      if (search && search.trim() !== "") {
        params.append("search", search.trim());
      }

      const res = await fetch(`${this.baseUrl}/songs?${params.toString()}`);
      const data = await res.json();
      return data.success ? data.songs : [];
    } catch (err) {
      console.warn("API error fetching local songs:", err);
      return [];
    }
  }

  async getPlaylists() {
    try {
      const res = await fetch(`${this.baseUrl}/playlists`);
      const data = await res.json();
      return data.success ? data.playlists : [];
    } catch (err) {
      console.warn("API error fetching playlists:", err);
      return [];
    }
  }

  // --- Free Music API Integration Endpoints ---
  async searchFreeMusicOnline(query) {
    if (!query || !query.trim()) return [];
    try {
      const res = await fetch(`${this.baseUrl}/free-music/search?q=${encodeURIComponent(query.trim())}`);
      const data = await res.json();
      return data.success ? data.songs : [];
    } catch (err) {
      console.warn("Free music search error:", err);
      return [];
    }
  }

  async getFreeMusicTrending(category) {
    try {
      const res = await fetch(`${this.baseUrl}/free-music/trending?category=${encodeURIComponent(category)}`);
      const data = await res.json();
      return data.success ? data.songs : [];
    } catch (err) {
      console.warn("Free music trending error:", err);
      return [];
    }
  }

  // --- Upload & Admin Endpoints ---
  async uploadSong(formData) {
    if (this.isGuest()) {
      return { success: false, message: "Please login to upload songs to Tarang!" };
    }
    try {
      const res = await fetch(`${this.baseUrl}/songs/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${this.getToken()}`
        },
        body: formData
      });
      return await res.json();
    } catch (err) {
      return { success: false, message: "Network error uploading song: " + err.message };
    }
  }

  async updateSong(songId, dataOrFormData) {
    if (!this.isAdmin()) {
      return { success: false, message: "Only administrators can edit song details!" };
    }
    try {
      const isFormData = dataOrFormData instanceof FormData;
      const headers = {
        Authorization: `Bearer ${this.getToken()}`
      };
      if (!isFormData) {
        headers["Content-Type"] = "application/json";
      }

      const res = await fetch(`${this.baseUrl}/songs/${songId}`, {
        method: "PUT",
        headers,
        body: isFormData ? dataOrFormData : JSON.stringify(dataOrFormData)
      });
      return await res.json();
    } catch (err) {
      return { success: false, message: "Network error updating song: " + err.message };
    }
  }

  async deleteSong(songId) {
    if (!this.isAdmin()) {
      return { success: false, message: "Only administrators can delete songs!" };
    }
    try {
      const res = await fetch(`${this.baseUrl}/songs/${songId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${this.getToken()}`
        }
      });
      return await res.json();
    } catch (err) {
      return { success: false, message: "Network error deleting song." };
    }
  }

  getDownloadUrl(song) {
    const isLiveServer = window.location.port !== "5000";
    const host = isLiveServer ? "http://localhost:5000" : "";
    const params = new URLSearchParams({
      id: song.id || song._id || "",
      url: song.url || "",
      title: song.title || "Track",
      artist: song.artist || "Artist"
    });
    return `${host}/api/songs/download?${params.toString()}`;
  }
}

window.musicAPI = new MusicAPI();
