from dotenv import load_dotenv

from spawn import SpawnClient

load_dotenv()
import os

TEST_APP_ID = os.environ.get("TEST_APP_ID")
TEST_APP_KEY = os.environ.get("TEST_APP_KEY")
TEST_APP_SECRET = os.environ.get("TEST_APP_SECRET")

spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET, external_id="Skippy Jack")

job = spawn.runStableDiffusion("Spawn")

spawn.subscribeToJob(job.data['job_id'],print)

# test the creation of a SpawnClient object
def test_SpawnClient():
    spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    assert spawn is not None
    message = spawn.echo("hello world")
    assert message.data == "hello world"

user_name = "Bertrand"
def test_userManagingFunctions():
    spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)
    assert spawn is not None

    user = spawn.createAppUser(user_name)
    assert user.data is not None

    token = spawn.createToken(user_name)
    assert token is not None

    token_value = spawn.getAppUserToken(user_name)
    assert token_value.data is not None
    assert token.data == token_value.data

    deleted = spawn.deleteTokenOfAppUser(user_name)
    assert deleted.data is not None

    credits = spawn.getAppUserCredits(user_name)
    assert credits.data == 0

    credits = spawn.setCredit(user_name, 100)
    assert credits.data == 100

    credits = spawn.getAppUserCredits(user_name)
    assert credits.data == 100

    history = spawn.getAppUserJobHistory("Skippy Jack", 10, 0)
    assert history.data is not None
    assert len(history.data) != 0

def test_isUser():
    spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    is_user = spawn.isUser("Skippy Jack")
    assert is_user.data == True

    is_user = spawn.isUser("Skippy Jack2")
    assert is_user.data == False


def test_getServicesAndAddOnsList():
    spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    assert spawn is not None
    services = spawn.getServiceList()
    assert services.data is not None
    assert len(services.data) > 0
    addons = spawn.getAddOnList()
    assert addons.data is not None
    assert len(addons.data) > 0

def test_addManagingFunctions():
    spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    renamed = spawn.renameAddOn('Skippy Jack/f-compote2','f-compete2')
    assert renamed.data == True

    shared = spawn.shareAddOn('Skippy Jack/f-compete2','Bertrand')
    assert shared.data == True

    deleted = spawn.deleteAddOn('Skippy Jack/f-compete2')
    assert deleted.data == True

def test_publishAddOn():
    spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    published = spawn.publishAddOn('f-crampoute8')
    assert published.data == True

def test_unpublishAddOn():
    spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    unpublished = spawn.unpublishAddOn('f-crampoute8')
    assert unpublished.data == True

def test_addOnPostingFunctions():
    spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    cost = spawn.costPatchTrainer(None,"archilul")
    assert cost.data > 0

    train_id = spawn.runPatchTrainer(
        [
            {
                "url": "https://img.sanctuary.fr/fiche/origin/78.jpg",
                "label": "fcompo style, a group of people standing next to each other, by Otomo Katsuhiro, french comic style, zenescope, complex emotion, cover corp"
            }
      ]
      ,"pypatch")
    assert train_id.data is not None

def test_stableDiffusionPostingFunctions():
    spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    cost = spawn.costStableDiffusion("Spawn")
    assert cost.data > 0

    job = spawn.runStableDiffusion("Spawn",patches = [{
        "name": 'Skippy Jack/f-boopboop',
        "alpha_text_encoder": 0.5,
        "alpha_unet": 0.5,
        "steps": 1000,
      }])
    assert job.data is not None

def test_getResults():
    spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    results = spawn.getResults("c841db43-6b2c-4f94-aa8f-8b31e48517a6")
    assert results.data is not None

def test_subscribe():
    spawn = SpawnClient(TEST_APP_ID, TEST_APP_KEY, TEST_APP_SECRET)

    job = spawn.runStableDiffusion("Spawn",patches = [{
        "name": 'Skippy Jack/f-boopboop',
        "alpha_text_encoder": 0.5,
        "alpha_unet": 0.5,
        "steps": 1000,
      }])
    
    print(job.data["job_id"])

    sub = spawn.subscribeToJob(job.data['job_id'],print)
    assert sub.data is not None

