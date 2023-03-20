import os
import openai
import streamlit as st

STORY_ELEMENTS = {
    "genres": ["Adventure", "Fantasy", "Mystery", "Science Fiction", "Historical Fiction", "Fairy Tales", "Superheroes", "Comedy", "Drama", "Horror"],
    "main characters": ["Animals", "Humans", "Mythical Creatures", "Robots or AI", "Aliens", "Superheroes", "Pirates", "Time Travelers", "Explorers", "Magical Beings"],
    "settings": ["Forest", "City", "Outer Space", "Underwater", "Desert", "Jungle", "Mountains", "Arctic or Antarctic", "Time Travel", "Alternate Universes or Dimensions"],
    "themes": ["Friendship", "Bravery", "Kindness", "Creativity", "Curiosity", "Perseverance", "Teamwork", "Responsibility", "Respect", "Environmentalism"],
    "plot devices": ["Quests", "Riddles", "Time Travel", "Magical Objects", "Secret Passageways", "Hidden Treasure", "Unexpected Allies", "Escapes and Chases", "Parallel Worlds", "Transformations"]
}


def main():
    st.set_page_config(
        page_title="StorySmoosh",
        page_icon=":book:",
        layout="centered")
    st.image(
        "https://em-content.zobj.net/thumbs/240/apple/325/open-book_1f4d6.png",
        width=100,
    )
    display_welcome_screen()
    api_key = get_api_key_from_user()
    initialize_openai_api(api_key)
    user_selections = collect_user_input()

    if st.button("Generate Story"):
        with st.spinner("Smooshing story..."):
            generated_story = create_story(
                user_selections, user_selections["show_api_info"])

        if user_selections['generate_images']:
            with st.spinner("Generating images..."):
                paragraphs = split_story_into_paragraphs(generated_story)
                summaries = summarize_paragraphs(
                    paragraphs, user_selections["show_api_info"])
                image_urls = generate_images_from_summaries(
                    summaries, user_selections['style'], user_selections["show_api_info"])
                display_images(paragraphs, image_urls)
        else:
            display_story_output_screen(generated_story)


def get_api_key_from_user():
    api_key = st.text_input("Enter your OpenAI API Key:",
                            value="", type="password")
    return api_key


def initialize_openai_api(api_key):
    openai.api_key = api_key


def display_welcome_screen():
    st.title("Welcome to StorySmoosh")
    st.subheader(
        "Create a unique and fun story by choosing your favorite story elements.")
    st.subheader("Let's get started!")


def collect_user_input():
    user_selections = {}
    for category, options in STORY_ELEMENTS.items():
        user_selections[category] = st.selectbox(
            f"Choose a {category[:-1]}", options)
    user_selections["age"] = st.slider("Child's Age", 3, 12)
    user_selections["show_api_info"] = st.checkbox(
        "Show API prompts and models", value=False)
    user_selections["generate_images"] = st.checkbox(
        "Generate images", value=True)

    if user_selections["generate_images"]:
        styles = ["Cartoon", "Realistic", "Watercolor",
                  "Sketch", "Comic", "Pixel Art", "Minimalist"]
        user_selections["style"] = st.selectbox(
            "Choose the desired style for the images:", styles)
    else:
        user_selections["style"] = None

    return user_selections


def create_story(user_selections, show_api_info):
    prompt = f"You write the most wonderful children's stories. You always start with a title and write a complete short story with a resolving ending. Create a {user_selections['genres']} story for a {user_selections['age']}-year-old child featuring a {user_selections['main characters']} in a {user_selections['settings']} setting. The story should focus on the theme of {user_selections['themes']} and include a {user_selections['plot devices']} as a key element. Make the story engaging and age-appropriate, using vocabulary and complexity suitable for a {user_selections['age']}-year-old."
    if show_api_info:
        st.write(f"Prompt: {prompt}")
        st.write(f"Model: gpt-3.5-turbo")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI language model that creates children's stories."},
                {"role": "user", "content": prompt}
            ]
        )
    except openai.error.AuthenticationError as e:
        st.error("An authentication error occurred. Please check your API key.")
        return ""
    return response.choices[0].message['content'].strip()


def display_story_output_screen(generated_story):
    st.header("Your story:")
    st.write(generated_story)


def split_story_into_paragraphs(story):
    paragraphs = story.split("\n\n")
    return paragraphs


def summarize_paragraphs(paragraphs, show_api_info):
    summaries = []
    for paragraph in paragraphs:
        summary = generate_summary(paragraph, show_api_info)
        summaries.append(summary)
    return summaries


def generate_summary(paragraph, show_api_info):
    prompt = f"Summarize the following paragraph in a brief image description:\n\n{paragraph}"
    if show_api_info:
        st.write(f"Prompt: {prompt}")
        st.write(f"Model: gpt-3.5-turbo")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an AI language model that summarizes text."},
                {"role": "user", "content": prompt}
            ]
        )
    except openai.error.AuthenticationError as e:
        st.error("An authentication error occurred. Please check your API key.")
        return ""
    summary = response.choices[0].message['content'].strip()
    return summary


def generate_images_from_summaries(summaries, style, show_api_info):
    image_urls = []
    for summary in summaries:
        image_url = generate_image_from_dalle(
            summary, style, with_spinner=True, show_api_info=show_api_info)
        image_urls.append(image_url)
    return image_urls


def generate_image_from_dalle(summary, style, with_spinner=False, show_api_info=False):
    if show_api_info:
        st.write(f"Prompt: {summary} In the style of {style} art.")
        st.write(f"Model: DALL-E")

    try:
        if with_spinner:
            with st.spinner(f"Generating image for: {summary} In the style of {style} art."):
                response = openai.Image.create(
                    prompt=f"{summary} In the style of {style} art.",
                    n=1,
                    size="512x512",
                )
        else:
            response = openai.Image.create(
                prompt=f"{style} {summary}",
                n=1,
                size="512x512",
            )
    except openai.error.AuthenticationError as e:
        st.error("An authentication error occurred. Please check your API key.")
        return ""
    except openai.error.APIError as e:
        st.error(f"An API error occurred: {e}")
        return ""

    image_url = response.data[0].get('url')
    return image_url


def display_images(paragraphs, image_urls):
    st.header("Your story with images:")
    for paragraph, image_url in zip(paragraphs, image_urls):
        st.subheader(paragraph)
        st.image(image_url)


if __name__ == "__main__":
    main()
