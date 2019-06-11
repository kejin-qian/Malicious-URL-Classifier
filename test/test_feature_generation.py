import os
import sys
sys.path.append('../')

import src.data_prep as dp

#urls for testing
url1 = 'www.aa@b@bb//Ccde.ff-gg.hh.ii&i--j.com/asd/aas/ddd/@//dd.com'
url2 = 'www.google.com'
url3 = '198.12.13.102'
url4 = 'http://www.donaldmadtrump.com'

def test_countdots():
    """ test the helper function which counts the number of dots"""
    assert dp.countdots(url1) == 6
    assert dp.countdots(url2) == 2
    
def test_containsip():
    """ test the helper function which checks if url contains IP address"""
    assert dp.containsip(url1) == 0
    assert dp.containsip(url3) == 1
    
def test_CountSoftHyphen():
    """ test the helper function which counts the number of soft hyphen"""
    assert dp.CountSoftHyphen(url1) == 3
    assert dp.CountSoftHyphen(url2) == 0
    
def test_CountAt():
    """ test the helper function which counts the number of @"""
    assert dp.CountAt(url1) == 3
    assert dp.CountAt(url2) == 0
    
def test_CountDSlash():
    """ test the helper function which counts the number of double slash //"""
    assert dp.CountDSlash(url1) == 2
    assert dp.CountDSlash(url2) == 0
    
def test_countSubDomain():
    """ test the helper function which counts the number of subdomain"""
    assert dp.countSubDomain(url1) == 7
    assert dp.countSubDomain(url2) == 3
    
def test_countQueries():
    """ test the helper function which counts the number of &"""
    assert dp.countQueries(url1) == 2
    assert dp.countQueries(url2) == 1
    
def test_get_ext():
    """ test the helper function which gets the url extension"""
    assert dp.get_ext(url1) == '.com'
    assert dp.get_ext(url2) == '.com'
    
def test_length():
    """ test the helper function which gets the url extension"""
    assert dp.length(url1) == 60
    assert dp.length(url2) == 14
    
def test_url_format():
    """ test the helper function which gets the url extension"""
    assert dp.url_format(url2) == 'http://www.google.com'
    assert dp.url_format(url4) == url4



