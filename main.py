import requests
import time
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1003004470180")
MONITORED_USERNAMES = os.getenv("MONITORED_USERNAMES", "").split(",")
FOLLOWING_FILE = "following_lists.json"
CHECK_INTERVAL = 60  # seconds

class TwitterAPI:
    def __init__(self):
        self.session = requests.Session()
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN", "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA")
        self.ct0 = os.getenv("TWITTER_CT0", "0cc140d1c5bbc2d6a5982653bf7103f01c2fb218019b09851221cbb1c64bee200ac0de753b53bf1316f2f08e1b48e15e97ef23be488cecba7e5b5decaaf92690aba8f9febaaa1b336b103b6efdf7fffb")
        self.auth_token = os.getenv("TWITTER_AUTH_TOKEN", "ec726039280b6c8ae0d4b8829ef53b5605e44607")

    def load_cookies(self):
        """Load cookies from the provided request"""
        cookies = {
            'guest_id': 'v1%3A175966151672660509',
            'gt': '1974789648829354466',
            '__cuid': '08f39168271c4546abfe28ace44a98f9',
            'd_prefs': 'MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw',
            'guest_id_ads': 'v1%3A175966151672660509',
            'guest_id_marketing': 'v1%3A175966151672660509',
            'personalization_id': '"v1_1Rm6A3VA96PKQpV9CGa6jw=="',
            'kdt': 'MVb6vFQnGFojTlUZX3Prr7i5B2CLffVDTLmSWsbJ',
            'auth_token': self.auth_token,
            'ct0': self.ct0,
            'twid': 'u%3D1803671138293174272',
            'att': '1-yVmUGx4cwRaX37p2Aocbw1SeDlnwiOCNwuZjn5WB',
            'lang': 'en',
            '_twitter_sess': 'BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCo0DLSZAToMY3NyZl9p%250AZCIlZDRkODRkNDExOTI1ZjQ1NTE1MTUzNzBmNTZkOWQ0YTY6B2lkIiViMGU5%250AMDBiOTJiNTk1M2RkY2RlMjAxZGUxNmFjNjdhNQ%253D%253D--755b2d90848b93ca90cde99a412cff2058f6d54c',
            '__cf_bm': '4ME_U3xrwl5CuPCfbu8.la3Hq.1DNb3bOYCPoN.3HzE-1759662306-1.0.1.1-fDYvKhAIPYbkBaHCtlV.ZaO6D788wh502HItgr5nnwVvbTHFuBB.Ci.FKev5nuf.fSk1_p8Fo_W2squ2wAUSsiasoMWUikyyATwIYPPSDCU',
            'cf_clearance': '.N7.ackq53TNFGmkwuI4P9X59urmNQBxTP_TMyewtfY-1759662322-1.2.1.1-eOF9dJxpllEOg84ILDIW_e4dpt5IubiKFbz8ovr8Dx7DCjYy.HXaOf59o3ZQtz3ybDKv.4XcCmqLVg3IaZ8LMqwtBU1cbiz.Hd1XJe5ufKxsi_tmSUyxRJPQTBBEJ2gzU5ImoAKnQ2pFnclVdb66dVCvbheGjUPxfWwJsCCk8Sl6hzkBFiN4w8UirnYPpTfzDtdPK5dMcZsRjDthlc1cCF1xT_Zz._ZF6Sih.rihMfA',
            'dnt': '1'
        }
        for name, value in cookies.items():
            self.session.cookies.set(name, value, domain='.x.com')
        print("Loaded Twitter session cookies")

    def get_user_id(self, username):
        """Get user ID using the new GraphQL endpoint"""
        try:
            url = "https://x.com/i/api/graphql/vqu78dKcEkW-UAYLw5rriA/useFetchProfileSections_canViewExpandedProfileQuery"
            params = {
                'variables': json.dumps({"screenName": username})
            }
            headers = {
                'Authorization': f'Bearer {self.bearer_token}',
                'x-csrf-token': self.ct0,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/json',
                'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en'
            }
            response = self.session.get(url, params=params, headers=headers)
            print(f"get_user_id for @{username}: Status {response.status_code}, Response: {response.text[:200]}...")
            if response.status_code == 200:
                data = response.json()
                encoded_id = data.get('data', {}).get('user_result_by_screen_name', {}).get('result', {}).get('id')
                if encoded_id:
                    try:
                        decoded_id = base64.b64decode(encoded_id).decode('utf-8')
                        user_id = decoded_id.split(':')[1] if ':' in decoded_id else decoded_id
                        print(f"Got user ID for @{username}: {user_id}")
                        return user_id
                    except Exception as e:
                        print(f"Error decoding user ID for @{username}: {e}")
                        return None
                else:
                    print(f"No user ID found for @{username}")
                    return None
            else:
                print(f"Error getting user ID: {response.status_code}, Response: {response.text}")
                return None
        except Exception as e:
            print(f"Error getting user ID for @{username}: {e}")
            return None

    def get_following_list(self, username):
        """Get list of users followed by the given username"""
        following = set()
        try:
            user_id = self.get_user_id(username)
            if not user_id:
                print(f"No user ID found for @{username}")
                return following

            url = "https://x.com/i/api/graphql/XKrIB4_YBx_J3JsUyDbruw/Following"
            cursor = None
            max_requests = 50
            request_count = 0

            while request_count < max_requests:
                variables = {
                    "userId": user_id,
                    "count": 20,
                    "includePromotedContent": False,
                    "withGrokTranslatedBio": False
                }
                if cursor:
                    variables["cursor"] = cursor

                params = {
                    'variables': json.dumps(variables),
                    'features': json.dumps({
                        "rweb_video_screen_enabled": False,
                        "payments_enabled": False,
                        "profile_label_improvements_pcf_label_in_post_enabled": True,
                        "rweb_tipjar_consumption_enabled": True,
                        "verified_phone_label_enabled": False,
                        "creator_subscriptions_tweet_preview_api_enabled": True,
                        "responsive_web_graphql_timeline_navigation_enabled": True,
                        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                        "premium_content_api_read_enabled": False,
                        "communities_web_enable_tweet_community_results_fetch": True,
                        "c9s_tweet_anatomy_moderator_badge_enabled": True,
                        "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
                        "responsive_web_grok_analyze_post_followups_enabled": True,
                        "responsive_web_jetfuel_frame": True,
                        "responsive_web_grok_share_attachment_enabled": True,
                        "articles_preview_enabled": True,
                        "responsive_web_edit_tweet_api_enabled": True,
                        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                        "view_counts_everywhere_api_enabled": True,
                        "longform_notetweets_consumption_enabled": True,
                        "responsive_web_twitter_article_tweet_consumption_enabled": True,
                        "tweet_awards_web_tipping_enabled": False,
                        "responsive_web_grok_show_grok_translated_post": False,
                        "responsive_web_grok_analysis_button_from_backend": True,
                        "creator_subscriptions_quote_tweet_preview_enabled": False,
                        "freedom_of_speech_not_reach_fetch_enabled": True,
                        "standardized_nudges_misinfo": True,
                        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                        "longform_notetweets_rich_text_read_enabled": True,
                        "longform_notetweets_inline_media_enabled": True,
                        "responsive_web_grok_image_annotation_enabled": True,
                        "responsive_web_grok_imagine_annotation_enabled": True,
                        "responsive_web_grok_community_note_auto_translation_is_enabled": False,
                        "responsive_web_enhance_cards_enabled": False
                    })
                }

                headers = {
                    'Authorization': f'Bearer {self.bearer_token}',
                    'x-csrf-token': self.ct0,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br, zstd',
                    'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/json',
                    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'x-twitter-active-user': 'yes',
                    'x-twitter-auth-type': 'OAuth2Session',
                    'x-twitter-client-language': 'en'
                }

                response = self.session.get(url, params=params, headers=headers)
                print(f"Batch {request_count + 1} Response status: {response.status_code}")
                if response.status_code != 200:
                    print(f"Error fetching following: {response.status_code}, Response: {response.text}")
                    break

                data = response.json()
                # Log the full response structure for debugging
                print(f"Batch {request_count + 1} Response (first 2000 chars): {json.dumps(data, indent=2)[:2000]}...")
                
                instructions = data.get('data', {}).get('user', {}).get('result', {}).get('timeline', {}).get('timeline', {}).get('instructions', [])

                cursor = None
                found_users = 0

                for instruction in instructions:
                    if instruction.get('type') == 'TimelineAddEntries':
                        for entry in instruction.get('entries', []):
                            entry_id = entry.get('entryId', '')
                            print(f"Processing entry: {entry_id}")
                            if entry_id.startswith('user-'):
                                content = entry.get('content', {})
                                item_content = content.get('itemContent', {})
                                user_results = item_content.get('user_results', {})
                                user_result = user_results.get('result', {})

                                # Try multiple paths to find screen_name and name
                                core = user_result.get('core', {})
                                legacy = user_result.get('legacy', {})
                                followed_username = core.get('screen_name') or legacy.get('screen_name') or user_result.get('screen_name')
                                name = core.get('name') or legacy.get('name') or user_result.get('name')

                                # Debug the user_result structure
                                if not (followed_username and name):
                                    print(f"Skipped user {entry_id}: no screen_name or name. User result: {json.dumps(user_result, indent=2)[:500]}...")
                                    continue

                                following.add((followed_username, name))
                                found_users += 1
                                print(f"Added user: @{followed_username} ({name})")
                            elif entry_id.startswith('cursor-bottom-'):
                                cursor = entry.get('content', {}).get('value')
                                print(f"Found cursor: {cursor}")

                print(f"Batch {request_count + 1}: Found {found_users} users, Total: {len(following)}")
                if not cursor:
                    print("No more pages (cursor not found)")
                    break

                request_count += 1
                time.sleep(1)  # Avoid rate limits

            print(f"Found {len(following)} accounts for @{username}")
            return following

        except Exception as e:
            print(f"Error getting following list for @{username}: {e}")
            return following

