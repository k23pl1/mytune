# 🎵 MyTune - Modern Audio-Reactive Web Music Player

MyTune is a modern, responsive web music player built with **HTML5, CSS3, Vanilla JavaScript, Node.js (Express), and SQLite (`database.db`)**.

---

## 🌟 Key Features

1. **5 Dedicated Music Sections**:
   - 🌐 **All Music**: Full catalog across all genres and industries.
   - 🎬 **Hollywood**: Global pop, cinematic hits & international charts.
   - ✨ **Bollywood**: Soulful melodies, romantic songs & commercial hits.
   - 🔥 **Tollywood**: Southern grooves, dance beats & power tracks.
   - 🥁 **Bhojpuri**: High-energy regional dhamaal & festival anthems.
   - ♥ **Liked Songs (Favorites)**: Personal library saved to SQLite.

2. **Audio-Reactive Ambient Background (`visualizer.js`)**:
   - Powered by the browser's **Web Audio API** (`AudioContext` & `AnalyserNode`).
   - Analyzes audio frequencies (bass, mid, treble) in real time.
   - Pulses ambient background glow and fluid gradients to the music rhythm while playing.
   - **When paused or stopped**, the background smoothly transitions back to a clean, simple dark state.

3. **Multi-Field Search Bar**:
   - Instant search filtering by **Song Title**, **Artist / Singer**, **Featured Actor / Cast**, **Movie / Album Name**, and **Category**.

4. **Multi-Tier Access Control**:
   - **Guest Mode**: 3-song preview limit. Prompts user to log in when the limit is reached.
   - **User Mode**: Unlimited music streaming, toggle Liked Songs (Favorites), and download tracks.
   - **Admin Mode**:
     - **Admin Dashboard**: View total registered users, user details, and songs catalog breakdown.
     - **Upload Songs**: Upload audio files (`.mp3`) and cover artwork directly to `database.db`.
     - **Edit & Delete Songs**: Modify song information or remove songs from the database.

5. **Direct MP3 Download**:
   - Download any song directly as an `.mp3` file to your computer.

---

## 🏗️ Clean Project Structure

```text
mytune/
│
├── package.json         # Project dependencies & scripts
├── server.js            # Node.js backend (Express + SQLite database.db)
├── database.db          # Self-contained SQLite relational database
│
├── public/              # Frontend Client
│   ├── index.html       # Webpage UI with 5 categories & audio player dock
│   ├── css/
│   │   └── style.css    # Modern dark/glassmorphic responsive stylesheet
│   └── js/
│       ├── api.js       # REST client & guest play limitation logic
│       ├── visualizer.js# Web Audio API real-time frequency analysis
│       ├── player.js    # Audio player queue, state & download engine
│       └── app.js       # Category navigation, search & modal controller
│
└── uploads/             # Stored audio files and cover art
    ├── audio/           # Uploaded .mp3 files
    └── covers/          # Uploaded album covers
```

---

## 🚀 How to Run in VS Code

1. Open VS Code:
   `File` > `Open Folder...` > Select the `mytune` folder.

2. Open the terminal (`` Ctrl + ` ``) and start the server:
   ```bash
   npm start
   ```

3. Open your browser:
   👉 **`http://localhost:5000`**

---

## 👤 Default Accounts

| Role | Username | Password | Privileges |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | Upload/delete/edit songs, view user list & stats |
| **User** | `listener` | `user123` | Unlimited streaming, like songs, download songs |
| **Guest** | *(None)* | *(None)* | 3-song preview limit |
