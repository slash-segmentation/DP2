
#
#Copyright (c) 2012, Richard J. Giuly
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#    * Any redistribution, use, or modification is done solely for personal benefit and not for any commercial purpose or for monetary gain
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


# run configurations
# arguments
# "/home/rgiuly/images/ting_labels/test_raw-histeq" "/media/rgiuly/My Book/output/ting_labels" --initseg="/home/rgiuly/images/ting_labels/test_label3d"  --zprocess --submit --sigma=4 --level=0.6 --access_key=AKIAJM2O42KWWQINR5NQ --secret_key=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 --seeds=[[235,916,26]] --input_format=image%03d.tif --initseg_format=image%03d.tif --initial_3d --restart


# old:
# arguments
# O:\images\neuropil\data3 I:\dp2_output --zprocess --submit
# O:\images\neuropil\data3 I:\dp2_output --zprocess --submit --sigma=4 --level=0.5
# /home/rgiuly/images/neuropil/data3 /home/rgiuly/output/paper_cerebellum --zprocess --submit
# /home/rgiuly/images/neuropil/data3 /home/rgiuly/output/paper_cerebellum --zprocess --submit --sigma=4 --level=0.5
#
# "/media/rgiuly/My Book/Spirou-P2_11-16-11_all_2Dbin2/contrast/first4" "/media/rgiuly/My Book/output/spirou"  --zprocess --submit --sigma=4 --level=0.5 --access_key=X --secret_key=X --init --seeds=[[5671,3333,1]] --input_format=contrastfile.%03d.tif





"""
python dseg.py /home/rgiuly/images/neuropil/data3 /home/rgiuly/output/cerebellum0 --zprocess --submit --sigma=4 --level=0.5 --zoffset=0
python dseg.py /home/rgiuly/images/neuropil/data3 /home/rgiuly/output/cerebellum1 --zprocess --submit --sigma=4 --level=0.5 --zoffset=1
python dseg.py /home/rgiuly/images/neuropil/data3 /home/rgiuly/output/cerebellum2 --zprocess --submit --sigma=4 --level=0.5 --zoffset=2
"""


useOnlyRegionsPeopleThoughtWereTouchingTwoCells = True


import sys
sys.path.append("../cytoseg")

import glob
import csv
import time
import re
from struct import *
from data_viewer import *
from volume3d_util import *
from contour_processing import *
import cv
import cv2
import random
import answers
import access_aws
from image_util import *
from images2gif import writeGif
from watershed import *
from dseg_util import *
from pygraph.classes.graph import graph
from random import choice
from collections import OrderedDict
import pygraph.algorithms.accessibility
import pygraph.algorithms.traversal
import argparse
import access_database
import cPickle
import shelve
import sqlite3
import binascii
import SimpleITK
import graph_util
import link_prob
import diffusion
from matplotlib import pyplot as plt
from boto.mturk.qualification import Requirement
import datetime


import sys



#todo: replace this function with getSavedImage and remove getSavedImage
def getInputImage(folder, z):

    filename = inputFilenameFormatString % z
    return scipy.misc.imread(os.path.join(folder, filename))



#imageCache = {}

def getImageStandardFilename(folder, z):

    #if (folder, z) in imageCache:
    #    return imageCache[(folder, z)]

    filename = "output%03d.png" % z
    image = scipy.misc.imread(os.path.join(folder, filename))
    #imageCache[(folder, z)] = image
    return image



#initSegFromPrecomputedStack = False
assignmentsPerHIT = 2
#renderInterval = 120
renderInterval = 40
storage = cv.CreateMemStorage(128000)

useGetPointsForZDecisionTestVersion = True


progressiveSplittingEnabled = False
minimumRegionSizeForSplit = 20

#minimumProbability = 0.525
#minimumProbability = 0.50001
minimumProbability = 50


#zScale = 10.0


# using imod coordinates
#startSlice = 110
startSlice = 0
#stopSlice = 124
#startSlice = 0
#stopSlice = 270



box = Box()

#box.cornerA = [None, None, startSlice]
#box.cornerB = [None, None, stopSlice]


#box.cornerA = [0, 0, 10]
#box.cornerB = [700, 650, 12]

#box.cornerA = [0, 0, 25]
#box.cornerB = [700, 650, 27]

#box.cornerA = [0, 0, 0]
#box.cornerB = [942, 942, 2]

#box.cornerA = [150, 150, 10]
#box.cornerB = [942-150, 942-150, 14]

#box.cornerA = [150, 150, 0]  # used for full run
#box.cornerB = [942-150, 942-150, 70]  # used for full run
#box.cornerA = [150, 150, 0]  # used for full run, christine's data
#box.cornerB = [942-150, 942-150, 70]  # used for full run, christine's data




#box.cornerA = [150, 150, 0]
#box.cornerB = [942-150, 942-150, 3]

##box.cornerA = [0, 0, 200]
##box.cornerB = [700, 700, 202]

#box.cornerA = [0, 0, 250] # for paper revision, cerebellum
#box.cornerA = [0, 0, 250]
#box.cornerB = [700, 700, 251]
#box.cornerB = [700, 700, 270] # for paper revision, cerebellum
#box.cornerB = [700, 700, 270]
#box.cornerB = [700, 700, 252] 
#box.cornerB = [700, 700, 255]

# planning to process last 20 slices with mturk


#box.cornerA = [None, None, None]
#box.cornerB = [None, None, None]

#box.cornerA = [None, None, 0]
#box.cornerB = [None, None, 3]
#box.cornerB = [None, None, 2]

oversegSourceForQualAndProcessAndRender = "watershed"



def makeDirectory(path):

   if not(os.path.isdir(path)):
    os.mkdir(path)

   return path


def clearDirectory(path):

    filelist = glob.glob(os.path.join(path, "*.png"))
    for filename in filelist:
        os.remove(filename)

def makeClearDirectory(path):
    makeDirectory(path)
    clearDirectory(path)



parser = argparse.ArgumentParser(description='DP2 distributed segmentation.')
parser.add_argument("input", action="store")
parser.add_argument("output", action="store")
parser.add_argument("--initseg", action="store", dest="initseg")
parser.add_argument("--threshold", action="store", dest="threshold")
parser.add_argument("--level", action="store", dest="level")
parser.add_argument("--sigma", action="store", dest="sigma")
parser.add_argument("--zoffset", action="store", dest="zoffset")
parser.add_argument("--access_key", action="store", dest="access_key")
parser.add_argument("--secret_key", action="store", dest="secret_key")
parser.add_argument("--answers", action="store", dest="answers")
parser.add_argument("--zoom", action="store", dest="zoom")
parser.add_argument("--xyqual", action="store_true", dest="xyqual")
parser.add_argument("--zqual", action="store_true", dest="zqual")
parser.add_argument("--splitqual", action="store_true", dest="splitqual")
parser.add_argument("--xyprocess", action="store_true", dest="xyprocess")
parser.add_argument("--zprocess", action="store_true", dest="zprocess")
#parser.add_argument("--render", action="store_true", dest="render", nargs="+")
parser.add_argument('--xyrender', metavar='N', nargs='+', help='')
parser.add_argument('--zrender', metavar='N', nargs='+', help='')
parser.add_argument("--skip_tiles", action="store_true", dest="skip_tiles")
parser.add_argument("--init", action="store_true", dest="init")
parser.add_argument("--restart", action="store_true", dest="restart")
parser.add_argument("--submit", action="store_true", dest="submit")
parser.add_argument("--print_regions", action="store_true", dest="print_regions")
parser.add_argument("--seeds", action="store", dest="seeds")
parser.add_argument("--delete", action="store", dest="delete")
parser.add_argument("--send_regions_to_database", action="store_true", dest="send_regions_to_database")
parser.add_argument("--dataset_id", action="store", dest="dataset_id")
parser.add_argument("--model_id", action="store", dest="model_id")
parser.add_argument("--qual_min_slice", action="store", dest="qual_min_slice")
parser.add_argument("--qual_max_slice", action="store", dest="qual_max_slice")
parser.add_argument("--approve_all", action="store_true", dest="approve_all")
parser.add_argument("--delete_all", action="store_true", dest="delete_all")
parser.add_argument("--input_format", action="store", dest="input_format")
parser.add_argument("--initseg_format", action="store", dest="initseg_format")
parser.add_argument("--quick_test_mode", action="store_true", dest="quick_test_mode")
parser.add_argument("--initial_3d", action="store_true", dest="initial_3d")
parser.add_argument("-q", action="store_true", dest="quick_test_mode")
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                   const=sum, default=max,
#                   help='sum the integers (default: find the max)')
#


args = parser.parse_args()

suffix = "suffix"

if args.xyrender or args.zrender:
    suffix = "render"

# default for send regions to database
if args.send_regions_to_database:
    suffix = "z"

# plane to plane processing specified
if args.zqual or args.zprocess or args.splitqual:
    suffix = "z"

# in plane processing
if args.xyqual or args.xyprocess:
    suffix = "xy"


if args.zqual or args.xyqual or args.splitqual:
    makeQualifications = True
else:
    makeQualifications = False

inputStack = args.input
outputFolderBase = args.output


#dataBasename = "TestDataName" # user should specify this
dataBasename = "dseg_test"
if makeQualifications:
    dataName = dataBasename + "_qualification_" + suffix
else:
    dataName = dataBasename + "_" + suffix

dataOutputFolder = os.path.join(outputFolderBase, dataBasename + "_" + suffix)

