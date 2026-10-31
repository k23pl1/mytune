import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.dates as mdates
import numpy as np
import os
from datetime import datetime, timedelta

output_dir = r"C:\Users\palku\OneDrive\เอกสาร\Desktop\EX_PROJECTS\mytune\docs_assets"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

# 1. Gantt Chart
def generate_gantt():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    tasks = [
        "Requirement Analysis & Survey",
        "System Architecture & DB Design",
        "Audio Engine & Web Audio Visualizer",
        "Express REST API & Dual-Engine SQLite",
        "Frontend Modern Glassmorphic UI",
        "Testing (Unit, Integration, Security)",
        "Render.com Cloud CI/CD Deployment",
        "Comprehensive Project Documentation"
    ]
    starts = [1, 3, 6, 9, 12, 16, 19, 21]
    durations = [3, 4, 4, 4, 5, 4, 3, 5]
    colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#9467bd']
    
    y_pos = np.arange(len(tasks))
    ax.barh(y_pos, durations, left=starts, align='center', color=colors, edgecolor='#333333', height=0.6, alpha=0.9)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tasks, fontsize=10, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlabel("Project Timeline (Weeks)", fontsize=11, fontweight='bold')
    ax.set_title("Figure 2.1: MyTune Project Work Breakdown Structure & Schedule", fontsize=12, fontweight='bold', pad=12)
    ax.set_xlim(0, 28)
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    for i in range(len(tasks)):
        ax.text(starts[i] + durations[i] / 2, i, f"W{starts[i]}-W{starts[i]+durations[i]}", 
                ha='center', va='center', color='black', fontsize=9, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig_gantt.png"), dpi=300)
    plt.close()
    print("Gantt generated")

# 2. Architecture Diagram
def generate_architecture():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis('off')
    
    # Title
    ax.text(5.5, 8.2, "Figure 3.1: MyTune 3-Tier Modular System Architecture", ha='center', fontsize=13, fontweight='bold')
    
    # Tier 1: Client Presentation Layer
    rect1 = patches.FancyBboxPatch((0.5, 5.5), 10, 2.3, boxstyle="round,pad=0.2", ec="#1e3a8a", fc="#dbeafe", lw=2)
    ax.add_patch(rect1)
    ax.text(0.8, 7.5, "PRESENTATION LAYER (Single Page Web Application)", fontsize=11, fontweight='bold', color="#1e3a8a")
    
    # Subcomponents in Tier 1
    c_boxes = [
        ("Player UI & Queue\n(player.js, app.js)", 1.0, 5.8, 2.6, 1.3),
        ("Web Audio Analyser\n(visualizer.js)", 4.2, 5.8, 2.6, 1.3),
        ("REST Client & Auth\n(api.js, JWT/State)", 7.4, 5.8, 2.6, 1.3)
    ]
    for text, x, y, w, h in c_boxes:
        b = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", ec="#2563eb", fc="#ffffff", lw=1.5)
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=9, fontweight='bold')
        
    # Tier 2: Business & Application Layer
    rect2 = patches.FancyBboxPatch((0.5, 2.8), 10, 2.2, boxstyle="round,pad=0.2", ec="#14532d", fc="#dcfce7", lw=2)
    ax.add_patch(rect2)
    ax.text(0.8, 4.7, "APPLICATION SERVICE LAYER (Node.js & Express API Gateway)", fontsize=11, fontweight='bold', color="#14532d")
    
    s_boxes = [
        ("Auth Controller\n(bcrypt / Guest Limiter)", 1.0, 3.1, 2.6, 1.3),
        ("Track & Stream Service\n(HTTP 206 Partial Content)", 4.2, 3.1, 2.6, 1.3),
        ("Admin & Playlist Engine\n(Multer Audio/Cover Upload)", 7.4, 3.1, 2.6, 1.3)
    ]
    for text, x, y, w, h in s_boxes:
        b = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", ec="#16a34a", fc="#ffffff", lw=1.5)
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=9, fontweight='bold')
        
    # Tier 3: Data Persistence Layer
    rect3 = patches.FancyBboxPatch((0.5, 0.4), 10, 2.0, boxstyle="round,pad=0.2", ec="#701a75", fc="#fae8ff", lw=2)
    ax.add_patch(rect3)
    ax.text(0.8, 2.1, "DATA & STORAGE LAYER (Dual-Engine SQLite & Static Storage)", fontsize=11, fontweight='bold', color="#701a75")
    
    d_boxes = [
        ("SQLite Engine Fallback\n(sqlite3 / node:sqlite)", 1.2, 0.6, 3.8, 1.2),
        ("File System Audio Assets\n(/uploads/songs, /uploads/covers)", 6.0, 0.6, 3.8, 1.2)
    ]
    for text, x, y, w, h in d_boxes:
        b = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", ec="#c026d3", fc="#ffffff", lw=1.5)
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=9, fontweight='bold')
        
    # Arrows between tiers
    ax.annotate("", xy=(5.5, 5.4), xytext=(5.5, 5.0), arrowprops=dict(arrowstyle="<|-|>", lw=2, color="#333333"))
    ax.text(5.6, 5.2, "HTTP/JSON & Audio Stream", fontsize=8, fontweight='bold')
    
    ax.annotate("", xy=(5.5, 2.7), xytext=(5.5, 2.4), arrowprops=dict(arrowstyle="<|-|>", lw=2, color="#333333"))
    ax.text(5.6, 2.55, "SQL Queries & File I/O", fontsize=8, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig_architecture.png"), dpi=300)
    plt.close()
    print("Architecture generated")

# 3. Entity-Relationship Diagram (ERD)
def generate_erd():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis('off')
    
    ax.text(5.5, 8.2, "Figure 3.2: MyTune Entity-Relationship Diagram (ERD)", ha='center', fontsize=13, fontweight='bold')
    
    entities = [
        ("USERS", 0.8, 4.5, 2.6, 2.8, ["id (INTEGER, PK)", "username (TEXT, UQ)", "password (TEXT)", "role (TEXT)", "created_at (DATETIME)"]),
        ("SONGS", 4.2, 4.5, 2.6, 2.8, ["id (INTEGER, PK)", "title (TEXT)", "artist (TEXT)", "category (TEXT)", "file_path (TEXT)", "cover_path (TEXT)", "duration (INTEGER)", "plays (INTEGER)"]),
        ("LIKES", 7.6, 4.5, 2.6, 2.8, ["id (INTEGER, PK)", "user_id (INT, FK)", "song_id (INT, FK)", "created_at (DATETIME)", "UNIQUE(user, song)"]),
        ("PLAYLISTS", 0.8, 0.8, 2.6, 2.5, ["id (INTEGER, PK)", "name (TEXT)", "user_id (INT, FK)", "created_at (DATETIME)"]),
        ("PLAY_HISTORY", 5.5, 0.8, 3.2, 2.5, ["id (INTEGER, PK)", "user_id (INT, FK)", "song_id (INT, FK)", "played_at (DATETIME)"])
    ]
    
    for title, x, y, w, h, cols in entities:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", ec="#1e293b", fc="#f8fafc", lw=1.8)
        ax.add_patch(box)
        hdr = patches.Rectangle((x, y + h - 0.5), w, 0.5, ec="#1e293b", fc="#0284c7", lw=1.5)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 0.25, title, ha='center', va='center', color='white', fontsize=10, fontweight='bold')
        
        cur_y = y + h - 0.8
        for col in cols:
            prefix = "PK  " if "PK" in col else ("FK  " if "FK" in col else "     ")
            col_color = "#b91c1c" if "PK" in col else ("#047857" if "FK" in col else "#334155")
            ax.text(x + 0.15, cur_y, col, fontsize=8, color=col_color, fontfamily='monospace')
            cur_y -= 0.35

    # Relationships
    # USERS -> LIKES (1:N)
    ax.annotate("", xy=(7.6, 5.8), xytext=(3.4, 5.8), arrowprops=dict(arrowstyle="->", lw=1.8, color="#dc2626"))
    ax.text(4.0, 6.0, "1 : N (likes)", fontsize=9, fontweight='bold', color="#dc2626")
    
    # SONGS -> LIKES (1:N)
    ax.annotate("", xy=(7.6, 5.2), xytext=(6.8, 5.2), arrowprops=dict(arrowstyle="->", lw=1.8, color="#2563eb"))
    ax.text(6.9, 5.4, "1 : N", fontsize=9, fontweight='bold', color="#2563eb")

    # USERS -> PLAYLISTS (1:N)
    ax.annotate("", xy=(2.1, 3.3), xytext=(2.1, 4.5), arrowprops=dict(arrowstyle="->", lw=1.8, color="#16a34a"))
    ax.text(2.2, 3.8, "1 : N (creates)", fontsize=9, fontweight='bold', color="#16a34a")

    # USERS -> PLAY_HISTORY (1:N)
    ax.annotate("", xy=(5.5, 2.0), xytext=(3.4, 4.8), arrowprops=dict(arrowstyle="->", lw=1.8, color="#9333ea"))
    ax.text(4.0, 3.2, "1 : N (listens)", fontsize=9, fontweight='bold', color="#9333ea")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig_erd.png"), dpi=300)
    plt.close()
    print("ERD generated")

