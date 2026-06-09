# SRB Studio — Social Media Setup Guide

**Studio:** SRB (Sisira · Rathnakar · Bhagya) — "Built by one. Shipped for many."

This guide walks you through creating the three accounts, posting your first week of content, and the posting workflow. Total setup time: ~30 minutes. First week of content: 2-3 hours of batched work.

---

## Step 1: Reserve your handles (5 minutes)

Open these three URLs on your phone and try to register. Save credentials in your password manager (Bitwarden is free).

| Platform | Try this handle first | Fallback handles |
|---|---|---|
| Instagram | `@srb.studio` | `@srbhq` · `@srb_studio` · `@srbstudioo` (with extra o) |
| TikTok | `@srb.studio` | `@srbhq` · `@srb_studio` |
| YouTube | `@SRBStudio` | `@SRBLab` · `@SRBHQ` · `@SRB-Studio` |

> Period in handle? Instagram and TikTok allow it. YouTube does not — go with the no-period version. Same brand, different platforms.

**Pro tip:** register the same handle across all 3 platforms even if one is "your favorite." You don't want a competitor squatting it.

---

## Step 2: Account profiles (10 minutes)

All three platforms need the same:

### Profile photo
Use the file: `social/assets/srb-favicon.svg` (or the same SVG exported to a 800×800 PNG).
- IG/TikTok: 320×320 minimum
- YouTube: 800×800

To export the SVG to PNG:
1. Open in browser at full size
2. Zoom to 400% (Ctrl/Cmd +)
3. Screenshot, save as PNG
4. Or use https://svgtopng.com

### Display name (consistent across all 3)
**`SRB Studio`**

### Bio / tagline (copy-paste)
```
Built by one. Shipped for many.
5 live SaaS apps · 1 founder · $0 to launch
↓ The portfolio + how I ship ↓
```

### Link in bio
Use **Linktree** (free) or **bento.me** (cleaner) with these 5 links:
1. PharmaIP Radar
2. CloudFinOps Co-Pilot
3. AutoHedge Pro
4. QuantaLab
5. PegWatch
6. (optional) SRB landing page — `srb.studio`

Set up Linktree at https://linktr.ee → claim `@srb.studio` handle → add the 5 links → copy the URL → paste as the bio link on all 3 platforms.

### Account type
- Instagram: **Creator** (not Personal, not Business — Creator gives you analytics + music)
- TikTok: **Creator** (lets you use trending sounds)
- YouTube: **Brand account** with custom handle (looks more legit than personal)

---

## Step 3: Account warm-up (DO THIS BEFORE POSTING)

New accounts get throttled. Post-flow for the first 7 days:

| Day | Action |
|---|---|
| Day -3 | Follow 30 accounts in your niches (pharma, SaaS, indie hacking, AI). Like 10 posts. |
| Day -2 | Follow 30 more. Comment thoughtfully on 5 posts. |
| Day -1 | Bio + profile pic + link in bio all set. No posts yet. |
| Day 1 | First post (Day 1 of the calendar). |
| Day 2-7 | One post per day. Reply to every comment within 1 hour for the first 30 days. |

**Why this matters:** the first 30 days of an account's life are when the algorithm decides if you're spam. Engagement velocity (likes + comments in the first 60 min after posting) is the single biggest signal.

---

## Step 4: Make your first post (5 minutes)

Open `social/post-generator.html` in your browser.

**Default load = "Built by one. Shipped for many." brand reveal. Right-click the canvas → "Save image as" → save as `day-01-instagram-1x1.png`.**

That's your first Instagram post.

