#!/usr/bin/env python3
"""
Voix off + bande son d'une vidéo, à partir d'un script JSON.

    python3 voix/voiceover.py voix/script-30s.json

Produit, à côté du script :
  - <nom>-voix.wav      la voix seule
  - <nom>-mix.wav       voix + musique + bruitages, normalisé pour les réseaux (-14 LUFS)
  - <nom>-timeline.js   le minutage de chaque morceau de phrase, lu par la scène HTML
                        pour caler les sous-titres et les animations sur la voix.

La voix est synthétisée en local avec Piper (via sherpa-onnx), sans compte ni abonnement.
Le modèle (~60 Mo) est téléchargé au premier lancement dans voix/models/.

Option --prises N : la synthèse varie un peu à chaque fois. Avec --prises 4, chaque phrase est
générée 4 fois, transcrite par Whisper (modèle « small », ~370 Mo téléchargés au premier usage)
et on garde la prise la plus proche du texte. Plus lent, mais évite les mots mâchés.

Dépendances : pip install sherpa-onnx numpy scipy soundfile, et ffmpeg dans le PATH.
"""
import json
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, resample_poly, sosfilt

SR = 44100
HERE = Path(__file__).resolve().parent
MODELS = HERE / "models"
MODEL_URL = "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-fr_FR-{voice}.tar.bz2"
WHISPER_URL = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.tar.bz2"


# ---------------------------------------------------------------- voix

def download(url, d, label):
    if d.exists():
        return
    MODELS.mkdir(exist_ok=True)
    print(f"Téléchargement de {label}…")
    with tempfile.NamedTemporaryFile(suffix=".tar.bz2") as tmp:
        urllib.request.urlretrieve(url, tmp.name)
        with tarfile.open(tmp.name) as tar:
            tar.extractall(MODELS, filter="data")


def load_tts(voice, speed):
    import sherpa_onnx

    d = MODELS / f"vits-piper-fr_FR-{voice}"
    download(MODEL_URL.format(voice=voice), d, f"la voix {voice}")
    vits = sherpa_onnx.OfflineTtsVitsModelConfig(
        model=str(d / f"fr_FR-{voice}.onnx"),
        tokens=str(d / "tokens.txt"),
        data_dir=str(d / "espeak-ng-data"),
    )
    tts = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(vits=vits, num_threads=4)))
    return lambda text: _synth(tts, text, speed)


def _synth(tts, text, speed):
    audio = tts.generate(text, sid=0, speed=speed)
    x = np.asarray(audio.samples, dtype=np.float64)
    if audio.sample_rate != SR:
        x = resample_poly(x, SR, audio.sample_rate)
    # On retire les silences de début et de fin pour maîtriser le rythme.
    env = np.abs(x)
    idx = np.where(env > env.max() * 0.02)[0]
    return x[max(0, idx[0] - int(0.03 * SR)): idx[-1] + int(0.08 * SR)]


def load_checker():
    """Renvoie une fonction score(audio, texte) entre 0 et 1, via Whisper."""
    import difflib
    import unicodedata

    import sherpa_onnx

    d = MODELS / "sherpa-onnx-whisper-small"
    download(WHISPER_URL, d, "Whisper (vérification de la voix)")
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(d / "small-encoder.int8.onnx"), decoder=str(d / "small-decoder.int8.onnx"),
        tokens=str(d / "small-tokens.txt"), language="fr", task="transcribe", num_threads=4)

    def norm(text):
        text = unicodedata.normalize("NFD", text.lower())
        return re.sub(r"[^a-z0-9 ]", "", "".join(ch for ch in text if not unicodedata.combining(ch)))

    def score(audio, text):
        x = resample_poly(audio, 16000, SR).astype(np.float32)
        x = np.concatenate([np.zeros(1600, np.float32), x, np.zeros(4000, np.float32)])
        st = rec.create_stream()
        st.accept_waveform(16000, x)
        rec.decode_stream(st)
        heard = st.result.text.strip()
        return difflib.SequenceMatcher(None, norm(heard), norm(text)).ratio(), heard

    return score


def weight(say):
    """Poids d'un morceau ≈ son temps de parole : lettres + petite pause sur la ponctuation."""
    w = len(re.sub(r"[^\wÀ-ÿ]", "", say))
    if re.search(r"[,:;]$", say.strip()):
        w += 5
    return max(w, 1)


# ---------------------------------------------------------------- bruitages et musique

