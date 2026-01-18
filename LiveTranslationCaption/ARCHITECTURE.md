# Application Flow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ System Tray  │  │   Settings   │  │   Caption Overlay       │  │
│  │   Icon       │  │   Dialog     │  │   (Always on Top)       │  │
│  │   • Start    │  │   • Audio    │  │                          │  │
│  │   • Stop     │  │   • Language │  │  "Hello!" → "こんにちは!" │  │
│  │   • Settings │  │   • Display  │  │                          │  │
│  │   • Quit     │  │              │  │  [Translated Caption]    │  │
│  └──────┬───────┘  └──────┬───────┘  └───────▲──────────────────┘  │
└─────────┼──────────────────┼──────────────────┼─────────────────────┘
          │                  │                  │
          ▼                  ▼                  │
┌─────────────────────────────────────────────────────────────────────┐
│                      APPLICATION CORE (main.py)                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  LiveTranslationApp                                            │ │
│  │  • Initializes all components                                  │ │
│  │  • Manages system tray                                         │ │
│  │  • Coordinates processing loop                                 │ │
│  │  • Handles start/stop/quit                                     │ │
│  └────┬───────────────┬────────────────┬──────────────┬──────────┘ │
└───────┼───────────────┼────────────────┼──────────────┼─────────────┘
        │               │                │              │
        ▼               ▼                ▼              ▼
