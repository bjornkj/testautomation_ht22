from http import HTTPStatus

import requests
import pytest
from data_model import User

GOREST_USERS = "https://gorest.co.in/public/v2/users"
GOREST_POSTS = "https://gorest.co.in/public/v2/posts"

TESTDATA = {"name": "Min Testuser",
            "email": "dennesadrss@outlook.se",
            "gender": "male",
            "status": "active"}

LIST_OF_USERS = [{"name": "Testperson Testsson",
                  "email": "endf@enmladres4s.se",
                  "gender": "male",
                  "status": "active"},
                 {"name": "En anna person",
                  "email": "endf@enmladres4.se",
                  "gender": "female",
                  "status": "active"},
                 {"name": "Ny Person",
                  "email": "dennes@adress.se",
                  "gender": "female",
                  "status": "active"},
                 {"name": "Min Testuser",
                  "email": "dennesadrss@outlook.se",
                  "gender": "male",
                  "status": "active"}
                 ]

LIST_OF_USERS_AND_STATUS_CODE = [
    ({"name": "Testperson Testsson",
      "email": "endf@enmladres4s.se",
      "gender": "male",
      "status": "active"}, HTTPStatus.CREATED),
    ({"name": "En anna person",
      "email": "endf@enmladres4.se",
      "gender": "female",
      "status": "active"}, HTTPStatus.CREATED),
    ({"name": "Ny Person",
      "email": "dennes@adress.se",
      "gender": "female",
      "status": "active"}, HTTPStatus.CREATED),
    ({"name": "Min Testuser",
      "email": "dennesadrss@outlook.se",
      "gender": "male",
      "status": "active"}, HTTPStatus.CREATED),
    ({"name": "Min Testuser",
      "gender": "male",
      "status": "active"}, HTTPStatus.UNPROCESSABLE_ENTITY),
    ({"name": "Min Testuser",
      "email": "dennesadrssoutlook.se",
      "gender": "male",
      "status": "active"}, HTTPStatus.CREATED)
]

with open("token") as f:
    TOKEN = f.read().strip()

HEADER = {"authorization": f"Bearer {TOKEN}"}


@pytest.fixture
def api_token() -> str:
    with open('token') as f:
        return f.read().strip()


@pytest.fixture
def header(api_token):
    return {'authorization': f"Bearer {api_token}"}


@pytest.fixture
def user_data():
    return {'name': "En Testperson",
            "email": "some_mail@mail.fr",
            "gender": "male",
            "status": "active"}


# H??r anv??nder vi en lista av anv??ndardata som argument till fixturen.
# Testfunktioner som anv??nder den h??r fixturen kommer k??ras en g??ng per element i listan
# Detta l??ter oss skriva en testfunktion som sedan k??rs med en stor m??ngd olika testdata.
# Exempelvis kan vi testa en stor m??ngd kombinationer av namn med olika specialtecken
@pytest.fixture(params=LIST_OF_USERS)
def user_data2(request):
    return request.param


# Ett test kan delas in i 3-4 olika delar.
# 1. Arrange, arrangera, f??rbereda
# 2. Act, agera. Interagera med SUT, genomf??r n??gon handling
# 3. Assert, kontrollera att utfallet blev det f??rv??ntade
# 4. Cleanup, st??da, rensa, ta bort s??dan som kan st??ra ytterligare tester


# Go rest har f??ljande resurser
# 1. Users, kr??ver unik epost
# 2. Posts, kr??ver en existerande anv??ndare
# 3. Comments
# 4. Todos

# Vi skall testa CRUD, skapa, l??sa, ??ndra, ta bort var och en av resurserna.
# Vi skall testa att h??mta b??de en och flera av varje resurs.
# Vi skall testa att systemet hanterar exempelvis svenska tecken. Fler uppslag?
# Vi skall testa responskoder och svarstider.
# Kontrollera responskoder n??r vi skall f?? fel.

# F??r att arbeta mot gorest.co.in beh??ver vi ett token, detta ber??ttar att vi har r??tt att skapa
# och ??ndra p?? resurser. Vi har lagt den i en separat fil som inte ??r under versionshantering
# f??r att undvika att vi oavsiktligt l??cker k??nslig information.
# Token skickas med i headern vid anrop mot gorest.co.in


# Users
#   Skapa

