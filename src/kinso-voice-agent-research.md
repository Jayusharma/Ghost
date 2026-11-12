# Kinso (kinso.ai): Voice Agent and Unit Economics Teardown

**Date:** 2026-11-12
**Question:** How is Kinso's voice agent built (human-sounding, low latency), how does it unify LinkedIn, Instagram, WhatsApp, Slack and multiple email accounts, and how can it sell for $59 per user per month?

---

## 1. Scope and method

All research used **public material only**. Nothing behind Kinso's login was accessed.

| Source | What was examined |
|---|---|
| `www.kinso.ai` | Marketing site (hosted on Framer) |
| `app.kinso.ai` | HTML, HTTP response headers and Content-Security-Policy (CSP) |
| Web app JavaScript | **523 bundle chunks (12.9 MB)**, which the app serves to every visitor, from `app.kinso.ai/assets/41dd8064de39/`. Lazy-loaded chunks were followed recursively. |
| DNS | TXT, MX and NS records, plus common subdomains |
| Third-party | Privacy policy, VentureBeat article, competitor reviews, founder podcasts, vendor pricing pages |

**Tooling:** The `reverse-engineer-anything` (REA) skill was installed at `~/.agents/skills/reverse-engineer-anything`, and its `SKILL.md` was read. The REA MCP tools were not connected in this session, so I ran the same kind of static JavaScript bundle analysis manually with `curl`, ripgrep and Node.

**Evidence labels used below:**
- **Observed**: literally present in Kinso's shipped code, headers or DNS.
- **Inferred**: my interpretation of observed evidence.
- **Unknown**: not determinable from public material.

Static analysis of client code shows what the app *calls*. It does **not** show what the backend does internally.

---

## 2. Infrastructure fingerprint (observed)

### Hosting
- `www.kinso.ai` is hosted on Framer (`Server: Framer/...`).
- `app.kinso.ai`, `api.kinso.ai` and `auth.kinso.ai` sit behind Cloudflare.
- DNS nameservers are on Cloudflare (`dakota.ns.cloudflare.com`, `norah.ns.cloudflare.com`).

### Email and SaaS (DNS TXT and MX)
- Google Workspace: MX is `smtp.google.com`, and SPF includes `_spf.google.com`.
- Help Scout handles support email (SPF includes `helpscoutemail.com`).
- Klaviyo is used for marketing email (`klaviyo-site-verification`).
- There is a Microsoft 365 verification record (`MS=ms56236309`).

### App endpoints (from the CSP `connect-src` and bundle constants)

```
https://api.kinso.ai/graphql      (GraphQL API)
wss://api.kinso.ai/graphql        (GraphQL subscriptions, real-time updates)
https://agent.kinso.ai            (AI agent and voice backend)
wss://agent.kinso.ai
https://auth.kinso.ai
https://analytics.kinso.ai        (PostHog, proxied through their own domain)
https://p.kinso.ai
*.ingest.de.sentry.io             (Sentry, EU region)
https://*.chime.aws / wss://*.chime.aws   (Amazon Chime SDK)
S3 (us-east-1) and Cloudflare R2  (file and audio storage)
connect.facebook.net              (Meta pixel)
```

### Frontend stack
- React with Apollo GraphQL, which persists its query cache to the browser.
- Zod schemas for validation.
- Sentry for error tracking and PostHog for analytics and session recording.

---

## 3. Voice agent architecture

### 3.1 Observed: what the client code does
The voice module is in chunk `2d3d7612.js`, component `LiveVoiceConnection`.

1. **Endpoints**
   ```js
   const k = "/voice/v1",
         C = `${k}/live/session`,
         M = `${k}/live/prepare`;
   ```
   - `/live/prepare` warms up a session before it starts.
   - `/live/session` performs the SDP exchange (the WebRTC connection handshake).

2. **The transport is WebRTC, not websockets.**
   - The client creates a `new RTCPeerConnection()`.
   - It calls `createOffer()` and `setLocalDescription()`, then waits for ICE gathering to complete.
   - It POSTs the SDP offer to the backend and applies the returned SDP answer with `setRemoteDescription`.
   - The mic is captured with `navigator.mediaDevices.getUserMedia({audio})`.