def send_telegram_message(message):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=data, timeout=30)
        print(f"send_telegram_message Response status: {response.status_code}, Response: {response.text}")
        if response.status_code == 200:
            print("Notification sent")
        else:
            print(f"Failed to send notification: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")

def load_previous_following():
    """Load previously saved following lists"""
    if os.path.exists(FOLLOWING_FILE):
        try:
            with open(FOLLOWING_FILE, 'r') as f:
                data = json.load(f)
                return {username: set(tuple(item) for item in following_list)
                        for username, following_list in data.items()}
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Corrupted data file, starting fresh: {e}")
            return {}
    return {}

def save_following_lists(following_dict):
    """Save following lists to file"""
    data = {username: list(following_set)
            for username, following_set in following_dict.items()}
    print(f"Saving to {FOLLOWING_FILE}: {json.dumps(data, indent=2)[:500]}...")  # Debug what’s being saved
    try:
        with open(FOLLOWING_FILE, 'w') as f:
            json.dump(data, f)
        print(f"Saved following lists to {FOLLOWING_FILE}")
    except Exception as e:
        print(f"Error saving following lists: {e}")

def monitor_follows():
    """Monitor followed accounts and send notifications for new follows"""
    api = TwitterAPI()
    api.load_cookies()

    # Test Telegram connectivity
    send_telegram_message("Starting Twitter Follow Monitor for @0xs8n")

    previous_following = load_previous_following()
    if not previous_following:
        print("\nInitializing following lists...")
        current_following = {}
        for username in MONITORED_USERNAMES:
            following = api.get_following_list(username)
            current_following[username] = following
            print(f"Initialized @{username} with {len(following)} accounts")
            time.sleep(5)
        save_following_lists(current_following)
        print("\nInitialization complete")
        previous_following = current_following

    cycle_count = 0
    while True:
        cycle_count += 1
        print(f"\nChecking at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Cycle #{cycle_count})")
        try:
            for username in MONITORED_USERNAMES:
                current_following = api.get_following_list(username)
                prev_following = previous_following.get(username, set())
                new_follows = current_following - prev_following

                if new_follows:
                    print(f"\n@{username}: {len(new_follows)} new follows detected")
                    for username_followed, name_followed in new_follows:
                        message = f"<b>New Follow Alert</b>\n\n"
                        message += f"<b>@{username}</b> is now following:\n"
                        message += f"<b>{name_followed}</b> (@{username_followed})\n"
                        message += f"https://x.com/{username_followed}"
                        print(f"Now following: @{username_followed}")
                        send_telegram_message(message)
                        time.sleep(1)
                    previous_following[username] = current_following
                else:
                    print(f"@{username}: No new follows")
                time.sleep(5)

            save_following_lists(previous_following)
            print(f"\nNext check in {CHECK_INTERVAL} seconds")
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            time.sleep(60)

if __name__ == "__main__":
    # Fancy startup banner
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

    print(f"\n{BOLD}{RED}╔══════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{RED}║            MAYANG BOT ACTIVATED           ║{RESET}")
    print(f"{BOLD}{RED}╚══════════════════════════════════════════╝{RESET}\n")

    print("Twitter Follow Monitor")
    print(f"Monitoring {len(MONITORED_USERNAMES)} accounts")
    print(f"Check interval: {CHECK_INTERVAL} seconds\n")

    try:
        monitor_follows()
    except KeyboardInterrupt:
        print("\nStopping monitor...")
