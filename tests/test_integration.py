import pytest
import dbcreator as dbc
from passwordAuth import store
import login

def test_validlogin(client):
    test = login.userlogin("sarahlee", "Word123$%")
    assert test == "user"

def test_invalidlogin(client):
    test = login.userlogin("leesarah", "Word123$%")
    assert test == "Invalid username"

def test_invalidpassword(client):
    test = login.userlogin("sarahlee", "abcd")
    assert test == "wrong password"