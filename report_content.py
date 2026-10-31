# -*- coding: utf-8 -*-
"""
Report content definitions for MyTune Documentation
Candidate: Kuldeep Pal (Roll No: 35)
College: Vande Mataram Degree College of Arts, Commerce & Science
Guide: Asst. Prof. Bharati Gaikar
"""

METADATA = {
    "title": "MyTune: Modern Audio-Reactive Web Music Player & Streaming Platform",
    "short_title": "MyTune: Audio-Reactive Web Music Streaming Platform",
    "student_name": "Kuldeep Pal",
    "roll_no": "35",
    "degree": "Third Year B.Sc. Computer Science",
    "academic_year": "2026–2027",
    "guide_name": "ASST. PROF. BHARATI GAIKAR",
    "college_name": "VANDE MATARAM DEGREE COLLEGE OF ARTS, COMMERCE & SCIENCE",
    "college_affiliation": "(Affiliated to University of Mumbai)",
    "college_address": "Telcos Wadi, Dr. Nemade Marg, Kopar, Old Dombivali West-421202, Maharashtra",
    "university": "UNIVERSITY OF MUMBAI",
    "render_url": "https://mytune-music.onrender.com/",
    "github_url": "https://github.com/k23pl1/mytune.git"
}

PAGES = []

# ================= PAGE 1: TITLE / COVER PAGE =================
PAGES.append({
    "page_num": 1,
    "type": "cover",
    "content": {
        "univ": "UNIVERSITY OF MUMBAI",
        "sub": "A Mini Project Report Submitted in Partial Fulfillment of the Requirements for the Award of Degree of",
        "degree": "THIRD YEAR B.SC. COMPUTER SCIENCE (2026–2027)",
        "project_title": "MYTUNE: MODERN AUDIO-REACTIVE WEB MUSIC STREAMING PLATFORM",
        "subtitle": "An Intelligent Zero-Install Web Audio Streaming Architecture with Dynamic Frequency Reactivity, Dual-Engine SQLite Persistence, Multi-Regional Cataloging, and Cloud CI/CD Hosting",
        "student_name": "Mr. Kuldeep Pal",
        "roll_no": "Roll No: 35",
        "guide": "ASST. PROF. BHARATI GAIKAR",
        "college": "VANDE MATARAM DEGREE COLLEGE OF ARTS, COMMERCE & SCIENCE",
        "affiliation": "(Affiliated to University of Mumbai)",
        "address": "Telcos Wadi, Dr. Nemade Marg, Kopar, Old Dombivali West-421202, Maharashtra",
        "render_link": "Public Deployment: https://mytune-music.onrender.com/"
    }
})

# ================= PAGE 2: CERTIFICATE =================
PAGES.append({
    "page_num": 2,
    "type": "certificate",
    "title": "CERTIFICATE BY THE INSTITUTE",
    "subtitle": "Third Year B.Sc. Computer Science – 2026/27",
    "cert_text": (
        "This is to certify that Mr. Kuldeep Pal, Student of Vande Mataram Degree College studying in "
        "Third Year B.Sc. Computer Science program, Seat/Roll No: 35, has successfully completed the "
        "Mini Project titled \"MyTune: Modern Audio-Reactive Web Music Player & Streaming Platform\" "
        "in the area of Web Multimedia Systems and Cloud Computing for the academic year 2026–2027.\n\n"
        "The project demonstrates high-order engineering competence in Web Audio API digital signal processing, "
        "Node.js microservices, resilient dual-engine SQLite persistence with native Linux fallback, "
        "multi-tiered authentication with guest playback limitations, and zero-downtime production deployment "
        "on Render Cloud Infrastructure.\n\n"
        "To the best of my knowledge and belief, the work embodied in this project report is original, authentic, "
        "and has been conducted under our continuous supervision and guidance. The information incorporated "
        "is correct and meets the prescribed university guidelines."
    ),
    "signatories": [
        ("__________________________\nAsst. Prof. Bharati Gaikar\nInternal Project Guide",
         "__________________________\nHead of Department\nDepartment of Computer Science",
         "__________________________\nDr. Rajkumar M. Kolhe\nPrincipal, VMDC")
    ]
})

