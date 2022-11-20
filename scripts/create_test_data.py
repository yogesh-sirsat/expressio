import json

import markdown as md
import markdownify as mdfy
import requests

from main.models import *

DEV_API = "https://dev.to/api"
ADMIN_USER = User.objects.get(username="yogesh")

# Creating test data from dev.to api's instead of lorem ipsum data just to give small real touch to
# whoever browsing the project, this data from dev.to is not getting used for any traffic or ads, its
# just for a dummy test data purpose.

# Number of articles to create.
ARTICLE_COUNTER = 2

# Number of users to create.
USER_COUNTER = 1


class MakeApiCall:

    def __init__(self, api):
        self.get_data(api)

        # parameters = {
        #     "username": "kedark"
        # }
        # self.get_data_by_params(api, parameters)

    def user_data_to_file(self, user_data_obj):
        with open("scripts/test_user_data_output.json", "w") as output_file:
            output = json.dumps(user_data_obj, sort_keys=True, indent=4)
            print(output, file=output_file)
            output_file.close()

    def get_data(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            print("sucessfully fetched the data.")
            return self.process_response_data(response.json())
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")
            return {}

    def get_data_by_params(self, api, parameters):
        response = requests.get(f"{api}", params=parameters)
        if response.status_code == 200:
            print("sucessfully fetched the data.")
            return self.process_response_data(response.json())
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")

    def get_user_data(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            user_data_obj = response.json()
            self.user_data_to_file(user_data_obj)
            print("sucessfully fetched the user data.")
            return self.create_user_from_data(user_data_obj)
        else:
            print(
                f"Hello person, there's a {response.status_code} error with your request")
            return {}

    def create_user_from_data(self, new_user_data):
        # global USER_COUNTER
        try:
            new_user = new_user_data["username"]
            new_user_email = f"{new_user}@expressio.live"
            new_user_password = f"{os.getenv('DUMMY_PASSWORD_PREFIX')}{new_user}"
            user = User.objects.create(
                username=new_user, first_name=new_user_data["name"], email=new_user_email, password=new_user_password)
            if (new_user_data["summary"]):
                user.profile.bio = new_user_data["summary"]
                user.profile.save(update_fields=["bio"])
            print(f"Created a new user: {user.username}.")
            # USER_COUNTER -= 1
            return user
        except:
            print("Error while creating new user from data.")
            return {}

    def create_comments_from_article_data(self, comment_data_obj, parent_post, parent_comment=False):
        try:
            for data_obj in comment_data_obj:
                comment_user = User.objects.filter(username=data_obj["user"]["username"])
                if comment_user.exists():
                    comment_author = comment_user[0]
                    print(f"Got the existing user for comment author.")
                else:
                    comment_author = self.get_user_data(f"{DEV_API}/users/{data_obj['user']['user_id']}")
                    if not comment_author:
                        comment_author = ADMIN_USER
                        print(f"Using admin user as a comment author.")
                comment_content = md.markdown(mdfy.markdownify(data_obj["body_html"], heading_style="ATX"))
                if not parent_comment:
                    new_comment = Comment.objects.create(author=comment_author, post=parent_post,
                                                         content=comment_content)
                    print(f"Created new comment.")
                    if data_obj["children"]:
                        self.create_comments_from_article_data(data_obj["children"], parent_post, new_comment)
                    else:
                        print("Replies of comment is empty or none")
                else:
                    new_comment = Comment.objects.create(author=comment_author, post=parent_post,
                                                         content=comment_content, parent=parent_comment)
                    print(f"Created new reply for comment.")
        except:
            print("Processing comments failed.")
            return {}

    def process_response_data(self, data_obj):
        global ARTICLE_COUNTER
        if isinstance(data_obj, list):
            if len(data_obj) > 0:
                if data_obj[0]["type_of"] == "comment":
                    print("Got the comments!")
                    return data_obj
                else:
                    print("Wrong list object.")
                    return {}
            else:
                print("Data is empty or none.")
                return {}
        elif data_obj["type_of"] == "article":
            print("Got the article!")
            article_already_created = Post.objects.filter(
                source=data_obj["url"])
            if article_already_created.exists():
                print("Article already created!")
                comment_data_obj = self.get_data(f"{DEV_API}/comments?a_id={data_obj['id']}")
                print(f"typeof comment data obj: {type(comment_data_obj)}")
                self.create_comments_from_article_data(comment_data_obj, article_already_created[0])
                # ARTICLE_COUNTER -= 1
            else:
                if data_obj["user"]:
                    try:
                        user = User.objects.get(
                            username=data_obj["user"]["username"])
                        print("Got the existing user.")
                    except:
                        user_id = data_obj["user"]["user_id"]
                        user = self.get_user_data(f"{DEV_API}/users/{user_id}")
                        if not user:
                            user = ADMIN_USER
                            print("Assigning article to admin user")
                else:
                    user = ADMIN_USER
                    print("Assigning article to admin user")

                article_content_cleaned = md.markdown(data_obj["body_markdown"])

                post_title = data_obj["title"]
                post_content = article_content_cleaned
                post_description = data_obj["description"]
                if data_obj["cover_image"] is None:
                    post_thumbnail_url = data_obj["social_image"]
                    print("using social image")
                else:
                    post_thumbnail_url = data_obj["cover_image"]
                    print("using cover image")

                post_tags = data_obj["tags"]
                post_source = data_obj["url"]
                try:
                    new_post = Post.objects.create(author=user, title=post_title, description=post_description,
                                                   content=post_content, source=post_source)
                    print("Created new post successfully!")
                    print(
                        f"author: {new_post.author} | title: {new_post.title}")
                    ARTICLE_COUNTER -= 1
                    if post_tags:
                        new_post.tags.add(*post_tags)
                    try:
                        new_post.thumbnail_url = post_thumbnail_url
                        new_post.save()
                    except:
                        print("Saving thumbnail failed.")
                    print(f"Comments count of new article: {data_obj['comments_count']}")
                    comment_data_obj = self.get_data(f"{DEV_API}/comments?a_id={data_obj['id']}")
                    self.create_comments_from_article_data(comment_data_obj, new_post, False)
                except:
                    print("Creating new post failed!")
                    return {}
            return False
        elif data_obj["type_of"] == "user":
            if User.objects.filter(username=data_obj["username"]).exists():
                print("User already exists in our DB.")
                return {}
            else:
                self.user_data_to_file(data_obj)
                return self.create_user_from_data(data_obj)
        print("Failed to get any data.")
        return {}


# if __name__ == "__main__":
#     api_call = MakeApiCall(f"{DEV_API}/articles/270180")


def make_api_call_for_articles():
    # Make api call for articles.

    # Counter: 150589 - 150740, 160740 - 
    init_count = ARTICLE_COUNTER
    article_id = 160740
    while ARTICLE_COUNTER:
        MakeApiCall(f"{DEV_API}/articles/{article_id}")
        article_id += 1
        print(f"<<<<<<<<<<<<<<<<<<<<<<<<<<<< Article Id Tried Fetch: {article_id} >>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(f"<<<<<<<<<<<<<<<<<<<<<<<<<<<< Success Api Call Count: {init_count - ARTICLE_COUNTER} >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")


def make_api_call_for_users():
    # Make api call for users.

    # Counter: 55003
    MakeApiCall(f"{DEV_API}/users/64628")


def run():
    # make_api_call_for_users()
    # ------------------------- #
    make_api_call_for_articles()
