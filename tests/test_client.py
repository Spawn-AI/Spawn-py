from dotenv import load_dotenv

from selas import SelasClient

load_dotenv()
import os

TEST_APP_ID = os.environ.get("TEST_APP_ID")
TEST_APP_KEY = os.environ.get("TEST_APP_KEY")
TEST_APP_SECRET = os.environ.get("TEST_APP_SECRET")

selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

job = selas.runStableDiffusion("Selas",patches = [{
    "name": 'Skippy Jack/f-boopboop',
    "alpha_text_encoder": 0.5,
    "alpha_unet": 0.5,
    "steps": 1000,
    }])

selas.subscribeToJob(job.data['job_id'],print)

# test the creation of a SelasClient object
def test_SelasClient():
    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    assert selas is not None
    message = selas.echo("hello world")
    assert message.data == "hello world"

user_name = "Bertrand"
def test_userManagingFunctions():
    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)
    assert selas is not None

    user = selas.createAppUser(user_name)
    assert user.data is not None

    token = selas.createToken(user_name)
    assert token is not None

    token_value = selas.getAppUserToken(user_name)
    assert token_value.data is not None
    assert token.data == token_value.data

    deleted = selas.deleteTokenOfAppUser(user_name)
    assert deleted.data is not None

    credits = selas.getAppUserCredits(user_name)
    assert credits.data == 0

    credits = selas.setCredit(user_name, 100)
    assert credits.data == 100

    credits = selas.getAppUserCredits(user_name)
    assert credits.data == 100

    history = selas.getAppUserJobHistory("Skippy Jack", 10, 0)
    assert history.data is not None
    assert len(history.data) != 0

def test_isUser():
    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    is_user = selas.isUser("Skippy Jack")
    assert is_user.data == True

    is_user = selas.isUser("Skippy Jack2")
    assert is_user.data == False


def test_getServicesAndAddOnsList():
    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    assert selas is not None
    services = selas.getServiceList()
    assert services.data is not None
    assert len(services.data) > 0
    addons = selas.getAddOnList()
    assert addons.data is not None
    assert len(addons.data) > 0

def test_addManagingFunctions():
    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    renamed = selas.renameAddOn('Skippy Jack/f-compote2','f-compete2')
    assert renamed.data == True

    shared = selas.shareAddOn('Skippy Jack/f-compete2','Bertrand')
    assert shared.data == True

    deleted = selas.deleteAddOn('Skippy Jack/f-compete2')
    assert deleted.data == True

def test_publishAddOn():
    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    published = selas.publishAddOn('f-crampoute8')
    assert published.data == True

def test_unpublishAddOn():
    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    unpublished = selas.unpublishAddOn('f-crampoute8')
    assert unpublished.data == True

def test_addOnPostingFunctions():
    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    cost = selas.costPatchTrainer(None,"archilul")
    assert cost.data > 0

    train_id = selas.runPatchTrainer(
        [
            {
                "url": "https://img.sanctuary.fr/fiche/origin/78.jpg",
                "label": "fcompo style, a group of people standing next to each other, by Otomo Katsuhiro, french comic style, zenescope, complex emotion, cover corp"
            }
      ]
      ,"pypatch")
    assert train_id.data is not None

def test_stableDiffusionPostingFunctions():
    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    cost = selas.costStableDiffusion("Selas")
    assert cost.data > 0

    job = selas.runStableDiffusion("Selas",patches = [{
        "name": 'Skippy Jack/f-boopboop',
        "alpha_text_encoder": 0.5,
        "alpha_unet": 0.5,
        "steps": 1000,
      }])
    assert job.data is not None

def test_getResults():
    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    results = selas.getResults("c841db43-6b2c-4f94-aa8f-8b31e48517a6")
    assert results.data is not None

def test_subscribe():
    selas = SelasClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    job = selas.runStableDiffusion("Selas",patches = [{
        "name": 'Skippy Jack/f-boopboop',
        "alpha_text_encoder": 0.5,
        "alpha_unet": 0.5,
        "steps": 1000,
      }])
    
    print(job.data["job_id"])

    sub = selas.subscribeToJob(job.data['job_id'],print)
    assert sub.data is not None

