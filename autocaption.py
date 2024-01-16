import os
import tempfile
import time
import json

import torch
import ffmpeg

from moviepy.editor import CompositeVideoClip, TextClip, VideoFileClip

start = time.time()

directory = tempfile.gettempdir()

def create_audio(videofilename):
    extension = os.path.splitext(videofilename)[1]
    audiofilename = videofilename.replace(extension, ".mp3")

    # Create the ffmpeg input stream
    input_stream = ffmpeg.input(videofilename)

    # Extract the audio stream from the input stream
    audio = input_stream.audio

    # Save the audio stream as an MP3 file
    output_stream = ffmpeg.output(audio, audiofilename)

    # # Overwrite output file if it already exists
    output_stream = ffmpeg.overwrite_output(output_stream)

    ffmpeg.run(output_stream)

    return audiofilename

def get_final_cliped_video(
    videofilename,
    wordlevel_info,
    # v_type,
    # subs_position,
    # highlight_color,
    # fontsize,
    # opacity,
    # color,
    # font,
    # stroke_color,
    # stroke_width,
    # kerning,
    # right_to_left,
):  
    input_video = VideoFileClip(videofilename)

    print("wordlevel_info", wordlevel_info["segments"])

    FONT_SIZE = 70
    TEXT_POSITION = ('center', 'center')

    subs = [input_video]
    for segment in wordlevel_info["segments"]:
        for word in segment["words"]:
            text = word["text"].upper().replace(",", "")
            start = word["start"]
            end = word["end"]
            duration = end - start
            txt_clip = (TextClip(text, fontsize=FONT_SIZE, font="Poppins/Poppins-ExtraBoldItalic.ttf", color='white', stroke_width=1, stroke_color='black').set_start(start).set_duration(duration))
            txt_clip = txt_clip.set_position(TEXT_POSITION)
            subs.append(txt_clip)

    print('about to composite video clip')

    final_video = CompositeVideoClip(subs, size=input_video.size)

    # Set the audio of the final video to be the same as the input video
    final_video = final_video.set_audio(input_video.audio)
    destination = os.path.join(directory, "output.mp4")
    # Save the final clip as a video file with the audio included
    final_video.write_videofile(destination, fps=24, codec="libx264", audio_codec="aac")
    return destination


def add_subtitle(
    videofilename,
    v_type,
    transcript_json,
    # subs_position,
    # highlight_color,
    # fontsize,
    # opacity,
    # MaxChars,
    # color,
    # font,
    # stroke_color,
    # stroke_width,
    # kerning
):
    print("video type is: " + v_type)


    outputfile = get_final_cliped_video(
        videofilename,
        transcript_json
        # v_type,
        # subs_position,
        # highlight_color,
        # fontsize,
        # opacity,
        # color,
        # font,
        # stroke_color,
        # stroke_width,
        # kerning
    )
    return outputfile