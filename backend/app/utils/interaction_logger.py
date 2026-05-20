from utils.logger import setup_logger

logger = setup_logger()


def log_interaction(user_id: str, query: str, response: str) -> None:

    try:

        safe_user_id = user_id.replace("\n", "").replace("\r", "")[:50]

        safe_query = query.replace("\n", " ").replace("\r", " ")[:500]

        safe_response = response.replace("\n", " ").replace("\r", " ")[:500]

        logger.info(f"[{safe_user_id}] Query: {safe_query}")

        logger.info(f"[{safe_user_id}] Response: {safe_response}")

    except Exception as e:

        logger.error(f"Failed to log interaction: {str(e)}")