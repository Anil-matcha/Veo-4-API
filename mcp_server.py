import os
import json
from mcp.server.fastmcp import FastMCP
from veo4_api import Veo4API

# Initialize FastMCP server
mcp = FastMCP("Veo 4 API Server")

def get_api():
    return Veo4API()

@mcp.tool()
def text_to_video(prompt: str, aspect_ratio: str = "16:9", duration: int = 8,
                  quality: str = "4k", with_audio: bool = False,
                  camera_control: str = None) -> str:
    """
    Generate a native 4K video from a text prompt using Veo 4 by Google DeepMind.

    Veo 4 features a 3x larger Transformer than Veo 3, native 4K output,
    integrated audio generation, and advanced camera controls.

    :param prompt: Descriptive text prompt.
    :param aspect_ratio: Video aspect ratio (e.g., '16:9', '9:16', '1:1').
    :param duration: Duration in seconds (8–30).
    :param quality: '1080p' or '4k'.
    :param with_audio: Set True to jointly generate audio alongside the video.
    :param camera_control: Optional camera movement (e.g., 'pan left', 'zoom in', 'orbit').
    """
    api = get_api()
    result = api.text_to_video(prompt, aspect_ratio, duration, quality, with_audio, camera_control)
    return json.dumps(result, indent=2)

@mcp.tool()
def image_to_video(prompt: str, images_list: list[str], aspect_ratio: str = "16:9",
                   duration: int = 8, quality: str = "4k", with_audio: bool = False,
                   camera_control: str = None) -> str:
    """
    Animate static images into a native 4K video using Veo 4.

    Reference images in the prompt using @image1, @image2, etc.

    :param prompt: Text prompt guiding the animation.
    :param images_list: List of image URLs to animate.
    :param aspect_ratio: Video aspect ratio.
    :param duration: Duration in seconds (8–30).
    :param quality: '1080p' or '4k'.
    :param with_audio: Set True to jointly generate audio.
    :param camera_control: Optional camera movement hint.
    """
    api = get_api()
    result = api.image_to_video(prompt, images_list, aspect_ratio, duration, quality, with_audio, camera_control)
    return json.dumps(result, indent=2)

@mcp.tool()
def text_to_video_with_audio(prompt: str, aspect_ratio: str = "16:9", duration: int = 8,
                              quality: str = "4k", camera_control: str = None) -> str:
    """
    Generate a Veo 4 video with integrated audio from a text prompt.

    Veo 4 generates synchronized dialogue, ambient sound, and music in one pass.
    Include explicit audio cues in the prompt (e.g. 'waves crashing', 'crowd cheering').

    :param prompt: Text prompt. Include audio cues for richer sound.
    :param aspect_ratio: Video aspect ratio.
    :param duration: Duration in seconds (8–30).
    :param quality: '1080p' or '4k'.
    :param camera_control: Optional camera movement hint.
    """
    api = get_api()
    result = api.text_to_video_with_audio(prompt, aspect_ratio, duration, quality, camera_control)
    return json.dumps(result, indent=2)

@mcp.tool()
def image_to_video_with_audio(prompt: str, images_list: list[str], aspect_ratio: str = "16:9",
                               duration: int = 8, quality: str = "4k",
                               camera_control: str = None) -> str:
    """
    Animate images into a Veo 4 video with integrated audio.

    :param prompt: Text prompt. Reference images with @image1, @image2, etc.
    :param images_list: List of image URLs to animate.
    :param aspect_ratio: Video aspect ratio.
    :param duration: Duration in seconds (8–30).
    :param quality: '1080p' or '4k'.
    :param camera_control: Optional camera movement hint.
    """
    api = get_api()
    result = api.image_to_video_with_audio(prompt, images_list, aspect_ratio, duration, quality, camera_control)
    return json.dumps(result, indent=2)

@mcp.tool()
def character_video(prompt: str, character_images: list[str], aspect_ratio: str = "16:9",
                    duration: int = 8, quality: str = "4k", with_audio: bool = False) -> str:
    """
    Generate a video with consistent character identity using Veo 4's character anchoring.

    Keeps faces, clothing, and distinguishing features consistent across all frames.

    :param prompt: Scene description. Reference the character with @image1.
    :param character_images: 1–3 reference image URLs of the character.
    :param aspect_ratio: Video aspect ratio.
    :param duration: Duration in seconds.
    :param quality: '1080p' or '4k'.
    :param with_audio: Set True to jointly generate audio.
    """
    api = get_api()
    result = api.character_video(prompt, character_images, aspect_ratio, duration, quality, with_audio)
    return json.dumps(result, indent=2)

@mcp.tool()
def extend_video(request_id: str, prompt: str = "", duration: int = 8,
                 quality: str = "4k") -> str:
    """
    Extend a previously generated Veo 4 video.

    :param request_id: ID of the video segment to extend.
    :param prompt: Optional prompt to guide the continuation.
    :param duration: Seconds to extend by (8–30).
    :param quality: '1080p' or '4k'.
    """
    api = get_api()
    result = api.extend_video(request_id, prompt, duration, quality)
    return json.dumps(result, indent=2)

@mcp.tool()
def video_edit(prompt: str, video_urls: list[str], images_list: list[str] = None,
               aspect_ratio: str = "16:9", quality: str = "4k") -> str:
    """
    Edit an existing video using natural language with Veo 4.

    :param prompt: Describe the desired edits.
    :param video_urls: List of video URLs to edit.
    :param images_list: Optional reference image URLs.
    :param aspect_ratio: Output video aspect ratio.
    :param quality: '1080p' or '4k'.
    """
    api = get_api()
    result = api.video_edit(prompt, video_urls, images_list, aspect_ratio, quality)
    return json.dumps(result, indent=2)

@mcp.tool()
def upload_file(file_path: str) -> str:
    """
    Upload a local file (image or video) to MuAPI for use in generation tasks.

    :param file_path: Local path to the file.
    """
    api = get_api()
    result = api.upload_file(file_path)
    return json.dumps(result, indent=2)

@mcp.tool()
def get_task_status(request_id: str) -> str:
    """
    Check the status and get results of a Veo 4 generation task.

    :param request_id: The ID returned from a generation tool call.
    """
    api = get_api()
    result = api.get_result(request_id)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()