class Logger(object):

    def __init__(self, type):
        if type == 'stdout':
            self.terminal = sys.stdout
            logFilename = os.path.join(dataOutputFolder, "dseg_log_%s.txt" % datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        elif type == 'stderr':
            self.terminal = sys.stderr
            logFilename = os.path.join(dataOutputFolder, "dseg_log_%s_err.txt" % datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        else:
            raise Exception("invalid type")
        self.log = open(logFilename, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()  

makeDirectory(dataOutputFolder)
sys.stdout = Logger('stdout')
sys.stderr = Logger('stderr')

print args
#print logFilename


# either data or qualification output folder (qualification output folder variable might be dropped to avoid confusion in the future)
outputFolder = os.path.join(outputFolderBase, dataName)


if args.input_format:
    inputFilenameFormatString = args.input_format
else:
    inputFilenameFormatString = "output%03d.png"


# for conversion to and from IMOD
imageHeight = getInputImage(args.input, 0).shape[0]
print "image height:", imageHeight


if args.dataset_id:
    access_database.dataset_id = int(args.dataset_id)

if args.model_id:
    access_database.model_number = int(args.model_id)


stopSlice = max(len(glob.glob1(args.input, "*.png")), len(glob.glob1(args.input, "*.tif")))

print "stop slice", stopSlice
print "input filename format string", args.input_format


if args.submit or args.approve_all or args.delete_all:
    access_aws.initializeMTC(args.access_key, args.secret_key)


if args.approve_all:
    access_aws.approveHITs()


if args.delete_all:
    access_aws.deleteHITs(True)


startPointZOffset = 0
if args.zoffset:
    startPointZOffset = int(args.zoffset)

#startPointsIMOD = [(412, 234, 250-startSlice)] 
#startPointsIMOD = [(412, 234, 250), (226, 442, 164)]
#startPointsIMOD = [(473, 44, 117 + startPointZOffset), (546, 87, 117 + startPointZOffset)]
if args.seeds:
    startPointsIMOD = eval(args.seeds)
#startPointsIMOD = [(412, 234, 0-startSlice)]


print "args", args
#for argument in dict(args):
#    print argument
#print args.accumulate(args.zanswers)




if args.zqual or args.xyqual:
    if args.answers == None:
        raise Exception("Please provide the --answers argument with a valid filename. For example: \n0 yes\n1 no\n2 yes\n")


def promptSplitQualAnswers():

    # todo: should give users the rendered blob and a raw image to look at

    template = os.path.join(dataOutputFolder, "tiles", "regions", "*.jpg")
    answersFilePath = os.path.join(outputFolder, "split_answers%d.txt" % (int(time.time()) % 10000))
    print "answers file:", answersFilePath

    #print "template", template
    #imageFileList = glob.glob(template)


    if useOnlyRegionsPeopleThoughtWereTouchingTwoCells:
        imageFileList = [os.path.join(dataOutputFolder, "tiles", "regions", "region_%s.jpg" % regionID) for regionID in touchMoreThanOne()]
    else:
        imageFileList = [glob.glob(template)]


    # clear the file
    dummy = open(answersFilePath, 'w')
    dummy.close()

    count = 0
    for filename in imageFileList:
        print filename
        image = scipy.misc.imread(filename)
        #print image
        #plt.ion()
        plt.imshow(image)
        #f = plt.figure()
        #f.canvas.flush_events()
        plt.show()
        print count
        number = raw_input("blue highlights more than one cell?: ")

        with open(answersFilePath, 'a') as answersFile:
            answersFile.write("__________\n")
            answersFile.write(str(count) + "\n")
            answersFile.write('%s\n' % filename)
            answersFile.write(number + "\n")

        print 'use --answers="%s"' % answersFilePath

        count += 1
               



#circleRadius = 3
circleRadius = 2
#scaleFactor = 3

if args.zoom:
    scaleFactor = int(args.zoom)
#print "scale factor:", scaleFactor

mturkScriptFolder = os.path.join("aws-mturk-clt-1.3.0", "samples")

if makeQualifications:
    #AWSUrl = "http://s3.amazonaws.com/supervoxel/qualifications/InsideCellCData/tiles/" # used for test run
    AWSUrl = "http://s3.amazonaws.com/%s/qualification/" % dataName
else:
    AWSUrl = "http://s3.amazonaws.com/%s/data/" % dataName

points = []

#outputFolder = r"o:\temp\output"
#inputStack = r"o:\images\neuropil\data\bmp\8bit"
#tileFolder = r"o:\temp\output\tiles"

#outputFolder = "/home/rgiuly/temp/output"
#inputStack = "/home/rgiuly/images/neuropil/data/bmp/8bit"
#tileFolder = "/home/rgiuly/temp/output/tiles"

#outputFolder = "/home/rgiuly/temp/output/guttman"
#inputStack = "/home/rgiuly/images/guttman/tifs/double"
#tileFolder = "/home/rgiuly/temp/output/guttman/tiles"

# used for test run
#outputFolder = "/home/rgiuly/temp/output/guttman"
#inputStack = "/home/rgiuly/images/guttman/wt/double/png"
#tileFolder = "/home/rgiuly/temp/output/guttman/tiles"

#inputStack = "/home/rgiuly/images/guttman/wt/double/png" # user should specify this
#outputFolderBase = "/home/rgiuly/temp/output" # user should specify this




makeDirectory(outputFolder)
tileFolder = os.path.join(outputFolder, "tiles")
makeDirectory(tileFolder)

originalOutputFolder = os.path.join(outputFolder, 'original')
gaussianOutputFolder = os.path.join(outputFolder, 'gaussian')

originalDataOutputFolder = os.path.join(dataOutputFolder, 'original')
gaussianDataOutputFolder = os.path.join(dataOutputFolder, 'gaussian')


#if initSegFromPrecomputedStack:
    #initialSegFolder = os.path.join(outputFolder, 'watershed_result')


if args.initseg:
    initSegFromPrecomputedStack = True
    initialSegFolder = args.initseg   
    initSegFilenameFormat = args.initseg_format
    initSegFileType = 'image'
else:
    initSegFromPrecomputedStack = False
    initialSegFolder = os.path.join(outputFolder, 'initial_seg')
    initSegFilenameFormat = "output%03d.pickle"
    initSegFileType = 'pickle'


renderRegionsInPlane = False

conn = sqlite3.connect(os.path.join(dataOutputFolder, 'dseg.db'))
cursor = conn.cursor()

#cursor.execute('''CREATE INDEX z_index ON regions (z)''')
#cursor.execute('''CREATE INDEX number_index ON regions (number)''')



def readAnswers(filename):

    file = open(filename)
    answers = {}

    while 1:
        line = file.readline()
        if not line:
            break
        print "line", line
        result = re.match(r"(.*)[ \t]+(.*)", line)
        if result == None:
            continue
        number = int(result.group(1))
        text = result.group(2)
        answers[number] = {'answer':text}
        print "number:", number, "   text:", text

    file.close()

    return answers





def readSplitAnswers(filename):

    file = open(filename)
    answers = {}

    while 1:
        dividerLine = file.readline()
        if not dividerLine:
            break
        numberLine = file.readline()
        filenameLine = file.readline()
        answerLine = file.readline()

        print "number line:", numberLine
        number = int(numberLine)
        entry = {'filename':filenameLine[0:-1], 'answer':answerLine[0:-1]}
        answers[number] = entry
        print "number:", number, "entry:", entry   

    file.close()

    return answers




from time import gmtime, strftime


#def uploadFileToAmazonS3(filename, subfolderName):
#
#    # subfolderName should be 'plane_to_plane' or 'in_plane'
#
#    localTileFolder = os.path.join(tileFolder, subfolderName)
#
#    # make bucket if possible
#    if os.name == 'nt':
#        pass
#        "need to use bucket s3://%s" % dataName
#    else:
#        mkdirCommand = "s3cmd mb s3://%s" % dataName
#        print "system", mkdirCommand 
#        os.system(mkdirCommand)
#
#    if makeQualifications:
#        path = "qualification"
#    else:
#        path = "data"
#
#    # upload file
#    print "starting upload"
#    
#    if os.name == 'nt':
#        putCommand = "i:\\downloads\\s3.exe put %s/%s/%s/ %s /acl:public-read" % (dataName, path, subfolderName, os.path.join(localTileFolder, filename))
#    else:
#        putCommand = "s3cmd put --acl-public %s s3://%s/%s/%s/" % (os.path.join(localTileFolder, filename), dataName, path, subfolderName)
#    print "system", putCommand
#    os.system(putCommand)
#    print "finished upload"



def copyTilesToAmazonS3(inputPath):

    mkdirCommand = "s3cmd mb s3://%s" % dataName
    print "system", mkdirCommand 
    os.system(mkdirCommand)

    if makeQualifications:
        path = "qualification"
    else:
        path = "data"

    putCommand = "s3cmd put --recursive --acl-public \"%s\" s3://%s/%s/" % (inputPath, dataName, path)
    print "system", putCommand
    os.system(putCommand)



def writeGlobalPropertiesFile(filename, access_key, secret_key):

    file = open(filename, 'w')
    text = """#
# This file will be overwritten by dseg.
#
# You can find your access keys by going to aws.amazon.com, hovering your mouse over "Your Web Services Account" in the top-right
# corner and selecting View Access Key Identifiers. Be sure to log-in with the same username and password you registered with your
# Mechanical Turk Requester account. 
#
# If you don't yet have a Mechanical Turk Requester account, you can create one by visiting http://requester.mturk.com/
#
# i.e.
access_key=%s
secret_key=%s


# -------------------
# ADVANCED PROPERTIES
# -------------------
#
# If you want to test your solution in the Amazon Mechanical Turk Developers Sandbox (http://sandbox.mturk.com)
# use the service_url defined below:
#service_url=https://mechanicalturk.sandbox.amazonaws.com/?Service=AWSMechanicalTurkRequester

# If you want to have your solution work against the Amazon Mechnical Turk Production site (http://www.mturk.com)
# use the service_url defined below:
service_url=https://mechanicalturk.amazonaws.com/?Service=AWSMechanicalTurkRequester

# The settings below should only be modified under special circumstances.
# You should not need to adjust these values.
retriable_errors=Server.ServiceUnavailable,503
retry_attempts=6
retry_delay_millis=500""" % (access_key, secret_key)
    file.write(text)
    file.close()


def writePropertiesFile(filename, qualificationBasename, description):

    file = open(filename, 'w')
    text = """#
# This file will be overwritten by dseg.
#
# Basic qualification attributes
#
name=%s_%s_%s
description=%s
keywords=knowledge
retrydelayinseconds=3600

# Workers will have 60 minutes to complete this test. 15 minutes = 60 seconds * 15 minutes = 3600
testdurationinseconds=3600
""" % (qualificationBasename, suffix, strftime("%j_%H_%M_%S", gmtime()), description)
    print text
    file.write(text)
    file.close()


def makeRegionIdentifier(zIndex, number):

    #return "%04d_%04d" % (zIndex, number)
    return "%d_%d" % (zIndex, number)


def removeBigDarkNodes(gr, v, allRegions):

    averageGrayValue = {}
    nodesToRemoveDict = {}

    for regionName in gr.nodes():

        (z, dummy) = regionIdentifierToNumbers(regionName)
        region = allRegions[regionName]
        
        total = 0
        for point in region:
            (x, y) = point
            total += v[x, y, z]

        average = float(total) / float(len(region))

        print "regionName:", regionName, "    average:", average, " size:", len(region)

        #if len(region) * (256 - average) > (256 - 80) * 1000:
        if len(region) > 800 and average < 90:
            nodesToRemoveDict[regionName] = True

    # remove edges associated with nodes that need to be deleted
    edges = gr.edges()
    for edge in edges:
        if edge[0] in nodesToRemoveDict or edge[1] in nodesToRemoveDict:
            if gr.has_edge(edge):
                gr.del_edge(edge)  

    # remove nodes that need to be deleted
    for node in gr.nodes():
        if node in nodesToRemoveDict:
            gr.del_node(node)


def averagePoint2D(points):

    x = 0
    y = 0
    for point in points:
        x += point[0]
        y += point[1]
    return (x / len(points), y / len(points))


startOfHeaderCerebellumExample = """<?xml version="1.0"?>
<QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd">
    <Overview>
        <Title>Are dots inside a cell</Title>
    <Text>
      Instructions
      Your task is to determine if both dots are inside of one cell. In order to do this, it's important to know what cells are in the image. Take a look at the raw image below and the corresponding image with cells outlined. This will give you an idea of what the cells are. Then take a look at the 10 examples. They show you exactly the kind of question you will need to answer (correct answers are given for the examples). Then you're ready to take the test (questions at the bottom of this page).
      
    </Text>
    <Text> Raw Image: </Text>
    <Binary>
         <MimeType>
          <Type>image</Type>
           <SubType>jpg</SubType>
         </MimeType>
         <DataURL>http://s3.amazonaws.com/supervoxel/examples/original_image.jpg</DataURL>
         <AltText>Cell Overview</AltText>
    </Binary>
    <Text> Image with cells outlined: </Text>
    <Binary>
         <MimeType>
          <Type>image</Type>
           <SubType>jpg</SubType>
         </MimeType>
         <DataURL>http://s3.amazonaws.com/supervoxel/examples/data0057_marked.jpg</DataURL>
         <AltText>Cell Overview</AltText>
    </Binary>
                  <Text>
                  ____________________________________________________________
                  </Text>
"""


startOfHeaderCerebellumExample2 = """<?xml version="1.0"?>
<QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd">
    <Overview>
        <Title>Are dots inside a cell</Title>
    <Text>
      Instructions
      Your task is to determine if both dots are inside of one cell. Take a look at the examples. They show you exactly the kind of question you will need to answer (correct answers are given for the examples). Then you're ready to take the test (questions at the bottom of this page).
      
    </Text>
    <Text> Raw Image: </Text>
    <Binary>
         <MimeType>
          <Type>image</Type>
           <SubType>jpg</SubType>
         </MimeType>
         <DataURL>http://s3.amazonaws.com/supervoxel/examples/original_image.jpg</DataURL>
         <AltText>Cell Overview</AltText>
    </Binary>
                  <Text>
                  ____________________________________________________________
                  </Text>
"""



startOfHeaderCerebellumExample3 = """<?xml version="1.0"?>
<QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd">
    <Overview>
        <Title>Are dots inside a cell</Title>
    <Text>
      Instructions
      Your task is to determine if both dots are inside of one cell. Take a look at the examples. They show you exactly the kind of question you will need to answer (correct answers are given for the examples). Then you're ready to take the test (questions at the bottom of this page).
      
    </Text>
                  <Text>
                  ____________________________________________________________
                  </Text>
"""


def makeStartOfHeader(title):

    return """<?xml version="1.0"?>
<QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd">
    <Overview>
        <Title>%s</Title>
    <Text>
      Instructions
      Take a look at the examples. They show you exactly the kind of question you will need to answer (correct answers are given for the examples). Then you're ready to take the test (questions at the bottom of this page).
      
    </Text>
                  <Text>
                  ____________________________________________________________
                  </Text>
""" % title

    
    



startOfHeaderAxonExample = """<?xml version="1.0"?>
<QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd">
    <Overview>
        <Title>Are dots inside a cell</Title>
    <Text>
      Instructions
      Your task is to determine if both dots are inside of one cell. In this image you will see cells and border (which is dark stuff that is not part of the cells). In order to do this task, it's important to know what cells are in the image. Take a look at the raw image below and the corresponding image with border (dark stuff between cells colored red). This will give you an idea of what the cells are and what the border between cells is. Then take a look at the 10 examples. They show you exactly the kind of question you will need to answer (correct answers are given for the examples). Then you're ready to take the test (questions at the bottom of this page).
      
    </Text>
    <Text> Raw Image: </Text>
    <Binary>
         <MimeType>
          <Type>image</Type>
           <SubType>jpg</SubType>
         </MimeType>
         <DataURL>http://s3.amazonaws.com/supervoxel/examples/out0045_cropped_raw.jpg</DataURL>
         <AltText>Cell Overview</AltText>
    </Binary>
    <Text> Image with cells outlined: </Text>
    <Binary>
         <MimeType>
          <Type>image</Type>
           <SubType>jpg</SubType>
         </MimeType>
         <DataURL>http://s3.amazonaws.com/supervoxel/examples/out0045_cropped_with_seg.jpg</DataURL>
         <AltText>Cell Overview</AltText>
    </Binary>
                  <Text>
                  ____________________________________________________________
                  </Text>
"""

#startOfHeader = startOfHeaderCerebellumExample3

endOfHeader = """</Overview>"""

footer = """    
</QuestionForm>"""


answersHeader = """<?xml version="1.0" encoding="UTF-8"?> 
<AnswerKey xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/AnswerKey.xsd">
"""

answersFooter = """</AnswerKey>"""



# image size
#s = [700, 700]


def initializeVolumes():

    global v
    global s

    v = loadImageStack(inputStack, box)
    makeClearDirectory(originalOutputFolder)
    writeStack(originalOutputFolder, v, startIndex=startSlice)
    
    print "starting gaussian"

    if args.sigma:
        sigma = float(args.sigma)
    else:
        sigma = 2.0


    if 1:
        makeClearDirectory(gaussianOutputFolder)
        processImageStack(originalOutputFolder,
                          gaussianOutputFolder,
                          gaussian2DNumpy,
                          (startSlice, stopSlice),
                          {'sigma':sigma})

    #gaussian = zeros(v.shape)
    #for z in range(gaussian.shape[2]):
    #    gaussian[:,:,z] = gaussian2DNumpy(v[:,:,z])
    #writeStack(gaussianOutputFolder, gaussian)

    s = v.shape


    if 1:
        makeDirectory(initialSegFolder)
    
        if not(initSegFromPrecomputedStack):
            makeLabelVolumeStackWatershed(os.path.join(outputFolder, 'original'), initialSegFolder)





def writeZEdges(zEdges):

    for filename in ("zEdges.pickle", "zEdges_original.pickle"): 
        zEdgesFile = open(os.path.join(outputFolder, filename), 'wb')
        cPickle.dump(zEdges, zEdgesFile)
        zEdgesFile.close()



def initializeZEdges():

    print "initialize zEdges"
    #filename = os.path.join(outputFolder, 'request_loop_data')
    #dict = shelve.open(filename)

    if initSegFromPrecomputedStack:
        zEdges = getZEdges(precomputedInitSeg=True)
    else:
        zEdges = getZEdges(precomputedInitSeg=False)
    #dict['zEdges'] = zEdges

    #dict.close()

    writeZEdges(zEdges)

    print "finished initialize zEdges"




#todo: move to util file
def toOpenCV_old(array, color=None):

    if color:
        channels = 3
    else:
        channels = 1
    s = array.shape
    openCVImage = cv.CreateImage((s[0], s[1]), 8, channels)
    #test = cv.CreateImage((s[1], s[0]), 8, channels)

    for i in range(0, s[0]):
        for j in range(0, s[1]):
            value = array[i, j]
            if channels == 3:
                openCVImage[j, i] = (value, value, value)
                #test[i, j] = (value, value, value)
            elif channels == 1:
                openCVImage[j, i] = value
                #test[i, j] = value
            else:
                raise Exception("invalid channel number")

    return openCVImage


def toOpenCV(array, color=None):

    s = array.shape
    #transposeArray = numpy.copy(array)
    #numpy.transpose(transposeArray)
    matRawUntransposed = cv.fromarray(array)
    print "type", matRawUntransposed.type
    print str(matRawUntransposed)
    #print "0", type(matRawUntransposed)
    # note: array is type 6, this tells you what type 6 means: str(cv.CreateMat(10, 10, 6))

    # image to store output of transpose operation
    matRaw = cv.CreateImage((s[0], s[1]), cv.IPL_DEPTH_64F, 1)
    cv.Transpose(matRawUntransposed, matRaw)

    mat = cv.CreateImage((s[0], s[1]), 8, 1)
    #mat = cv.CreateImage((s[0], s[1]), cv.IPL_DEPTH_8U, 1)
    #print "1", cv.GetSize(matRaw)
    #print "2", cv.GetSize(mat)
    #print "3", type(matRaw)
    #print "4", type(mat) #mat.type()
    # convert to 8 bit integer
    cv.ConvertScaleAbs(matRaw, mat)
    #matRaw.ConvertTo(mat, cv2.CV_8U)

    #print mat.depth()

    if color:

        channels = 3
        openCVImage = cv.CreateImage((s[0], s[1]), 8, channels)
        #print openCVImage.depth()
        cv.CvtColor(mat, openCVImage, cv.CV_GRAY2RGB)
        return openCVImage

    else:

        #raise Exception("todo: test this before removing exception")
        #return mat
        return toOpenCV_old(array, color=color)





def resizeCV(image, factor, color=None):

    if color:
        channels = 3
    else:
        channels = 1

    result = cv.CreateImage((int(image.width*factor), int(image.height*factor)), 8, channels)
    cv.Resize(image, result)

    return result


def isBoxInside(width, height, boundingBox):

    x1 = boundingBox[0]
    y1 = boundingBox[1]
    x2 = boundingBox[2]
    y2 = boundingBox[3]

    if x1 < 0:
        return False
        #x1 = 0
    if y1 < 0:
        return False
        #y1 = 0
    if x2 >= height:
        return False
        #x2 = array.height
    if y2 >= width:
        return False
        #y2 = array.width

    return True


def cropCV(array, boundingBox):

    #return none if the requested box is not inside of the image
    #if not(isBoxInside(array.width, array.height, boundingBox)):
    #    return None

    x1 = boundingBox[0]
    y1 = boundingBox[1]
    x2 = boundingBox[2]
    y2 = boundingBox[3]

    channels = 3
    sizeX = x2 - x1
    sizeY = y2 - y1
    #result = zeros((sizeX, sizeY))
    result = cv.CreateImage((sizeY, sizeX), 8, channels)
    cv.Set(result, (255, 255, 255))
    for x in range(x1, x2):
        for y in range(y1, y2):
            #if x >= 0 and y >= 0 and x < array.width and y < array.height:
            if x >= 0 and y >= 0 and x < array.height and y < array.width:
                #print x, y
                result[x-x1, y-y1] = array[x, y]

    return result




def getRegions2D(image, zIndex):

    regions = {}
    s1 = image.shape
    count = 0
    lastId = -1 #todo: probably not used

    map = {}

    for i in range(0, s1[0]):
        for j in range(0, s1[1]):
            number = image[i, j]

            # map number in image to a unique id
            if number in map:
                id = map[number]
            else:
                #id = uuid.uuid1()
                id = makeRegionIdentifier(zIndex, number)
                map[number] = id

            if id in regions:
                regions[id].append((i, j))
            else:
                region = graph_util.Region2D()
                region.z = zIndex
                region.append((i, j))
                regions[id] = region
                #print "id", id

    return regions


def getRegionStack_old(labelVolume):

    stack = []
    for z in range(labelVolume.shape[2]):
        stack.append(getRegions2D(labelVolume[:, :, z]))

    return stack


def getRegionStack_old2(labelVolume):

    allRegions = {}
    for z in range(labelVolume.shape[2]):
        regionDict = getRegions2D(labelVolume[:, :, z])
        for r in regionDict:
            #print "(z, r)", (z, r)
            allRegions[(z, r)] = regionDict[r]

    return allRegions


def getAllRegions_depricated_ouput_as_dictionary(labelVolume):

    allRegions = {}
    for z in range(labelVolume.shape[2]):
        regionDict = getRegions2D(labelVolume[:, :, z], z)
        for id in regionDict:
            #print "id", id
            allRegions[id] = regionDict[id]

    return allRegions


def getStartAndStop(zStart, zStop, max):
    if zStart == None:
        zStartResult = 0
    else:
        zStartResult = zStart

    if zStop == None:
        zStopResult = max
    else:
        zStopResult = zStop

    return zStart, zStop


def makeAllRegions(initialSegFolder, inputFileExtension="pickle"):

    count = 0

    # clear lock on database if there is one
    conn = sqlite3.connect(os.path.join(dataOutputFolder, 'dseg.db'))
    conn.commit()
    conn.close()

    conn = sqlite3.connect(os.path.join(dataOutputFolder, 'dseg.db'))

    c = conn.cursor()


    # Create table
    #c.execute('''CREATE TABLE stocks
    #             (date text, trans text, symbol text, qty real, price real)''')

    print "database file:", os.path.join(dataOutputFolder, 'dseg.db')
    print "reseting regions table"
    try:
        c.execute('DROP TABLE regions')
    except:
        print "didn't drop table"

    #c.execute('''IF OBJECT_ID('regions', 'U') IS NOT NULL
    #  DROP TABLE regions''')
    c.execute('''CREATE TABLE regions
                 (z INT, number INT, points BLOB, id INT PRIMARY KEY)''')
    c.execute('''CREATE INDEX z_index ON regions (z)''')
    c.execute('''CREATE INDEX number_index ON regions (number)''')

    numFiles = len(glob.glob(os.path.join(initialSegFolder, "*." + inputFileExtension)))

    print "adding regions"
    zStart, zStop = getStartAndStop(startSlice, stopSlice, numFiles)
    for z in range(zStart, zStop):

        if args.quick_test_mode and z > 10:
            break

        print "adding regions in plane", z

        #filename = "output%03d.pickle" % z

        #regionDict = getRegions2D(labelVolume[:, :, z], z)
        #regionDict = getRegions2D(numpy.transpose(scipy.misc.imread(os.path.join(initialSegFolder, filename))), z)

        #inputImageFile = open(os.path.join(initialSegFolder, filename), 'rb')
        #regionDict = getRegions2D(numpy.transpose(cPickle.load(inputImageFile)), z)
        #inputImageFile.close()
        image = getSavedImage(initialSegFolder, z, initSegFilenameFormat, initSegFileType)
        print "image shape", image.shape
        print image
        SimpleITK.WriteImage(SimpleITK.GetImageFromArray(array(image, dtype=ushort)), "i:\\temp\\test.png") 
        regionDict = getRegions2D(numpy.transpose(image), z)

        for id in regionDict:
            print "id", id
            #allRegions[id] = regionDict[id]

            (zValue, numberValue) = regionIdentifierToNumbers(id)

            region = regionDict[id]

            # Insert a row of data
            #regionString = cPickle.dumps(region)
            #regionString = binascii.hexlify(regionString)
            regionString = binascii.hexlify(cPickle.dumps(region))
            c.execute("INSERT INTO regions VALUES (%d, %d,'%s', %d)" % (zValue, numberValue, regionString, count))
            count += 1

        # Save (commit) the changes
        print "commit"
        conn.commit()


    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


#def getRegionStack(allRegions):
#
#    regionStack = {}
#
#    for region in allRegions.values():
#
#        # add region
#        if not(region.z in regionStack):
#            regionStack[region.z] = []
#        regionStack[region.z].append(region)
#
#    return regionStack


def getEdges2D(image, zIndex):

    edges = {}
    s1 = image.shape
    count = 0
    lastNumber = None
    #lastNumber = -1 #todo: this should be at the beginning of each scan line probably

    # scan for changes along first coordinate
    for i in range(0, s1[0]):
        lastNumber = None
        for j in range(0, s1[1]):
            number = image[i, j]
            if lastNumber != None and number != lastNumber:
                center = (i, j)
                points.append(center)
                node1 = makeRegionIdentifier(zIndex, number)
                node2 = makeRegionIdentifier(zIndex, lastNumber)
                if number < lastNumber:
                    #key = (number, lastNumber)
                    key = (node1, node2)
                else:
                    #key = (lastNumber, number)
                    key = (node2, node1)
                #print "get edges 2D key", key
                if not(key in edges):
                    edges[key] = []
                edges[key].append(center)
            lastNumber = number

    # scan for changes along second coordinate
    for j in range(0, s1[1]):
        lastNumber = None
        for i in range(0, s1[0]):
            number = image[i, j]

            if lastNumber != None and number != lastNumber:
                center = (i, j)
                points.append(center)
                node1 = makeRegionIdentifier(zIndex, number)
                node2 = makeRegionIdentifier(zIndex, lastNumber)
                if number < lastNumber:
                    #key = (number, lastNumber)
                    key = (node1, node2)
                else:
                    #key = (lastNumber, number)
                    key = (node2, node1)
                if not(key in edges):
                    edges[key] = []
                edges[key].append(center)
            lastNumber = number

    return edges


def getZEdges_old(labelVolume):

    edges = {}
    s1 = labelVolume.shape

    # scan for changes along third coordinate
    for i in range(0, s1[0]):
        for j in range(0, s1[1]):

            lastNumber = None

            for k in range(0, s[2]):

                number = (k, labelVolume[i, j, k])

                # if this is not the first iteration, add the edge
                if lastNumber != None:
                    key = (lastNumber, number)
                    edges[key] = True

                lastNumber = number

    return edges


def getZEdges_depricated_because_reads_whole_volume(labelVolume):
    # this is maybe incorrect because there is always assumed to be a change from one plane to the next, it should not even check to see if they have different numbers

    edges = {}
    s1 = labelVolume.shape

    # scan for changes along third coordinate
    for i in range(0, s1[0]):
        for j in range(0, s1[1]):

            lastNumber = None

            for k in range(0, s[2]):

                number = labelVolume[i, j, k]

                # if this is not the first iteration, add the edge
                if lastNumber != None:

                    node1 = makeRegionIdentifier(k, number)
                    node2 = makeRegionIdentifier(lastK, lastNumber)

                    if number < lastNumber:
                        key = (node1, node2)
                    else:
                        key = (node2, node1)

                    edges[key] = True

                lastNumber = number
                lastK = k

    return edges




def getSavedImage(folder, z, filenameFormat, type):

    #numFiles = len(glob.glob(os.path.join(folder, "*." + fileExtension)))

    if type == 'pickle':
        filename = filenameFormat % z
        file = open(os.path.join(folder, filename), 'rb')
        result = cPickle.load(file)
        file.close()
    elif type == 'image':
        #filename = "out%04d_cv2_float.mha" % z
        filename = filenameFormat % z
        fullFilename = os.path.join(folder, filename)
        if not(os.path.isfile(fullFilename)):
            raise Exception("image file %s does not exist" % fullFilename)
        result = SimpleITK.GetArrayFromImage(SimpleITK.ReadImage(fullFilename))
    else:
        raise Exception("invalid type")

    return result


#def getZEdges(fileExtension="pickle"):

def getZEdges(precomputedInitSeg):

    if precomputedInitSeg:
        fileCountFormat = "*.tif" #todo: this should be a configurable extension
    #    type = 'image'
    #    format = args.initseg_format
    else:
        fileCountFormat = "*.pickle"
    #    type = 'pickle'
    #    format = "output%03d.pickle"


    stepSize = 2
    print "get z edges step size:", 2

    edges = OrderedDict()

    gap = 1

    numFiles = len(glob.glob(os.path.join(initialSegFolder, fileCountFormat)))
    startZ, stopZ = getStartAndStop(startSlice, stopSlice, numFiles)
    for k in range(startZ, stopZ - gap):
        print "getting z edges"
        print "current slices: %d and %d, stop: %d" % (k, k + gap, stopZ - gap)

        if args.quick_test_mode and k > 10:
            break

        #filename1 = "output%03d.png" % k
        #filename2 = "output%03d.png" % (k + 1)

        #image1 = numpy.transpose(scipy.misc.imread(os.path.join(initialSegFolder, filename1)))
        #image2 = numpy.transpose(scipy.misc.imread(os.path.join(initialSegFolder, filename2)))
        image1 = numpy.transpose(getSavedImage(initialSegFolder, k, initSegFilenameFormat, initSegFileType))
        image2 = numpy.transpose(getSavedImage(initialSegFolder, k + gap, initSegFilenameFormat, initSegFileType))


        # scan for changes along third coordinate
        for i in range(0, image1.shape[0], stepSize):
            for j in range(0, image1.shape[1], stepSize):
    
                    number1 = image1[i, j]
                    number2 = image2[i, j]
    
                    if 1:
    
                        node1 = makeRegionIdentifier(k, number1)
                        node2 = makeRegionIdentifier(k + gap, number2)

                        # makes the ordering consistent    
                        if number1 < number2:
                            key = (node1, node2)
                        else:
                            key = (node2, node1)
    
                        edges[key] = True
    

    return edges











def addAnimationSuffix(filename):
    return filename + "_" + "animation"


def makeInPlaneUrl(filename):

    extension = ".jpg"
    url = AWSUrl + "in_plane" + "/" + filename + extension
    return url


def makePlaneToPlaneUrl(filename):

    extension = ".gif"
    url = AWSUrl + "plane_to_plane" + "/" + addAnimationSuffix(filename) + extension
    return url


def makeRegionsUrl(filename):

    url = AWSUrl + "regions" + "/" + filename
    return url


def drawEdges(cvImage, edges):

    # draw translucent green edges
    for key in edges:
        for point in edges[key]:
            if 1:
                background = cvImage[point[1], point[0]]
            else:
                background = (0, 0, 0)
            color = (background[0], (background[1] + 255) / 2, background[2], 0)
            cv.Circle(cvImage, (point[0], point[1]), 0, color)


def makeTilesInPlane(outputCSVFilename, useEdges=False, useCenterPoints=False):

    examples = ""
    questions = ""
    answersText = ""

    # image is the label image (not used in this method)
    # todo: cvImage and tempImage are redundant
    zIndex = 1

    #(edges, regions, cvImage, tempImage, image) = processXYSlice_old(v[:, :, zIndex], zIndex)

    labelVolume = makeLabelVolumeWatershed(v)
    #labelVolume = makeLabelVolumeSLIC(v)

    fileList = []

    if 0:
        # calculate total number of edges and display the total
        totalNumberOfEdges = 0
        for zIndex in range(labelVolume.shape[2]):
            labelImage = labelVolume[:, :, zIndex]
            edges = getEdges2D(labelImage, zIndex)
            totalNumberOfEdges += len(edges)
        print "total number of edges:", totalNumberOfEdges
        sys.exit()


    for zIndex in range(labelVolume.shape[2]):

        labelImage = labelVolume[:, :, zIndex]
        regions = getRegions2D(labelImage, zIndex)
        edges = getEdges2D(labelImage, zIndex)
    
        cvImage = toOpenCV(v[:, :, zIndex], color=True)
    
        #drawEdges(cvImage, edges)
    
        print "edges:", edges
        print "number of edges for this plane:", len(edges)
        print "regions sample (first 3)"
        regionPrintCount = 0
        for regionKey in regions:
            print regionKey, regions[regionKey]
            regionPrintCount += 1
            if regionPrintCount >= 3:
                break
    
        usedEdges = {}
        i = 0
        #fileList = []
    

        # function: makeTilesInPlane    
        # for each edge between supervoxels
        for key in edges:
        
            edge = edges[key]
            #print "edge", edge

            #(xMin, yMin, xMax, yMax) = array(boundingBox(edge))
            #b1 = (yMin, xMin, yMax, xMax)
            #borderSize = 180

            #print "regions", regions
            region0 = regions[key[0]]
            region1 = regions[key[1]]
            #insidePoints = [getPointInside(region0), getPointInside(region1)]
            insidePoints = [getMaxPoint(region0, gaussian[:, :, region0.z]), getMaxPoint(region1, gaussian[:, :, region1.z])]
            #b2 = boundingBoxTwoPoint(insidePoints[0], insidePoints[1])
            #b1 = array([b2[1], b2[0], b2[3], b2[2]])
            b1 = boundingBoxTwoPoint(insidePoints[0], insidePoints[1])
            #borderSize = 65
            borderSize = 100

            # add boarder
            b = b1 + array([-borderSize, -borderSize, borderSize, borderSize])
            #b = b1
    
            # extract a a tile from the full image
            # b is a bounding box around the current edge
            # croppedCV returns None if the cropped region doesn't fit in the full image
            b2 = array([b[1], b[0], b[3], b[2]])
            #croppedRaw1 = cropCV(cvImage, b)
            #cropped1 = cropCV(cvImage, b)
            croppedRaw1 = cropCV(cvImage, b2)
            cropped1 = cropCV(cvImage, b2)

            inPlaneTileFolder = os.path.join(tileFolder, "in_plane")

            writeInPlaneMultilayerGIF(inPlaneTileFolder, v, b, region0.z, insidePoints, key)

            if croppedRaw1: croppedRaw = resizeCV(croppedRaw1, scaleFactor, color=True)
            else: croppedRaw = None
            #print "hello"
            if cropped1: cropped = resizeCV(cropped1, scaleFactor, color=True)
            else: cropped = None
        
            #print "box", b
        
            # if there's a cropped region, draw edge or dot on the cropped region
            if cropped != None:
    
                usedEdges[key] = edges[key]
    
                # draw edge
                # todo: this needs to be tested
                if useEdges:
                    #print "edge", edge
                    for point in edge:
                        print "------------------------"
                        print "b1", b1
                        print "point", point
                        center = array(point) - array([b[1], b[0]])
                        print "center", center
                        cv.Circle(cropped, (center[1] * scaleFactor, center[0] * scaleFactor), scaleFactor, (0, 0, 255, 0), thickness=-1)
    
                # draw dot
                if useCenterPoints:
                    for regionIndex in range(0, 2):
                        #print "regionIndex", regionIndex
                        #print "key[regionIndex]", key[regionIndex]
                        #print "regions.keys()", regions.keys()
                        #print "edges.keys()", edges.keys()
                        #center = averagePoint2D(regions[key[regionIndex]]) - array([b[1], b[0]])
                        center = array(insidePoints[regionIndex]) - array([b[0], b[1]])
                        print "center", center
                        # fill region with color
                        if renderRegionsInPlane:
                            regionColor = [(0, 255, 0, 0), (0, 127, 0, 0)]
                            for rawPoint in [region0, region1][regionIndex]:
                                point = rawPoint - array([b[0], b[1]])
                                cv.Circle(cropped, (point[0] * scaleFactor, point[1] * scaleFactor), 4, regionColor[regionIndex], thickness=-1)
                        cv.Circle(cropped, (center[0] * scaleFactor, center[1] * scaleFactor), 4, (0, 0, 255, 0), thickness=-1)
    
    
                # write the current tile to file
                filename = "crop"
                print "key", key
                for id in key:
                    filename += "_%s" % id
                #filename += ".png"
                extension = ".jpg"
                inPlaneDiagnosticTileFolder = os.path.join(tileFolder, "in_plane_diagnostic")
                makeDirectory(inPlaneTileFolder)
                makeDirectory(inPlaneDiagnosticTileFolder)
                fullFilename = os.path.join(inPlaneTileFolder, filename + extension)
                fullFilenameRaw = os.path.join(inPlaneDiagnosticTileFolder, filename + "_raw" + extension)
                fileList.append(filename)
                i += 1
                print fullFilename
                cv.SaveImage(fullFilename, cropped)
                cv.SaveImage(fullFilenameRaw, croppedRaw)

                if makeQualifications:
                    if i >= 50: break
                    #if i >= 5: break
    

    if not(makeQualifications):

        # make tiles in plane, write csv file that specifies image files for questions
    
        #file.write("id1,id2\n")
        file = open(outputCSVFilename, 'w')
        file.write("image1,image2\n")
    
        #for key in usedEdges:
        #
        #    edge = usedEdges[key]
        #    for index in key:
        #        file.write("%d," % index)
        #    file.write("\n")
    
        for filename in fileList:
            url1 = makeInPlaneUrl(filename)
            file.write(url1)
            file.write(",")
            url2 = makeInPlaneUrl(filename + "_raw")
            file.write(url2)
            #file.write(AWSUrl + "in_plane" + "/" + filename + "_raw" + extension)
            file.write("\n")

        file.close()


    if makeQualifications:

        answersDict = readAnswers(args.answers)

        # examples
        print "making examples"
        for i in range(0, 20):
            url = makeInPlaneUrl(fileList[i])
            examples += makeInPlaneExample(i, url, answersDict[i])

        # make questions and answers
        print "making questions and answers"
        for i in range(20, 50):
            url = makeInPlaneUrl(fileList[i])
            number = i
            questions += makeInPlaneQuestion(number, url)
            answersText += makeAnswer(number, answersDict[i])
            print "makeAnswer", number, answersDict[i]

        # write questions and answers to file
        print "writing questions and answers to file"
        questionFilename = os.path.join(mturkScriptFolder, "in_plane", "qualification.question")
        print "writing file", questionFilename
        questionFile = open(questionFilename, 'w')
        #todo: makeStartOfHeader(text) will need the text variable to exist
        questionFile.write(makeStartOfHeader(text) + examples + endOfHeader + questions + footer)
        questionFile.close()
    
        answerFilename = os.path.join(mturkScriptFolder, "in_plane", "qualification.answer")
        print "writing file", answerFilename
        answerFile = open(answerFilename, 'w')
        answerFile.write(answersHeader + answersText + answersFooter)
        answerFile.close()




def getPointInside(region):

    centerWithoutOffset = averagePoint2D(region)
    #print "regions[imageNumber]", regions[imageNumber]
    print "centerWithoutOffset", tuple(centerWithoutOffset)
    isInsideTheRegion = tuple(centerWithoutOffset) in region
    print "centerWithoutOffset in regions[imageNumber]", isInsideTheRegion
    if not(isInsideTheRegion):
        numPixels = len(region)
        arbitraryIndex = int(numPixels / 2)
        #centerWithoutOffset = choice(region)
        centerWithoutOffset = region[arbitraryIndex]
        print "changing to centerWithoutOffset:", centerWithoutOffset

    return centerWithoutOffset


def getMaxPoint(region, intensity2DImage):

    numPixels = len(region)

    arbitraryIndex = int(numPixels / 2)
    max = 0
    maxCoordinatePair = region[arbitraryIndex] 

    for coordinatePair in region:

        value = intensity2DImage[coordinatePair[0], coordinatePair[1]]
        if value > max:
            max = value
            maxCoordinatePair = coordinatePair

    return maxCoordinatePair


def cvToNumpy(cvImageTemp):
    a = zeros((cvImageTemp.height, cvImageTemp.width), dtype=int)
    for coordinateI in range(cvImageTemp.height):
        for coordinateJ in range(cvImageTemp.width):
            #print "width", cvImageTemp.width
            #print "height", cvImageTemp.height
            #print "i, j: ", (coordinateI, coordinateJ)
            #print cvImageTemp[coordinateI, coordinateJ][0]
            #print a[coordinateI, coordinateJ]
            a[coordinateI, coordinateJ] = cvImageTemp[coordinateI, coordinateJ][0]
            #if a[coordinateI, coordinateJ] < 0 or a[coordinateI, coordinateJ] > 255:
            #if a[coordinateI, coordinateJ] > 10:
            #    a[coordinateI, coordinateJ] = 10
            #print "grayscale value:", a[coordinateI, coordinateJ]
    return a



def boundingBoxTwoPoint(midPoint1, midPoint2):

    if midPoint1[0] < midPoint2[0]:
        xMin = midPoint1[0]
        xMax = midPoint2[0]
    else:
        xMin = midPoint2[0]
        xMax = midPoint1[0]
    if midPoint1[1] < midPoint2[1]:
        yMin = midPoint1[1]
        yMax = midPoint2[1]
    else:
        yMin = midPoint2[1]
        yMax = midPoint1[1]
        
    #(xMin, yMin) = midPoint1
    #(xMax, yMax) = midPoint2
    b1 = (xMin, yMin, xMax, yMax)
    return b1



def makeLabelVolume(inputVolume, oversegSource):

    if oversegSource == "watershed":
        labelVolume = makeLabelVolumeWatershed_depricated(inputVolume)
    if oversegSource == "file":
        path = "/home/rgiuly/images/overseg/"
        labelVolume = loadRawStack(path, box, swapXY=True, flipLR=True)

    return labelVolume



def writeInPlaneMultilayerGIF(fileFolder, imageVolume, boundingBox, zIndex, insidePoints, regionIDs):

    #filename = "crop_multi"
    filename = "crop"

    b = boundingBox
    b2 = array([b[1], b[0], b[3], b[2]])

    for id in regionIDs:
        filename += "_%s" % id

    filename += "_multi"

    #cvImages = [None, None, None]
    cvImages = []

    if zIndex > 0:
        cvImages.append(resizeCV(cropCV(toOpenCV(imageVolume[:, :, zIndex-1], color=True), b2), scaleFactor, color=True))

    cvImages.append(resizeCV(cropCV(toOpenCV(imageVolume[:, :, zIndex], color=True), b2), scaleFactor, color=True))

    if zIndex + 1 < imageVolume.shape[2]:
        cvImages.append(resizeCV(cropCV(toOpenCV(imageVolume[:, :, zIndex+1], color=True), b2), scaleFactor, color=True))

    print "insidePoints", insidePoints
    #scaleFactor = 1

    # draw dots
    for centerWithoutOffset in insidePoints:

        center = centerWithoutOffset - array([boundingBox[0], boundingBox[1]])

        cv.Circle(cvImages[1], (center[0] * scaleFactor, center[1] * scaleFactor), circleRadius, (255, 255, 255, 0), thickness=-1)
        cv.Circle(cvImages[1], (center[0] * scaleFactor, center[1] * scaleFactor), circleRadius+1, (0, 0, 0, 0), thickness=2)


    print "writing gif"
    animationFilename = os.path.join(fileFolder, addAnimationSuffix(filename) + ".gif")
    animationImages = []
    reversedList = list(cvImages)
    reversedList.reverse()
    # this goes through the list forwards the backwards
    for cvImageTemp in (cvImages[0:-1] + reversedList[0:-1]):
        #if cvImageTemp != None:
        a = cvToNumpy(cvImageTemp)
        animationImages.append(a)
    writeGif(animationFilename, animationImages, duration=1, dither=0)
    print animationFilename



def createCVImages_depricated_because_it_needs_whole_label_volume_in_memory(labelVolume):

    cvImages = []


    # function: makeTilesPlaneToPlane
    # for each XY image
    for z in range(labelVolume.shape[2]):

        # create open cv image
        currentLabelImageCV = toOpenCV(transpose(normalize2D(labelVolume[:, :, z], 255)), color=True)
        cvImages.append(currentLabelImageCV)
        edges = getEdges2D(labelVolume[:, :, z], z)

        # draw edges in images
        for key in edges:
            for point in edges[key]:
                #background = currentLabelImageCV[point[0], point[1]]
                background = (0, 0, 0, 0)
                color = (background[0], (background[1] + 255) / 2, background[2], 0)
                cv.Circle(currentLabelImageCV, (point[1], point[0]), 0, color)
                #print point

    return cvImages






def createCVImages(folder):

    #cvImages = []
    cvImages = {}


    # function: makeTilesPlaneToPlane
    # for each XY image
    #for z in range(labelVolume.shape[2]):

    numFiles = len(glob.glob(os.path.join(folder, "*.pickle")))
    startZ, stopZ = getStartAndStop(startSlice, stopSlice, numFiles)

    for z in range(startZ, stopZ):

        print "creating cv image with edges drawn %d" % z

        #filename = "output%03d.png" % z
        #currentLabelImage = numpy.transpose(scipy.misc.imread(os.path.join(folder, filename)))
        currentLabelImage = numpy.transpose(getSavedImage(folder, z, 'pickle'))

        # create open cv image
        currentLabelImageCV = toOpenCV(transpose(normalize2D(currentLabelImage, 255)), color=True)
        #cvImages.append(currentLabelImageCV)
        cvImages[z] = currentLabelImageCV
        edges = getEdges2D(currentLabelImage, z)

        # draw edges in images
        for key in edges:
            for point in edges[key]:
                #background = currentLabelImageCV[point[0], point[1]]
                background = (0, 0, 0, 0)
                color = (background[0], (background[1] + 255) / 2, background[2], 0)
                cv.Circle(currentLabelImageCV, (point[1], point[0]), 0, color)
                #print point

    return cvImages



def getPointsForZDecision(region1, region2):

    #todo: this is not an efficient way to handle the gaussian
    midPoint1 = getMaxPoint(region1,
                            scipy.ndimage.filters.gaussian_filter(numpy.transpose(getInputImage(args.input, region1.z)), 3.0))
    midPoint2 = getMaxPoint(region2,
                            scipy.ndimage.filters.gaussian_filter(numpy.transpose(getInputImage(args.input, region2.z)), 3.0))

    return (midPoint1, midPoint2)


def sigmoid(x):
  return 1 / (1 + math.exp(-x))



def getPointForDecisionInRegion(newRegion, existingRegionID, newRegionID, pointLocations):

    useDiagnostic = True

    #todo: this is not an efficient way to handle the gaussian
    image = scipy.ndimage.filters.gaussian_filter(numpy.transpose(getInputImage(args.input, newRegion.z)), 1.0)

    #edgeOfRegionImage = ones((image.shape[0], image.shape[1])) * 255
    edgeOfRegionImage = image

    contours = regionToContours(storageForRegionToContours, newRegion)
    # probably just one contour for this region but theoretically there could be more than one
    print "contours for new region:", contours
    print "shape:", image.shape
    for c in contourIterator(contours):
        points = []
        for point in c:
            points.append((point[1], point[0]))
            #edgeOfRegionImage[point[0], point[1]] = 0

        lastPoint = points[-1]
        for point in points:
            #cv2.line(edgeOfRegionImage, point, lastPoint, (128, 128, 128, 0), thickness=14)
            cv2.line(edgeOfRegionImage, point, lastPoint, (0, 0, 0, 0), thickness=10)
            lastPoint = point

    edgeOfRegionImage = scipy.ndimage.filters.gaussian_filter(edgeOfRegionImage, 6.0)

 
    #if useDiagnostic:
    #    fullPath = os.path.join(outputFolder, "tiles", "plane_to_plane_diagnostic", "image_%s.jpg" % newRegionID)
    #    scipy.misc.imsave(fullPath, image)
    #    print fullPath

    
    if useDiagnostic:
        #diagnosticImage = (image + edgeOfRegionImage) / 2.0
        diagnosticImage = edgeOfRegionImage
        fullPath = os.path.join(outputFolder, "tiles", "plane_to_plane_diagnostic", "image_%s_faded_edge.jpg" % newRegionID)
        scipy.misc.imsave(fullPath, diagnosticImage)
        print fullPath


    max = -1000000000000000000000000000000000

    diagnosticValues = []

    # search for best point in region
    for coordinatePair in newRegion:



        dist = numpy.linalg.norm(array(pointLocations[existingRegionID]) - array(coordinatePair))

        # brighter is better and closer is better
        # distance subtracts from score, up to maxDistancePenalty
        #maxDistancePenalty = 50
        #intensityValue = sigmoid((image[coordinatePair[0], coordinatePair[1]]-128)/10.0) * 255.0
        #intensityValue = image[coordinatePair[0], coordinatePair[1]]
        intensityValue = edgeOfRegionImage[coordinatePair[0], coordinatePair[1]]
        #contourBoundaryProximityValue = edgeOfRegionImage[coordinatePair[0], coordinatePair[1]]
        # effectively, this will ignore distance if it's already pretty close
        #if dist < 40.0:
        #    dist = 40.0
        value = intensityValue - (float(dist) / 60.0)# - min(dist/2.8, maxDistancePenalty)# + (contourBoundaryProximityValue * 1.0)

        diagnosticValues.append((coordinatePair, value))

        if value > max:
            max = value
            bestCoordinatePair = coordinatePair

    #pointLocations[newRegionID] = bestCoordinatePair

    return (bestCoordinatePair, diagnosticValues)



def getPointsForZDecision_test_version(edge, pointLocations):

    """returns (point0, point1, newRegionID)"""


    if edge[0] in pointLocations and edge[1] not in pointLocations:
        existingRegionID = edge[0]
        newRegionID = edge[1]
        existingCoordinatePair = pointLocations[edge[0]]
        existingRegionFirst = True
    elif edge[0] not in pointLocations and edge[1] in pointLocations:
        newRegionID = edge[0]
        existingRegionID = edge[1]
        existingCoordinatePair = pointLocations[edge[1]]
        existingRegionFirst = False
    elif edge[0] in pointLocations and edge[1] in pointLocations:
        print "warning: both already have regions already have locations, expected just one"
        return (pointLocations[edge[0]], pointLocations[edge[1]], None)
    elif edge[0] not in pointLocations and edge[1] not in pointLocations:
        raise Exception("expects to have one node of the edge with a defined point location, neither has a location")
    else:
        raise Exception("error")


    newRegion = getRegionByID(cursor, newRegionID)

    (bestCoordinatePair, diagnosticValues) = getPointForDecisionInRegion(newRegion, existingRegionID, newRegionID, pointLocations)

    if existingRegionFirst:
        return (existingCoordinatePair, bestCoordinatePair, newRegionID, diagnosticValues)
    else:
        return (bestCoordinatePair, existingCoordinatePair, newRegionID, diagnosticValues)




#def makeZDecisionImage(allRegions, cvImages, key, useCenterPoints):
def makeZDecisionImage(key, useCenterPoints, pointLocations, baseFilename="crop"):
    """key is an edge represented as a list with form (regionID, regionID)"""

    creatingImage = False

    generateDiagnostic = True

    #print "number of adjacencies for plane to plane", numProcessed, "total number", len(zEdges)
    #print "number of adjacencies processed for plane to plane", numProcessed, "total number", len(zEdges)

    z = [None, None]
    #regionsAtZ = [None, None]
    #regionIndexes = [None, None]

    print "key", key

    #((z[0], regionIndexes[0]), (z[1], regionIndexes[1])) = key
    regionIDs = key
    #region0 = allRegions[regionIDs[0]]
    #region1 = allRegions[regionIDs[1]]
    region0 = getRegionByID(cursor, regionIDs[0])
    region1 = getRegionByID(cursor, regionIDs[1])
    z[0] = region0.z
    z[1] = region1.z
    regions = [region0, region1]

    #regionsAtZ[0] = regionStack[z[0]]
    #regionsAtZ[1] = regionStack[z[1]]
    #regions = [regionsAtZ[0][regionIndexes[0]], regionsAtZ[1][regionIndexes[1]]]

    useBoxAroundARegion = False


    #function: makeTilesPlaneToPlane
    if useBoxAroundARegion:
        b1 = array(boundingBox(regions[0]))
        borderSize = 180
    else:
        #midPoint1 = getPointInside(regions[0])
        #midPoint2 = getPointInside(regions[1])
        ##midPoint1 = getMaxPoint(regions[0], gaussian[:, :, z[0]])
        ##midPoint2 = getMaxPoint(regions[1], gaussian[:, :, z[1]])
        print "z[0]", z[0]
        print "z[1]", z[1]
        print "start get image for mid point"


        #todo: write this to a diagnostic image to see if it matches the input images
        #midPoint1 = getMaxPoint(regions[0], numpy.transpose(getImageStandardFilename(gaussianDataOutputFolder, z[0])))
        #midPoint2 = getMaxPoint(regions[1], numpy.transpose(getImageStandardFilename(gaussianDataOutputFolder, z[1])))

        if useGetPointsForZDecisionTestVersion:
            (midPoint1, midPoint2, regionIDForDiagnosticValues, diagnosticValues) = getPointsForZDecision_test_version(regionIDs, pointLocations)
        else:
            (midPoint1, midPoint2, diagnosticImage) = getPointsForZDecision(regions[0], regions[1])

        print "finished image image for mid point"
        b1 = boundingBoxTwoPoint(midPoint1, midPoint2)
        #borderSize = 65
        #borderSize = 100
        borderSize = 120


    midPoints = [midPoint1, midPoint2]


    # add border
    b = b1 + array([-borderSize, -borderSize, borderSize, borderSize])
    #b = b1


    (xMin, yMin, xMax, yMax) = b
    biggestLength = max(double(xMax - xMin), double(yMax - yMin))
    print "biggest length", biggestLength
    scaleFactor = 700.0 / biggestLength
    print "scale factor", scaleFactor



    croppedRaw = [None, None]
    cropped = [None, None]


    #inside = True
    #for imageNumber in range(0, 2):
    #    if not(isBoxInside(v.shape[1], v.shape[0], b)):
    #        inside = False
    #print v.shape[1], v.shape[0], b, inside

    #function: makeTilesPlaneToPlane
    #if inside:
    if 1:
        for imageNumber in range(0, 2):

            # extract a a tile from the full image
            # b is a bounding box around the current edge
            # croppedCV returns None if the cropped region doesn't fit in the full image

            ##transposedImage = transpose(v[:, :, z[imageNumber]])
            #print "loading original image"
            transposedImage = getImageStandardFilename(originalDataOutputFolder, z[imageNumber])


            #testImage = scipy.ndimage.filters.gaussian_filter(numpy.transpose(getInputImage(args.input, z[imageNumber])), 1.0)


            #print "finished loading original image"
            #print "dimension check"
            #print toOpenCV(transposedImage, color=True).width, "=", v.shape[1]
            #print toOpenCV(transposedImage, color=True).height, "=", v.shape[0]

            #print "toOpenCV"
            croppedRaw[imageNumber] = cropCV(toOpenCV(normalize2D(transposedImage, 255), color=True), b)
            print "-----------------"
            #xx = cropCV(toOpenCVTest(normalize2D(transposedImage, 255), color=True), b)
            #print croppedRaw[imageNumber] == xx
            #for iii in range(10):
            #    for jjj in range(10):
            #        print "--"
            #        print croppedRaw[imageNumber][iii, jjj]
            #        print xx[iii, jjj]
            #sys.exit()
            print "finished toOpenCV"
            #if generateDiagnostic: cropped[imageNumber] = cropCV(cvImages[z[imageNumber]], b)
            #temporarily pulling this out
            if generateDiagnostic: cropped[imageNumber] = cropCV(toOpenCV(normalize2D(transposedImage, 255), color=True), b)
            #if generateDiagnostic: cropped[imageNumber] = cropCV(toOpenCV(normalize2D(testImage, 255), color=True), b)

            #print "croppedRaw", croppedRaw[imageNumber]
            #print "cropped", cropped[imageNumber]

            if croppedRaw[imageNumber]: croppedRaw[imageNumber] = resizeCV(croppedRaw[imageNumber], scaleFactor, color=True)
            else: croppedRaw[imageNumber] = None
            #print "hello"

            if generateDiagnostic:
                if cropped[imageNumber]: cropped[imageNumber] = resizeCV(cropped[imageNumber], scaleFactor, color=True)
                else: cropped[imageNumber] = None


        # if there's a cropped region, draw dot on the cropped region
        #print "cropped[0]", cropped[0]
        #print "cropped[1]", cropped[1]
        ##if cropped[0] != None and cropped[1] != None:
        if croppedRaw[0] != None and croppedRaw[1] != None:

            for imageNumber in range(0, 2):
                if 1:
                    if generateDiagnostic:
                        # fill in regions for diagnostic images
                        diagnosticColors = ((255, 255, 0, 0), (255, 0, 255, 0))
                        for rawPoint in regions[imageNumber]:
                            #print "raw point", rawPoint
                            point = array(rawPoint) - array([b[0], b[1]])
                            cv.Circle(cropped[imageNumber], (int(point[1] * scaleFactor), int(point[0] * scaleFactor)), circleRadius, diagnosticColors[imageNumber], thickness=-1)

                        print "check for match:", regionIDs[imageNumber], regionIDForDiagnosticValues
                        if regionIDs[imageNumber] == regionIDForDiagnosticValues:
                            for rapPointValue in diagnosticValues:
                                rawPoint, v = rawPointValue
                                point = array(rawPoint) - array([b[0], b[1]])
                                cv.Circle(cropped[imageNumber], (int(point[1] * scaleFactor), int(point[0] * scaleFactor)), circleRadius, (v, v, v, 0), thickness=-1)

    
                    # draw dot
                    if useCenterPoints:
                        ##centerWithoutOffset = averagePoint2D(regions[imageNumber])
                        ###print "regions[imageNumber]", regions[imageNumber]
                        ##print "centerWithoutOffset", tuple(centerWithoutOffset)
                        ##isInsideTheRegion = tuple(centerWithoutOffset) in regions[imageNumber]
                        ##print "centerWithoutOffset in regions[imageNumber]", isInsideTheRegion
                        ##if not(isInsideTheRegion):
                        ##    centerWithoutOffset = choice(regions[imageNumber])
                        ##    print "changing to centerWithoutOffset:", centerWithoutOffset
                        #centerWithoutOffset = getPointInside(regions[imageNumber])
                        centerWithoutOffset = midPoints[imageNumber]
                        center = centerWithoutOffset - array([b[0], b[1]])
                        if generateDiagnostic: cv.Circle(cropped[imageNumber], (int(center[1] * scaleFactor), int(center[0] * scaleFactor)), 4, (0, 0, 255, 0), thickness=-1)
                        cv.Circle(croppedRaw[imageNumber], (int(center[1] * scaleFactor), int(center[0] * scaleFactor)), circleRadius, (255, 255, 255, 0), thickness=-1)
                        cv.Circle(croppedRaw[imageNumber], (int(center[1] * scaleFactor), int(center[0] * scaleFactor)), circleRadius+1, (0, 0, 0, 0), thickness=2)
    
    
                    # write the current tile to file
                    filename = baseFilename
        
                    for id in regionIDs:
                        filename += "_%s" % id
        
                    extension = ".jpg"
                    planeToPlaneDiagnosticTileFolder = os.path.join(tileFolder, "plane_to_plane_diagnostic")
                    planeToPlaneTileFolder = os.path.join(tileFolder, "plane_to_plane")
                    makeDirectory(planeToPlaneTileFolder)
                    makeDirectory(planeToPlaneDiagnosticTileFolder)
                    fullFilename = os.path.join(planeToPlaneDiagnosticTileFolder, filename + "_" + str(imageNumber) + "_diagnostic" + extension)
                    fullFilenameRaw = os.path.join(planeToPlaneDiagnosticTileFolder, filename + "_" + str(imageNumber) + "_raw" + extension)

                    if imageNumber == 0:
                        resultFilename = filename
                        #fileList.append(filename)

                    creatingImage = True
                    print fullFilename
                    if generateDiagnostic:
                        print "saving diagnostic image", fullFilename
                        cv.SaveImage(fullFilename, cropped[imageNumber])
                    cv.SaveImage(fullFilenameRaw, croppedRaw[imageNumber])


            print "writing gif"
            #contrast = 1.0
            animationFilename = os.path.join(planeToPlaneTileFolder, addAnimationSuffix(filename) + ".gif")
            animationImages = []
            for cvImageTemp in croppedRaw:
                ##pilImage = CVToPIL(cvImageTemp, color=True)
                ##gifImage = pilImage.convert('RGB').convert('P', palette=Image.ADAPTIVE)
                ##print "gifImage", gifImage
                #animationImages.append(255 - numpy.asarray(gifImage))
                #print numpy.asarray(gifImage)
                a = cvToNumpy(cvImageTemp)
                animationImages.append(a)
            writeGif(animationFilename, animationImages, duration=0.5, dither=0)
            print animationFilename

            #print "image count", i
            #if i >=10: break
            #if makeQualifications:
            #    if i >= 60*2: break


    return (creatingImage, resultFilename)


# crop and allows for the crop frame to go outside of the input image (it will end up white)
def cropArray(inputArray, b):

    (xMin, yMin, xMax, yMax) = b

    outputArray = 255 * ones((xMax-xMin, yMax-yMin))

    if xMin < 0:
        xOffset = -xMin
        xInputMin = 0
    else:
        xOffset = 0
        xInputMin = xMin

    if yMin < 0:
        yOffset = -yMin
        yInputMin = 0
    else:
        yOffset = 0
        yInputMin = yMin

    rawCrop = inputArray[xInputMin:xMax, yInputMin:yMax]
    length = rawCrop.shape[0]
    height = rawCrop.shape[1]

    outputArray[xOffset:xOffset+length, yOffset:yOffset+height] = rawCrop

    return outputArray



def splitRegion(regionID):

    generateDiagnostic = True

    region = getRegionByID(cursor, regionID)
    z = region.z
    newSplitDepth = region.splitDepth + 1
    # using 0.1 to make this work but it's a hack, it shouldn't be needed
    newLevel = float(args.level) - (newSplitDepth * 0.025)
    print "new level:", newLevel

    b1 = array(boundingBox(region))
    borderSize = 120

    # add border
    b = b1 + array([-borderSize, -borderSize, borderSize, borderSize])

    (xMin, yMin, xMax, yMax) = b
    biggestLength = max(double(xMax - xMin), double(yMax - yMin))


    print "loading original image"
    transposedImage = getImageStandardFilename(originalDataOutputFolder, z)
    image = numpy.transpose(transposedImage)
    cropped = cropArray(image, b)
    #cropped = cropCV(toOpenCV(normalize2D(transposedImage, 255), color=True), b)


    folder = os.path.join(tileFolder, "regions")

    # perform watershed
    # extract regions from watershed (only within the original region)
    print os.path.join(folder, "test_cropped.png")
    print "cropped:", os.path.join(folder, "test_cropped.png")
    print "cropped dimensions:", cropped.shape
    print "x", xMin, xMax, "y", yMin, yMax
    scipy.misc.imsave(os.path.join(folder, "test_cropped.png"), cropped)
    #watershed = watershed2DNumpy(cropped, 0.00015, .5, useGradientMagnitude=False)

    # this make leak memory
    #for levelIndex in range(0, 15):
    #    newLevelTest = levelIndex * 0.025
    #    for thresholdIndex in range(0, 10):
    #        thresholdTest = .00015 + thresholdIndex * 0.01
    #        watershed = watershed2DNumpyRaw(scipy.ndimage.filters.gaussian_filter(cropped, 4.0), thresholdTest, newLevelTest, useGradientMagnitude=False)
    #        print os.path.join(outputFolder, "test_watershed_%f_%f.png" % (thresholdTest, newLevelTest))
    #        scipy.misc.imsave(os.path.join(outputFolder, "test_watershed_%f_%f.png" % (thresholdTest, newLevelTest)), watershed)


    # this make leak memory
    #watershed = watershed2DNumpyRaw(scipy.ndimage.filters.gaussian_filter(cropped, 4.0), .00015, newLevel, useGradientMagnitude=False)
    watershed = watershed2DNumpyRaw(cropped, .00015, newLevel, useGradientMagnitude=False)
    scipy.misc.imsave(os.path.join(folder, "test_watershed.png"), watershed)
    print "watershed:", os.path.join(folder, "test_watershed.png")


    dict = {}

    # for point in region, check the value in watershed and use it as a key to a new region
    for point in region:
        pointInCroppedImage = array(point) - array([b[0], b[1]])
        index = watershed[pointInCroppedImage[0], pointInCroppedImage[1]]
        if index in dict:
            dict[index].append(point)
        else:
            newRegion = graph_util.Region2D()
            newRegion.z = region.z
            newRegion.splitDepth = newSplitDepth
            newRegion.append(point)
            dict[index] = newRegion

    newRegions = []
    for region in dict.values():
        newRegions.append(region)

    return newRegions



def makeRegionImageUsingID(regionID, baseFilename="region"):

    region = getRegionByID(cursor, regionID)

    return makeRegionImage(region, name=regionID, baseFilename=baseFilename)



def makeRegionImage(region, name="untitled", baseFilename="region"):

    regionID = name

    z = region.z

    generateDiagnostic = True

    b1 = array(boundingBox(region))
    borderSize = 120

    # add border
    b = b1 + array([-borderSize, -borderSize, borderSize, borderSize])

    (xMin, yMin, xMax, yMax) = b
    biggestLength = max(double(xMax - xMin), double(yMax - yMin))
    print "biggest length", biggestLength
    scaleFactor = 700.0 / biggestLength
    print "scale factor", scaleFactor


    print "loading original image"
    transposedImage = getImageStandardFilename(originalDataOutputFolder, z)
    print "finished loading original image"
    print "toOpenCV"
    croppedRaw = cropCV(toOpenCV(normalize2D(transposedImage, 255), color=True), b)
    print "-----------------"
    print "finished toOpenCV"
    if generateDiagnostic: cropped = cropCV(toOpenCV(normalize2D(transposedImage, 255), color=True), b)

    if croppedRaw:
        croppedRaw = resizeCV(croppedRaw, scaleFactor, color=True)
        success = True
    else:
        croppedRaw = None
        success = False

    if generateDiagnostic:

        if cropped:

            # render region
            for rawPoint in region:
    
                #print "raw point", rawPoint
                point = array(rawPoint) - array([b[0], b[1]])
                intensity = cropped[point[0], point[1]][0]
                #intensity = 100
                #print "intensity", intensity
                regionIntensity = 0.3
                background = 1.0 - regionIntensity
                backgroundFactor = float(intensity) / float(255) # fade out color in black places
                diagnosticColor = (regionIntensity*255*backgroundFactor + background*intensity, regionIntensity*255*backgroundFactor + background*intensity, background*intensity)
                #cv.Circle(cropped, (point[1], point[0]), circleRadius, (255, 0, 0, 0), thickness=-1)
                cropped[point[0], point[1]] = diagnosticColor
    
            # resize image
            cropped = resizeCV(cropped, scaleFactor, color=True)

        else:

            cropped = None



        if croppedRaw != None:
    
            # write the current tile to file
            filename = baseFilename

            filename += "_%s" % regionID

            extension = ".jpg"
            regionsDiagnosticTileFolder = os.path.join(tileFolder, "regions_diagnostic")
            regionsTileFolder = os.path.join(tileFolder, "regions")
            makeDirectory(regionsTileFolder)
            makeDirectory(regionsDiagnosticTileFolder)
            fullFilename = os.path.join(regionsTileFolder, filename + extension)
            fullFilenameRaw = os.path.join(regionsDiagnosticTileFolder, filename + "_raw" + extension)

            resultFilename = filename

            creatingImage = True
            print fullFilename
            print "saving image", fullFilename
            cv.SaveImage(fullFilename, cropped)
            cv.SaveImage(fullFilenameRaw, croppedRaw)


    return (success, resultFilename)




def getComponentGroups(gr):

    componentsDict = pygraph.algorithms.accessibility.connected_components(gr)

    for regionID in componentsDict:

        groupID = componentsDict[regionID]

        # if a group does not exist yet, create it
        if not(groupID in componentGroups):
            componentGroups[groupID] = []

        # add regionID to the group
        componentGroups[groupID].append(regionID)



def makeZDecisionImage2_depricated(gr, regionIDs, useCenterPoints):

    creatingImage = False

    generateDiagnostic = False

    #print "number of adjacencies for plane to plane", numProcessed, "total number", len(zEdges)
    #print "number of adjacencies processed for plane to plane", numProcessed, "total number", len(zEdges)

    z = [None, None]
    #regionsAtZ = [None, None]
    #regionIndexes = [None, None]


    #((z[0], regionIndexes[0]), (z[1], regionIndexes[1])) = key
    print regionIDs
    #region0 = allRegions[regionIDs[0]]
    #region1 = allRegions[regionIDs[1]]

    #todo: important, could be multiple isolated regions of the super region on a given plane, rip out all of them unless they are connected in the two planes under evaluation. so, use the graph library to get all transitive connections, rip out all of the nodes that are on the wrong plane (not on one of the two), and do connected components again to get components. then pick the component that is actually touching the existing node.


    if not gr.has_node(regionIDs[0]) and gr.has_node(regionIDs[1]):
        newRegionID = regionIDs[0]
        existingRegionID = regionIDs[1]

    if not gr.has_node(regionIDs[1]) and gr.has_node(regionIDs[0]):
        newRegionID = regionIDs[1]
        existingRegionID = regionIDs[0]

    if not gr.has_node(regionIDs[1]) and not gr.has_node(regionIDs[0]):
        return makeZDecisionImage(regionIDs, useCenterPoints)

    # build super region associated with existing node
    #componentGroups = getComponentsGroups(gr)
    #for groupID in componentGroups:
    #    if existingRegionID in componentGroups[groupID]:
    #        superRegionGroup

    #region0 = getRegionByID(regionIDs[0])
    #region1 = getRegionByID(regionIDs[1])

    newRegion = getRegionByID(newRegionID)
    existingRegion = getRegionByID(existingRegionID)

    superRegionInPlane = []
    for regionID in gr.nodes():
        r = getRegionByID(regionID)
        if existingRegion.z == r.z:
            superRegionInPlane += getRegionByID(regionID)


    z[0] = existingRegion.z
    z[1] = newRegion.z
    regions = [superRegionInPlane, newRegion]

    #regionsAtZ[0] = regionStack[z[0]]
    #regionsAtZ[1] = regionStack[z[1]]
    #regions = [regionsAtZ[0][regionIndexes[0]], regionsAtZ[1][regionIndexes[1]]]

    useBoxAroundARegion = False


    #function: makeTilesPlaneToPlane
    if useBoxAroundARegion:
        #b1 = array(boundingBox(regions[0]))
        #borderSize = 180
        raise Exception("depricated use box around region")
    else:
        #midPoint1 = getPointInside(regions[0])
        #midPoint2 = getPointInside(regions[1])
        ##midPoint1 = getMaxPoint(regions[0], gaussian[:, :, z[0]])
        ##midPoint2 = getMaxPoint(regions[1], gaussian[:, :, z[1]])
        print "z[0]", z[0]
        print "z[1]", z[1]
        midPoint1 = getMaxPoint(regions[0], numpy.transpose(getImage(gaussianOutputFolder, z[0])))
        midPoint2 = getMaxPoint(regions[1], numpy.transpose(getImage(gaussianOutputFolder, z[1])))
        b1 = boundingBoxTwoPoint(midPoint1, midPoint2)
        #borderSize = 65
        borderSize = 100


    midPoints = [midPoint1, midPoint2]

    # add border
    b = b1 + array([-borderSize, -borderSize, borderSize, borderSize])
    #b = b1

    croppedRaw = [None, None]
    cropped = [None, None]


    #inside = True
    #for imageNumber in range(0, 2):
    #    if not(isBoxInside(v.shape[1], v.shape[0], b)):
    #        inside = False
    #print v.shape[1], v.shape[0], b, inside

    #function: makeTilesPlaneToPlane
    #if inside:
    if 1:
        for imageNumber in range(0, 2):

            # extract a a tile from the full image
            # b is a bounding box around the current edge
            # croppedCV returns None if the cropped region doesn't fit in the full image

            ##transposedImage = transpose(v[:, :, z[imageNumber]])
            transposedImage = getImage(originalOutputFolder, z[imageNumber])
            #print "dimension check"
            #print toOpenCV(transposedImage, color=True).width, "=", v.shape[1]
            #print toOpenCV(transposedImage, color=True).height, "=", v.shape[0]

            croppedRaw[imageNumber] = cropCV(toOpenCV(normalize2D(transposedImage, 255), color=True), b)
            if generateDiagnostic: cropped[imageNumber] = cropCV(cvImages[z[imageNumber]], b)

            #print "croppedRaw", croppedRaw[imageNumber]
            #print "cropped", cropped[imageNumber]

            if croppedRaw[imageNumber]: croppedRaw[imageNumber] = resizeCV(croppedRaw[imageNumber], scaleFactor, color=True)
            else: croppedRaw[imageNumber] = None
            #print "hello"

            if generateDiagnostic:
                if cropped[imageNumber]: cropped[imageNumber] = resizeCV(cropped[imageNumber], scaleFactor, color=True)
                else: cropped[imageNumber] = None


        # if there's a cropped region, draw dot on the cropped region
        #print "cropped[0]", cropped[0]
        #print "cropped[1]", cropped[1]
        ##if cropped[0] != None and cropped[1] != None:
        if croppedRaw[0] != None and croppedRaw[1] != None:

            for imageNumber in range(0, 2):
                if 1:

                    # draw dot
                    if useCenterPoints:
                        ##centerWithoutOffset = averagePoint2D(regions[imageNumber])
                        ###print "regions[imageNumber]", regions[imageNumber]
                        ##print "centerWithoutOffset", tuple(centerWithoutOffset)
                        ##isInsideTheRegion = tuple(centerWithoutOffset) in regions[imageNumber]
                        ##print "centerWithoutOffset in regions[imageNumber]", isInsideTheRegion
                        ##if not(isInsideTheRegion):
                        ##    centerWithoutOffset = choice(regions[imageNumber])
                        ##    print "changing to centerWithoutOffset:", centerWithoutOffset
                        #centerWithoutOffset = getPointInside(regions[imageNumber])
                        centerWithoutOffset = midPoints[imageNumber]
                        center = centerWithoutOffset - array([b[0], b[1]])
                        if generateDiagnostic: cv.Circle(cropped[imageNumber], (center[1] * scaleFactor, center[0] * scaleFactor), 4, (0, 0, 255, 0), thickness=-1)
                        cv.Circle(croppedRaw[imageNumber], (center[1] * scaleFactor, center[0] * scaleFactor), circleRadius, (255, 255, 255, 0), thickness=-1)
                        cv.Circle(croppedRaw[imageNumber], (center[1] * scaleFactor, center[0] * scaleFactor), circleRadius+1, (0, 0, 0, 0), thickness=2)
    
    
                    # write the current tile to file
                    filename = "crop"
        
                    for id in regionIDs:
                        filename += "_%s" % id
        
                    extension = ".jpg"
                    planeToPlaneDiagnosticTileFolder = os.path.join(tileFolder, "plane_to_plane_diagnostic")
                    planeToPlaneTileFolder = os.path.join(tileFolder, "plane_to_plane")
                    makeDirectory(planeToPlaneTileFolder)
                    makeDirectory(planeToPlaneDiagnosticTileFolder)
                    fullFilename = os.path.join(planeToPlaneDiagnosticTileFolder, filename + "_" + str(imageNumber) + extension)
                    fullFilenameRaw = os.path.join(planeToPlaneDiagnosticTileFolder, filename + "_" + str(imageNumber) + "_raw" + extension)

                    if imageNumber == 0:
                        resultFilename = filename
                        #fileList.append(filename)

                    creatingImage = True
                    print fullFilename
                    if generateDiagnostic: cv.SaveImage(fullFilename, cropped[imageNumber])
                    cv.SaveImage(fullFilenameRaw, croppedRaw[imageNumber])


            print "writing gif"
            #contrast = 1.0
            animationFilename = os.path.join(planeToPlaneTileFolder, addAnimationSuffix(filename) + ".gif")
            animationImages = []
            for cvImageTemp in croppedRaw:
                ##pilImage = CVToPIL(cvImageTemp, color=True)
                ##gifImage = pilImage.convert('RGB').convert('P', palette=Image.ADAPTIVE)
                ##print "gifImage", gifImage
                #animationImages.append(255 - numpy.asarray(gifImage))
                #print numpy.asarray(gifImage)
                a = cvToNumpy(cvImageTemp)
                animationImages.append(a)
            writeGif(animationFilename, animationImages, duration=0.5, dither=0)
            print animationFilename

            #print "image count", i
            #if i >=10: break
            #if makeQualifications:
            #    if i >= 60*2: break


    return (creatingImage, resultFilename)






def makeTilesPlaneToPlane(outputCSVFilename, useEdges=False, useCenterPoints=False, oversegSource="watershed"):

    examples = ""
    questions = ""
    answersText = ""

    labelVolumeFolder = os.path.join(outputFolder, "labelVolume")
    if not(os.path.isdir(labelVolumeFolder)): os.mkdir(labelVolumeFolder)

    labelVolume = makeLabelVolume(v, oversegSource)
    #labelVolume = makeLabelVolumeSLIC(v)

    writeStack(labelVolumeFolder, labelVolume)
    #sys.exit()

    # image is the label image (not used in this method)
    # todo: cvImage and tempImage are redundant
    zEdges = getZEdges(labelVolume)
    #print edges

    allRegions = getAllRegions(labelVolume)

    usedEdges = {}
    #i = 0
    fileList = []


    cvImages = createCVImages(labelVolume)


    # for each edge between supervoxels
    print "zEdges", zEdges

    numProcessed = 0


    # create images that will represent the decision of each possible edge
    for key in zEdges:
        (success, filename) = makeZDecisionImage(allRegions, cvImages, key, useCenterPoints)
        if success:
            numProcessed += 1
            fileList.append(filename)

        #todo: this has not been tested
        if makeQualifications:
            if numProcessed >= 60: break


    return fileList



def getAnswers(HITId, max_assignments):

    answerList = []

    while True:
        try:
            results = access_aws.mtc.get_assignments(HITId)
            break
        except:
            print "could not get assignments for %s, trying again in a minute..."
            time.sleep(60)
            

    # if there's an answer
    #print "checking HIT:", hit.HITId, " number of answers so far:", len(results)
    if len(results) == max_assignments or max_assignments == None:
        for assignment in results:
            #print dir(assignment)
            #print "answer", assignment.answers[0]
            for questionFormAnswer in assignment.answers[0]:
                print "qid", questionFormAnswer.qid
                value = questionFormAnswer.fields[0]
                print "value", value
                answerList.append(str(value))
        return answerList
    else:
        return None

            #ans = {}
            #for j in assignment.answers[0]:
            #    if j.qid!='commit': ans[j.qid] = j.fields[0].split('/')[-1]
            #print assignment.AssignmentId, assignment.WorkerId, ans['image1']
            #resultDict = {'AssignmentId':[assignment.AssignmentId], 'WorderID':assignment.WorkerId, 'Song1':ans['song1'], 'Song2':ans['song2'], 'Answer':ans['boxradio']}


def adjacentEdges(edges, edge):

    result = []

    for currentEdge in edges:
        if (currentEdge[0] == edge[1] or
            currentEdge[1] == edge[0] or
            currentEdge[0] == edge[0] or
            currentEdge[1] == edge[1]):
                result.append(currentEdge)

    return result



def adjacentRegions(edges, regionID):

    result = []

    for currentEdge in edges:
        #print "current edge:", currentEdge
        if (regionID == currentEdge[1]): result.append(currentEdge[0])
        if (regionID == currentEdge[0]): result.append(currentEdge[1])

    return result



def edgesAdjToRegion(regionID, edges, verbose=False):

    result = []

    print "searching for an edge that has region", regionID

    for currentEdge in edges:
        if verbose: print "region: %s edge: %s" % (regionID, str(currentEdge))
        #try:
        if (regionID == currentEdge[1]): result.append(currentEdge)
        if (regionID == currentEdge[0]): result.append(currentEdge)
        #except:
        #    print "current edge", currentEdge

    print "found", result

    return result





def regionsTouchingPoints_old(regionCursor, startPoints):

    touchingRegions = []

    # for each region
    while True:
    #for key in regions:
        #print key
        #zPlane, number = regionIdentifierToNumbers(key)
        #region = regions[key]
        r = fetchRegion(regionCursor) # could just fetch z first to see if the plane is needed
        if r == None: break
        zPlane, number, region = r

        # for each start point, check if this region touches
        for startPoint3D in startPoints:
            print "start point 3D", startPoint3D, "region", zPlane, number
            if zPlane != startPoint3D[2]:
                continue
            for point in region:
                print point, startPoint3D
                if startPoint3D[0] == point[0] and startPoint3D[1] == point[1]:
                    #touchingRegions.append(key)
                    touchingRegions.append(makeRegionIdentifier(zPlane, number))

    return touchingRegions




def regionsTouchingPoints(startPoints):

    touchingRegions = []
    #inputFileExtension = "pickle"

    for point in startPoints:

        z = point[2]
        print "getting region for point", point
        image = getSavedImage(initialSegFolder, z, initSegFilenameFormat, initSegFileType)
        print "image shape", image.shape
        #print image
        number = image[point[1], point[0]]
        id = makeRegionIdentifier(z, number)
        print "region id:", id
        touchingRegions.append(id)

    return touchingRegions


def getStartPoints():

    startPoints = []
    #height = labelVolume.shape[1]
    for startPointIMOD in startPointsIMOD:
        startPoints.append((startPointIMOD[0], imageHeight - startPointIMOD[1], startPointIMOD[2] - 1))

    return startPoints


def initializeRequestLoop():

    print "initializing request loop"


    #dict = shelve.open(filename)
    dict = {}

    gr = graph()
    dict['gr'] = gr

    #labelVolume = makeLabelVolume(v, oversegSourceForQualAndProcessAndRender)

    #dict['labelVolume'] = labelVolume
    ##allRegions = getAllRegions(labelVolume)
    ##dict['allRegions'] = allRegions

    startPoints = getStartPoints()


    #startRegions = regionsTouchingPoints(allRegions, startPoints)
    print "finding regions touching start points"
    #startRegions = regionsTouchingPoints(getCursorForRegions(), startPoints)
    startRegions = regionsTouchingPoints(startPoints)
    print "start regions:", startRegions

    # place point locations on the start regions
    dict['pointLocations'] = {}
    for i in range(len(startRegions)):
        dict['pointLocations'][startRegions[i]] = startPoints[i][0:2]


    ##labelVolumeFolder = os.path.join(outputFolder, 'labelVolume')
    ##if not(os.path.isdir(labelVolumeFolder)): os.mkdir(labelVolumeFolder)
    #labelVolume = makeLabelVolume(v, oversegSource)
    #writeStack(labelVolumeFolder, labelVolume)
    #zEdges = getZEdges(labelVolume)

    #if initSegFromPrecomputedStack:
    #    zEdges = getZEdges(fileExtension="mha")
    #else:
    #    zEdges = getZEdges(fileExtension="pickle")
    #dict['zEdges'] = zEdges

    #print "first 100 zEdges"
    #allRegions = getAllRegions(labelVolume)
    #usedEdges = {}
    #fileList = []

    zEdgesFile = open(os.path.join(outputFolder, "zEdges.pickle"), 'rb')
    zEdges = cPickle.load(zEdgesFile)
    zEdgesFile.close()

    nodeCreationTime = {}

    startEdges = []
    for e in zEdges:
        for key in startRegions:
            if e[0] == key or e[1] == key:
                startEdges.append(e)
                nodeCreationTime[e[0]] = time.time()
                nodeCreationTime[e[1]] = time.time()

    print "start edges", startEdges
    dict['startEdges'] = startEdges
    dict['startRegions'] = startRegions

    numProcessed = 0

    edgesToBeEvaluated = list(startEdges)
    dict['edgesToBeEvaluated'] = edgesToBeEvaluated
    hitCreated = {} # True for created, not in the dictionary means it's not created
    dict['regionsToBeEvaluated'] = []
    dict['hitCreated'] = hitCreated
    hitID = {}
    dict['hitID'] = hitID
    hitEvaluated = {} # True for evaluated, not in the dictionary means it's not created
    dict['hitEvaluated'] = hitEvaluated
    hitAnswer = {}
    dict['hitAnswer'] = hitAnswer
    dict['nodeCreationTime'] = nodeCreationTime
    poisoned = {}
    dict['poisoned'] = poisoned

    dict['possibleUndersegRegionDict'] = {}


    filename = os.path.join(outputFolder, "request_loop_data")
    file = open(filename, 'wb')

    #dict.close()
    cPickle.dump(dict, file)
    file.close()

    print "initialized graph"
    print "request loop is now initialized"


probabilityCache = {}


def selectMostProbable(gr, edges, hitCreatedDict, hitEvaluated, hitID, requiredHitCreatedValue, mustBeAnswered, minimumProbability=0, favorAlreadyConnected=False):

    unansweredQuestionsExist = False

    mostProbableEdge = None
    max = 0

    for index, e in enumerate(edges):

        if args.quick_test_mode and index > 10:
            break

        # skip edges that are already fully evaluated
        if (frozenset(e) in hitEvaluated):
            continue

        # skip edges that are already connected in the graph
        if gr.has_node(e[0]) and gr.has_node(e[1]):
            if graph_util.connected(gr, e[0], e[1]):
                continue

        # skip edges that have the wrong HIT created value
        if frozenset(e) in hitCreatedDict:
            hitCreatedValue = True
        else:
            hitCreatedValue = False
        if requiredHitCreatedValue != hitCreatedValue:
            continue


        if e in probabilityCache:
            p = probabilityCache[e]
        else:
            region1 = getRegionByID(cursor, e[0])
            region2 = getRegionByID(cursor, e[1])
            p = link_prob.linkProbability(region1, region2)
            probabilityCache[e] = p
        print "index:", index, " total:", len(edges)
        print "probability:", p, "    minimum probablility:", minimumProbability

        if favorAlreadyConnected and alreadyConnected(gr, e):
            p += 1.0

        # skip low probability connections
        if p < max:
            continue


        OK = False
        if not mustBeAnswered:
            OK = True
        else:
            if frozenset(e) in hitCreatedDict:
                id = hitID[frozenset(e)]
                for repeat in range(0, 20):
                    print "repeat", repeat
                    try:
                        #results = access_aws.mtc.get_assignments(id)
                        answers = getAnswers(id, None)
                        break
                    except:
                        "couldn't get HIT in probability function"
                    time.sleep(200)
                print "checking edge:", e, " HIT:", id, " number of answers so far:", len(answers), answers
                if len(answers) < assignmentsPerHIT:
                    unansweredQuestionsExist = True
                # if there's an answer
                if access_aws.simulateYes or (len(answers) == assignmentsPerHIT):
                    OK = True


        if requiredHitCreatedValue == hitCreatedValue and OK:
            mostProbableEdge = e
            max = p


    print "most probable edge:", mostProbableEdge

    if max < minimumProbability:
        print "probability %f not high enough" % max
        return (None, unansweredQuestionsExist)

    return (mostProbableEdge, unansweredQuestionsExist)


#todo: use alreadyConnected
def removeIfAlreadyConnected(edge, gr, edgesToBeEvaluated):

    if gr.has_node(edge[0]) and gr.has_node(edge[1]):
        if graph_util.connected(gr, edge[0], edge[1]):
            edgesToBeEvaluated.remove(edge)
            print "the edge %s will not be evaluated because the nodes are already connected by some path" % str(edge)
            return True

    return False


def alreadyConnected(gr, edge):

    if gr.has_node(edge[0]) and gr.has_node(edge[1]):
        if graph_util.connected(gr, edge[0], edge[1]):
            return True

    return False




def removeEdgesWithRegion(zEdgesDict, regionID, verbose=False):

    edges = edgesAdjToRegion(regionID, zEdgesDict, verbose=verbose)
    for edge in edges:
        del zEdgesDict[edge]


def removeEdgesWithRegionFromList(edgesToBeEvaluated, regionID):

    #for i in range(len(edgesToBeEvaluated)):
    i = 0

    while i < len(edgesToBeEvaluated):

        #print i, edgesToBeEvaluated[i], "number of edges:", len(edgesToBeEvaluated)
        if edgesToBeEvaluated[i][0] == regionID or edgesToBeEvaluated[i][1] == regionID:
            print "removing edge from edgesToBeEvaluated:", edgesToBeEvaluated[i]
            del edgesToBeEvaluated[i]
            # don't need to increment i here because the ith element just got deleted
        else:
            i += 1




def overlap(region1, region2):

    region2Dict = link_prob.listToDict(region2)
    for point in region1:
        if point in region2Dict:
            return True

    return False


def overlapCount(region1, region2):

    count = 0

    region2Dict = link_prob.listToDict(region2)
    for point in region1:
        if point in region2Dict:
            count += 1

    return count



def replaceRegionWithChildren(parentRegionID, zEdges, edgesToBeEvaluated, gr):
    """Replaces region with children after running a watershed operation.
    Updates graph gr, the region database, and zEdges.
    Returns list of new edges."""

    # Throughout this function, consider all the data structures where
    # the region matters:
    # (1) the graph, (2) the region database, (3) zEdges


    connection = sqlite3.connect(os.path.join(dataOutputFolder, 'dseg.db'))
    cursor = connection.cursor()

    parentRegion = getRegionByID(cursor, parentRegionID)

    print "replacing region:", parentRegionID
    makeRegionImageUsingID(parentRegionID)
    newRegions = splitRegion(parentRegionID)

    newRegionIDs = []
    newEdgeList = []

    # put new regions in the (1) graph and (2) region database
    for index, r in enumerate(newRegions):

        print "creating new child of", parentRegionID, "index:", index, "total number:", len(newRegions)

        number = 1000000000 + int(round(time.time() * 1000))
        regionID = makeRegionIdentifier(r.z, number)
        newRegionIDs.append(regionID)

        # need to say something like gr.add_node(regionID) here

        makeRegionImage(r, name=regionID)
        regionString = binascii.hexlify(cPickle.dumps(r))
        #todo: should use a better index like SQL AUTO INCREMENT
        cursor.execute("INSERT INTO regions VALUES (%d, %d,'%s', %d)" %\
                       (r.z, number, regionString, number))
        connection.commit()


    adjRegionIDs = adjacentRegions(zEdges, parentRegionID)

    # (3) put new edges in zEdges
    for adjRegionID in adjRegionIDs:
        # check for overlap with any of the new regions on adjacent planes
        for newRegionID in newRegionIDs:
            if overlap(getRegionByID(cursor, adjRegionID), getRegionByID(cursor, newRegionID)):
                # add edge to zEdges
                newEdge = (newRegionID, adjRegionID)
                print "new edge:", newEdge
                zEdges[newEdge] = True
                newEdgeList.append(newEdge)


    # delete the parent region and associated links

    # (1) leave the region in the database, it won't hurt anything and you might want to restart the process and use it again
    #numbers = regionIdentifierToNumbers(parentRegionID)
    #command = "DELETE FROM regions WHERE z=%d AND number=%d" % numbers
    #print command
    #cursor.execute(command)

    # (2) delete the region node from the graph gr
    if gr.has_node(parentRegionID):
        gr.del_node(parentRegionID)

    # (3) delete edges that involve the deleted region
    removeEdgesWithRegion(zEdges, parentRegionID)
    removeEdgesWithRegionFromList(edgesToBeEvaluated, parentRegionID)


    # write the changes to permanent storage if needed
    # (1) graph will get written to disk later, nothing will be done here
    # (2) commit new entries to the the region database
    connection.commit()
    connection.close()
    # (3) write zEdges to disk
    writeZEdges(zEdges)


    # also, need to add new edges onto the list of edges to be evaluated
    # (something that can be done after this function is called)
    return (newRegionIDs, newEdgeList)



#simulateYes = True

#if simulateYes:
#    # no need to pay if the answers are assumed to be Yes, so use sandbox
#    useSandbox = True




def touchMoreThanOne():
    """Those regions that are thought to touch more than one cell"""

    filename = os.path.join(dataOutputFolder, "request_loop_data")
    file = open(filename, 'rb')
    dict = cPickle.load(file)
    hitAnswer = dict['hitAnswer']
    file.close()

    resultList = []

    for answerKey in hitAnswer:
        if hitAnswer[answerKey] == 'Yes':
            if isinstance(answerKey, basestring):
                print answerKey
                resultList.append(answerKey)

    return resultList



def resetAllRegionHITs(requestLoopDict):

    hitCreated = requestLoopDict['hitCreated']
    hitID = requestLoopDict['hitID'] 
    hitEvaluated = requestLoopDict['hitEvaluated']
    hitAnswer = requestLoopDict['hitAnswer']

    for key in hitCreated.keys():
        if isinstance(key, basestring):
            del hitCreated[key]

    for key in hitID.keys():
        if isinstance(key, basestring):
            del hitID[key]

    for key in hitEvaluated.keys():
        if isinstance(key, basestring):
            del hitEvaluated[key]

    for key in hitAnswer.keys():
        if isinstance(key, basestring):
            del hitAnswer[key]




def findAllPossibleNewEdges(startNodes, gr, zEdges):
    """finds edges that are connected to the graph gr but not in the graph gr already"""

    print "finding possible new edges"

    nodeDict = {}
    resultDict = {}

    for startNode in startNodes:
        nodes = pygraph.algorithms.traversal.traversal(gr, startNode, 'pre')
        lst = [element for element in nodes]
        print "regions to consider for start region %s:" % startNode, lst
        for node in lst:
            nodeDict[node] = True

    print "node dictionary:", nodeDict

    for regionID in nodeDict:
        print "finding possible new edges connected to region:", regionID
        for e in edgesAdjToRegion(regionID, zEdges):
            if not gr.has_edge(e):
                resultDict[e] = True

    result = []
    for key in resultDict:
        result.append(key)

    print "result edges", result

    return result





def findUndersegmentedRegionsThatCouldExtendObject(startNodes, gr, zEdges, hitCreated):

    sizeOfSetToProcess = 10

    edges = findAllPossibleNewEdges(startNodes, gr, zEdges)

    #print "all possible:", edges

    regionList = []

    edgeRankList = []

    for edge in edges:
        region0 = getRegionByID(cursor, edge[0])
        region1 = getRegionByID(cursor, edge[1])
        intersection = overlapCount(region0, region1)
        edgeRankList.append((edge, intersection))

    edgeRankList.sort(key=lambda x: x[1], reverse=True)

    for edgeRank in edgeRankList:
        if edgeRank[0][0] not in hitCreated:
            regionList.append(edgeRank[0][0])
        if edgeRank[0][1] not in hitCreated:
            regionList.append(edgeRank[0][1])

    # try processing the top candidates

    # todo *************** only return the regions that have not already been checked for splitting

    topPart = regionList[0:sizeOfSetToProcess]

    print "size of set to process:", sizeOfSetToProcess
    print "top part of edge rank list:", edgeRankList[0:sizeOfSetToProcess]
    print "top part of region list:", topPart

    return topPart




def changeStartRegionsIfNeeded(newRegionIDsAfterSplit, removedRegionID, startRegions, startPoints):

    print "change start regions if needed"

    if removedRegionID in startRegions:
        startRegions.remove(removedRegionID)

        # consider each new region, if it contains a start point, add id
        for regionID in newRegionIDsAfterSplit:
            #print "new region after split", regionID
            region = getRegionByID(cursor, regionID)
            for startPoint in startPoints:
                #print "start point", startPoint
                if (startPoint[0], startPoint[1]) in region:
                    print "adding new start region:", regionID
                    startRegions.append(regionID)

    print "updated start region list:", startRegions



def requestLoop(useEdges=False, useCenterPoints=False, oversegSource="watershed"):

    numHITs = 0

    filename = os.path.join(outputFolder, "request_loop_data")
    file = open(filename, 'rb')
    #dict = shelve.open(filename)
    dict = cPickle.load(file)

    #resetAllRegionHITs(dict)


    gr = dict['gr']
    #labelVolume = dict['labelVolume']
    #allRegions = dict['allRegions']
    #zEdges = dict['zEdges']
    zEdgesFile = open(os.path.join(outputFolder, "zEdges.pickle"), 'rb')
    zEdges = cPickle.load(zEdgesFile)
    zEdgesFile.close()
    #startEdges = dict['startEdges']
    regionsToBeEvaluated = dict['regionsToBeEvaluated']
    edgesToBeEvaluated = dict['edgesToBeEvaluated']


    hitCreated = dict['hitCreated']
    hitID = dict['hitID'] 
    hitEvaluated = dict['hitEvaluated']
    hitAnswer = dict['hitAnswer']
    nodeCreationTime = dict['nodeCreationTime']
    poisoned = dict['poisoned']


    print "startRegions", dict['startRegions']

    file.close()

    print "writing imod file"
    compositeOutputFolder = os.path.join(outputFolder, "composite")
    renderGraphToIMODMerged(compositeOutputFolder, gr, dict['startRegions'], allRegionsSeparate=False, onlyUseRegionsThatWereSelectedByAUser=True)
    print "finished writing imod file"

    print "request loop"

    
    # strictly test code, not to be used for a real run
    testRegionSplit = False
    if testRegionSplit:
        edgesToBeEvaluated = []
        (newRegionIDsAfterSplit, newEdgesAfterSplit) = replaceRegionWithChildren('1_5', zEdges, edgesToBeEvaluated, gr)
        changeStartRegionsIfNeeded(newRegionIDsAfterSplit, '1_5', dict['startRegions'], getStartPoints())
        for startRegionIdentifier in dict['startRegions']:
            if not gr.has_node(startRegionIdentifier):
                gr.add_node(startRegionIdentifier)
        edgesToBeEvaluated = findAllPossibleNewEdges(dict['startRegions'], gr, zEdges)
        print "edges to be evaluated from test:", edgesToBeEvaluated


#    print "regions that people believe touche more than one:"
#    tempFileList = []
#    for answerKey in hitAnswer:
#        if hitAnswer[answerKey] == 'Yes':
#            if isinstance(answerKey, basestring):
#                print answerKey
#                tempFileList.append(answerKey)
#    makeQualificationsFile(tempFileList, range(0, len(tempFileList)/2), range(len(tempFileList)/2, len(tempFileList)), "Does blue highlight more than one cell?", 'regions')
#    propertiesFile = os.path.join(mturkScriptFolder, "plane_to_plane", "qualification.properties")
#    print "properties", propertiesFile
#    writePropertiesFile(propertiesFile, "Region")
#    command = "cd " + os.path.join(mturkScriptFolder, "plane_to_plane") + ";" + "./run.sh"
#    print command
#    os.system(command)
#    print "end regions that people believe touche more than one:"



    nextScheduledRender = numHITs + 0

    #cvImages = createCVImages(initialSegFolder)

    #while(len(edgesToBeEvaluated) != 0):

    refreshEdgesCountdown = 0

    while True:

        # refresh the list of possible edges based on the graph named gr every 10th iteration
        print "refreshed edges countdown:", refreshEdgesCountdown
        if refreshEdgesCountdown == 0:
            for startRegionIdentifier in dict['startRegions']:
                if not gr.has_node(startRegionIdentifier):
                    gr.add_node(startRegionIdentifier)
            edgesToBeEvaluated = findAllPossibleNewEdges(dict['startRegions'], gr, zEdges)
            refreshEdgesCountdown = 10
        else:
            refreshEdgesCountdown -= 1


        # if there is nothing left to do, break out of the loop (todo: This condition won't be met because regionsToBeEvaluated now contains evaluated edges. Might want to clean them out.)
        if len(edgesToBeEvaluated) == 0 and len(regionsToBeEvaluated) == 0:
            break

        compositeOutputFolder = os.path.join(outputFolder, "composite")
        makeDirectory(compositeOutputFolder)
        #renderGraph(compositeOutputFolder, v, allRegions, gr, allRegionsSeparate=False, onlyUseRegionsThatWereSelectedByAUser=True)

        # This allows user to specify nodes that should be removed no matter what the workers choose for connections.
        # It's a way to correct what the workers have done.
        if args.delete:
            for regionID in eval(args.delete):
                gr.del_node(regionID)


        if  numHITs >= nextScheduledRender:
            nextScheduledRender = numHITs + renderInterval
            #renderGraph(compositeOutputFolder, gr, poisoned, showBackgroundImage=False, allRegionsSeparate=False, onlyUseRegionsThatWereSelectedByAUser=True, startRegions=dict['startRegions'])
            #renderGraphToIMOD(compositeOutputFolder, gr, dict['startRegions'], allRegionsSeparate=False, onlyUseRegionsThatWereSelectedByAUser=True)
            renderGraphToIMODMerged(compositeOutputFolder, gr, dict['startRegions'], allRegionsSeparate=False, onlyUseRegionsThatWereSelectedByAUser=True)
            if args.send_regions_to_database:
                sendRegionsToDatabase()


        print "answers:"
        for key in hitAnswer:
            print hitAnswer[key], key

        print "edges to be evaluated:", edgesToBeEvaluated
        #todo: option: could just pop one edge to evaluate
        #for edge in edgesToBeEvaluated:
        #for task in ('submitHumanEvaluation', 'expandToNext'):
        #if 1:

        print "number of HITs created so far: %d" % numHITs
        print "size of list to be evaluated:", len(edgesToBeEvaluated)



        ###########################################
        # examine edge answers
        # expand edges on a HIT if it has been answered Yes
        # edge is an edge identifier, a list of two region ID's

        (edge, unansweredEdgeQuestionsExist) = selectMostProbable(gr, edgesToBeEvaluated, hitCreated, hitEvaluated, hitID, True, True, favorAlreadyConnected=False) #favorAlreadyConnected=True for poisoned test

        #if edge == None:
        #    print "currently there are no new answers"
        #    examineEdgeAnswersHasWorkToDo = False
        #else:
        #    examineEdgeAnswersHasWorkToDo = True

        # if the nodes are already connected somehow by any existing path, do not process this edge
        if edge != None:
            removed = removeIfAlreadyConnected(edge, gr, edgesToBeEvaluated)
            #removed = False #for poisoned test
        if (edge != None) and (not removed):

        #if frozenset(edge) in hitCreated:

            # check whether the user has evaluated the edge and what the answer is

            #todo: this is now redundant
            id = hitID[frozenset(edge)]
            results = access_aws.mtc.get_assignments(id)
            print "checking edge:", edge, " HIT:", id, " number of answers so far:", len(results)
            # if there's an answer
            #todo: this is now redundant
            if access_aws.simulateYes or (len(results) == assignmentsPerHIT):

                # remove this edge from edgesToBeEvaluated list
                answerList = getAnswers(id, assignmentsPerHIT)
                print "answers from mturk", answerList

                # require that both are 'Yes'
                if access_aws.simulateYes or (answerList[0] == 'Yes' and answerList[1] == 'Yes'):
                    answer = 'Yes'
                else:
                    answer = 'No'


                # if the 3D segmentation input suggests that they are connected, one vote is enough
                if args.initial_3d:
                    (dummy, numericID0) = regionIdentifierToNumbers(edge[0])
                    (dummy, numericID1) = regionIdentifierToNumbers(edge[1])
                    if numericID0 == numericID1:
                        if (answerList[0] == 'Yes' or answerList[1] == 'Yes'):
                            answer = 'Yes'


                if answer == "Yes" or answer == "No":
                    hitEvaluated[frozenset(edge)] = True
                    hitAnswer[frozenset(edge)] = answer
                    edgesToBeEvaluated.remove(edge) #todo: this may not work as expected


                    # add regions that make up the edge to be evaluated for splitting
                    for r in edge:
                        if (r not in hitCreated) and (r not in regionsToBeEvaluated):
                            print " adding", r
                            regionsToBeEvaluated.append(r)
                        else:
                            print " skipping", r




                # if both answers for two users are positive
                if answer == "Yes":

                    # add nodes and edge
                    if not(gr.has_node(edge[0])):
                        gr.add_node(edge[0])
                        nodeCreationTime[edge[0]] = time.time()
                    if not(gr.has_node(edge[1])):
                        gr.add_node(edge[1])
                        nodeCreationTime[edge[1]] = time.time()
                    gr.add_edge(edge)

                    # set the location if needed
                    if useGetPointsForZDecisionTestVersion:
                        (dummy, newCoordinatePair, rID, dummy) = getPointsForZDecision_test_version(edge, dict['pointLocations'])
                        if rID != None:
                            print "setting region", rID, "to have point location", newCoordinatePair
                            dict['pointLocations'][rID] = newCoordinatePair


                    #add all adjacent edges to edgesToBeEvaluated list (if it's not already marked with hitCreated)
                    adjEdges = adjacentEdges(zEdges, edge)

                    for e in adjEdges:
                        #if not(frozenset(e) in hitCreated):
                        if not(frozenset(e) in hitCreated) and not(e in edgesToBeEvaluated):
                        #if not(frozenset(e) in hitCreated) and not(e in edgesToBeEvaluated) and not(frozenset(e) in hitEvaluated):
                            print " adding", e
                            edgesToBeEvaluated.append(e)
                        else:
                            print " skipping", e



                elif answer == "No":
                    # if it's connected somehow, mark newer as a poisoned node
                    if 0: #for poisoned test
                        if alreadyConnected(gr, edge):
                            if nodeCreationTime[edge[0]] > nodeCreationTime[edge[1]]:
                                poisoned[e[0]] = True
                            else:
                                poisoned[e[1]] = True
                    pass
                elif answer == None:
                    pass
                else:
                    raise Exception("invalid answer")



        ###########################################
        # create an edge HIT
        #
        # parameters for selectMostProbable:
        # HIT created must be false
        # whether it's answered or not won't be checked

        #todo: this should be like top 10% rather than an absolute number
        (edge, dummy) = selectMostProbable(gr, edgesToBeEvaluated, hitCreated, hitEvaluated, hitID, False, False, minimumProbability=minimumProbability, favorAlreadyConnected=False) #favorAlreadyConnected=True for poisoned test
        # if the nodes are already connected somehow by any existing path, do not process this edge

        print "creating HIT for edge %s" % str(edge)

        if edge == None:
            createEdgeHITHasWorkToDo = False
        else:
            createEdgeHITHasWorkToDo = True

        if edge != None:
            #removed = False #for poisoned test
            removed = removeIfAlreadyConnected(edge, gr, edgesToBeEvaluated)

        if (edge != None) and (not removed):

            # HIT does not exist for this edge, so create it

            # create image for HIT
            useCenterPoints = True
            #(success, filename) = makeZDecisionImage(allRegions, cvImages, edge, useCenterPoints)
            (success, filename) = makeZDecisionImage(edge, useCenterPoints, dict['pointLocations'])

            #print "zEdges keys:", zEdges.keys()[0:10]
            #newEdgeList = replaceRegionWithChildren(edge[0], zEdges, gr) # test
            #for newEdge in newEdgeList:
            #    edgesToBeEvaluated.append(newEdge)
            #(success, filename) = makeZDecisionImage2(gr, edge, useCenterPoints)
            #uploadFileToAmazonS3(addAnimationSuffix(filename) + ".gif", 'plane_to_plane')

            access_aws.uploadFileToAmazonS3(
                os.path.join(tileFolder, 'plane_to_plane', addAnimationSuffix(filename) + ".gif"),
                dataName,
                'data/plane_to_plane',
                addAnimationSuffix(filename) + ".gif",
                args.access_key,
                args.secret_key)

            # create edge HIT
            resultSet = access_aws.createHIT(makePlaneToPlaneUrl(filename),
                                             assignmentsPerHIT,
                                             "Does the dot stay inside the cell",
                                             "2TUKSSZVXX2Q5G8GJGFYNNIW1QSN5K",
                                             "23VZHHRRLFQ0PY1HQ7SKKO9EGTEOFG",
                                             (Requirement("22V6DG67D1X3WBT6Z2FK9JE1MAQ9GG", "GreaterThanOrEqualTo", "25"),))
                                              #Requirement("2LTFK0COK2JE2XLBJA0LYW6OZDFKRJ", "GreaterThanOrEqualTo", "6")))
                                             

            numHITs += 1
            print "url:", makePlaneToPlaneUrl(filename)
            hit = resultSet[0]
            hitID[frozenset(edge)] = hit.HITId
            print "creating HIT:", hit.HITId, "for", edge
            hitCreated[frozenset(edge)] = True



        ###########################################
        # create a region HIT
        #

        print "regions to be evaluated:", regionsToBeEvaluated

        regionIDForHIT = None

        # find a region that doesn't already have a HIT created (if there is one at all)
        for r in regionsToBeEvaluated:
            if progressiveSplittingEnabled or (r in dict['possibleUndersegRegionDict']):
                if r not in hitCreated:
                    regionSize = len(getRegionByID(cursor, r))
                    if regionSize > minimumRegionSizeForSplit:
                        regionIDForHIT = r
                        break
                    else:
                        print "region", r, "with size", regionSize, "is not big enough to be split"

        # randomly create a region HIT for testing purposes
        #regionIDForHIT = edgesToBeEvaluated[random.randint(len(edgesToBeEvaluated))][0]

        if (regionIDForHIT == None):
            createRegionHITHasWorkToDo = False
        else:
            createRegionHITHasWorkToDo = True

        if (regionIDForHIT != None):

            if (regionIDForHIT in dict['possibleUndersegRegionDict']):
                print "handling possible underseg region"

            print "creating HIT for region %s" % str(regionIDForHIT)

            makeRegionImageUsingID(regionIDForHIT)

            # HIT does not exist for this region, so create it

            regionFilename = "region_%d_%d.jpg" % regionIdentifierToNumbers(regionIDForHIT)
            regionFullFilename =  os.path.join(tileFolder, "regions", regionFilename)

            access_aws.uploadFileToAmazonS3(
                regionFullFilename,
                dataName,
                'data/regions',
                regionFilename,
                args.access_key,
                args.secret_key)

            # create region HIT
            resultSet = access_aws.createHIT(makeRegionsUrl(regionFilename),
                                             assignmentsPerHIT,
                                             "Does the blue highlight more than one cell",
                                             "2HQBMJTUHYW2H43VQ0YSCWM16G4NI8",
                                             "27RSVQ8H88MQVHZRN1MCL1RXX6P7QF",
                                             #(Requirement("2LTFK0COK2JE2XLBJA0LYW6OZDFKRJ", "GreaterThanOrEqualTo", "6"),
                                              (Requirement("2CHFXRDS4IC1F9R9W96M81A2IY2VYJ", "GreaterThanOrEqualTo", "11"),))

            numHITs += 1
            print "url:", makeRegionsUrl(filename)
            hit = resultSet[0]
            hitID[regionIDForHIT] = hit.HITId
            print "creating HIT:", hit.HITId, "for", edge
            hitCreated[regionIDForHIT] = True






        ###########################################
        # examine region answers
        # split region if needed

        # consider HITs for all regions to be evaluated, check for answers
        unansweredRegionQuestionsExist = False
        for regionIDForAnswerCheck in regionsToBeEvaluated:

            print "checking if region has hit created, id:", regionIDForAnswerCheck
            #print "hitID dictionary:", hitID


            if regionIDForAnswerCheck in hitID:
                "HIT is created"
            else:
                "HIT is not created"
                # if there is no HIT yet, skip this region
                continue


            id = hitID[regionIDForAnswerCheck]
            #results = access_aws.mtc.get_assignments(id)
            answerListForRegion = getAnswers(id, None)
            print "checking region:", regionIDForAnswerCheck, " HIT:", id, " number of answers so far:", len(answerListForRegion), "answer list for region:", answerListForRegion

            if len(answerListForRegion) < assignmentsPerHIT:
                unansweredRegionQuestionsExist = True

            answer = None

            # handle one answer 'Yes' received
            #if access_aws.simulateYes or (len(results) == 1):
            #    if access_aws.simulateYes or (answerListForRegion[0] == 'Yes'):
            #        print "one answer is Yes, and that's all that is needed"
            #        answer = 'Yes'

            # handle all answers received
            if access_aws.simulateYes or (len(answerListForRegion) == assignmentsPerHIT):

                print "found region with answers"
        
                answerListForRegion = getAnswers(id, assignmentsPerHIT)
                print "answers from mturk", answerListForRegion
        
                # if one answer is 'Yes', at least one user said it needs to be split
                if access_aws.simulateYes or (answerListForRegion[0] == 'Yes') or (answerListForRegion[1] == 'Yes'):
                    answer = 'Yes'
                else:
                    answer = 'No'
        
            if answer == "Yes" or answer == "No":

                hitEvaluated[regionIDForAnswerCheck] = True
                hitAnswer[regionIDForAnswerCheck] = answer

                if regionIDForAnswerCheck in regionsToBeEvaluated:
                    regionsToBeEvaluated.remove(regionIDForAnswerCheck) #todo: this may not work as expected
    
            # if the answer to positive
            if answer == "Yes":
    
                (newRegionIDsAfterSplit, newEdgesAfterSplit) = replaceRegionWithChildren(regionIDForAnswerCheck, zEdges, edgesToBeEvaluated, gr)
                changeStartRegionsIfNeeded(newRegionIDsAfterSplit, regionIDForAnswerCheck, dict['startRegions'], getStartPoints())
                #edgesToBeEvaluated = findAllPossibleNewEdges(dict['startRegions'], gr, zEdges)
                refreshEdgesCountdown = 0 # effectively, this is a request that the system find where new edges may need to be added to the current object now that this region has been split

                for e in newEdgesAfterSplit:
                    if not(frozenset(e) in hitCreated) and not(e in edgesToBeEvaluated):
                        print " adding", e
                        edgesToBeEvaluated.append(e)
                    else:
                        print " skipping", e
                # one region processed, break out out of loop that scans for regions to process
                break
    
            elif answer == "No":
                pass
            elif answer == None:
                pass
            else:
                raise Exception("invalid answer")
    


            #break
                


        
        ###########################################
        # add splits to undersegmented regions an connect if needed

        print "checks:", createEdgeHITHasWorkToDo, unansweredEdgeQuestionsExist, createRegionHITHasWorkToDo, unansweredRegionQuestionsExist

        if (not createEdgeHITHasWorkToDo) and (not unansweredEdgeQuestionsExist) \
            and (not createRegionHITHasWorkToDo) and (not unansweredRegionQuestionsExist):


            dict['possibleUndersegRegionDict'] = {}

            print "Edge scanning is complete, and there are no more known connections."
            print "Attempting to break undersegmented regions to find more."

            possibleUndersegRegionList = findUndersegmentedRegionsThatCouldExtendObject(dict['startRegions'], gr, zEdges, hitCreated)

            for item in possibleUndersegRegionList:
                dict['possibleUndersegRegionDict'][item] = True
                regionsToBeEvaluated.append(item)



        ###########################################
        # write to file


        print "graph:", gr
        print "poisoned:", poisoned
        #outFile = open(os.path.join(outputFolderBase, dataName, "graph.pickle"), 'wb')
        #cPickle.dump(gr, outFile)
        #outFile.close()

        print "writing dictionary to disk, keys:", dict.keys()

        filename = os.path.join(outputFolder, "request_loop_data")
        file = open(filename, 'wb')
        #dict = shelve.open(filename)

        dict['gr'] = gr
        dict['edgesToBeEvaluated'] = edgesToBeEvaluated
        dict['regionsToBeEvaluated'] = regionsToBeEvaluated
        dict['hitCreated'] = hitCreated
        dict['hitID'] = hitID
        dict['hitEvaluated'] = hitEvaluated
        dict['hitAnswer'] = hitAnswer
        dict['nodeCreationTime'] = nodeCreationTime
        dict['poisoned'] = poisoned
        #dict.sync()

        cPickle.dump(dict, file)
        file.close()

        print "next scheduled rending after %d HITs are submitted" % (nextScheduledRender - numHITs)

        if numHITs % 5 == 0:
            print "sleeping"
            print "you can abort the process now, while sleeping, and come back later"
            time.sleep(6)
            print "finished sleeping"



    # text description:
    #loop
        # add hit or explore more edges as needed




# fileList is a list of image files that represent the examples to be presented to users
def makeQualificationsFile(fileList, exampleIndexes, questionIndexes, text, type):

    examples = ""
    questions = ""
    answersText = ""

    #if makeQualifications:

    # if answers file is specified
    if args.answers:

        answersDict = readSplitAnswers(args.answers)

        # get file list (dictionary in this case) from answers file
        fileList = {}
        for i in exampleIndexes:
            fileList[i] = os.path.basename(answersDict[i]['filename'])
        for i in questionIndexes:
            fileList[i] = os.path.basename(answersDict[i]['filename'])



    # examples
    print "fileList", fileList

    for i in exampleIndexes: #range(10, 35):
        if type == 'plane_to_plane':
            url = makePlaneToPlaneUrl(fileList[i])
        elif type == 'regions':
            url = makeRegionsUrl(fileList[i])
        else:
            raise Exception("invalid type")

        if args.answers:
            currentAnswer = answersDict[i]['answer']
        else:
            currentAnswer = "." # no answer
        examples += makeExample(i, text, url, currentAnswer)

    # questions and answers
    #questionCount = 1
    for i in questionIndexes: #range(35, 60):
        if type == 'plane_to_plane':
            url = makePlaneToPlaneUrl(fileList[i])
        elif type == 'regions':
            url = makeRegionsUrl(fileList[i])
        else:
            raise Exception("invalid type")
        #number = questionCount
        number = i
        questions += makeQuestion(number, url, text)
        if args.answers:
            currentAnswer = answersDict[i]['answer']
        else:
            currentAnswer = "." # no answer
        answersText += makeAnswer(number, currentAnswer)
        #print "makeAnswer", number, answersDict[i]
        #questionCount += 1

    questionFilename = os.path.join(mturkScriptFolder, "plane_to_plane", "qualification.question")
    print "writing question file", questionFilename
    questionFile = open(questionFilename, 'w')
    questionFile.write(makeStartOfHeader(text) + examples + endOfHeader + questions + footer)
    questionFile.close()

   
    answerFilename = os.path.join(mturkScriptFolder, "plane_to_plane", "qualification.answer")
    print os.getcwd()
    print "writing answer file", answerFilename
    answerFile = open(answerFilename, 'w')
    answerFile.write(answersHeader + answersText + answersFooter)
    answerFile.close()



def makeProcessCSVFile(fileList):

    #if not(makeQualifications):

    # makes tiles plane to plane, write csv file for the questions

    #csvFullPath = os.path.join(outputFolder, "images_plane_to_plane.csv")
    #csvFullPath = outputCSVFilename
    #file = open(csvFullPath, 'w')
    #print "writing", csvFullPath
    file = open(outputCSVFilename, 'w')
    print "writing", outputCSVFilename

    #file.write("id1,id2\n")
    file.write("image1\n")


    for filename in fileList:
        url = makePlaneToPlaneUrl(filename)
        file.write(url)
        file.write("\n")


    file.close()


# function: makeTilesPlaneToPlane

def normalizeMaxToOne(numbers):
    m = max(numbers)
    return numpy.array(numbers) / float(m)


def paintRegion(openCVImages, imageVolume, region, regionID, componentsDict, colorMap, nodeCount, allRegionsSeparate, showBackgroundImage, renderingScaleFactor, isPoisoned, concentration=None):


        # note: possible feature: make color brighter for connected components with 2 or more nodes

        if regionID in componentsDict:
            count = nodeCount[componentsDict[regionID]]
        else:
            count = 0
        #print "count", count
        #if count > 1:
        if allRegionsSeparate or count == 0:
            color = (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))
        else:
            if concentration != None:
                normalizedConcentration = normalizeMaxToOne(concentration[regionID])
                newColor = [0, 0, 0]
                #newColor[0] = min(255.0 * concentration[regionID][0], 100)
                #newColor[1] = min(255.0 * concentration[regionID][1], 100)
                newColor[0] = 255.0 * normalizedConcentration[0]
                newColor[1] = 255.0 * normalizedConcentration[1]
                newColor[2] = 0
                color = newColor
            else:
                color = colorMap[componentsDict[regionID]]
                if isPoisoned:
                    newColor = [0, 0, 0]
                    newColor[0] = color[0] / 2.0
                    newColor[1] = color[1] / 2.0
                    newColor[2] = color[2] / 2.0
                    color = newColor
                print "color", color
            #else:
            #    color = array(colorMap[componentsDict[key]]) / 10.0

        #if thickness[componentsDict[key]] >= 1:
        if 1:

            # render the region

            if count != 0:
                labelValue = componentsDict[regionID]
            else:
                labelValue = nextLabelValueForUnconnectedComponent
                nextLabelValueForUnconnectedComponent += 1


            #z = key[0]
            z = region.z
            for point in region:
                #print "point", point
                if showBackgroundImage:
                    backgroundValue = imageVolume[point[0], point[1], z]
                    blendedColor = [int((backgroundValue+color[0])/2), int((backgroundValue+color[1])/2), int((backgroundValue+color[2])/2), 0]
                else:
                    blendedColor = [int(color[0]), int(color[1]), int(color[2]), 0]
                #print "background", background
                #blendedColor = (array(background) + array(color)) / 2
                #blendedColor = background
                center = array(point)
                if showBackgroundImage:
                    cv.Circle(openCVImages[z], (center[0] * renderingScaleFactor,
                                                center[1] * renderingScaleFactor),
                              renderingScaleFactor, blendedColor, thickness=-1)
                else:
                    #cv.Circle(openCVImages[z], (center[0] * renderingScaleFactor,
                    #                            center[1] * renderingScaleFactor),
                    #          renderingScaleFactor, labelValue, thickness=-1)
                    cv.Circle(openCVImages[z], (center[0] * renderingScaleFactor,
                                                center[1] * renderingScaleFactor),
                              renderingScaleFactor, blendedColor, thickness=-1)
                    if 0: resultVolume[center[0], center[1], z] = labelValue



def processRenderingGraph(gr, onlyUseRegionsThatWereSelectedByAUser):

    componentsDict = pygraph.algorithms.accessibility.connected_components(gr)

    nextLabelValueForUnconnectedComponent = len(componentsDict) + 1

    print "connected components", componentsDict

    colorMap = {}
    nodeCount = {}

    # create dictionary where regions identifiers are grouped into lists of connected components
    componentGroups = {}

    for regionID in componentsDict:

        groupID = componentsDict[regionID]
        print "groupID", groupID

        # if a group does not exist yet, create it
        if not(groupID in componentGroups):
            componentGroups[groupID] = []

        # add regionID to the group
        componentGroups[groupID].append(regionID)

    print "component groups", componentGroups
    print "number of component groups", len(componentGroups)

    thickness = {}
    for groupID in componentGroups:
        zList = []
        for regionID in componentGroups[groupID]:
            numberPair = regionIdentifierToNumbers(regionID)
            z = numberPair[0]
            zList.append(z)
        minimum = min(zList)
        maximum = max(zList)
        thickness[groupID] = maximum - minimum
        print "thickness[groupID]", thickness[groupID]

    largeObjectCount = 0
    for id in thickness:
        if thickness[id] > 5:
            largeObjectCount += 1
    print "large object count:", largeObjectCount

    for componentIndex in componentsDict.values():
        # create a color for each connected component
        colorMap[componentIndex] = (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))

        # count how many nodes are in each component
        if componentIndex in nodeCount:
            nodeCount[componentIndex] += 1
        else:
            nodeCount[componentIndex] = 1

    if onlyUseRegionsThatWereSelectedByAUser:
        regionsInGraph = gr.nodes()
    else:
        regionsInGraph = regions


    return regionsInGraph, componentsDict, colorMap, nodeCount






def renderGraphToIMODMerged(folder, gr, startRegions, allRegionsSeparate=False, showBackgroundImage=True, onlyUseRegionsThatWereSelectedByAUser=False):

    renderingScaleFactor = 1
    print "scale factor for rendering", renderingScaleFactor

    regionsInGraph, componentsDict, colorMap, nodeCount = processRenderingGraph(gr, onlyUseRegionsThatWereSelectedByAUser)

    file = open(os.path.join(outputFolder, "imod_file.txt"), 'wb')

    surface = 0
    currentRegionNumber = 0
    contoursFound = []

    conn = sqlite3.connect(os.path.join(dataOutputFolder, 'dseg.db'))
    cur = conn.cursor()

    # region is indexed like this: region[componentID][z][index]
    regionsByComponent = {}

    for regionID in regionsInGraph:
        componentID = componentsDict[regionID] 

        # if component is not represented already, added it
        if componentID not in regionsByComponent:
            regionsByComponent[componentID] = {}

        z, index = regionIdentifierToNumbers(regionID)

        # if plane is not represented already, add it
        if z not in regionsByComponent[componentID]:
            regionsByComponent[componentID][z] = []

        # add this region to the plane
        regionsByComponent[componentID][z].append(regionID)

    #print "regionsByComponent", regionsByComponent


    contoursByComponent = {}


    for componentID, componentSet in regionsByComponent.items():
        #print "componentSet", componentSet

        planeCount = 0
        for planeSet in componentSet.values():

            planeCount += 1
            #if planeCount > 1: break

            mergedRegion = []
            for regionID in planeSet:
                print "region:", currentRegionNumber, "    total number:", len(regionsInGraph)
                currentRegionNumber += 1
                region = getRegionByID(cur, regionID)
                mergedRegion += region

            contours = regionToContours(storageForRegionToContours, mergedRegion)

            print "contours:"
    
            for c in contourIterator(contours):
    
                print "contour"
                print c
                points = []
                for point in c:
                    points.append(point)
    
                # start new list of contours for this component if needed
                if componentID not in contoursByComponent:
                    contoursByComponent[componentID] = []
    
                contoursByComponent[componentID].append({'points':points, 'z': region.z, 'name':regionID})



    objectIndex = 0

    numObjects = len(contoursByComponent)
    file.write(IMODHeaderOnly(numObjects))


    for componentID, contoursFound in contoursByComponent.items():

        numContours = len(contoursFound)
        color = colorMap[componentID]
        print "color", color
        file.write(IMODObjectString(objectIndex,
                                    numContours,
                                    "",
                                    numpy.array(color)/255.0))

        contourIndex = 0

        for i in range(len(contoursFound)):
            contour = contoursFound[i]['points']

            # todo: is this needed?  
            #if len(contour) > 0:
            if 1:

                print "writing contour:", contour
                numPoints = len(contour)
                regionID = contoursFound[i]['name']
                #color = (min(255.0 * concentration[regionID][0], 100),
                #         min(255.0 * concentration[regionID][1], 100),
                #         0)
    
                file.write("contour %d %d %d\n" % (contourIndex, surface, numPoints))
                for p in contour:
                    print p
                    file.write("%d %d %d\n" % (p[0], imageHeight - p[1], contoursFound[i]['z']))
    
                contourIndex += 1

        objectIndex += 1

    file.close()












def renderGraphToIMOD(folder, gr, startRegions, allRegionsSeparate=False, showBackgroundImage=True, onlyUseRegionsThatWereSelectedByAUser=False):

    renderingScaleFactor = 1
    print "scale factor for rendering", renderingScaleFactor

    regionsInGraph, componentsDict, colorMap, nodeCount = processRenderingGraph(gr, onlyUseRegionsThatWereSelectedByAUser)

    file = open(os.path.join(outputFolder, "imod_file.txt"), 'wb')

    surface = 0
    currentRegionNumber = 0
    contoursFound = []

    conn = sqlite3.connect(os.path.join(dataOutputFolder, 'dseg.db'))
    cur = conn.cursor()

    concentration = diffuseFromStartRegions(gr, startRegions)



    for key in regionsInGraph:

        print "region:", currentRegionNumber, "    total number:", len(regionsInGraph)
        #if currentRegionNumber > 100: break
        currentRegionNumber += 1
        region = getRegionByID(cur, key)
        contours = regionToContours(storageForRegionToContours, region)
        # probably just one contour for this region but theoretically there could be more than one
        print "contours:", contours

        for c in contourIterator(contours):

            print "contour"
            #count = 0
            #todo: there a way to get the size better than this
            #for dummy in c:
            #    count += 1
            #numPoints = count
            points = []
            for point in c:
                points.append(point)

            contoursFound.append({'points':points, 'z': region.z, 'name':key})


        #paintRegion(openCVImages, imageVolume, region, key, componentsDict, colorMap, nodeCount, allRegionsSeparate, showBackgroundImage, renderingScaleFactor)

    index = 0
    numContours = len(contoursFound)
    if 0:
        file.write(IMODHeader(numContours))
    file.write(IMODHeaderOnly(len(contoursFound)))
    #todo: set z scale
    for i in range(len(contoursFound)):
    #for i in range(100):
    #while True:
        #i = index
        contour = contoursFound[i]['points']

        if len(contour) > 0:
            print "writing contour:", contour
            numPoints = len(contour)
            regionID = contoursFound[i]['name']
            color = (min(255.0 * concentration[regionID][0], 100),
                     min(255.0 * concentration[regionID][1], 100),
                     0)

            file.write(IMODObjectString(index, 1, contoursFound[i]['name'], color))
            #file.write("contour %d %d %d\n" % (index, surface, numPoints))
            file.write("contour %d %d %d\n" % (0, surface, numPoints))
            for p in contour:
                print p
                file.write("%d %d %d\n" % (p[0], imageHeight - p[1], contoursFound[i]['z']))

        index += 1
        #if index == len(contoursFound):
        #    break
    file.close()



def IMODHeaderOnly(numObjects):
    return """# imod ascii file version 2.0


imod {numObjects}
max 700 700 270
offsets 0 0 0
angles 0 0 0
scale 1 1 1
mousemode  1
drawmode   1
b&w_level  51,232
resolution 3
threshold  128
pixsize    1
units      pixels
refcurscale 1 1 1
refcurtrans 0 0 0
refcurrot 0 0 0
refoldtrans 0 0 0
""".format(numObjects=numObjects)



def IMODHeader(numContours):
    return  """# imod ascii file version 2.0

imod 3
max 700 700 270
offsets 0 0 0
angles 0 0 0
scale 1 1 1
mousemode  1
drawmode   1
b&w_level  51,232
resolution 3
threshold  128
pixsize    1
units      pixels
refcurscale 1 1 1
refcurtrans 0 0 0
refcurrot 0 0 0
refoldtrans 0 0 0

object 0 0 0
name 
color 0 1 0 0
hastimes
linewidth 1
surfsize  0
pointsize 0
axis      0
drawmode  1
width2D   1
symbol    1
symsize   3
symflags  0
ambient   102
diffuse   255
specular  127
shininess 4
obquality 0
valblack  0
valwhite  255
matflags2 0

object 1 %d 0
name 
color 0 1 1 0
linewidth 1
surfsize  0
pointsize 0
axis      0
drawmode  1
width2D   1
symbol    1
symsize   3
symflags  0
ambient   102
diffuse   255
specular  127
shininess 4
obquality 0
valblack  0
valwhite  255
matflags2 0
""" % numContours


def IMODObjectString(index, numContours, name, color):
    return """
object {index} {numContours} 0
name {name}
color {red} {green} {blue} 0
linewidth 1
surfsize  0
pointsize 0
axis      0
drawmode  1
width2D   1
symbol    1
symsize   3
symflags  0
ambient   102
diffuse   255
specular  127
shininess 4
obquality 0
valblack  0
valwhite  255
matflags2 0
""".format(index=index, numContours=numContours, name=name,
           red=color[0], green=color[1], blue=color[2])



def diffuseFromStartRegions(gr, startRegions):

    c = {}
    constantNodes = {}
    for classNumber, startRegionID in enumerate(startRegions):
        c[startRegionID] = numpy.zeros(len(startRegions))
        c[startRegionID][classNumber] = 100000000.0
        constantNodes[startRegionID] = True

    print "initial concentration:", c

    concentration = diffusion.diffusion(gr,
          c,
          constantNodes,
          len(startRegions))

    return concentration



#def renderGraph(folder, imageVolume, regions, gr, allRegionsSeparate=False, showBackgroundImage=True, onlyUseRegionsThatWereSelectedByAUser=False):
def renderGraph(folder, gr, poisoned, allRegionsSeparate=False, showBackgroundImage=True, onlyUseRegionsThatWereSelectedByAUser=False, startRegions=None):

    conn = sqlite3.connect(os.path.join(dataOutputFolder, 'dseg.db'))
    cur = conn.cursor()

    imageVolume = loadImageStack(inputStack, None)

    renderingScaleFactor = 1
    print "scale factor for rendering", renderingScaleFactor

    openCVImages = {}
    if 0: s = imageVolume.shape

    if 0: resultVolume = zeros(s)

    numFiles = len(glob.glob(os.path.join(originalOutputFolder, "*.png")))

    # create open cv images
    #for z in range(imageVolume.shape[2]):

    zStart, zStop = getStartAndStop(startSlice, stopSlice, numFiles)
    for z in range(zStart, zStop):

        print z

        if showBackgroundImage:
            #openCVImages[z] = toOpenCV(imageVolume[:, :, z], color=True)
            openCVImages[z] = toOpenCV(numpy.transpose(getImage(originalOutputFolder, z)), color=True)
        else:
            #openCVImages[z] = cv.CreateImage((s[0], s[1]), 8, 3)

            # todo: this is an inefficient way to get the size of the image
            tempCVImage = toOpenCV(numpy.transpose(getImage(originalOutputFolder, z)), color=True)

            #openCVImages[z] = cv.CreateImage((s[0], s[1]), 32, 1)
            openCVImages[z] = tempCVImage
            cv.SetZero(openCVImages[z])


    regionsInGraph, componentsDict, colorMap, nodeCount = processRenderingGraph(gr, onlyUseRegionsThatWereSelectedByAUser)

    concentration = diffuseFromStartRegions(gr, startRegions)

    print "concentration:", concentration

    # render regions in volume of open cv images
    currentRegionNumber = 0
    for key in regionsInGraph:

        print "region:", currentRegionNumber, "    total number:", len(regionsInGraph)
        currentRegionNumber += 1

        ##region = regions[key]
        region = getRegionByID(cur, key)
        #color = (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))

        paintRegion(openCVImages, imageVolume, region, key, componentsDict, colorMap, nodeCount, allRegionsSeparate, showBackgroundImage, renderingScaleFactor, key in poisoned, concentration=concentration)


    labelVolumePath = makeDirectory(os.path.join(outputFolder, "labels_separate=%s" % allRegionsSeparate))
    if 0: outBasename = os.path.join(labelVolumePath, "out%d_%d_32bit" % (resultVolume.shape[0], resultVolume.shape[1]))
    if 0: print outBasename
    # write labels to 32 bit volume
    # added 1000 to make sure zero isn't a label
    if 0: writeRawStack32Bit(outBasename, resultVolume+1000)


    if 0: resultEdgeVolume = makeEdgeVolume(resultVolume)
    if 0: edgeVolumePath = makeDirectory(os.path.join(outputFolder, "edges_separate=%s" % allRegionsSeparate))
    if 0: print edgeVolumePath
    if 0: writeStack(edgeVolumePath, resultEdgeVolume)


    #makeDirector("/tmp/out")
    #filename = "/tmp/out/out%d_%d_%d.raw" % resultVolume.shape
    #writeRaw(filename, resultVolume)


    # write open cv images for file
    #for z in range(imageVolume.shape[2]):
    for z in range(zStart, zStop):

        if allRegionsSeparate:
            separate = "_sep"
        else:
            separate = ""

        fullFilename = os.path.join(folder, "render_graph_%04d%s.png" % (z, separate))
        print fullFilename
        cv.SaveImage(fullFilename, openCVImages[z])



def renderAllRegions_depricated(imageVolume, regions):

    openCVImages = {}

    # create open cv images
    for z in range(imageVolume.shape[2]):
        #todo: just use blanks for this
        openCVImages[z] = toOpenCV(imageVolume[:, :, z], color=True)


    count = 0

    for key in regions:

        print "region:", count, "    total number:", len(regions)
        count += 1

        region = regions[key]
        color = (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))

        z = region.z
        for point in region:
            backgroundValue = imageVolume[point[0], point[1], z]
            blendedColor = [int((backgroundValue+color[0])/2), int((backgroundValue+color[1])/2), int((backgroundValue+color[2])/2), 0]
            center = array(point)
            cv.Circle(openCVImages[z], (center[0] * scaleFactor, center[1] * scaleFactor), scaleFactor, blendedColor, thickness=-1)


    # write open cv images for file
    for z in range(imageVolume.shape[2]):

        tag = "_all"

        fullFilename = os.path.join(outputFolder, "render_graph_%04d%s.bmp" % (z, tag))
        print fullFilename
        cv.SaveImage(fullFilename, openCVImages[z])


