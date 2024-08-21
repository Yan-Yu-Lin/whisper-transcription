# Whisper Transcription Project

## Overview

This project utilizes OpenAI's Whisper model to transcribe audio and video files. It provides an automated workflow for processing multiple files, organizing transcriptions, and managing the transcription history.

## Features

- Transcribe audio and video files using OpenAI's Whisper model
- Automatic file organization for input and output
- Maintains a history of transcriptions
- Supports multiple audio and video formats

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7 or higher
- pip (Python package manager)
- Git (for version control)

You'll also need an OpenAI API key to use the Whisper model.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Yan-Yu-Lin/whisper-transcription.git
   cd whisper-transcription
   ```

2. Create a virtual environment:
   ```
   python -m venv myenv
   ```

3. Activate the virtual environment:
   - On macOS and Linux:
     ```
     source myenv/bin/activate
     ```
   - On Windows:
     ```
     myenv\Scripts\activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Project Structure

The project creates and uses the following folder structure:
- `Processing_Video`: Place your audio/video files here for transcription
- `Processed_Video`: Processed files are moved here after transcription
- `Result_Text`: Contains the latest transcription results
- `Result_Archive`: Stores previous transcription results

## Usage

1. Place the audio or video files you want to transcribe in the `Processing_Video` folder.

2. Run the transcription script:
   ```
   python transcribe.py
   ```

3. The script will process all files in the `Processing_Video` folder:
   - Transcribe each file using the Whisper model
   - Move processed files to the `Processed_Video` folder
   - Save transcriptions in the `Result_Text` folder
   - Move any existing transcriptions to the `Result_Archive` folder

4. Check the `Result_Text` folder for your transcriptions.

## Supported File Formats

This project supports the following input file types:
- Audio: mp3, wav, m4a, flac, aac, ogg, wma
- Video: mp4, avi, mov, wmv, flv, mkv

## Troubleshooting

If you encounter any issues:
1. Ensure your OpenAI API key is correctly set in the `.env` file
2. Check that you have sufficient API credits with OpenAI
3. Verify that your input files are in a supported format
4. Make sure you're running the script from the project root directory

## Contributing

Contributions to improve the project are welcome. Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the Whisper model
- All contributors who have helped to improve this project
