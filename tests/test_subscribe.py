import os
from spawn import SpawnClient
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":

    TEST_APP_ID = os.environ.get("TEST_APP_ID")
    TEST_APP_KEY = os.environ.get("TEST_APP_KEY")
    TEST_APP_SECRET = os.environ.get("TEST_APP_SECRET")

    spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    # job = spawn.runStableDiffusion("Spawn", patches=[{
    #     "name": 'Skippy Jack/f-boopboop',
    #     "alpha_text_encoder": 0.5,
    #     "alpha_unet": 0.5,
    #     "steps": 1000,
    # }])

    job = spawn.runPatchTrainer(
        [
            {
                "url": "https://img.sanctuary.fr/fiche/origin/78.jpg",
                "label": "fcompo style, a group of people standing next to each other, by Otomo Katsuhiro, french comic style, zenescope, complex emotion, cover corp"
            }
      ]
      ,"pypatch")
