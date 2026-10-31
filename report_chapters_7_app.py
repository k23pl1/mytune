# -*- coding: utf-8 -*-
"""
Chapter 7, Chapter 8, and Appendices Content Definitions
MyTune Project Report - Kuldeep Pal (Roll No: 35)
"""

CHAPTERS_7_TO_APP = []

# ================= PAGE 41: CHAPTER 7 - CONCLUSION & FUTURE WORK (PART 1) =================
CHAPTERS_7_TO_APP.append({
    "page_num": 41,
    "chapter": "Chapter 7",
    "title": "CHAPTER 7: CONCLUSION AND FUTURE WORK",
    "sections": [
        {
            "num": "7.1",
            "title": "Concluding Summary & Operational Significance",
            "content": (
                "The MyTune engineering project successfully conceptualized, designed, implemented, and deployed an advanced, "
                "lightweight, audio-reactive web music streaming platform. By harmonizing modern web technologies—the W3C Web Audio API, "
                "HTML5 Canvas, asynchronous JavaScript, Node.js/Express microservices, and resilient dual-engine SQLite persistence—the "
                "system bridges the gap between high-fidelity digital audio playback and dynamic visual interactivity.\n\n"
                "The implemented platform delivers several notable technical milestones:\n"
                "1. Zero-Install Audio Reactivity: The browser natively performs real-time Fast Fourier Transform (FFT) frequency "
                "decomposition on incoming audio streams, dynamically modulating canvas spectrum visualizers and ambient background glow "
                "without relying on heavy third-party plugins or external graphic shaders.\n"
                "2. Resilient Cloud-Ready Persistence: The dual-engine SQLite persistence architecture completely eliminates host-level "
                "Linux binary incompatibilities (GLIBC 2.38 errors), ensuring flawless execution across diverse local and cloud environments.\n"
                "3. Multi-Cultural Musical Curation: The platform categorizes music into five specialized hubs—All, Hollywood, Bollywood, "
                "Tollywood, and Bhojpuri—providing a culturally diverse audio catalog for global and regional listeners.\n"
                "4. Balanced Monetization & Frictionless Preview: The 3-song guest preview limiter allows unauthenticated visitors to test "
                "audio quality and interface aesthetics immediately, driving organic user registration without intrusive upfront barriers.\n"
                "5. Verified Public Production Deployment: The system is deployed and publicly accessible 24/7 on Render Cloud "
                "(https://mytune-music.onrender.com/), sustained by automated keep-awake telemetry."
            )
        }
    ]
})

# ================= PAGE 42: CHAPTER 7 - CONCLUSION & FUTURE WORK (PART 2) =================
CHAPTERS_7_TO_APP.append({
    "page_num": 42,
    "chapter": "Chapter 7",
    "title": "CHAPTER 7: LIMITATIONS & FUTURE ROADMAP",
    "sections": [
        {
            "num": "7.2",
            "title": "System Limitations",
            "content": (
                "While MyTune satisfies all primary engineering requirements, certain architectural limitations exist:\n"
                "• Monolithic Single-Node Storage: Audio binaries and SQLite files reside on the local container filesystem. On ephemeral "
                "cloud instances without persistent volume attachments, dynamically uploaded songs are purged upon container redeployment.\n"
                "• Absence of Offline Service Worker Caching: The client application currently requires active Internet connectivity to "
                "stream audio; client-side IndexedDB caching for offline Progressive Web App (PWA) playback is not yet implemented.\n"
                "• Lossy MP3 Encoding Only: The player currently streams standard 128/320 kbps MP3 streams; lossless FLAC or adaptive bitrate "
                "streaming (HLS / DASH) is not yet integrated."
            )
        },
        {
            "num": "7.3",
            "title": "Future Enhancement Roadmap",
            "content": (
                "Future research and development iterations will focus on the following enhancements:\n"
                "1. Object Storage & CDN Integration: Migrate audio file storage to AWS S3 or Cloudflare R2 paired with global CDN distribution "
                "for multi-region caching and infinite horizontal media scaling.\n"
                "2. Progressive Web App (PWA) Offline Mode: Implement Service Workers with Cache API and IndexedDB to cache user-favorite "
                "tracks for zero-data offline playback.\n"
                "3. Adaptive Bitrate Streaming (HLS / MPEG-DASH): Implement FFmpeg server-side transcoding to generate multi-bitrate HLS streams, "
                "automatically adapting audio quality to fluctuating mobile network bandwidths.\n"
                "4. Collaborative Real-Time Listening Rooms: Integrate WebSockets (Socket.io) to enable synchronized multi-user audio listening "
                "and shared playlist authoring across remote participants."
            )
        }
    ]
})

