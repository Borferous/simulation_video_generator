import os
import time
from dotenv import load_dotenv
from obswebsocket import obsws, requests

# Load .env file
load_dotenv()

# OBS WebSocket credentials
host = os.getenv("OBS_HOST", "localhost")
port = int(os.getenv("OBS_PORT", 4455))
password = os.getenv("OBS_PASSWORD", "")

# Connect to OBS
ws = obsws(host, port, password)

# Scene and recordings folder
SCENE_NAME = "game_scene"  # <-- OBS scene name
PROJECT_DIR = os.path.dirname(__file__)
RECORDINGS_DIR = os.path.join(PROJECT_DIR, "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)

def test_connection():
    """Test OBS connection and get info."""
    try:
        ws.connect()
        print("✅ Connected to OBS successfully!")
        version_info = ws.call(requests.GetVersion())
        print(f"OBS Version: {version_info.getObsVersion()}")
        print(f"WebSocket Version: {version_info.getObsWebSocketVersion()}")
        scenes = ws.call(requests.GetSceneList())
        print(f"Available scenes: {[scene['sceneName'] for scene in scenes.getScenes()]}")
        current_scene = ws.call(requests.GetCurrentProgramScene())
        print(f"Current scene: {current_scene.getCurrentProgramSceneName()}")
        status = ws.call(requests.GetRecordStatus())
        print(f"Recording active: {status.getOutputActive()}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def startRecord():
    """Switch to specific scene, set folder, and start recording."""
    try:
        if not test_connection():
            return False
        
        # Switch to desired scene
        print(f"Switching to scene: {SCENE_NAME}")
        ws.call(requests.SetCurrentProgramScene(sceneName=SCENE_NAME))
        time.sleep(0.5)
        
        # Set recording folder to project recordings directory
        ws.call(requests.SetRecordDirectory(directory=RECORDINGS_DIR))
        print(f"Recording directory set to: {RECORDINGS_DIR}")
        
        # Start recording
        status = ws.call(requests.GetRecordStatus())
        if status.getOutputActive():
            print("⚠️ Already recording!")
            return False
        ws.call(requests.StartRecord())
        time.sleep(0.5)
        
        # Verify
        status = ws.call(requests.GetRecordStatus())
        if status.getOutputActive():
            print(f"✅ Recording started! Scene: {SCENE_NAME}")
            return True
        else:
            print("❌ Recording failed to start")
            return False
    except Exception as e:
        print(f"❌ Error starting recording: {e}")
        return False

def stopRecord():
    """Stop OBS recording."""
    try:
        status = ws.call(requests.GetRecordStatus())
        if not status.getOutputActive():
            print("⚠️ Not currently recording")
            return False
        ws.call(requests.StopRecord())
        print("✅ Recording stopped!")
        return True
    except Exception as e:
        print(f"❌ Error stopping recording: {e}")
        return False

def disconnect():
    """Disconnect from OBS."""
    try:
        ws.disconnect()
        print("✅ Disconnected from OBS")
    except Exception as e:
        print(f"❌ Error disconnecting: {e}")
