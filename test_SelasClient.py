from src.SelasClient import SelasClient

from dotenv import load_dotenv
load_dotenv()
import os

TEST_APP_ID = os.environ.get("TEST_APP_ID")
TEST_APP_KEY = os.environ.get("TEST_APP_KEY")
TEST_APP_SECRET = os.environ.get("TEST_APP_SECRET")

#test the creation of a SelasClient object
def test_SelasClient():
    selas = SelasClient(TEST_APP_ID,
                        TEST_APP_KEY,
                        TEST_APP_SECRET)

    assert selas is not None
    message = selas.echo("hello world")
    assert message.data == "hello world"

def test_getAppSuperUser():
    selas = SelasClient(TEST_APP_ID,
                        TEST_APP_KEY,
                        TEST_APP_SECRET)

    assert selas is not None
    user = selas.getAppSuperUser()
    assert user.data is not None    
    
def test_createAppUser():
    selas = SelasClient(TEST_APP_ID,
                        TEST_APP_KEY,
                        TEST_APP_SECRET)

    assert selas is not None
    user = selas.createAppUser()
    assert user.data is not None

def test_tokenFunctions():
    selas = SelasClient(TEST_APP_ID,
                        TEST_APP_KEY,
                        TEST_APP_SECRET)

    assert selas is not None
    user = selas.createAppUser()
    assert user.data is not None
    token = selas.createToken(user.data)
    assert token.data is not None
    token_value = selas.getAppUserToken(user.data)
    assert token_value.data is not None
    assert token == token_value

def test_creditFunctions():
    selas = SelasClient(TEST_APP_ID,
                        TEST_APP_KEY,
                        TEST_APP_SECRET)

    assert selas is not None
    user = selas.createAppUser()
    assert user.data is not None
    credits = selas.addCredit(user.data, 100)
    assert credits.data is not None
    assert credits.data == 100
    credits = selas.getAppUserCredits(user.data)
    assert credits.data is not None
    assert credits.data == 100

def test_getServiceList():
    selas = SelasClient(TEST_APP_ID,
                        TEST_APP_KEY,
                        TEST_APP_SECRET)

    assert selas is not None
    services = selas.getServiceList()
    assert services.data is not None
    assert len(services.data) > 0