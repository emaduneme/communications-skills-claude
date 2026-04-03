#!/usr/bin/env python3
"""
transcribe.py — Transcribe interview audio using OpenAI Whisper (runs locally).

Requires:
  pip install openai-whisper
  System: ffmpeg (sudo apt install ffmpeg OR brew install ffmpeg)

Models (smallest to largest, speed vs accuracy tradeoff):
  tiny, base, small, medium, large

Usage:
  python transcribe.py --audio interview.mp3
  python transcribe.py --audio recording.m4a --model medium --output transcript.txt
  python transcribe.py --audio call.wav --model large --language en
"""

import argparse
import os
import sys
from datetime import datetime


def check_dependencies():
    try:
        import whisper
        return whisper
    except ImportError:
        print("OpenAI Whisper not installed.")
        print("Install with: pip install openai-whisper")
        print("Also requires ffmpeg: sudo apt install ffmpeg  OR  brew install ffmpeg")
        sys.exit(1)


def transcribe_audio(audio_path, model_name="base", language="en", output_path=None):
    whisper = check_dependencies()

    if not os.path.exists(audio_path):
        print(f"Audio file not found: {audio_path}")
        sys.exit(1)

    file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    print(f"Loading Whisper model: {model_name}")
    print(f"Audio file: {audio_path} ({file_size_mb:.1f} MB)")
    print("Transcribing... (this may take a few minutes for longer recordings)")

    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, language=language, verbose=False)

    transcript_text = result["text"].strip()
    segments = result.get("segments", [])

    # Format with timestamps
    timestamped_lines = []
    for seg in segments:
        start = int(seg["start"])
        mins, secs = divmod(start, 60)
        hours, mins = divmod(mins, 60)
        timestamp = f"[{hours:02d}:{mins:02d}:{secs:02d}]"
        timestamped_lines.append(f"{timestamp} {seg['text'].strip()}")

    # Build output
    header = [
        f"TRANSCRIPT",
        f"Source file: {os.path.basename(audio_path)}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Model: {model_name} | Language: {language}",
        f"Duration: {int(segments[-1]['end']) // 60}:{int(segments[-1]['end']) % 60:02d} min" if segments else "",
        "=" * 60,
        "",
    ]

    full_output = "\n".join(header) + "\n" + "\n".join(timestamped_lines)

    # Output
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_output)
        print(f"\nTranscript saved to: {output_path}")
    else:
        # Auto-name based on audio file
        base = os.path.splitext(audio_path)[0]
        auto_path = f"{base}_transcript.txt"
        with open(auto_path, "w", encoding="utf-8") as f:
            f.write(full_output)
        print(f"\nTranscript saved to: {auto_path}")
        output_path = auto_path

    print(f"Words transcribed: ~{len(transcript_text.split())}")
    print("\nFirst 300 characters of transcript:")
    print("-" * 40)
    print(transcript_text[:300] + "..." if len(transcript_text) > 300 else transcript_text)

    return output_path, transcript_text


def main():
    parser = argparse.ArgumentParser(description="Transcribe interview audio using Whisper.")
    parser.add_argument("--audio", required=True, help="Path to audio/video file")
    parser.add_argument("--model", default="base",
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size (default: base). Use 'medium' for better accuracy.")
    parser.add_argument("--language", default="en", help="Language code (default: en)")
    parser.add_argument("--output", help="Output transcript file path")
    args = parser.parse_args()

    transcribe_audio(args.audio, args.model, args.language, args.output)


if __name__ == "__main__":
    main()
