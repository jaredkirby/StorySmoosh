# StorySmoosh  

StorySmoosh is a creative and interactive web application that generates unique and engaging stories for children based on user-selected story elements. Using the OpenAI API and Streamlit, StorySmoosh creates a personalized story experience complete with generated images.  

## Features  

- Choose your story elements: genre, main character, setting, theme, and plot device 
- Customize the story's age-appropriateness by selecting a target age range 
- Option to generate images that accompany the story, with a variety of visual styles to choose from 
- View the API prompts and models used during story generation (optional)  

## Usage

To use StorySmoosh, you will need an OpenAI API key. If you don't have one, sign up for OpenAI [here](https://beta.openai.com/signup/).

1.  Clone the repository and navigate to the directory.

```
git clone https://github.com/example/StorySmoosh.git cd StorySmoosh
```

2.  Install the dependencies.

```
pip install -r requirements.txt
```

3.  Run the application.

```
streamlit run app.py
```

4.  Enter your OpenAI API key in the text input field in the sidebar.
5.  Choose your preferred story elements and click the "Generate Story" button to generate a story.
6.  If you have selected to generate images, the application will use DALL-E to generate images for each paragraph of the story. This may take a while to complete. Once the images are generated, they will be displayed along with the story.
