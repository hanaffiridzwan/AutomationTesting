*** Settings ***
Library           SeleniumLibrary
#Resource         ../Testcase/tescase_keyword.robot
Library          ../Testcase/testcase_keywords.py

*** Test Cases ***
Test case 1- Compare two data in the ebay and Amazon
    When user open the Amazon and search iPhone 11
    Then user save the record for Amazon
    When user open the eBay and search iPhone 11
    Then user save the record for eBay
    And combine the data
