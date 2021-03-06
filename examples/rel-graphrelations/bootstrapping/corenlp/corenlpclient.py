__author__ = 'hadyelsahar'

import json
import requests


class CoreNlPClient:

    def __init__(self, serverurl="http://127.0.0.1:9000/", annotators="tokenize, ssplit, pos, lemma, ner, parse, dcoref"):

        self.properties = {}
        self.properties["annotators"] = annotators
        self.properties["tokenize.whitespace"] = False
        self.properties["tokenize.whitespace"] = False
        self.properties["outputFormat"] = "json"
        self.serverurl = serverurl


    def annotate(self, s):

        properties = json.dumps(self.properties)
        r = requests.post("%s?properties=%s" %(self.serverurl, properties), data=s)

        if r.status_code == 200:
            x = json.loads(unicode(r.text), strict=False)

            return Parse(x)

        else:
            raise RuntimeError("%s \t %s"%(r.status_code, r.reason))


class Parse:
    """
    a class to hold the output of the corenlp parsed result
    """
    def __init__(self, parsed):
        """

        :param parsed:
        :return:
        """

        self.tokens = [i['originalText'] for i in parsed["sentences"][0]["tokens"]]
        self.positions = [(i['characterOffsetBegin'],i['characterOffsetEnd']) for i in parsed["sentences"][0]["tokens"]]
        self.postags = [i['pos'] for i in parsed["sentences"][0]["tokens"]]
        self.ner = [i['ner'] for i in parsed["sentences"][0]["tokens"]]

        self.parsed_tokens = parsed["sentences"][0]["tokens"]

        # for every token list all incoming or out-coming relations
        # redundant but easy to call afterwards when writing rule based
        # [{"in":[], "out":[]}] ... etc

        # removing the root note and starting counting from 0
        self.dep = [{"in": [], "out":[]} for i in self.tokens]

        for d in parsed["sentences"][0]["basic-dependencies"]:

            if d['dep'] == "ROOT":
                self.dep[d['dependent']-1]["in"].append(("ROOT", None))

            else:
                self.dep[d['dependent']-1]["in"].append((d['dep'], d['governor']-1))
                self.dep[d['governor']-1]["out"].append((d['dep'], d['dependent']-1))

        # removing the root note and starting counting from 0
        self.ccdep = [{"in": [], "out":[]} for i in self.tokens]

        for d in parsed["sentences"][0]["collapsed-ccprocessed-dependencies"]:

            if d['dep'] == "ROOT":
                self.ccdep[d['dependent']-1]["in"].append(("ROOT", None))

            else:
                self.ccdep[d['dependent']-1]["in"].append((d['dep'], d['governor']-1))
                self.ccdep[d['governor']-1]["out"].append((d['dep'], d['dependent']-1))

        self.corefs = parsed["corefs"]
        self.all = parsed