# Vad beh??ver vi f??r att skapa en anv??ndare?
# name, email, gender, status
# header med token
#
# 1. Skapa testdata, en dictionary med name, email, gender, status
# 2. Skapa en header med bearer token.
# 3. G??r http POST mot resursen(users)
# 4. Tolka resultatet som json
# 5. Kontrollera att det vi fick tillbaks var samma sak som det vi skickade in
# 6. Kontrollera statuskod, HTTP CREATED
# 7. Ta bort anv??ndaren igen s?? att testet kan k??ras igen.
#
# TODO vilka andra statusar finns, hur kan vi ??ndra

def test_create_user():
    response = requests.post(GOREST_USERS, data=TESTDATA, headers=HEADER)
    response_json = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert response_json['name'] == TESTDATA['name']
    assert response_json['email'] == TESTDATA['email']
    assert response_json['gender'] == TESTDATA['gender']
    assert response_json['status'] == TESTDATA['status']

    # F??r att ta bort en anv??ndare anv??nder vi en DELETE request mot den specifika anv??ndaren
    # https://gorest.co.in/public/v2/users/123  <- den specifika anv??ndaren 123
    delete_response = requests.delete(GOREST_USERS + f"/{response_json['id']}", headers=HEADER)


# Uppgift 1.
# Skriv test som skapar en ny anv??ndare och d??refter h??mtar anv??ndaren med  hj??lp av en get-request
# kontrollera att anv??ndaren har r??tt data.

# Skriv test som skapar en ny anv??ndare och d??refter uppdaterar namnet med en patch-request
# kontrollera att anv??ndaren d??refter har uppdaterats med hj??lp av en get-request

@pytest.fixture
def new_user_request():
    user_response = requests.post(GOREST_USERS, data=TESTDATA, headers=HEADER)
    yield user_response
    requests.delete(GOREST_USERS + f"/{user_response.json()['id']}", headers=HEADER)


@pytest.fixture
def new_user(new_user_request):
    return new_user_request.json()


@pytest.fixture
def new_user_and_response(new_user_request) -> tuple[dict, requests.Response]:
    return new_user_request.json(), new_user_request


def test_foo(new_user_and_response):
    user, response = new_user_and_response
    assert "name" in user
    assert response.status_code == HTTPStatus.CREATED


# Uppgift 2.
# Skriv om n??gra av dina tester med fixturen new_user ist??llet f??r att sj??lv skapa anv??ndare
#
# F??rs??k skapa en ny fixtur som ger en ny post


@pytest.fixture
def new_post(new_user):
    post_data = {"user_id": new_user['id'], "title": "Postens titel", "body": "Postens br??dtext"}
    new_post_response = requests.post(GOREST_POSTS, data=post_data, headers=HEADER)
    post = new_post_response.json()
    yield post
    requests.delete(GOREST_POSTS + f"/{post['id']}", headers=HEADER)


# Uppgift 3
# Kan du skapa en fixtur som ist??llet ger tillbaks responsobjektet s?? att vi kan kontrollera svarstider och returkoder?

def test_create_post_with_fixture(new_post):
    assert "title" in new_post


def test_check_post_user(new_user, new_post):
    assert new_user['id'] == new_post['user_id']


# Tester av statuskoder och svarstider
def test_new_user_response_time(new_user_request):
    assert new_user_request.elapsed.microseconds < 700000


def test_new_user_status_code(new_user_request):
    assert new_user_request.status_code == HTTPStatus.CREATED


# Hur n??r vi beh??ver tv?? eller fler anv??ndare?
# Vi vill fortfarande att det skall st??das upp automatiskt efter att testet k??rts
# Vi kan inte anv??nda de existerande fixturerna, de ger oss bara en anv??ndare
# Vad vi beh??ver ??r en fixtur som kan skapa anv??ndare p?? kommando och som sedan st??dar upp n??r vi ??r klara.
# Fixturen beh??ver h??lla koll p?? vilka anv??ndare som skapats f??r att kunna ta bort dom efter??t.
@pytest.fixture
def make_user():
    created_users = []

    def _make_user(name: str, email: str, gender: str, status: str) -> tuple[requests.Response, User]:
        response = requests.post(GOREST_USERS, data={"name": name, "email": email, "gender": gender, "status": status},
                                 headers=HEADER)
        created_user = User(**response.json())
        created_users.append(created_user)
        return response, created_user

    yield _make_user
    for user in created_users:
        requests.delete(GOREST_USERS + f"/{user.id}", headers=HEADER)


