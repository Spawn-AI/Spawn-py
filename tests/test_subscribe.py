import os
from selas import SelasClient
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":

    TEST_APP_ID = os.environ.get("TEST_APP_ID")
    TEST_APP_KEY = os.environ.get("TEST_APP_KEY")
    TEST_APP_SECRET = os.environ.get("TEST_APP_SECRET")

    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    job = selas.runStableDiffusion("Selas", patches=[{
        "name": 'Skippy Jack/f-boopboop',
        "alpha_text_encoder": 0.5,
        "alpha_unet": 0.5,
        "steps": 1000,
    }])

    # job = selas.runPatchTrainer(
    #     [
    #         {
    #             "url": "https://img.sanctuary.fr/fiche/origin/78.jpg",
    #             "label": "fcompo style, a group of people standing next to each other, by Otomo Katsuhiro, french comic style, zenescope, complex emotion, cover corp"
    #         }
    #   ]
    #   ,"pypatch")