# 4. Data Flow Diagram (DFD Level 0 & Level 1)
def generate_dfd():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7.5), dpi=300)
    
    # Level 0 DFD
    ax1.set_xlim(0, 11)
    ax1.set_ylim(0, 4)
    ax1.axis('off')
    ax1.text(5.5, 3.7, "Figure 3.3 (a): Level-0 Context Data Flow Diagram", ha='center', fontsize=11, fontweight='bold')
    
    # Entities
    b_user = patches.Rectangle((0.5, 1.2), 2.2, 1.4, ec="#1e3a8a", fc="#dbeafe", lw=1.5)
    ax1.add_patch(b_user)
    ax1.text(1.6, 1.9, "User / Visitor\n(Browser)", ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Process
    p_sys = patches.Circle((5.5, 1.9), 1.1, ec="#15803d", fc="#dcfce7", lw=1.8)
    ax1.add_patch(p_sys)
    ax1.text(5.5, 1.9, "0.0\nMyTune Streaming\nPlatform", ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Admin
    b_admin = patches.Rectangle((8.3, 1.2), 2.2, 1.4, ec="#7e22ce", fc="#fae8ff", lw=1.5)
    ax1.add_patch(b_admin)
    ax1.text(9.4, 1.9, "Administrator\n(Role Admin)", ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Flows
    ax1.annotate("", xy=(4.4, 2.2), xytext=(2.7, 2.2), arrowprops=dict(arrowstyle="->", lw=1.5, color="#2563eb"))
    ax1.text(3.55, 2.4, "Auth, Stream Request", ha='center', fontsize=8, fontweight='bold')
    ax1.annotate("", xy=(2.7, 1.6), xytext=(4.4, 1.6), arrowprops=dict(arrowstyle="->", lw=1.5, color="#2563eb"))
    ax1.text(3.55, 1.35, "Audio Stream, Song Data", ha='center', fontsize=8, fontweight='bold')

    ax1.annotate("", xy=(6.6, 2.2), xytext=(8.3, 2.2), arrowprops=dict(arrowstyle="->", lw=1.5, color="#7e22ce"))
    ax1.text(7.45, 2.4, "Uploads, Track CRUD", ha='center', fontsize=8, fontweight='bold')
    ax1.annotate("", xy=(8.3, 1.6), xytext=(6.6, 1.6), arrowprops=dict(arrowstyle="->", lw=1.5, color="#7e22ce"))
    ax1.text(7.45, 1.35, "System Metrics & Logs", ha='center', fontsize=8, fontweight='bold')

    # Level 1 DFD
    ax2.set_xlim(0, 11)
    ax2.set_ylim(0, 4.5)
    ax2.axis('off')
    ax2.text(5.5, 4.2, "Figure 3.3 (b): Level-1 Decomposed Data Flow Diagram", ha='center', fontsize=11, fontweight='bold')
    
    procs = [
        ("1.0 Authenticate\n& Guest Counter", 1.0, 2.2),
        ("2.0 Audio Catalog\n& Filter Engine", 3.8, 2.2),
        ("3.0 Web Audio\nFFT Visualizer", 6.6, 2.2),
        ("4.0 User Favorites\n& Download Mgr", 9.4, 2.2)
    ]
    for title, x, y in procs:
        p = patches.Circle((x, y), 0.85, ec="#0369a1", fc="#e0f2fe", lw=1.5)
        ax2.add_patch(p)
        ax2.text(x, y, title, ha='center', va='center', fontsize=7.5, fontweight='bold')
        
    # Data stores
    ds1 = patches.Rectangle((2.0, 0.4), 2.8, 0.7, ec="#334155", fc="#f1f5f9", lw=1.5)
    ax2.add_patch(ds1)
    ax2.text(3.4, 0.75, "D1: SQLite Database (database.db)", ha='center', va='center', fontsize=8, fontweight='bold')
    
    ds2 = patches.Rectangle((6.2, 0.4), 2.8, 0.7, ec="#334155", fc="#f1f5f9", lw=1.5)
    ax2.add_patch(ds2)
    ax2.text(7.6, 0.75, "D2: Audio Storage (/uploads)", ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Interconnecting arrows
    ax2.annotate("", xy=(3.8, 1.1), xytext=(2.0, 2.0), arrowprops=dict(arrowstyle="<->", lw=1.2, color="#475569"))
    ax2.annotate("", xy=(3.8, 1.1), xytext=(3.8, 1.4), arrowprops=dict(arrowstyle="<->", lw=1.2, color="#475569"))
    ax2.annotate("", xy=(7.6, 1.1), xytext=(6.6, 1.4), arrowprops=dict(arrowstyle="<->", lw=1.2, color="#475569"))
    ax2.annotate("", xy=(4.8, 0.75), xytext=(9.4, 1.4), arrowprops=dict(arrowstyle="<->", lw=1.2, color="#475569"))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig_dfd.png"), dpi=300)
    plt.close()
    print("DFD generated")

# 5. Sequence Diagram
def generate_sequence():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis('off')
    ax.text(5.5, 8.2, "Figure 3.4: Audio Streaming & Guest Limit Verification Sequence", ha='center', fontsize=12, fontweight='bold')
    
    lifelines = [
        ("User Browser\n(Client)", 1.5),
        ("Player Controller\n(player.js)", 4.0),
        ("Express REST API\n(server.js)", 6.8),
        ("Database / Storage\n(SQLite / Disk)", 9.5)
    ]
    
    for title, x in lifelines:
        box = patches.FancyBboxPatch((x-1.0, 7.2), 2.0, 0.6, boxstyle="round,pad=0.1", ec="#1e3a8a", fc="#dbeafe", lw=1.5)
        ax.add_patch(box)
        ax.text(x, 7.5, title, ha='center', va='center', fontsize=8.5, fontweight='bold')
        ax.plot([x, x], [1.0, 7.2], linestyle="--", color="#64748b", lw=1.2)
        
    # Sequence steps
    steps = [
        (6.7, 1.5, 4.0, "1. Click Song Track Tile", "#2563eb", True),
        (6.0, 4.0, 4.0, "2. Check Guest Preview Counter (<=3)", "#16a34a", False),
        (5.3, 4.0, 6.8, "3. GET /api/songs/:id/stream", "#2563eb", True),
        (4.6, 6.8, 9.5, "4. Fetch metadata & check range header", "#9333ea", True),
        (3.9, 9.5, 6.8, "5. Return Audio Buffer / 206 Partial", "#9333ea", False),
        (3.2, 6.8, 4.0, "6. Audio Stream Chunk & AnalyserNode", "#2563eb", False),
        (2.5, 4.0, 1.5, "7. Render Reacting Neon Background & Waves", "#16a34a", False),
        (1.8, 1.5, 6.8, "8. POST /api/likes/toggle (User Session)", "#dc2626", True),
        (1.2, 6.8, 9.5, "9. INSERT/DELETE from LIKES table", "#dc2626", True)
    ]
    
    for y, x1, x2, label, color, is_solid in steps:
        if x1 == x2:
            # Self call
            ax.annotate("", xy=(x1, y-0.3), xytext=(x1, y), arrowprops=dict(arrowstyle="->", lw=1.4, color=color))
            ax.text(x1 + 0.15, y - 0.15, label, fontsize=8, fontweight='bold', color=color)
        else:
            style = "->" if is_solid else "--"
            ax.annotate("", xy=(x2, y), xytext=(x1, y), 
                        arrowprops=dict(arrowstyle="->", lw=1.4, color=color, linestyle="solid" if is_solid else "dashed"))
            mid_x = (x1 + x2) / 2
            ax.text(mid_x, y + 0.12, label, ha='center', fontsize=8, fontweight='bold', color=color)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig_sequence.png"), dpi=300)
    plt.close()
    print("Sequence generated")

# 6. Web Audio API Processing Pipeline
def generate_webaudio():
    fig, ax = plt.subplots(figsize=(11, 4.8), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.text(5.5, 5.5, "Figure 3.5: Web Audio API Real-time Frequency Analyser FFT Pipeline", ha='center', fontsize=12, fontweight='bold')
    
    nodes = [
        ("<audio> Element\n(DOM Media Node)", 0.6, 2.5, 1.8, 1.4, "#fef3c7", "#d97706"),
        ("MediaElement\nSourceNode", 2.8, 2.5, 1.8, 1.4, "#dbeafe", "#2563eb"),
        ("AnalyserNode\n(fftSize=128/256)", 5.0, 2.5, 1.8, 1.4, "#dcfce7", "#16a34a"),
        ("AudioContext\nDestination (Speakers)", 7.2, 3.7, 1.8, 1.2, "#f1f5f9", "#475569"),
        ("Uint8Array\nFrequency Data", 7.2, 1.5, 1.8, 1.2, "#fae8ff", "#9333ea"),
        ("Canvas / Ambient\nColor Glow Engine", 9.4, 1.5, 1.4, 1.2, "#ffe4e6", "#e11d48")
    ]
    
    for title, x, y, w, h, bg, border in nodes:
        b = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", ec=border, fc=bg, lw=1.6)
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=8, fontweight='bold')
        
    # Connections
    ax.annotate("", xy=(2.8, 3.2), xytext=(2.4, 3.2), arrowprops=dict(arrowstyle="->", lw=1.8, color="#333333"))
    ax.annotate("", xy=(5.0, 3.2), xytext=(4.6, 3.2), arrowprops=dict(arrowstyle="->", lw=1.8, color="#333333"))
    ax.annotate("", xy=(7.2, 4.3), xytext=(6.8, 3.5), arrowprops=dict(arrowstyle="->", lw=1.8, color="#333333"))
    ax.annotate("", xy=(7.2, 2.1), xytext=(6.8, 2.8), arrowprops=dict(arrowstyle="->", lw=1.8, color="#9333ea"))
    ax.text(6.8, 2.3, "getByteFrequencyData()", fontsize=7.5, fontweight='bold', color="#9333ea", ha='right')
    ax.annotate("", xy=(9.4, 2.1), xytext=(9.0, 2.1), arrowprops=dict(arrowstyle="->", lw=1.8, color="#e11d48"))
    ax.text(9.2, 2.3, "requestAnimationFrame", fontsize=7.5, fontweight='bold', color="#e11d48", ha='center')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig_webaudio.png"), dpi=300)
    plt.close()
    print("WebAudio generated")

# 7. Render Cloud Deployment Architecture
def generate_deployment():
    fig, ax = plt.subplots(figsize=(11, 5.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.5)
    ax.axis('off')
    ax.text(5.5, 6.1, "Figure 6.1: Render.com Cloud Production Architecture & 24/7 Keep-Awake Workflow", ha='center', fontsize=12, fontweight='bold')
    
    boxes = [
        ("Developer Workspace\n(Local Git Repo)", 0.6, 3.8, 2.4, 1.4, "#eff6ff", "#3b82f6"),
        ("GitHub Remote\n(k23pl1/mytune.git)", 4.0, 3.8, 2.6, 1.4, "#f8fafc", "#0f172a"),
        ("Render.com Web Service\n(Node.js / Express)", 7.6, 3.8, 2.8, 1.4, "#ecfdf5", "#059669"),
        ("24/7 External Uptime Pinger\n(Cron-Job.org / UptimeRobot)", 7.6, 1.2, 2.8, 1.4, "#fef2f2", "#dc2626"),
        ("Global Web Visitors\n(mytune-music.onrender.com)", 4.0, 1.2, 2.6, 1.4, "#faf5ff", "#7e22ce")
    ]
    
    for title, x, y, w, h, bg, border in boxes:
        b = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", ec=border, fc=bg, lw=1.6)
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=8.5, fontweight='bold')

    # Arrows
    ax.annotate("", xy=(4.0, 4.5), xytext=(3.0, 4.5), arrowprops=dict(arrowstyle="->", lw=1.8, color="#3b82f6"))
    ax.text(3.5, 4.7, "git push origin main", ha='center', fontsize=8, fontweight='bold', color="#3b82f6")
    
    ax.annotate("", xy=(7.6, 4.5), xytext=(6.6, 4.5), arrowprops=dict(arrowstyle="->", lw=1.8, color="#059669"))
    ax.text(7.1, 4.7, "Auto Deploy Webhook", ha='center', fontsize=8, fontweight='bold', color="#059669")
    
    ax.annotate("", xy=(9.0, 3.8), xytext=(9.0, 2.6), arrowprops=dict(arrowstyle="<->", lw=1.8, color="#dc2626"))
    ax.text(9.1, 3.2, "HTTP GET /ping\nEvery 10 Mins (Prevent Spin-Down)", va='center', fontsize=8, fontweight='bold', color="#dc2626")

    ax.annotate("", xy=(7.6, 4.1), xytext=(6.6, 1.9), arrowprops=dict(arrowstyle="<->", lw=1.8, color="#7e22ce"))
    ax.text(6.8, 2.8, "HTTPS Streaming", fontsize=8, fontweight='bold', color="#7e22ce")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig_deployment.png"), dpi=300)
    plt.close()
    print("Deployment generated")

if __name__ == "__main__":
    generate_gantt()
    generate_architecture()
    generate_erd()
    generate_dfd()
    generate_sequence()
    generate_webaudio()
    generate_deployment()
    print("ALL DIAGRAMS SUCCESSFULLY GENERATED!")
