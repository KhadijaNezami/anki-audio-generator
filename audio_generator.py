#!/usr/bin/env python3

"""
Anki Audio Generator

Generates MP3 pronunciation audio from a TSV file and creates
an Anki-compatible TSV containing sound tags.

Usage:
    python audio_generator.py sentences.tsv
"""

import argparse
import os
import re
from pathlib import Path

import pandas as pd
from google.cloud import texttospeech


VOICE_NAME = "de-DE-Chirp3-HD-Achernar"
LANGUAGE_CODE = "de-DE"
OUTPUT_DIR = "audios"
OUTPUT_TSV = "anki_audio_list.tsv"


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """Convert sentence into a safe filename."""
    clean = re.sub(r"[^a-zA-Z0-9äöüÄÖÜß\s-]", "", text)
    clean = "_".join(clean.split())
    return clean[:max_length]


def generate_audio(
    client: texttospeech.TextToSpeechClient,
    text: str,
    output_path: Path,
):
    """Generate a single MP3 audio file."""

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=LANGUAGE_CODE,
        name=VOICE_NAME,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    with open(output_path, "wb") as f:
        f.write(response.audio_content)


def process_file(input_file: Path):
    """Read TSV and generate audio files."""

    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_file}")

    df = pd.read_csv(input_file, sep="\t")

    if "German Sentence" not in df.columns:
        raise ValueError(
            "TSV file must contain a column named 'German Sentence'"
        )

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    client = texttospeech.TextToSpeechClient()

    anki_entries = []

    total = len(df)

    for idx, row in enumerate(df.iterrows(), start=1):
        _, row_data = row

        text = str(row_data["German Sentence"]).strip()

        if not text:
            continue

        filename = sanitize_filename(text) + ".mp3"
        audio_path = output_dir / filename

        if audio_path.exists():
            print(f"[{idx}/{total}] Skipped: {filename}")
        else:
            try:
                generate_audio(client, text, audio_path)
                print(f"[{idx}/{total}] Generated: {filename}")
            except Exception as e:
                print(f"[{idx}/{total}] Error: {text}")
                print(f"    {e}")
                continue

        anki_entries.append(
            {
                "sentence": text,
                "audio": f"[sound:{filename}]",
            }
        )

    output_tsv = Path(OUTPUT_TSV)

    pd.DataFrame(anki_entries).to_csv(
        output_tsv,
        sep="\t",
        index=False,
    )

    print("\nDone!")
    print(f"Generated entries: {len(anki_entries)}")
    print(f"Anki file: {output_tsv}")
    print(f"Audio folder: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Anki audio from TSV sentence lists."
    )

    parser.add_argument(
        "input_file",
        help="Path to TSV file containing a 'German Sentence' column",
    )

    args = parser.parse_args()

    process_file(Path(args.input_file))


if __name__ == "__main__":
    main()
