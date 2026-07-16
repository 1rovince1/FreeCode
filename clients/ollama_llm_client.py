import logging

from ollama import AsyncClient

from config.env_config import env_settings

logger = logging.getLogger(__name__)


class OllamaClient:
    def __init__(self):
        self.client = None

    async def connect(self):
        logger.info("Connecting to Ollama client...")
        self.client = AsyncClient(
            host = "https://ollama.com",
            headers = {"Authorization": "Bearer " + env_settings.OLLAMA_API_KEY}
        )
        logger.info("Connected to Ollama client!")

    async def disconnect(self):
        logger.info("Disconnecting from Ollama client...")
        self.client = None
        logger.info("Disconnected from Ollama client!")

ollama_manager = OllamaClient()