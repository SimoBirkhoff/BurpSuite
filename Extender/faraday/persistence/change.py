'''
Faraday Penetration Test IDE - Community Version
Copyright (C) 2013  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information

'''

from model.common import (ModelObjectNote, ModelObjectCred, ModelObjectVuln,
                          ModelObjectVulnWeb)
from model.hosts import Host, Interface, Service


class ChangeFactory(object):
    def __init__(self):
        pass

    def create(self, dic):
        _type = dic.get("type")
        if _type in [Host.class_signature,
                     Interface.class_signature,
                     Service.class_signature,
                     ModelObjectNote.class_signature,
                     ModelObjectVuln.class_signature,
                     ModelObjectVulnWeb.class_signature,
                     ModelObjectCred.class_signature,
                     'unknown']:
            return ChangeModelObject(dic)
        else:
            return ChangeCmd(dic)


class Change(object):
    MODEL_OBJECT_ADDED = 1,
    MODEL_OBJECT_MODIFIED = 2
    MODEL_OBJECT_DELETED = 3
    CMD_EXECUTED = 4
    CMD_FINISHED = 5
    UNKNOWN = 999

    def __init__(self, doc):
        self.type = doc.get("type")
        self.action = self.UNKNOWN
        self.msg = "Change: Action: %s - Type: %s" % (self.type, self.action)

    def getAction(self):
        return self.action

    def getType(self):
        return self.type

    def getMessage(self):
        return self.msg


class ChangeModelObject(Change):
    def __init__(self, doc):
        Change.__init__(self, doc)
        num_of_rev = int(doc.get("_rev")[0])
        self.object_name = doc.get("name")
        if doc.get("_deleted"):
            self.action = self.MODEL_OBJECT_DELETED
            self.msg = "Object deleted"
        elif num_of_rev > 1:
            self.action = self.MODEL_OBJECT_MODIFIED
            self.msg = "%s %s modified" % (self.getType(),
                                           self.getObjectName())
        else:
            self.action = self.MODEL_OBJECT_ADDED
            self.msg = "%s %s added" % (self.getType(),
                                        self.getObjectName())

    def getObjectName(self):
        return self.object_name


class ChangeCmd(Change):
    def __init__(self, doc):
        Change.__init__(self, doc)
        self.cmd_info = doc.get('command') + " " + doc.get('params')
        if doc.get("duration"):
            self.action = self.CMD_FINISHED
            self.msg = "Command finished: %s" % self.getCmdInfo()
        else:
            self.action = self.CMD_EXECUTED
            self.msg = "Command executed: %s" % self.getCmdInfo()

    def getCmdInfo(self):
        return self.cmd_info

change_factory = ChangeFactory()