def getCursorForRegions():

    conn = sqlite3.connect(os.path.join(dataOutputFolder, 'dseg.db'))
    c = conn.cursor()
    c.execute('SELECT * FROM regions')
    return c


def fetchRegion(c):

    fetchResult = c.fetchone()
    if fetchResult == None: return None
    z, number, regionBlob, primaryKey = fetchResult
    region = cPickle.loads(binascii.unhexlify(regionBlob))
    return z, number, region





def renderAllRegions(imageVolume, scaleFactorForRendering):

    print "render all regions in database"

    openCVImages = {}

    numImages = imageVolume.shape[2]

    zStart, zStop = getStartAndStop(startSlice, stopSlice, numImages)

    # create open cv images
    for z in range(zStart, zStop):
        print "convert to opencv"
        print z
        #todo: just use blanks for this
        openCVImages[z] = toOpenCV_old(imageVolume[:, :, z], color=True)


    count = 0

    #for key in regions:
    conn = sqlite3.connect(os.path.join(dataOutputFolder, 'dseg.db'))
    c = conn.cursor()


    #while True:

    for index in range(zStart, zStop):

        print "index:", index
        c.execute('SELECT * FROM regions WHERE z=%d' % index)

        # read region on this plane
        while True:

            #print "region:", count, "    total number:", len(regions)
            print count
            count += 1
    
            fetchResult = c.fetchone()
            #print fetchResult
            if fetchResult == None: break
            (z, number, regionBlob, primaryKey) = fetchResult
            print "region number:", number
            print "z:", z
            region = cPickle.loads(binascii.unhexlify(regionBlob))
            
    
            #region = regions[key]
            color = (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))
    
            z = region.z
            for point in region:
                backgroundValue = imageVolume[point[0], point[1], z]
                blendedColor = [int((backgroundValue+color[0])/2), int((backgroundValue+color[1])/2), int((backgroundValue+color[2])/2), 0]
                #blendedColor = number
                center = array(point)
                cv.Circle(openCVImages[z],
                 (center[0] * scaleFactorForRendering,
                  center[1] * scaleFactorForRendering),
                 #(center[1] * scaleFactorForRendering,
                 # center[0] * scaleFactorForRendering),
                  scaleFactorForRendering,
                  blendedColor,
                  thickness=-1)


        # write open cv images for file
        for z in range(zStart, zStop):
    
            tag = "_all"
    
            fullFilename = os.path.join(outputFolder, "render_graph_%04d%s.bmp" % (z, tag))
            print fullFilename
            cv.SaveImage(fullFilename, openCVImages[z])



    conn.close()