def env_exp(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def sfx_whoosh():
    n = int(0.55 * SR)
    t = np.arange(n) / SR
    noise = np.random.default_rng(1).standard_normal(n)
    # balayage passe-bande de 300 Hz à 4 kHz, en cloche
    out = np.zeros(n)
    for i, (a, b) in enumerate(zip(np.linspace(300, 3000, 8), np.linspace(900, 6000, 8))):
        sl = slice(i * n // 8, (i + 1) * n // 8 + 2000)
        sos = butter(2, [a, b], btype="band", fs=SR, output="sos")
        seg = sosfilt(sos, noise[sl])
        out[sl][: len(seg)] += seg * np.hanning(len(seg))
    return out / np.abs(out).max() * 0.35 * np.sin(np.pi * t / t[-1]) ** 2


def sfx_boom():
    n = int(1.2 * SR)
    t = np.arange(n) / SR
    freq = 38 + 90 * np.exp(-t * 18)
    body = np.sin(2 * np.pi * np.cumsum(freq) / SR) * env_exp(n, 0.35)
    click = np.random.default_rng(2).standard_normal(n) * env_exp(n, 0.008) * 0.4
    return (body + click) * 0.9


def sfx_stamp():
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    freq = 70 + 160 * np.exp(-t * 40)
    body = np.sin(2 * np.pi * np.cumsum(freq) / SR) * env_exp(n, 0.09)
    slap = np.random.default_rng(4).standard_normal(n) * env_exp(n, 0.02)
    slap = sosfilt(butter(2, [400, 3000], btype="band", fs=SR, output="sos"), slap)
    return (body * 0.8 + slap * 0.5) * 0.8


def sfx_coin():
    n = int(0.6 * SR)
    t = np.arange(n) / SR
    ping = lambda f, d: np.sin(2 * np.pi * f * t) * np.exp(-np.maximum(t - d, 0) / 0.12) * (t >= d)
    return (ping(1975, 0) * 0.6 + ping(2637, 0.07) * 0.5 + ping(3951, 0.07) * 0.15) * 0.18


def sfx_pop():
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    freq = 900 * np.exp(-t * 25) + 400
    return np.sin(2 * np.pi * np.cumsum(freq) / SR) * env_exp(n, 0.025) * 0.22


def note(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def music(duration, bpm=96):
    """Petit beat lo-fi : nappe d'accords Am–F–C–G, basse, kick et charley."""
    n = int(duration * SR)
    out = np.zeros(n)
    beat = 60 / bpm
    bar = 4 * beat
    chords = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 55, 60, 64], [55, 59, 62, 67]]  # Am7 Fmaj7 C G
    rng = np.random.default_rng(3)
    k = 0
    while k * bar < duration:
        start = int(k * bar * SR)
        length = min(int(bar * SR), n - start)
        t = np.arange(length) / SR
        ch = chords[k % 4]
        att = np.minimum(1, t / 0.25) * np.minimum(1, (bar - t) / 0.3)
        pad = np.zeros(length)
        for m in ch:
            for det in (-0.08, 0.08):
                f = note(m + det)
                pad += sum(np.sin(2 * np.pi * f * h * t) / h ** 1.6 for h in range(1, 5))
        out[start:start + length] += pad * att * 0.022
        # basse : fondamentale sur les temps 1 et 3
        for b in (0, 2.5):
            s = start + int(b * beat * SR)
            m = int(0.9 * beat * SR)
            if s + m > n:
                continue
            tb = np.arange(m) / SR
            out[s:s + m] += np.sin(2 * np.pi * note(ch[0] - 24) * tb) * env_exp(m, 0.35) * 0.16
        # kick sur 1 et 3, charley sur les contretemps
        for b in range(4):
            s = start + int(b * beat * SR)
            if b in (0, 2):
                m = int(0.35 * SR)
                if s + m <= n:
                    tk = np.arange(m) / SR
                    f = 45 + 110 * np.exp(-tk * 30)
                    out[s:s + m] += np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(m, 0.12) * 0.35
            h = s + int(beat / 2 * SR)
            m = int(0.05 * SR)
            if h + m <= n:
                out[h:h + m] += rng.standard_normal(m) * env_exp(m, 0.012) * 0.05
        k += 1
    sos = butter(2, 5000, btype="low", fs=SR, output="sos")
    out = sosfilt(sos, out)
    hat_sos = butter(2, 120, btype="high", fs=SR, output="sos")
    out = sosfilt(hat_sos, out)
    fade = int(1.2 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    return out


def add(buf, sig, at):
    s = int(at * SR)
    e = min(len(buf), s + len(sig))
    if s < e:
        buf[s:e] += sig[: e - s]


# ---------------------------------------------------------------- assemblage

def main(script_path, takes=1):
    script_path = Path(script_path).resolve()
    cfg = json.loads(script_path.read_text(encoding="utf-8"))
    stem = script_path.stem.replace("script-", "")
    out_dir = script_path.parent
    synth = load_tts(cfg.get("voice", "siwis-medium"), cfg.get("speed", 1.0))
    check = load_checker() if takes > 1 else None

    duration = cfg["duration"]
    voice = np.zeros(int(duration * SR))
    sfx = np.zeros_like(voice)
    sentences, cursor = [], cfg.get("lead", 0.3)
    sounds = {"whoosh": sfx_whoosh(), "boom": sfx_boom(), "stamp": sfx_stamp(), "coin": sfx_coin()}
    pop = sfx_pop()

    for s in cfg["sentences"]:
        cursor += s.get("pause", 0)
        say = " ".join(c[1] for c in s["chunks"])
        audio = synth(say)
        if check:
            best = (*check(audio, say), audio)
            for _ in range(takes - 1):
                if best[0] > 0.97:
                    break
                a = synth(say)
                cand = (*check(a, say), a)
                if cand[0] > best[0]:
                    best = cand
            print(f"  {best[0]:.2f}  « {best[1]} »")
            audio = best[2]
        start, dur = cursor, len(audio) / SR
        add(voice, audio, start)
        if s.get("sfx"):
            add(sfx, sounds[s["sfx"]], max(0, start - (0.25 if s["sfx"] == "whoosh" else 0.05)))

        ws = [weight(c[1]) for c in s["chunks"]]
        t, chunks = start, []
        for chunk, w in zip(s["chunks"], ws):
            show, extra = chunk[0], chunk[2] if len(chunk) > 2 else None
            d = dur * w / sum(ws)
            gold = show.startswith("*")
            chunks.append({"text": show.lstrip("*"), "gold": gold, "start": round(t, 3), "end": round(t + d, 3)})
            if extra:  # bruitage propre à ce morceau (3e élément), à la place du « pop »
                add(sfx, sounds[extra], t)
            elif gold:
                add(sfx, pop, t)
            t += d
        sentences.append({"segment": s["segment"], "start": round(start, 3), "end": round(start + dur, 3), "chunks": chunks})
        cursor = start + dur + cfg.get("gap", 0.2)

    if cursor > duration:
        sys.exit(f"La voix dure {cursor:.1f} s, plus que les {duration} s prévues : raccourcis le texte ou augmente 'speed'.")

    # Segments : chacun commence avec sa première phrase et finit au début du suivant.
    segments = []
    for s in sentences:
        if not segments or segments[-1]["name"] != s["segment"]:
            segments.append({"name": s["segment"], "start": 0 if not segments else s["start"] - 0.3})
    for a, b in zip(segments, segments[1:] + [{"start": duration}]):
        a["end"] = round(b["start"], 3)
        a["start"] = round(a["start"], 3)

    voice /= np.abs(voice).max() / 0.89
    sf.write(out_dir / f"{stem}-voix.wav", voice, SR, subtype="PCM_16")

    # Musique avec « ducking » : elle baisse quand la voix parle.
    bed = music(duration)
    env = np.convolve(np.abs(voice), np.ones(int(0.08 * SR)) / int(0.08 * SR), mode="same")
    duck = 1 - 0.55 * np.clip(env / 0.05, 0, 1)
    duck = np.convolve(duck, np.ones(int(0.15 * SR)) / int(0.15 * SR), mode="same")
    mix = voice + bed * duck * 0.9 + sfx
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    stereo = np.stack([mix, mix], axis=1)

    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "mix.wav"
        sf.write(raw, stereo, SR, subtype="PCM_24")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
                        "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", str(SR),
                        str(out_dir / f"{stem}-mix.wav")], check=True)

    timeline = {"duration": duration, "segments": segments, "sentences": sentences}
    (out_dir / f"{stem}-timeline.js").write_text(
        "// Généré par voix/voiceover.py : ne pas modifier à la main.\nwindow.VO = "
        + json.dumps(timeline, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")

    print(f"✓ voix {cursor:.1f} s sur {duration} s → {stem}-voix.wav, {stem}-mix.wav, {stem}-timeline.js")
    for seg in segments:
        print(f"  {seg['name']:5} {seg['start']:5.2f} → {seg['end']:5.2f} s")


if __name__ == "__main__":
    args = sys.argv[1:]
    takes = 1
    if "--prises" in args:
        i = args.index("--prises")
        takes = int(args[i + 1])
        del args[i:i + 2]
    main(args[0] if args else HERE / "script-30s.json", takes)