# ================= PAGE 3: STUDENT'S DECLARATION =================
PAGES.append({
    "page_num": 3,
    "type": "declaration",
    "title": "STUDENT'S DECLARATION",
    "text": (
        "I, Mr. Kuldeep Pal, Student of Vande Mataram Degree College of Arts, Commerce & Science studying in "
        "Third Year B.Sc. Computer Science program (Roll No: 35), hereby declare that I have individually "
        "designed, engineered, and completed the Mini Project titled \"MyTune: Modern Audio-Reactive Web Music "
        "Player & Streaming Platform\" during the academic year 2026–2027.\n\n"
        "I solemnly affirm that this project report is an authentic record of my original technological development "
        "and experimental testing. The empirical data, algorithmic formulations, architectural schemas, and code listings "
        "presented herein have emerged from my direct implementation efforts.\n\n"
        "I further declare that this work has not been submitted previously, in part or in full, to the University "
        "of Mumbai or any other university or examining body for the award of any degree, diploma, or fellowship. "
        "Due credit has been extended to all open-source libraries, standards, and referenced academic literature "
        "by endorsing them in the Bibliography and References section as per standard IEEE/ACM citation norms.\n\n"
        "The live production application has been deployed publicly on the Render cloud ecosystem and is verifiable at: "
        "https://mytune-music.onrender.com/"
    ),
    "meta": {
        "name": "Kuldeep Pal",
        "roll": "Roll No: 35",
        "date": "15th March 2027",
        "place": "Dombivali (W), Mumbai"
    }
})

# ================= PAGE 4: ABSTRACT & ROLE STATEMENT =================
PAGES.append({
    "page_num": 4,
    "type": "abstract",
    "title": "ABSTRACT",
    "abstract": (
        "Contemporary commercial web music streaming platforms impose severe operational overheads, including "
        "monolithic client runtimes exceeding 150 MB, intrusive telemetry, aggressive DRM restrictions, and recurring "
        "subscription paywalls. Furthermore, traditional web audio interfaces rely on passive playback controls that "
        "fail to leverage browser-native Digital Signal Processing (DSP) for dynamic visual engagement.\n\n"
        "MyTune is an advanced, lightweight, zero-install audio-reactive web music player engineered to deliver "
        "instantaneous audio playback coupled with real-time frequency-spectrum visualization. The frontend is built "
        "with vanilla JavaScript, HTML5 Canvas, and modern glassmorphic CSS, utilizing the W3C Web Audio API "
        "(AnalyserNode with Fast Fourier Transform - FFT) to analyze live audio streams and dynamically modulate "
        "ambient neon background lighting, particle pulses, and spectrum visualizers in real-time. The backend is "
        "constructed on Node.js and Express, implementing a resilient dual-database abstraction that dynamically selects "
        "between precompiled SQLite3 and Node's built-in node:sqlite engine, thereby guaranteeing zero GLIBC binary "
        "failures across heterogeneous Linux server environments. The system incorporates multi-tiered access control: "
        "a 3-song guest preview limiter, password-hashed user accounts with persistent favorites and MP3 downloads, and a "
        "comprehensive administrative dashboard for multi-part song uploads and system monitoring. The application is "
        "continuously deployed on Render Cloud (https://mytune-music.onrender.com/) with automated 24/7 keep-awake telemetry."
    ),
    "role_title": "Role & Responsibility Statement",
    "role_text": (
        "This engineering project was solely executed by the candidate across all conceptual, analytical, and developmental "
        "stages: Web Audio API signal processing formulation; RESTful API routing and HTTP 206 Partial Content byte-range "
        "streaming; dual-engine SQLite schema architecture; bcrypt cryptographic credential protection; responsive glassmorphic "
        "UI design; cross-browser unit and integration test verification; and automated Render CI/CD cloud pipeline configuration."
    )
})