# ================= PAGE 43: CHAPTER 8 - REFERENCES & GLOSSARY =================
CHAPTERS_7_TO_APP.append({
    "page_num": 43,
    "chapter": "Chapter 8",
    "title": "CHAPTER 8: REFERENCES & TECHNICAL GLOSSARY",
    "sections": [
        {
            "num": "8.1",
            "title": "Academic & Technical References",
            "content": (
                "[1] W3C Web Audio API Specification. World Wide Web Consortium (W3C) Recommendation, 2021. https://www.w3.org/TR/webaudio/\n"
                "[2] Fielding, R., et al. Hypertext Transfer Protocol (HTTP/1.1): Range Requests. RFC 7233, Internet Engineering Task Force, 2014.\n"
                "[3] Crockford, D. JavaScript: The Good Parts. O'Reilly Media, 2008.\n"
                "[4] Tilkov, S., & Vinoski, S. Node.js: Using JavaScript to Build High-Performance Network Programs. IEEE Internet Computing, 14(6), 2010.\n"
                "[5] Hipp, D. R. SQLite: An Embeddable SQL Database Engine. Software: Practice and Experience, 2020.\n"
                "[6] MDN Web Docs. Visualizations with Web Audio API. Mozilla Developer Network, 2023.\n"
                "[7] Resig, J., & Bibeault, B. Secrets of the JavaScript Ninja. Manning Publications, 2016."
            )
        },
        {
            "num": "8.2",
            "title": "Technical Glossary of Terms",
            "content": (
                "• AnalyserNode: A Web Audio API node providing real-time frequency and time-domain analysis via Fast Fourier Transforms.\n"
                "• FFT (Fast Fourier Transform): An algorithmic formulation computing the Discrete Fourier Transform of an audio sample buffer.\n"
                "• frequencyBinCount: An unsigned integer representing half the FFT size, defining the number of discrete data points.\n"
                "• smoothingTimeConstant: An averaging constant (0 to 1) smoothing changes between successive analysis frames.\n"
                "• HTTP 206 Partial Content: HTTP status indicating that the server is fulfilling a partial byte-range request.\n"
                "• bcrypt: A cryptographic password-hashing function based on the Blowfish cipher incorporating automated salting.\n"
                "• GLIBC: The GNU C Library, the fundamental system C library utilized across Linux distributions.\n"
                "• Render PaaS: A cloud platform-as-a-service provider offering automated containerized web service hosting.\n"
                "• Glassmorphism: A modern user interface design trend characterized by translucent frosted-glass backgrounds and subtle borders.\n"
                "• requestAnimationFrame: A browser API signaling the intention to execute an animation prior to the next screen repaint."
            )
        }
    ]
})

