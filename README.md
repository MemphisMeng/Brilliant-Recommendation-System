# Brilliant Recommendation System 
Brilliant Recommendations System is [Made With ML] Data Science Incubator Summer 2020 project. This is a recommendation system simulating some existing prestigious streaming platfrom (e.g. Netflix, YouTube) and utilizing content-based filtering which is configured with TF-IDF.

### Installation 
First, create virtual environment using  [Anaconda] so that the installation does not conflict with system wide installs.
```sh
$ conda create -n <envname> python=3.7
```

Clone the project and install the dependencies
```sh
$ git clone https://github.com/MemphisMeng/Brilliant-Recommendation-System.git
$ cd Brilliant-Recommendation-System
```

Activate environment and Install the dependencies.
```sh
$ conda activate <envname>
$ pip install -r requirements.txt
```

### Usage 
```sh 
$ streamlit run app.py

```

### Deployment
Please feel free check it out [here](https://recommendation-sys.herokuapp.com)!

### [Article] (https://towardsdatascience.com/movie-recommendation-system-based-on-movielens-ef0df580cd0e)

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
[Anaconda]: <https://www.anaconda.com/distribution/>
[Made With ML]: <https://madewithml.com/incubator/>
[here]: <https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line#creating-a-token>
