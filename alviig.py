import random
import time
from instagrapi import Client
from instagrapi.exceptions import ClientError

class SafeInstagramFollower:
    def __init__(self):
        self.cl = Client()
        # Anti-detection settings
        self.cl.set_locale('en_US')
        self.cl.set_country('US')
        self.cl.set_country_code(1)
        self.cl.set_device({
            "manufacturer": "Apple",
            "model": "iPhone 13,4",
            "android_version": 26,
            "android_release": "8.0.0"
        })
        self.cl.set_user_agent('Instagram 219.0.0.12.117 Android')
        # Removed set_uuids to avoid demand for generate_uuid
        
    def login(self, username, password):
        try:
            # Try to load previous session to avoid frequent logins
            self.cl.load_settings('session.json')
            self.cl.login(username, password)
        except Exception as e:
            print(f"Regular login failed: {e}. Trying with proxy...")
            self.cl.set_proxy(self.get_random_proxy())
            self.cl.login(username, password)
        self.cl.dump_settings('session.json')
    
    def get_random_proxy(self):
        proxies = [
            'http://user:pass@proxy1:port',
            'http://user:pass@proxy2:port',
            # Add more proxies
        ]
        return random.choice(proxies)
    
    def safe_follow(self, user_id):
        try:
            time.sleep(random.randint(30, 120))
            if random.random() > 0.7:
                self.cl.user_stories(user_id)
                time.sleep(random.randint(5, 15))
            result = self.cl.user_follow(user_id)
            if random.random() > 0.5:
                medias = self.cl.user_medias(user_id, amount=3)
                for media in random.sample(medias, min(len(medias), random.randint(1, 3))):
                    time.sleep(random.randint(10, 30))
                    self.cl.media_like(media.id)
            return result
        except ClientError as e:
            print(f"Error following {user_id}: {e}")
            if "rate limited" in str(e).lower():
                self.handle_rate_limit()
            return False
    
    def handle_rate_limit(self):
        print("Rate limit detected. Sleeping for 1-2 hours...")
        time.sleep(random.randint(3600, 7200))
        self.cl.set_proxy(self.get_random_proxy())
    
    def mass_follow(self, username_list, max_follows=2000):
        successful_follows = 0
        for username in username_list:
            if successful_follows >= max_follows:
                break
            try:
                user_id = self.cl.user_id_from_username(username)
                if self.safe_follow(user_id):
                    successful_follows += 1
                    print(f"Successfully followed {username} ({successful_follows}/{max_follows})")
                    if successful_follows % 50 == 0:
                        nap_time = random.randint(900, 1800)
                        print(f"Taking a {nap_time//60} minute break...")
                        time.sleep(nap_time)
            except Exception as e:
                print(f"Error processing {username}: {e}")
        print(f"Finished! Successfully followed {successful_follows} users.")

# Usage Example
if __name__ == "__main__":
    bot = SafeInstagramFollower()
    bot.login("vin_calisa", "1234alvinkalisa")
    target_users = ["user1", "user2", "user3"]  # Replace with your
    
    