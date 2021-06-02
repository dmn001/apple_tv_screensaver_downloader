import requests
import os
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Scraper(object):
    def __init__(self):
        self.user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        self.output_dir = './output/'
        self.ensure_dir(self.output_dir)
        self.return_data = True
        self.response_content = ''
        self.overwrite = False
        self.headers = {'user-agent':self.user_agent_string}
        self.count = 0
        self.request_count = 0
        self.delay = 0
        self.s = None
        self.init_session()

    def init_session(self):
        self.s = requests.Session()
        self.s.headers.update({'User-Agent':self.user_agent_string})

    def ensure_dir(self,dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def set_output_dir(self,dir):
        self.output_dir = dir
        self.ensure_dir(dir)

    def is_file_older_than_a_day(self,filename):
        mtime = os.path.getmtime(self.output_dir + filename)
        a_day_ago = time.time() - 60 * 60 * 24
        if mtime < a_day_ago:
            return True
        else:
            return False

    def make_request(self,url=None,filename=None,overwrite=False,check_age=False,payload=None):
        if url is None:
            url = self.url
        if overwrite is True:
            self.overwrite = True

        self.count += 1

        output_path = self.output_dir + filename
        if os.path.isfile(output_path):
            if self.overwrite is True:
                if check_age is True:
                    if self.is_file_older_than_a_day(filename):
                        pass
                    else:
                        file = open(output_path, "r")
                        return file.read()
                else:
                    pass
            elif self.return_data is False:
                return None
            else:
                file = open(output_path, "r")
                return file.read()

        self.request_count += 1
        if self.request_count > 1:
            time.sleep(self.delay)

        if payload:
            print "posting url: " + url
            self.response = self.s.post(url,data=payload,timeout=20,verify=False)
        else:

            print "getting url: " + url
            if self.s is not None:
                # print "using session object"
                # print self.s.cookies
                self.response = self.s.get(url,timeout=20,verify=False)
            else:
                self.response = requests.get(url,headers=self.headers,timeout=20,verify=True)

        # for item in self.response.headers:
        #     print item, self.response.headers[item]
        # print self.response.content
        print self.response.status_code
        print "status code = [%s]" % self.response.status_code
        print

        self.check_valid_response()


        if self.response.status_code == requests.codes.ok:
            self.response_content = self.response.content
        elif self.response.status_code == 201:
            self.response_content = self.response.content
        elif self.response.status_code == 404:
            self.response_content = str(self.response.status_code)
        else:
            self.response_content = self.response.content
            # self.output_response_to_file("debug.htm")
            self.response_content = str(self.response.status_code)
            # raise Exception("error: status code",self.response_content)
        self.output_response_to_file(filename)
        return self.response_content

    def check_valid_response(self):
        if 'Request unsuccessful' in self.response.content:
            raise Exception("error: request unsuccessful")
        if '//content.incapsula.com/jsTest.html' in self.response.content:
            raise Exception("error: //content.incapsula.com/jsTest.html found in source")

        if 'A technical error has occured' in self.response.content:
            raise Exception("error: A technical error has occured")

    def output_response_to_file(self,filename=None):
        if filename is None:
            return
        output_path = self.output_dir + filename
        file = open(output_path, "wb")
        file.write(self.response_content)
        file.close()
        print self.count,"saved to:",output_path

    def get_mtime_for_filename(self,filename=None):
        try:
            mtime = os.path.getmtime(self.output_dir + filename)
        except Exception:
            mtime = None
        return mtime

    # self.s.headers.update( self.load_headers('1_Request.txt') )
    # json_str = self.make_request(ajax_url, ajax_filename, payload=payload)
    def load_headers(self,filename=None):
        if filename is None:
            raise Exception("no input filename entered, for loading headers")
        headers = {}

        with open(filename) as f:
            lines = f.readlines()
            lines = [i.strip() for i in lines]

        for line in lines:
            if line.startswith('GET'):
                continue
            if line.startswith('#'):
                continue
            if line:
                try:
                    left,right = line.split(': ')
                    headers.update({left:right})
                except Exception:
                    pass
            # print(line)

        # print(headers)
        return headers

if __name__ == "__main__":
    s = Scraper()
