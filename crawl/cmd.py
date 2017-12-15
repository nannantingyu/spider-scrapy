# -*- coding: utf-8 -*-
import os, sys
import optparse

def parse_options():
    parser = optparse.OptionParser(
            usage=("usage: %prog [options] -c ControllerName"))
    parser.add_option("-c", "--cmd", dest="cmdname", default="cmd_weixin_keywords",
            help=("controller name to run",
                  "[default %default]"))

    opts, args = parser.parse_args()
    return opts, args

def closest_scrapy_cfg(path='.', prevpath=None):
    """Return the path to the closest scrapy.cfg file by traversing the current
    directory and its parents
    """
    if path == prevpath:
        return ''
    path = os.path.abspath(path)
    cfgfile = os.path.join(path, 'scrapy.cfg')
    if os.path.exists(cfgfile):
        return cfgfile
    return closest_scrapy_cfg(os.path.dirname(path), path)

if __name__ == '__main__':
    (opts, args) = parse_options()
    cmdName = "%s" % opts.cmdname.capitalize()
    className = "".join([x.capitalize() for x in cmdName.split("_")])

    module_path = os.path.dirname(closest_scrapy_cfg())
    sys.path.append(module_path)
    cmd_module = "crawl.Cmd.%s" % cmdName

    __import__(cmd_module)

    objCmd = getattr(sys.modules[cmd_module], className)
    obj = objCmd()
    obj.start()