@pytest.fixture
def make_user_request():
    created_users = []

    def _make_request(user_dict) -> requests.Response:
        response = requests.post(GOREST_USERS, data=user_dict,
                                 headers=HEADER)
        if response.status_code == HTTPStatus.CREATED:
            created_users.append(response.json())
        return response

    yield _make_request

    for user in created_users:
        requests.delete(GOREST_USERS + f"/{user['id']}", headers=HEADER)


def test_with_two_users(make_user):
    # H??r ser vi att vi kan skapa tv?? nya anv??ndare som sedan automatiskt tas bort efter att testet k??rts
    user1 = make_user("Anv??ndare 1", "laskjdf@sdlkfaj.com", "male", "active")
    user2 = make_user("Anv??ndare 2", "laskjdf@sdlasdfaskfaj.com", "female", "active")
    print(user1)
    print(user2)


def test_create_user_with_param(user_data2, make_user):
    _, user = make_user(**user_data2)
    assert user.name == user_data2['name']
    assert user.email == user_data2['email']
    assert user.gender == user_data2['gender']
    assert user.status == user_data2['status']



# Om det ??r relativt enkel testdata kan vi ist??llet parametrisera sj??vlva testfunktionen enligt f??ljande
# H??r talar vi om att testfunktionen skall anropas en g??ng f??r varje element i LIST_OF_USERS
# Vid varje anrop kommer elementet ur LIST_OF_USERS ges till testfunktionen under namnet user_dict
@pytest.mark.parametrize("user_dict", LIST_OF_USERS)
def test_create_user_with_mark_param(user_dict, make_user):
    _, user = make_user(**user_dict)
    assert user.name == user_dict['name']
    assert user.email == user_dict['email']
    assert user.gender == user_dict['gender']
    assert user.status == user_dict['status']


# Vi kan genom att para ihop testdata med det f??rv??ntade utfallet anv??nda en testfunktion
# f??r att testa en stor m??ngd olika variationer av testdata
# I det h??r fallet har vi i listan LIST_OF_USERS_AND_STATUS_CODE
# par av data f??r att skapa nya anv??ndare i systemet tillsammans med den f??rv??ntade statuskoden.
# Exempelvis 201 CREATED om det ??r data som skall kunna reseultera i en ny anv??ndare
# eller 422 UNPROCESSABLE_ENTITY om det ??r anv??ndardata som saknar ett viktigt f??lt som epost
# Textstr??ngen "user_dict, status_code" talar om vad vi vill kalla de olika delarna av paren testdata, utfall ur listan
# Vi ser sedan samma namn, user_dict och status_code i argumentlistan till testfunktionen.
# pytest kommer att k??ra testfunktionen en g??ng f??r varje par av v??rden i LIST_OF_USERS_AND_STATUS_CODE
@pytest.mark.parametrize("user_dict, status_code", LIST_OF_USERS_AND_STATUS_CODE)
def test_create_user_status_code(user_dict, status_code, make_user_request):
    response = make_user_request(user_dict)
    assert response.status_code == status_code, f"Expected {status_code} got {response.status_code}"


# Gammalt skr??p
def test_create_post():
    # 1. Skapa en ny anv??ndare
    # 2. Skapa en ny post med id fr??n anv??ndaren fr??n steg 1.
    #   1. Skapa post-data, user_id, title, body
    # 3. Asserts
    # 4. Ta bort posten
    # 5. Ta bort anv??ndaren fr??n steg 1.
    new_user = requests.post(GOREST_USERS, data=TESTDATA, headers=HEADER).json()
    post_data = {"user_id": new_user['id'], "title": "Postens titel", "body": "Postens br??dtext"}

    new_post_response = requests.post(GOREST_POSTS, data=post_data, headers=HEADER)
    new_post = new_post_response.json()

    assert new_post['user_id'] == new_user['id']

    requests.delete(GOREST_POSTS + f"/{new_post['id']}", headers=HEADER)
    requests.delete(GOREST_USERS + f"/{new_user['id']}", headers=HEADER)


def test_create_post2(new_user):
    post_data = {"user_id": new_user['id'], "title": "Postens titel", "body": "Postens br??dtext"}
    new_post_response = requests.post(GOREST_POSTS, data=post_data, headers=HEADER)
    new_post = new_post_response.json()

    assert new_post['user_id'] == new_user['id']

    requests.delete(GOREST_POSTS + f"/{new_post['id']}", headers=HEADER)
