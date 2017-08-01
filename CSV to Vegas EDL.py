#! /usr/bin/env python

import argparse
import csv
import decimal
import os.path


def get_clips(filename):  # Gets clips from CSV file.
    row_number = 0
    clips = []
    with open(filename, 'r', newline='') as csvfile:  # Open CSV file.
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:  # Read each row
            row_number += 1
            if row_number > 3 and row != []:  # For every non-empty line after
                # line 3...
                row = row[0].split(',')  # Split string into list.
                row[0] = int(row[0]) + 1  # Increase scene number / ID by 1 to
                # make place for first clip added later.
                row[0] = str(row[0])  # Convert back to string
                row.pop(1)  # Remove starting frame number
                row.pop(1)  # Remove timecode
                row[1] = decimal.Decimal(row[1])  # Convert string to decimal
                row[2] = decimal.Decimal(row[2])
                clips.append(row)  # Add row to list of clips
    clips.insert(0, ['1', decimal.Decimal(
        '0000.0000'), clips[0][1]])  # Create clip from beginning of
    # video up to first cut.
    return clips


def seconds_to_milliseconds(clips):  # Convert clip starting points and
    # lengths from seconds to milliseconds.
    for clip in clips:  # For each clip...
        clip[1] = (
            decimal.Decimal(clip[1]) * decimal.Decimal(
                1000))  # Convert starting point
        clip[2] = (
            decimal.Decimal(clip[2]) * decimal.Decimal(
                1000))  # Convert length
        clip[1] = clip[1].quantize(
            decimal.Decimal('.0001'))  # Round to four decimals.
        clip[2] = clip[2].quantize(decimal.Decimal('.0001'))
        clip[1] = str(clip[1])  # Convert to string.
        clip[2] = str(clip[2])
    return clips


def edl(outfile, clips, videof):  # Creates Vegas EDL file from clips list.
    f = open(outfile, 'w')
    f.write('"ID";"Track";"StartTime";"Length";"PlayRate";'
            '"Locked";"Normalized";"StretchMethod";"Looped";'
            '"OnRuler";"MediaType";"FileName";"Stream";'
            '"StreamStart";"StreamLength";"FadeTimeIn";'
            '"FadeTimeOut";"SustainGain";"CurveIn";"GainIn";'
            '"CurveOut";"GainOut";"Layer";"Color";"CurveInR";'
            '"CurveOutR":"PlayPitch";"LockPitch"\n')
    for clip in clips:  # For every clip clip
        f.write(
            '%s;    1;    %s;    %s;    1.000000;    FALSE;    FALSE;    '
            '0;    TRUE;    FALSE;    VIDEO;    "%s";    0;    '
            '%s;    %s;    0.0000;    0.0000;    1.000000;    4;    '
            '0.000000;    4;    0.000000;    0;    -1;    4;    4;    '
            '0.000000;    FALSE\n' % (
                clip[0], clip[1], clip[2], videof, clip[1],
                clip[2]))  # Add video track of clip to EDL.
    for clip in clips:
        f.write('%s;    0;    %s;    %s;    1.000000;    FALSE;    FALSE;   '
                '0;    TRUE;    FALSE;    AUDIO;    "%s";    0;   '
                '%s;    %s;    0.0000;    0.0000;    1.000000;    2;    '
                '0.000000;    -2;    0.000000;    0;    -1;    -2;    2;    '
                '0.000000;    FALSE\n' % (
                    clip[0], clip[1], clip[2], videof, clip[1],
                    clip[2]))  # Add audio track of clip to EDL.
    f.close()


class command_line_arguments():  # Parses command-line arguments
    parser = argparse.ArgumentParser(
        description='Convert PySceneDetect CSV files to Vegas EDL files.')

    parser.add_argument(
        'VIDEO_FILE', help='Video file that you used PySceneDetect on.',
        action='store')  # Add command-line argument for locating video file.
    parser.add_argument(
        'INFILE', help='CSV file to convert (will not be touched).',
        action='store')  # Add command-line argument for locating CSV file.
    parser.add_argument(
        '-o', '--outfile',
        help='Name of the Vegas EDL text file. Default: \"[INFILE].txt.\"',
        action='store')  # Add command-line argument for
    # naming the Vegas EDL text file.

    args = parser.parse_args()

    global videof
    global infile
    global outfile
    videof = os.path.abspath(
        args.VIDEO_FILE)  # Assign variable from command-line argument value
    infile = args.INFILE  # Assign variable from command-line argument value
    outfile = args.outfile  # Assign variable from command-line argument value
    if outfile is None:  # If outfile is not passed...
        outfile = infile.replace('.csv', '.txt')  # Assign outfile the
        # value of infile and change extension.
    if not outfile.endswith(
            '.txt'):  # If outfile does not have the extension ".txt".
        outfile = '{}.txt'.format(outfile)  # Add TXT file extension.


class Main():
    command_line_arguments()
    clips = get_clips(infile)
    decimal.getcontext().rounding = decimal.ROUND_DOWN
    clips = seconds_to_milliseconds(clips)
    edl(outfile, clips, videof)
    print('\n--> {}'.format(os.path.abspath(outfile)))


if __name__ == '__main__':
    Main()
