---
title: "The Magic of Pixels: How I Write Music"
date: 2026-03-18
section: blog
location: "Ozersk, Russia"
category: Music
---

You know that strange feeling when a simple 16-bit tune from *Undertale* or *Deltarune* starts playing, and for some reason it takes you breath away? Or when a boss theme kicks in, and without even realizing it, you start nodding your head to the beat?

I've always listened to indie game soundtracks with a sense of awe. I really wanted to learn to play the piano, but somehow I've never once in my life sat down at a real instrument. My attempt to learn the drums also ended with me hopelessly losing the rhythm by the second bar - my hands and feet simply refused to work as a single unit.

But then I discovered FL Studio. And I realized something amazing: to write music that strikes right at the heart, you don't need to be a virtuoso performer. You need a sequencer, imagination, and an understanding of *why* sounds evoke emotions.

I write music for myself, I'm still learning, and I'm constantly tinkering with the settings, trying to find "that" sound. In this post, I've compiled my personal journal of sisocveires - techniques, life hacks, and principles from Toby Fox that helped me turn a set of digital notes into a living story. I hope this will be interesting for both beginners and experienced users.

---

## 1. Palette: Choosing Soul Over Realism

My first mistake was trying to make the sound "expensive". I used massive VST libraries that took up tens of gigabytes. The music sounded high-quality, but... faceless.

The magic of indie games lies in **Soundfonts (.sf2)** - old sound banks from the '90s and 2000s. Yes, they cost next to nothing and sound a bit gritty, but they have character. My working arsenal, from which almost everything is assembled, looks like this:

* **SGM-V2.01:** The foundation. From here I take a clean piano (Bright Yamaha), an acoustic bass, an oboe for sad scenes, and those very orchestral hits (Orchestra Hits).

* **Mega Man X:** If I need a bass that doesn't just hum, but aggressively rattles and rocks (Synth Bass).

* **EarthBound / KirbysDreamLand3:** Priceless for weird synths, overdriven buitars, clean 8-bits squares (Square Wave), and "whistling" leads.

* **Chrono Trigger (CTinstruments) / Illusion of Gaia:** If you need ancient magic - I grab the pads (Strings) and harp from here. They have a phenomenal warm, "tape-like" hum.

* **THDrum / THInst (Touhou):** Dry, snappy drums and aggressive trumpets (ZUNpets) for boss fights.

* **Super Mario World / Yoshi's Island / Ultimate Guitar Kit 2:** For atmospheric percussion and solo guitars.

![Screenshot 1: Channel Rack in FL Studio wth loaded Soundfont Players, colored in dirrerent hues](/assets/about-my-music-1.png)

---

## 2. Piano: The Cassette Effect and the Dialogue Between Both Hands

Since I can't play the piano live, the Piano Roll has become my keyboard. And here I've discovered a few key secrets.

### *Secret #1: The "Old Cassette" Secret (Detune & Layering)*

Sometimes I want to achieve that very "worn-out" sound, as if we're hearing a piano from an old game that's been sitting in an abandoned hall of many years.

**When I use layering:**
I clone the piano channel. On the second layer, I turn the *Fine Tune* knob in the settings (MISC) to **+12 or +15 cents**. If I add an equalizer with a low-pass filter to this layer, it starts to sound "muted" and "warm". When the clean and detuned layers play together, a slight "beating" (chorus) effect occurs.

### *Secret #2: The Art of Polyphony (A Dialogue Between Two Hands)*

For a long time, I made a mistake: my left hand simply "supported" the right, repeating the rhythm of the chords. As a result, everything sounded flat. Listen to *Death by Glamour* or *Spider Dance* - there, both hands are busy.

**The secret of the "conversation":**
I stopped thinking of the piano as a single instrument. Now I imagine it as **two different musicians**.

* **Right Hand (Soloist):** Leads the melody, jumps across octaves, uses grace notes and syncopation.

* **Left Hand (Rhythm Section):** It doesn't just play chords; it "dances" along with the main melody. It fills in the soloist's pauses. When the right hand plays a long note, the left hand starts playing a fast, bouncy bass line. When the right hand starts "running", the left hand pauses on heavy, accented beats.

**How I Achieve This (The "Interlocking" Technique):**

1. **Interval:** I try to make the right and left hands move in opposite directions. If the right hand's melody goes up, the left hand (the bass line) goes down. This expands the sonic pallete and makes the track sound "mature".
2. **The Discipline of Silence:** I've stopped being afraid to include pauses in the accompaniment. In *Death by Glamour*, the piano constantly makes "staccato stabs". I program the left hand so that it plays only in those micro-moments when the right hand isn't busy with a complex passage. This creates "intervals of clarity".
3. **Humanization (Breathing):** To make the dialogue between the hands sound natural, I apply **Strum (`Alt`+`S`)** to the left-hand chords, but with a very low value. This creates the illusion that the pianist physically cannot strike all the keys at once, and it adds that very "vintage" quality that is missing in "sterile" tracks.

![Screenshot 2: Piano Roll, showing that the right-hand notes (melody) and left-hand notes (rhythm) almost never play simultaneously on the downbeats in dence passages](/assets/about-my-music-2.png)

---