# ================= PAGE 5: ACKNOWLEDGEMENT =================
PAGES.append({
    "page_num": 5,
    "type": "acknowledgement",
    "title": "ACKNOWLEDGEMENT",
    "text": (
        "The successful completion of this project report on \"MyTune: Modern Audio-Reactive Web Music Player & "
        "Streaming Platform\" marks a significant milestone in my academic development. I express my deepest "
        "sense of gratitude to all individuals whose continuous guidance, constructive criticism, and encouragement "
        "have shaped this endeavor.\n\n"
        "I take immense pleasure in expressing my profound gratitude to our esteemed Principal, Dr. Rajkumar M. Kolhe, "
        "Vande Mataram Degree College of Arts, Commerce & Science, for fostering an academic environment equipped with "
        "state-of-the-art laboratory infrastructure and technological resources.\n\n"
        "I am profoundly indebted to my internal project guide, Asst. Prof. Bharati Gaikar, whose exceptional domain "
        "expertise, rigorous architectural critiques, and methodological guidance proved invaluable throughout the lifecycle "
        "of this system. Her insistence on engineering robustness, code efficiency, and formal documentation standards "
        "provided the foundational direction for this work.\n\n"
        "I also extend my sincere appreciation to the Head of the Department and all respected faculty members of the "
        "Department of Computer Science for imparting foundational knowledge in distributed systems, web architectures, "
        "and database systems.\n\n"
        "Lastly, I extend my heartfelt thanks to my parents, family, and peers for their unwavering patience, moral support, "
        "and encouragement throughout the design and testing phases of this platform."
    ),
    "sig_name": "Kuldeep Pal",
    "sig_roll": "Roll No: 35 | TY B.Sc. CS"
})

# ================= PAGE 6: TABLE OF CONTENTS (PART 1) =================
PAGES.append({
    "page_num": 6,
    "type": "toc1",
    "title": "TABLE OF CONTENTS",
    "entries": [
        ("Preliminary Pages", "Page"),
        ("Certificate by the Institute", "ii"),
        ("Student's Declaration", "iii"),
        ("Abstract & Role Statement", "iv"),
        ("Acknowledgement", "v"),
        ("Table of Contents", "vi"),
        ("List of Figures & List of Tables", "vii"),
        ("Chapter 1: Introduction", "1"),
        ("1.1 Background & Digital Audio Streaming Landscape", "1"),
        ("1.2 Problem Formulation & Modern Web Audio Limitations", "2"),
        ("1.3 Project Objectives, Purpose & Technical Scope", "3"),
        ("1.4 Applicability & Implemented System Achievements", "4"),
        ("1.5 Report Organisation Overview", "4"),
        ("Chapter 2: Survey of Technologies & System Analysis", "5"),
        ("2.1 Conventional Web Music Streaming Workflows", "5"),
        ("2.2 Problems and Structural Limitations of Existing Approaches", "6"),
        ("2.3 Proposed System Architecture & Core Engineering Principles", "6"),
        ("2.4 End-to-End Operational Lifecycle Workflow", "7"),
        ("2.5 Comprehensive Requirements Specification (FR & NFR)", "7"),
        ("2.6 Hardware & Software Specification Matrices", "8"),
        ("2.7 Platform Justification & Technical Trade-offs", "8"),
        ("2.8 Multi-Dimensional Feasibility Study & Economic Model", "9"),
        ("2.9 Project Planning, Gantt & PERT Network Charts", "10"),
        ("Chapter 3: System Design & Architectural Modeling", "11"),
        ("3.1 Modular System Architecture & Decomposition", "11"),
        ("3.2 Comprehensive SQLite Data Dictionaries", "12"),
        ("3.3 Entity-Relationship (ER) Modeling", "14"),
        ("3.4 Data Flow Diagrams (Level-0 Context & Level-1 Decomposed)", "15"),
        ("3.5 Sequence Models for Guest Preview Limit & Audio Streaming", "16"),
        ("3.6 Web Audio API Real-time Frequency Analyser FFT Design", "17"),
        ("3.7 User Interface & Responsive Design Architecture", "18"),
        ("3.8 Security & 3-Tier Access Control Architecture", "19"),
        ("3.9 System Test Case Design Matrix", "19")
    ]
})

