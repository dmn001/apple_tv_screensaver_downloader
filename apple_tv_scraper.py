from scraper import Scraper
from pprint import pprint
# from csv_data_output import csv_data_output
import tarfile
import json
import re
import operator

class apple_tv_scraper(Scraper):
    def __init__(self):
        super(apple_tv_scraper, self).__init__()
        self.set_output_dir('./cache/')

        self.source_urls = ['https://sylvan.apple.com/Aerials/resources-13.tar',
                            'https://sylvan.apple.com/Aerials/resources.tar',
                            'https://sylvan.apple.com/Aerials/2x/entries.json',
                            'http://a1.phobos.apple.com/us/r1000/000/Features/atv/AutumnResources/videos/entries.json']

        self.source_filenames = ['tvOS13', 'tvOS12', 'tvOS11', 'tvOS10']
        self.source_extensions = ['.tar','.tar','.json','.json']

        # self.csv = csv_data_output()
        # self.csv.init_csv()

        self.filename_for_url = {}

    def run(self):
        for url, source, extension in zip(self.source_urls,self.source_filenames,self.source_extensions):
            filename = source + extension
            print url, filename

            self.return_data = False
            self.make_request(url, filename)

            my_tarfile = tarfile.open(self.output_dir + filename)
            # print(my_tarfile.getmembers())

            entries_json = my_tarfile.extractfile('entries.json').read()

            print(len(entries_json))

            self.parse_entries(entries_json)

            break

        for url, filename in sorted(self.filename_for_url.items(), key=operator.itemgetter(1)):
            print filename

        self.output_urls()

    def parse_entries(self,json_str):
        json_obj = json.loads(json_str)

        assets = json_obj['assets']
        for item in assets:
            # url = item['url-4K-SDR']
            url = item['url-4K-SDR']
            filename = "%s" % (item['accessibilityLabel'])

            m = re.match('.*/(.+)',url)
            if m:
                base_filename = m.group(1)

            filename = filename + " " + base_filename
            self.filename_for_url[url] = filename

    def output_urls(self):
        file = open('urls_aria.txt', "wb")
        for x in sorted(self.filename_for_url.items(), key=operator.itemgetter(1)):
            out_str = "%s\n out=%s" % (x[0],x[1])
            file.write(out_str + "\n")
        file.close()

if __name__ == "__main__":
    s = apple_tv_scraper()
    s.run()