3. **The data channel is named `"oai-events"`.**
   ```js
   const s = u.createDataChannel("oai-events")
   ```
   `oai-events` is the channel name defined by the **OpenAI Realtime API** WebRTC protocol.

4. **Session start payload (Zod schema)**
   ```js
   { sdp, timezone, threadId?, isNewThread?, viewContext?, briefing? }
   ```
   The `briefing` field is defined as follows:
   ```js
   priorityThreads: array(max 5) of
     { summary(≤280), reason(≤280), from(≤120), subject(≤200), sentAt, platform }
   prioritySummary: string(≤600)
   ```
   The response is `{ sdp, sessionId, threadId }`.

5. **The server sends Kinso's own event format.** It is not OpenAI's native schema.
   ```js
   type: "session.input_transcript.delta" | "session.output_transcript.delta"
   fields: event_id, delta, start_ms, end_ms
   plus "session.closed"
   ```
   OpenAI's native events have different names, such as `conversation.item.input_audio_transcription.delta`.

6. **Session end reasons**
   ```js
   endedBy: "caller" | "goodbye" | "duration_limit" | "idle" | "drain"
          | "replaced" | "startup_timeout" | "provider" | "disconnected"
   providerReason?: string
   ```

7. **Surfaces**
   ```js
   ["web", "phone", "carplay"]
   ```
   CarPlay is behind the feature flag `frontend-voice-carplay-enable`.

