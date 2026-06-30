import sys
from src.utils.logger import logger
from src.utils.config import config

def main():
    """
    Main entry point for the AI MC project.
    Verifies that the project foundation (Phase 0) is correctly set up.
    """
    banner = """
    ==================================================
    *                                                *
    *               AI LIVE STREAM MC                *
    *              Phase 0: Foundation               *
    *                                                *
    ==================================================
    """
    print(banner)
    logger.info("Initializing AI Live Stream MC system...")

    # Log application metadata
    app_name = config.get("app.name", "AI_MC")
    app_version = config.get("app.version", "0.0.0")
    app_env = config.get("app.env", "unknown")
    logger.info(f"Loaded App: {app_name} v{app_version} ({app_env} environment)")

    # Print selected configurations for verification
    logger.info(f"Logging file path: {config.get('logging.file_path')}")
    logger.info(f"Voice provider configured: {config.get('voice.provider')}")
    logger.info(f"Voice name: {config.get('voice.voice_name')}")
    logger.info(f"Avatar model configured: {config.get('avatar.model_name')}")
    logger.info(f"OBS WebSocket destination: {config.get('streaming.obs_websocket.host')}:{config.get('streaming.obs_websocket.port')}")

    logger.info("Project Foundation (Phase 0) verification successful. Ready for Phase 1.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