# render the results from mechanical turk
#todo: simplify this
#todo: put this in its own file
def render_old(edges, edgeExistsAnswer='Yes'):

    reader = csv.reader(open(r'c:\users\user\downloads\Batch_791128_batch_results.csv', 'rb'), delimiter=',', quotechar='"')

    answers = {}


    # collect answers into a dictionary
    for i, row in enumerate(reader):

        # find accept field index
        if i == 0:
            for fieldIndex, field in enumerate(row):
                if field == 'Answer.edge_correct':
                    acceptIndex = fieldIndex
                if field == 'Input.image1':
                    image1Index = fieldIndex
            print "accept:", row[acceptIndex]
            print "image1:", row[image1Index]
        else:
            result = re.match(r".*crop_(.*)_(.*)\.jpg", row[image1Index])
            region1 = int(result.group(1))
            region2 = int(result.group(2))
            answers[(region1, region2)] = row[acceptIndex]


    #openCVImage = cv.CreateImage((s[0], s[1]), 8, 3)

    openCVImage = toOpenCV(v[:, :, 3], color=True)


    for key in edges:
    
        edge = edges[key]
        b1 = array(boundingBox(edge))

        visible = False
        if key in answers:
            if answers[key] == edgeExistsAnswer:
                color = (255, 0, 0, 0)
                visible = True
            else:
                color = (0, 255, 0, 0)
                visible = True
        else:
            color = (0, 0, 255)

        if visible:
            for point in edge:
                #print "------------------------"
                #print "point", point
                center = array(point)
                #print "center", center
    
                #todo: write all of these into one image if they are approved
                cv.Circle(openCVImage, (center[1] * scaleFactor, center[0] * scaleFactor), scaleFactor, color, thickness=-1)


        #for index in key:
        #    print index,
        #print

    fullFilename = r"o:\temp\output\all.bmp"
        #fileList.append(filename)

    print fullFilename
    cv.SaveImage(fullFilename, openCVImage)


