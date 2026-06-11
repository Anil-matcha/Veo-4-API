import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Veo4API:
    def __init__(self, api_key=None):
        """
        Initialize the Veo 4 API client.
        :param api_key: Your MuAPI.ai API key. Defaults to MUAPI_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("MUAPI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required. Set MUAPI_API_KEY in .env or pass it to the constructor.")

        self.base_url = "https://api.muapi.ai/api/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def text_to_video(self, prompt, aspect_ratio="16:9", duration=8, quality="4k",
                      with_audio=False, camera_control=None):
        """
        Submits a Veo 4 Text-to-Video (T2V) generation task.

        Veo 4 by Google DeepMind generates native 4K video using an upgraded
        Transformer architecture (3x parameters vs Veo 3). Supports integrated
        audio generation and advanced camera controls.

        :param prompt: The text prompt describing the video.
        :param aspect_ratio: Video aspect ratio (e.g., '16:9', '9:16', '1:1').
        :param duration: Video duration in seconds (8–30).
        :param quality: Output quality ('1080p' or '4k').
        :param with_audio: Whether to jointly generate audio alongside the video.
        :param camera_control: Optional camera movement hint (e.g., 'pan left',
                               'zoom in', 'orbit', 'tracking shot').
        :return: JSON response with request_id.
        """
        endpoint = f"{self.base_url}/veo-4-t2v"
        if with_audio:
            endpoint = f"{self.base_url}/veo-4-t2v-audio"
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "quality": quality,
        }
        if camera_control:
            payload["camera_control"] = camera_control
        return self._post_request(endpoint, payload)

    def image_to_video(self, prompt, images_list, aspect_ratio="16:9", duration=8,
                       quality="4k", with_audio=False, camera_control=None):
        """
        Submits a Veo 4 Image-to-Video (I2V) generation task.

        Animate one or more static images into a native 4K video. Reference images
        in the prompt using @image1, @image2, etc.

        :param prompt: Text prompt to guide the animation. Use @image1, @image2, etc.
        :param images_list: A list of image URLs to animate.
        :param aspect_ratio: Video aspect ratio.
        :param duration: Video duration in seconds (8–30).
        :param quality: Output quality ('1080p' or '4k').
        :param with_audio: Whether to jointly generate audio alongside the video.
        :param camera_control: Optional camera movement hint.
        :return: JSON response with request_id.
        """
        endpoint = f"{self.base_url}/veo-4-i2v"
        if with_audio:
            endpoint = f"{self.base_url}/veo-4-i2v-audio"
        payload = {
            "prompt": prompt,
            "images_list": images_list,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "quality": quality,
        }
        if camera_control:
            payload["camera_control"] = camera_control
        return self._post_request(endpoint, payload)

    def text_to_video_with_audio(self, prompt, aspect_ratio="16:9", duration=8,
                                 quality="4k", camera_control=None):
        """
        Generate a Veo 4 video with integrated audio from a text prompt.

        Veo 4 generates synchronized dialogue, ambient sound, and music jointly
        in one pass. Include audio cues in the prompt for best results
        (e.g. 'waves crashing', 'crowd cheering', 'piano melody').

        :param prompt: Text prompt. Include audio cues for richer sound.
        :param aspect_ratio: Video aspect ratio.
        :param duration: Video duration in seconds (8–30).
        :param quality: Output quality ('1080p' or '4k').
        :param camera_control: Optional camera movement hint.
        :return: JSON response with request_id.
        """
        return self.text_to_video(
            prompt, aspect_ratio, duration, quality,
            with_audio=True, camera_control=camera_control
        )

    def image_to_video_with_audio(self, prompt, images_list, aspect_ratio="16:9",
                                  duration=8, quality="4k", camera_control=None):
        """
        Animate images into a Veo 4 video with integrated audio.

        :param prompt: Text prompt. Reference images with @image1, @image2, etc.
                       Include audio cues for richer output.
        :param images_list: List of image URLs to animate.
        :param aspect_ratio: Video aspect ratio.
        :param duration: Video duration in seconds (8–30).
        :param quality: Output quality ('1080p' or '4k').
        :param camera_control: Optional camera movement hint.
        :return: JSON response with request_id.
        """
        return self.image_to_video(
            prompt, images_list, aspect_ratio, duration, quality,
            with_audio=True, camera_control=camera_control
        )

    def character_video(self, prompt, character_images, aspect_ratio="16:9",
                        duration=8, quality="4k", with_audio=False):
        """
        Generate a video with consistent character identity using Veo 4's
        character anchoring technology.

        Veo 4 keeps faces, clothing, and distinguishing features consistent
        across all frames, even through complex movements and camera changes.

        :param prompt: Scene description. Reference the character with @image1.
        :param character_images: List of 1–3 reference image URLs of the character.
        :param aspect_ratio: Video aspect ratio.
        :param duration: Video duration in seconds.
        :param quality: Output quality ('1080p' or '4k').
        :param with_audio: Whether to jointly generate audio.
        :return: JSON response with request_id.

        Example::

            result = api.character_video(
                prompt="@image1 walks through a futuristic city, confident stride",
                character_images=["https://example.com/person.jpg"],
                aspect_ratio="16:9",
                duration=8,
                quality="4k",
            )
            video = api.wait_for_completion(result["request_id"])
            print(video["outputs"][0])
        """
        endpoint = f"{self.base_url}/veo-4-character"
        payload = {
            "prompt": prompt if "@image1" in prompt else f"@image1 {prompt.strip()}",
            "images_list": character_images,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "quality": quality,
            "with_audio": with_audio,
        }
        return self._post_request(endpoint, payload)

    def extend_video(self, request_id, prompt="", duration=8, quality="4k"):
        """
        Extends a previously generated Veo 4 video.

        :param request_id: The request_id of the video segment to extend.
        :param prompt: Optional text prompt to guide the continuation.
        :param duration: Seconds to extend by (8–30).
        :param quality: Output quality ('1080p' or '4k').
        :return: JSON response with request_id.
        """
        endpoint = f"{self.base_url}/veo-4-extend"
        payload = {
            "request_id": request_id,
            "prompt": prompt,
            "duration": duration,
            "quality": quality,
        }
        return self._post_request(endpoint, payload)

    def video_edit(self, prompt, video_urls, images_list=None, aspect_ratio="16:9",
                   quality="4k"):
        """
        Edit an existing video using natural language with Veo 4.

        :param prompt: Describe the desired edits.
        :param video_urls: List of video URLs to edit.
        :param images_list: Optional list of reference image URLs.
        :param aspect_ratio: Output video aspect ratio.
        :param quality: Output quality ('1080p' or '4k').
        :return: JSON response with request_id.
        """
        endpoint = f"{self.base_url}/veo-4-video-edit"
        payload = {
            "prompt": prompt,
            "video_urls": video_urls,
            "images_list": images_list or [],
            "aspect_ratio": aspect_ratio,
            "quality": quality,
        }
        return self._post_request(endpoint, payload)

    def _post_request(self, endpoint, payload):
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def upload_file(self, file_path):
        """
        Uploads a local file (image or video) to MuAPI for use in generation tasks.

        :param file_path: Path to the local file to upload.
        :return: JSON response containing the URL of the uploaded file.
        """
        endpoint = f"{self.base_url}/upload_file"
        headers = {"x-api-key": self.api_key}
        with open(file_path, "rb") as file_data:
            files = {"file": file_data}
            response = requests.post(endpoint, headers=headers, files=files)
        response.raise_for_status()
        return response.json()

    def get_result(self, request_id):
        """
        Polls for the result of a Veo 4 generation task.

        :param request_id: The request_id returned from a generation call.
        :return: JSON response with status and outputs.
        """
        endpoint = f"{self.base_url}/predictions/{request_id}/result"
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, request_id, poll_interval=5, timeout=600):
        """
        Blocks until a Veo 4 generation task completes and returns the result.

        :param request_id: The request_id returned from a generation call.
        :param poll_interval: Seconds between status polls (default 5).
        :param timeout: Maximum seconds to wait before raising TimeoutError (default 600).
        :return: Completed result JSON with 'outputs' list.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self.get_result(request_id)
            status = result.get("status")

            if status == "completed":
                return result
            elif status == "failed":
                raise Exception(f"Video generation failed: {result.get('error')}")

            print(f"Status: {status}. Waiting {poll_interval} seconds...")
            time.sleep(poll_interval)

        raise TimeoutError("Timed out waiting for Veo 4 video generation to complete.")


if __name__ == "__main__":
    try:
        api = Veo4API()
        prompt = "A cinematic tracking shot through a lush rainforest, sunlight filtering through the canopy, birds calling"

        print(f"Submitting T2V task with prompt: {prompt}")
        submission = api.text_to_video(prompt=prompt, duration=8, quality="4k")
        request_id = submission.get("request_id")
        print(f"Task submitted. Request ID: {request_id}")

        print("Waiting for completion...")
        result = api.wait_for_completion(request_id)
        print(f"Generation completed! Video URL: {result.get('outputs', [None])[0]}")

    except Exception as e:
        print(f"Error: {e}")
