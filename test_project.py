import pytest
from project import evaluate_password, register_user, user_verification


class TestClass:
    # Test evealuate_password
    def test_evaluate_password(self):
        # Evaluate password with 14 characters
        assert evaluate_password("#R>gxFMi#&R-1v") == True
        # Evaluate password with 64 characters
        assert evaluate_password('{~S7U".Oh/.b!U}T0[U]J"T6?&o{p#$gFRzjIeNw5CJO^)ue9J4.hS>I^-Oj;rR+') == True
        # Evaluate password without uppercase
        assert evaluate_password("sohelp1}%me.god") == False
        # Evaluate password without lowercase
        assert evaluate_password("GOOD#*BETTER~BEST9") == False
        # Evaluate password without numbers
        assert evaluate_password("IloveThisNinety_nine%") == False
        # Evaluate password without special character
        assert evaluate_password("My1stJourney100") == False
        # Evaluate password with email
        assert evaluate_password("9009ineworlwide@gmail.com") == False
        # Evaluate password with less than 14 characters
        assert evaluate_password("iL0v{You99") == False
        # Evaluate password with more than 64 characters
        assert evaluate_password('Wt54*7[p^.tAFv{YOlTAl8b\a\t[skUC~Z"]k`Zu/>Z>2CT|z(Zp9Si,UvcL$QArL,789') == False

    # Test register_user
    def test_register_user(self):
        assert register_user("jamal", "#R>gxFMi#&R-1v")  == True
        assert register_user("jonna", "Wt54*7[p^.tAFv{YOlTAl8b") == True
        assert register_user("okon", "]e1suO{2G|/fU!") == True

    # Test user_verification
    def test_user_verification(self):
        assert user_verification("jamal", "#R>gxFMi#&R-1v") == True
        assert user_verification("jonna", "Wt54*7[p^.tAFv{YOlTAl8b") == True
        assert user_verification("okon", "#R>gxFMi#&R-1v") == False
        assert user_verification("jonna", "#R>gxFMi#&R-1v") == False
        assert user_verification("jay", "Zu/>Z>2CT|z(Zp9Si,UvcL$QArL,") == 0
        assert user_verification("ken", "%yu2CT|z(Zp9Si,UvcL$") == 0