#def addMTurkResultsToGraph(allRegions, csvFilename):
def addMTurkResultsToGraph(gr, csvFilename, suffix, limits):

    #reader = csv.reader(open(r"c:\users\user\downloads\Batch_791128_batch_results.csv", 'rb'), delimiter=',', quotechar='"')
    #reader = csv.reader(open("/home/rgiuly/Downloads/Batch_791128_batch_results.csv", 'rb'), delimiter=',', quotechar='"')
    reader = csv.reader(open(csvFilename, 'rb'), delimiter=',', quotechar='"')

    weights = {}

    #gr = graph()

    #for regionKey in allRegions.keys():
    #    gr.add_node(regionKey)

    # collect answers into a dictionary
    for i, row in enumerate(reader):

        # find accept field index
        if i == 0:

            for fieldIndex, field in enumerate(row):
                print "field", field
                if field == 'Answer.same_object':
                    acceptIndex = fieldIndex
                if field == 'Input.image1':
                    image1Index = fieldIndex
            print "accept:", row[acceptIndex]
            print "image1:", row[image1Index]

        else:

            print "row[acceptIndex]", row[acceptIndex]

            # get region id's out of the filename
            print "suffix", suffix
            print "row[image1Index]", row[image1Index]
            result = re.match(r".*crop_(.*)_(.*)_(.*)_(.*)" + suffix, row[image1Index])
            z0 = int(result.group(1))
            region0 = int(result.group(2))
            z1 = int(result.group(3))
            region1 = int(result.group(4))

            id0 = makeRegionIdentifier(z0, region0)
            id1 = makeRegionIdentifier(z1, region1)


            renderNonYesNodes = False

            if row[acceptIndex] == "Yes" or renderNonYesNodes:

                if not(gr.has_node(id0)):
                    gr.add_node(id0)

                if not(gr.has_node(id1)):
                    gr.add_node(id1)

            if row[acceptIndex] == "Yes":
                # add edge

                # if it's in the limits
                if limits == None or (z0 >= limits[0] and z0 <= limits[1]) or (z1 >= limits[0] and z1 <= limits[1]):

                    #print "z0 region0:", z0, region0
                    #print "z1 region1:", z1, region1
                    #print "makeRegionIdentifier(z0, region0)", makeRegionIdentifier(z0, region0)
                    #print "makeRegionIdentifier(z1, region1)", makeRegionIdentifier(z1, region1)
    
                    edge = (id0, id1)
                    #if not(gr.has_edge(edge)):
                    #    gr.add_edge(edge)
    
                    if edge in weights:
                        weights[edge] += 1
                    else:
                        weights[edge] = 1


    for edge in weights:
        # if weight is great enough, add edge
        if weights[edge] >= 1:
            if not(gr.has_edge(edge)):
                gr.add_edge(edge)

    return gr





