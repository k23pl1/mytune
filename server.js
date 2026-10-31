require("dotenv").config();
const express = require("express");
const cors = require("cors");
const path = require("path");
const fs = require("fs");
const multer = require("multer");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const https = require("https");
const http = require("http");

const app = express();
const PORT = process.env.PORT || 5000;
const JWT_SECRET = process.env.JWT_SECRET || "aurora_music_super_secret_jwt_key_2026";

// Directories
const uploadsAudioDir = path.join(__dirname, "uploads/audio");
const uploadsCoversDir = path.join(__dirname, "uploads/covers");
const publicDir = path.join(__dirname, "public");
const DB_PATH = path.join(__dirname, "database.db");

// Ensure directories exist
[uploadsAudioDir, uploadsCoversDir, publicDir].forEach((dir) => {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

// Middleware
app.use(cors({ origin: "*" }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static assets
app.use("/uploads", express.static(path.join(__dirname, "uploads")));
app.use(express.static(publicDir));

// ==========================================
// SQLITE DATABASE INITIALIZATION & ADAPTER
// ==========================================
let dbRun, dbAll, dbGet;

try {
  const sqlite3 = require("sqlite3").verbose();
  const db = new sqlite3.Database(DB_PATH, (err) => {
    if (err) {
      console.error("❌ Failed to connect to SQLite database.db:", err.message);
    } else {
      console.log("💾 [SQLite] Connected successfully to database.db");
    }
  });

  dbRun = function (sql, params = []) {
    return new Promise((resolve, reject) => {
      db.run(sql, params, function (err) {
        if (err) reject(err);
        else resolve(this);
      });
    });
  };

  dbAll = function (sql, params = []) {
    return new Promise((resolve, reject) => {
      db.all(sql, params, (err, rows) => {
        if (err) reject(err);
        else resolve(rows || []);
      });
    });
  };

  dbGet = function (sql, params = []) {
    return new Promise((resolve, reject) => {
      db.get(sql, params, (err, row) => {
        if (err) reject(err);
        else resolve(row || null);
      });
    });
  };
} catch (nativeErr) {
  console.warn("⚠️ Native sqlite3 binding unavailable, activating Node.js built-in node:sqlite fallback:", nativeErr.message);
  const { DatabaseSync } = require("node:sqlite");
  const db = new DatabaseSync(DB_PATH);
  console.log("💾 [node:sqlite] Connected successfully to database.db via built-in engine!");

  dbRun = async function (sql, params = []) {
    const stmt = db.prepare(sql);
    const result = stmt.run(...params);
    return { lastID: result.lastInsertRowid, changes: result.changes };
  };

  dbAll = async function (sql, params = []) {
    const stmt = db.prepare(sql);
    return stmt.all(...params);
  };

  dbGet = async function (sql, params = []) {
    const stmt = db.prepare(sql);
    return stmt.get(...params) || null;
  };
}

// Initialize tables and seed defaults
async function initDatabase() {
  await dbRun(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      name TEXT,
      role TEXT DEFAULT 'user',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  await dbRun(`
    CREATE TABLE IF NOT EXISTS songs (
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      artist TEXT NOT NULL,
      movie TEXT DEFAULT '',
      actor TEXT DEFAULT '',
      category TEXT NOT NULL,
      cover TEXT DEFAULT '',
      url TEXT NOT NULL,
      duration TEXT DEFAULT '3:30',
      plays INTEGER DEFAULT 0,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  await dbRun(`
    CREATE TABLE IF NOT EXISTS favorites (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      song_id TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(user_id, song_id)
    )
  `);

  await dbRun(`
    CREATE TABLE IF NOT EXISTS playlists (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      name TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  await dbRun(`
    CREATE TABLE IF NOT EXISTS playlist_songs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      playlist_id INTEGER NOT NULL,
      song_id TEXT NOT NULL,
      UNIQUE(playlist_id, song_id)
    )
  `);

  // Ensure default admin user
  const admin = await dbGet("SELECT * FROM users WHERE username = 'admin'");
  if (!admin) {
    const salt = bcrypt.genSaltSync(10);
    const hash = bcrypt.hashSync("admin123", salt);
    await dbRun(
      "INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)",
      ["admin", hash, "Administrator", "admin"]
    );
    console.log("👤 [Seed] Created default Admin account: admin / admin123");
  }

  // Ensure default listener user
  const listener = await dbGet("SELECT * FROM users WHERE username = 'listener'");
  if (!listener) {
    const salt = bcrypt.genSaltSync(10);
    const hash = bcrypt.hashSync("user123", salt);
    await dbRun(
      "INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)",
      ["listener", hash, "Demo Listener", "user"]
    );
    console.log("👤 [Seed] Created default User account: listener / user123");
  }
}

initDatabase().catch(console.error);

// ==========================================
// MULTER FILE UPLOAD CONFIGURATION
// ==========================================
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    if (file.fieldname === "audioFile") cb(null, uploadsAudioDir);
    else if (file.fieldname === "coverFile") cb(null, uploadsCoversDir);
    else cb(new Error("Unknown field"), null);
  },
  filename: (req, file, cb) => {
    const cleanName = file.originalname.replace(/[^a-zA-Z0-9.-]/g, "_");
    cb(null, `${Date.now()}-${cleanName}`);
  }
});

const upload = multer({
  storage,
  limits: { fileSize: 50 * 1024 * 1024 } // 50 MB
});

// ==========================================
// AUTHENTICATION HELPER & MIDDLEWARE
// ==========================================
function getAuthUser(req) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith("Bearer ")) return null;
  const token = authHeader.split(" ")[1];
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (err) {
    // Fallback for base64 tokens
    try {
      const raw = Buffer.from(token, "base64").toString("ascii");
      const [id, username, role] = raw.split(":");
      return { id: parseInt(id) || id, username, role: role || "user" };
    } catch {
      return null;
    }
  }
}

function requireAuth(req, res, next) {
  const user = getAuthUser(req);
  if (!user) {
    return res.status(401).json({ success: false, message: "Authentication required" });
  }
  req.user = user;
  next();
}

function requireAdmin(req, res, next) {
  const user = getAuthUser(req);
  if (!user || user.role !== "admin") {
    return res.status(403).json({ success: false, message: "Admin privileges required" });
  }
  req.user = user;
  next();
}

// ==========================================
// AUTH ROUTES
// ==========================================

// Register
app.post("/api/auth/register", async (req, res) => {
  try {
    const { username, password, name, role } = req.body;
    if (!username || !password) {
      return res.status(400).json({ success: false, message: "Username and password are required" });
    }

    const cleanUsername = username.trim().toLowerCase();
    const existing = await dbGet("SELECT * FROM users WHERE username = ?", [cleanUsername]);
    if (existing) {
      return res.status(400).json({ success: false, message: "Username is already taken" });
    }

    const userRole = role === "admin" ? "admin" : "user";
    const salt = bcrypt.genSaltSync(10);
    const hash = bcrypt.hashSync(password, salt);

    const result = await dbRun(
      "INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)",
      [cleanUsername, hash, name || cleanUsername, userRole]
    );

    const user = {
      id: result.lastID,
      username: cleanUsername,
      name: name || cleanUsername,
      role: userRole,
      favorites: []
    };

    const token = jwt.sign(user, JWT_SECRET, { expiresIn: "30d" });
    res.json({ success: true, message: "Registration successful!", user, token });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// Login
app.post("/api/auth/login", async (req, res) => {
  try {
    const { username, password } = req.body;
    if (!username || !password) {
      return res.status(400).json({ success: false, message: "Username and password are required" });
    }

    const cleanUsername = username.trim().toLowerCase();
    const userRow = await dbGet("SELECT * FROM users WHERE username = ?", [cleanUsername]);
    if (!userRow) {
      return res.status(401).json({ success: false, message: "Invalid username or password" });
    }

    const isMatch = bcrypt.compareSync(password, userRow.password);
    if (!isMatch) {
      return res.status(401).json({ success: false, message: "Invalid username or password" });
    }

    // Fetch user favorites
    const favRows = await dbAll("SELECT song_id FROM favorites WHERE user_id = ?", [userRow.id]);
    const favorites = favRows.map(r => r.song_id);

    const user = {
      id: userRow.id,
      username: userRow.username,
      name: userRow.name || userRow.username,
      role: userRow.role,
      favorites
    };

    const token = jwt.sign(user, JWT_SECRET, { expiresIn: "30d" });
    res.json({ success: true, message: `Welcome back, ${user.name}!`, user, token });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// Get Current User Profile & Favorites
app.get("/api/auth/me", async (req, res) => {
  try {
    const auth = getAuthUser(req);
    if (!auth) {
      return res.json({ success: false, user: null });
    }

    const userRow = await dbGet("SELECT id, username, name, role, created_at FROM users WHERE id = ?", [auth.id]);
    if (!userRow) {
      return res.json({ success: false, user: null });
    }

    const favRows = await dbAll("SELECT song_id FROM favorites WHERE user_id = ?", [userRow.id]);
    const favorites = favRows.map(r => r.song_id);

    res.json({
      success: true,
      user: {
        id: userRow.id,
        username: userRow.username,
        name: userRow.name,
        role: userRow.role,
        favorites
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// ==========================================
// SONGS ROUTES (All, Hollywood, Bollywood, Tollywood, Bhojpuri & Search)
// ==========================================

// Helper: Handle Song Queries
async function querySongs(req) {
  let { category, search, playlist } = req.query;
  let sql = "SELECT * FROM songs WHERE 1=1";
  const params = [];

  // Playlist filter (e.g., Emraan Hashmi or T-Series)
  if (playlist === "emraan") {
    sql += " AND (lower(actor) LIKE '%emraan%' OR lower(movie) IN ('jannat', 'murder 2', 'zeher', 'tum mile', 'gangster', 'raaz', 'crook', 'awarapan'))";
  } else if (playlist === "tseries") {
    sql += " AND (lower(artist) LIKE '%arijit%' OR lower(artist) LIKE '%jubin%' OR lower(artist) LIKE '%atif%' OR lower(movie) IN ('animal', 'shershaah', 'kabir singh', 'luka chuppi'))";
  } else if (category && category !== "all" && category !== "undefined" && category !== "favorites") {
    sql += " AND lower(category) = lower(?)";
    params.push(category.trim());
  }

  // Deep search across Title, Artist, Movie, Actor, Category
  if (search && search.trim()) {
    const q = `%${search.trim().toLowerCase()}%`;
    sql += " AND (lower(title) LIKE ? OR lower(artist) LIKE ? OR lower(movie) LIKE ? OR lower(actor) LIKE ? OR lower(category) LIKE ?)";
    params.push(q, q, q, q, q);
  }

  sql += " ORDER BY created_at DESC";
  return await dbAll(sql, params);
}

// Get Songs (Supports both direct array and { success: true, songs })
app.get("/api/songs", async (req, res) => {
  try {
    const rows = await querySongs(req);
    // Respond with both structures for frontend backwards-compatibility
    res.json({ success: true, count: rows.length, songs: rows });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// Get single song by ID
app.get("/api/songs/:id", async (req, res) => {
  try {
    const song = await dbGet("SELECT * FROM songs WHERE id = ?", [req.params.id]);
    if (!song) return res.status(404).json({ success: false, message: "Song not found" });
    res.json({ success: true, song });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// Upload Handler Function
async function handleUpload(req, res) {
  try {
    const { title, artist, movie, actor, category, duration, coverUrl, audioUrl } = req.body;

    if (!title || !artist || !category) {
      return res.status(400).json({ success: false, message: "Title, artist, and category are required" });
    }

    let finalAudioUrl = "";
    if (req.files && req.files["audioFile"] && req.files["audioFile"][0]) {
      finalAudioUrl = `/uploads/audio/${req.files["audioFile"][0].filename}`;
    } else if (audioUrl && audioUrl.trim()) {
      finalAudioUrl = audioUrl.trim();
    } else {
      return res.status(400).json({ success: false, message: "Please provide an audio file or direct audio stream URL" });
    }

    let finalCoverUrl = "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600";
    if (req.files && req.files["coverFile"] && req.files["coverFile"][0]) {
      finalCoverUrl = `/uploads/covers/${req.files["coverFile"][0].filename}`;
    } else if (coverUrl && coverUrl.trim()) {
      finalCoverUrl = coverUrl.trim();
    }

    const newId = `song-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`;
    const songCat = category.trim().toLowerCase();

    await dbRun(`
      INSERT INTO songs (id, title, artist, movie, actor, category, cover, url, duration, plays)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
    `, [
      newId,
      title.trim(),
      artist.trim(),
      movie ? movie.trim() : "",
      actor ? actor.trim() : "",
      songCat,
      finalCoverUrl,
      finalAudioUrl,
      duration || "3:30"
    ]);

    const createdSong = await dbGet("SELECT * FROM songs WHERE id = ?", [newId]);
    res.status(201).json({ success: true, message: "Song published successfully to database.db!", song: createdSong });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
}

// Admin Upload Song Endpoints
app.post("/api/songs", requireAdmin, upload.fields([{ name: "audioFile", maxCount: 1 }, { name: "coverFile", maxCount: 1 }]), handleUpload);
app.post("/api/songs/upload", requireAdmin, upload.fields([{ name: "audioFile", maxCount: 1 }, { name: "coverFile", maxCount: 1 }]), handleUpload);

// Admin Update Song
app.put("/api/songs/:id", requireAdmin, upload.fields([{ name: "audioFile", maxCount: 1 }, { name: "coverFile", maxCount: 1 }]), async (req, res) => {
  try {
    const songId = req.params.id;
    const existing = await dbGet("SELECT * FROM songs WHERE id = ?", [songId]);
    if (!existing) return res.status(404).json({ success: false, message: "Song not found" });

    const { title, artist, movie, actor, category, duration, cover, url } = req.body;

    let finalAudioUrl = existing.url;
    if (req.files && req.files["audioFile"] && req.files["audioFile"][0]) {
      finalAudioUrl = `/uploads/audio/${req.files["audioFile"][0].filename}`;
    } else if (url && url.trim()) {
      finalAudioUrl = url.trim();
    }

    let finalCoverUrl = existing.cover;
    if (req.files && req.files["coverFile"] && req.files["coverFile"][0]) {
      finalCoverUrl = `/uploads/covers/${req.files["coverFile"][0].filename}`;
    } else if (cover && cover.trim()) {
      finalCoverUrl = cover.trim();
    }

    await dbRun(`
      UPDATE songs SET
        title = ?,
        artist = ?,
        movie = ?,
        actor = ?,
        category = ?,
        cover = ?,
        url = ?,
        duration = ?
      WHERE id = ?
    `, [
      title ? title.trim() : existing.title,
      artist ? artist.trim() : existing.artist,
      movie !== undefined ? movie.trim() : existing.movie,
      actor !== undefined ? actor.trim() : existing.actor,
      category ? category.trim().toLowerCase() : existing.category,
      finalCoverUrl,
      finalAudioUrl,
      duration || existing.duration,
      songId
    ]);

    const updated = await dbGet("SELECT * FROM songs WHERE id = ?", [songId]);
    res.json({ success: true, message: "Song updated successfully in database.db!", song: updated });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// Admin Delete Song
app.delete("/api/songs/:id", requireAdmin, async (req, res) => {
  try {
    const songId = req.params.id;
    const song = await dbGet("SELECT * FROM songs WHERE id = ?", [songId]);
    if (!song) return res.status(404).json({ success: false, message: "Song not found" });

    // Remove local file if stored in uploads
    if (song.url && song.url.startsWith("/uploads/audio/")) {
      const filePath = path.join(__dirname, song.url);
      if (fs.existsSync(filePath)) {
        try { fs.unlinkSync(filePath); } catch (e) { console.warn("Could not delete audio file:", e.message); }
      }
    }

    await dbRun("DELETE FROM songs WHERE id = ?", [songId]);
    await dbRun("DELETE FROM favorites WHERE song_id = ?", [songId]);
    await dbRun("DELETE FROM playlist_songs WHERE song_id = ?", [songId]);

    res.json({ success: true, message: `"${song.title}" deleted from database.db` });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// ==========================================
// FAVORITES (LIKED SONGS) ROUTES
// ==========================================

// Toggle favorite handler
async function handleToggleFavorite(userId, songId) {
  const existing = await dbGet("SELECT * FROM favorites WHERE user_id = ? AND song_id = ?", [userId, songId]);
  let favorited = false;

  if (existing) {
    await dbRun("DELETE FROM favorites WHERE user_id = ? AND song_id = ?", [userId, songId]);
    favorited = false;
  } else {
    await dbRun("INSERT INTO favorites (user_id, song_id) VALUES (?, ?)", [userId, songId]);
    favorited = true;
  }

  const favRows = await dbAll("SELECT song_id FROM favorites WHERE user_id = ?", [userId]);
  const favorites = favRows.map(r => r.song_id);

  return { favorited, favorites };
}

app.post("/api/favorites/toggle", requireAuth, async (req, res) => {
  try {
    const { songId } = req.body;
    if (!songId) return res.status(400).json({ success: false, message: "songId is required" });
    const result = await handleToggleFavorite(req.user.id, songId);
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

app.post("/api/favorites/:songId", requireAuth, async (req, res) => {
  try {
    const result = await handleToggleFavorite(req.user.id, req.params.songId);
    res.json({ success: true, ...result });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// Get user's favorites
app.get("/api/favorites", requireAuth, async (req, res) => {
  try {
    const userId = req.user.id;
    const rows = await dbAll(`
      SELECT s.* FROM songs s
      JOIN favorites f ON s.id = f.song_id
      WHERE f.user_id = ?
      ORDER BY f.created_at DESC
    `, [userId]);
    res.json({ success: true, songs: rows });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// ==========================================
// ADMIN DASHBOARD & STATS ROUTES
// ==========================================

// Get all registered users (Admin only)
app.get("/api/admin/users", requireAdmin, async (req, res) => {
  try {
    const users = await dbAll("SELECT id, username, name, role, created_at FROM users ORDER BY created_at DESC");
    res.json({ success: true, users });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// Get database analytics & statistics (Admin only)
app.get("/api/admin/stats", requireAdmin, async (req, res) => {
  try {
    const totalUsers = (await dbGet("SELECT count(*) as count FROM users")).count;
    const totalSongs = (await dbGet("SELECT count(*) as count FROM songs")).count;
    const categoryStats = await dbAll("SELECT category, count(*) as count FROM songs GROUP BY category");

    res.json({
      success: true,
      stats: {
        totalUsers,
        totalSongs,
        categories: categoryStats
      }
    });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

// ==========================================
// SONG DOWNLOAD ROUTE
// ==========================================
function streamOrDownload(song, res) {
  const safeTitle = (song.title + " - " + song.artist).replace(/[^a-zA-Z0-9_\- ]/g, "").trim();
  const filename = `${safeTitle}.mp3`;

  if (song.url.startsWith("/uploads/audio/")) {
    const filePath = path.join(__dirname, song.url);
    if (fs.existsSync(filePath)) {
      res.download(filePath, filename);
      return;
    }
  }

  // External stream download proxy
  res.setHeader("Content-Disposition", `attachment; filename="${filename}"`);
  res.setHeader("Content-Type", "audio/mpeg");

  const client = song.url.startsWith("https") ? https : http;
  client.get(song.url, (streamRes) => {
    streamRes.pipe(res);
  }).on("error", () => {
    res.redirect(song.url);
  });
}

app.get("/api/download/:id", async (req, res) => {
  try {
    const song = await dbGet("SELECT * FROM songs WHERE id = ?", [req.params.id]);
    if (!song) return res.status(404).send("Song not found");
    streamOrDownload(song, res);
  } catch (err) {
    res.status(500).send("Error initiating download");
  }
});

app.get("/api/songs/download", async (req, res) => {
  try {
    const { id, url, title, artist } = req.query;
    if (id) {
      const song = await dbGet("SELECT * FROM songs WHERE id = ?", [id]);
      if (song) return streamOrDownload(song, res);
    }
    if (url) {
      return streamOrDownload({ url, title: title || "Track", artist: artist || "Artist" }, res);
    }
    res.status(400).send("Song ID or URL required");
  } catch (err) {
    res.status(500).send("Error downloading track");
  }
});

// Audio Stream CORS Proxy (for Web Audio API visualizer on external audio)
app.get("/api/songs/stream", (req, res) => {
  const targetUrl = req.query.url;
  if (!targetUrl) return res.status(400).send("Target URL required");

  const client = targetUrl.startsWith("https") ? https : http;
  client.get(targetUrl, (audioStream) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Content-Type", audioStream.headers["content-type"] || "audio/mpeg");
    if (audioStream.headers["content-length"]) {
      res.setHeader("Content-Length", audioStream.headers["content-length"]);
    }
    audioStream.pipe(res);
  }).on("error", (err) => {
    res.status(500).send("Proxy error: " + err.message);
  });
});

// Start Server
app.listen(PORT, () => {
  console.log(`\n======================================================`);
  console.log(`🎵 MYTUNE MUSIC PLAYER RUNNING WITH SQLITE (database.db)!`);
  console.log(`🌐 Local URL:  http://localhost:${PORT}`);
  console.log(`📁 Database:   ${DB_PATH}`);
  console.log(`👑 Admin Auth: admin / admin123`);
  console.log(`👤 User Auth:  listener / user123`);
  console.log(`======================================================\n`);
});
