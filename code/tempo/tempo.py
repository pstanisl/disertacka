from __future__ import print_function
from functools import partial
from os import makedirs
from os.path import basename, exists, join, splitext

import argparse
import noiser as ns
import re
import wavext

from utils import load_file, load_mlf_to_dict

parser = argparse.ArgumentParser()
parser.add_argument('scp', help='file path to the file list')
parser.add_argument('mlf', help='file path to the aligment')

parser.add_argument('-t', '--tempo', action='store', help='tempo')

parser.add_argument('-o', '--output', action='store',
                    help='output folder')

parser.add_argument('-a', action='store_true',
                    help='output is from AP recognizer')

parser.add_argument('-s', '--skip', action='store_true',
                    help='skip missing')

parser.set_defaults(output='./')
parser.set_defaults(tempo=100)


def reader(sound, params):
    """Method used by the Noiser lib as a read callback.

    Args:
        sound: list with the raw WAV samples (bind by partial)
        params: dictionary with params used for reading the
                original WAV file (bind by partial)

    Return:
        list: window of raw audio samples from the sound file
    """
    # Get index of the current window
    index = params['index']
    # Read proper window from the raw Wav samples
    samples = sound[100 * index: 100 * (index + 1)]
    # Return nothing if the window is empty
    if not samples:
        return None
    # Check if it is save to schedule another effect
    # (because of limitation in noiser.ScheduleEffect)
    if params['schedule']:
        # Is another effect available?
        try:
            effect = next(params['effects'])
            print('[INFO] - scheduling effect in reader')
            # Schedule the effect
            params['noiser'].ScheduleEffect(effect)
        except StopIteration:
            # No effect available
            pass
        params['schedule'] = False

    # Increase the index of the window for further processing
    params['index'] += 1
    # Return array with samples (window)
    return samples


def writer(output, params, sound, applied_effects):
    """Method used by the Noiser lib as a write callback.

    Args:
        output: array with previously saved samples (bind by partial)
        sound: raw WAV samples (Noiser)
        applied_effects: applied effects (Noiser)
    """
    # Check if the next effect was applied and if so, set the flag
    # to schedule a another. Schedule if some effect was applied and
    # for the effect was not scheduled another. It saves windows so
    # the effect can be applied over multiple windows.
    if applied_effects and applied_effects[0] != params['effect']:
        params['effect'] = applied_effects[0]
        params['schedule'] = True

    output.extend(sound)


def get_effects(noiser, alignment, phonemes, tempo):
    # Definition of the regular expression used to parsing an alignment line
    re_alignment = re.compile(r'(\d+).(\d+).([^\b]+)')
    # Initialization of the effect index
    effect_index = 1
    stop_prev = 0
    # Go through all alignments and create noiser effect for
    # changing the tempo of the part of the audio from the alignment.
    for line in alignment:
        # Check if a phoneme is in aligment line
        if not any(map(lambda p: '-{}+'.format(p) in line, phonemes)):
            continue
        # Parse alignment line
        match = re_alignment.match(line)
        # Skip line that is not in match with regular expression used
        # to parsing the line
        if not match:
            continue
        # Get start and stop time of the alignment of the phoneme,
        # values are in hunderts of nanoseconds
        start = int(match.group(1)) / 10000
        stop = int(match.group(2)) / 10000
        print('[INFO] - creting an effect id={} for {} from {} duration {} tempo={}'.format(
            effect_index, match.group(3), start, stop - start, tempo))
        # Create an effect changing the tempo of the sound in
        # the interval <start; stop - start>
        effect = noiser.BuildNewEffect(ns.TYPE_TEMPO, effect_index)

        effect.SetWait(effect_index - 1)

        effect.SetValue(effect.TYPE_DELAY, start - stop_prev)
        effect.SetValue(effect.TYPE_LENGT, stop - start)
        effect.SetValue(effect.TYPE_RATIO, tempo)
        # return created effect
        yield effect
        # Increase the index of the sound effect generated by the noiser
        effect_index += 1
        # Save end of current segment
        stop_prev = stop