**For TikTok (vertical 9:16):** click "9:16" format in the left panel → right-click → save as `day-01-tiktok-9x16.png` (this is the cover image; you'll layer this with a video — see Step 5).

**For YouTube Short (vertical 9:16):** same as TikTok.

**For YouTube long-form (landscape 16:9):** click "16:9" → save as `day-04-yt-longform.png`.

---

## Step 5: Make a video (10 minutes per video)

You need actual video for TikTok/Reels/Shorts. The cleanest workflow:

### Option A: Screen-record + voiceover (recommended for tutorials)
1. **OBS Studio** (free) — record your screen at 1080p
2. **CapCut** (free desktop + phone) — trim, add captions, add sound
3. **Your phone mic** — narrate live while recording

### Option B: Talking head (recommended for hot takes, founder story)
1. **Phone camera** (4K) or **Sony A6400** (if you have it)
2. **Natural light** from a window, no ring light needed
3. **CapCut** — auto-captions (this is the #1 hack for watch-time)
4. **9:16 vertical**, 30-60 seconds max

### Option C: Text-on-screen with stock B-roll (fastest)
1. Download 5-10 Pexels.com stock clips (free, no attribution)
2. Layer with **CapCut text overlays** synced to the script
3. Add a **trending sound** from TikTok's commercial music library

### The 8 scripts you already have
Open `social/scripts/01-ipo-hook.md` through `08-cliffhanger-app6.md`. Each one has:
- A shot list
- Spoken VO or text overlay
- Ready-to-paste caption
- Why it works

Pick the script for the day → record → edit in CapCut → export at 1080×1920 → upload.

---

## Step 6: Upload workflow per platform

### Instagram
- Open the app → "+" → Reel (for video) or Post (for image)
- Trim if needed
- Caption: paste from the calendar
- Cover: choose a frame OR upload the PNG you generated
- Hashtags: paste the 5 from the calendar
- Tag: @srb.studio (your own account, for analytics)
- Share

### TikTok
- Open the app → "+" → upload from camera roll
- Caption: paste from the calendar
- Sound: leave as the original audio OR swap to a trending sound (search "trending" in TikTok's music library, pick one with 50k+ uses this week)
- Cover: pick a high-contrast frame
- Hashtags: paste the 5 from the calendar
- Post

### YouTube
- Open YouTube Studio → Create → Short (for short-form) OR Upload Video (for long-form)
- Title: from the calendar
- Description: from the calendar
- Thumbnail: for Shorts, pick a frame; for long-form, you need a custom thumbnail (use the 16:9 generator template, save as PNG, upload)
- Tags: copy 3-5 from the calendar hashtags (skip the #)
- Visibility: Public
- Publish

---

## Step 7: Posting schedule (the calendar is your source of truth)

Open `social/CONTENT_CALENDAR.md`. Each day has a full spec for all 3 platforms.

**Recommended cadence:**
- **Mon:** BIP / MRR update
- **Tue:** Demo
- **Wed:** Tutorial
- **Thu:** Demo
- **Fri:** Hot take / BIP
- **Sat:** BTS / Day-in-the-life
- **Sun:** Founder story

**Best times (US East + India friendly):**
- 9:00 AM ET (6:30 PM IST)
- 12:00 PM ET (9:30 PM IST)
- 6:00 PM ET (3:30 AM IST — only for US-only content)

**Repurpose rule:** every Instagram Reel = a TikTok = a YT Short within 24 hours. Every YouTube long-form = a 60-second teaser on IG/TikTok.

---

## Step 8: Engagement (the actual growth hack)

Posting is 30% of the work. Engagement is the other 70%.

### Daily (15 min)
- Reply to every comment on your own posts within 1 hour of posting
- Reply to comments on 5 large accounts in your niche (pharma, SaaS, indie hacking)

### Weekly (30 min)
- DM 3 people who liked/commented on your posts. Just say "thanks for the comment, what part resonated?" Not sales. Just conversation.
- Comment on 10 posts from accounts 10x your size (not asking for follows, just adding value)

### Monthly (1 hour)
- Review analytics. What got the most saves? Most comments? Most shares? Make 2 more posts in that style.
- Update your link in bio. Drop the lowest-performer, add the highest.

---

## Folder structure reference

```
D:/maxie_made/
├── landing/
│   └── index.html              # SRB Studio landing page
├── social/
│   ├── CONTENT_CALENDAR.md     # 30-day post spec
│   ├── README.md               # this file
│   ├── post-generator.html     # open in browser, edit, screenshot
│   ├── assets/
│   │   ├── srb-logo.svg        # main logo
│   │   ├── srb-favicon.svg     # profile pic
│   │   └── srb-og-card.svg     # 1200×630 link preview
│   ├── instagram/              # saved IG exports (start empty)
│   ├── youtube/                # saved YT exports (start empty)
│   ├── tiktok/                 # saved TT exports (start empty)
│   └── scripts/
│       ├── 01-ipo-hook.md
│       ├── 02-stack-breakdown.md
│       ├── 03-before-after-cloudfinops.md
│       ├── 04-roast-saas.md
│       ├── 05-day-in-life.md
│       ├── 06-demo-pegwatch-depeg.md
│       ├── 07-pricing-reveal-pharmaip.md
│       └── 08-cliffhanger-app6.md
└── (5 app folders)
```

---

## Quick start: 30 minutes from now to first post live

1. **5 min** — Open `social/post-generator.html` in browser
2. **5 min** — Right-click canvas, save as PNG, save to `social/instagram/day-01.png`
3. **5 min** — Register `@srb.studio` on Instagram (phone required)
4. **5 min** — Set profile pic (srb-favicon.svg) + bio + link
5. **5 min** — Upload day-01.png to Instagram with the Day 1 caption from the calendar
6. **5 min** — Screenshot the live post. Share in a group chat. Tell one friend.

That's it. You're live.

---

## Things to avoid

- **Don't post and ghost.** The first 30 days, every comment gets a reply. After that, you can slack.
- **Don't use trending sounds you didn't actually hear.** Watch the sound's other videos first.
- **Don't link to your paid product in the first 5 posts.** Build the audience first, sell later.
- **Don't post the same content on all 3 platforms.** Adapt: IG captions are long, TikTok captions are short, YT descriptions are SEO-heavy.
- **Don't buy followers.** Ever. The engagement rate plummets and the algorithm punishes you.
- **Don't delete underperforming posts.** The algorithm reads a delete as "this creator is fragile." Just post the next one.

---

## What "viral" actually means here

A single viral post is not the goal. Consistent posting for 90 days is. The math:

- 1 post/day × 90 days = 90 posts
- Average 2,000 views per post = 180,000 total views
- 1% follow rate = 1,800 new followers
- 5% of those become paying users (generous) = 90 paying users
- Average $50/mo ARPU = $4,500 MRR by month 3

That's the realistic outcome if you post every day for 90 days. The viral post is a bonus, not a plan.

---

## When you get stuck

- Don't know what to post? → `social/CONTENT_CALENDAR.md` has 30 days planned
- Don't know how to design? → `social/post-generator.html` has 7 templates
- Don't know what to say? → `social/scripts/` has 8 viral scripts ready
- Don't know what to write in the caption? → The calendar has the full caption
- Don't know what time to post? → The calendar has the schedule

Everything you need is in this folder. The only variable is showing up.
