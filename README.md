# Anki Audio Generator

Anki Audio Generator is a Python tool that converts sentence lists into pronunciation audio and Anki-compatible flashcard assets.

The program:

- Reads German sentences from a TSV file
- Generates speech using Google Cloud Text-to-Speech
- Creates MP3 audio files automatically
- Skips already generated files
- Produces an Anki-compatible TSV containing sound tags

## Features

- Bulk audio generation
- Automatic filename sanitization
- German TTS support
- Anki integration
- Reusable for large sentence collections

## Requirements

- Python 3.10+
- Google Cloud Text-to-Speech API enabled
- Google Cloud credentials configured

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/anki-audio-generator.git
cd anki-audio-generator