## 3. Rhythm: How to Make Music Groove

As someone who couldn't keep a beat on a real drum kit, I found my zen in FL Studio. To make a track groove, you need to follow a couple of rules:

* **No Long Notes:** The bass in battle tracks shouldn't drone. I make the notes extremely short (staccato) and turn off the *Release* parameter. The bass should snap: *"Boom! Band!"*
* **Octave jumps (Slap effect):** To make a 16-bit bass sound like a cool bassist, I insert short notes an octave higher on the off-beat. This "click" instantly gives the track a funky bounce.
* **Ghost Notes:** Between the main, loud hits, I add micro-notes with very low volume (Velocity 30-40). You can barely hear them, but they create an aggressive "rustle".
* **The Magic of Swing:** In battle themes, I turn the global *Swing* up by 20-30%. The even 16th notes start to lag slightly , and the rhythm begins to brazenly "limp".

![Screenshot 3: Bass part with bright red notes, octave jumps, and pale "ghost" notes in between](/assets/about-my-music-3.png)

---

## 4. Harmony: How to Ligitimately Break Hearts

You can whistle Toby Fox's melodies with just one finger, but they bring tears to your eyes because of *how* they interact with the harmony.

* **The "Breathless" Rule (Syncopation):** I almost never start main melodies exactly on the 'one' beat. I take a micro-pause and come in on the "and". It counds like a character has taken an uncertain breath.
* **Octave Doubling:** At the climax, I always duplicate the melody an octave higher. This instantly makes the sound huge and "concert-like".
* **Minor SUbdominant (Toby Chord):** Let's say we're playing a warm theme in C major. And suddenly, at the very end of the phrase, I insect an F minor chord (**Fm**). This foreign note in the middle of the major chord takes your breath away.
* **Diminished Chords and Tritones:** In boss fights, I use "wrong" notes. The blues tritone grates on the ear and gives the track a defiant edge. And I use diminished chords right before the drop - they sound like mounting panic or a system crash.

---

## 5. Conposition Architecture: Thinking in Phases

The most common mistake is to write a cool 4-bar loop and copy it for 3 minutes. A boss fight is all about drama. Here's my favorite structure:

1. **Intro (Vacuum):** A muffled filter (Low Pass), a strange rhythm. Tension hangsin the air.
2. **Drop:** An explosion. A heavy bass and the main melody kick in.
3. **Stalking:** The guitars and kick drum fade out. Only the edge violins and pulsating bass remain.
4. **Breakdown (The Pit / Sorrow):** A brilliant trick. The track's tempo doesn't change, but the drums start playing in **half-time** (the snare drum hits half as often). The harmony shifts to minor, and the choir enters. The music suddenly becomes massive and tragic.
5. **Total Climax:** We returnto the original tempo, the melody soars into the octaves, and there's a hard stereo pan.
6. **Finale:** Here are three ways I handle endings:
    1. **Natural Fade-out:** Instead of abruptly cutting off all tracks, I program an 8-bar fade-out
    2. **Echo in silence:** In the last bar, everything falls silent, leaving only a single high note (from a bell, for example) that lingers in the air for 5-6 seconds
    3. **System crash:** In the last bar, I set the Master Pitch automation to drop sharply by -1 semitone; it sounds like someone yanked the plug out of an old tape recorder

![Screenshot 4: Wide view of the Playlist, where the track is divided into segments: Intro, Drop, B-section, Climax](/assets/about-my-music-4.png)

---

## 6. Mixing for Hooligans (The Mixing Magic)

Indie music should bite. A mix that's too clean kills the character.

* **Distortion on the violins:** If I need an aggressive lead, I take classic violins (Detache), slap some guitar overdrive (*Fruity Blood Overdrive*) on them, and cut the lows. The violin screeches like a chainsaw.
* **Digital Pollen (Ping-Pong Delay):** To fill the space with magic, I take a music box (Celesta), write fast arpeggios in the 6th octave, and run *Fruity Delay 3* in Ping-Pong mode. The sound jumps from my left ear to my right, like a swarm of fireflies.
* **Sidechain:** In the final climaxes, when 10 instruments are playing, I heavily sidechain the bass and drum pads (through the Fruity Limiter). The entire mix begins to "sway" rhythmically to the drum beats, making room for the rhythm.
* **Floating Tape:** I send the *Fruity Pitch Shifter* to the Master channel and draw an automation curve that slowly shifts the pitch of the entire track up and down by 3–5 cents.
* **Seamless Looping:** When exporting a track for games, I always select the **"Wrap Remainder"** mode in FL Studio. The reverb tail from the end of the track is neatly carried over to the beginning of the file, and the music plays endlessly in the game without any clicks.

---

## Instead of a conclusion

Bringing melodies from your head into the real world is a complex process, especially when your fingers aren't used to flying across the keys. But digital instruments give us incredible freedom.

Retro-RPG music is a triumph of emotion over technology. It's the ability to take a cheap synthesizer from the '90s, add a little "grit", make the bass bounce rhythmically, and let the melody speak to the listener.

Don't be afraid of silence. Don't be afraid of "wrong" dissonant notes. And when you hit Play and get goosebumps - that means your've found your magic.

*Someday I'll add a player with my tracks here.*
