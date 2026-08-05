---
name: "make-a-movie"
description: "Create dynamic, narrated, music-backed, friend-shareable reels with polished motion and audio mixing."
---

# Make A Movie

Create a short narrated video from structured inputs. Default to a polished, Telegram-friendly 9:16 MP4 that is engaging enough to share outside the household.

## Input

Prefer a JSON manifest with a title, output name, voice, slides, and delivery target. Each slide needs a title, concise narration, readable on-screen text, and either an image or a public source URL that can be captured.

Use `en-US-GuyNeural` at `+5%` by default, one audio segment per slide, and a short pause between segments.

## Creative Standard

Treat the reel as a finished social artifact, not an internal report.

- Write audience-facing copy that a friend can understand without context.
- Never include workflow labels such as “unconfirmed,” “scout suggestion,” “not household-approved,” “candidate,” or “internal.”
- Present verified facts confidently. Express genuine uncertainty as a useful consumer caveat, such as “ask about dairy” or “menu changes seasonally.”
- Open with a strong hook, build momentum, and end with a save/share/visit takeaway.
- Prefer bold typography, intentional color changes, strong hierarchy, and visual contrast over generic dark slideshow styling.
- Add real motion: subtle push-ins, pans, animated crops, kinetic text, or short transitions. A sequence of motionless screenshots is not sufficient unless the user explicitly asks for a plain slideshow.
- Keep pacing energetic. Use short narration and change visual emphasis every few seconds.
- Design for muted viewing with large, concise on-screen text.
- Avoid repetitive layouts when multiple slides use the same source image.
- Keep branding and source screenshots legible; do not stretch, obscure, or use screenshots only as dark background texture.
- Add dynamic, rights-safe instrumental background music by default unless the user requests silence or the subject calls for a restrained treatment.

## Audio Design

- Choose music that matches the reel’s visual energy and subject. Prefer instrumental tracks with an immediate hook and enough arrangement space for narration.
- Use generated or explicitly licensed/rights-safe music. Do not assume a random web track is reusable.
- Duck music beneath narration with sidechain compression or deliberate automation; speech must remain effortless to understand on phone speakers.
- Let the music rise slightly during pauses, transitions, the opening hook, and the closing beat without overpowering the voice.
- Fade cleanly at both ends and avoid abrupt loops or truncated musical phrases.
- Mix toward roughly -16 to -19 integrated LUFS for a social reel, keep true peak below -1 dBFS, and listen-check the balance when possible.
- If music generation fails, use a verified local/right-safe source or create a simple original bed; do not silently omit music.

## Workflow

1. Create a task folder under `movie-renders/<slug>/`.
2. Gather grounded public assets. Prefer official sites, menus, ordering pages, public booking pages, or official social media. Do not bypass access controls.
3. Capture web visuals with Playwright/Chromium at a phone-friendly viewport. Personally verify the rendered page.
4. Convert the request into a manifest. Write a hook, 2–4 concise content beats, and a clear closing beat.
5. Write one narration segment per slide.
6. Generate one neural TTS clip per slide and obtain or create a rights-safe instrumental music bed.
7. Render 1080×1920 frames or motion scenes with strong visual hierarchy and readable captions.
8. Compute scene timing from its matching audio plus a short pause.
9. Add motion and transitions in the rendered video. Subtle movement is acceptable; static concatenation is not the default.
10. Duck and mix the music beneath narration, then assemble H.264/AAC MP4 with `yuv420p`.
11. Validate with `ffprobe`. Extract thumbnails across the timeline and inspect at least two representative frames with `view_image`.
12. Send the MP4 with the messaging tool using `media`, `filename`, and `mimeType: video/mp4`.

## Restaurant Reels

For restaurant discoveries:

- Frame the video as a recommendation or discovery someone can share with friends.
- Use a hook such as “New in Boston,” “Save this lunch spot,” or a similarly specific audience-facing line.
- Include location, hours when useful, and 2–4 concrete menu highlights.
- Keep dietary caveats factual and helpful without exposing internal recommendation status.
- For a single restaurant, use an intro/hook, food or menu highlights, a useful caveat or practical detail, and a save/share outro.
- If food photography is unavailable, use official menu/site captures with varied crops, bold layout changes, and motion.

## Validation

Before delivery, verify:

- video and audio streams are present;
- background music is audible, dynamically ducked beneath narration, rights-safe, and cleanly faded;
- narration and scene changes remain synchronized;
- the MP4 is vertical, readable on a phone, and small enough for the destination;
- motion is visible and the pacing feels intentional;
- screenshots are legible and no private or paywalled content appears;
- no internal workflow language remains;
- the reel makes sense to a recipient who has not seen the preceding chat.

## Rendering Helper

A starting-point renderer is bundled at
[`scripts/render_movie_from_manifest.mjs`](scripts/render_movie_from_manifest.mjs).
Given a manifest JSON path, it renders each slide's foreground-panel frame with
Playwright/Chromium (title, subtitle, bullets, per-slide crop position, accent
color) into a `frames/` folder next to the manifest. It requires Node with the
`playwright` package installed. Treat it as a scaffold to adapt, not a complete
pipeline — timing, motion, TTS, and audio mixing still follow the workflow
above.

## Reliability Notes

- Embed local images as data URLs when rendering HTML with Playwright.
- Use per-slide audio and computed durations; do not pair one continuous voiceover with guessed timings.
- Use `libx264` when available or `libopenh264` as a fallback.
- Use explicit decimal durations in ffmpeg filters, for example `0.18`, because shorthand such as `.18` may fail.
- Use `sidechaincompress` or equivalent automation for music ducking, then measure integrated loudness and true peak before delivery.