8. **Speaking indicator**
   - An `AnalyserNode` (`fftSize = 512`) polls the remote audio level every 100 ms with a threshold of `0.35`.
   - This only drives the UI animation. **There is no client-side VAD** (voice activity detection, the logic that decides when you've stopped talking).

9. **Analytics events**
   - `voice_call_started {newChat, surface, startTrigger}`
   - `voice_call_ended {durationBucket, endedBy, surface}`
   - `carplay_session`, `dictation_take_sent`

10. **Error handling**
    - Timeouts produce "Voice took too long to connect."
    - Microphone errors are mapped to `microphoneDenied`, `microphoneMissing` and `unsupported`.
    - On `pagehide`, the session is released with `keepalive: true`.

### 3.2 Inferred: how the system fits together

```
 Browser / iPhone / CarPlay
   │ mic → WebRTC (Opus over UDP, browser AEC/NS)
   │ data channel "oai-events" (transcripts only)
   ▼
 agent.kinso.ai  ── Kinso's own real-time voice server
   │  • /live/prepare: pre-builds context (top 5 threads, summaries)
   │  • injects context + tools (search inbox, draft reply, etc.)
   │  • server-side VAD / turn-taking / barge-in
   │  • enforces duration_limit, idle, one session per user (replaced)
   │  • normalizes provider events → session.*_transcript.delta
   ▼
 Upstream speech-to-speech "provider"
   (endedBy:"provider" + providerReason prove an upstream exists;
    "oai-events" naming points to OpenAI Realtime lineage)
```

### 3.3 Why it sounds human and has low latency
1. **It uses a speech-to-speech model (inferred).** Audio goes in and audio comes out directly, with no speech-to-text → LLM → text-to-speech chain. That keeps prosody, laughter, tone and natural interruptions.
2. **It uses WebRTC (observed).** Audio travels over UDP with the Opus codec, jitter buffering and built-in echo cancellation and noise suppression. Websocket PCM streaming typically adds 100 ms or more.
3. **It pre-warms (observed).** `/live/prepare` runs before the user speaks, so the context is ready and the upstream session can start immediately.
4. **The context is small and pre-summarized (observed).** At most 5 threads at 280 characters each, plus a 600-character summary. The model answers "what's important today?" without a tool call, so time to first audio is short.
5. **Turn-taking is server-side (inferred from the absence of client VAD).** Endpointing and barge-in happen close to the model.
6. **Transcripts use a separate channel (observed).** They arrive as delta events with timestamps, so the UI renders text without touching the audio path.

### 3.4 Other audio feature: meeting recorder (observed)
Chunk `68ff84a8.js` contains a web recorder:
- It captures two channels: system audio via `getDisplayMedia` and the mic via `getUserMedia`.
- It records with `MediaRecorder`, through an AudioWorklet called `pcm-source-worklet` (`pcm-source-processor`).
- Chunk `d3d0d409.js` has a schema for transcripts with `segments` and `speakers`, and stores audio metadata (`encoding`, `sampleRate`, `channels`, `sizeBytes`).
- This is a Granola-style meeting-notes feature.

The CSP's `*.chime.aws` (Amazon Chime SDK) may serve this feature or the `phone` surface. **This is unconfirmed.** Chime is not referenced anywhere in the bundle code itself.

---

## 4. Multi-channel inbox: how "many apps in one" works

### 4.1 Platform enum (observed)

```
gmail, nylasGmail, nylasOutlook, microsoftOutlook, microsoftTeams,
slack, whatsapp, whatsappBusiness, linkedin, instagram, kinsoChat, synapse
```

### 4.2 Per-channel evidence

| Channel | Evidence (observed) | Integration method |
|---|---|---|
| **Email (Gmail/Outlook)** | `nylasGmail`, `nylasOutlook` (144 references), with `initiateOAuth` for `nylasGmail`; a native `gmail` platform with `historyId` (Gmail API sync cursor); also `microsoftOutlook` | **Nylas** unified email/calendar API, plus direct Gmail and Microsoft Graph |
| **LinkedIn** | GraphQL fragment `linkedin { unipileChatId type name subject folder contentType readOnly organizationId organizationName mailboxId archived mutedUntil }` | **Unipile** |
| **WhatsApp** | `whatsapp { roomType roomTopic avatarMxcUrl otherUserId nextBatch isPinned isMuted muteEndTime disappearingMessages }`; a `"synapse"` platform value; WhatsApp IDs normalized to `...@lid` | **A Matrix bridge** (`mxc://` = Matrix content URI, `nextBatch` = Matrix sync token, Synapse = Matrix homeserver). Very likely self-hosted **mautrix-whatsapp**. |
| **WhatsApp Business** | Separate `whatsappBusiness` platform; flag `frontend-whatsapp-business-connect` | Official Meta Cloud API or a business-solution provider (BSP) (unknown) |
| **Slack** | `slack { contextTeamId isIm isMpim isPrivate }`; Slack message editing via `channelId`/`messageId` | Native Slack API |
| **Microsoft Teams** | `microsoftTeams` platform; meeting links → `teams` vs `googleMeet` | Microsoft Graph |
| **Instagram** | `instagram { handle followerCountLabel isVerified followState followStateLabel }` | **Unknown.** Possibly Unipile or a Matrix bridge (mautrix-meta). |

Other observed details:
- Each platform has a capability config with formatting options, attachments, `voiceNotes`, character limits and max recipients. This is how one composer adapts to every channel.
- Cross-platform contact identity uses keys like `email:<addr>`, `whatsapp:<phone|lid>` and `<platform>:<id>`, which is how one person's threads get linked across apps.

### 4.3 Text AI layer (observed)
The DevTools panel (chunk `374e70d9.js`) has an **agent model override** list:

```js
{ label:"Default",       value:null },
{ label:"Claude Haiku",  value:"us.anthropic.claude-haiku-4-5-20251001-v1:0" },
{ label:"Claude Sonnet", value:"us.anthropic.claude-sonnet-4-6" },
{ label:"Grok 4.6",      value:"us.xai.grok-4.6" },
{ label:"GPT-5.6 Sol",   value:"openai.gpt-5.6-sol" },
{ label:"GPT-5.6 Terra", value:"openai.gpt-5.6-terra" },
{ label:"GPT-6 Luna",    value:"openai.gpt-6-luna" },
{ label:"GPT-5.6 Luna",  value:"openai.gpt-5.6-luna" },
{ label:"GPT-5.5",       value:"openai.gpt-5.5" },
{ label:"GPT-5.4",       value:"openai.gpt-5.4" }
```

- The `us.anthropic.…-v1:0` and `provider.model` ID format is **AWS Bedrock** model-ID syntax, including cross-region inference profiles.
- **Inferred:** Text LLM calls are routed through **Bedrock**, and Kinso swaps models per task.
- **Unknown:** The "Default" model in production.

Other DevTools items show an internal priority engine called **"Jev"** ("Jev re-run failed", `rerunJevPriority`), along with `priorityProvider`, `priorityReasoningBadges`, `agentTurnTraces`, `fakeVoice` and `seedSuggestions`.

### 4.4 Data handling (privacy policy)
- Data is primarily stored in **Australia**, with additional storage in the UK, US and NZ.
- **Communication content is deleted after 6 months.**
- Personal information may be used to train or improve models, de-identified for general improvements.
- No subprocessor or LLM vendor is named.

---

## 5. Pricing and unit economics

### 5.1 Public price
- **$59/month per user**, one all-inclusive plan, attributed to the founder at the invite-only launch.
- It is not on a public Kinso pricing page.
- A card is required for the trial.

Source: this+that (a competitor).

### 5.2 Vendor costs (list prices from public sources, approximate)

| Vendor | Price |
|---|---|
| Unipile | About €5/account/month, falling to about €3 at volume; €49 minimum; unlimited API calls |
| Nylas | Full Platform about $15/month including 5 accounts, then about $1.50–2 per extra account/month |
| OpenAI Realtime (flagship) | About $32 / $64 per 1M audio tokens (in/out); cached input about $0.40/M |
| OpenAI Realtime (mini) | About $10 / $20 per 1M audio tokens; cached input about $0.30/M |
| Claude Haiku 4.5 | About $1 / $5 per 1M tokens (in/out) |
| Claude Sonnet 4.6 | About $3 / $15 per 1M tokens (in/out) |

### 5.3 Estimated cost per user per month (my model)

| Item | Assumption | Estimate |
|---|---|---|
| Email | 1–3 inboxes via Nylas, or free via the direct Gmail API | $0–6 |
| LinkedIn (and maybe Instagram) | Unipile, 1–2 accounts | $3.5–10 |
| WhatsApp | Self-hosted Matrix bridge (compute only) | ~$0.1–0.5 |
| Slack / Teams | Native APIs | ~$0 |
| Text AI | ~4,500 messages triaged by a Haiku-class model with caching, plus ~300 Sonnet-class drafts, plus daily briefs | $5–15 |
| Voice | ~150–300 min/month, capped sessions, small cached context, mini-class pricing | $5–15 (typical user) |
| Infrastructure | Cloudflare, AWS, Sentry, PostHog, storage with 6-month retention | $1–3 |
| **Total** | | **About $16–45, so roughly 25–70% gross margin at $59** |

### 5.4 Why they can sell it for $59
1. **They buy the hard integrations and self-host the cheap one.** Unipile and Nylas solve LinkedIn and email OAuth and anti-ban problems at a few dollars per account. WhatsApp runs over a self-hosted Matrix bridge at almost zero marginal cost, avoiding per-message Business API fees.
2. **They route each task to the cheapest capable model** through Bedrock. A Haiku-class model triages the volume, and stronger models are used only where the user sees quality (drafts, voice). Bedrock also enables AWS credits and committed-spend discounts. That last part is speculation.
3. **They summarize once and reuse everywhere.** The same compact briefing (5 threads, 280 characters each) feeds the inbox ranking, the morning brief and voice context, so they don't re-read full inboxes per request.
4. **Voice is hard-capped.** Sessions end on `duration_limit` and `idle`, there's one session per user (`replaced`), and context is small and cached. The worst-case cost per user is bounded.
5. **Light users subsidize heavy users.** Most users open voice briefly each day, like a gym membership.
6. **Retention limits storage.** The 6-month content deletion caps storage and re-indexing costs.
7. **The business context helps.** It's invite-only launch pricing, and the founder is self-funded after a $180M exit (Realbase, acquired by Domain). Thin early margins are an accepted trade for distribution: a waitlist of about 27k people.

---

## 6. Company context
- **Founders:** Frank Greeff and Jacques Greeff. Frank previously co-founded Realbase, which was acquired by Domain in a $180M exit.
- **Funding:** Self-funded. A podcast segment covers "Why VCs rejected Kinso and why Frank's self-funding".
- **Positioning:** An "AI brain for conversations, calendars, and contacts", with an "opportunity stack" that ranks messages by business impact, plus schema-less ingestion and a semantic memory layer (VentureBeat, sponsored piece).
- **Status:** Waitlist and invite-only.
- **Features:** Unified inbox, priority ranking, tone-matched drafts, universal search, cross-platform linking, morning briefing, voice mode, meeting recorder, CarPlay (behind a flag).

---

## 7. Unknowns
- Kinso's backend code and internal pipeline.
- **The exact voice model and provider in production.** OpenAI Realtime lineage is likely but not confirmed.
- How Instagram connects (Unipile vs a Matrix bridge vs the official API).
- What Amazon Chime is used for (phone, meetings, or unused).
- Which "Default" text model runs in production.
- Actual negotiated vendor prices and real per-user usage.

---

## 8. Blueprint for building something similar

```
Client (web / iOS / CarPlay)
  └─ WebRTC (Opus) ──► Voice relay server (your own)
                        ├─ /prepare: precompute top-N threads + summary
                        ├─ speech-to-speech model (OpenAI Realtime or similar)
                        ├─ tools: search, draft, send, schedule
                        ├─ server-side VAD, barge-in, duration/idle caps
                        └─ transcript deltas → data channel

Integrations
  ├─ Email: direct Gmail API (free) + Nylas for Outlook/others
  ├─ LinkedIn / Instagram: Unipile
  ├─ WhatsApp: mautrix-whatsapp on a Synapse homeserver
  └─ Slack / Teams: native APIs

AI layer
  ├─ LLM gateway (Bedrock / OpenRouter), task-based routing
  ├─ cheap model for triage/priority, strong model for drafts
  ├─ shared compact "briefing" artifact reused by inbox, brief, voice
  └─ prompt caching everywhere
```

---

## 9. Corrections log
- An intermediate keyword scan reported "playht" and "vapi". These were **false positives**: "playht" matched inside the identifier `displayHtml`, and "vapi" matched inside base64 data. Neither vendor appears in Kinso's code.

---

## 10. Sources
- Kinso homepage: https://www.kinso.ai/
- Kinso privacy policy: https://www.kinso.ai/privacy-policy
- `app.kinso.ai` public JavaScript bundles, HTTP headers and CSP (retrieved 2026-11-12)
- VentureBeat, "Cracking the universal inbox: Inside Kinso's quest": https://venturebeat.com/business/cracking-the-universal-inbox-inside-kinsos-quest-to-make-cross-channel-ai
- this+that, Kinso pricing (competitor): https://www.thisandthat.chat/blog/kinso-pricing/
- this+that, Kinso review (competitor): https://www.thisandthat.chat/blog/kinso-review/
- Day One podcast with Frank Greeff: https://podcastrex.com/shows/day-one/how-to-build-distribution-before-you-build-the-product-with-frank-greeff-from-kinso-replay-ep
- Audioscrape, "Beyond a $180M Exit": https://www.audioscrape.com/podcast/dayonefm/episode/beyond-a-180m-exit-frank-greeff-on-purpose-and-building-kinso-ai-88400
- Unipile pricing: https://www.unipile.com/pricing/
- Nylas pricing: https://www.nylas.com/pricing/
- Zeeg, Nylas pricing guide: https://zeeg.me/en/blog/post/nylas-api-pricing
- OpenAI API pricing: https://openai.com/api/pricing/
- eesel, GPT Realtime Mini pricing: https://www.eesel.ai/blog/gpt-realtime-mini-pricing
- Forasoft, OpenAI Realtime API pricing: https://www.forasoft.com/article/openai-realtime-api-pricing
