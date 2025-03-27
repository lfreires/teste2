from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def extract_audio_from_video(video_path, output_dir=None):
    # Garante que o caminho existe
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {video_path}")

    # Extrai o nome base do arquivo (sem pasta, sem extensão)
    base_name = os.path.splitext(os.path.basename(video_path))[0]

    # Define o caminho de saída
    if output_dir is None:
        output_dir = os.path.dirname(video_path)

    os.makedirs(output_dir, exist_ok=True)
    output_audio_path = os.path.join(output_dir, f"{base_name}.mp3")

    print('Transformando em MP3...')
    # Extração segura com liberação de recursos
    with VideoFileClip(video_path) as video:
        if video.audio is None:
            raise ValueError("O vídeo não contém áudio.")
        video.audio.write_audiofile(output_audio_path, codec='libmp3lame')
    print('Video transformado!')
    return output_audio_path