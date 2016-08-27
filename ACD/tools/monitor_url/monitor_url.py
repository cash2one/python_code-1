import ConfigParser
import logging
import sys
import subprocess

import requests


# !/usr/bin/python
# _*_ encoding:utf-8_*_
__author__ = "Miles.Peng"


def run_cmd(cmd, output=False):
    print "Starting run: %s " % cmd
    cmdref = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = cmdref.communicate()
    if error:
        error_msg = "{cmd} run Failed: {error}".format(cmd=cmd, error=error)
        logging.error(error_msg)
        sys.exit(1)
    else:
        output_msg = "{cmd} run Success: {output}".format(cmd=cmd, output=output)
        logging.info(output_msg)
        return output


def _init_log():
    # set basic config when printing file;
    try:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            # filename='/home/qa/scripts/sendReport/sendReport/send_report.log',
                            filename='monitor_url.log',
                            filemode='a')
        # set basic config when printing console;
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
    except IOError, e:
        print "Can't open log file", e
        sys.exit(1)


def get_config(filename, values):
    cf = ConfigParser.SafeConfigParser()
    sections = values
    cf.read(filename)
    configDataSection = cf.sections()
    returnData = {}

    if sections in configDataSection:
        _list = cf.items(sections)
        for _key, _value in _list:
            returnData[_key] = _value
    else:
        print "[ERROR] %s is not in config files,PLS check it %s" % (sections, filename)
        msg_info = "===%s: Get info Failed!!===" % sections
        logging.error(msg_info)
        sys.exit(1)

    return returnData


def get_check_list(config_file, check_section):
    return_values = dict()

    if check_section.lower() == 'all':
        cf = ConfigParser.SafeConfigParser()
        cf.read(config_file)
        sections = cf.sections()
    else:
        sections = check_section.split(',')

    for section in sections:
        return_values[section] = get_config(config_file, section)
    return return_values


def check_argv():
    if len(sys.argv) != 3:
        print "Runing must like monitor_url.py check_url.ini all"
        error_msg = "argv is wrong"
        logging.error(error_msg)
        sys.exit(1)


def check_url(item, values, correct_return):
    url = values.get('url', None)
    if url:
        try:
            r = requests.get(url)
        except requests.ConnectionError:
            error_msg="[ERROR] {url} run Failed by ConnectionError . ".format(url=url)
            logging.error(error_msg)
            sys.exit(1)

        if r.status_code not in correct_return:
            error_msg = "[ERROR] {url} get code: {code}".format(url=url, code=r.status_code)
            logging.error(error_msg)
        else:
            output_msg = "{url} get code: {code}".format(url=url, code=r.status_code)
            logging.info(output_msg)


def main_proce():
    _init_log()
    check_argv()
    config_file = sys.argv[1]
    check_section = sys.argv[2]
    correct_return = [200, 302]

    # get check list(dict)
    check_item = dict()
    check_item = get_check_list(config_file, check_section)

    items = check_item.keys()
    for item in items:
        check_url(item, check_item[item], correct_return)


if __name__ == "__main__":
    main_proce()
