# Spawn Python

A Python implementation of the Spawn protocol.

## Overview

The Spawn Python module is a python implementation of the Spawn protocol. It allows you to run jobs on the Spawn platform from your python code. You can find the source code for the Spawn Python module on [GitHub](https://github.com/SpawnAI/spawn-py). The Spawn Python module is licensed under the [MIT License](https://opensource.org/licenses/MIT). The Spawn Python module is currently in beta, so please report any bugs or issues you encounter.

## Installation

Install the library using pip:

```bash
pip install spawn
```

## Usage

To use the Spawn Python module, you need to require it in your JavaScript code and create a Spawn client object. To get started, you need to create a Spawn account and create an app. You can find more information about creating a Spawn account and creating an app in the [Spawn documentation](https://spawn.ai/docs/). Once you have created an app, you can get the app_id, key, and secret from the app settings page. You can then use these values to create a Spawn client object:


```py3
from spawn import SpawnClient

spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)
```

### Administration of the users

#### Authorizing or denying the access to the services

Using the Spawn-py client, you can manage how your customers can access our services. 

To allow a user to access our services, you first need to create an app user. During the creation, you need to provide an identifier that will be necessary to access to the usage data. It will be refered in this client as an external id. This external id can be an email, a username, a phone number, a crypto wallet address, etc. 

```py
user = spawn.createAppUser(user_name)
```

Once a user is created, you can allow or deny the usage of paid services for this user. This is done by handling the tokens of the user. You can create a token for a user by providing the external id of the user.


```py
token = spawn.createToken(user_name)
```

There is no need to store the token in your database. You can retrieve it at any time by providing the external id of the user.

```py
token_value = spawn.getAppUserToken(user_name)
```

There is no need to give a token for every utilisation. Once a token is created, it remain active until it is deleted. If you need to deny the access to a user, you can delete all the tokens of the user.

```py
is_deleted = spawn.deleteTokenOfAppUser(user_name)
```

Moreover, the AI usage of a user is limited by the amount of credit that you give it. You can set the credit of a user by providing the external id of the user and the amount of credit you want to give. This security is mandatory to avoid a user to use all the credit of your app.

```py
credits = spawn.setCredit(user_name, 100);
```

#### Accessing user usage

As the administror of your application, you can access all the informations that we have on your users.

You can get the credit of a user by providing the external id of the user.
```py
credits = spawn.getAppUserCredits(user_name)
```

You can get the history of all the jobs that a user has run on our service.
```py
history = spawn.getAppUserJobHistory(user_name, 10, 0)
```

If you want to get the specific result of a job (be it an image or an add-on), you can user the getResult method. You need to provide the job_id of the job you want to get the result of. It will return a json object with the result of the job.
```py
results = spawn.getResults(job_id)
```

As your user will be able to create add-ons, you will have a complete right to access them. All add-ons create by your customers and by you will be accessible by the getAddOnList method. It will return a json object with all the add-ons of your app.
```py
addons = spawn.getAddOnList()
```

Moreover, you can delete, share or rename any add-on created on your application.
```py
is_renamed = spawn.renameAddOn('User1/landscape add-on', 'forest add-on')

is_shared = spawn.shareAddOn('User1/forest add-on', 'Benoit')

is_deleted = spawn.deleteAddOn('User1/forest add-on');
```


### Usage of IA services

Even if this the Spawn-py client is created to manage applications and its users, it has all the needed methods for running jobs on the Spawn platform. When running jobs on Spawn-py, you are seen as a super-user and do not have to use tokens or credit.

To know how many workers are active on the Spawn platform, you can use the getCountActiveWorker method. It will return the number of workers for each service.
```py
count_workers = client.getCountActiveWorker();
```

#### Running an image generation job

The following example shows how to run a stable diffusion job with minimal parameters.

```py
response = client.runStableDiffusion("a cute cat");
```

To get the cost of a job without running it, you can use the costStableDiffusion method. Its syntax is exactly the same as runStableDiffusion.

```py
cost = client.costStableDiffusion("a cute cat");
```

It is possible to specify additional parameters for the jobs. Those parameters are defined in this list :
```js
/**
  * @param prompt - the description of the image to be generated
  * @param args.negative_prompt - description of the image to be generated, but with negative words like "ugly", "blurry" or "low quality"
  * @param args.width - the width of the generated image
  * @param args.height - the height of the generated image
  * @param args.steps - the number of steps of the StableDiffusion algorithm. The higher the number, the more detailed the image will be. Generally, 30 steps is enough, but you can try more if you want.
  * @param args.batch_size - the number of images to be generated at each step.
  * @param args.guidance_scale - the weight of the guidance image in the loss function. Typical values are between 5. and 15. The higher the number, the more the image will look like the prompt. If you go too high, the image will look like the prompt but will be low quality.
  * @param args.init_image - the url of an initial image to be used by the algorithm. If not provided, random noise will be used. You can start from an existing image and make StableDiffusion refine it. You can specify the skip_steps to choose how much of the image will be refined (0 is like a random initialization, 1. is like a copy of the image).
  * @param args.mask - the url of a mask image. The mask image must be a black and white image where white pixels are the pixels that will be modified by the algorithm. Black pixels will be kept as they are. If not provided, the whole image will be modified.
  * @param args.skip_steps - the number of steps to skip at the beginning of the algorithm. If you provide an init_image, you can choose how much of the image will be refined. 0 is like a random initialization, 1. is like a copy of the image.
  * @param args.seed - the seed of the random number generator. Using twice the same we generate the same image. It can be useful to see the effect of parameters on the image generated. If not provided, a random seed will be used.
  * @param args.image_format - the format of the generated image. It can be "png" or "jpeg".
  * @param args.nsfw_filter - if true, the image will be filtered to remove NSFW content. It can be useful if you want to generate images for a public website.
  * @param args.translate_prompt - if true, the prompt will be translated to English before being used by the algorithm. It can be useful if you want to generate images in a language that is not English.
  */
```

To specify those parameters, you can use the runStableDiffusion method and pass in an object with the parameters you want to change as arguments.

```py
response = client.runStableDiffusion("a cute cat",width: 640, height: 384, image_format: "jpeg");
```

More specific at our plateform, you can alter your jobs by using one or multiple add-ons that are have been trained or shared to your application.
```py
response = client.runStableDiffusion("a cute cat",patches: [
      {
        name: 'Serge/chinese_landscape',
        alpha_text_encoder: 0.5,
        alpha_unet: 0.5,
        steps: 1000,
      },
    ]);
```

The response object will contain the job_id of the job that was created. You can use this job_id to check the status of the job and to retrieve the results of the job. This result can take a few second to be produced.

```js
result = client.getResult(response['job_id']);
```

#### Running a patch creation job

The following example shows how to run a patch creation job with minimal parameters.

```py
spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

cost = spawn.costPatchTrainer(None,"archilul")
assert cost.data > 0

train_id = spawn.runPatchTrainer(
    [
        {
            "url": "https://img.sanctuary.fr/fiche/origin/78.jpg",
            "label": "fcompo style, a group of people standing next to each other, by Otomo Katsuhiro, french comic style, zenescope, complex emotion, cover corp"
        }
        # You can add more images here
]
,"my_patch")
```

To get the cost of a job without posting it, you can use the costPatchTrainer method. Its syntax is the same as the runPatchTrainer method.

```py
cost = await spawn.costPatchTrainer(dataset, "my_patch");
```

To train a patch, you need a list of images and label that will be used to train the patch. They will alter the stable diffusion model to generate images that are similar to the images you provide. The label is used to describe the images you provide. It can be a sentence or a list of words.

## Documentation

For more information about the Spawn Python module, please refer to the [Spawn Python documentation](https://spawn.ai/docs/spawn-py).