#def addSCIResultsToGraph(gr, filePath):
#
#    file = open(filePath, 'r')




#def makePlaneToPlaneExample(number, imageUrl, answer):
#
#    text = "Does the dot stay inside the same cell? (The dot has to stay strictly inside. The answer is no if the dot touches a cell border.)"
#    return makeExample(number, text, imageUrl, answer)


def makeInPlaneExample(number, imageUrl, answer):

    text = "Are the dots both inside the same cell? (They have to both be inside, on the border doesn't count.)"
    return makeExample(number, text, imageUrl, answer)


def makeExample(number, text, imageUrl, answer):

    return """
                  <FormattedContent><![CDATA[
                    <h3>Example %(number)d. %(text)s</h3>
                    ]]></FormattedContent>
                  <Binary>
                    <MimeType>
                      <Type>image</Type>
                      <SubType>jpg</SubType>
                    </MimeType>
                    <DataURL>%(imageUrl)s</DataURL>
                    <AltText>Image</AltText>
                  </Binary>
                  <FormattedContent><![CDATA[
                    <h2>%(answer)s</h2>
                    ]]></FormattedContent>
                  <Text>
                  ____________________________________________________________
                  </Text>
                    """\
                    % {'number':number, 'text':text, 'imageUrl':imageUrl, 'answer':answer}
                    #% {'number':number, 'text':text, 'imageUrl':imageUrl, 'answer':answer.title()}


