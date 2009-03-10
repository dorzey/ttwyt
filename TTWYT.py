'''
TTWYT.py v.0.1
Author: dorzey@gmail.com

A library that provides a python binding to the Tell Them What You Think API(www.tellthemwhatyouthink.org)

   This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import datetime
import time
import urllib

#API Spec
API = {'ttwyt':{
       'search':[('output',), 
                 ('terms', ' departments', 'startPubRange', 'endPubRange', ' startCloseRange', 'endCloseRange', 'currentOnly', 'sort', 'sortDir')],
       'get':[('output','guid'), ()],
       'getdepts':[('output',), ()],
       }}

OUTPUTS = ['xml', 'php']
SERVICE_URL = 'http://data.tellthemwhatyouthink.org/api/dispatch.php?'

class TTWYT():
    """
    Create an instance of this class with an API key to enable python bindings
    """
    def __init__(self):
        for prefix, methods in API.items():
            setattr(self, prefix, TTWYTAPICategory(self, prefix, methods))
       
    def get(self, **params):
        """
        Calls the ttwyt API
        """
        params_encoded = urllib.urlencode(params)
        print SERVICE_URL+params_encoded
        return urllib.urlopen(SERVICE_URL+params_encoded).read()

class TTWYTAPICategory:
    """
    TTWYTAPICategory is a modified version of RTMAPICategory in pyrtm (http://repo.or.cz/w/pyrtm.git)
    See the `API` structure and `TTWYT.__init__`
    """
   
    def __init__(self, ttwyt, prefix, methods):
        self.ttwyt = ttwyt
        self.prefix = prefix
        self.methods = methods

    def __getattr__(self, attr):
        if attr in self.methods:
            rargs, oargs = self.methods[attr]
            return lambda **params: self.call_method(attr, rargs, oargs, **params)
        else:
            raise AttributeError, 'No such attribute: %s' % attr

    def call_method(self, aname, rargs, oargs, **params):
        """
        Checks for errors before calling the API"
        """
        if params['output'] in OUTPUTS:
            for required in rargs:
                if required not in params:
                    raise TypeError, 'Required parameter (%s) missing' % required

            for param in params:
                if param not in rargs + oargs:
                    raise TypeError, 'Invalid parameter (%s)' % param
                
            if 'startPubRange' in params:
                if not is_valid_date(params['startPubRange']):
                    raise TypeError, 'Invalid date given: (%s)' % params['startPubRange']
            if 'endPubRange' in params:
                if not is_valid_date(params['endPubRange']):
                    raise TypeError, 'Invalid date given: (%s)' % params['endPubRange']
            if 'startCloseRange' in params:
                if not is_valid_date(params['startCloseRange']):
                    raise TypeError, 'Invalid date given: (%s)' % params['startCloseRange']
            if 'endCloseRange' in params:
                if not is_valid_date(params['endCloseRange']):
                    raise TypeError, 'Invalid date given: (%s)' % params['endCloseRange']
                
            return self.ttwyt.get(function=aname, **params)
        else:
            raise TypeError, 'Invalid output given: (%s)' % params['output']

def is_valid_date(date):
    """
    Checks to see if the date is valid. dd/mm/yyyy
    """
    if date == '':
        return True
    else:
        try:
            c = time.strptime(date, "%d/%m/%Y")
            if datetime.datetime(*c[:6]).date() <= datetime.datetime.today().date():
                return True
            else:
                return False
        except (ValueError, TypeError):
            return False

if __name__ == '__main__':
    y = TTWYT()
    print y.ttwyt.get(output='xml',guid='con-1821-proposed-changes-charging-northern-ireland')
