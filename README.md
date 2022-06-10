# tfedUD_shoebox_app

An app intended to be used for early phase parametric | computational studies of shoebox models

## Quickstart

Install dependencies:

```
> pip install -r requirements.txt
```

Start Streamlit

```
> streamlit run app.py

  You can now view your Streamlit app in your browser.

  Network URL: http://172.17.0.2:8501
  External URL: http://152.37.119.122:8501

```

Make changes to your app in the `app.py` file inside the "app" folder.

## Run inside Docker image locally (Optional)

You can run the app locally inside Docker to ensure the app will work fine after the deployment.

You need to install Docker on your machine in order to be able to run this command

```
> pollination-apps run app Trevor Fedyna --name "tfedUD_shoebox_app"
```

## Deploy to Pollination

```
> pollination-apps deploy app --name "tfedUD_shoebox_app" --public --api-token "Your api token from Pollination"
```



## Configure Github Actions

In order to configure github actions to deploy your app you will need to:

1. Configure a secret called `POLLINATION_TOKEN` with your Pollination API key as the value
2. Create [a new release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) of your app on Github with a new tag

Github actions will then package and deploy your code to an app called [tfedUD_shoebox_app](https://app.pollination.cloud/Trevor Fedyna/applications/tfedud_shoebox_app)


