#!/usr/local/bin/python3

from html.parser import HTMLParser
from string import printable
import departments_list

class Section():
    def __init__(self,data):
        self.number = data["number"]
        self.section = data["section"]
        self.time = data["time"]
        self.room = data["room"]
        # not finished

class Course():
    def __init__(self,title):
        readable_title = "".join(filter(lambda x: x in printable, title))
        self.identifier = readable_title[:9] #CSCI 3155
        self.name = readable_title[12:] #Principles of Programming Languages
        # some of these will be empty lists for many classes
        self.lectures = [] #list of lectures information
        self.recitations = [] #list of recitation information
        self.labs = [] #list of lab information
        self.seminars = [] #list of labs information
        self.pra = [] #I don't know what pra means?
        self.oth = [] #I don't know what oth means?
    def add_section(self,data):
        if data["section"][-3:] == "LEC":
            self.lectures.append(Section(data))
        elif data["section"][-3:] == "REC":
            self.recitations.append(Section(data))
        elif data["section"][-3:] == "LAB":
            self.labs.append(Section(data))
        elif data["section"][-3:] == "SEM":
            self.seminars.append(Section(data))
        elif data["section"][-3:] == "PRA":
            self.pra.append(Section(data))
        elif data["section"][-3:] == "OTH":
            self.oth.append(Section(data))
        else:
            print(data["section"][-3:])

class MyHTMLParser(HTMLParser):
    def __init__(self,verbose = True):
        self.courses = []
        self.fields = {}
        self.current = None
        self.title = None
        self.verbose = verbose
        super(MyHTMLParser, self).__init__()

    def handle_starttag(self, tag, attrs):
        for attr, value in attrs:
            if attr == "id":
                if "win0divSSR_CLSRSLT_WRK_GROUPBOX2GP$" in value:
                    self.current = "title"
                if "MTG_CLASS_NBR$" in value:
                    self.current = "number"
                if "MTG_CLASSNAME$" in value:
                    self.current = "section"
                if "MTG_DAYTIME$" in value:
                    self.current = "time"
                if "MTG_ROOM$" in value:
                    self.current = "room"
                if "MTG_INSTR$" in value:
                    self.current = "instructor"
                if "MTG_TOPIC$" in value:
                    self.current = "dates"
                if "CU_CLS_RSL_WRK_CU_SSR_UNITS_RANGE$" in value:
                    self.current = "units"
                if "CU_CLS_RSL_WRK_CU_SSR_ENRL_RES$" in value:
                    self.current = "restriction"
                if "CU_CLS_RSL_WRK_CU_SSR_CNSNT_REQ$" in value:
                    self.current = "consent"
                if "CU_CLS_RSL_WRK_AVAILABLE_SEATS$" in value:
                    self.current = "seats"
                if "CU_CLS_RSL_WRK_WAIT_TOT$" in value:
                    self.current = "waitlist"

    def handle_endtag(self, tag):
        # at end of class
        if self.current == "waitlist":
            if self.verbose:
                if "title" in self.fields:
                    print(self.fields["title"] + ":")
                print("Class: " + self.fields["number"])
                print("Section: " + self.fields["section"])
                print("Time: " + self.fields["time"])
                print("Room: " + self.fields["room"])
                print("Instructor: " + self.fields["instructor"])
                print("Dates: " + self.fields["dates"])
                #print("Status: " + self.fields["status"])
                print("Units: " + self.fields["units"])
                print("Enrollment Restriction: " + self.fields["restriction"])
                print("Instructor Consent Required: " + self.fields["consent"])
                print("Available Seats: " + self.fields["seats"])
                print("Wait List Total: " + self.fields["waitlist"])
                print()
            self.courses[-1].add_section(self.fields)
            self.fields = {}
            self.current = None
        if self.current in self.fields:
            self.current = None

    def handle_data(self, data):
        if self.current is not None:
            # Filter out non-printable characters (note: find out why there are non-printable characters!?)
            printable_data = "".join(filter(lambda x: x in printable, data))
            self.fields[self.current] = printable_data
            if self.current == "title":
                self.courses.append(Course(printable_data))


with open("2016-09-26-CSCI.html","r") as f:
    parser = MyHTMLParser(False)
    parser.feed(f.read())
    print(parser.courses[0].identifier)