def merge(content):
    # Regullar expression pattern for parsing values from the MLF. The
    # AP format is more rich.
    re_filter = re.compile(r'(\d+)\s(\d+)\s([^\[]+)')
    # variable initialization used in merge cycle
    phoneme_prev = ''
    start_prev = 0
    stop_prev = 0
    # Go through content of the AP decoder mlf result. In this format,
    # they are some items multiple times. This cycle merge this lines
    # into one with proper time interval.
    for item in content:
        match = re_filter.match(item)
        # Continue with next line because the current line is in
        # the unknown format.
        if not match:
            continue
        # Every line contains start and stop time in hunderts of
        # nanoseconds and phoneme. Some lines can contain other info,
        # but for the tempo change effect are irrelevant.
        start, stop, phoneme = match.groups()

        if not phoneme_prev == phoneme:
            # yield only regular items. If the 'phoneme_prev' is empty it
            # means that no line was processed yet
            if phoneme_prev:
                yield '{start} {stop} {phoneme}'.format(
                    start=start_prev, stop=stop_prev, phoneme=phoneme_prev)
            # Save new values for
            phoneme_prev = phoneme
            start_prev = start
        # Move stop time
        stop_prev = stop
    else:
        # yield last part of the mlf
        yield '{start} {stop} {phoneme}'.format(
            start=start_prev, stop=stop_prev, phoneme=phoneme_prev)


def process_ap(alignment):
    ret = {}

    for key, content in alignment.items():
        ret[key] = list(merge(content))

    return ret


def get_wave(paths):
    for path in paths:
        # Get the name of the file, in the alignment it is used as a key
        name = basename(splitext(path)[0])
        # Load wave and return to the further processing
        yield name, wavext.WavRead(path)


def process(waves, alignemnt, output_dir, tempo, skip=False):
    # Check existence of the output directory
    if not exists(output_dir):
        print('[INFO] - creating output directory: {}'.format(output_dir))
        makedirs(output_dir)
    # List with all phonemes where the effect would applied
    phonemes = ['b', 'd', 'D', 'k', 's', 'v', 'S']
    # Go through all the WAV files and apply the Tempo effect
    # based on the alignment
    for index, (name, wave) in enumerate(waves):
        print('[INFO] - processing file {}'.format(name))
        # Create instance of the noiser for the wave file
        noiser = ns.Noiser('file://Noiser.db', wave.getframerate())
        # Get raw sound
        sound = wave[:]
        # Create generator with effects, because the Noiser ScheduleEffect has
        # the limitation in the number (33) of ScheduledEffects at once. First
        # we schedule 10 effects and then after applying an effect another is
        # scheduled.
        # If the alignemt is not available, just create empty iterator and the
        # file is then just copied.
        effects = get_effects(noiser, alignemnt[name], phonemes, tempo) \
            if name in alignemnt else iter(())
        # Skip file that is not in the alignemt
        if name not in alignemnt:
            print('[WARNING] - missing alignemt for file', name)
            if skip:
                print('[INFO] - skipping processing file', name)
                continue
        # Initialize variable used in data read and write calbacks.
        params = {
            # Index of applied effect (used in writer)
            'effect': -1,
            # Iterator with all effects.
            'effects': effects,
            # Index of the windows (used in reader)
            'index': 0,
            # Instance of the Noiser used to scheduling of
            # the effects (used in reader)
            'noiser': noiser,
            # Flag used to schedule next effect (in reader)
            'schedule': False
        }
        output = []
        # Bind variables to the callbacks used by the Noiser lib
        reader_partial = partial(reader, sound, params)
        writer_partial = partial(writer, output, params)
        # Schedule first 10 effects, because ScheduleEffect has limitation. It
        # is able schedule only 33 effects at once. Other effects are scheduled
        # after applying previous effect. One applied (in writer) another
        # scheduled (in readed - beacuse of lock in writer).
        for index in range(10):
            try:
                effect = next(effects)
                noiser.ScheduleEffect(effect)
            except StopIteration:
                break
        print('[INFO] - initial effects applied')
        # Apply noiser effects
        noiser.Run(reader_partial, writer_partial)
        # Creating output path
        output_path = join(output_dir, '{}.wav'.format(name))
        print('[INFO] - saving to {}'.format(output_path))
        # Write the output into a wav file
        wavext.WriteWav(output_path, output, wave.getframerate(), 1)


def main(args):
    # Load alignment of the phonemes
    alignment = load_mlf_to_dict(args.mlf, clean=False)
    # Merge items in the mlf if the output is from AP decoder
    if (args.a):
        alignment = process_ap(alignment)
    # Load path to the processed WAV files, should corresponds to the alignment
    paths = load_file(args.scp)
    # Load WAV files
    waves = get_wave(paths)
    # Use Noiser library to the changing of the tempo
    process(waves, alignment, args.output, int(args.tempo), args.skip)


if __name__ == '__main__':
    # Load run argumengs
    args = parser.parse_args()
    # Start the processing
    main(args)