def makeQuestion(number, imageUrl, text):

    return """<Question>
        <QuestionIdentifier>%(number)d</QuestionIdentifier>
        <QuestionContent>
              <FormattedContent><![CDATA[
                <h3>Question %(number)d. %(text)s</h3>
                ]]></FormattedContent>
                  <Binary>
                    <MimeType>
                      <Type>image</Type>
                      <SubType>jpg</SubType>
                    </MimeType>
                    <DataURL>%(imageUrl)s</DataURL>
                    <AltText>Image</AltText>
                </Binary>
        </QuestionContent>
        <AnswerSpecification>
            <SelectionAnswer>
              <StyleSuggestion>radiobutton</StyleSuggestion>
              <Selections>
                <Selection>
                  <SelectionIdentifier>%(number)dYes</SelectionIdentifier>
                  <Text>Yes</Text>
                </Selection>
                <Selection>
                  <SelectionIdentifier>%(number)dNo</SelectionIdentifier>
                  <Text>No</Text>
                </Selection>
              </Selections>
            </SelectionAnswer>
        </AnswerSpecification>
    </Question>
""" % {'number':number, 'imageUrl':imageUrl, 'text':text}


def makeInPlaneQuestion(number, imageUrl):

    text = "Are the dots both inside the same cell? (They have to both be inside, on the border doesn't count.)"
    return makeQuestion(number, imageUrl, text)


