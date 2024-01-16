# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

import json
import os
import shutil
import tempfile
from typing import List

from cog import BasePredictor, Input, Path

import autocaption

class Predictor(BasePredictor):
    def setup(self) -> None:
        """No setup needed."""

    def predict(
        self,
        video_file_input: Path = Input(description="Video file"),
        transcript_json_string: str = Input(description="Transcript json"),
        subs_position: str = Input(
            description="Subtitles position",
            choices=["bottom75", "center", "top", "bottom", "left", "right"],
            default="bottom75",
        ),
        color: str = Input(description="Caption color", default="white"),
        highlight_color: str = Input(description="Highlight color", default="yellow"),
        fontsize: float = Input(
            description="Font size. 7.0 is good for videos, 4.0 is good for reels",
            default=4.0,
        ),
        MaxChars: int = Input(
            description="Max characters space for subtitles. 20 is good for videos, 10 is good for reels",
            default=10,
        ),
        opacity: float = Input(
            description="Opacity for the subtitles background", default=0.0
        ),
        font: str = Input(
            description="Font",
            default="Poppins/Poppins-ExtraBold.ttf",
            choices=[
                "Poppins/Poppins-Bold.ttf",
                "Poppins/Poppins-BoldItalic.ttf",
                "Poppins/Poppins-ExtraBold.ttf",
                "Poppins/Poppins-ExtraBoldItalic.ttf",
                "Poppins/Poppins-Black.ttf",
                "Poppins/Poppins-BlackItalic.ttf",
                "Atkinson_Hyperlegible/AtkinsonHyperlegible-Bold.ttf",
                "Atkinson_Hyperlegible/AtkinsonHyperlegible-BoldItalic.ttf",
                "M_PLUS_Rounded_1c/MPLUSRounded1c-ExtraBold.ttf",
                "Arial/Arial_Bold.ttf",
                "Arial/Arial_BoldItalic.ttf",
            ],
        ),
        stroke_color: str = Input(description="Stroke color", default="black"),
        stroke_width: float = Input(description="Stroke width", default=2.6),
        kerning: float = Input(description="Kerning for the subtitles", default=-5.0),
    ) -> List[Path]:
        """Run a single prediction on the model"""
        temp_dir = tempfile.mkdtemp()
        extension = os.path.splitext(video_file_input)[1]
        videofilename = os.path.join(temp_dir, f"input{extension}")
        shutil.copyfile(video_file_input, videofilename)

        # audiofilename = autocaption.create_audio(videofilename)
        # wordlevel_info = autocaption.transcribe_audio(self.model, audiofilename)

        # print("wordlevel_info", wordlevel_info)

        print("json string", transcript_json_string)
        transcript_json = json.loads(transcript_json_string)
        print("transcript json", transcript_json)
        
        outputs = []
        
        outputfile = autocaption.add_subtitle(
            videofilename,
            "other aspect ratio",  # v_type is unused
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
            # kerning,
        )

        outputs.append(Path(outputfile))
        
        return outputs