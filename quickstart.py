#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Text-To-Speech API sample application .
Example usage:
    python synthesize_text.py --text "hello"
    python synthesize_text.py --ssml "<speak>Hello there.</speak>"
"""

import argparse
import os
import sys


# [START tts_synthesize_text]
def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Standard-C',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
# [END tts_synthesize_text]


# [START tts_synthesize_ssml]
def synthesize_ssml(ssml):
    """Synthesizes speech from the input string of ssml.
    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    Example: <speak>Hello there.</speak>
    """
    # ssml_string = ssml

    ssml_string = ''
    with open(ssml, "r") as textfile:
        for line in textfile.readlines():
            ssml_string += line

    ssml_string = ssml_string.replace('\n','')

    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(ssml=ssml_string)

    print("************")
    print(input_text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Standard-C',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
# [END tts_synthesize_ssml]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text',
                       help='The text from which to synthesize speech.')
    group.add_argument('--ssml',
                       help='The ssml string from which to synthesize speech.')

    args = parser.parse_args()

    if args.text:
        synthesize_text(args.text)
    else:
        synthesize_ssml(args.ssml)