┌───────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────────┐
│ Configuration │ │Audio Capture│ │   Audio     │ │ Translation  │
│   Manager     │ │   Module    │ │  Processor  │ │    Module    │
│ (config.py)   │ │(capture.py) │ │(processor.py│ │(translator.py│
│               │ │             │ │             │ │              │
│ • Load/Save   │ │• PyAudio    │ │• Speech Rec │ │• Google      │
│ • Get/Set     │ │• Loopback   │ │• Japanese   │ │  Translate   │
│ • Defaults    │ │• Threading  │ │• Audio→Text │ │• Caching     │
│               │ │• Queue      │ │             │ │• Ja→En       │
└───────┬───────┘ └──────┬──────┘ └──────┬──────┘ └──────┬───────┘
        │                │                │                │
        └────────────────┴────────────────┴────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Processing Thread      │
                    │  _process_audio_loop()  │
                    └─────────────────────────┘
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                       AUDIO PROCESSING PIPELINE                  │
└─────────────────────────────────────────────────────────────────┘

1. CAPTURE
   ┌──────────────────────────────────────┐
   │ System Audio (Stereo Mix/Loopback)   │
   │  • Games, Videos, Music, Apps        │
   └─────────────────┬────────────────────┘
                     │ Raw Audio Bytes
                     ▼
   ┌──────────────────────────────────────┐
   │ AudioCapture.get_audio_chunk()       │
   │  • Collect 3 seconds of audio        │
   │  • Sample rate: 16000 Hz             │
   │  • Format: 16-bit PCM                │
   └─────────────────┬────────────────────┘
                     │
                     ▼
2. RECOGNIZE
   ┌──────────────────────────────────────┐
   │ AudioProcessor.process_audio()       │
   │  • Convert audio to AudioData        │
   │  • Google Speech Recognition API     │
   │  • Language: Japanese (ja-JP)        │
   └─────────────────┬────────────────────┘
                     │ Japanese Text
                     │ e.g., "こんにちは"
                     ▼
3. TRANSLATE
   ┌──────────────────────────────────────┐
   │ Translator.translate()               │
   │  • Check translation cache           │
   │  • Google Translate API              │
   │  • Source: ja, Target: en            │
   └─────────────────┬────────────────────┘
                     │ English Text
                     │ e.g., "Hello"
                     ▼
4. DISPLAY
   ┌──────────────────────────────────────┐
   │ CaptionWindow.update_caption()       │
   │  • Thread-safe signal emission       │
   │  • Update overlay label              │
   │  • Start fade timer (5 seconds)      │
   └──────────────────────────────────────┘
                     │
                     ▼
   ┌──────────────────────────────────────┐
   │ On-Screen Caption Display            │
   │  • Position: Bottom-center           │
   │  • Style: Semi-transparent black bg  │
   │  • Font: Arial 18pt Bold White       │
   │  • Duration: 5 seconds (configurable)│
   └──────────────────────────────────────┘
```

## Thread Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MAIN THREAD (Qt)                      │
│  • GUI Event Loop                                       │
│  • System Tray Icon                                     │
│  • Caption Window Display                               │
│  • Settings Dialog                                      │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ spawn
                 ▼
┌─────────────────────────────────────────────────────────┐
│              AUDIO CAPTURE THREAD                        │
│  • Continuous audio recording                           │
│  • PyAudio stream reading                               │
│  • Queue population                                     │
│  • Runs in background (daemon)                          │
└─────────────────────────────────────────────────────────┘
                 │
                 │ audio data
                 ▼ (via queue)
┌─────────────────────────────────────────────────────────┐
│            PROCESSING THREAD                             │
│  • Get audio chunks from queue                          │
│  • Speech recognition (blocking API calls)              │
│  • Translation (blocking API calls)                     │
│  • Emit signals to main thread for UI update            │
│  • Runs in background (daemon)                          │
└─────────────────────────────────────────────────────────┘
                 │
                 │ pyqtSignal
                 ▼
┌─────────────────────────────────────────────────────────┐
│              MAIN THREAD (Qt)                            │
│  • Receive caption update signal                        │
│  • Update caption label text                            │
│  • Start fade timer                                     │
└─────────────────────────────────────────────────────────┘

Note: Thread-safe communication via:
  - queue.Queue for audio data
  - PyQt5 signals/slots for UI updates
```

## Timing Diagram

```
Time →
═══════════════════════════════════════════════════════════════════

User: Click "Start"
  │
  ├─→ [Main Thread] Start audio capture
  │
  ├─→ [Audio Thread] Begin recording ━━━━━━━━━━━━━━━━━━━━━━━━━━→
  │                   ↓ ↓ ↓ ↓ ↓ (continuous audio chunks)
  │
  ├─→ [Process Thread] Loop starts ━━━━━━━━━━━━━━━━━━━━━━━━━━→
       │
       ├─→ Get 3s audio chunk (0.0s - 3.0s)
       │   └─→ Takes ~3 seconds to collect
       │
       ├─→ Process audio to text (~1-2s API call)
       │   └─→ Result: "おはようございます"
       │
       ├─→ Translate text (~0.5-1s API call)
       │   └─→ Result: "Good morning"
       │
       ├─→ Signal main thread
       │   └─→ Caption displayed ━━━━━━━━━━→ (5 seconds)
       │                                   ↓
       │                                Auto-fade
       │
       ├─→ Get next chunk (3.0s - 6.0s)
       │
       └─→ ... repeat ...

Total loop time: ~4-6 seconds per caption
```

## Configuration Flow

```
┌──────────────────────────────────────────────────────┐
│                   config.json                         │
│  {                                                    │
│    "language": "ja",                                  │
│    "translation_language": "en",                      │
│    "caption_display_duration": 5,                     │
│    "sample_rate": 16000,                              │
│    ...                                                │
│  }                                                    │
└─────────────┬────────────────────────────────────────┘
              │
              │ Loaded on startup
              ▼
┌──────────────────────────────────────────────────────┐
│            Config("config.json")                      │
│  • _load_config()                                     │
│  • Merge with defaults                                │
│  • Provide get/set methods                            │
└─────────────┬────────────────────────────────────────┘
              │
              ├─→ Used by AudioCapture
              │   └─→ sample_rate, chunk_size
              │
              ├─→ Used by AudioProcessor
              │   └─→ language, energy_threshold
              │
              ├─→ Used by Translator
              │   └─→ source_lang, target_lang
              │
              └─→ Used by CaptionWindow
                  └─→ fade_duration
```

## Error Handling

```
┌─────────────────────────────────────────────────────┐
│              Error Recovery Strategies               │
└─────────────────────────────────────────────────────┘

Audio Capture Errors:
  • Device not found → Use default device
  • Stream error → Print error, continue loop
  • Queue overflow → Drop old data

Speech Recognition Errors:
  • UnknownValueError → Skip (unintelligible)
  • RequestError → Print error, continue
  • No audio → Return None

Translation Errors:
  • Network error → Return original text
  • Rate limit → Use cached translation
  • Timeout → Return original text

UI Errors:
  • Window closed → Recreate if needed
  • Signal error → Log and continue
```

## State Machine

```
┌─────────────────────────────────────────────────────┐
│           Application State Machine                  │
└─────────────────────────────────────────────────────┘

    [Started]
       │
       ├─→ Initialize Components
       │   └─→ Create Audio/Processor/Translator/UI
       │
       ▼
    [Idle]
       │
       ├─→ "Start" clicked
       │   └─→ start_capture()
       │
       ▼
    [Running]
       │   │
       │   ├─→ Audio capturing ━━━━━━→
       │   ├─→ Processing loop ━━━━━━→
       │   └─→ Captions displaying
       │
       ├─→ "Stop" clicked
       │   └─→ stop_capture()
       │
       ▼
    [Stopped]
       │
       ├─→ "Settings" clicked
       │   └─→ Show dialog → Reload config
       │
       ├─→ "Start" again → Back to [Running]
       │
       ├─→ "Quit" clicked
       │   └─→ cleanup() → [Exit]
       │
       ▼
    [Exit]
```

This diagram shows the complete architecture and data flow of the LiveTranslationCaption application.