# ================= PAGE 7: TOC (PART 2) & LIST OF FIGURES / TABLES =================
PAGES.append({
    "page_num": 7,
    "type": "toc2",
    "title": "TABLE OF CONTENTS (CONTD.) & LIST OF FIGURES",
    "entries": [
        ("Chapter 4: Implementation and Testing", "20"),
        ("4.1 Monorepo Implementation & Directory Structure", "20"),
        ("4.2 Verified Core Algorithmic Code Listings", "21"),
        ("4.2.1 Express Backend Server & Dual-Engine Fallback (server.js)", "21"),
        ("4.2.2 Web Audio Frequency Visualizer Engine (visualizer.js)", "22"),
        ("4.2.3 Audio Player Queue Controller (player.js)", "23"),
        ("4.2.4 REST API Client & Cross-Origin Handler (api.js)", "24"),
        ("4.3 Code Efficiency & Performance Optimization Strategies", "25"),
        ("4.4 Comprehensive Testing Methodologies & Verification Log", "26"),
        ("Chapter 5: Results and Operational Demonstrations", "27"),
        ("5.1 Operational Screen Demonstrations & Interface Breakdown", "27"),
        ("5.2 Five Regional & Global Music Categories", "28"),
        ("5.3 Dynamic Audio Spectrum Visualizer & Ambient Lighting", "29"),
        ("5.4 Liked Songs Collection & User Favorites Persistence", "30"),
        ("5.5 Administrative Control Panel & Track Management", "30"),
        ("5.6 Test Summary & Architectural Evaluation Matrix", "30"),
        ("Chapter 6: Cloud Deployment & Public Hosting on Render", "31"),
        ("6.1 Cloud Hosting Architecture Overview & Platform Analysis", "31"),
        ("6.2 Git Version Control & Continuous Deployment (CI/CD) Pipeline", "32"),
        ("6.3 Environment Variables, Port Binding & Network Routing", "33"),
        ("6.4 Cross-Platform Native Dependency Management & GLIBC Resolution", "33"),
        ("6.5 24/7 Keep-Awake Ping Process with Cron-Job.org", "33"),
        ("6.6 Production Verification & Live System Link (https://mytune-music.onrender.com/)", "33"),
        ("Chapter 7: Conclusion and Future Work", "34"),
        ("7.1 Concluding Summary & Operational Significance", "34"),
        ("7.2 System Limitations", "35"),
        ("7.3 Future Enhancement Roadmap", "35"),
        ("Chapter 8: References & Technical Glossary", "36"),
        ("Appendices (API Reference, Schema DDL, User Manual)", "37")
    ],
    "figures": [
        ("Figure 2.1", "MyTune Project Work Breakdown Structure & Schedule Gantt Chart", "10"),
        ("Figure 3.1", "MyTune 3-Tier Modular System Architecture", "11"),
        ("Figure 3.2", "MyTune Entity-Relationship Diagram (ERD)", "14"),
        ("Figure 3.3", "Data Flow Diagrams (Level-0 Context & Level-1 Decomposed)", "15"),
        ("Figure 3.4", "Sequence Diagram for Guest Limit & Audio Streaming", "16"),
        ("Figure 3.5", "Web Audio API Real-time Frequency Analyser FFT Pipeline", "17"),
        ("Figure 6.1", "Render Cloud CI/CD Architecture & 24/7 Keep-Awake Workflow", "32")
    ],
    "tables": [
        ("Table 2.1", "Hardware Specification Matrix (Development vs Client vs Cloud)", "8"),
        ("Table 2.2", "Software Technology Stack Specification", "8"),
        ("Table 3.1", "SQLite Data Dictionary - USERS Table", "12"),
        ("Table 3.2", "SQLite Data Dictionary - SONGS Table", "13"),
        ("Table 3.3", "SQLite Data Dictionary - LIKES & PLAYLISTS Tables", "13"),
        ("Table 3.4", "Comprehensive System Test Case Design Matrix", "19"),
        ("Table 4.1", "Empirical Test Execution Verification Log", "26"),
        ("Table A.1", "Complete REST API Endpoints Specification", "37")
    ]
})

print("Content Pages 1 to 7 defined.")