#def makePlaneToPlaneQuestion(number, imageUrl):
#
#    text = "Does the dot stay inside the cell? (The dot has to stay inside, on the border doesn't count.)"
#    return makeQuestion(number, imageUrl, text)


def makeAnswer(number, answer):

    return """
             <Question>
              <QuestionIdentifier>%(number)d</QuestionIdentifier>
              <AnswerOption>
               <SelectionIdentifier>%(number)d%(answer)s</SelectionIdentifier>
               <AnswerScore>1</AnswerScore> 
              </AnswerOption>
             </Question>
           """\
           % {'number':number, 'answer':answer}
           #% {'number':number, 'answer':answer.title()}


def makeLabelVolumeSLIC(imageVolume):

    s = imageVolume.shape
    labelVolume = zeros(s)

    for i in range(imageVolume.shape[2]):
        #(edges, regions, cvImage, tempImage, imageLabels) = processXYSlice_old(imageVolume[:, :, i])
        (edges, regions, cvImage, tempImage, imageLabels) = processXYSlice_old(imageVolume[:, :, i], i)
        print "labelVolume[:, :, i].shape", labelVolume[:, :, i].shape
        print "imageLabels.shape", imageLabels.shape
        labelVolume[:, :, i] = transpose(imageLabels)

    return labelVolume


def makeLabelVolumeWatershed_depricated(imageVolume):

    s = imageVolume.shape
    labelVolume = zeros(s)

    for i in range(imageVolume.shape[2]):
        print "labelVolume[:, :, i].shape", labelVolume[:, :, i].shape
        #labelVolume[:, :, i] = watershed2DNumpy(imageVolume[:, :, i], 0.00015, 0.25, useGradientMagnitude=False)
        labelVolume[:, :, i] = watershed2DNumpy(imageVolume[:, :, i], 0.00015, 0.35, useGradientMagnitude=False)

    return labelVolume



def makeLabelVolumeStackWatershed(inputFolder, outputFolder):

    print "watershed"

    if args.threshold:
        threshold = float(args.threshold)
    else:
        threshold = 0.00015

    if args.level:
        level = float(args.level)
    else:
        level = 0.35

    processImageStack(inputFolder,
                      outputFolder,
                      watershed2DNumpy,
                      (startSlice, stopSlice),
                      {'threshold':threshold, 'level':level, 'useGradientMagnitude':False})


# Execute the function f on the files in the input folder,
# and place output files in the output filder.
def processImageStack(inputFolder, outputFolder, f, bounds, arguments):

    makeClearDirectory(outputFolder)

    #fileList = os.listdir(inputFolder)
    #fileList.sort()
    #for filename in fileList:
    for i in range(bounds[0], bounds[1]):

        filename = "output%03d.png" % i
        #fullFilename = path.join(inputFolder, filename)
        #(path, filename) = os.path.split(fullFilename)
        inputFilename = os.path.join(inputFolder, filename)
        input = scipy.misc.imread(inputFilename)
        #output = watershed2DNumpy(input, 0.00015, 0.35, useGradientMagnitude=False)
        arguments['array'] = input
        print "arguments:", arguments
        output = f(**arguments)
        base, extension = os.path.splitext(filename)
        outputFilenamePickle = os.path.join(outputFolder, base + ".pickle")
        outputFilenamePNG = os.path.join(outputFolder, base + ".png")
        print "input file:", inputFilename
        print "output file:", outputFilenamePickle
        print "output file:", outputFilenamePNG
        print "png file is just for viewing. it will not have required bit depth to preserve all labels."
        #print "minimum label value:", min(output)
        #print "maximum label value:", max(output)
        print "writing"
        scipy.misc.imsave(outputFilenamePNG, output)
        outputFile = open(outputFilenamePickle, 'wb')
        cPickle.dump(output, outputFile)
        outputFile.close()
        print "finished writing"


#makeClearDirectory(gaussianOutputFolder)
#processImageStack(originalOutputFolder,
#                  gaussianOutputFolder,
#                  gaussian2DNumpy,
#                  (startSlice, stopSlice),
#                  {'sigma':float(args.sigma)})



def makeEdgeVolume(labelVolume):

    resultVolume = ones(labelVolume.shape) * 255

    for zIndex in range(labelVolume.shape[2]):

        edges = getEdges2D(labelVolume[:, :, zIndex], zIndex)

        for edge in edges.values():
            for point in edge:
                resultVolume[point[0], point[1], zIndex] = 0

    return resultVolume


def testReadRawFile():

    #s = [700, 700]
    #filename = "/home/rgiuly/images/overseg/init200.raw"
    #labelImage = readRawFile(filename, (s[1], s[0]))
    #fullFilename = os.path.join(outputFolder, "ting.bmp")
    #print fullFilename
    #cv.SaveImage(fullFilename, toOpenCV(labelImage))

    print "read stack"
    path = "/home/rgiuly/images/overseg/"
    #labels = loadRawStack(path, Box((0,0,0), (500, 600, 10)))
    labels = loadRawStack(path, box, swapXY=True, flipLR=True)
    print "write stack"
    writeStack(os.path.join(outputFolder, "seg_stack"), labels)


# returns (edges, regions, cvImage, tempImage, labelImage)
def processXYSlice_old(array2D, zIndex):

    tempImage = toOpenCV(array2D, color=True)
    tempFilename = os.path.join(outputFolder, 'test.bmp')
    cv.SaveImage(tempFilename, tempImage)
    tempOutFilename = os.path.join(outputFolder, "slic_")
    
    
    print "tempOutFilename", tempOutFilename
    slic = r"SLIC_Windows_commandline\SLICSuperpixelSegmentation.exe"
    #os.system("%s %s 10 1200 %s" % (slic, tempFilename, tempOutFilename))
    result = os.system("%s %s 10 300 %s" % (slic, tempFilename, tempOutFilename))
    print "result from SLIC command line", result

    # slic probably creates a file by this name
    filename = tempOutFilename + "test.dat"
    
    #f = open(tempOutFilename + "test.dat", 'rb')
    
    #f = open(r"o:\temp\1.tmp", 'rb')
    #print tempOutFilename + "test.dat"
    #print "file size", os.path.getsize(r"o:\temp\1.tmp")
    #string = f.read()
    
    #print len(string)
    
    #for i in xrange(0,1000000000,1):
        #string = f.read(1)
        #print tempOutFilename + "test.dat"
        #print i, len(s)#unpack('<L', string)
    
    #sys.exit()
    
    #byte = f.read(1)
    
    
    
    labelImage = readRawFile(filename, (v.shape[1], v.shape[0]))
    
    #cvImage = toOpenCV(image, color=True)
    cvImage = tempImage
    
    
    
    # draw all edges
    edges = getEdges2D(labelImage, zIndex)
    regions = getRegions2D(labelImage, zIndex)

    # draw translucent green edges
    if 1:
        for key in edges:
            #color = (255, 0, 0, 0)
            for point in edges[key]:
                #cv.Circle(cvImage, point, 1, color)
                #if point[0] >= 0 and point[0] < cvImage.width and point[1] >= 0 and point[1] < cvImage.height:
                if 1:
                    background = cvImage[point[0], point[1]]
                else:
                    background = (0, 0, 0)
                color = (background[0], (background[1] + 255) / 2, background[2], 0)
                #print point, color
                cv.Circle(cvImage, (point[1], point[0]), 0, color)
    
    print "saving image"
    cv.SaveImage(r"o:\temp\output\edge_out.bmp", cvImage)
    cv.SaveImage(r"o:\temp\output\original_out.bmp", toOpenCV(labelImage))
    cv.SaveImage(r"o:\temp\output\test_out.bmp", toOpenCV(v[:, :, 1], color=True))
    #cropped = crop(image,10,20,140,160)
    #cv.SaveImage(r"o:\temp\output\crop.bmp", toOpenCV(cropped, color=True))
    
    
    #print "edges.keys()", edges.keys()

    return (edges, regions, cvImage, tempImage, labelImage)




#(useEdges=False, useCenterPoints=True)
#render(edges, edgeExistsAnswer='No')


storageForRegionToContours = cv.CreateMemStorage(0)



def contourIterator(contour):

    while contour:
        yield contour
        contour = contour.h_next() 


def drawRegionsTest(regions):

    print "number of regions", len(regions)

    contours_image = cv.CreateImage((700, 700), cv.IPL_DEPTH_8U, 3)
    cv.SetZero(contours_image)


    for region in regions.values():

        #print "region", region

        contours = regionToContours(region)

        _red =  (0, 0, 255, 0);
        _green =  (0, 255, 0, 0);
    
        cv.DrawContours(contours_image, contours,
                        _red, _green,
                        1, 1, cv.CV_AA,
                        (0, 0))
    
    
        current = contours
        while(current):
            #print "contour"
            #for (x, y) in current:
            #    print (x, y),
            print
            current = current.h_next()
    
    print r"i:\temp\out_image.jpg"
    cv.SaveImage(r"i:\temp\out_image.jpg", contours_image)



def sendRegionsAsContours(regions):

    idInformation = access_database.initializeSendContour()

    print "number of regions", len(regions)
    for region in regions.values():
        #print "region", region
        contours = regionToContours(storageForRegionToContours, region)
        current = contours
        while(current):
            # send contour to spatial database
            #print "contour"
            #for (x, y) in current:
            #    print (x, y),
            #print
            #sendContour(current, 0)
            access_database.sendContour(region.z, current)
            current = current.h_next()

    print idInformation
    print "http://ccdb-dev-portal.crbs.ucsd.edu/WebImageBrowser/index.html?plugin=SLASH&user=rgiuly&datasetID=%d&modelID=%d" %  (idInformation['dataset_id'], idInformation['model_number'])

#todo: this is not tested
#def submitHITs(fileList):
#
#    for filename in fileList:
#        access_aws.submitHIT(filename)



if args.xyqual or args.zqual or args.splitqual:
    writeGlobalPropertiesFile(os.path.join("aws-mturk-clt-1.3.0", "bin", "mturk.properties"), args.access_key, args.secret_key)


# make tiles for determining if superpixel should be connected
# to adjacent superpixel
if args.xyqual or args.xyprocess:
    if not(args.skip_tiles):
        csvFilename = os.path.join(outputFolder, "images_in_plane.csv")
        makeTilesInPlane(csvFilename, useEdges=False, useCenterPoints=True)
        copyTilesToAmazonS3(os.path.join(tileFolder, "in_plane"))
        print "finished creating and uploading in plane tiles"
        print "file to upload to Amazon Mechanical Turk:", csvFilename
if args.xyqual:
    propertiesFile = os.path.join(mturkScriptFolder, "in_plane", "qualification.properties")
    print "properties", propertiesFile
    writePropertiesFile(propertiesFile, "Cell", "Are dots inside the same cell")
    os.system("cd " + os.path.join(mturkScriptFolder, "in_plane") + ";" + "./run.sh")




def runCSVProcess_old():

    # make all tiles if you are using CSV file method
    csvFilename = os.path.join(outputFolder, "images_plane_to_plane.csv")
    makeTilesPlaneToPlane(csvFilename, useEdges=False, useCenterPoints=True, oversegSource=oversegSourceForQualAndProcessAndRender)

    # make qualification test if it's specified
    if makeQualifications:
        makeQualificationsFile(fileList)
    else:
        makeProcessCSVFile(fileList)

    copyTilesToAmazonS3(os.path.join(tileFolder, "plane_to_plane"))
    print "finished creating and uploading plane to plane tiles"
    print "file to upload to Amazon Mechanical Turk:", csvFilename



def makeZQual():

    print "make z qual"

    print "Writing template file with all \"no\" that you can use as a starting point. You'll need to set where the \"yes\"'s are manually."
    filePath = os.path.join(outputFolder, "answers%d.txt" % (int(time.time()) % 10000))
    print filePath
    file = open(filePath, 'w')

    zEdgesFile = open(os.path.join(dataOutputFolder, "zEdges.pickle"), 'rb')
    zEdges = cPickle.load(zEdgesFile)
    zEdgesFile.close()

    #print "zEdges", zEdges

    useCenterPoints = True


    imageFileList = []

    #edgeIndex = 0
    edges = zEdges.keys()
    #for edge in zEdges.keys():
    numExampleImages = 50
    for i in range(numExampleImages):

        print i, "number:", numExampleImages
        random.seed(i)
        edgeIndex = random.randint(len(zEdges))
        file.write("%d no\n" % i)
        edge = edges[edgeIndex]
        print "edge", edge
        (success, filename) = makeZDecisionImage(edge, useCenterPoints, baseFilename="qual_%03d"%edgeIndex)
        #(success, filename) = makeZDecisionImage2(gr, edge, useCenterPoints)
        #uploadFileToAmazonS3(addAnimationSuffix(filename) + ".gif", 'plane_to_plane')
        #edgeIndex += 1

        imageFileList.append(filename)

    file.close()
    print filePath


    #todo: seems this doesn't upload all files. looks like just one?
    access_aws.uploadFileToAmazonS3(
        os.path.join(tileFolder, 'plane_to_plane', addAnimationSuffix(filename) + ".gif"),
        dataName,
        'data/plane_to_plane',
        addAnimationSuffix(filename) + ".gif",
        args.access_key,
        args.secret_key)


    # make all tiles if you are using CSV file method
    csvFilename = os.path.join(outputFolder, "images_plane_to_plane.csv")
    #makeTilesPlaneToPlane(csvFilename, useEdges=False, useCenterPoints=True, oversegSource=oversegSourceForQualAndProcessAndRender)

    # make qualification test if it's specified
    makeQualificationsFile(imageFileList, range(0, 24+1), range(25, 49+1), "Does the dot stay inside the same cell? (The dot has to stay strictly inside. The answer is no if the dot touches a cell border.)", 'plane_to_plane')


    copyTilesToAmazonS3(os.path.join(tileFolder, "plane_to_plane"))
    print "finished creating and uploading plane to plane tiles"
    print "file to upload to Amazon Mechanical Turk:", csvFilename







def makeSplitQual():

    print "make split qual"

    #print "Writing template file with all \"no\" that you can use as a starting point. You'll need to set where the \"yes\"'s are manually."
    #filePath = os.path.join(outputFolder, "split_answers%d.txt" % (int(time.time()) % 10000))
    #print filePath

    template = os.path.join(dataOutputFolder, "tiles", "regions", "*.jpg")
    print "template", template

    if useOnlyRegionsPeopleThoughtWereTouchingTwoCells:
        imageFileList = ["region_%s.jpg" % regionID for regionID in touchMoreThanOne()]
    else:
        imageFileList = [os.path.basename(p) for p in glob.glob(template)]


    print "image file list", imageFileList

    #todo: is this needed?
    #access_aws.uploadFileToAmazonS3(
    #    os.path.join(tileFolder, 'plane_to_plane', addAnimationSuffix(filename) + ".gif"),
    #    dataName,
    #    'data/plane_to_plane',
    #    addAnimationSuffix(filename) + ".gif",
    #    args.access_key,
    #    args.secret_key)


    # make qualification test if it's specified
    print "number of files:", len(imageFileList)
    #makeQualificationsFile(imageFileList, (0, 5, 2, 4, 1), (14, 16, 8, 9, 11, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40), "Does blue highlight more than one cell?", 'regions')
    makeQualificationsFile(imageFileList,
                           range(0,11),
                           range(11,22),
                           "Does blue highlight more than one cell?",
                           'regions')

    print "copy tiles to amazon s3"
    copyTilesToAmazonS3(os.path.join(dataOutputFolder, "tiles", "regions"))
    print "finished creating and uploading plane to plane tiles"
    #print "file to upload to Amazon Mechanical Turk:", csvFilename







# make tiles for determining if superpixel should be connected
# to superpizel that's above it
print "----------------------------------------------"
#if args.zqual or args.zprocess:
if args.zprocess:
    #if args.zqual: print "processing zqual"
    if args.zprocess: print "processing zprocess"
    if initSegFromPrecomputedStack:
        inputFileExtension = "mha"
    else:
        inputFileExtension = "pickle"
    if not(args.skip_tiles):
        if args.submit:
            if 0 or args.init: initializeVolumes()
            if 0 or args.init: initializeZEdges()
            if 0 or args.init: makeAllRegions(initialSegFolder, inputFileExtension=inputFileExtension)
            if 0 or args.init: renderAllRegions(loadImageStack(inputStack, None), 1)
            if 0 or args.init or args.restart: initializeRequestLoop()
            requestLoop()
        else:
            runCSVProcess_old()



if args.splitqual:

    if not args.answers:
        print "prompt"
        promptSplitQualAnswers()

    else:

        makeSplitQual()
        propertiesFile = os.path.join(mturkScriptFolder, "plane_to_plane", "qualification.properties")
        print "properties", propertiesFile
        writePropertiesFile(propertiesFile, "Region", "Does blue highlight more than one cell")
        command = "cd " + os.path.join(mturkScriptFolder, "plane_to_plane") + ";" + "./run.sh"
        print command
        os.system(command)



if args.zqual:
    makeZQual()
    propertiesFile = os.path.join(mturkScriptFolder, "plane_to_plane", "qualification.properties")
    print "properties", propertiesFile
    writePropertiesFile(propertiesFile, "Cell", "Does the dot stay in one cell")
    #os.system("echo $JAVA_HOME")
    command = "cd " + os.path.join(mturkScriptFolder, "plane_to_plane") + ";" + "./run.sh"
    print command
    os.system(command)

# render graph
if args.xyrender or args.zrender:
    scaleFactor = 1 #todo: this would be better as a parameter rather than just a global variable
    #labelVolume = makeLabelVolume(v, "file")
    labelVolume = makeLabelVolume(v, oversegSourceForQualAndProcessAndRender)
    allRegions = getAllRegions(labelVolume)
    print "number of regions", len(allRegions)
    #sys.exit()
    #gr = graph()
    #for key in allRegions:
    #    gr.add_node(key)
    #edge = (allRegions.keys()[100], allRegions.keys()[101])
    #print "edge", edge
    #gr.add_edge(edge)
    #gr = mturkToGraph(allRegions, "/home/rgiuly/Downloads/Batch_821341_batch_results.csv")

    gr = graph()
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_822213_batch_results.csv", r"\.jpg")
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_863623_batch_results.csv", r"_animation\.gif")
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_870142_batch_results.csv", r"_animation\.gif")

    # Christine's data
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_879262_batch_results.csv", r"_animation\.gif") # incomplete job on mturk
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_880322_batch_results.csv", r"_animation\.gif") # incomplete job on mturk
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_885916_batch_results.csv", r"_animation\.gif")
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_886583_batch_results.csv", r"_animation\.gif")
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_892496_batch_results.csv", r"_animation\.gif")
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_901613_batch_results.csv", r"_animation\.gif")
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_902441_batch_results.csv", r"_animation\.gif")
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_903246_batch_results.csv", r"_animation\.gif")
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_908647_batch_results.csv", r"_animation\.gif") # test run
    #gr = addMTurkResultsToGraph(gr, "/home/rgiuly/Downloads/Batch_911615_batch_results.csv", r"_animation\.gif") # test run

    if args.xyrender:
        for csvPath in args.xyrender:
            print "reading", csvPath
            gr = addMTurkResultsToGraph(gr, csvPath, r"\.jpg")

    if args.zrender:
        for csvPath in args.zrender:
            print "reading", csvPath
            #if args.use_sci:
            if 0:
                gr = addSCIResultsToGraph(gr, filePath)
            else:
                #gr = addMTurkResultsToGraph(gr, csvPath, r"_animation\.gif", None) # limited
                gr = addMTurkResultsToGraph(gr, csvPath, r"_animation\.gif", (0, 3)) # limited

    print "graph edges", gr.edges()
    renderAllRegionsToFile = True
    if renderAllRegionsToFile:
        print "render all regions"
        renderAllRegions(v, allRegions)

    print "render graph, all regions"
    renderGraph(outputFolder, v, allRegions, gr, allRegionsSeparate=True)

    compositeOutputFolder = os.path.join(outputFolder, "composite")
    makeDirectory(compositeOutputFolder)

    #removeBigDarkNodes(gr, v, allRegions)
    print "render graph"
    renderGraph(outputFolder, v, allRegions, gr, allRegionsSeparate=False)
    renderGraph(compositeOutputFolder, v, allRegions, gr, allRegionsSeparate=False)
    print "render graph without background"
    segFolder = os.path.join(outputFolder, "seg")
    if not(os.path.isdir(segFolder)):
        os.mkdir(segFolder)
    renderGraph(segFolder, v, allRegions, gr, allRegionsSeparate=False, showBackgroundImage=False)


if args.print_regions:

    labelVolume = makeLabelVolume(v, oversegSourceForQualAndProcessAndRender)
    allRegions = getAllRegions(labelVolume)
    zEdges = getZEdges(labelVolume)
    regionsFile = open(os.path.join(outputFolder, "regions.txt"), 'w')
    regionsFile.write(str(allRegions))
    regionsFile.close()
    edgesFile = open(os.path.join(outputFolder, "adj.txt"), 'w')
    edgesFile.write(str(zEdges))
    edgesFile.close()



def sendRegionsToDatabase():

    #labelVolume = makeLabelVolume(v, oversegSourceForQualAndProcessAndRender)
    #allRegions = getAllRegions(labelVolume)
    #drawRegionsTest(allRegions)
    #sendRegionsAsContours(allRegions)

    conn = sqlite3.connect(os.path.join(dataOutputFolder, 'dseg.db'))
    cur = conn.cursor()

    filename = os.path.join(outputFolder, "request_loop_data")
    file = open(filename, 'rb')
    dict = cPickle.load(file)
    gr = dict['gr']

    regionsInGraph, componentsDict, colorMap, nodeCount = processRenderingGraph(gr, True)

    regionDict = {}
    for id in regionsInGraph:
        regionDict[id] = getRegionByID(cur, id)
        #print "region", regionDict[id]
        #break

    sendRegionsAsContours(regionDict)

    file.close()




if args.send_regions_to_database:
    sendRegionsToDatabase()
























HITText = """<h2>Does the dot stay inside of the cell? (Note: If the dot goes on the border between cells, the answer is No.)</h2>
<h3>&nbsp;&nbsp;</h3>
<p><input type="radio" name="same_object" value="Yes" /> Yes</p>
<p><input type="radio" name="same_object" value="No" /> No</p>
<p><img alt="image1" style="margin-right: 30px;" src="${image%d}" /></p>"""

hitLayoutFile = open("hit.html", 'w')
print
print
print "hit.html"
hitLayoutFile.write(HITText % 1)
hitLayoutFile.write(HITText % 2)
hitLayoutFile.close()

#testReadRawFile()