# ================= PAGE 44: APPENDIX A - COMPLETE REST API SPECIFICATION =================
CHAPTERS_7_TO_APP.append({
    "page_num": 44,
    "chapter": "Appendix A",
    "title": "APPENDIX A: COMPLETE REST API SPECIFICATION",
    "sections": [
        {
            "num": "A.1",
            "title": "Comprehensive RESTful Endpoint Architecture",
            "content": "The complete catalog of REST API endpoints exposed by the Node.js/Express backend is documented below:"
        }
    ],
    "tables": [
        {
            "caption": "Table A.1: Complete REST API Endpoints Specification",
            "headers": ["Method", "Endpoint Route", "Auth / Role", "Payload Parameters", "Expected Response Status"],
            "rows": [
                ["GET", "/api/songs", "Public (Guest)", "None", "200 OK: Array of all song objects"],
                ["GET", "/api/songs/category/:cat", "Public (Guest)", "cat in URL", "200 OK: Filtered array of category songs"],
                ["GET", "/api/songs/:id/stream", "Public (Guest Limit)", "Range Header", "206 Partial Content: Audio binary stream"],
                ["POST", "/api/auth/register", "Public", "username, password", "201 Created: { success, user, token }"],
                ["POST", "/api/auth/login", "Public", "username, password", "200 OK: { success, user, token }"],
                ["GET", "/api/likes", "User (Bearer)", "Token header", "200 OK: Array of user's favorited songs"],
                ["POST", "/api/likes/toggle", "User (Bearer)", "song_id (JSON)", "200 OK: { liked: true/false }"],
                ["GET", "/api/admin/stats", "Admin Only", "Token header", "200 OK: { usersCount, songsCount, playsCount }"],
                ["POST", "/api/admin/songs", "Admin Only", "Multer: audio, cover", "201 Created: New song record"],
                ["DELETE", "/api/admin/songs/:id", "Admin Only", "id in URL", "200 OK: { success: true }"],
                ["GET", "/api/ping", "Public (Cron)", "None", "200 OK: { status: 'alive', time: timestamp }"]
            ]
        }
    ]
})

# ================= PAGE 45: APPENDIX B & C - SCHEMA DDL & OPERATIONAL MANUAL =================
CHAPTERS_7_TO_APP.append({
    "page_num": 45,
    "chapter": "Appendix B & C",
    "title": "APPENDIX B: DATABASE SCHEMA DDL & APPENDIX C: USER MANUAL",
    "sections": [
        {
            "num": "B.1",
            "title": "Appendix B: Complete SQLite Relational Schema DDL",
            "content": (
                "CREATE TABLE IF NOT EXISTS users (\n"
                "  id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                "  username TEXT UNIQUE NOT NULL,\n"
                "  password TEXT NOT NULL,\n"
                "  role TEXT NOT NULL DEFAULT 'user',\n"
                "  created_at DATETIME DEFAULT CURRENT_TIMESTAMP\n"
                ");\n\n"
                "CREATE TABLE IF NOT EXISTS songs (\n"
                "  id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                "  title TEXT NOT NULL,\n"
                "  artist TEXT NOT NULL DEFAULT 'Unknown Artist',\n"
                "  category TEXT NOT NULL DEFAULT 'Hollywood',\n"
                "  file_path TEXT NOT NULL,\n"
                "  cover_path TEXT DEFAULT '/uploads/covers/default.jpg',\n"
                "  duration INTEGER DEFAULT 0,\n"
                "  plays INTEGER DEFAULT 0,\n"
                "  created_at DATETIME DEFAULT CURRENT_TIMESTAMP\n"
                ");\n\n"
                "CREATE TABLE IF NOT EXISTS likes (\n"
                "  id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                "  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,\n"
                "  song_id INTEGER NOT NULL REFERENCES songs(id) ON DELETE CASCADE,\n"
                "  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,\n"
                "  UNIQUE(user_id, song_id)\n"
                ");"
            )
        },
        {
            "num": "C.1",
            "title": "Appendix C: End-User & Administrator Operational Manual",
            "content": (
                "1. Accessing Public Application: Open any modern web browser and navigate to: https://mytune-music.onrender.com/\n"
                "2. Browsing Music: Click any category in the sidebar (All, Hollywood, Bollywood, Tollywood, Bhojpuri) to explore tracks.\n"
                "3. Audio Playback & Visualizer: Click the play overlay on any track card. The bottom player dock displays metadata, "
                "playback scrubber, and audio visualizer. Ambient background glow reacts to rhythm.\n"
                "4. Guest Preview Notice: Guests enjoy 3 free tracks. On track 4, a login modal prompts registration or sign-in.\n"
                "5. Favoriting Tracks: Click the heart icon on any card to add it to 'Liked Songs' (requires user login).\n"
                "6. Downloading Music: Click the download icon on the player dock to save the high-definition MP3 file locally.\n"
                "7. Admin Access: Log in with admin credentials and navigate to /admin.html to upload tracks or audit users."
            )
        }
    ]
})

print("Chapters 7 to Appendices defined successfully (Pages 41 to 45).")
