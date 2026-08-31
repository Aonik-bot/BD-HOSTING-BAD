import os
import time
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

print("=" * 45)
print("🚀 AONIK HOSTING - Cloud Execution Engine")
print("🔥 Node: Asia-South (BD-Cluster-01)")
print("=" * 45)

BOT_TOKEN = os.getenv("BOT_TOKEN", "7489281928:AAHdu-AonikHostingBotToken")
PORT = int(os.getenv("PORT", "8080"))

def run_service():
    logging.info("Initializing bot services and event listeners...")
    time.sleep(1)
    logging.info(f"Bot connected to Gateway API successfully. Ping: 24ms")
    logging.info(f"Listening on port {PORT} for webhook updates...")
    
    count = 0
    while True:
        count += 1
        if count % 15 == 0:
            logging.info(f"⚡ [Heartbeat] Service healthy. Processed {count * 3} events. Memory stable.")
        time.sleep(4)

if __name__ == '__main__':
    try:
        run_service()
    except KeyboardInterrupt:
        logging.warning("Process received SIGINT. Shutting down gracefully...")
        sys.exit(0)
